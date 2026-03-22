from Crypto.Cipher import AES

# Read the encrypted file
with open("../ecb.dat", "rb") as f:
    ciphertext = f.read()

# Create AES cipher in ECB mode with a 16-byte (128-bit) zero key
key = b'\x00' * 16
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt the ciphertext
plaintext = cipher.decrypt(ciphertext)

# Optionally strip padding (e.g., PKCS7), if used
# from Crypto.Util.Padding import unpad
# plaintext = unpad(plaintext, AES.block_size)

# Print or save the decrypted output
print(plaintext.decode(errors="ignore"))  # Or write to a file
