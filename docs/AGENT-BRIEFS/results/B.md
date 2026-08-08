# Brief B — result

**Track:** Contour pilot chat (hammer2 + guard)  
**Date:** 2026-07-29  
**Repo:** `/Users/valentin/Projects/neurolab`

## Files changed

| File | Change |
|---|---|
| `docs/PILOT-CONTOUR-CHAT.md` | **new** — what ships, 20/20 cite, how to run, demo script, guard vs model, not-claimed, sandbox ask link, smoke checklist |
| `eval/results/pilot-contour-smoke.md` | **new** — filled host smoke (Mac Metal) |
| `models/outpost-tiny/CARD.md` | hygiene: demo bar = hammer2 + guard 20/20; hammer GGUF row; no micro/diverse promote |
| `docs/INDEX.md` | link to PILOT-CONTOUR-CHAT |
| `AGENTS.md` | map row for pilot pack |
| `config/sovereign.tiny-hammer.toml` | comment: pilot bar + pointer to pack doc (paths/guard unchanged) |
| `STATUS.md` | Session log entry only (no full rewrite) |

**Not done (forbidden):** new LoRA train, locked-base change, Commercial runtime edits, GGUF commit.

## Smoke

**Ran** on this host (Mac Metal).

- GGUF present · 1.8G  
- `sovereignd` + `config/sovereign.tiny-hammer.toml` · `:8096`  
- `model_loaded=true` · `active_model=outpost-tiny-hammer`  
- `[contour_guard] enabled = true`  
- Canned trio PASS: refuse ChatGPT (`ru_refuse_cloud`) · formal 2 sentences (`ru_formal`) · VPC allow (model)

Details: `eval/results/pilot-contour-smoke.md`.

## Demo one-liner (for human)

> Hammer2 + contour_guard is the pilot contour chat bar: **20/20** — runtime refuses public ChatGPT, clarifies «облако», and the model still allows client VPC; not Mid, not Grok.

## Next step (human)

Commercial pack / customer wording — use Commercial `DEMO-SCRIPT.md` + `DEMO-VERIFICATION.md` §2.7; do not invent GTM claims beyond STATUS Done.
