# [★☆☆] Adversary

## Almost Classic

<details open>
<summary>
Description
</summary>

We've captured communication of two adversaries. We need to decrypt it.

[`communication.txt`](Almost%20Classic/communication.txt)

</details>
<details>
<summary>
Solution
</summary>

It was [Adbash cipher](https://www.dcode.fr/atbash-cipher).

```
SK-CERT{have_you_ever_heard_about_a_block_cipher???}
```

</details>

## 3AES

<details open>
<summary>
Description
</summary>

We have intercepted a ciphertext along with a presumed key exchange in plaintext. Our sources informed us that the
adversary is using a custom-made cipher they call "3AES".

[`intercept.txt`](3AES/intercept.txt)

</details>
<details>
<summary>
Solution
</summary>

Back in the day, [Triple DES](https://en.wikipedia.org/wiki/Triple_DES#Algorithm) decryption worked as follows:

${\displaystyle {\textrm {plaintext}}=D_{K1}(E_{K2}(D_{K3}({\textrm {ciphertext}})))}$

So we have to mimic that but with AES. I had to write [`intercept.py`](3AES/Solution/intercept.py) to experiment easier,
but here's a one-liner:

```shell
r.emit 'k8JzsMNxiG5KPGSdM/YjGjW7y8dzgG8vsQ3RB062Kz1/EzwUaWz5Sr2UFNuq0jcWqDdj3Y9I0UKz0rYdZuTxMHZ+oKVEqI8Xv9CuvOmOzkdBoBgsjaWT9ke6+BPcMH9Kpwq/jgoYVQ7SfJDKx5GCAxzSLyyS6tXGIZRrUny6jiU=' | r.b64 | r.aes -r b64:ihpLsXPURUTwH4ULO9/87rHRCQibQO6+V4/QKJL7Bgg= | r.aes -rR b64:CznIYU0rBgmzSb7WyqYfj+WKyDSXbbnsa8Wp/IRvUOc= | r.aes -r b64:h+NvKyaJFRhpn7lRWo0JGGcSk7TOd2ltibSSI1CGDCk=
We had to flee. Our guy will wait for you near Slavin. Come right at noon. SK-CERT{1_w0nd3r_why_th3y_d0nt_us3_7h1s_1rl}	
```

</details>

## Key exchange

<details open>
<summary>
Description
</summary>

The adversary started using a new algorithm for key exchange. We were able to get its schema from our source. We attach
the communication where we suspect the adversary might be agreeing upon a key and then using the 3AES encryption we've
seen previously.

![Key exchange](Key%20exchange/exchange.png)

[`message.txt`](Key%20exchange/messages.txt)

</details>
<details>
<summary>
Solution
</summary>

Just XOR $M1$ (message 1), $M2$ (message 2) and $M3$ (message 3). $M1 \oplus M2$ cancels out $S1$. $M2 \oplus M3$
cancels out $S2$.
Therefore, $M1 \oplus M2 \oplus M3$ cancels out $S1$ and $S2$ and only leaves $Key$.

Then just use the previous code to decrypt Triple AES. Implemented
in [`exchange.py`](Key%20exchange/Solution/exchange.py).

```
SK-CERT{d1ff13_h3llm4n_15_n07_7h47_51mpl3_l0l}
```

</details>
