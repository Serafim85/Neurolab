# Neurolab STATUS

**Last updated:** 2026-08-13

> **Единственный источник правды о текущем фокусе — этот файл** (§Summary + §Next).
> `AGENTS.md` §6 и `docs/ARCHITECTURE.md` §6 — только указатели сюда; дубликаты там
> не держим, потому что они расходятся.

## Summary

| Area | State |
|---|---|
| **Best lab GGUF** | hammer2 (model alone was 17/20) |
| **Demo / eval bar** | **hammer2 + contour_guard · 20/20** (ADR-047) |
| micro / diverse | 17 / 16 — not promoted |
| **Closed Sandbox** | **D0–D4** · **P01–P05** · **by_scenario split** · Gate pilot ON |
| **Pilot chat** | pack + smoke green (`PILOT-CONTOUR-CHAT.md`) |
| **Agent-eval** | **LIVE hn + agent_format · 20/20** (`:8102`) |
| **Synapse bridge** | **v0.3** · Gate ADR-054 · **pilot-contour-gate ON** (:8097) · smoke 3/3 · SOW Approved |
| **Eval scorer** | `scripts/score_agent_eval.py` · 55/60 совпадений с ручной оценкой · repeats |
| **CI / gate** | GitHub Actions + `scripts/gate.sh` (6 шагов) · 85 sandbox + 56 root tests |
| **⚠️ Base LICENSE** | **`qwen-research` — NON-COMMERCIAL only** ([`docs/BASE-LICENSE.md`](docs/BASE-LICENSE.md)) · блокирует коммерческую поставку весов · решение человека |

### Ladder

| Ver | Score |
|---|---|
| Tiny-v0 | 15 |
| hammer2 | 17 (GGUF alone) |
| micro / diverse | 17 / 16 |
| **hammer2 + guard** | **20/20** |

**Artifact:** `outpost-tiny-hammer2.Q4_K_M.gguf` is a **byte-identical alias** of
`outpost-tiny-hammer.Q4_K_M.gguf` (SHA256 `3a7129549bf19c69…`). Ladder score columns
that differ are **eval/runtime history**, not two separate GGUFs.

GGUF (use): `artifacts/outpost-tiny-hammer.Q4_K_M.gguf`  
Runtime: Commercial Outpost `[contour_guard] enabled = true`

## Next

1. **Решение по базе (человек, блокер).** База под `qwen-research`, non-commercial;
   производные — наши LoRA-merge и пилотный GGUF. Варианты и цена — в
   [`docs/BASE-LICENSE.md`](docs/BASE-LICENSE.md) §5, черновик — NL-ADR-028 (Proposed).
   Переход на 7B (Apache-2.0) снимает вопрос; смена locked base = ADR + человек.
   **Сначала бесплатное:** проверить MLX-путь (LoRA поверх 4-бит на Apple Silicon) —
   если 7B укладывается в 16 GB, вопрос бюджета GPU не возникает вовсе.
2. ~~Дописать ADR 025–027~~ — **done** (wave 3 / J): Accepted в `DECISIONS.md`.
3. **`cli.py stress` + UI без спайкового хардкода** — brief L (slot 2).
4. **LICENSE репозитория** — три варианта в `docs/AGENT-BRIEFS/results/I.md`.
   Actions: репозиторий приватный — проверить в браузере.
5. **Перепрогнать лист 20/20 с сохранением сырья** — Metal-хост (C-05).
6. **§ Proof points в `docs/INVESTOR-NORTH-STAR.md`** — по `CLAIMS.md`; человек (`AGENTS.md` §9).
7. Дубль `hammer2` GGUF — **docs done** (alias, K); удаление с диска ~1.8 GB = human.
8. **MLX 7B probe** — brief M (slot 2); dual train-lock scaffold — brief O (slot 3).
9. Pause Tiny LoRA sheet chase · (optional) richer D4 fronts / Chip PDK-adjacent later

Сделано wave 2: автоскорер, envelope, CLAIMS, CI/gate.  
Сделано wave 3 slot 1 (cheap): ADR 025–027 · hammer2 alias docs · VERIFY/MVP → 85/CI.

## Session log

> Записи старше 2026-08-01 — в архиве [`docs/SESSIONS-2026-07.md`](docs/SESSIONS-2026-07.md)
> (перенесены 2026-08-08 без изменения текста).

