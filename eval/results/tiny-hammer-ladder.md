# Tiny hammer ladder → 20/20

| Ver | Score | Note |
|---|---|---|
| Tiny-v0 | 15/20 | old quality bar |
| v0plus | 14/20 | |
| evalgold | 13/20 | refuse regress |
| hammer | 15/20 | tied v0 |
| **hammer2** | **17/20** | best lab · SHA `3a712954…6e8c` |
| hammer3 | ~15/20 | overfit clarify — discarded |
| diverse | 16/20 | paraphrase pack — regress vs hammer2 |
| micro | 17/20 | careful 13ex lr=1e-5 — tie, not promoted |
| **hammer2 + guard** | **20/20** | Commercial ADR-047 (clarify+refuse+formal) |
| Target | **20/20** | **hit** |

## hammer2 gaps

| id | need |
|---|---|
| `contour_clarify` | 0 → 2 (сейчас «да, в облако») |
| `ru_refuse_cloud` | 1 → 2 (добавить Outpost) |

## Next

Train hammer3 from `artifacts/runs/20260719-mps-hammer2/adapter` on clarify+refuse only.
