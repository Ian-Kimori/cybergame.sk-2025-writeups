# [★☆☆] Bastion

## So much just from logs

<details open>
<summary>
Description
</summary>

A routine inspection of authentication logs reveals an overwhelming pattern of suspicious access attempts to a
dockerized SSH bastion server. Inspect the logs and look for any unordinary activity.

[`part1_toolbox_logs.tar.gz`](So%20much%20just%20from%20logs/part1_toolbox_logs.tar.gz)

</details>
<details>
<summary>
Solution
</summary>

```shell
gzip -d *.gz
cat auth.log* | grep -v -e 'Connection closed by invalid user' -e 'Failed password for invalid user' -e 'Failed none for invalid user' -e 'Invalid user ' -e 'Could not get shadow information' -e 'not allowed because account is locked' -e 'Connection closed by authenticating user' -e 'Failed password for ' | r.csd b64 | r.csd hex
i hope they wont find me, and this flag (SK-CERT{n3v3r_f0r637_4b0u7_d47_p3r51573nc3}) keeps on beaconing
```

</details>

## Inspect the file system

<details open>
<summary>
Description
</summary>

Based on your findings, continue your analysis with the docker layer of the docker container.

[`part2_docker_layer.tar.gz`](Inspect%20the%20file%20system/part2_docker_layer.tar.gz)

</details>
<details>
<summary>
Solution
</summary>

Actually found this flag from the reference in `/usr/local/bin/insider.sh` but yolo.

```shell
grep -rao 'SK-CERT{[^}]*}' .
./19d1ccfb743d216f8186a3e0273a24132bb7c4c8813d741108c14722a85732fe/diff/var/data/keylogger.bin:SK-CERT{l34v3_17_70_7h3_pr05}
./19d1ccfb743d216f8186a3e0273a24132bb7c4c8813d741108c14722a85732fe/diff/tmp/persistence:SK-CERT{n3v3r_f0r637_4b0u7_d47_p3r51573nc3}
grep: ./19d1ccfb743d216f8186a3e0273a24132bb7c4c8813d741108c14722a85732fe/work/work: Permission denied
./19d1ccfb743d216f8186a3e0273a24132bb7c4c8813d741108c14722a85732fe/merged/var/data/keylogger.bin:SK-CERT{l34v3_17_70_7h3_pr05}
./19d1ccfb743d216f8186a3e0273a24132bb7c4c8813d741108c14722a85732fe/merged/tmp/persistence:SK-CERT{n3v3r_f0r637_4b0u7_d47_p3r51573nc3}
```

```
SK-CERT{l34v3_17_70_7h3_pr05}
```

</details>

## Clean bastion

<details open>
<summary>
Description
</summary>

The keylogger binary was passed to a malware analyst. Regarding the server, no further changes were detected, so the
container was rebuilt and redeployed to a test environment. Ssh to the system. WARNING: be aware that the system is
running as a single container for all CTF players, so behave.

`ssh://exp.cybergame.sk:7009`
`(ratchet:23ekmnjr4bh5tgvfhbejncidj)`

</details>
<details>
<summary>
Solution
</summary>

Flag upon login to SSH:

```
$ ssh exp.cybergame.sk -p7009 -lratchet
Welcome, Ratchet!
ratchet@exp.cybergame.sk's password: 
Come in and don't be shy

     SK-CERT{bru73_f0rc1n6_u53r5_w0rk5}


3f35af04c9ab:/home/ratchet$ 
```

</details>

## Feel free to dig in

<details open>
<summary>
Description
</summary>

Inside the quarantined system, dig in and search for any remnants or traces of the attackers.

`ssh://exp.cybergame.sk:7009`

</details>
<details>
<summary>
Solution
</summary>

```shell
3f35af04c9ab:/home/ratchet$ cat .ssh/authorized_keys 
ecdsa-sha2-nistp256 AAAAvZHODysGbxHo1wGtqbqi1Ffnr2li7j8ov/V26Nt4w/HR26mWOtT/APG1qBilJoVmCQChz/hCWuIWwzqqZNe1BQ== ratchet@infocube
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOSeOZtJmXS7zliVg5tEaEk9KvhIRn4S3FBjLuo1s0eUvHi6HkzuLTNXiphR8Lth/DWQNeC/A+meex8Y09RtZQA= hacker-U0stQ0VSVHtoMEx5X00wTGx5X1RIM3lfNHIzXzV0aUxsX2gzUjN9
3f35af04c9ab:/home/ratchet$ 
```

```shell
r.emit 'U0stQ0VSVHtoMEx5X00wTGx5X1RIM3lfNHIzXzV0aUxsX2gzUjN9' | r.b64
SK-CERT{h0Ly_M0Lly_TH3y_4r3_5tiLl_h3R3}
```

</details>

## The backdoor culprit

<details open>
<summary>
Description
</summary>

Explore the source git repository for the bastion server docker deployment and look for the source of the dropped
backdoor.

[`part5_ssh-bastion-repo.tar.gz`](The%20backdoor%20culprit/part5_ssh-bastion-repo.tar.gz)

</details>
<details>
<summary>
Solution
</summary>

```shell
git log --all | grep SK-CERT
    update ssh keys SK-CERT{r09U3_3MPL0Y33_0r_5uPpLycH41n}
```

</details>
