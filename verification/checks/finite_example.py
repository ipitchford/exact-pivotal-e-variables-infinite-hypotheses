#!/usr/bin/env python3
"""Finite-hypothesis margin algorithm and an exact four-state certificate.

The general linear programmes use floating point. The worked example is also
verified independently with fractions.Fraction and an explicit primal/dual pair.
The rational competitor only supplies a lower bound on unrestricted exact growth.
Run: python checks/finite_example.py > finite_margin_results.json
Run with --no-scipy for the standard-library-only rational checks.
"""
from fractions import Fraction as F
import argparse
import json
import math
import platform


def check(condition, message):
    """A certificate check that remains active under python -O."""
    if not condition:
        raise ArithmeticError(message)


def solve_margin(p, q):
    """P, Q have one probability row per hypothesis and one column per state.

    Dual: max t, P h=0, Q h>=t, -1<=h<=1.
    Primal: min ||Q.T w + P.T lambda||_1, w>=0, sum(w)=1.
    """
    import numpy as np
    from scipy.optimize import linprog
    p, q = np.asarray(p, float), np.asarray(q, float)
    if p.ndim != 2 or q.ndim != 2 or p.shape[1] != q.shape[1]:
        raise ValueError("P and Q must be matrices on the same finite states")
    if min(p.min(), q.min()) < 0:
        raise ValueError("Negative probability")
    if not (np.allclose(p.sum(axis=1), 1) and np.allclose(q.sum(axis=1), 1)):
        raise ValueError("Probability rows must sum to one")
    i, k = p.shape
    j = q.shape[0]
    dual = linprog(
        np.r_[np.zeros(k), -1.0],
        A_ub=np.c_[-q, np.ones(j)], b_ub=np.zeros(j),
        A_eq=np.c_[p, np.zeros(i)], b_eq=np.zeros(i),
        bounds=[(-1, 1)] * k + [(None, None)], method="highs",
    )
    block = np.c_[q.T, p.T]
    primal = linprog(
        np.r_[np.zeros(j+i), np.ones(k)],
        A_ub=np.r_[np.c_[block, -np.eye(k)],
                   np.c_[-block, -np.eye(k)]],
        b_ub=np.zeros(2*k),
        A_eq=np.r_[np.ones(j), np.zeros(i+k)][None, :],
        b_eq=[1.0],
        bounds=[(0, None)] * j + [(None, None)] * i + [(0, None)] * k,
        method="highs",
    )
    if not dual.success or not primal.success:
        raise RuntimeError({"dual": dual.message, "primal": primal.message})
    return {
        "dual_margin": float(dual.x[-1]),
        "primal_margin": float(primal.fun),
        "duality_gap": float(primal.fun-dual.x[-1]),
        "h": dual.x[:-1].tolist(),
        "null_score_means": (p @ dual.x[:-1]).tolist(),
        "alternative_score_means": (q @ dual.x[:-1]).tolist(),
        "primal_alternative_weights": primal.x[:j].tolist(),
        "primal_null_coefficients": primal.x[j:j+i].tolist(),
    }


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def binary_information(delta):
    if delta == 1:
        return math.log(2)
    return ((1+delta)*math.log1p(delta)+(1-delta)*math.log1p(-delta))/2


def worked_example(with_scipy=True):
    p = [
        [F(2, 5), F(3, 10), F(1, 5), F(1, 10)],
        [F(1, 10), F(1, 5), F(3, 10), F(2, 5)],
    ]
    q = [
        [F(2, 5), F(1, 10), F(1, 10), F(2, 5)],
        [F(7, 20), F(3, 20), F(2, 5), F(1, 10)],
    ]
    h = [F(17, 31), F(-1), F(11, 31), F(3, 31)]
    delta = F(6, 31)
    weights = [F(13, 31), F(18, 31)]
    coefficients = [F(-26, 31), F(-11, 31)]
    residual = [
        sum((weights[j]*q[j][k] for j in range(2)), F(0))
        + sum((coefficients[i]*p[i][k] for i in range(2)), F(0))
        for k in range(4)
    ]
    null_means = [dot(pi, h) for pi in p]
    alternative_means = [dot(qj, h) for qj in q]
    check(null_means == [0, 0], "Null score means")
    check(alternative_means == [delta, delta], "Alternative score means")
    check(all(abs(x) <= 1 for x in h), "Score bound")
    check(residual == [0, -delta, 0, 0], "Signed primal residual")
    check(sum(abs(x) for x in residual) == delta, "Primal variation norm")
    check(all(w >= 0 for w in weights) and sum(weights) == 1, "Mixture weights")
    conditional_success = [(1+x)/2 for x in h]
    null_success = [dot(pi, conditional_success) for pi in p]
    alternative_success = [dot(qj, conditional_success) for qj in q]
    check(null_success == [F(1, 2), F(1, 2)], "Null binary success")
    check(alternative_success == [F(37, 62), F(37, 62)], "Alternative binary success")
    # The conditional expectation of the binary e-variable is exact but, in
    # general, is not pivotal. Jensen gives at least as much expected log power.
    conditional_mean_e = [1+delta*x for x in h]
    check([dot(pi, conditional_mean_e) for pi in p] == [1, 1], "Conditional e exactness")
    mean_e_logpowers = [
        sum(float(qj[k])*math.log(float(conditional_mean_e[k])) for k in range(4))
        for qj in q
    ]
    competitor = [F(19, 15), F(1, 2), F(6, 5), F(31, 30)]
    competitor_means = [dot(pi, competitor) for pi in p]
    check(competitor_means == [1, 1], "Competitor exactness")
    competitor_loggrowth = [
        sum(float(qj[k])*math.log(float(competitor[k])) for k in range(4))
        for qj in q
    ]
    check(min(competitor_loggrowth) > binary_information(float(delta)), "Competitor comparison")
    return {
        "exact_certificate": {
            "P": [[str(x) for x in row] for row in p],
            "Q": [[str(x) for x in row] for row in q],
            "delta": str(delta), "h": list(map(str, h)),
            "alternative_mixture": list(map(str, weights)),
            "null_span_coefficients": list(map(str, coefficients)),
            "signed_residual": list(map(str, residual)),
            "conditional_success_probabilities": list(map(str, conditional_success)),
            "null_success_probabilities": list(map(str, null_success)),
            "alternative_success_probabilities": list(map(str, alternative_success)),
            "binary_e_values": [str(1+delta), str(1-delta)],
            "binary_guaranteed_loggrowth": binary_information(float(delta)),
            "conditional_mean_e_values": list(map(str, conditional_mean_e)),
            "conditional_mean_loggrowth": mean_e_logpowers,
            "rational_certificate_verified": True,
        },
        "optional_primal_and_dual_linear_programmes": solve_margin(p, q) if with_scipy else "Not run (--no-scipy)",
        "rational_nonpivotal_exact_competitor": {
            "e_values": list(map(str, competitor)),
            "alternative_loggrowth": competitor_loggrowth,
            "null_expectations": list(map(str, competitor_means)),
            "status": "Exact feasible competitor; log values evaluated numerically; no optimality claimed",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-scipy", action="store_true", help="Run only the standard-library rational certificate")
    args = parser.parse_args()
    with_scipy = not args.no_scipy
    output = {
        "python": platform.python_version(), "example": worked_example(with_scipy),
    }
    if with_scipy:
        import numpy as np
        import scipy
        output.update(numpy=np.__version__, scipy=scipy.__version__)
    print(json.dumps(output, indent=2))
