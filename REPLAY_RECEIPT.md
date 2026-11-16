# Replay receipt (release 0.1.0-candidate, 16 November 2026)

The scripts were rerun by the publisher from fresh copies of the approved candidate before the release was frozen, with
the package copy as working directory, CPython 3.12.11 and the pinned requirements (see ENVIRONMENT.txt).

| Run | Mode | Result |
|---|---|---|
| `finite_example.py` | normal and `-O -I -B` | exit 0; output identical to `verification/outputs/finite_example.json` apart from the interpreter version field (recorded under 3.11.14); delta 6/31, rational certificate verified, binary guarantee 0.018849221152617 |
| `pivot_comparison.py` | normal and `-O -I -B` | exit 0; output byte-identical to `verification/outputs/pivot_comparison.json` (ternary gains 0.0393180, 0.0390658; kernel and ray optimum 0.0391953681; grid LP 0.0391797; exact optimum 0.05560; F gains 0.056589, 0.054972) |
| `extension_checks.py` | normal and `-O -I -B` | exit 0; output byte-identical to `verification/outputs/extension_checks.json` (lower bound 0.1308120; E_Q log E 0.2512319; 1 - log 2 = 0.3068528; all `*_ok` true) |
| negative control: `finite_example.py` with delta 6/31 changed to 7/31 | `-O -I -B` | exit 1 (ArithmeticError: Alternative score means) |
| negative control: `extension_checks.py` with the lower bound (1/4) log(27/16) changed to (1/3) log(27/16) | `-O -I -B` | exit 1 (ArithmeticError: lower bound identity) |

No script uses `assert`: every check raises `ArithmeticError`, so the checks stay active under `-O`.

After this replay only the title-page version/DOI line and the companion entry of the bibliography (now with its DOI and
release URL) changed in the manuscript (PDF rebuilt), together with the release records (README, metadata); no script
or recorded output changed. GitHub CI reruns all three scripts under `-O`, compares their output with the recorded files
(exact fields exactly; floats, which come from linear programmes, an optimiser and quadrature, within a declared tolerance of 1e-6 relative or 1e-9 absolute; the coordinates of the optimiser's maximiser `exact_optimum_e`, which the paper does not quote and which move by about 1e-6 between macOS and Linux, within 1e-4 absolute) and runs both negative controls (blocking).
