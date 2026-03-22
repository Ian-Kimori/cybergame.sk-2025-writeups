

import json
import hashlib
from Crypto.Cipher import AES

# Load the provided data
with open('../data.json', 'r') as f:
    data = json.load(f)

# Reconstruct the target message
pub0_hex = data['public_key'][0]
message2 = (pub0_hex + ' transfered 999999 CERTcoins to me').encode()

# Hash of the target message
h2 = hashlib.sha256(message2).digest()

# Parse the given signatures and their messages
signatures = data['signatures']
hashes = [hashlib.sha256(sig['message'].encode()).digest() for sig in signatures]

# Forge the missing signature by leveraging reused OTS keys
signature2 = []
for i in range(32):
    target_byte = h2[i]
    # Find a provided signature whose hash byte ≥ target_byte
    for j, h in enumerate(hashes):
        if h[i] >= target_byte:
            delta = h[i] - target_byte
            sig_piece = bytes.fromhex(signatures[j]['signature'][i])
            # Hash forward delta times to match the needed chain length
            for _ in range(delta):
                sig_piece = hashlib.sha256(sig_piece).digest()
            signature2.append(sig_piece)
            break
    else:
        raise ValueError(f"No suitable signature found for index {i}")

# Derive the AES key (first byte of each signature piece)
aes_key = bytes(piece[0] for piece in signature2)

# Decrypt the flag
iv = bytes.fromhex(data['iv'])
enc = bytes.fromhex(data['enc'])
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
flag = cipher.decrypt(enc)

print(flag.decode())