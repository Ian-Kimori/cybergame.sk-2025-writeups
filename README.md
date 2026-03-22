# CyberGame.sk 2025

All challenges are archived (if possible) in their respective directories, you should find all files that were given for
the challenge. Many of them can be run/solved locally. Files related to solving the challenge are always in `Solution/`
folder, avoid it if you don't want spoilers.

I tend to over-do and over-complicate things - you've been warned. If you have a better solution, send me a Pull Request
🙂.

## Dependencies

When you see commands like `r.emit` or `r.b64` or other `r.<something>` in some of the write-ups, that
is [Binary Refinery](https://github.com/binref/refinery), basically CyberChef in a command-line, but better, lol. If
you do not use it yet, you should.

Some of the crypto challenges use [SageMath](https://www.sagemath.org/), you can find follow
the [Sage Installation Guide](https://doc.sagemath.org/html/en/installation/index.html).

### Python virtual environment

A lot of the solutions use Python and various libraries, if you want to play with the scripts, it is best to create a
virtual environment and install the dependencies:

```shell
python3.13 -m venv venv # may work with a different version, 3.13 is what I used
source venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
```

## Challenges (Table of Contents)

Some write-ups are split-up per sub-challenge, some are not - depends on their length and how related they are.

### Cryptography

#### [[☆☆☆] Advanced Decryption Standard](Advanced%20Decryption%20Standard)

- Codebook (1 pts)
- Blockchain (1 pts)
- easy like counting up to three (1 pts)

#### [[★☆☆] Adversary](Adversary)

- Almost Classic (3 pts)
- 3AES (3 pts)
- Key exchange (9 pts)

#### [[★☆☆] Ransomware](Ransomware)

- Recovery 1 (3 pts)
- Recovery 2 (3 pts)
- Recovery 3 (9 pts)

#### [★★☆] Short Crypto Tales

- [MorizOtis (3 pts)](Short%20Crypto%20Tales/MorizOtis)
- [Suibom (3 pts)](Short%20Crypto%20Tales/Suibom)
- [SecretFunction^2 (18 pts)](Short%20Crypto%20Tales/SecretFunction%5E2)

#### [★★★] Elliptic

- [Simple curve definition (9 pts)](Elliptic/Simple%20curve%20definition)
- [How to break so many bits? (9 pts)](Elliptic/How%20to%20break%20so%20many%20bits%3F)
- [3 Curves and mysterious story (27 pts)](Elliptic/3%20Curves%20and%20mysterious%20story)

### Malware Analysis and Reverse Engineering

#### [[☆☆☆] SanityChecker](SanityChecker)

- Sleepy python (1 pts)
- Bash dropper (1 pts)
- Password protected (1 pts)

#### [[★☆☆] ConnectionChecker](ConnectionChecker)

- Tool (3 pts)
- Lies (3 pts)
- Executer (9 pts)

#### [★★☆] The Chronicles of Greg

- [SystemUpdate incident report (6 pts)](The%20Chronicles%20of%20Greg/SystemUpdate%20incident%20report)
- [The Blob Whisperer (6 pts)](The%20Chronicles%20of%20Greg/The%20Blob%20Whisperer)
- [The Shared Object Prophecy (18 pts)](The%20Chronicles%20of%20Greg/The%20Shared%20Object%20Prophecy)

#### [★★★] JAILE3

- [MathEmulator (9 pts)](JAILE3/MathEmulator)
- [Loader (27 pts)](JAILE3/Loader)

### Forensics

#### [[☆☆☆] First Contact](First%20Contact)

- Hard choices (1 pts)
- In competition with jellyfish (1 pts)
- So long, but wait, we’re still playing! (1 pts)
- Still fighting (1 pts)
- Between 15 and 17 (1 pts)
- A Day in the Strife (1 pts)
- Independence day (1 pts)
- Or hack their mainframe... (1 pts)

#### [[★☆☆] Bastion](Bastion)

- So much just from logs (3 pts)
- Inspect the file system (3 pts)
- Clean bastion (3 pts)
- Feel free to dig in (3 pts)
- The backdoor culprit (9 pts)

#### [★☆☆] The Chronicles of Greg 2

- [Frustrating compression (3 pts)](The%20Chronicles%20of%20Greg%202/Frustrating%20compression)
- [You need stronger glasses (6 pts)](The%20Chronicles%20of%20Greg%202/You%20need%20stronger%20glasses)

#### [[★★☆] Eugene’s FATigue](Eugene's%20FATigue)

- FATigue (6 pts)
- Is that it? (6 pts)
- Was that the only file? (6 pts)
- It tastes like a poem (6 pts)
- Wrapping it up (18 pts)

### OSINT

#### [[★☆☆] The digital trail](The%20digital%20trail)

- The tip (3 pts)
- The evidence (3 pts)
- The digital footprint (3 pts)
- The private channel (3 pts)
- The escape plan (9 pts)

#### [[★★★] Suspect tracking](Suspect%20tracking)

- Identification (9 pts)
- Localization (9 pts)
- Golden Hour (27 pts)

### Process and Governance

#### [[★☆☆] Reading the dusty books](Reading%20the%20dusty%20books)

- Handling (3 pts)
- Colors of the rainbow (6 pts)

### Web Exploitation and Binary Exploitation

#### [[★★☆] Equestria](Equestria)

- Door To The Stable (6 pts)
- Shadow Realm (6 pts)
- The Dark Ruler (6 pts)
- Final Curse (18 pts)

#### [[★★☆] JAILE](JAILE)

- Calculator (6 pts)
- User (6 pts)
- Final Escape (18 pts)

#### [★★☆] JAILE2

- [Calculator v2 (6 pts)](JAILE2/Calculator%20v2)
- [The Tasty Bun (6 pts)](JAILE2/The%20Tasty%20Bun)
- [dictFS (6 pts)](JAILE2/dictFS)
- [Blazing-fast, memory-safe interpreter (18 pts)](JAILE2/Blazing-fast,%20memory-safe%20interpreter)

#### [★★☆] ByteBusters

- [Terminal Magic (6 pts)](ByteBusters/Terminal%20Magic)
- [Secure Shell (6 pts)](ByteBusters/Secure%20Shell)
- [Memory Phantoms (6 pts)](ByteBusters/Memory%20Phantoms)
- [Binary Sabotage (18 pts)](ByteBusters/Binary%20Sabotage)

#### [★★★] Meme History Blog

- [Scratching the surface (9 pts)](Meme%20History%20Blog/Scratching%20the%20surface)
- [Digging Deep (27 pts)](Meme%20History%20Blog/Digging%20Deep)