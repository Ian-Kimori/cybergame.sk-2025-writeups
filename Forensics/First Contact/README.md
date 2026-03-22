# [☆☆☆] First Contact

## Hard choices

<details open>
<summary>
Description
</summary>

The sky tore open as the ship descended, a gleaming monolith against the midday sun. Without warning, every screen
flickered - phones, billboards, watches - replaced by a single message: "You are invited." A voice followed: "This is
the first contact. Your species has been selected to participate in CyberGame, an interstellar CTF. Success grants you
access to galactic science, post-scarcity tech, and diplomatic recognition. Failure means we proceed with scheduled
construction of a hyperspace bypass that, regrettably, requires the demolition of your planet. Here is Message One."

Then a stream of cryptic data pulsed across the screens - elegant, alien, and waiting.

Additional instructions from the Earth Command:

- download the file,
- find a hidden message,
- the messages are in the format SK-CERT{something} unless stated otherwise. Enter the full flag from the first "S" to
  the last "}".
- do not write anything else into the answer field; the aliens expect the exact flag.

[`part1.txt`](part1.txt)

</details>
<details>
<summary>
Solution
</summary>

Flag is in `part1.txt`, plain text.

```
SK-CERT{th1s-w0rks-w3ll}
```

</details>

## In competition with jellyfish

<details open>
<summary>
Description
</summary>

The alien ship projected a new message: "Congratulations, Earthlings. The first part has been successfully solved by
three people, fifteen orcas, one octopus, a colony of ants, and two jellyfish. Let's make it harder!". It almost sounded
like an insult.

[`part2.html`](part2.html)

Additional instructions from the Earth Command:

- click the link
- find a hidden message
- you need to dig deeper. Lots of options here - see the source, or download the file and open it in a text editor.
- it will be in the SK-CERT{something} format, you know the drill

</details>
<details>
<summary>
Solution
</summary>

Parsed by hand from [part2.html](part2.html).

```
SK-CERT{hello}
```

</details>

## So long, but wait, we’re still playing!

<details open>
<summary>
Description
</summary>

The alien ship updated their omnipresent dashboards after the second flag: ants are out. One last jellyfish remains in
the game. One octopus. And you. Meanwhile, the orcas fled the planet. No pressure, right?

New day, new challenge. The message says:

> Jura vg pbzrf gb pryrfgvny zbirzragf, FX-PREG{ebg4gv0a} vf cvibgny.

Additional instruction from the jellyfish:

- do NOT enter dumb stuff. The flag is in the form SK-CERT{something}, not FX-PREG.
- this time you may need CyberChef

</details>
<details>
<summary>
Solution
</summary>

ROT 13

```
Jura vg pbzrf gb pryrfgvny zbirzragf, FX-PREG{ebg4gv0a} vf cvibgny.
When it comes to celestial movements, SK-CERT{rot4ti0n} is pivotal.
```

</details>

## Still fighting

<details open>
<summary>
Description
</summary>

The alien ship fell eerily silent for a moment. Then, in a deep sarcastic tone:

"Congratulations, human. You've managed to outwit jellyfish. The galaxy is... impressed."

A single clap echoed through every smart speaker on Earth. It almost felt like the sound was made with just one hand,
but that's impossible, right? Right?

Then the voice continued: "One jellyfish short of a leaderboard and still you persist. Very well. Let's see if you
covered all your bases."

> Once upon a time, there was an encoded message
>
VGhlIGVuY29kZWQgbWVzc2FnZSBzYWlkIGRHaGxJR1pzWVdjZ2FYTWdhR2xrWkdWdUlHUmxaWEJsY2lCaVdGWnFZVU5DYTFwWFZuZGFXRWxuV1d4b1YyRnRSa1JrTW1ScFYwWmFjVmxWVGtOaE1YQllWbTVrWVZkRmJHNVdiWFJyWWpKS1JtSkZhRTVXTTJoeFZGUkJNV0l4WkhGVGJGcGhUV3RhV2xaR1VtRlRiRXB5VGxVeFZWSnNXbEJWYlhoWFl6RldjVnBGT1ZOTk1tZ3pWa1pTU2sxV2JGZGhSRnBWWW14YVlWcFhkRXRqYkZKVlVsUlNUazFyV2taVlZ6VnpWR3hPUjFkdVZscFdWMUV3VmpJeFlWWkZOVWhhUm1Sb1RXeEtNbGRYZEZkak1VNUhWMjVXVjJKVldsTmFWM2hMVkZaRmVWbDZiRkZWVnpnNVEyYzlQUW89Cg==

Additional instruction from the orcas, transmitting back home from the nearest star cluster:

- CyberChef is your friend.

</details>
<details>
<summary>
Solution
</summary>

Annoying base64 loop

