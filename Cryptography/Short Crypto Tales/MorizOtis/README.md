# [★★☆] Short Crypto

## MorizOtis

<details open>
<summary>
Description
</summary>

Moriz Otis, cryptographer and CERTcoin tycoon, sent coins to a phishing awareness hotline, a jar of entropy, and even
himself. But when he tried one final mega-transfer and locked his flag with it, something went horribly wrong. Now the
flag’s encrypted, Moriz is panicking, and it’s your job to fix the mess.

[`main.py`](main.py) [`data.json`](data.json)

</details>
<details>
<summary>
Solution
</summary>

### Vulnerability

The script re‑uses the same one‑time signature (OTS) key pair to sign 20 different messages. That’s fatal for
hash‑based OTS: by comparing the hash‑chain lengths between the provided signatures and the target message, you can
“walk” one of the existing signatures forward (by hashing a few more times) to forge the signature on the challenge
message.

### Forge the missing signature

- Compute `h2 = SHA256(target_message)` for the challenge message:

  ```
  "<public_key[0]> transfered 999999 CERTcoins to me"
  ```

- For each index i (0…31), find one of the 20 given signatures whose hash at position i (i.e. SHA256 of its
  message’s i‑th byte) is `≥ h2[i]`.
- The difference `d = h1[i] - h2[i]` tells you how many extra times to hash that signature piece to match the chain
  length required.
- Hash it forward `d` times to get the `i‑th` component of the new signature.

### Recover the AES key and decrypt

Once you’ve forged the full 32‑piece signature, the AES key is simply the array of first bytes of each signature
piece. With the provided IV and ciphertext, decrypt with AES‑CBC to reveal the flag.

Implemented in [`solve.py`](Solution/solve.py).

```
SK-CERT{h45h_0n3_71m3_51gn47ur3}
```

</details>
