#!/usr/bin/env python3
"""
Recover a 16-byte PNG encryption key using known plaintext blocks.
"""

import argparse


def rotate_right(b: int, bits: int) -> int:
    """
    Rotate an 8-bit value right by the given number of bits.
    """
    return ((b >> bits) & 0xFF) | ((b << (8 - bits)) & 0xFF)


# Known PNG header bytes 0–15 (IHDR chunk signature prefix)
PNG_HDR = bytes.fromhex("89504E470D0A1A0A0000000D49484452")


def recover_key(enc_path: str, orig_path: str) -> bytes:
    """
    Recover the 16-byte encryption key given:
      - enc_path: path to the encrypted PNG file (.enc)
      - orig_path: path to the original plaintext PNG file

    The algorithm:
      1. Read first 16 bytes of ciphertext (block 0) and use PNG_HDR
         to extract the top 7 bits of each key byte.
      2. Read next 16 bytes of ciphertext (block 1), undo the left
         rotation by 3, XOR with the known plaintext bytes from the
         original file, and extract each LSB of the rotated key.
      3. Combine the 7 bits from step 1 and the single LSB from step 2
         to reconstruct each full key byte.
    """
    # Read first 32 bytes of ciphertext
    with open(enc_path, "rb") as f:
        data = f.read(32)
    enc0 = data[0:16]
    enc1 = data[16:32]

    # Step 1: extract top 7 bits from block 0
    key_top7 = [(enc0[i] ^ PNG_HDR[i]) & 0xFE for i in range(16)]

    # Read plaintext block 1 from the original PNG
    with open(orig_path, "rb") as f:
        f.seek(16)
        plain1 = f.read(16)

    # Step 2: undo the rotate_left(…,3) on block 1 ciphertext
    unrot1 = [rotate_right(b, 3) for b in enc1]

    # XOR with plaintext to obtain the rotated key bytes
    rotated_key = bytes(u ^ p for u, p in zip(unrot1, plain1))

    # Step 3: extract each LSB from the rotated key and combine
    full_key = bytes(
        key_top7[i] | (rotated_key[(i - 1) % 16] & 1)
        for i in range(16)
    )
    return full_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recover PNG encryption key using known plaintext."
    )
    parser.add_argument(
        "enc_path",
        help="Path to the encrypted .enc PNG file"
    )
    parser.add_argument(
        "orig_path",
        help="Path to the original plaintext PNG file"
    )
    args = parser.parse_args()

    key = recover_key(args.enc_path, args.orig_path)
    print(key.hex())
