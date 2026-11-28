# Skill: `scorecard-v2-redteam-eval`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #2 — Scorecard v2 Evaluation + Independent Red Team  
> **Companion Files**: [redteam_brief.md.tmpl](redteam_brief.md.tmpl), [blind_score_brief.md.tmpl](blind_score_brief.md.tmpl), [narrow_recheck_brief.md.tmpl](narrow_recheck_brief.md.tmpl), [scorecard_v2_rubric.md](scorecard_v2_rubric.md)

---

## 1. Purpose & Trigger

**Purpose**: Deliver independent, blinded, evidence-first script evaluation and Red Team causal/factual auditing under Scorecard v2 (`18/22/18/16/16/10` + 4 zero-weight Hard Gates + D2 59-pt cap) — eliminating author self-scoring bias, unverified historical/news claims, POV contradictions, and unshootable dialogue speeds prior to Creator Gate A3.

**Trigger**: Invoke for:
- Any new episode script draft (`v0.1` Red Team audit or `v0.2+` full blind score).
- Major Canon refactors affecting multiple dimensions (e.g., `v0.3` 2022 arrival refactor).
- Targeted patch verification (narrow recheck on explicitly named dimensions/gates only, e.g., `v0.2.1` or `v0.3.1`).

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Blinded Script File** | Yes | Script draft with **all author self-scores and revision self-grades stripped** (e.g., `DRYRUN-EP01-v0.2-BLIND.md`, `DRYRUN-EP01-v0.3-BLIND.md`). |
| **Scorecard v2 Rubric** | Yes | [scorecard_v2_rubric.md](scorecard_v2_rubric.md) (distilled from `SCORECARD-V2-PROPOSAL.md`: 6 dims `18/22/18/16/16/10` + 4 Hard Gates + calibration rules). |
| **Evaluation Mode & Brief** | Yes | One of: [redteam_brief.md.tmpl](redteam_brief.md.tmpl) (full adversarial audit), [blind_score_brief.md.tmpl](blind_score_brief.md.tmpl) (full 6-dim blind score), or [narrow_recheck_brief.md.tmpl](narrow_recheck_brief.md.tmpl) (scoped dims/gates only). |
| **Event Card Sources** | Yes | L1/L2 news URLs, `event_time`, `data_cutoff_at`, and primary historical references (e.g., *Shiji*《史記》vs later *Wu-Yue Chunqiu*). |
| **Prior Review Report** | Narrow Recheck Only | Prior Red Team / blind-score report specifying the exact defects being re-verified. |

---

## 3. Protocol

1. **Verify blindness before reading or scoring** — Confirm the input script contains zero author self-scores (`BLIND_SCORE_BRIEF.md` §評分規矩 5). Never search VM logs for or guess the author's self-score; evaluate independently.
2. **Execute all 4 Project Hard Gates (zero-weight veto — any FAIL rejects the draft)** — Grade PASS/FAIL with verbatim evidence per [scorecard_v2_rubric.md](scorecard_v2_rubric.md) §3:
   - **Gate 1 (IP Red Lines)**: Correct `FACT`/`INFERENCE`/`FICTION` tiering; real living people restricted strictly to FACT news layer (never impersonated or assigned unverified motives); Fan Li non-omniscient (memory ≤ Spring-Autumn + 2022–2026).
   - **Gate 2 (One-Sentence Story Test)**: Cold reader can state who wants what / who blocks them / what happens if they lose.
   - **Gate 3 (AI Shootability)**: Independently recalculate every shot's duration (`≤ 6.5s`) and dialogue speaking rate (`≤ 5.0` pure chars/sec or `≤ 5.5` chars/sec with punctuation — never trust the beat sheet's own word count column blindly; `BLIND_SCORE_BRIEF.md` #4, `V03_REVIEW_BRIEF.md` #6); verify zero 3-person long dialogue shots.
   - **Gate 4 (Independent Fact & History Verification)**: Verify every `FACT` entry against L1/L2 sources, `event_time`, `data_cutoff_at`, exact metric definitions (e.g., closing vs intraday, exact date `11/25` vs `11/27`, day-count arithmetic `1,461` vs `1,454`), and primary historical sources (*Shiji* vs later folklore, `DRYRUN_EP01_REDTEAM.md`, `DRYRUN_EP01_v031_RECHECK.md`).
