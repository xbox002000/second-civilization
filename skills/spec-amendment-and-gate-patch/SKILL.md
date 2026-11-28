# Skill: `spec-amendment-and-gate-patch`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #11 — Spec Amendment & Tool-Patch Process (`STORYBOARD-SPEC-V2.md` v2.0 → v2.4.1)  
> **Companion Files**: [patch_brief.md.tmpl](patch_brief.md.tmpl), [patch_report.md.tmpl](patch_report.md.tmpl), [flywheel_promotion_checklist.md](flywheel_promotion_checklist.md)

---

## 1. Purpose & Trigger

**Purpose**: Codify approved Creator rulings, postmortem root causes, and GO smoke-test conditions cleanly into `STORYBOARD-SPEC-V2.md`, `bible/**/*.yaml`, and deterministic Python gate tools (`tools/preflight_gate.py`, `tools/diff_sheet_gen.py`) with regression `--selftest` proofs — turning one-off strong-model catches into permanent, model-independent gates without schema bloat or silent scope creep.

**Trigger**: Invoke upon any of:
- Approved Creator direction/ruling (e.g., `SYS01-MANIFESTATION-DIRECTION.md`, `INSERT_ECU_DURATION` addendum).
- Accepted postmortem root-cause package (e.g., `WORKFLOW-POSTMORTEM-DEMO02.md` → `AMD-01–07`).
- Smoke test achieving `ADOPT` / `ADOPT WITH CONDITIONS` / `CARRIER PASS` (e.g., `SM-7A`, `CLAY_TEST`, `SM-8`).

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Authoritative Source Ruling / Memo** | Yes | Verbatim Creator ruling, accepted postmortem, or smoke-test result (e.g., `SYS01-MANIFESTATION-DIRECTION.md`, `SM7A_RESULT.md`, `CAMERA_COVERAGE_AGY_MEMO.md`). |
| **Storyboard Spec** | Yes | `~/drama-line/STORYBOARD-SPEC-V2.md` (currently `v2.4.1 FINAL`). |
| **Affected Bible YAMLs** | As needed | `bible/anchors/{FANLI,SYS01}.yaml`, `bible/camera/named_shots.yaml`, `bible/performance/micro_expressions.yaml`. |
| **Gate Tools** | Yes | `tools/preflight_gate.py` (`64/64` selftests) and `tools/diff_sheet_gen.py` (`15/15` selftests). |
| **Active Staging Docs** | Only if authorized | `EP01_PRODUCTION_WORKFLOW.md`, `DEMO03_TREATMENT.md`, `sm8/SM8_RESULT.md` (strictly within brief scope). |

---

## 3. Protocol

