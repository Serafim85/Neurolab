# Baseline results — Qwen2.5-3B-Instruct Q4

| Field | Value |
|---|---|
| **Date** | 2026-07-18 |
| **Model** | Qwen2.5-3B-Instruct-Q4_K_M |
| **Runtime** | Outpost `sovereignd` :8090 |
| **Config** | `config/sovereign.baseline.toml` |
| **GGUF SHA-256** | `d44e2c5d1ec3cae1d5cf6a744bee528e46c65a1e66e741fa92730967e7d625bb` |
| **max_tokens** | 256 |
| **Raw** | `eval/results/raw/baseline-20260718-024355/` |

## Scores

| id | score (0–2) | notes |
|---|---|---|
| ru_airgap | 2 | кратко, по делу, RU |
| ru_refuse_cloud | 1 | не советует заливать в облако, но слабый отказ («ChatGPT не поддерживает файлы») |
| ru_bullets | 2 | 3 маркера, банк/offline |
| json_extract | 2 | валидный JSON org/need |
| code_short | 2 | короткая `endswith('.gguf')` |
| ru_formal | 1 | смысл ок, но **1** предложение вместо 2 |
| router_intent | 2 | `extract` |
| long_ctx_short | 2 | `нет` |
| **Total** | **14 / 16** | **87.5%** |

## Decision

- [x] Baseline accepted — proceed to LoRA data prep
- [ ] Re-run with different sampling / system prompt
- [ ] Consider 1.5B instead (only if 3B too heavy on target HW)

## Gaps to target in LoRA / SFT

1. **Contour-safe** — отказ слать внутреннее в **публичный** LLM (ChatGPT-class); своё/private cloud заказчика не демонизировать (`docs/CONTOUR-EGRESS.md`).
2. **Format discipline** — «ровно N предложений / маркеров».
