#!/usr/bin/env python3
"""Numerical and exact checks for Sections 4-6 (Theorem 4.5, Remark 4.6, Example 4.8, Remark 5.5, Propositions 6.1-6.2).

Checks raise ArithmeticError and stay active under python -O.
Run: python checks/extension_checks.py > outputs/extension_checks.json
"""
import json
from fractions import Fraction as F
from mpmath import mp, mpf, log, sqrt, exp, quad, inf, nsum

mp.dps = 30
out = {}


def check(cond, msg):
    if not cond:
        raise ArithmeticError(msg)


# Theorem 4.5: E(a_n)=1/2, E(b_n)=(n+1)/2 is exact for M_n and N_n
for n in range(2, 2001):
    m = (1 - F(1, n)) * F(1, 2) + F(1, n) * F(n + 1, 2)
    check(m == 1, f"exactness fails at n={n}")
out["thm_notfree_exact_for_n_2_to_2000"] = True
check(nsum(lambda n: 2 * mpf(2) ** (-n), [2, inf]) == 1, "H weights")
lb = log(mpf(27) / 16) / 4
check(abs(mpf(3) / 4 * log(mpf(3) / 2) - log(2) / 4 - lb) < mpf(10) ** -25, "lower bound identity")
# E_H log E = sum_n 2^{-n} [ (1-1/n) log(1/2) * 2 + (1/n) log((n+1)/2) * 2 ] / ... (M_n and N_n give the same E-law)
EH = nsum(lambda n: 2 * mpf(2) ** (-n) * ((1 - 1 / n) * log(mpf(1) / 2) + (1 / n) * log((n + 1) / mpf(2))), [2, inf])
EQ = mpf(3) / 4 * log(mpf(3) / 2) + EH / 4
check(EQ >= lb, "E_Q log E below the stated bound")
out["thm_notfree_lower_bound"] = float(lb)
out["thm_notfree_E_Q_logE"] = float(EQ)

# Remark 4.6: D(Q||Unif) = 1 - log 2 for q = (2 sqrt x)^{-1}; v_eps norm -> 0
D = quad(lambda t: 1 / (2 * sqrt(t)) * log(1 / (2 * sqrt(t))), [0, 1])
check(abs(D - (1 - log(2))) < mpf(10) ** -12, "D(Q||U)")
out["remark_continuous_D"] = float(D)
for eps in [mpf(10) ** -k for k in (2, 4, 8)]:
    check(abs(quad(lambda t: 1 / (2 * sqrt(t)) - 1, [0, eps]) - (sqrt(eps) - eps)) < mpf(10) ** -15, "phi(1_[0,eps])")
out["remark_continuous_v_eps_norms"] = [float(e / (sqrt(e) - e)) for e in (mpf(10) ** -2, mpf(10) ** -4, mpf(10) ** -8)]

# Example 4.8: chi^2(N(mu,1)||N(0,1)) = exp(mu^2) - 1
for mu in (mpf("0.1"), mpf("0.5"), mpf(1)):
    chi = quad(lambda z: (exp(mu * z - mu ** 2 / 2) - 1) ** 2 * exp(-z ** 2 / 2) / sqrt(2 * mp.pi), [-inf, inf])
    check(abs(chi - (exp(mu ** 2) - 1)) < mpf(10) ** -15, "chi-square formula")
out["example_gauss_chi2_ok"] = True

# Section 6 constants
c = mpf(1) / 2 - log(2); g = c + 2
EPE = quad(lambda x: 1 / (2 * sqrt(x)), [0, 1]); EPl = quad(lambda x: log(1 / (2 * sqrt(x))), [0, 1])
check(abs(EPE - 1) < mpf(10) ** -15 and abs(EPl - c) < mpf(10) ** -15, "null constants")
for n in (2, 3, 5):
    L = exp(-4 * n)
    EA = quad(lambda x: log(1 / (2 * sqrt(x))), [0, L]) / L
    check(abs(EA - (c + 2 * n)) < mpf(10) ** -12, "A_n log mean")
    check(abs((1 - mpf(1) / n) * c + EA / n - g) < mpf(10) ** -12, "Q_n log mean")
    tv = (1 - L) / n  # d_TV(Q_n,P) = (1/n) d_TV(A_n,P) = (1/n)(1-L)
    out[f"tv_n{n}"] = float(tv)
    mass = (1 - mpf(1) / n) * L + mpf(1) / n
    check(mass <= mpf(2) / n, "UI mass bound")
out["c"] = float(c); out["g"] = float(g)


# Prop 6.1: sup_n E_{Q_n}(log E - a)_+ = 2 + e^{-2a}/8, approached as n grows
def tail(n, a):
    r = exp(-2 * a) / 8
    # under A_n, log E = -log 2 + Z + 2n with Z ~ Exp(2): E(Y+2n-a)_+ computed exactly
    k = 2 * n - log(2) - a  # Y+2n-a = k + Z
    ea = k + mpf(1) / 2 if k >= 0 else exp(2 * k) / 2
    return (1 - mpf(1) / n) * r + ea / n
for a in (0, 1, 3):
    vals = [tail(n, mpf(a)) for n in (2, 10, 100, 10 ** 6)]
    target = 2 + exp(-2 * mpf(a)) / 8
    check(all(v <= target + mpf(10) ** -20 for v in vals) and abs(vals[-1] - target) < mpf(10) ** -4, "tail sup")
out["prop_exacttail_ok"] = True

# Prop 6.2: 1 + (1-alpha) sum_{k>=1}(1-1/n)^k = n(1-alpha)+alpha
for n in (2, 10, 100):
    for al in (F(1, 20), F(1, 2)):
        s = 1 + (1 - al) * (n - 1)  # geometric sum (1-1/n)/(1/n) = n-1
        check(s == n * (1 - al) + al, "delay identity")
out["prop_delay_identity_ok"] = True
print(json.dumps(out, indent=2))
