import base64
import math
from collections import Counter
from typing import List, Iterator

from Crypto.Cipher import AES

ENCRYPTED_DATA = base64.b64decode(open('recovered/b0003185_file.zip_unpacked/fourth-flag.aes.b64.txt', 'rb').read())

print(len(ENCRYPTED_DATA))

# put 16-byte keys here to be tried as keys and IVs
keys = [b'\x00' * 16, bytes.fromhex("01020304050607080102030405060708"),
        bytes.fromhex('11111111111111111111111111111111'), bytes.fromhex("99999999999999999999999999999999"),
        b'R3c0V3r3D_R3cip3']

modes: List[int] = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_CTR, AES.MODE_GCM]


def shannon_entropy(data: bytes) -> float:
    """
    Compute the Shannon entropy (in bits per byte) of `data`.
    Returns a number between 0 (all bytes identical) and 8 (uniformly random).
    """
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    return -sum(
        (freq / length) * math.log2(freq / length)
        for freq in counts.values()
    )


def generate_keys(iv_only: bool = False) -> Iterator[bytes]:
    for key in keys:
        if len(key) == 16:
            yield key
            if not iv_only:
                yield key + key[:8]  # 24-byte key
                yield key * 2  # 32-byte key
        else:
            raise ValueError(f'Key {key.hex()} is not 16 bytes long!')


def decrypt_and_print(mode: int, ciphertext: bytes, key: bytes, iv: bytes = None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, AES.MODE_ECB)
        print(f'Trying key {key.hex()} (len={len(key)}, mode {type(cipher)}')
    else:
        cipher = AES.new(key, mode, iv)
        print(f'Trying key {key.hex()} (len={len(key)}, iv {iv.hex()}, mode {type(cipher)}')
    plaintext = cipher.decrypt(ciphertext)
    entropy = shannon_entropy(plaintext)
    print(f'entropy: {entropy:.3f}, plaintext:', plaintext)
    if entropy < 7.5:
        input(f'Woot entropy is {entropy}, check this out! Press any key to continue.')
    print('\n' + '-' * 100 + '\n')


def main():
    for mode in modes:
        for key in generate_keys():
            if mode == AES.MODE_ECB:
                decrypt_and_print(AES.MODE_ECB, ENCRYPTED_DATA, key)
            else:
                for iv in generate_keys(iv_only=True):  # only generate 16-byte IVs
                    decrypt_and_print(AES.MODE_CBC, ENCRYPTED_DATA, key, iv)


if __name__ == '__main__':
    main()
