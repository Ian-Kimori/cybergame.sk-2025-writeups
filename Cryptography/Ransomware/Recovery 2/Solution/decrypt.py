def rotate_right(byte, bits):
    return ((byte >> bits) & 0xff) | ((byte << (8 - bits)) & 0xff)


def decrypt_file(encrypted_file, key):
    with open(encrypted_file, "rb") as f:
        data = f.read()

    decrypted = bytearray()
    block_size = len(key)
    num_blocks = (len(data) + block_size - 1) // block_size

    for i in range(num_blocks):
        block = data[i * block_size: (i + 1) * block_size]
        if i == 0:
            # First block: XOR with key, ignoring LSB
            dec_block = bytearray()
            for b, k in zip(block, key):
                # Clear LSB before XOR to get original byte
                dec_byte = (b & 0xFE) ^ k
                dec_block.append(dec_byte)
        else:
            # Other blocks: reverse the encryption steps
            # 1. First rotate key
            offset = i % block_size
            rotated_key = key[offset:] + key[:offset]
            # 2. Then rotate right by 3 to undo the left rotation
            rotated_block = bytes(rotate_right(b, 3) for b in block)
            # 3. Finally XOR with rotated key
            dec_block = bytes(b ^ k for b, k in zip(rotated_block, rotated_key))
        decrypted.extend(dec_block)

    return decrypted


def main():
    # Example usage
    # encrypted_file = "./files/slon.png.enc"
    # output_file = "./files/slon.png"

    encrypted_file = "./files/slopes_of_the_unknowable.txt.enc"
    output_file = "./files/slopes_of_the_unknowable.txt"

    # Decrypt the file
    decrypted_data = decrypt_file(encrypted_file, bytes.fromhex('a58b3283477d8470cba5c8f083634e2a'))

    # Write decrypted data
    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] Decrypted file written to {output_file}")


if __name__ == "__main__":
    main()
