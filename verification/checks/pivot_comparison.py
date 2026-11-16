#!/usr/bin/env python3
"""Section 7: binary pivot, the optimal pivotal e-variable (ternary kernel and extreme-ray reduction), and the exact optimum.

Rational identities are checked with fractions.Fraction; logarithms with mpmath (30 digits).
The pivotal-kernel linear programme and the exact optimum use scipy (numerical, reported as such).
Checks raise ArithmeticError and stay active under python -O.
Run: python checks/pivot_comparison.py > outputs/pivot_comparison.json
"""
import json
from fractions import Fraction as F
from mpmath import mp, mpf, log, findroot

mp.dps = 30


def check(cond, msg):
    if not cond:
        raise ArithmeticError(msg)


P = [[F(2, 5), F(3, 10), F(1, 5), F(1, 10)], [F(1, 10), F(1, 5), F(3, 10), F(2, 5)]]
Q = [[F(2, 5), F(1, 10), F(1, 10), F(2, 5)], [F(7, 20), F(3, 20), F(2, 5), F(1, 10)]]
out = {}

# Binary guarantee I(6/31)
d = mpf(6) / 31
I = (1 + d) / 2 * log(1 + d) + (1 - d) / 2 * log(1 - d)
out["I_6_31"] = float(I)

# Ternary kernel: rows = states 1..4, columns = outcomes A, B, C
K = [[F(0), F(1, 3), F(2, 3)],   # state 1
     [F(1), F(0), F(0)],         # state 2
     [F(0), F(1), F(0)],         # state 3
     [F(1, 3), F(0), F(2, 3)]]   # state 4
for row in K:
    check(sum(row) == 1 and min(row) >= 0, "kernel row")
law = lambda m: [sum(m[s] * K[s][o] for s in range(4)) for o in range(3)]
nulls = [law(p) for p in P]
alts = [law(q) for q in Q]
check(nulls[0] == nulls[1] == [F(1, 3)] * 3, "null laws not uniform")
check(alts[0] == [F(7, 30), F(7, 30), F(16, 30)], "Q1 law")
check(alts[1] == [F(11, 60), F(31, 60), F(18, 60)], "Q2 law")
x = [F(627, 1000), F(1113, 1000), F(63, 50)]
check(sum(v * w for v, w in zip(nulls[0], x)) == 1, "ternary e-variable not exact")
gains = [sum(mpf(a.numerator) / a.denominator * log(mpf(v.numerator) / v.denominator) for a, v in zip(al, x)) for al in alts]
check(min(gains) > mpf("0.039"), "ternary gain below 0.039")
out["ternary_null_law"] = [str(v) for v in nulls[0]]
out["ternary_alt_laws"] = [[str(v) for v in a] for a in alts]
out["ternary_values"] = [str(v) for v in x]
out["ternary_gains"] = [float(g) for g in gains]

# Saddle optimum of the ternary kernel: x = 3(l q1 + (1-l) q2) equalising both gains
q1 = [mpf(a.numerator) / a.denominator for a in alts[0]]
q2 = [mpf(a.numerator) / a.denominator for a in alts[1]]
def gs(l):
    xx = [3 * (l * a + (1 - l) * b) for a, b in zip(q1, q2)]
    return sum(a * log(v) for a, v in zip(q1, xx)), sum(b * log(v) for b, v in zip(q2, xx))
lam = findroot(lambda l: gs(l)[0] - gs(l)[1], 0.5)
out["ternary_kernel_saddle_value"] = float(gs(lam)[0])

# Extreme-ray reduction (Section 7): kernels with one outcome per extreme ray of {k>=0: 3k1+k2-k3-3k4=0},
# weights (w1, 1-w1, 1-3w1, w1), 0<=w1<=1/3; best uniform e-power = min_lambda D(q_lambda || pi).
rays = [[1, 0, 3, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 3, 0, 1]]
for rr in rays:
    check(3 * rr[0] + rr[1] - rr[2] - 3 * rr[3] == 0, "ray not in cone")