```shell
r.emit 'VGhlIGVuY29kZWQgbWVzc2FnZSBzYWlkIGRHaGxJR1pzWVdjZ2FYTWdhR2xrWkdWdUlHUmxaWEJsY2lCaVdGWnFZVU5DYTFwWFZuZGFXRWxuV1d4b1YyRnRSa1JrTW1ScFYwWmFjVmxWVGtOaE1YQllWbTVrWVZkRmJHNVdiWFJyWWpKS1JtSkZhRTVXTTJoeFZGUkJNV0l4WkhGVGJGcGhUV3RhV2xaR1VtRlRiRXB5VGxVeFZWSnNXbEJWYlhoWFl6RldjVnBGT1ZOTk1tZ3pWa1pTU2sxV2JGZGhSRnBWWW14YVlWcFhkRXRqYkZKVlVsUlNUazFyV2taVlZ6VnpWR3hPUjFkdVZscFdWMUV3VmpJeFlWWkZOVWhhUm1Sb1RXeEtNbGRYZEZkak1VNUhWMjVXVjJKVldsTmFWM2hMVkZaRmVWbDZiRkZWVnpnNVEyYzlQUW89Cg==' | r.b64 | r.csd b64 | r.csd b64 | r.csd b64 | r.csd b64
The message is: SK-CERT{4li3nZ_3nc0d3_7h0r0ughlY}. VGhlIGVuZC4K
```

</details>

## Between 15 and 17

<details open>
<summary>
Description
</summary>

The whole wider galactic society knows the universe is nothing but numbers. You are the only competitor still standing,
human, but we have to say, the octopus was DELICIOUS! Decrypt this flag, given to you in hexadecimal format.

Additional instruction from the orcas, transmitting back home from the nearest star cluster:

- what we said earlier.

53 4b 2d 43 45 52 54 7b 36 33 37 5f 75 35 33 64 5f 37 30 5f 68 33 78 34 64 33 63 31 6d 34 6c 7d

</details>
<details>
<summary>
Solution
</summary>

```
r.emit '53 4b 2d 43 45 52 54 7b 36 33 37 5f 75 35 33 64 5f 37 30 5f 68 33 78 34 64 33 63 31 6d 34 6c 7d' | r.hex
SK-CERT{637_u53d_70_h3x4d3c1m4l}
```

</details>

## A Day in the Strife

<details open>
<summary>
Description
</summary>

Orcas were right from day one. Turns out these aliens were not friendly AT ALL. Having eaten all the other competitors,
they tried to eat you as well. Luckily, we intercepted their comms in binary saying:

> 01010011 01001011 00101101 01000011 01000101 01010010 01010100 01111011 00110011 00110100 00110111 01011111 00110111
> 01101000 00110011 01011111 01101000 01110101 01101101 00110100 01101110 00110101 00101100 01011111 00110111 01101000
> 00110011 01111001 01011111 01101011 01101110 00110000 01110111 01011111 00110111 00110000 00110000 01011111 01101101
> 01110101 01100011 01101000 01111101

</details>
<details>
<summary>
Solution
</summary>

```python
binary_str = '01010011 01001011 00101101 01000011 01000101 01010010 01010100 01111011 00110011 00110100 00110111 01011111 00110111 01101000 00110011 01011111 01101000 01110101 01101101 00110100 01101110 00110101 00101100 01011111 00110111 01101000 00110011 01111001 01011111 01101011 01101110 00110000 01110111 01011111 00110111 00110000 00110000 01011111 01101101 01110101 01100011 01101000 01111101'

decoded = ''.join(chr(int(b, 2)) for b in binary_str.split())
print(decoded)
```

```
SK-CERT{347_7h3_hum4n5,_7h3y_kn0w_700_much}
```

</details>

## Independence day

<details open>
<summary>
Description
</summary>

Mankind started coordinating a response. Since these aliens are incredibly technologically advanced, and also have seen
all our movies, the idea of using morse code is burned. We needed to use something else. This link will save our
planet: https://v2.cryptii.com/

> LXXXIII LXXV XLV LXVII LXIX LXXXII LXXXIV CXXIII LXXXIV CIV CXIV CXI CXIX LXXIV XCVII CXVIII CI CVIII CV CX CXV LXXIX
> CX LXXXIV CIV CI CIX CXXV

</details>
<details>
<summary>
Solution
</summary>

Roman numbers into decimal and then `chr()`

```python
def roman_to_int(s):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
                  'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman_dict[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total


roman_numerals = [
    "LXXXIII", "LXXV", "XLV", "LXVII", "LXIX", "LXXXII", "LXXXIV",
    "CXXIII", "LXXXIV", "CIV", "CXIV", "CXI", "CXIX", "LXXIV", "XCVII",
    "CXVIII", "CI", "CVIII", "CV", "CX", "CXV", "LXXIX", "CX", "LXXXIV",
    "CIV", "CI", "CIX", "CXXV"
]

ascii_values = [roman_to_int(rn) for rn in roman_numerals]
decoded_chars = [chr(num) for num in ascii_values]
decoded_string = ''.join(decoded_chars)

print(decoded_chars)
print(decoded_string)
```

```
SK-CERT{ThrowJavelinsOnThem}
```

</details>

## Or hack their mainframe...

<details open>
<summary>
Description
</summary>

Even though we contracted the best javelin thrower in the whole world, the alien spaceship seems to have a force field.
Switching to plan B - we must hack their mainframe. We know their computer would shut down if we pass the right keyword.
However, the keyword is verified by a regular expression (regex). Can you find the correct string?

> ^(?:S[K])-(?:C(?:E|E{0})R)(?:T){v(?:3)r[y]_[5]7r(?:4)n6(?:3)_r3(?:6)3x}$

</details>
<details>
<summary>
Solution
</summary>

Find input that fits regex

```
^(?:S[K])-(?:C(?:E|E{0})R)(?:T){v(?:3)r[y]_[5]7r(?:4)n6(?:3)_r3(?:6)3x}$
```

```
SK-CERT{v3ry_57r4n63_r363x}
```

</details>