### 2026-08-13 — Wave 3 slot 1 (cheap): J + K + N

- **J:** NL-ADR-025/026/027 Accepted в `DECISIONS.md`; Reserved block снят; 028 Proposed
  без изменений.
- **K:** `hammer2` зафиксирован как byte-alias `hammer` (`3a712954…`) в Ladder / CLAIMS
  C-01 / CARD Limits; GGUF с диска не удаляли.
- **N:** VERIFY + MVP: unit **85**, `gate.sh`, CI workflow; «51» остался только как история.
- Брифы L/M/O готовы на слоты 2–3. Правило экономии моделей: `01-model-economy.mdc`.
- Verify: `gate.sh` PASS · `gen_model_card.py --check` · `check_doc_links` OK.

### 2026-08-08 — NL-ADR-028 (Proposed) + 84 GB диска

- Черновик **NL-ADR-028**: locked base обязан уйти с 3B по лицензии, цель — 7B-Instruct
  (Apache-2.0 проверен и в метаданных, и в тексте `LICENSE`; 72B — другая лицензия,
  не выход). Статус Proposed: решение за человеком по `AGENTS.md` §9.
- Считая цену переезда, выяснилось, что дело **не в вычислениях**: 11 наборов по
  13–92 примера, 456 всего — вся лестница это пара GPU-часов. Упирается в память.
- **Диск: `artifacts/` занимала 216 GB**, из них незаменимого ~26 GB (12 Q4 GGUF,
  19 адаптеров по 125 МБ, base). Снёс `runs/*/trainer` — это чекпойнты процесса,
  а не результат: **освободилось 84 GB**, свободно стало 91 GB вместо 6.6 GB.
  У двух прогонов адаптера не было и веса лежали только в чекпойнтах
  (`20260719-085839`, `v1.1-nan12e4`) — спасены в `adapter-rescued/` до удаления.
- Verify после очистки: `hammer` по-прежнему `3a712954…`, 19 адаптеров и 19 `NOTES.md`
  на месте, 12 Q4 GGUF целы. Пересобираемое (`hf/` 63 GB, `*.f16.gguf` 40 GB) не тронул.
- Коллизия номеров ADR решена: 025 остаётся за треком F (уже в коде), 026/027 — за G и H.
- Следующий бесплатный шаг: проверить MLX для 7B LoRA на 16 GB.

### 2026-08-08 — Base LICENSE: не Apache-2.0 (проверено по первоисточнику)

- Трек H заметил, что upstream LICENSE не зафиксирована нигде в репозитории.
  Проверка по официальной карточке `Qwen/Qwen2.5-3B-Instruct` дала однозначный
  ответ: `license: other`, `license_name: qwen-research`, текст —
  **«FOR NON-COMMERCIAL PURPOSES ONLY»**, где Non-Commercial = research or
  evaluation only, а коммерческое использование требует отдельной лицензии
  Alibaba Cloud. **Записанное у нас «Apache-2.0» было неверным.**
- Почему это не документационная мелочь: §2.a лицензии покрывает производные
  работы. Наши LoRA-merge и GGUF — производные, включая пилотный `hammer`.
  Передача весов платящему пилоту не попадает в research/evaluation.
- 3B — исключение в линейке: 0.5B/1.5B/7B/14B/32B под Apache-2.0. То есть переход
  locked base на 7B/14B снимает вопрос целиком и уже стоит в `SCALE-PLAN` как Mid.
- Исправлено: новый [`docs/BASE-LICENSE.md`](docs/BASE-LICENSE.md) (факт, последствие,
  три варианта с ценой), ложные Apache-2.0 в `datasets/base-qwen25-3b.md` и
  `datasets/manifest-tiny-lora-v0.md`, паспорт перегенерирован, C-53 в `CLAIMS.md`
  переписана, в §7 добавлен запрет заявлять право коммерческой поставки весов.
- Verify: `rg -i apache datasets/ models/` → ложных утверждений о базе нет;
  `python3 scripts/gen_model_card.py --check`; `bash scripts/gate.sh` → PASS.
- Решение за человеком (`AGENTS.md` §9): 7B/14B, запрос лицензии, или research-only.

### 2026-08-08 — One source of truth + STATUS rotation (brief G)

