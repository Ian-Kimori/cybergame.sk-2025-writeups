# [☆☆☆] Advanced Decryption Standard

## Codebook

<details open>
<summary>
Description
</summary>

You know that feeling—waking up after a wild night of gambling, pockets full of keys you’re sure are yours, but
somehow every single one feels wrong, and you can’t, for the life of you, remember which one fits where, or even what
it’s supposed to unlock?

Now imagine being a novice cryptographer after that same night. You’ve got the keys—sure—but absolutely no clue what
they open, how they work, or why you even have them in the first place. Welcome to the hangover of cryptography.

You think this file should contain a flag encrypted using... AES? Also, the letters ECB come to mind although you don’t
know what it is. The flag should be in the usual format SK-CERT{something}.

key (hex format): 00000000000000000000000000000000

[`ecb.dat`](Codebook/ecb.dat)

</details>
<details>
<summary>
Solution
</summary>

`ecb.dat` is encrypted with just `0x00`. See [`codebook.py`](Codebook/Solution/codebook.py) or just:

```shell
r.ef ecb.dat | r.aes h:00000000000000000000000000000000
SK-CERT{f1r57_15_3cb}
```

</details>

## Blockchain

<details open>
<summary>
Description
</summary>

You can’t, for the life of you, remember why each flag ended up with a different chaining method. Must’ve been one
heck of a night...

This file contains the flag encrypted using AES with mode CBC.

key (hex format): 00000000000000000000000000000000 iv (hex format): 01020304050607080102030405060708

[`cbc.dat`](Blockchain/cbc.dat)

</details>
<details>
<summary>
Solution
</summary>

`cbc.dat` is encrypted with just `0x00` and IV `01020304050607080102030405060708`.
See [`blockchain.py`](Blockchain/Solution/blockchain.py) or just:

```shell
r.ef cbc.dat | r.aes -i h:01020304050607080102030405060708 h:00000000000000000000000000000000
SK-CERT{cbc_m0d3_15_n3x7}
```

</details>

## easy like counting up to three

<details open>
<summary>
Description
</summary>


The math of this is beyond your comprehension, but you just know this file contains a third flag, encrypted using
AES with CTR (counter) mode.

key (hex format): 11111111111111111111111111111111 iv (hex format): 99999999999999999999999999999999

[`ctr.dat`](easy%20like%20counting%20up%20to%20three/ctr.dat)

</details>
<details>
<summary>
Solution
</summary>

`ctr.dat` is encrypted with just `11111111111111111111111111111111` and IV `99999999999999999999999999999999`.
See [`ctr.py`](easy%20like%20counting%20up%20to%20three/Solution/ctr.py) or just:

```shell
r.ef ctr.dat | r.aes -m CTR -i h:99999999999999999999999999999999 h:11111111111111111111111111111111
SK-CERT{4nd_7h3_l457_15_c7r}
```

</details>