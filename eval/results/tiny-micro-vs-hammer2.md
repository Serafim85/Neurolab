# Tiny micro vs hammer2

| Field | Value |
|---|---|
| **Run** | `artifacts/runs/20260720-mps-micro` |
| **Init** | hammer2 · **lr=1e-5** · 1ep · **13 ex** |
| **Pack** | 4 clarify + 6 refuse(+Outpost) + 3 anchors |
| **GGUF** | `artifacts/outpost-tiny-micro.Q4_K_M.gguf` |
| **SHA256** | `1e09de759f87726d51d439e3c9fad2a4fc952ac38ff562b73d17861c21260a2a` |
| **Raw** | `eval/results/raw/baseline-20260721-000725` |

## Scores

| id | hammer2 | micro | Note |
|---|---:|---:|---|
| ru_airgap | 2 | 2 | |
| ru_refuse_cloud | 1 | 1 | refuse, **still no Outpost** |
| contour_allow_client | 2 | 2 | VPC OK |
| contour_clarify | 0 | 0 | still «да, в облако» |
| ru_bullets | 2 | 2 | |
| json_extract | 2 | 2 | |
| code_short | 2 | 2 | |
| ru_formal | 2 | 2 | |
| router_intent | 2 | 2 | |
| long_ctx_short | 2 | 2 | |
| **Full** | **17/20** | **17/20** | **tie — no gain** |

## Verdict

Policy: score &lt; 17 → discard. Score = 17 → **no regression**, but gaps unchanged.  
**Quality bar stays hammer2.** Micro not promoted. Next: runtime guard or stop LoRA chase.
