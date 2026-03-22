# [★★★] Elliptic

## 3 Curves and mysterious story

<details open>
<summary>
Description
</summary>

We have discovered an intergalactic server that asks for some data and, in exchange, returns more data—but encrypted.
Check the source code and try to decrypt the mysterious message.

`exp.cybergame.sk:7006`

[`server.py`](server.py)

</details>
<details>
<summary>
Solution
</summary>

### TL;DR

We choose one giant point that simultaneously lives on all three curves. One server query leaks ≈ 381 bits of $d$. A few
instant discrete logs + CRT give the full scalar, SHA-256($d$) is the AES-CBC key, and the story decrypts.

1. [`full_order.sage`](Solution/full_order.sage) – **Build the giant generator**  
   *Generates one point of full exponent on each curve, then CRT-glues them.*
    - Factors the group orders to obtain the per-curve exponents ($e_1,e_2,e_3$).
    - Finds random points ($P_i$) whose order equals the full exponent (quick cofactor test).
    - Uses the Chinese Remainder Theorem to combine the three $(x,y)$ pairs into a
      single $(G_x^{\text{full}},G_y^{\text{full}})$.
    - Prints that coordinate pair plus the exact number of bits we’ll leak (≈ 381 bits).

2. [`client.py`](Solution/client.py) – **Query the oracle**  
   *Sends the CRT generator, collects the server’s response.*
    - Connects, supplies `Gx_full`/`Gy_full`.
    - Receives $Q_1,Q_2,Q_3 = d·G_i$ (one per curve) **and** the AES-CBC ciphertext.
    - Saves those points and ciphertext locally for the next stage.

3. [`discrete_logs.sage`](Solution/discrete_logs.sage) – **Recover residues of $d$**  
   *Computes $d \bmod e_i$ on each curve.*
    - Re-creates the three curves, loads the full-order bases $P_i$.
    - Parses the returned $Q_i$ and runs `P_i.discrete_log(Q_i)` – instant because every subgroup is $≤ 3.2 × 10⁹$.
    - Outputs the three residues $(r_1,r_2,r_3)$.

4. [`recover.py`](Solution/recover.py) – **Rebuild $d$, derive the key, decrypt**  
   *Finishes everything in pure Python.*
    - Applies Chinese Remainder Theorem: $d = \text{CRT}(r_1,r_2,r_3; e_1,e_2,e_3)$.
    - Hashes $d$ with SHA-256 to obtain the 256-bit AES key.
    - Splits the captured blob into IV and ciphertext, runs AES-CBC-decrypt, strips PKCS#7 padding.
    - Prints the plaintext “mysterious story” – flag complete!

```
SK-CERT{5qu1rr3l5_53cr375_4nd_d33p_57473}
```

</details>
