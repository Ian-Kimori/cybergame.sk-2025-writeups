# [★☆☆] Ransomware

## Recovery 1

<details open>
<summary>
Description
</summary>

You've been contacted by a movie production company that has been hit by ransomware. They need your help recovering the
script for the next episode of a long-awaited series. It's urgent—millions (and possibly billions) of impatient fans are
waiting.

[`recovery_1.zip`](Recovery%201/recovery_1.zip)

</details>
<details>
<summary>
Solution
</summary>

Easy XOR - first 16 bytes of almost every PNG are the same, XOR those with the `slon.png.enc` to get key

```shell
r.ef Ransomware/files/inescapable_storyception_of_doom.txt.enc | r.xor h:8382D29E0559CF6F21BE0CB2F97E5955
```

```
SK-CERT{7r1v14l_r4n50mw4r3_f0r_7h3_574r7}
```

</details>

## Recovery 2

<details open>
<summary>
Description
</summary>

The producer did not upgrade their infrastructure, and their servers were encrypted again. The attackers used slightly
modified malware, but it should not be too hard to decrypt.

[`recovery_2.zip`](Recovery%202/recovery_2.zip)

</details>
<details>
<summary>
Solution
</summary>

Use [`gpt_key.py`](Recovery%202/Solution/gpt_key.py) first, it recovers the key properly included the scrambled LSB
bits. Then use [`decrypt.py`](Recovery%202/Solution/decrypt.py) to decrypt the contents, first block (16 bytes) will
have LSB wrong but YOLO, not needed for solving.

```
SK-CERT{r1ck_4nd_m0r7y_4dv3n7ur35}
```

</details>

## Recovery 3

<details open>
<summary>
Description
</summary>

The script for the final episode is encrypted with a completely different ransomware. It’s the grand finale of the
series, and we have to recover it.

[`recovery_3.zip`](Recovery%203/recovery_3.zip)

</details>
<details>
<summary>
Solution
</summary>

The most important part is that the `PRNG` is initialized only once and it seems the `flag.txt` was
encrypted first and then the `slonik.png`, meaning we have to backtrack that many blocks (size of `flag.txt` / 4) in the
PRNG state to get to the beginning.

Implemented in [`decrypt.py`](Recovery%203/Solution/decrypt.py); ChatGPT wrote most of it, hate the code, was faster
than doing it by hand, YOLO.

```shell
python3 decrypt.py --skip-bytes 3315 ./files/slonik.png.enc ./files 
```

```
SK-CERT{h4rd3r_x0r5h1f7_r3v3r53}
```

</details>
