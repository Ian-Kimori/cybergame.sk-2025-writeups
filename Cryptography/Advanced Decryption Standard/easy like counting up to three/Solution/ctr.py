from Crypto.Cipher import AES
from Crypto.Util import Counter

# Read encrypted data
with open("../ctr.dat", "rb") as f:
    ciphertext = f.read()

# Key: 16 bytes of zero
key = bytes.fromhex('11111111111111111111111111111111')

# IV / nonce as bytes
iv = bytes.fromhex("99999999999999999999999999999999")

# Create a counter from the IV
ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))

# Create AES cipher in CTR mode
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

# Decrypt
plaintext = cipher.decrypt(ciphertext)

# Output the result
print(plaintext.decode(errors='ignore'))  # Or save to file