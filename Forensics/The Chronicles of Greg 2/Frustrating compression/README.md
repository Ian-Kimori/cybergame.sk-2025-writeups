# [★☆☆] The Chronicles of Greg 2

## Frustrating compression

<details open>
<summary>
Description
</summary>

Greg didn’t think much of the file when it showed up—just a zipped folder with a generic name. But the moment he opened
it, he realized it was something else entirely. One archive led to another, then another, each packed with more layers,
more files, more dead ends. His system crawled under the load, but he kept digging, knowing this wasn’t random. Buried
somewhere in the mess was a single file—different, deliberate, hidden for a reason. It was a challenge meant for someone
with his skills. And Greg wasn’t about to back down.

[`00114021.tar`](00114021.tar)

</details>
<details>
<summary>
Solution
</summary>

There was a **lot** of archives here, after fiddling with it manually for a minute or so, it quickly became clear
that it was a no-go. I made [`extract.py`](Solution/extract.py) to unpack it all, then just found the flag:

```shell
% grep -Er 'SK-CERT{.*}' /tmp/out
/tmp/out/2NKY5QZQw94j.flag:ThisIsSK-CERT{n33dl3_1n_h4yst4ck}
```

</details>