- Фокус больше не дублируется: `AGENTS.md` §6 и `ARCHITECTURE.md` §6 — указатели
  на этот файл; мёртвая шкала `14/16` из §6 убрана (актуальная — `/20`)
- Ритуал `AGENTS.md` §4 «Старт» шаг 3 теперь ведёт в `STATUS.md` §Summary + §Next,
  а не в устаревший `ARCHITECTURE.md` §6; требование коммита в «Конец» не тронуто
- Листы верификации освежены: VERIFY + MVP §9 → **51 passed** (`not integration`,
  3 deselected) на 2026-08-08; integration не прогонялся (нужен Metal/GPU host +
  Commercial release `sovereignd`) — так и записано, число не выдумано
- Ротация журнала: 32 записи ≤2026-07-31 → `docs/SESSIONS-2026-07.md` (verbatim,
  diff = 0); STATUS **449 → 248 строк**; INDEX + Cursor rule обновлены
- Verify: `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"`
  → **51 passed, 3 deselected**; в VERIFY §2 появилась строка 2026-08-08,
  прежние «11 passed» остались только как история прогонов
- Остаётся вне брифа G: `README.md` §Треки и `docs/SCALE-PLAN.md` §3 всё ещё
  объявляют «сейчас» Track A / baseline 14/16, `sandbox/README.md` — «expect 11 passed»

### 2026-08-08 — Repo audit + first push in 3 weeks

- **Root risk closed:** last commit was 2026-07-19 while the log ran to 08-05 —
  4610 py LOC of `sandbox/`, all Closed Sandbox docs, eval and datasets sat
  uncommitted in a repo with **no remote**. Now 14 thematic commits pushed to
  `git@github.com:Serafim85/Neurolab.git`
- **Silent data loss found:** the hand-maintained `.gitignore` dataset allowlist
  had stopped being updated, excluding `tiny-lora-hammer2` (the flagship GGUF's
  training data), `hammer`, `hammer3`, `agent` and `eval/prompts/agent-v0.jsonl`.
  Replaced with rules — a new dataset now needs no `.gitignore` edit
- **Ritual hole closed:** session end asked for `STATUS.md` but never for a
  commit. `AGENTS.md` §4 + Cursor rule 12 now require clean `git status` + push
- Audit verdict: strengths are layer boundaries (`engine.py` 88 lines, no domain
  formulas across D0–D4), real tests (51 unit / 1342 test LOC), recorded negative
  results, mandatory proxy disclaimers. Weakness is measurement — see §Next 1–2
- Verify: `cd sandbox && PYTHONPATH=src python -m pytest -q -m "not integration"`
  → **51 passed**; `git status` clean; `git log origin/master` = 14 commits

### 2026-08-05 — Real by_scenario splits D1–D4

- D1 neuro_chip: activity loads `nominal` / `high_activity` / `sparse` → distinct `chip_fit_score` / power
- D2 biocompute: input bias `balanced` / `sparse` / `dense`
- D3/D4 biosignal+hybrid: signal conditions `clean` / `arrhythmia` / `noisy`
- Examples + `test_by_scenario_domains` all **split** (≥2 distinct rows); stub fallback remains for plugins without by_scenario
- Verify: `pytest tests/test_by_scenario_domains.py` (+ domain suite) green

### 2026-08-05 — Port CS-P01 Overview + CS-P02 Editor

- ★ + Port: Commercial `CS-P01`/`CS-P02` + parity; neurolab `/` + `/editor` (Run moved to `/run`)
- API: `/api/projects`, `/api/manifest`, `/api/validate` (+ save)
- Verify: UI suite P01–P05 **12 passed**; `closed-sandbox ui` → `:8765` health screens P01…P05

### 2026-08-05 — Gate enable on named pilot contour

- Commercial: `config/sovereign.pilot-contour-gate.toml` — hammer2 + guard + **`[synapse_bridge] enabled`** (:8097)
- Chat-only pilot `:8096` stays Gate-off; example.toml default still off
- Verify: `./scripts/synapse-gate-smoke.sh` → **3 pass / 0 fail** + audit `synapse.*`

### 2026-08-05 — by_scenario on all domains

- Engine `ensure_by_scenario`: stub rows for D1–D4 (+ synapse_import) from manifest names
- snn_lif stays `by_scenario_mode=split`; others `stub` (identical aggregate copy per name)
- Verify: `pytest tests/test_by_scenario_domains.py` + demo_pack

