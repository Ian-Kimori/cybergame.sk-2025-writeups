# [★☆☆] The digital trail

## The tip

<details open>
<summary>
Description
</summary>

We've received a tip about a suspicious website promoting a privacy-focused browser extension. The website seems
legitimate, but you should check it thoroughly. Sometimes the most interesting things are hidden in plain sight.

</details>
<details>
<summary>
Solution
</summary>

Repo corresponding to the link we were given in the challenge is this: https://github.com/alexmercer-dev/datashield-web/

Very bottom of `README.md` has this: `U0stQ0VSVHtoMWRkM25fMW5fcGw0MW5fczFnaHR9`

```shell
r.emit 'U0stQ0VSVHtoMWRkM25fMW5fcGw0MW5fczFnaHR9' | r.b64
SK-CERT{h1dd3n_1n_pl41n_s1ght}
```

</details>

## The evidence

<details open>
<summary>
Description
</summary>

We have gathered more information about the website. It seems like some time ago it contained malicious code.

</details>
<details>
<summary>
Solution
</summary>

In the
[commit here](https://github.com/AlexMercer-dev/datashield-web/pull/6/commits/d76658afa4964698f6ffaebe4968110117c1b5bb#diff-66890216d671b1c02636e231ae893ae7e4833c163ffa1606dc58c85a7250a9e9),
file `docs/static/js/analytics-enhanced.js`, line 144.
Then you want to search through **all commits** for the flag pattern:

```bash
git clone <repo-url>
cd <repo-name>

# Search all commit diffs for the flag format
git log -p --all | grep -i "SK-CERT{"
```

If that's too slow or the history is large:

```bash
# Faster - search all historical versions of all files
git grep "SK-CERT{" $(git rev-list --all)
```

Or if you want more context around the match:

```bash
# Shows commit hash, file, and surrounding lines
git log -p --all -S "SK-CERT{" --source --all
```

The `-S` flag (pickaxe) is the most efficient — it finds commits where that string was **added or removed**, so it catches malicious code that was later deleted too, which is exactly the scenario this challenge describes.

```
SK-CERT{m4l1c10us_c0mm1t_d3t3ct3d}
```

</details>

## The digital footprint

<details open>
<summary>
Description
</summary>

The suspect behind the malicious pull request appears to be a well-known figure. We need to track his digital footprint
across the internet. Where else might he be active?

</details>
<details>
<summary>
Solution
</summary>
if you want more context around the match:

```bash
# Shows commit hash, file, and surrounding lines
git log -p --all -S "SK-CERT{" --source --all
```
Perfect. Now you have:

- **Username:** `evanmassey1976` (from the email `evanmassey1976@proton.me`)

**Next step — run Sherlock:**
```bash
sherlock evanmassey1976
```

It will scan across platforms and return wherever that username exists. Then manually visit each hit and look for suspicious posts/content that might hide a flag.

If you don't have Sherlock installed:
```bash
pip install sherlock-project --break-system-packages
sherlock evanmassey1976
```

Found posts from `evanmassey1976` on reddit.com, the post with the flag
is: https://www.reddit.com/user/evanmassey1976/comments/1kpmiaw/security_practices_that_are_actually_underrated/

Take the first letter of each line.

```
SK-CERT{S0C14L-M3D14-0S1NT-TR41L}
```

</details>

## The private channel

<details open>
<summary>
Description
</summary>

Our investigation has led us to a private communication channel. There seems to be a group controlling access to certain
areas. What secrets might it be hiding?

</details>
<details>
<summary>
Solution
</summary>

The user `evanmassey1976` on reddit.com included a discord invite, in the #random channel some bots are talking and
mention this:

> **Aleah Franco**
> Note to self: Password for Mark's channel is 'ReallySecretNobodyKnowsAboutThisPassword'. Need to keep this safe.
> SK-CERT{d1sc0rd_b0t_s3cr3ts}

That is the third flag.

</details>

## The escape plan

<details open>
<summary>
Description
</summary>

They are suspecting us! It seems like they are migrating to a new, closed platform. We need to find where they're going
before they disappear completely.

</details>
<details>
<summary>
Solution
</summary>

- To join the secret channel one has to DM Mark Wesley and send the password
  `ReallySecretNobodyKnowsAboutThisPassword`
- You are then added to the #hacking channel. There is an image posted of a forum where all the operations are being
  migrated to.
- In the descriptive text of that image, still in Discord you will find the text `freirehf-fancr.rh`.
- This is ROT13 of the domain `serverus-snape.eu`.

This domain has a TXT record with a weird looking base64:

```shell
host -t ANY serverus-snape.eu
...
serverus-snape.eu descriptive text "U0stQ0VSVHtkbnNfcjNjMHJkXzFuc3AzY3Qwcn0="
...
```

Decoding that leads to the final flag of this challenge:

```shell
r.emit 'U0stQ0VSVHtkbnNfcjNjMHJkXzFuc3AzY3Qwcn0=' | r.b64
SK-CERT{dns_r3c0rd_1nsp3ct0r}
```

</details>
