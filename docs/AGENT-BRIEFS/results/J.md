# Brief J — result

**Track:** Land ADR 025–027 into `docs/DECISIONS.md`  
**Date:** 2026-08-13  
**Git:** not committed / not pushed (per brief)

---

## What changed

**File:** `docs/DECISIONS.md` only.

1. Removed the `> **Reserved numbers.** …` block (lines 475–480 before edit).
2. Inserted three ADRs before NL-ADR-028, all **Accepted (2026-08-08)**:
   - **NL-ADR-025** — from `results/F.md` §7 (metrics envelope: `metric_primary` core, `METRICS_FAMILY` spikes, economy, goldens).
   - **NL-ADR-026** — from `results/G.md` §6 п.3, expanded to NL-ADR-024 tone (STATUS sole focus, monthly session-log rotation to `docs/SESSIONS-YYYY-MM.md`).
   - **NL-ADR-027** — from `results/H.md` §7 proposed ADR, expanded (outward numbers only from `CLAIMS.md` + caveats, `gen_model_card.py` passport).
3. **NL-ADR-028** untouched (still Proposed).

---

## Verify

```bash
rg -n '^## NL-ADR-02[5-8]' docs/DECISIONS.md
```

```
475:## NL-ADR-025 — Common metrics envelope: `metric_primary` core, spikes by family
500:## NL-ADR-026 — STATUS as sole focus source + monthly session-log rotation
520:## NL-ADR-027 — Outward numbers quoted only from `CLAIMS.md`
541:## NL-ADR-028 — Locked base must leave Qwen2.5-3B (licence); target 7B
```

```bash
rg -n 'Reserved numbers' docs/DECISIONS.md
```

```
(empty — no matches)
```

```bash
python3 scripts/check_doc_links.py
```

```
scanned 65 markdown files · 153 relative links checked · 29 external/anchor-only skipped
note: anchors (FILE.md#section) are not validated, only the file part
result: OK
```

---

## Blockers

None for this track. Follow-ups already noted inside the ADRs (not J scope):

- NL-ADR-025: update `CLOSED-SANDBOX-CODE.md` §3 / `CLOSED-SANDBOX-MVP.md` §7; generalize `cli.py stress` + UI table.
- NL-ADR-026: `README.md` / `SCALE-PLAN.md` stale "current" lines.
- NL-ADR-027: rewrite `INVESTOR-NORTH-STAR.md` § Proof points via CLAIMS IDs; re-run 20/20 with raw evidence.