1. **Read the authoritative source verbatim & classify every delta** — Apply [flywheel_promotion_checklist.md](flywheel_promotion_checklist.md) (`ADR-002` anti-bloat rule) to assign each requirement to exactly one tier: **HARD `FAIL` gate**, **ADVISORY `WARN` gate**, **Bible YAML / QC checklist**, or **staging/playbook note** *(grounded in `SYS01_DIRECTION_PATCH_REPORT.md` §2.5 & `SKILLIFY_MAP_AGY_MEMO.md` §5.1)*.
2. **Patch `STORYBOARD-SPEC-V2.md` with version bump & provenance** — Increment version following spec convention (`v2.X` for major merges like v2.4, `v2.X.Y` for targeted patches like v2.4.1), append a `版本沿革` entry, update §零 Bible Index, update §三/§六/§C tables, and annotate superseded smoke tests with split verdicts (`CARRIER PASS | COMPOSITION SUPERSEDED`) rather than erasing history *(grounded in `STORYBOARD-SPEC-V2.md` lines 5–11, `SYS01_DIRECTION_PATCH_REPORT.md` §2.1 & §2.3)*.
3. **Update affected `bible/**/*.yaml` preserving backward compatibility** — Add new canonical values while retaining safe aliases where legacy packs exist (e.g., `eye_level_in_front` + synonym `conversation_eyeline`, `retired_scale_modes: ["manifestation_hero"]` in `bible/anchors/SYS01.yaml`). Validate with `yaml.safe_load` and `diff_sheet_gen.load_anchors_dir()`.
4. **Implement rule deltas + positive & negative `--selftest` unit tests** — Patch `tools/preflight_gate.py` and/or `tools/diff_sheet_gen.py`. Every new rule MUST add dedicated positive (PASS) and negative (FAIL/WARN) test cases (`Txx`) reproducing the exact caught defect while keeping 100% of prior tests passing (`15/15 → 32/32 → 59/59 → 64/64`, per `ASSET_PROD_REPORT.md` §4.2 & `SYS01_DIRECTION_PATCH_REPORT.md` §2.5). If a check requires invasive schema surgery outside scope, do NOT hack the schema — document it plainly in the report instead (`AGY-SYS01-DIRECTION-PATCH-BRIEF.md` §4).
5. **Patch active staging docs ONLY within authorized scope** — Modify strictly what the brief authorizes (e.g., composition notes column only — zero edits to locked dialogue, shot durations, or routing). Leave historical memos (`AMD05_V3_AGY_MEMO.md`, `DRYRUN-EP01-arrival-v0.3.2.md`, grandfathered `DEMO02_v2`) untouched to preserve decision provenance *(grounded in `SYS01_DIRECTION_PATCH_REPORT.md` §2.4 & §4)*.
6. **Run full verification suite** — Run `py_compile`, `preflight_gate.py --selftest`, `diff_sheet_gen.py --selftest`, and `load_anchors_dir()` + `resolve_shot_anchors()` verification on VM.
7. **Write `<TOPIC>_PATCH_REPORT.md` & hand off to `repo-sync-and-hygiene`** — Use [patch_report.md.tmpl](patch_report.md.tmpl) including the mandatory **"Deliberately NOT Changed (and Why)"** section, then execute [`repo-sync-and-hygiene`](../repo-sync-and-hygiene/SKILL.md) on a new `agy/*` branch (re-running selftests inside `~/repos/sc-sync`).

---

## 4. Gates & Tools

| Gate / Tool | Command | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **Syntax Check** | `python3 -m py_compile tools/preflight_gate.py tools/diff_sheet_gen.py` | Exit `0` | Standard Python gate |
| **Preflight Regression Suite** | `python3 tools/preflight_gate.py --selftest` | `64/64 PASS` (and all newly added `Txx` PASS) | `SYS01_DIRECTION_PATCH_REPORT.md` §3 |
| **Diff-Sheet Regression Suite** | `python3 tools/diff_sheet_gen.py --selftest` | `15/15 PASS` | `SYS01_DIRECTION_PATCH_REPORT.md` §3 |
| **Multi-Char Anchor Load Check** | `python3 -c "from pathlib import Path; import tools.diff_sheet_gen as d; db=d.load_anchors_dir(Path('bible/anchors')); assert 'FANLI' in db and 'SYS01' in db"` | Loads all `bible/anchors/*.yaml` without error | `ASSET_PROD_REPORT.md` §4.2, `SYS01_DIRECTION_PATCH_REPORT.md` §3 |
| **Flywheel Anti-Bloat Check** | [flywheel_promotion_checklist.md](flywheel_promotion_checklist.md) | Every rule classified correctly; zero unmotivated HARD gates | `SKILLIFY_MAP_AGY_MEMO.md` §5.1 |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **HARD vs ADVISORY severity classification, schema compatibility, & regression test design** | **Tier 1 Frontier** (`Claude Opus 5.5` or `Gemini Pro High`) | Cross-pool **Tier 1**; OR **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) draft + **Tier 1 / Muse** independent review + `--selftest` 100% PASS | **Any new HARD `FAIL` rule or Canon change requires Creator sign-off.** |
| **Spec wording sync, YAML formatting, staging-note updates, & report drafting** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) | Cross-pool **Tier 1** | Verified against verbatim source ruling + "Deliberately NOT Changed" audit. |
| **Selftest execution & repo sync handoff** | **Tier 3 (Python/git)** via [`repo-sync-and-hygiene`](../repo-sync-and-hygiene/SKILL.md) | **Tier 2** / Flash calling deterministic tools | In-clone `preflight_gate.py` & `diff_sheet_gen.py` `--selftest` 100% PASS. |

