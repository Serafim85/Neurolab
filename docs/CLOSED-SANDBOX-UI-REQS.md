# Closed Sandbox — UI functional requirements (FR)

> **Статус:** v0 draft (2026-07-28)  
> **Связь:** каждый FR покрывается макетом в Design Studio (`fr_ids`) — см. [`CLOSED-SANDBOX-UI-PIPELINE.md`](CLOSED-SANDBOX-UI-PIPELINE.md)  
> **Поведение SoT:** CLI в `sandbox/` + MVP  
> **IA / визуал:** [`CLOSED-SANDBOX-UI.md`](CLOSED-SANDBOX-UI.md)

ID стабильны. Новое требование = новый id (не переиспользовать).

---

## 1. Легенда

| Поле | Значение |
|---|---|
| **Priority** | P0 = v0.2 UI must · P1 = v1 · P2 = later |
| **CLI** | команда/артефакт, который UI обязан отражать |
| **Mock** | целевой id макета (Lab → Prod) |
| **Status** | `spec` \| `lab-mock` \| `starred` \| `ported` |

---

## 2. Primary views (P0)

### FR-UI-001 — Project overview

| | |
|---|---|
| **User** | Engineer opens Sandbox |
| **Need** | See projects, last run status, F1 / spike_count / budget_ok at a glance |
| **Priority** | P0 |
| **CLI** | list of `examples/*` + last `out/metrics.json` if present |
| **Mock** | CS-L01 → CS-P01 |
| **Status** | `ported` (2026-08-05) |
| **Accept** | Status readable in ≤3s; no marketing hero |

### FR-UI-002 — Manifest editor

| | |
|---|---|
| **User** | Engineer edits network/budget/contour |
| **Need** | Edit `project.toml` (form and/or raw); show `domain` badge; validate before run |
| **Priority** | P0 |
| **CLI** | file edit + `run` validation errors |
| **Mock** | CS-L02 → CS-P02 |
| **Status** | `ported` (2026-08-05) |
| **Accept** | Invalid manifest blocks Run with clear message; domain visible |

### FR-UI-010 — Run project

| | |
|---|---|
| **User** | Engineer starts sandbox |
| **Need** | Choose seed / scenarios; start run; see progress; cancel if possible |
| **Priority** | P0 |
| **CLI** | `closed-sandbox run <project> [--seed]` |
| **Mock** | CS-L03 → CS-P03 |
| **Status** | `spec` |
| **Accept** | Same metrics keys as CLI JSON |

### FR-UI-011 — Results metrics

| | |
|---|---|
| **User** | Engineer reads outcome |
| **Need** | Cards/table: f1, accuracy, spike_count, synops, latency_proxy_ms, budget_ok |
| **Priority** | P0 |
| **CLI** | `out/metrics.json` + `out/report.md` |
| **Mock** | CS-L03 → CS-P03 (same screen section) |
| **Status** | `spec` |
| **Accept** | Values match CLI file byte-for-byte for same seed |

### FR-UI-012 — Results export

| | |
|---|---|
| **User** | Engineer archives run |
| **Need** | Download/export JSON + Markdown report |
| **Priority** | P0 |
| **CLI** | files in `--out` |
| **Mock** | CS-L03 → CS-P03 |
| **Status** | `spec` |

### FR-UI-020 — Diff versions

| | |
|---|---|
| **User** | Engineer compares two runs |
| **Need** | Side-by-side metrics delta (and later manifest keys) |
| **Priority** | P0 |
| **CLI** | `closed-sandbox diff a.json b.json` |
| **Mock** | CS-L04 → CS-P04 |
| **Status** | `ported` (2026-08-04) |
| **Accept** | `n_changed` and deltas match CLI |

### FR-UI-030 — Ask assistant

| | |
|---|---|
| **User** | Engineer asks about metrics |
| **Need** | Chat with report attached; provider chip `local` \| `public` |
| **Priority** | P0 |
| **CLI** | `closed-sandbox ask` |
| **Mock** | CS-L05 → CS-P05 |
| **Status** | `ported` (2026-08-04) |
| **Accept** | Public provider shows **visible risk banner**; local default |

### FR-UI-031 — Contour honesty

| | |
|---|---|
| **User** | Security-conscious operator |
| **Need** | Always see whether data may leave the machine |
| **Priority** | P0 |
| **CLI** | `[contour] provider` |
| **Mock** | CS-L05 → CS-P05 |
| **Status** | `ported` (2026-08-04) |
| **Accept** | Cannot hide public mode |

---

## 3. Secondary (P1)

| ID | Title | Priority | Mock | Notes |
|---|---|---|---|---|
| FR-UI-040 | Spike / time plot | P1 | CS-L06 | optional chart in Results |
| FR-UI-041 | Scenario picker UI | P1 | CS-L03 | nominal/anomaly/noise |
| FR-UI-050 | Domain switcher (D1+) | P1 | later | after D0 Port |
| FR-UI-060 | Multi-project workspace | P1 | later | |
| FR-UI-070 | Keyboard shortcuts help | P1 | CS-L07 | |

---

## 4. Non-goals (explicit)

| ID | Not doing in UI v0.2 |
|---|---|
| FR-UI-X01 | Marketing landing inside app |
| FR-UI-X02 | Cloud account / SaaS signup |
| FR-UI-X03 | Full EDA / GDSII canvas |
| FR-UI-X04 | Wet-lab instrument control |
| FR-UI-X05 | Replacing CLI |

---

## 5. Traceability matrix (start empty → fill as mocks appear)

| FR | Lab mock | Prod mock | Parity yaml | Ported |
|---|---|---|---|---|
| FR-UI-001 | CS-L01 | CS-P01 | `parity/CS-P01.yaml` | ✅ neurolab `sandbox/ui/overview.html` (2026-08-05) |
| FR-UI-002 | CS-L02 | CS-P02 | `parity/CS-P02.yaml` | ✅ neurolab `sandbox/ui/editor.html` (2026-08-05) |
| FR-UI-010 | CS-L03 | CS-P03 | `parity/CS-P03.yaml` | ✅ neurolab `sandbox/ui/` (2026-08-02) |
| FR-UI-011 | CS-L03 | CS-P03 | `parity/CS-P03.yaml` | ✅ |
| FR-UI-012 | CS-L03 | CS-P03 | `parity/CS-P03.yaml` | ✅ |
| FR-UI-020 | CS-L04 | CS-P04 | `parity/CS-P04.yaml` | ✅ neurolab `sandbox/ui/diff.html` (2026-08-04) |
| FR-UI-030 | CS-L05 | CS-P05 | `parity/CS-P05.yaml` | ✅ neurolab `sandbox/ui/ask.html` (2026-08-04) |
| FR-UI-031 | CS-L05 | CS-P05 | `parity/CS-P05.yaml` | ✅ |

Studio: Commercial `design/studio/` → project **Closed Sandbox** · hub `#closed-sandbox-hub`.  
Mocks: `AI-Platform-Vision/design/sandbox/CS-L01…05.html` · ★ `CS-P03`.  
Port UI: `neurolab/sandbox/ui/` · `closed-sandbox ui` · NL-ADR-018.

---

## 6. Acceptance for “design phase done”

См. pipeline §8. Код UI v0.2 стартует только когда P0 FR имеют Lab mocks + human ★ на первый Port slice (обычно CS-P03 Run/Results).
