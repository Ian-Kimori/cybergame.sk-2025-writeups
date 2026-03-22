#!/usr/bin/env python3
import math
import json
import csv
import random
import argparse

def is_prime(n):
    if n < 2:
        return False
    for a in (2, 7, 61):
        if a >= n:
            continue
        if pow(a, n-1, n) != 1:
            return False
    return True

def pollards_rho(n):
    if n % 2 == 0:
        return 2
    if is_prime(n):
        return n
    while True:
        c = random.randrange(1, n)
        f = lambda x: (x*x + c) % n
        x = y = 2
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n):
    if n == 1:
        return {}
    if is_prime(n):
        return {n: 1}
    d = pollards_rho(n)
    f1 = factor(d)
    f2 = factor(n // d)
    for pr, exp in f2.items():
        f1[pr] = f1.get(pr, 0) + exp
    return f1

def discrete_log(a, b, p, order):
    m = int(math.ceil(math.sqrt(order)))
    table = {}
    cur = 1
    for j in range(m):
        table.setdefault(cur, j)
        cur = (cur * a) % p
    inv_am = pow(a, -m, p)
    gamma = b
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * inv_am) % p
    raise ValueError("Logarithm not found")

def crt(residues, moduli):
    x = 0
    M = math.prod(moduli)
    for ai, mi in zip(residues, moduli):
        Mi = M // mi
        inv = pow(Mi, -1, mi)
        x = (x + ai * Mi * inv) % M
    return x

def main():
    parser = argparse.ArgumentParser(description="Solve the Möbius inversion crypto challenge")
    parser.add_argument("--params", default="params.json", help="Path to params.json")
    parser.add_argument("--values", default="values.csv", help="Path to CSV of F(n) values")
    args = parser.parse_args()

    with open(args.params) as f:
        params = json.load(f)
    p = int(params["p"])
    g = int(params["g"])
    N = int(params["N"])

    F = {}
    with open(args.values) as f:
        reader = csv.reader(f)
        next(reader)
        for n_str, val_str in reader:
            F[int(n_str)] = int(val_str)

    gx = F[1]

    factors = factor(N)
    primes = list(factors.keys())

    residues = []
    moduli = []
    for qi in primes:
        gi = pow(g, N // qi, p)
        hi = pow(gx, N // qi, p)
        xi = discrete_log(gi, hi, p, qi)
        residues.append(xi)
        moduli.append(qi)

    x = crt(residues, moduli)
    flag_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    print(flag_bytes.decode())

if __name__ == "__main__":
    main()