- **Forbidden-Alone**: Unreviewed Tier 2 / Flash model inventing HARD rules; rule edits shipped without positive + negative `--selftest` cases.

---

## 6. Evidence

This workflow is **proven across 6 completed spec amendments after v2.0 on `workhorse-90d`**:

1. **v2.0 + Appendix A**: Camera workflow & smoke register integration (`CAMERA_WORKFLOW_AGY_MEMO.md`).
2. **v2.1 + Appendix B**: Director Layer spec integration (`DIRECTOR_LAYER_AGY_MEMO.md`).
3. **v2.2 + Appendix C / §九 (`tools/DELIVERY_NOTE.md`)**: `AMD-01–07` codified in `preflight_gate.py` (`15/15 PASS`) + `diff_sheet_gen.py` (`10/10 PASS`) + `sys01_composite.py`.
4. **v2.3 (`demo02_v2/FULL_RUN_REPORT.md` Phase 1)**: Merged `V23_AMENDMENT_AGY_MEMO.md` + `SM-7A` 3 conditions + Clay Test 4 conditions + `bible/anchors/FANLI.yaml` + `micro_expressions.yaml` → `preflight_gate.py` `32/32 PASS`.
5. **v2.4 (`ASSET_PROD_REPORT.md` Phase C, commit `857e719`)**: Merged Appendix D V14 + §C.4 `AMD-05 v3` + H3 spec reconcile + Creator `INSERT_ECU_DURATION` → `preflight_gate.py` `59/59 PASS`, `diff_sheet_gen.py` `15/15 PASS` (with `--anchors-dir` multi-char `FANLI+SYS01`).
6. **v2.4.1 (`SYS01_DIRECTION_PATCH_REPORT.md`, commit `1bd6712`)**: Patched Creator's eye-level / `editorial_cut_in` / Pre-Shot Cue Triple direction + `SYS01.yaml` + split SM-8 verdict + Advisory `SYS01_MANIFESTATION_DIRECTION` (`T55–T59`) → `preflight_gate.py` `64/64 PASS`, `diff_sheet_gen.py` `15/15 PASS`.

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **Over-Gating (Rule Bloat / False Positives)** | Legitimate artistic holds or legacy packs blocked by a new HARD `FAIL` | Downgrade to **ADVISORY `WARN`** with optional justification field (e.g., `hold_justification` in `INSERT_ECU_DURATION` and `apparition_justification` in `SYS01_MANIFESTATION_DIRECTION`), per `ADR-002`. |
| **Spec vs Code Drift** | Spec documents a CLI flag or YAML field not implemented in `tools/*.py` (e.g., `diff_sheet_gen.py --anchors-dir` gap caught in `FULL_RUN_REPORT.md` §5) | Always run in-clone `--selftest` and a real smoke invocation of every new CLI flag/YAML loader; if deferred, flag explicitly in "Deliberately NOT Changed". |
| **Scope Creep Into Locked Upstream Docs** | Patch accidentally rewrites dialogue, durations, routing, or historical memos | Enforce strict diff review against brief constraints; revert any out-of-scope edit and log untouched files in §4 "Deliberately NOT Changed". |
| **Breaking Legacy Packs on Schema Rename** | Existing `script_pack.json` fails validation after field rename | Keep backward-compatible synonyms in code & YAML (e.g., `conversation_eyeline` alias for `eye_level_in_front`, `apparition_mode` alias for `sys01_apparition_mode`). |
| **HTTP 429 Quota Exhaustion During Patch Run** | `RESOURCE_EXHAUSTED (code 429)` in `*_RUN_*.log` | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (or switch to Gemini flagship pool if Anthropic third-party quota is exhausted, per `quota-dispatch-and-recovery`). Re-verify `git diff` and `--selftest` before committing. |
