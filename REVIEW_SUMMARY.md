# Review summary (public, 0.1.0-candidate)

This is an internal, AI-assisted review record, not peer review. Five reviewer roles (editor, methodology, domain,
perspective, devil's advocate) read the first draft with its sources; a second AI model carried out an adversarial
review; the lead replayed the checks from a fresh copy. One revision round followed, with an extension. The revision was
then checked by a re-review, a proof audit of every new or rewritten proof, and an audit of the new proofs by the second
AI model. No reviewer or replay found a mathematical error, and every load-bearing number reproduced.

## Objections and how they were handled

| Objection | Disposition |
|---|---|
| Positioning: the draft did not say what it settles relative to Zhang, Ramdas and Wang | The abstract and introduction state that Theorem 3.1 proves the "if" direction of Conjecture 6.9 (print numbering) in bounded form, that the "only if" direction fails for unbounded e-variables by prior examples (Ramdas-Wang Example 3.15; Ram-Larsson-Ruf-Ramdas Example 5.1), and Corollary 3.4 gives a transport-free proof of Theorem 6.1 (e) => (a),(b) |
| Credit for precedents: ZRW Example 6.11 (sign test) already contains the binary e-value; test randomisation and bounded-to-p conversion are in the Ramdas-Wang monograph; Lemma 2.2 follows ZRW's proof of Theorem 6.8 | Credited with theorem-level locators; the coin is described as a randomised similar test of size 1/2 and the bet as a Kelly bet; the contribution is stated as the infinite-family route with the best guarantee in delta |
| Missing related work (He-Cheng on asymptotically lossless pivotal e-values; classical similar tests, Kraft-Le Cam separation, comparison of experiments, Kelly; the companion release) | Cited and compared in the introduction |
| Mixed print/arXiv numbering of Zhang, Ramdas and Wang | Print numbering used throughout, arXiv v4 numbers given once in parentheses; the published version was obtained and read |
| Tone of the tightness counterexample | Stated as a correction of one sentence; the main criterion of Theorem 6.8 is unaffected |
| "Sharp" was ambiguous | "Best guarantee depending on delta alone" (Theorem 3.2, Remark 3.3); "sharp margins" dropped from the title |
| Proof hygiene (finiteness in the truncation identity, openness in Proposition 5.3, where independence of the randomisation is assumed, an almost-sure finiteness hypothesis in Proposition 6.2, the derivative of I, notation collisions) | Corrected; Proposition 6.2 now uses a tail-sum bound E tau >= n(1 - alpha) + alpha |
| Readability: the draft assumed the reader knew e-values and the conjecture; process prose | New plain introduction (definitions, what was known, what is new, the idea in one paragraph, roadmap); each section opens with what it does; author line "Anonymous" and an AI-use statement |
| Extension: what does pivotality cost? | Done: pivotal statistics see only the closed null span (Proposition 4.3); an example where pivotality removes all e-power (Theorem 4.5, Remark 4.6); the necessary condition is not sufficient (Lemma 4.7, Example 4.8); the conjecture holds under weak compactness (Corollary 5.4); the four-state example now compares the binary pivot, a better pivotal e-variable and the exact optimum (Section 7) |
| Points from the verification round (the subspace used in Theorem 4.5, "free" wording, variation norm versus total variation, the Section 7 pivotal optimum via a ray reduction, description of Larsson-Ruf-Ramdas Theorem 1.8, several precise locators and docstrings) | Corrected before freezing |

## Not attempted (recorded as open questions in Section 8)

A formula for the optimal pivotal e-variable in general; a geometric characterisation of unbounded exact pivotal
existence; pointwise positivity of e-power for infinite alternative families; n-observation rates for infinite families;
computation of the separating score for infinite families. Three classical references on similar tests and experiments
that were not read are not cited.
