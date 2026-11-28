# Flywheel Promotion Checklist (One-Off Catch → Permanent Skill Gate)

> Grounded in `~/drama-line/SKILLIFY_MAP_AGY_MEMO.md` §5.1–§5.2 and `ADR-002` (subtraction / anti-bloat discipline).

Run this 6-step checklist whenever a strong model, Muse, or Creator catches a non-obvious defect in live output or dry-run:

### Step 1 — Catch
- [ ] Record the exact crime-scene artifact (clip/frame/script path, shot ID, timestamp, or metric).

### Step 2 — Forensic Root-Cause
- [ ] Trace the defect to the missing process or contract boundary — **do not patch only the single symptom**.
- [ ] Separate **Carrier / Tech verdict** from **Creative / Composition verdict** (proven by `SM-8` → v2.4.1).

### Step 3 — Enforcement Tiering (`ADR-002` Anti-Bloat Filter)
Classify into **EXACTLY ONE** bucket:
- [ ] **(a) HARD `FAIL` gate (`preflight_gate.py` / `diff_sheet_gen.py`)** — ONLY if the violation is *always* wrong across all episodes AND machine-detectable with near-zero false positives (e.g., `V9` stray text, wrong-side scar, lone-`LOC` derivation, multi-grid charactercard ref). Requires Creator sign-off.
- [ ] **(b) ADVISORY `WARN` gate** — Use when legitimate artistic exceptions exist; always include an explicit justification field (e.g., `INSERT_ECU_DURATION` + `hold_justification`; `SYS01_MANIFESTATION_DIRECTION` + `apparition_justification`).
- [ ] **(c) Bible YAML / Visual QC Checklist** — Use for visual invariants verified on 2.5× zoom crops (`bible/anchors/*.yaml`, `PROP-QC-1`, `LOC-QC-1`).
- [ ] **(d) Playbook Note (`bible/director/playbook.md`)** — Use for one-off creative/directorial lessons; **do NOT over-gate taste**.

### Step 4 — Codify + Regression Test
- [ ] Patch `STORYBOARD-SPEC-V2.md` (with version bump), affected `bible/**/*.yaml`, and `tools/*.py`.
- [ ] Add dedicated positive (PASS) AND negative (FAIL/WARN) `--selftest` unit tests (`Txx`) reproducing the exact caught defect.

### Step 5 — Proof Run
- [ ] Verify the new gate catches the historical defect (or reproduces it cleanly in `Txx`) AND passes the repaired/new artifact with `0` waivers.

### Step 6 — Embed in Skill & Down-Shift Tier
- [ ] Update the owning `skills/<skill-name>/SKILL.md` (protocol, gate command, template, failure mode).
- [ ] Re-classify the day-to-day execution node down to **Tier 2 / Tier 3** once the mechanical gate carries the invariant.
