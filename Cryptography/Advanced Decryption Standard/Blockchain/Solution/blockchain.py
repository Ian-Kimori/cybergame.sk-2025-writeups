from Crypto.Cipher import AES

# Load encrypted data
with open("../cbc.dat", "rb") as f:
    ciphertext = f.read()

# Key: 16 bytes of 0x00
key = b'\x00' * 16

# IV: from the given hex string
iv = bytes.fromhex("01020304050607080102030405060708")

# Create AES cipher in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt
plaintext = cipher.decrypt(ciphertext)

# Optionally unpad if padded (e.g. PKCS7)
# from Crypto.Util.Padding import unpad
# plaintext = unpad(plaintext, AES.block_size)

# Output result
print(plaintext.decode(errors='ignore'))  # Or save to file