3. **Run evidence-first 6-dimension scoring (or scoped dims only in narrow recheck)** — For each evaluated dimension in [scorecard_v2_rubric.md](scorecard_v2_rubric.md) §2:
   - First quote **verbatim script lines and shot IDs** (any score without verbatim evidence is invalid).
   - Answer every binary sub-check (`Y/N`) explicitly.
   - Enforce **Dimension 2 Built-in Hard Gate**: if ANY POV/mechanism contradiction or uncaused climax exists (e.g., `S04` viewer-only implant vs `S18` protagonist confrontation caught in `DRYRUN_EP01_v03_REVIEW.md`), cap the **total score at `59`** regardless of other dimensions.
   - Assign a score strictly aligned to the rubric's anchor band.
4. **Apply divergence & adjudication check (when paired with a second evaluator)** — If `|Δtotal| > 5` OR any `|Δdim| > 4` OR any Hard Gate verdict disagrees, flag **mandatory evidence-based adjudication** citing verbatim script text and anchor criteria. **NEVER silently average a `> 5` split** (`SCORECARD-V2-PROPOSAL.md` §四.5 — averaging 88 and 53 into 70.5 manufactures a fake score).
5. **Emit structured report without editing the script body** — Write `~/drama-line/<SCRIPT>_<REDTEAM|BLINDSCORE|RECHECK>.md` containing: summary dashboard, 4 Hard Gate verdicts + evidence, per-dimension `evidence → binary sub-checks → score` breakdown, shootability math audit, and Top 3 (max 7 for Red Team) highest-leverage fixes ranked by severity. **Never modify the script file itself and never push git during evaluation** (`DRYRUN_REDTEAM_BRIEF.md`, `BLIND_SCORE_BRIEF.md`).

---

## 4. Gates & Tools

| Gate / Tool | Check / Formula | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **Blind-Input Check** | Inspect input file for stripped self-score | Zero author score visible in blinded file | `BLIND_SCORE_BRIEF.md` |
| **V2 Dialogue Rate & Shot-Length Calculator** | Independent arithmetic per shot: `duration ≤ 6.5s`; `chars / duration ≤ 5.0` (pure) / `≤ 5.5` (with punct) | `0` unflagged violations (same V2 ceiling enforced later by `tools/preflight_gate.py`) | `SCORECARD-V2-PROPOSAL.md` §三.3, `V03_REVIEW_BRIEF.md` #6 |
| **4 Hard Gates + D2 59-pt Cap** | Every gate PASS with cited evidence; D2 mechanism/POV contradiction = `0` | All 4 gates PASS; `total` uncapped | `SCORECARD-V2-PROPOSAL.md` §二–§三 |
| **Evidence-First Quote Gate** | Every scored dimension contains verbatim shot ID + script line quote | `100%` of scored dimensions backed by quotes | `SCORECARD-V2-PROPOSAL.md` §四.2 |
| **Divergence Adjudication Gate** | `\|Δtotal\| ≤ 5` AND `\|Δdim\| ≤ 4` AND identical Hard Gate verdicts | Within band or escalated to formal adjudication | `SCORECARD-V2-PROPOSAL.md` §四.5 |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **Independent Red Team causal/POV audit (D2), fact/history check (Gate 4), & real-person legal boundary (Gate 1)** | **Tier 1 Frontier** (`Claude Opus 5.5` or `Gemini Pro High`, with web/source verification) | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) blind draft + **second independent evaluator (cross-model or Muse)** with mandatory adjudication on `\|Δtotal\| > 5` | Never single-pass Tier 2 / Flash alone; author may never self-approve. |
| **Narrow recheck on already-localized patches** | **Tier 1 Frontier** or **Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) | Cross-pool **Tier 1** | Strictly bounded to named items; must independently recompute arithmetic/rates. |
| **Dimension 6 (Surprise) & Gate A3 Final Script Lock** | **Human Only (Creator)** *(with Muse + LLM strictly as documented "third vote")* | **None** | Per `SCORECARD-V2-PROPOSAL.md` §四.7, LLM has structural bias against genuine surprise and may NEVER solo-decide D6 or sign Gate A3. |

