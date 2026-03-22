# [★☆☆] The Chronicles of Greg 2

## You need stronger glasses

<details open>
<summary>
Description
</summary>

Greg sat in his lab, staring at a blurry screen recording someone sent him without context. As a forensic analyst, he
was used to piecing together distorted footage, but this one was almost useless—shaky, low resolution, and barely a few
seconds long. He ran it through every tool he had, trying to stabilize and sharpen it. Slowly, vague movements took
shape—someone doing something at a desk, maybe typing, maybe hiding something. Nothing was clear. But whoever sent it
wanted Greg to figure it out. And they knew he couldn’t walk away.

[`f_conv.m4v`](f_conv.m4v)

</details>
<details>
<summary>
Solution
</summary>

When I saw the video, I immediately remembered
[this challenge from Jeff Geerling](https://www.youtube.com/watch?v=gaV-O6NPWrI&t=297s), he moved his Finder window
around with a mosaic-censored names of files and asked people to uncover what the filenames were offering $50. KoKuToru
provided a [full GitHub repo](https://github.com/KoKuToru/de-pixelate_gaV-O6NPWrI) with his solution.

I took that as my starting point.

I first trimmed the video to only the relevant part. I chose to only trim to the part of the video where the window is
moving, as that is leaking extra data, having many frames with the mosaic in the same position won't help us:

```shell
ffmpeg -ss '00:01:05' -i f_conv.m4v -to '00:00:13' -c copy trimmed.mp4
```

Next, I extracted the individual frames of the video (like KoKuToru did):

```shell
mkdir -p frames
ffmpeg -i trimmed.mp4 -filter_complex "select=bitor(gt(scene\,0.001)\,eq(n\,0))" -vsync drop frames/%04d.png
```

Here, I deviated from KoKuToru's solution, because I am lazy. I decided to use OpenCV's `matchTemplate` to match a piece
of the window without the mosaic in each frame, so that I can crop the window out and have it in the same position in
each resulting image. This is not pixel-perfect, but hey, it was fast!
See in [`extract_windows.py`](Solution/extract_windows.py).

```shell
python3 extract_windows.py
```

Back to KoKuToru's solution—he dealt with a mosaic of 25 x 25 pixels, our mosaic is more like 8 or 9 pixels by 8 or 9
pixels. This is kind of annoying, so I calculated the average size of a mosaic square on the top of the
[`demosaic.py`](Solution/demosaic.py) script:

```python3
# this is my estimate made in Photoshop, manually measured a few squares horizontally and vertically and
# divided by the number of squares measured
MOSAIC_SIZE = (112 / 13, 190 / 22)
```

Another thing that had to be adjusted were the 25 px and 50 px sizes in the script, I replaced those with
`MOSAIC_SQUARE_SIZE`.

I also changed KoKuToru's magic value for to be `MAGIC_VAL` and just using some trial and error I bumped it to 15. When
you look inside of `mosaics/` directory that the script generates, you want to be sure the blue lines are aligned to the
grid and that the green dots are in the middle of the squares. Tweaking this and `MOSAIC_SIZE` influences that behavior.

The last thing I did was implement an alternative
to [KoKuToru's fill algorithm](https://github.com/KoKuToru/de-pixelate_gaV-O6NPWrI?tab=readme-ov-file#accumulate-the-pixels)
with some help from ChatGPT. This makes the resulting image look a little different—perhaps it helps.

Just run the script and check the `accumulated/` folder - the further in frames you go the more clear it should be, this
does not work universally, sometimes it gets messed up later on, YMMV. Play with the different settings, I ended up
getting a few results and then combined them using overlays to help me read various parts of the flag.

```shell
python3 demosaic.py
```

Later on, I was able to improve this a bit with help from Claude. It thought it would be better to sample the entire
mosaic squares/blocks and "smartly accumulate" the pixels in them instead of just picking the one in the center. This
did make the text a little bit more readable. It also added some sharpening to the result, that might have helped a bit
too. The [`demosaic_claude.py`](Solution/demosaic_claude.py) is based on the [`demosaic.py`](Solution/demosaic.py),
compare the two to see the differences.

After squinting between the various results for a while, I was able to make out the flag:

```
SK-CERT{n0b0dy_will_3v3r_r34d_th15_0f7d55a1}
```

PS: if you wear glasses, take them off, it helps 😁.

PS2: You can make a nice video of the transformation in the `accumulated/` folder with this:

```shell
ffmpeg -framerate 30 -start_number 1 -i accumulated/%04d.png -c:v libx264 -pix_fmt yuv420p accumulate.mp4
```

One of the less blurry images:

![less blurry](Solution/less_blurry.jpg)

</details>