p = 6277101735386680763835789423207666416083908700390324961279
a = -3

def get_invalid_curves(cutoff=10 ** 4):
    factors = {}
    total = 1
    i = 0
    while total < p * 3:
        try:
            E = EllipticCurve(GF(p), [a, i])
            order = E.order()
            n_facs = order.factor()
        except ArithmeticError:
            i += 1
            continue
        for prime, power in n_facs:
            if prime > cutoff:
                break
            if prime in factors:
                if factors[prime][0] < power:
                    gen = E.gen(0) * (order // prime)
                    # total *= prime**(power-factors[prime][0])
                    factors[prime] = [power, int(gen[0]), int(gen[1]), i]
            else:
                gen = E.gen(0) * (order // prime)
                factors[prime] = [power, int(gen[0]), int(gen[1]), i]
                # total *= prime**(power)
                total *= prime
        print(i, total)
        i += 1
    return factors


print('-' * 120)
for prime, curve in get_invalid_curves().items():
    print(f'{prime}: {curve}')
