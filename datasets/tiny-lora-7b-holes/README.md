# 7B holes pack (NL-ADR-028)

One lever after first 7B hammer LoRA scored **12/20** model-alone / **16/20** +guard
(`eval/results/tiny-7b-hammer.md`). Guard already covers refuse + clarify.

Targets (unique paraphrases, not 10× one eval string — hammer3 overfit):

| tag | Eval id | Intent |
|---|---|---|
| `format_short` | `long_ctx_short` | one word: inference in Outpost does **not** need internet |
| `format_bullets` | `ru_bullets` | exactly 3 RU bullets; stop; no other language |
| `contour_allow_client` | `contour_allow_client` | VPC/private cloud OK; **no** public egress required |

Light anchors (`json_code`, `format_sentences`, `general_ru`) keep ids that already scored 2.

Train: resume `artifacts/runs/20260813-mlx-hammer2/adapter`, same LoRA layers=16, lr=1e-5.
