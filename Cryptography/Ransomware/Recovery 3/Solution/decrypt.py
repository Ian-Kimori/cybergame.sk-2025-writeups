#!/usr/bin/env python3
"""
Recover the PRNG seed from the first 8 ciphertext bytes of an encrypted PNG,
then decrypt all .enc files in a folder.
"""

import argparse
import os
import struct


# PRNG definition (must match the one in main.py)
class PRNG:
    def __init__(self, x: int, y: int, counter: int = 0):
        self.x = x & 0xFFFFFFFF
        self.y = y & 0xFFFFFFFF
        self.counter = counter & 0xFFFFFFFF

    def rand(self) -> int:
        # exactly as in your encryptor
        t = (self.x ^ (self.x << 10)) & 0xFFFFFFFF
        self.x = self.y
        self.y = ((self.y ^ (self.y >> 10)) ^ (t ^ (t >> 13))) & 0xFFFFFFFF
        self.counter = (self.counter + 362437) & 0xFFFFFFFF
        return (self.y + self.counter) & 0xFFFFFFFF


# PNG’s first 8 bytes as big-endian u32 words
PNG_SIG0 = int.from_bytes(b'\x89PNG', byteorder='little')
PNG_SIG1 = int.from_bytes(b'\r\n\x1a\n', byteorder='little')


def invert_xor_right(v: int, shift: int) -> int:
    """Invert v = x ^ (x >> shift) for 32‑bit x."""
    x = 0
    for i in reversed(range(32)):
        if i + shift < 32:
            bit = ((v >> i) & 1) ^ ((x >> (i + shift)) & 1)
        else:
            bit = (v >> i) & 1
        x |= bit << i
    return x


def invert_xor_left(v: int, shift: int) -> int:
    """Invert v = x ^ (x << shift) for 32‑bit x."""
    x = 0
    for i in range(32):
        if i - shift >= 0:
            bit = ((v >> i) & 1) ^ ((x >> (i - shift)) & 1)
        else:
            bit = (v >> i) & 1
        x |= bit << i
    return x


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def recover_seed(enc_png: str, skip_blocks: int = 0):
    # read first 8 ciphertext bytes
    with open(enc_png, "rb") as f:
        data = f.read(8)
    c0 = struct.unpack("<I", data[0:4])[0]
    c1 = struct.unpack("<I", data[4:8])[0]

    # keystream words = ciphertext ^ plaintext
    k0 = c0 ^ PNG_SIG0
    k1 = c1 ^ PNG_SIG1

    # counter increments by 362437 each call; initial counter was 0
    C1 = ((skip_blocks + 1) * 362437) & 0xFFFFFFFF
    C2 = ((skip_blocks + 2) * 362437) & 0xFFFFFFFF

    # y1 and y2 are the PRNG’s y after call #1 and call #2
    y1 = (k0 - C1) & 0xFFFFFFFF
    y2 = (k1 - C2) & 0xFFFFFFFF
    print("y1: ", y1)
    print("y2: ", y2)

    # backtrack PRNG state skip_blocks times to align with initial outputs
    for _ in range(skip_blocks):
        A_bt = y2 ^ (y1 ^ (y1 >> 10))
        t_bt = invert_xor_right(A_bt, 13)
        y0_bt = invert_xor_left(t_bt, 10)
        y2, y1 = y1, y0_bt

    # Step A: recover y0 and x0
    # call #1: y1 = f(y0, t0), where t0 = x0 ^ (x0<<10)
    # so   A0 = y1 ^ (y0 ^ (y0>>10)) = t0 ^ (t0>>13)
    # invert that to get t0, then invert x^ (x<<10) to get x0
    # But we don’t yet know y0—so first recover y0 from the second step:
    # call #2: y2 = f(y1, t1) ⇒ A1 = y2 ^ (y1 ^ (y1>>10)) = t1 ^ (t1>>13)
    A1 = y2 ^ (y1 ^ (y1 >> 10))
    t1 = invert_xor_right(A1, 13)
    # t1 = x1 ^ (x1<<10), and x1 == y0 (because x was set to old y at each step)
    y0 = invert_xor_left(t1, 10)

    # now back‐solve x0:
    A0 = y1 ^ (y0 ^ (y0 >> 10))
    t0 = invert_xor_right(A0, 13)
    x0 = invert_xor_left(t0, 10)

    return x0, y0


def decrypt_folder(folder: str, x0: int, y0: int):
    prng = PRNG(x0, y0, counter=0)
    print('PAY ATTENTION THE SORT ORDER MIGHT BE WRONG AND THAT WILL MESS EVERYTHING UP!')
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".enc"):
            continue
        inp = os.path.join(folder, fn)
        out = os.path.join(folder, fn[:-4])  # strip “.enc”
        with open(inp, "rb") as f_in, open(out, "wb") as f_out:
            while True:
                blk = f_in.read(4)
                if not blk:
                    break
                ks = prng.rand().to_bytes(4, "little")
                pt = bytes(b ^ k for b, k in zip(blk, ks))
                f_out.write(pt)
        print(f"→ Decrypted {fn} → {os.path.basename(out)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recover PRNG state from a PNG and decrypt all .enc files"
    )
    parser.add_argument("encrypted_png", help="One of your .enc PNGs")
    parser.add_argument("folder", help="Directory containing all .enc files")
    parser.add_argument(
        "--skip-bytes", type=int, default=0,
        help="Number of plaintext bytes encrypted before the PNG (to adjust PRNG offset)"
    )
    args = parser.parse_args()
    # compute how many 4-byte blocks to skip based on earlier plaintext
    skip_blocks = (args.skip_bytes + 3) // 4
    x0, y0 = recover_seed(args.encrypted_png, skip_blocks)
    print(f"Recovered PRNG seed: x0=0x{x0:08x} ({x0}), y0=0x{y0:08x} ({y0})")
    decrypt_folder(args.folder, x0, y0)