P1m = [mpf(v.numerator) / v.denominator for v in P[0]]
Qm = [[mpf(v.numerator) / v.denominator for v in q] for q in Q]
def ray_value(w1):
    w = [w1, 1 - w1, 1 - 3 * w1, w1]
    cols = [[w[r] * rays[r][s] for s in range(4)] for r in range(4)]
    pi = [sum(P1m[s] * cc[s] for s in range(4)) for cc in cols]
    q = [[sum(qm[s] * cc[s] for s in range(4)) for cc in cols] for qm in Qm]
    def Dl(l):
        return sum((l * a + (1 - l) * b) * log((l * a + (1 - l) * b) / pp) for a, b, pp in zip(q[0], q[1], pi) if pp > 0)
    lo, hi = mpf(0), mpf(1)
    for _ in range(150):
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        if Dl(m1) < Dl(m2):
            hi = m2
        else:
            lo = m1
    return Dl((lo + hi) / 2)
ws = [mpf(k) / 900 for k in range(301)]
vals = [ray_value(w) for w in ws]
kbest = max(range(len(vals)), key=lambda k: vals[k])
check(kbest == len(vals) - 1, "ray optimum not at w1=1/3")
check(abs(vals[-1] - gs(lam)[0]) < mpf(10) ** -20, "ray optimum differs from ternary kernel value")
check(all(vals[k] <= vals[k + 1] for k in range(len(vals) - 1)), "ray value not increasing on grid")
out["ray_reduction_grid_points"] = len(ws)
out["ray_reduction_optimum"] = float(vals[-1])

# Linear programme over all pivotal kernels with a grid of output values (numerical lower bound)
import numpy as np
from scipy.optimize import linprog, minimize
Pn = np.array([[float(v) for v in r] for r in P]); Qn = np.array([[float(v) for v in r] for r in Q])
grid = np.exp(np.linspace(-4, 2, 400)); J = len(grid); X = 4; nv = J * X + J + 1
c = np.zeros(nv); c[-1] = -1
Aub, bub, Aeq, beq = [], [], [], []
for m in range(2):
    row = np.zeros(nv)
    for j in range(J):
        row[j * X:(j + 1) * X] = -Qn[m] * np.log(grid[j])
    row[-1] = 1; Aub.append(row); bub.append(0)
for i in range(2):
    for j in range(J):
        row = np.zeros(nv); row[j * X:(j + 1) * X] = Pn[i]; row[J * X + j] = -1; Aeq.append(row); beq.append(0)
for s in range(X):
    row = np.zeros(nv); row[[j * X + s for j in range(J)]] = 1; Aeq.append(row); beq.append(1)
row = np.zeros(nv); row[J * X:J * X + J] = grid; Aeq.append(row); beq.append(1)
r = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (J * X + J) + [(None, None)], method="highs")
check(r.status == 0, "LP failed")
out["pivotal_grid_lp_value"] = float(-r.fun)
check(-r.fun <= out["ternary_kernel_saddle_value"] + 1e-9, "grid LP exceeds the ternary kernel value")

# Exact (non-pivotal) optimum: concave programme, multistart SLSQP
best = None
for seed in range(30):
    x0 = np.random.default_rng(seed).uniform(0.5, 1.5, 4)
    res = minimize(lambda e: -min(Qn @ np.log(e)), x0, method="SLSQP", bounds=[(1e-9, None)] * 4,
                   constraints=[{"type": "eq", "fun": (lambda e, i=i: Pn[i] @ e - 1)} for i in range(2)],
                   options={"ftol": 1e-13, "maxiter": 1000})
    if res.success and (best is None or res.fun < best.fun):
        best = res
out["exact_optimum_value"] = float(-best.fun)
out["exact_optimum_e"] = [float(v) for v in best.x]
Fc = [F(19, 15), F(1, 2), F(6, 5), F(31, 30)]
check(all(sum(p[s] * Fc[s] for s in range(4)) == 1 for p in P), "F not exact")
out["F_gains"] = [float(sum(mpf(q[s].numerator) / q[s].denominator * log(mpf(Fc[s].numerator) / Fc[s].denominator) for s in range(4))) for q in Q]
print(json.dumps(out, indent=2))
