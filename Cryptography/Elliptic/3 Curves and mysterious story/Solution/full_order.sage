# === Sage composite‐generator builder ===

# 1) Your curve parameters
p1, a1, b1 = 221967046828044394711140236713523917903, 65658963385979676651840182697743045469, 84983839731806025530466837176590714802
p2, a2, b2 = 304976163582561072712882643919358657903, 178942576641362013096198577367493407586, 135070218427063732846149197221737213566
p3, a3, b3 = 260513061321772526368859868673058683903, 125788353697851741353605717637937028517, 206616519683095875870469145870134340888

# 2) Instantiate curves
E1 = EllipticCurve(GF(p1), [a1, b1])
E2 = EllipticCurve(GF(p2), [a2, b2])
E3 = EllipticCurve(GF(p3), [a3, b3])

# 3) Factor each group order
N1, facs1 = E1.order(), [int(f) for f,_ in E1.order().factor()]
N2, facs2 = E2.order(), [int(f) for f,_ in E2.order().factor()]
N3, facs3 = E3.order(), [int(f) for f,_ in E3.order().factor()]

print("N1 =", N1, "factors:", facs1)
print("N2 =", N2, "factors:", facs2)
print("N3 =", N3, "factors:", facs3)

# 3b) Compute group exponents via abelian invariants
G1 = E1.abelian_group(); inv1 = G1.invariants()
e1 = inv1[-1]; fac_e1 = [int(f) for f,_ in e1.factor()]
G2 = E2.abelian_group(); inv2 = G2.invariants()
e2 = inv2[-1]; fac_e2 = [int(f) for f,_ in e2.factor()]
G3 = E3.abelian_group(); inv3 = G3.invariants()
e3 = inv3[-1]; fac_e3 = [int(f) for f,_ in e3.factor()]

print("e1 =", e1, "factors:", fac_e1)
print("e2 =", e2, "factors:", fac_e2)
print("e3 =", e3, "factors:", fac_e3)

# 4) Find a generator of each full‐order subgroup
def find_full_order(E, N, facs):
    # precompute cofactors once for speed
    cofactors = [N//f for f in facs]
    attempts = 0
    while True:
        attempts += 1
        R = E.random_point()
        # ensure R has full order by checking all cofactors
        if all(co * R != E(0) for co in cofactors):
            print(f"  succeeded after {attempts} trials")
            return R

P1 = find_full_order(E1, e1, fac_e1)
print("Found P1 of order e1:", P1)

P2 = find_full_order(E2, e2, fac_e2)
print("Found P2 of order e2:", P2)

P3 = find_full_order(E3, e3, fac_e3)
print("Found P3 of order e3:", P3)

# 5) CRT‐glue their coordinates
from sympy.ntheory.modular import crt
mods = [p1, p2, p3]

Gx_full, _ = crt(mods, [int(P1[0]), int(P2[0]), int(P3[0])])
Gy_full, _ = crt(mods, [int(P1[1]), int(P2[1]), int(P3[1])])

print("\n=== FULL‐ORDER CRT GENERATOR ===")
print("Gx_full =", Gx_full)
print("Gy_full =", Gy_full)

# 6) sanity check: ensure (Gx_full mod p_i) == P_i
assert (Gx_full % p1, Gy_full % p1) == (int(P1[0]), int(P1[1]))
assert (Gx_full % p2, Gy_full % p2) == (int(P2[0]), int(P2[1]))
assert (Gx_full % p3, Gy_full % p3) == (int(P3[0]), int(P3[1]))

# 7) how many bits you’ll leak:
import math
print("Bits leaked =", math.log2(lcm([e1,e2,e3])))