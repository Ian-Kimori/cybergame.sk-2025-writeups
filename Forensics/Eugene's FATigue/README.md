# [★★☆] Eugene’s FATigue

## FATigue

<details open>
<summary>
Description
</summary>

National hero and local legend, Eugene "Gene" Securewitz, famous for single-handedly preventing the Great Cyber
Catastrophe by unplugging the internet router at City Hall, has suddenly vanished. Rumor has it he's fled his apartment
to escape fans, bill collectors, and overly enthusiastic historians.

The "Committee for the Preservation of Gene's Greatness" (CPGG) desperately wants to immortalize Gene's groundbreaking
research. It's up to you, the city's most underpaid forensic expert, to unravel the mysteries hidden on Gene’s USB
stick - which reportedly includes profound insights about the universe, meticulously detailed recipes, and an eclectic
collection of heartfelt poems.

Just remember: the fate of national pride - and perhaps the location of Gene’s secret cookie stash - is in your hands.
Download and unzip the diskimage.bin from [`diskimage.bin.gz`](diskimage.bin.gz).

SHA256 after uncompression: 720d7a3167fd3de3d96b4180cc3d30c5efa005dd572fa9642c5063565b085c9a

</details>
<details>
<summary>
Solution
</summary>

This string just came up in `strings` of the whole image:

```
This feels like FX-PREG{cy41a_5vTu7} to me. Cannot hide my best work here.
```

ROT13 to `SK-CERT{pl41n_5iGh7}`.

</details>

## Is that it?

<details open>
<summary>
Description
</summary>

You can’t believe your eyes. Gene was more secretive than you can imagine. Can you recover the hidden stash of wisdom?

</details>
<details>
<summary>
Solution
</summary>

Just casually searching for stuff in a hex editor (YOLO), I noticed a PDF in there somewhere; there is some weird base64
inside the PDF:

```
VuwtuTeEEf9uthkAwc1_zzpRq9x4c/LV0TOw5x6a_U0stQ0VSVHs3aDFzX1dBU18xN19hZnRlcl9hbGx9$EucR/FqMoVaZvjx3OvGT_EV4u/Y7EDwDeA/w9QO3+^ALYXhvTD3R1JcGJUgKFi_mhzkezdqaIHzm261y9IQ_EV4u/Y7EDwDeA/w9QO3+
```

Inside it is a flag:

```
SK-CERT{7h1s_WAS_17_after_all}
```

</details>

## Was that the only file?

<details open>
<summary>
Description
</summary>

You have a persistent feeling there must be more to it. We are still searching for Gene’s recipe. Keep recovering.

</details>
<details>
<summary>
Solution
</summary>

Ok, enough messing around with `strings` and hex editors, we were clearly intended to actually recover data for real.

Here the recovery was attempted with PhotoRec/TestDisk, in one of the runs corrupted files were enabled; this recovered
the files in [`recovered/`](Solution/recovered). The corrupted ZIP can be unpacked with:

```shell
7z x b0003185_file.zip
```

This unpacks three files:

```
fifth.txt
file
fourth-flag.aes.b64.txt
```

`file` is the file relevant for the third flag:

> Begin by gently whispering to a fresh beetroot, ensuring it's thoroughly startled before peeling. Simmer beef slices
> under moonlight until they hum softly, indicating readiness. Combine with precisely three beetroot dreams, diced
> finely, and a pinch of yesterday’s laughter. Allow the mixture to philosophize in an oven preheated to curiosity.
> Occasionally stir with a skeptical spoon, preferably wooden, until the aroma resembles purple jazz. Serve only after
> garnishing with a sprinkle of questions unanswered, paired with a side dish of a sautéed third flag
> SK-CERT{R3c0V3r3D_R3cip3}.

```
SK-CERT{R3c0V3r3D_R3cip3}
```

</details>

## It tastes like a poem

<details open>
<summary>
Description
</summary>

So, turns out, Gene is also a skilled CyberChef! Some of his best inventions were so sensitive he has hidden them under
layers of military grade encryption.

</details>
<details>
<summary>
Solution
</summary>

It seems the `fourth-flag.aes.b64.txt` is the file for this challenge.

I wrote [`aes_decrypt.py`](Solution/aes_decrypt.py) and it brute-forced the AES with 32-byte 0x00 key and 0x00 IV.

```
Trying key 0000000000000000000000000000000000000000000000000000000000000000 (len=32, iv 00000000000000000000000000000000, mode <class 'Crypto.Cipher._mode_cbc.CbcMode'>
entropy: 4.726, plaintext: b'In kitchens made of knitted cheese,\nthe spoons recite old Greek decrees.\nA purple horse with wings of bread,\nplays chess against a talking shed.\n\nGravity sneezes, stars run late,\nthe soup complains about its fate.\nOn Tuesdays clocks wear hats and sigh,\nbananas teaching clouds to fly.\n\nMy socks debate philosophy,\nwhile hummingbirds drink cups of tea.\nA mailbox dreams of being king,\nwhenever cabbages loudly sing.\n\nSo here we float in jelly seas,\na pickle reading prophecies.\nReality slipped on buttered floor\xe2\x80\x94\njust nonsense knocking at the door.\n\nSK-CERT{d0esnt_m4ke_s3nse_7o_d0_f0rensics_anym0r3}\n\x06\x06\x06\x06\x06\x06'
```

```
SK-CERT{d0esnt_m4ke_s3nse_7o_d0_f0rensics_anym0r3}
```

</details>

## Wrapping it up

<details open>
<summary>
Description
</summary>

We have recovered it all; all the Gene’s knowledge. That is - with the exception of the most precious study on time
travel, hidden in the secret file “fifth.txt”. You have a strong feeling you’re on the edge of groundbreaking discovery.

</details>
<details>
<summary>
Solution
</summary>

The `fifth.txt` contains `SK-CERT{1mp0ss1bly_H4RD}` - that was the flag for this challenge. It seems PhotoRec/TestDisk
recovered enough mess after the ZIP or 7z did a good job to extract this anyway, not sure, to be honest.

</details>
