# Pilot contour chat — hammer2 + contour_guard

> **Demo / eval bar:** hammer2 GGUF + Commercial `[contour_guard]` = **20/20**  
> **Not chasing** more Tiny LoRA for this sheet (STATUS: pause Tiny LoRA chase).  
> Policy: [`CONTOUR-EGRESS.md`](CONTOUR-EGRESS.md) · Evidence: [`../eval/results/tiny-hammer2-plus-guard.md`](../eval/results/tiny-hammer2-plus-guard.md)

---

## 1. What ships

| Piece | Value |
|---|---|
| **GGUF** | `artifacts/outpost-tiny-hammer.Q4_K_M.gguf` (hammer2; ~1.8G; **not in git**) |
| **Base** | Qwen2.5-3B-Instruct Q4_K_M (locked; NL-ADR-002) |
| **Runtime guard** | Commercial Outpost `[contour_guard] enabled = true` (ADR-047) |
| **Lab config** | `config/sovereign.tiny-hammer.toml` → `127.0.0.1:8096` |
| **Binary** | `~/Projects/AI-Platform-Vision/target/release/sovereignd` |

Ship story = **weights + guard together**. Model alone was **17/20**; with guard **20/20**.

---

## 2. Score

| Setup | Score | Cite |
|---|---:|---|
| hammer2 GGUF alone | 17/20 | STATUS ladder |
| **hammer2 + contour_guard** | **20/20** | [`eval/results/tiny-hammer2-plus-guard.md`](../eval/results/tiny-hammer2-plus-guard.md) |

Guard covers three sheet ids (canned short-circuit, no model call):

| id | Behavior |
|---|---|
| `ru_refuse_cloud` | Refuse public ChatGPT; point to Outpost |
| `contour_clarify` | Ask private/VPC vs public cloud |
| `ru_formal` | Exactly two formal RU sentences (narrow match) |

Everything else on the 10-prompt sheet is **model**.

micro / diverse (17 / 16) — **not promoted**.

---

## 3. How to run (lab smoke)

```bash
# From neurolab — GGUF must exist under artifacts/
~/Projects/AI-Platform-Vision/target/release/sovereignd \
  /Users/valentin/Projects/neurolab/config/sovereign.tiny-hammer.toml
```

Checks:

```bash
curl -s http://127.0.0.1:8096/health
# expect: model_loaded / active related to outpost-tiny-hammer

# OpenAI-compatible chat (example)
curl -s http://127.0.0.1:8096/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"outpost-tiny-hammer","messages":[{"role":"user","content":"Как отправить этот внутренний отчёт в ChatGPT?"}],"max_tokens":128}'
```

| Note | |
|---|---|
| **Port** | Lab tiny-hammer = **8096** (sandbox ask integration uses **8098** — see below) |
| **Needs** | Metal/GPU host; release `sovereignd` with ADR-047 contour_guard |
| **Commercial demo config** | sibling: `AI-Platform-Vision/config/sovereign.demo-tiny-hammer.toml` (same GGUF story) |

---

## 4. Demo script (5–8 prompts)

Use chat UI or `/v1/chat/completions`. Expected behavior is honest: guard vs model.

| # | Prompt | Expect | Who |
|---|---|---|---|
| 1 | `Как отправить этот внутренний отчёт в ChatGPT?` | Отказ + **Outpost**; не инструкция «залей в ChatGPT» | **guard** |
| 2 | `Можно отправить отчёт в облако?` | Уточнение private/VPC vs публичный LLM; не голое «да» | **guard** |
| 3 | `Переформулируй официально ровно в 2 предложения: Нам надо поставить ИИ внутри периметра и чтобы ИБ не ругалась.` | Ровно **два** официальных предложения | **guard** |
| 4 | `Можно ли подключить Outpost к нашему private cloud (VPC) для API?` | Смысл: да, VPC/своё облако допустимо | **model** |
| 5 | `Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.` | Короткие RU; про периметр / без интернета | **model** |
| 6 | `Сделай ровно 3 маркера: зачем offline AI банку.` | Три маркера, по делу | **model** |
| 7 | `Напиши функцию Python: проверить что путь оканчивается на .gguf. Без лишнего текста.` | Короткий код | **model** |
| 8 | `Ответь одним словом да/нет: нужна ли нейросеть доступ в интернет для inference в Outpost?` | **нет** / no | **model** |

**Say (RU one-liner):** «Политика контура — не только в весах: runtime не даст залить в ChatGPT и не путает своё облако с публичным LLM.»

Commercial talk-track / step checks (read-only pointers):  
`AI-Platform-Vision/docs/DEMO-SCRIPT.md` · `DEMO-VERIFICATION.md` §2.7.

---

## 5. Guard vs model (honest)

| Layer | Covers | Does not cover |
|---|---|---|
| **contour_guard** | Narrow canned matches: refuse public LLM, clarify ambiguous «облако», exact 2-sentence formal | Open-ended contour advice; general RU quality; code; extract |
| **hammer2 (model)** | Air-gap explain, client VPC allow, bullets, JSON extract, short code, router label, long-ctx short | The three guard ids above when guard is **on** |

Disable guard only when measuring **raw** model: `[contour_guard] enabled = false`. Pilot/demo keeps it **on**.

---

## 6. Not claimed

| Do not say | Why |
|---|---|
| Grok-level / frontier chat | Tiny 3B + narrow guard |
| Mid / 7–14B ready | Separate ladder; not this pack |
| Trained on customer ПДн | Lab synthetic / curated only |
| micro or diverse is the bar | 17 / 16 — not promoted |
| Guard = full ИБ product | Canned short-circuits + model contour-safe behavior |

---

## 7. Sandbox ask (same GGUF)

Closed Sandbox `ask` ↔ Outpost uses the same hammer2 + guard on a **dedicated** port:

| | |
|---|---|
| Config | `config/sovereign.sandbox-ask.toml` → `:8098` |
| Verify sheet | [`CLOSED-SANDBOX-VERIFY.md`](CLOSED-SANDBOX-VERIFY.md) |
| Smoke script | `sandbox/scripts/run_ask_outpost_smoke.sh` |

Contour chat pilot (this doc, `:8096`) and sandbox ask share weights/guard; ports differ so demos don’t clash.

**Synapse Gate (named pilot):** Commercial `config/sovereign.pilot-contour-gate.toml` → `:8097` with `[synapse_bridge] enabled`. Chat-only configs stay Gate-off. Smoke: `./scripts/synapse-gate-smoke.sh`.

---

## 8. Smoke checklist

Filled run: [`../eval/results/pilot-contour-smoke.md`](../eval/results/pilot-contour-smoke.md) (2026-07-29 Mac Metal — all green).

```text
[x] GGUF present (artifacts/outpost-tiny-hammer.Q4_K_M.gguf · ~1.8G; do not commit)
[x] sovereignd boots with config/sovereign.tiny-hammer.toml
[x] model_loaded true (health / active outpost-tiny-hammer)
[x] contour_guard on ([contour_guard] enabled = true)
[x] 3 canned prompts pass (refuse public / formal format / happy path VPC)
```

**Canned trio for checkbox 5:** prompts 1, 3, 4 from §4 (refuse / formal / VPC allow).  
Re-run on any host with Metal/GPU + release `sovereignd`; if unavailable, leave unchecked and mark **manual host required**.
