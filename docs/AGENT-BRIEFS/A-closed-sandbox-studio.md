# Brief A — Closed Sandbox Design Studio section

**Track:** Design Studio Lab placeholders  
**Primary repo:** `/Users/valentin/Projects/AI-Platform-Vision`  
**Also read (neurolab, read-only):**  
- `docs/CLOSED-SANDBOX-UI-PIPELINE.md` (§2, §5, §8)  
- `docs/CLOSED-SANDBOX-UI-REQS.md` (FR-UI-001…031)  
- `docs/CLOSED-SANDBOX-UI.md` (IA / anti-patterns)  
- `docs/DECISIONS.md` → NL-ADR-015  

**Commercial rules:** `.cursor/rules/08-design-mockups.mdc` · `design/README.md`  
**Template hub:** `design/studio/pages/pharos-hub.html` (structure, not Pharos branding copy)

---

## Mission

Create the **Closed Sandbox** category in Design Studio with Hub + **5 Lab mocks** (CS-L01…05).  
No production UI. No Port. No ★. Lab only.

---

## Do exactly

### 1. Folder layout

```text
design/sandbox/
  README.md                 # Lab vs Prod ★; link to neurolab PIPELINE + FR
  parity/                   # empty except .gitkeep (yaml later after ★)
  CS-L01-overview.html
  CS-L02-editor.html
  CS-L03-run-results.html
  CS-L04-diff.html
  CS-L05-ask.html
design/studio/pages/closed-sandbox-hub.html
```

### 2. Each Lab HTML mock must include HTML comment:

```html
<!--
  id: CS-L0N
  fr: FR-UI-…
  cli: …
  status: lab
-->
```

| id | Title | FR ids (min) | cli_parity |
|---|---|---|---|
| CS-L01 | Overview | FR-UI-001 | list examples + last `out/metrics.json` |
| CS-L02 | Manifest editor | FR-UI-002 | validate `project.toml` before run |
| CS-L03 | Run + Results | FR-UI-010,011,012 | `closed-sandbox run` + metrics/report |
| CS-L04 | Diff | FR-UI-020 | `closed-sandbox diff a.json b.json` |
| CS-L05 | Ask (contour) | FR-UI-030 (+ related ask FRs if listed) | `closed-sandbox ask` |

### 3. Visual / UX constraints (from UI canon)

- Scientific / industrial HMI — **not** consumer AI / purple SaaS.  
- Dense tables, clear status (F1, spike_count, budget_ok, provider local/public).  
- Visible **Lab** badge; banner: “Lab / Dev — not Port”.  
- Placeholder content OK (fake metrics), but labels must match CLI metric keys.  
- Prefer simple standalone HTML + CSS (like Pharos hub), no React build.  
- Contour honesty: Ask mock shows provider banner if public.

### 4. Studio wiring

In `design/studio/manifest.json`:

1. Add project (recommended):

```json
{
  "id": "closed-sandbox",
  "label": "Closed Sandbox",
  "icon": "◎",
  "description": "SNN studio Lab mocks — not Outpost Prod Port (NL-ADR-015)"
}
```

2. Add category `closed-sandbox` with:
   - Hub page first (`featured: true`)
   - Section comment / labels for **Prod mockups ★** (empty or “none yet”) vs **Lab / Dev**
   - Five Lab items pointing at `../sandbox/CS-L0N-*.html`
   - Tags: `["lab", "closed-sandbox"]` — **never** `prod-target` / `star`

3. Bump `previewBust` date string.

4. Update `design/README.md` — one row for `sandbox/` + Studio hub note.  
5. **Do not** add Closed Sandbox into `#outpost-prod-hub`.

### 5. Hub page requirements

`closed-sandbox-hub.html` must have:

- Banner: Lab ≠ Port; specs live in neurolab  
- Links to five Lab mocks  
- Table **FR → mock → status** (at least FR-UI-001,002,010,011,012,020,030 → CS-L*)  
- Empty Prod ★ section: “No Port candidates yet — human promote only”  
- Link text paths to neurolab docs (absolute or `~/Projects/neurolab/docs/...`)

---

## Forbidden

- Production React / Port into `/ui/` or `crates/sovereign-api/static/`  
- Promoting Lab → Prod ★ without human  
- Mixing into Outpost Prod hub  
- Inventing new FR ids (use existing FR-UI-*)  
- Committing unless human asks  

---

## Definition of Done

- [ ] `design/sandbox/` + 5 Lab HTML + README + `parity/.gitkeep`  
- [ ] Hub page + category in `manifest.json`  
- [ ] `design/README.md` updated  
- [ ] Studio opens category (human can run `./scripts/design-studio.sh`)  
- [ ] Result file written (below)

---

## Result file

Write `/Users/valentin/Projects/neurolab/docs/AGENT-BRIEFS/results/A.md` with:

- files created/changed  
- how to verify (`cd AI-Platform-Vision && ./scripts/design-studio.sh` → open Closed Sandbox hub)  
- blockers  
- next human step (review Lab → promote)

**Do not** rewrite neurolab `STATUS.md` (orchestrator merges).
