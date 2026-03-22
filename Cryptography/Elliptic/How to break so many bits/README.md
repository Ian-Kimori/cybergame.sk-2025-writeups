# [★★★] Elliptic

## How to break so many bits?

<details open>
<summary>
Description
</summary>

We have gained access to a service that provides encryption and signature validation using an elliptic curve with a very
large prime. The service is also guarding something very secret, and you must pass its signature test to get its
secrets.

`exp.cybergame.sk:7005`

[`server.py`](server.py)

</details>
<details>
<summary>
Solution
</summary>

### Links

- http://the2702.com/2015/05/08/invalid-curve-attack.html
- https://deut-erium.github.io/WriteUps/2023/nullcon_hackim/crypto/curvy_decryptor/2023-08-21-Nullcon-HackIM-Curvy-Decryptor

### Is this invalid-curve or small-subgroup attack?

It’s really both – you’re performing a small‑subgroup key‐recovery attack, enabled by an invalid‑curve trick.

- Invalid‑curve refers to the fact that you send the server a point $Q$ that doesn’t lie on the genuine secp192r1
  curve (you’ve “twisted” $b$ to get a new curve $E^{\prime}$).
- Small‑subgroup refers to the fact that on your fake $E^{\prime}$, $Q$ has a tiny, known order $r$. The server’s ECDH
  then collapses to revealing $\mathsf{priv}\bmod r$.

So the attack is:

1. Invalid‑curve injection to get the server to do ECDH on your chosen $E^{\prime}$, and
2. Small‑subgroup extraction to learn $\mathsf{priv}\bmod r$.

Repeat for enough small $r$ and CRT them together to recover the full $\mathsf{priv}$.

### Plan

We must know the private key to generate signature with SHA256 for sure.

Exploit outline: an invalid‑curve / small‑subgroup attack to recover $\mathsf{priv}$

By abusing the missing validation in the `2) Encrypt message`, one can recover the server's 192‑bit secret as follows:

1. Pick a "twisted" curve or singular curve over the same prime field $\mathbb F_p$, but with a group order $r$ that has
   small factors. For example, choose a $b{\prime}$ so that
   $$
   E^{\prime}: y^2 = x^3 + a x + b{\prime}\pmod p
   $$
   has a point of (say) order $r\le2^{16}$.

2. Construct a point $Q$ of known small order $r$ on $E^{\prime}$. (You don’t need to prove it’s on the real curve—our
   code never checks!)

3. Submit that Q as your “client pubkey.”
   The server computes
   $$P = [\mathsf{priv}]\,Q$$
   but because $r\,Q=O$, in fact
   $$
   P = [\,\mathsf{priv}\bmod r\,]\,Q,
   $$
   so there are only $r$ possibilities for $P$.

4. Use the encryption oracle:
   The server will encrypt a one–block, chosen plaintext under
   $$
   K = \mathsf{to\_16\_bytes}(P_x),\quad
   IV = \mathsf{to\_16\_bytes}(P_y)
   $$
   For a fixed small‐block plaintext (e.g. a single pad‐block of `\x10…\x10`), you receive
   $$
   C_0 \;=\; \mathrm{AES\_ENC}_K(IV)\;\oplus\;\text{plaintext}.
   $$
   Since you know the plaintext, you recover
   $$
   \mathrm{AES\_ENC}_K(IV)
   $$

5. Brute‑force the $r$ candidates $\{0,1,\dots,r-1\}$ for $\mathsf{priv}\bmod r$: for each $s\in[0,r)$,
   compute $[s]Q\!\to\!P_s$, derive candidate $(K_s,IV_s)$, compute $\mathrm{AES\_ENC}_{K_s}(IV_s)$
   and compare to the observed block. Only the true $\mathsf{priv}\bmod r$ will match.

6. Repeat with several different small orders $r_1,r_2,\dots$ so that $\prod_i r_i>n$. Then CRT them together to recover
   the full 192‑bit $\mathsf{priv}$.

7. Forge your signature Once you know $\mathsf{priv}$, you can trivially compute

```python
signature = SHA256(long_to_bytes(priv) + your_document).digest()
```

and pass the >256‑byte check to read out `sig_verified.txt`.

### Pwn it already!

[`client.py`](Solution/client.py) and [`get_invalid_curves.sage`](Solution/get_invalid_curves.sage) finally lead to the
flag. A little catch was the document also contained `b'\n'` in it so the client side signature also had to be
calculated with new-line at the end.

```
SK-CERT{wh3r3_15_7h47_p01n7}
```

</details>
