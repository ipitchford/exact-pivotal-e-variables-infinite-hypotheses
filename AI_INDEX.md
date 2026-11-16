# AI index: Exact pivotal e-variables for infinite hypotheses (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What this
is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is a plain
introduction with what was known, what is new, the idea in one paragraph and a roadmap). DOI 10.5281/zenodo.24268845
(concept 10.5281/zenodo.24268844). Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

Null family P and alternative family Q on (Omega, F), dominated by a probability R; densities identified with measures.
E >= 0 is an e-variable if E_P E <= 1 for all P in P; exact if E_P E = 1 for all P; pivotal if its law is the same under
all P. Uniform e-power g_Q(E) = inf_{Q in Q} E_Q log E. S = L^1-closed span of the null densities, C = convex hull of the
alternative densities; margin delta = dist_{L^1(R)}(0, closure(S + C)), a variation-norm distance (twice total
variation). Lemma 2.2: delta = max over |h| <= 1 with E_P h = 0 for all P of inf_Q E_Q h. Joint atomlessness: an
independent uniform randomisation is available. I(d) = D(Bern((1+d)/2) || Bern(1/2)) =
[(1+d)log(1+d) + (1-d)log(1-d)]/2. ZRW = Zhang, Ramdas and Wang, Ann. Statist. 52(5) 2024, print numbering (arXiv v4
numbers Theorem 6.8, Conjecture 6.9 and Example 6.11 as 6.7, 6.8, 6.10).

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A | Under domination and joint atomlessness: delta > 0 iff a bounded exact e-variable with g > 0 exists iff a bounded exact pivotal one exists iff an exact p-variable T with Q(T <= t) >= t + eta min(t, 1-t) exists; E_delta = 1 + delta(2B - 1), B = 1{U <= (1+h)/2}, has g_Q(E_delta) >= I(delta) | Theorem 3.1 | written proof; the coin is a randomised similar test of size 1/2 (Lehmann-Romano), the bet a Kelly bet; ZRW Example 6.11 is a special case; Lemma 2.2 follows ZRW's proof of Theorem 6.8 |
| B | For each d in (0,1] there is an experiment with margin d in which every exact e-variable (pivotal or not, bounded or not) has g <= I(d) | Theorem 3.2 | written proof; "best" means best as a function of delta alone (Remark 3.3) |
| C | "If" direction of ZRW Conjecture 6.9 (bounded form); with "bounded" added the conjecture holds in both directions; transport-free proof of ZRW Theorem 6.1 (e) => (a),(b) for finite families | Corollary 3.4 | written proof |
| D | A pivotal statistic X satisfies d_TV(Q^X, pi) <= dist_{L^1}(Q, S); hence an exact pivotal e-variable with g > 0 forces conv Q disjoint from the closed span | Proposition 4.3, Corollary 4.4 | written proof |
| E | Pivotality is not free for unbounded e-variables: a dominated, jointly atomless experiment with a convex variation-closed null family and one alternative Q, with an unbounded exact E having E_Q log E >= (1/4)log(27/16) (about 0.1308; computed 0.2512) while every pivotal e-variable has e-power <= 0 | Theorem 4.5; continuous variant Remark 4.6 (D(Q||Unif) = 1 - log 2) | written proof; that the conjecture's "only if" direction fails for unbounded e-variables is prior work (Ramdas-Wang Example 3.15; Ram-Larsson-Ruf-Ramdas Example 5.1) |
| F | Unbounded pivotal problem: uniform-integrability tail criterion (Theorem 4.1); chi-square obstruction (Lemma 4.7, extends ZRW arXiv Example A.4 to all e-variables); strict two-sided bracket | Theorem 4.1, Proposition 4.2, Lemma 4.7, Example 4.8 | written proof; no geometric characterisation |
| G | The final sentence of ZRW Theorem 6.8 (tightness of Q makes the closure condition equivalent to disjointness of the closed span and the closed convex hull) is false, even on a compact space; weak compactness in L^1 is a correct replacement; under weak compactness of conv Q, Conjecture 6.9 holds in both directions | Theorem 5.1, Proposition 5.2, Proposition 5.3, Corollary 5.4 | written proof; the main criterion of ZRW Theorem 6.8 is unaffected |
| H | Sequential consequences: escaping tail sup = 2 + e^{-2a}/8; expected detection delay at least n(1 - alpha) + alpha; bounded-pivot sequential test | Propositions 6.1-6.3 | written proof |
| I | Four-state example: delta = 6/31 with exact primal-dual certificate; binary guarantee I(6/31) = 0.0188492; ternary pivotal kernel with gains 0.039318, 0.039066; pivotal optimum 0.0391954 (one-parameter ray reduction, numerical grid); exact optimum about 0.0556 (exact competitor F gives 0.056589, 0.054972) | Section 7 | rational identities exact; logarithms and optima numerical |

Not claimed: a formula for the optimal pivotal e-variable in general; a geometric characterisation of unbounded exact
pivotal existence; pointwise (rather than uniform) positivity of e-power; n-observation rates for infinite families;
computation of the separating score for infinite families.

## Evidence files

- [verification/checks/finite_example.py](verification/checks/finite_example.py) ->
  [verification/outputs/finite_example.json](verification/outputs/finite_example.json): exact Fraction certificate
  (null means 0, alternative means 6/31, signed residual, coin probabilities 24/31, 0, 21/31, 17/31; 37/62 under both
  alternatives), the LP primal and dual, and the exact non-pivotal competitor.
- [verification/checks/pivot_comparison.py](verification/checks/pivot_comparison.py) ->
  [verification/outputs/pivot_comparison.json](verification/outputs/pivot_comparison.json): ternary kernel laws (exact),
  gains, kernel saddle value, 301-point ray reduction with a monotonicity check, grid LP 0.0391797, exact optimum
  0.0556007 (SLSQP, 30 fixed seeds).
- [verification/checks/extension_checks.py](verification/checks/extension_checks.py) ->
  [verification/outputs/extension_checks.json](verification/outputs/extension_checks.json): exactness for n = 2..2000,
  (1/4)log(27/16), E_Q log E, 1 - log 2, chi-square identity, Section 6 constants.
- [verification/requirements.txt](verification/requirements.txt), [ENVIRONMENT.txt](ENVIRONMENT.txt),
  [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md): environment and the release replay (normal and `python -O`, negative controls).
- [PRIOR_ART.md](PRIOR_ART.md): dated prior-art record. [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md): internal review objections
  and dispositions. [RESEARCH_GATES.json](RESEARCH_GATES.json): contribution map, sources read in full, searches and
  limitation triage.
- [refs.bib](refs.bib): bibliography from Crossref, arXiv and DataCite records. [LICENSE.md](LICENSE.md): CC0-1.0 text
  and data, MIT code. [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json): citation metadata. CI:
  [.github/workflows/replay.yml](.github/workflows/replay.yml) (blocking: manifest, all checks under -O compared with the
  recorded outputs, two negative controls). [MANIFEST.sha256](MANIFEST.sha256): SHA-256 of every file.

## Limits

No human peer review, independent human reproduction or formal verification. The computations test the stated constants
and the worked example; the general statements rest on the written proofs. The pivotal optimum of Section 7 rests on a
one-dimensional numerical grid. Seven of the sixteen cited works are arXiv preprints. Priority rests on a bounded search.
