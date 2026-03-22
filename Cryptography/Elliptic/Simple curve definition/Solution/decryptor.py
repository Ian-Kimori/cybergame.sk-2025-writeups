#!/usr/bin/env python3
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# — Curve parameters from main.py —
p = 298211241770542957242152607176537420651
a = p - 1
G = (
    107989946880060598496111354154766727733,
    36482365930938266418306259893267327070
)

# — Client’s public key from cache.jsonl —
client_pub = (
    291216048318375702409990419027018106946,
    219380392381458352976435257541531938506
)

# — Recovered server private scalar k —
k = 37041828426322252952359931953705367198


def modinv(x, m):
    """Modular inverse via extended GCD."""
    lm, hm = 1, 0
    low, high = x % m, m
    while low > 1:
        ratio = high // low
        nm = hm - lm * ratio
        new = high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % m


def ec_add(P, Q):
    """Elliptic-curve point addition on y^2 = x^3 + a x over F_p."""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == y2:
        if y1 == 0:
            return None
        s = (3 * x1 * x1 + a) * modinv(2 * y1, p) % p
    else:
        if x1 == x2:
            return None
        s = (y2 - y1) * modinv(x2 - x1, p) % p
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def ec_scalar_mult(k, P):
    """Double‑and‑add scalar multiplication on the curve."""
    result = None
    addend = P
    while k:
        if k & 1:
            result = ec_add(result, addend)
        addend = ec_add(addend, addend)
        k >>= 1
    return result


def int_to_bytes(x):
    """Big-endian byte representation, at least one byte."""
    return x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')


# 1) Compute the shared EC point S = k * client_pub
S = ec_scalar_mult(k, client_pub)

# 2) Derive the 32-byte AES key from S.x
shared_key = int_to_bytes(S[0])[:32]


def decrypt_log(filename, field):
    """Decrypt and print each JSONL entry from `filename` using AES-CBC."""
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            blob = bytes.fromhex(record[field])
            iv, ct = blob[:16], blob[16:]
            cipher = AES.new(shared_key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            print(pt.decode())


if __name__ == "__main__":
    print("== Decrypted received messages ==")
    decrypt_log("cache/cache_recv.jsonl", "recv")
    print("\n== Decrypted sent messages ==")
    decrypt_log("cache/cache_send.jsonl", "send")