### 2026-08-04 — Port CS-P05 Ask (FR-UI-030/031)

- ★ + Port: Commercial `CS-P05-ask.html` + `parity/CS-P05.yaml`; neurolab `sandbox/ui/ask.html` · `/api/ask`
- Public risk banner mandatory; local default; CLI `contour_ask.ask`
- Verify: `pytest tests/test_ui_cs_p05.py` (+ UI suite)

### 2026-08-04 — Port CS-P04 Diff (FR-UI-020)

- ★ + Port: Commercial `CS-P04-diff.html` + `parity/CS-P04.yaml`; neurolab `sandbox/ui/diff.html` · `/api/diff`
- CLI parity: `closed-sandbox diff` shape (`n_changed` + `changed`)
- Verify: `pytest tests/test_ui_cs_p04.py` (+ CS-P03 suite) green
- Nested `by_scenario` table rows waived (API still full)

### 2026-08-04 — Per-scenario metrics (snn_lif)

- Engine: generative conditions `nominal` / `anomaly` / `noise` → `metrics.by_scenario`
- UI CS-P03 table + `report.md` § Per scenario; parity `per-scenario-metrics` → **done**
- Verify: `pytest tests/test_snn_lif.py tests/test_ui_cs_p03.py` green; rows differ by scenario

### 2026-08-03 — Demo pack (D0–D4 + UI + Gate)

- Runbook: `docs/DEMO-PACK-SANDBOX.md` · script `sandbox/scripts/demo_pack.sh`
- Verify: **6 pass / 0 fail** (~10s domains)
- Wording: Approved SOW one-liners in runbook table

### 2026-08-03 — Synapse Gate SOW wording **Approved**

- Human: OK on `docs/SYNAPSE-GATE-SOW-WORDING.md`
- Handoff §10 / checklist human OK ticked
- Agents may reuse §3–§5; Gate flag still default **off** until pilot enable

### 2026-08-03 — Synapse Gate SOW wording draft (await human)

- (superseded by Approved above)

### 2026-08-03 — D4 `hybrid` opened (NL-ADR-024)

- Composition: `[front]` synthetic ECG/EEG → encode → `[backend]` `snn_lif`
- Example `hybrid_ecg_snn_v0` · metrics `hybrid_pipeline`
- Domain suite D0–D4 now runnable
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/hybrid_ecg_snn_v0/project.toml`

### 2026-08-03 — D2 closed · D3 `biosignal` opened (NL-ADR-023)

- D2 v0.1 marked complete (`boolean_grn_v0`)
- D3: `synthetic_ecg_v0` / `synthetic_eeg_v0` · threshold encode · LIF classify
- Example `biosignal_ecg_v0` · not clinical
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/biosignal_ecg_v0/project.toml`

### 2026-08-03 — D2 `biocompute` opened (NL-ADR-022)

