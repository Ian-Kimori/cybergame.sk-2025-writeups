# SPDX-License-Identifier: CC0-1.0
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

import os

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

# this is my estimate made in Photoshop, manually measured a few squares horizontally and vertically and
# divided by the number of squares measured
MOSAIC_SIZE = (112 / 13, 190 / 22)

MOSAIC_SQUARE_SIZE = 9
MAGIC_VAL = 15

# ChatGPT came up with a different algorithm to fill the holes between pixels,
# read more here: https://github.com/KoKuToru/de-pixelate_gaV-O6NPWrI
GPT_FILL = True


def load_png_frames(frames_folder, sample_only: bool = False):
    count = 0
    for filename in sorted(os.listdir(frames_folder)):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(frames_folder, filename)
            try:
                image = Image.open(filepath)
                image = image.convert("RGBA")
                transform = transforms.ToTensor()
                img = transform(image).mul(0xFF).to(torch.uint8)
                count += 1
                if sample_only:
                    if count > 10:
                        return
                yield filename, img
            except Exception as e:
                print(f"Error processing {filename}: {e}")


# GPT's method to "fill the holes" between pixels in a different way - see the bottom of this file
def fill_holes(img: torch.Tensor, max_iter: int = 25) -> torch.Tensor:
    """
    Diffusion‑based in‑painting that fills every pixel whose alpha channel is
    zero.  It repeatedly averages 3×3 neighborhoods (Jacobi relaxation) until
    no holes remain or `max_iter` iterations have elapsed.

    Args:
        img: Tensor shaped (4, H, W) in premultiplied RGBA.
        max_iter: Maximum number of diffusion passes.

    Returns:
        A *float32* tensor with the same shape as `img`, where all alpha‑zero
        pixels have been in‑painted.
    """
    work = img.float().clone()  # ensure float for maths
    kernel = torch.ones(1, 1, 3, 3, device=work.device)

    missing = (work[3:4] == 0)
    if not torch.any(missing):
        return work

    for _ in range(max_iter):
        if not torch.any(missing):
            break

        valid = (~missing).float()
        weight = F.conv2d(valid, kernel, padding=1)

        # sum of neighbours, computed per‑channel via grouped convolution
        nbr_sum = F.conv2d(
            work.unsqueeze(0),  # (1, 4, H, W)
            kernel.repeat(4, 1, 1, 1),  # (4, 1, 3, 3)
            padding=1,
            groups=4
        )[0]

        filled_vals = nbr_sum / weight.clamp(min=1e-3)
        work = torch.where(missing.expand_as(work), filled_vals, work)
        missing = (work[3:4] == 0)

    return work


transform = transforms.ToPILImage()

os.makedirs('mosaics', exist_ok=True)
os.makedirs('accumulated', exist_ok=True)

gframe = None
for name, frame in load_png_frames('windows', sample_only=False):
    print(f'Processing {name}...')
    # find mosaic position (this takes lots of memory.. not optimized.. just casting to bytes sometimes.. very slow..)
    hframe = frame.float().mean(-1, keepdim=True)
    vframe = frame.float().mean(-2, keepdim=True)
    mframe = (hframe.expand_as(frame) + vframe.expand_as(frame)).div(2)
    hframe2 = (mframe[:, :-1, :-1] - mframe[:, 1:, :-1]).abs().mean(0, keepdim=True)
    vframe2 = (mframe[:, :-1, :-1] - mframe[:, :-1, 1:]).abs().mean(0, keepdim=True)
    hframe2 = hframe2 > MAGIC_VAL
    vframe2 = vframe2 > MAGIC_VAL
    # get x,y position
    for y in range(MOSAIC_SQUARE_SIZE, vframe2.size(-2) - MOSAIC_SQUARE_SIZE):
        if hframe2[0, y, MOSAIC_SQUARE_SIZE * 2]:
            break
    for x in range(MOSAIC_SQUARE_SIZE, vframe2.size(-1) - MOSAIC_SQUARE_SIZE):
        if vframe2[0, MOSAIC_SQUARE_SIZE * 2, x]:
            break
    mosaic_y = int(y + 1)
    mosaic_x = int(x + 1)
    while mosaic_y - MOSAIC_SIZE[-2] > 0:
        mosaic_y -= MOSAIC_SIZE[-2]
    while mosaic_x - MOSAIC_SIZE[-1] > 0:
        mosaic_x -= MOSAIC_SIZE[-1]
    print(f"{name} Mosaic offset found at (x={mosaic_x}, y={mosaic_y})")
    mframe2 = hframe2 | vframe2
    mframe2 = F.pad(mframe2, (0, 1, 1, 0))
    mframe = mframe.to(torch.uint8)
    mframe2[:, :MOSAIC_SQUARE_SIZE] = 0
    mframe2[:, -MOSAIC_SQUARE_SIZE:] = 0
    mframe2[:, :, :MOSAIC_SQUARE_SIZE] = 0
    mframe2[:, :, -MOSAIC_SQUARE_SIZE:] = 0
    # print(mframe2.size(), mframe.size(), frame.size())
    mframe = torch.where(mframe2.expand_as(mframe),
                         torch.tensor((0, 0, 0xFF, 0xFF), dtype=torch.uint8).view(4, 1, 1).expand_as(mframe), frame)
    mask = torch.zeros_like(frame, dtype=float)
    y = mosaic_y + MOSAIC_SIZE[-2] / 2
    while y < hframe2.size(-2):
        x = mosaic_x + MOSAIC_SIZE[-1] / 2
        while x < vframe2.size(-1):
            x_int = int(x)
            y_int = int(y)
            mask[:, y_int, x_int] = 1
            mframe[0, y_int, x_int] = 0
            mframe[1, y_int, x_int] = 0xFF
            mframe[0, y_int, x_int] = 0
            mframe[1, y_int, x_int] = 0xFF

            x += MOSAIC_SIZE[-1]
        y += MOSAIC_SIZE[-2]
    # mframe[1, mosaic_y::mosaic_size, mosaic_x::mosaic_size] = 1
    image = transform(mframe)
    image.save(os.path.join('mosaics', name))

    if gframe is None:
        gframe = torch.zeros_like(frame, dtype=float)
    gframe += frame * mask

    # image = gframe.div(gframe[3:4]).mul(0xFF)
    image = torch.zeros_like(gframe)
    image[:] = gframe

    if GPT_FILL:
        # different padding attempt - in‑paint missing pixels with diffusion
        image = fill_holes(image)
    else:
        # grow pixels
        run = True
        while run:
            c = image[3:4] == 0
            run = torch.any(c)
            image += c.float() * F.avg_pool2d(image, 3, 1, 1, False, False, 1)

    image = image.div(image[3:4]).mul(0xFF)
    image = image.to(torch.uint8)
    image = transform(image)
    image.save(os.path.join('accumulated', name))
