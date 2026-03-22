# [★★★] Elliptic

## Simple curve definition

<details open>
<summary>
Description
</summary>

I am using a very good and secure messaging system, but I found logs that are not from my communications. Because it is
so secure, I need your help to decrypt the messages so I can find out what was going on.

[`server_data.zip`](server_data.zip)

</details>
<details>
<summary>
Solution
</summary>

### Recover $k$

First, we extract ECDH public points—these are the two public points represented as $P=k \cdot G$ and $Q=k' \cdot G$.
This is what is exchanged during the ECDH handshake.

Then, we compute subgroup order—we need the group order to ensure the discrete log operates correctly in that order.
This involves using tools like Sage and some elliptic curve group math.

- The full elliptic‑curve group $E(F_p)$ has some order $N$.
- Our base point G generates a cyclic subgroup of order $r | N$.
- Discrete‑log algorithms (like Pollard’s Rho) work modulo the subgroup order.
- Knowing $r$ ensures that the discrete logarithm solution $k$ is computed modulo the correct subgroup order, which
  defines the cyclic group where $G$ and $P$ reside.

Then, we recover server's private scalar:

- Elliptic‑Curve Discrete Logarithm Problem (ECDLP): find $k$ such that $k \cdot G = P$
- That $k$ is exactly the server's private key used in the ECDH exchange.

This is it in SageMath:

```python
p = 298211241770542957242152607176537420651
a = p - 1
E = EllipticCurve(GF(p), [a, 0])

G = E(107989946880060598496111354154766727733,
      36482365930938266418306259893267327070)

P = E(72947667249607227642932393260968830921,
      261432642373021661017738970173175343657)

r = G.order()
assert r * P == E(0)  # sanity check

k = G.discrete_log(P)

assert k * G == P  # sanity check
print("Recovered k =", k)
```

```
Recovered k = 37041828426322252952359931953705367198
```

### Derive AES key and decrypt

This part is implemented in [`decryptor.py`](Solution/decryptor.py).

First, we derive the shared AES key:

- Compute the shared point $S = k \cdot Q$.
- Truncate the x‑coordinate of S to 32 bytes to form the AES‑CBC key.

```python
S = ec_scalar_mult(k, client_pub, a, p)
key = int_to_bytes(S[0])[:32]
```

Then we just AES-CBC decrypt the logs.

```
== Decrypted received messages ==
hi
how are you?
good, want secret?
SK-CERT{n33d_70_k33p_m0v1n6}
bye

== Decrypted sent messages ==
hi
good, u?
y
thx bye
```

</details>