- Domain `boolean_grn_v0` · example `biocompute_grn_v0`
- Metrics: accuracy/f1 + `bio_*` · wet-lab explicitly out
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/biocompute_grn_v0/project.toml`

### 2026-08-03 — FPGA named target `fpga_snn_lite_v0` (NL-ADR-021)

- Target + LUT/BRAM/DSP proxies · example `chip_fpga_lite_v0`
- CLI writes `out/chip_export.json` when `chip_export` present
- Still no bitstream / vendor SDK · tests extended
- Verify: `PYTHONPATH=src python -m closed_sandbox.cli run examples/chip_fpga_lite_v0/project.toml`

### 2026-08-02 — D1 `neuro_chip` opened (NL-ADR-020)

- Domain plugin + example `chip_estimate_v0` · target `generic_neuromorphic_v0`
- Metrics: `chip_area_mm2`, `chip_power_mw`, `chip_fit_score` + disclaimer
- Tests: `tests/test_neuro_chip.py` · run: `closed-sandbox run examples/chip_estimate_v0/project.toml`
- Non-goals locked: no fab/PDK/GDSII / measured silicon claims

### 2026-08-02 — Commercial Gate implemented (ADR-054)

- Outpost: `[synapse_bridge]` · `POST /v1/synapse/escalate` · audit `synapse.*`
- Live smoke **3/3** on hammer2 (`sovereign.synapse-gate.toml` `:8097`)
- Handoff checklist + `SYNAPSE-BRIDGE.md` → **implemented**
- Next agreed: **D1 neuro_chip**

### 2026-08-02 — Commercial Gate handoff (#1)

- Doc: `docs/COMMERCIAL-GATE-HANDOFF.md` — shape A; (superseded by ADR-054 ship above)

### 2026-08-02 — Investor one-pager + build ladder + economy v0

- Docs: `INVESTOR-NORTH-STAR.md` · `NORTH-STAR-BUILD.md` · INDEX / STRATEGY / GRANTS pointers
- Code: sandbox `quality_per_kspike` / `quality_per_ksynop` in report JSON+MD; stress summary mean
- Verify: `cd sandbox && PYTHONPATH=src python -m pytest tests/test_cli_report.py -q`
- Next lever: Commercial Gate handoff checklist **or** next Sandbox ★/Port screen

### 2026-08-02 — North star documented (NL-ADR-019)

- Thesis: cover frontier strengths with **our system** + measured resource economy; distinct breed (not Kimi/Grok clone)
- Docs: `STRATEGY.md` (north star + delivery A/B/C) · `DECISIONS.md` NL-ADR-019 · pointers in GOALS / SCALE-PLAN / SYNAPSE-BRIDGE / INTELLECTUAL-CANON / AGENTS / INDEX
- No code; no Mid/Large kickoff — narrative lock only

### 2026-08-02 — Port CS-P03 (NL-ADR-018)

- Host **A**: neurolab `sandbox/ui/` + `ui_server.py` · `closed-sandbox ui` → `:8765`
- FR-UI-010/011/012 wired to `run_project` + metrics/report export
- Tests: `tests/test_ui_cs_p03.py` (3) · unit suite green (synapse fixture assert refreshed)
- Parity: Commercial `parity/CS-P03.yaml` → ported (cancel + per-scenario waived)
- Verify: `cd sandbox && PYTHONPATH=src python -m closed_sandbox.cli ui`

### 2026-08-02 — ★ CS-P03 promoted (move pipeline forward)

- Human: Lab soft-OK; tweaks later in ops; **двигать дальше** → ★ promote
- Commercial: `CS-P03-run-results.html` · `parity/CS-P03.yaml` · hub + Studio manifest Prod ★
- Neurolab: `docs/STUDIO-STAR-REVIEW-CS-P03.md` closed ★
- **No Port yet** — production UI waits explicit Port kickoff

### 2026-08-02 — Studio review: soft-OK, ★ deferred

- Human: Lab mocks look fine for now; future tweaks possible
- (superseded same day by ★ promote above)

### 2026-08-02 — Studio ★ review opened (CS-P03)

- Design Studio up · Closed Sandbox hub + CS-L01…05 browsable
- First Port slice candidate: **CS-L03 Run+Results** (FR-UI-010/011/012)
- Checklist: `docs/STUDIO-STAR-REVIEW-CS-P03.md` — waiting human ★ / правки
- No Port / no CS-P* until human says `★ CS-P03`

### 2026-08-01 — Synapse v0.3 → sandbox → ask ✅

- Fixture from `2026-08-01-e5-brains-v2-skip-llm.json` · class_fix=**specialist** **0.8636**
- Exporter handles brains-v2 rows; `contour_ask` uses dynamic class_fix
- Ask 3/3 PASS on `:8098` · report `sandbox/reports/e5-roles-ask-20260801.md`
- Bridge pointer already v0.3; STATUS Synapse row updated

### 2026-08-01 — Design Studio Closed Sandbox confirmed

- Commercial section already live (hub + CS-L01…05); pipeline §5–8 + FR matrix marked Lab done
- Rule `08-design-mockups` lists `design/sandbox/`; parity folder ready for ★ yaml
- Open: `cd ~/Projects/AI-Platform-Vision && ./scripts/design-studio.sh` → **Closed Sandbox**
- Next: human review → promote CS-P03 ★ (no UI code before)

### 2026-08-01 — Agent format LIVE 20/20

- Rebuilt `sovereignd` into Commercial `target/` (not sandbox cache)
- Live `:8102` hn + `[agent_format]` → agent-v0 **20/20**
- Raw `eval/results/raw/agent-v0-live-format-20260801/` · report `agent-v0-runtime-format.md`
- Pilot contour sheet untouched