- **Forbidden-Alone**: Single Tier 2 / Flash pass without independent cross-check; author self-audit; any LLM solo-ruling D6 or approving Gate A3.

---

## 6. Evidence

This workflow is **proven across 5 completed evaluation runs on the EP-01 dry-run lineage on `workhorse-90d` (2026-11-27)**:

1. **Run 1 — `DRYRUN_EP01_REDTEAM.md` (v0.1 Red Team)**: Caught `11/25` vs `11/27` TWSE date error, *Shiji* S06 historical errors, real-person boundary risks, and `88` vs `53` uncalibrated scoring split — directly triggering adoption of Scorecard v2.
2. **Run 2 — `DRYRUN_EP01_v02_BLINDSCORE.md` (v0.2 First Full v2 Blind Score)**: Scored `73/100` (adjudicated to `77` with Muse's `82`), flagged Gate 4 FAIL (3 missing/unbound fact specs) and two D2 causal gaps (`S02→S03`, `S16→S17`).
3. **Run 3 — `DRYRUN_EP01_v021_RECHECK.md` (v0.2.1 Narrow Recheck)**: Verified Gate 4 PASS on F1–F3 dates/definitions and raised D2 `14 → 18` without re-running unrelated dimensions.
4. **Run 4 — `DRYRUN_EP01_v03_REVIEW.md` (v0.3 Affected-Dims Blind Review)**: Audited the 2022-arrival 3-era refactor; caught critical `S04` (viewer-only) → `S18` (protagonist confrontation) POV contradiction, triggering the D2 59-pt hard-gate cap.
5. **Run 5 — `DRYRUN_EP01_v031_RECHECK.md` (v0.3.1 Narrow Recheck)**: Verified POV contradiction eliminated (cap lifted, D2 `12 → 17`, D4 `12 → 15`), verified S04/S10 V2 rates, and caught a `1,461` vs `1,454` day-count arithmetic error (`DRYRUN-EP01-arrival-v0.3.2.md` assembled reference score `80/100`).

*(Note: The 18-script calibration anchor bank specified in `SCORECARD-V2-PROPOSAL.md` §四.1 has `0` runs so far and is explicitly NOT claimed as proven here.)*

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **Anchoring Bias (Non-Blind Input)** | Author self-score (`88/100`) leaks into prompt or file | Stop and strip self-score / changelog into a `*-BLIND.md` copy before invoking evaluator (`BLIND_SCORE_BRIEF.md`). |
| **Uncalibrated Score Split (`\|Δtotal\| > 5`)** | Dual scores diverge by `> 5` pts (e.g., `88 vs 53` or `73 vs 82`) | Never average silently. Run structured evidence-based adjudication quoting verbatim lines & rubric bands (`SCORECARD-V2-PROPOSAL.md` §四.5). |
| **Beat-Sheet Arithmetic Trust** | Script beat sheet claims a shot is within V2 speed or day-count (`1,461` vs `1,454`), hiding real error | Always independently recount characters/duration per shot and recompute calendar math (`V031_RECHECK`). |
| **LLM Bias on Dimension 6 (Surprise)** | LLM penalizes genuine subversion or rewards cliché twists | Flag D6 as advisory third-vote only; require Muse + Creator human verdict (`SCORECARD-V2-PROPOSAL.md` §四.7). |
| **Scope Creep Into Editing Script** | Evaluator rewrites script dialogue instead of auditing | Hard rule in every brief: output report only, zero edits to script body. |
| **HTTP 429 Quota Exhaustion During Eval** | `RESOURCE_EXHAUSTED (code 429)` in `*_RUN_*.log` | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (or cross-pool Gemini flagship if Anthropic third-party quota is exhausted, per `quota-dispatch-and-recovery`). If downgraded to Tier 2, pair with a second independent evaluator (cross-model or Muse) before accepting scores. |
