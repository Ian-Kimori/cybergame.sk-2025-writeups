#!/usr/bin/env python3
import base64
from functools import reduce

from Crypto.Cipher import AES

MESSAGES = [
    'tL90zeX19A2CLF9PH9oMQEuAPURmv7rp+oQ/DWiXEwTTQ6Ry/yDBHgqBGAa+OCaoI5JfdGYqhM2SHCWQyVdKJPj8HTY3gkxG38JEaET+CgX7h3cPQrufwYG8UOH6scrk1+guWvLOIAb/VJZ7pbjnEeORtN9C91EvxhNAO7r9pSFczo2TCGyFSaNOsvzN6C88Gw+4eXMTtVw=',
    'mBpf0ZTjWUczik9rrfwdM4wgVrN4I+++PGQSctBkAliziynxXJxYT0KnWxf5q8f1utv9ERPaWsJ+e/fENymhCWELXAnXGFaF8LHLzl9N1TWxu4b1CPPsU2pi2Rar9pm9FLfN4x/yYfP7daqKD7Rvq67wRu9+jsrgQKFj7687mZA4I9s11NpQQ7TSrEVr8Xx0d8FIZsV4x9M=',
    'R8BSLUs24ieC8nV22ER/HYDYE7ltrz548dNMJeC+SwsOrcXFmuTdYHlSCnor9NU28nSoDhCJ7DXMDL5gzEiPWsikIgeM30CNfyH2ny/A6H0eZrOyLiEK8ZOS79hoFDsbiA3IidA2KpB9EgbRz1vRzXoOsAhUTa27/Px3nlCOboZRhXnTruzsPnKpWYjvXRQLKKW/d4Y4BbI=',
    'xl24Q/q0QOTK0hl1zOrSLgOEfbg+pzUf2FLNfS4OJD8k+R5hviqHb+DFSO2m1gXzkNoQa2guDRSRtKmHqigFKB/azqdEahvEnbH/wUImMc5UeC1FjOwsc7MBrhELI2M+rpo0z2RvzX+2VF0fCQWGm8by5D7yyJL8VHsE6acQjGSvkz0L+kRNtAQXh4ywjAet3rxnSlyu1kO9N4BPjCpCYNtfuPbnccMUCWiePiyj+GXh838frFEDdzL9gVOA4CZSNIOOgIJ0Re1c3dPQBdxhqpeXXyoj4PUK1W1Q6ZjOr362SoD8PwUU55nQTPUW50cp',
    'CuU+OFj7FoHmmT1Ppsfn+kbLwwQF9A9hvdLgE8sEIi6D6RyCr6b2E+YxQi2x9qkECPJkiuSeYypnDifjavlhvTez6hM2JbZV4WrrzmePjWd/a63ZBgTs/JR9j0XdO0xoXCi5Y0rPDjj0oJsfLilu34PXtO8t1Y2MnlPQ/aRvhn+xe3mKauDuDtPjI+N3Tood',
    'AYdjr4yUpFrQC23EKtj0+w5m6Qq5QnxHcCC8WeU9GUPH6rAig0auAEKMVyfGnj/qxHKXuFSnWX+9Z04hY3RYLw=='
]


def xor_bytes(*args):
    return bytes(reduce(lambda x, y: [a ^ b for a, b in zip(x, y)], args))


def triple_decrypt_cbc(ciphertext, k1, k2, k3):
    cipher3 = AES.new(k3, AES.MODE_ECB)
    step1 = cipher3.decrypt(ciphertext)

    cipher2 = AES.new(k2, AES.MODE_ECB)
    step2 = cipher2.encrypt(step1)

    cipher1 = AES.new(k1, AES.MODE_ECB)
    plaintext = cipher1.decrypt(step2)

    return plaintext


def main():
    m1 = base64.b64decode(MESSAGES[0])
    m2 = base64.b64decode(MESSAGES[1])
    m3 = base64.b64decode(MESSAGES[2])

    key = xor_bytes(m1, m2, m3)
    print("Recovered key (hex):", key)

    """
    Recovered key (hex): b'key1: Om3TeRjbnnGxxNs3k/73aZXMZWneHF9XD11tIklg4kk=\nkey2: kl426dwQSc8lEZNPRy94s7MTZBHdiycxLf/9ShBKR+0=\nkey3: eWYw7oB8h46tzNTJEHR75h/urZ94e5G1IDGCDkOh0Sw='
    """

    key1 = base64.b64decode('Om3TeRjbnnGxxNs3k/73aZXMZWneHF9XD11tIklg4kk=')
    key2 = base64.b64decode('kl426dwQSc8lEZNPRy94s7MTZBHdiycxLf/9ShBKR+0=')
    key3 = base64.b64decode('eWYw7oB8h46tzNTJEHR75h/urZ94e5G1IDGCDkOh0Sw=')

    for message in MESSAGES[3:]:
        ciphertext = base64.b64decode(message.encode())
        print(f'ciphertext (len={len(ciphertext)}:', ciphertext)
        plaintext = triple_decrypt_cbc(ciphertext, key1, key2, key3)

        try:
            print("Decrypted text:")
            print(plaintext.decode('utf-8'))
        except UnicodeDecodeError:
            print("Raw decrypted bytes:")
            print(plaintext)

        print('\n' + '=' * 120 + '\n')


if __name__ == '__main__':
    main()
