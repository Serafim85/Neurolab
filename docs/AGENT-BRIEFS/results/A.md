# Brief A — result

**Track:** Closed Sandbox Design Studio Lab  
**Date:** 2026-07-29  
**Primary repo:** `/Users/valentin/Projects/AI-Platform-Vision`  
**Commit:** none (per brief)

---

## Files created / changed

### Created (Commercial)

| Path | Role |
|---|---|
| `design/sandbox/README.md` | Lab vs Prod ★; links to neurolab PIPELINE + FR |
| `design/sandbox/parity/.gitkeep` | Empty parity dir (yaml after ★) |
| `design/sandbox/CS-L01-overview.html` | Lab · FR-UI-001 |
| `design/sandbox/CS-L02-editor.html` | Lab · FR-UI-002 |
| `design/sandbox/CS-L03-run-results.html` | Lab · FR-UI-010,011,012 |
| `design/sandbox/CS-L04-diff.html` | Lab · FR-UI-020 |
| `design/sandbox/CS-L05-ask.html` | Lab · FR-UI-030,031 |
| `design/studio/pages/closed-sandbox-hub.html` | Hub · FR table · Prod ★ empty · Lab links |

### Changed (Commercial)

| Path | Change |
|---|---|
| `design/studio/manifest.json` | Project `closed-sandbox`; category with hub + Prod/Lab section labels + 5 Lab items (`fr_ids`, `cli_parity`, tags `lab`/`closed-sandbox` only); `previewBust` → `20260729-closed-sandbox-lab` |
| `design/README.md` | Tree row + table row + bullet for `sandbox/` / Studio hub |

### Neurolab

| Path | Change |
|---|---|
| `docs/AGENT-BRIEFS/results/A.md` | This file |
| `STATUS.md` | **Not** rewritten (orchestrator merges) |

### Explicitly not touched

- No `/ui/` or `crates/sovereign-api/static/` production UI  
- No Port / ★ promote  
- No items added under `#outpost-prod-hub`

---

## How to verify

```bash
cd ~/Projects/AI-Platform-Vision
./scripts/design-studio.sh
# → http://127.0.0.1:9394/design/studio/  (or outpost.localhost:9394)
# Switch project → Closed Sandbox → Hub · Closed Sandbox
# Open CS-L01…05; confirm Lab banner and Ask public risk banner on CS-L05
```

Spot-check HTML comments at top of each `CS-L0N-*.html` (`id` / `fr` / `cli` / `status: lab`).

---

## Blockers

- None for Lab placeholders.  
- Studio live open requires human to run `design-studio.sh` (not started by agent).  
- Concurrent edit briefly duplicated the `closed-sandbox` category in `manifest.json`; merged to a single category before handoff.

---

## Next human step

1. Review Lab mocks in Design Studio vs `CLOSED-SANDBOX-UI.md` IA.  
2. Promote selected CS-L* → CS-P* (`status=candidate`) when ready.  
3. ★ Approve first Port slice (likely CS-P03 Run/Results) + create `design/sandbox/parity/*.yaml`.  
4. Only then Port UI — not before.
