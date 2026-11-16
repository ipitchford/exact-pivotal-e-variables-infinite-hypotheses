# Exact pivotal e-variables for infinite hypotheses: a binary construction and what pivotality costs

*A fair coin built from any separating score gives exact, pivotal evidence with the best possible guarantee; for unbounded evidence, pivotality can cost everything*

Version 0.1.0-candidate. DOI [10.5281/zenodo.24268845](https://doi.org/10.5281/zenodo.24268845) (all versions:
[10.5281/zenodo.24268844](https://doi.org/10.5281/zenodo.24268844)). Creator: Anonymous. Release page:
https://evidencepress.org/releases/exact-pivotal-e-variables-infinite-hypotheses/

**Status: unrefereed research candidate.** The checking behind it is internal AI-assisted review and computation, not
peer review (see "How it was checked" below).

## What this is about

**E-values.** An e-value is a number that measures evidence against a hypothesis, like the payoff of a fair bet against
it: if the hypothesis is true, its average is at most one, so large values are unlikely by chance. Its quality is how
fast evidence grows when the hypothesis is false, measured by the expected logarithm under the alternative (the
"e-power").

**Two stronger demands.** Often the hypothesis being tested (the null) is not one distribution but a whole family, for
example because of unknown nuisance parameters. Then two stronger properties are natural. An e-value is *exact* if its
average is exactly one under every null distribution. It is *pivotal* if its whole distribution is the same under every
null, so its behaviour under the null is known exactly even though the true null is not.

**What was known.** For finitely many distributions, Zhang, Ramdas and Wang (Annals of Statistics, 2024) showed that
exact pivotal e-values with positive e-power exist exactly when the alternatives stay away from the linear span of the
nulls; their proof used optimal transport. For infinite families they characterised *bounded exact* e-values (Theorem
6.8 in the print numbering) and conjectured a pivotal version (Conjecture 6.9).

**What is new.**

1. *A binary pivot* (Theorems 3.1 and 3.2, Corollary 3.4). Take any bounded score that averages zero under every null and
   at least delta under every alternative. Flip a coin whose heads probability is (1 + score)/2. It is a fair coin under
   every null and a biased coin under every alternative. Bet a fraction delta of your stake on heads. The result is an
   exact, pivotal e-value whose e-power is at least the information in a coin with bias delta,
   I(delta) = [(1 + delta) log(1 + delta) + (1 - delta) log(1 - delta)]/2, and no guarantee based on delta alone can do
   better. This proves the "if" half of the conjecture and gives a short, transport-free proof of the step of the finite
   theorem that produces exact pivotal p- and e-values. The ingredients (similar tests, randomisation, Kelly betting) are
   classical; the contribution is that this simple route works for infinite families, with the best possible guarantee.
2. *Pivotality can cost everything for unbounded e-values* (Section 4). A pivotal statistic cannot tell apart an
   alternative that lies in the closed span of the nulls (Proposition 4.3). There is an example with one alternative and a
   closed convex family of nulls in which an exact e-value grows (e-power at least (1/4) log(27/16), about 0.13) but
   every pivotal e-value is powerless (Theorem 4.5). That the conjecture's "only if" half fails for unbounded e-values
   was already known (Ramdas and Wang, Example 3.15; Ram, Larsson, Ruf and Ramdas, Example 5.1); the new point is the
   cost of pivotality itself.
3. *Compactness* (Section 5). One sentence of Zhang, Ramdas and Wang's Theorem 6.8, saying that tightness of the
   alternatives makes a simpler test of the criterion equivalent, is false, even on a compact space (Theorem 5.1). Weak
   compactness in L^1 is the right condition (Proposition 5.2), and under it the conjecture holds in both directions
   (Corollary 5.4). Their main criterion is unaffected: this corrects one sentence, not the paper.
4. *Illustrations* (Sections 6 and 7). Sequential consequences for detection time, and a four-state example with an
   exact rational certificate (delta = 6/31): the binary coin guarantees about 0.019, the best pivotal e-value reaches
   about 0.039, and the best exact e-value about 0.056. In this example pivotality costs about thirty per cent of the
   exact optimum, and the binary construction recovers about half of the pivotal optimum.

**Limits.** The results concern one observation; sequential results follow only by repeating it. There is no general
formula for the best pivotal e-value, and no full characterisation for unbounded pivotal e-values (a uniform-integrability
criterion and a strict two-sided bracket are given). The separating score comes from functional analysis; for finite
tables it is computable by linear programming, but for infinite families computing it is a separate task. The binary
guarantee is a worst case and can be well below what is achievable in a given problem.

**Credit.** The existence theorem for finite families, the closure criterion for bounded exact e-values and Conjecture
6.9 are due to Zhang, Ramdas and Wang, whose sign-test example (Example 6.11) is a special case of the binary pivot. The
coin is a randomised similar test of size one half (Lehmann and Romano) and the bet is a Kelly bet. He and Cheng show
that for finitely many nulls pivotality is asymptotically free. A companion release,
[The cost of exact calibration for growing Gaussian null families](https://evidencepress.org/releases/exact-calibration-gaussian-null-families/)
([doi:10.5281/zenodo.24252837](https://doi.org/10.5281/zenodo.24252837)), quantifies the cost of exactness for growing
Gaussian null families.

## What is in this package

| File | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (16 pages). Section 1 is a plain introduction with a roadmap; Section 8 states the scope and open questions. |
| [verification/checks/finite_example.py](verification/checks/finite_example.py) | The margin as a pair of linear programmes, and the exact rational certificate for the four-state example (delta = 6/31). Output [verification/outputs/finite_example.json](verification/outputs/finite_example.json). |
| [verification/checks/pivot_comparison.py](verification/checks/pivot_comparison.py) | The four-state comparison: the ternary pivotal kernel (exact rational laws), the ray reduction for the pivotal optimum, a grid linear programme over pivotal kernels and the exact optimum. Output [verification/outputs/pivot_comparison.json](verification/outputs/pivot_comparison.json). |
| [verification/checks/extension_checks.py](verification/checks/extension_checks.py) | Exact and high-precision checks of the constants in Sections 4 to 6 (Theorem 4.5, Remark 4.6, Example 4.8, Propositions 6.1 and 6.2). Output [verification/outputs/extension_checks.json](verification/outputs/extension_checks.json). |
| [verification/requirements.txt](verification/requirements.txt), [ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md) | Environment and the release replay. |
| [PRIOR_ART.md](PRIOR_ART.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) | Dated prior-art record; contribution map, sources read and limitation triage; objections from internal review and how they were handled. |
| [AI_INDEX.md](AI_INDEX.md) | Machine-oriented map of claims, evidence and limits. |
| [refs.bib](refs.bib) | Bibliography built from Crossref, arXiv and DataCite records. |
| [LICENSE.md](LICENSE.md), [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json), [MANIFEST.sha256](MANIFEST.sha256) | Licences, citation metadata and SHA-256 sums. |

## Reproduce the checks

From the package root, with [uv](https://docs.astral.sh/uv/) (each script prints its results as JSON; about a second each):

```
UV="uv run --no-project --python 3.12 --with numpy==2.3.5 --with scipy==1.17.0 --with mpmath==1.3.0"
for s in finite_example pivot_comparison extension_checks; do
  $UV python -I -B -O verification/checks/$s.py > $s.json || echo "FAILED: $s"
done
```

Every script raises an exception (exit 1) if any check fails and uses no `assert`, so the checks stay active under
`python -O`. The outputs match the recorded files apart from the interpreter version field and, on other platforms,
possibly the last digits of linear-programming floats and of the optimiser's maximiser (not quoted in the paper). `finite_example.py --no-scipy` runs only the standard-library
rational certificate. The computations check the stated constants and the worked example; the general statements rest on
the written proofs.

## How it was checked

Internal, AI-assisted review only: five reviewer roles, an adversarial review and an audit of the new proofs by a second
AI model, clean replays of the scripts, one revision round with an extension, a re-review and a proof audit. This is not
peer review, independent reproduction or formal verification. The paper's AI-use statement describes the use of AI.

## Licence

Text, paper and data: CC0-1.0. Code (`verification/checks/*.py`, `.github/workflows/*.yml`): MIT. See
[LICENSE.md](LICENSE.md).
