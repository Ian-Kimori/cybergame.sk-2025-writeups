#!/usr/bin/env python3
import base64

from Crypto.Cipher import AES

KEY1 = base64.b64decode('h+NvKyaJFRhpn7lRWo0JGGcSk7TOd2ltibSSI1CGDCk=')
KEY2 = base64.b64decode('CznIYU0rBgmzSb7WyqYfj+WKyDSXbbnsa8Wp/IRvUOc=')
KEY3 = base64.b64decode('ihpLsXPURUTwH4ULO9/87rHRCQibQO6+V4/QKJL7Bgg=')

MESSAGES = [
    'rOkz0hogqrrjVXe8KhfwPmTXqy0NI5BaaVRwg8g4490Gi//XIIYY6t7pMpw/0DN4V26tcdwmmOOne75oEt4/oQ==',
    't+WZSn6H1mA9XUQJrQ2xxt33nVh6orKFygb7Q+8xMe9JSk7XgMdZ8Fwq9rSMw9SuCZWoIJ8qYOSOKwmyyvMmW7/kkPDoWNEezfme08HmEWi3DrPAefIpNVVewbfVzt5j',
    'dNMxxcWRHkxNxHu17gw5g5IE/Jf6tNmxw4OfBHEXfRv0cx4pKVKYjZofSRAgFspLnWcdR5GGasKxCgpOANPyS4liypMrPFKlXy/pm2BG7bM=',
    'k8JzsMNxiG5KPGSdM/YjGjW7y8dzgG8vsQ3RB062Kz1/EzwUaWz5Sr2UFNuq0jcWqDdj3Y9I0UKz0rYdZuTxMHZ+oKVEqI8Xv9CuvOmOzkdBoBgsjaWT9ke6+BPcMH9Kpwq/jgoYVQ7SfJDKx5GCAxzSLyyS6tXGIZRrUny6jiU='
]


def triple_decrypt_cbc(ciphertext, k1, k2, k3):
    cipher3 = AES.new(k3, AES.MODE_ECB)
    step1 = cipher3.decrypt(ciphertext)

    cipher2 = AES.new(k2, AES.MODE_ECB)
    step2 = cipher2.encrypt(step1)

    cipher1 = AES.new(k1, AES.MODE_ECB)
    plaintext = cipher1.decrypt(step2)

    return plaintext


def main():
    for message in MESSAGES:
        ciphertext = base64.b64decode(message.encode())
        print(f'ciphertext (len={len(ciphertext)}:', ciphertext)
        plaintext = triple_decrypt_cbc(ciphertext, KEY1, KEY2, KEY3)

        try:
            print("Decrypted text:")
            print(plaintext.decode('utf-8'))
        except UnicodeDecodeError:
            print("Raw decrypted bytes:")
            print(plaintext)

        print('\n' + '=' * 120 + '\n')


if __name__ == '__main__':
    main()
