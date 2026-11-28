# Skill: `quota-dispatch-and-recovery`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #14 — Quota, Model Routing & Resumable Dispatch  
> **Companion Files**: [run_wrapper.sh.tmpl](run_wrapper.sh.tmpl), [continuation_brief.md.tmpl](continuation_brief.md.tmpl), [progress_ledger_schema.md](progress_ledger_schema.md)

---

## 1. Purpose & Trigger

**Purpose**: Ensure unattended multi-phase `agy` runs on `workhorse-90d` survive HTTP 429 (`RESOURCE_EXHAUSTED`) quota limits, CLI `--print-timeout` cutoffs, and Colab allocation hangs without losing state, duplicating completed work, or breaching spend caps.

**Trigger**: Invoke whenever launching or recovering:
- Any multi-phase unattended `agy --print` mandate or chained shell dispatcher (`run_*.sh`).
- An interrupted run returning `RESOURCE_EXHAUSTED (code 429)` (`Individual quota reached` or `Third-party quota reached`).
- A CLI `--print-timeout` cutoff (e.g., 3000s / 50m timeout mid-ComfyUI job).
- A hung Colab allocation (`allocating` timeout) or stalled gateway state.

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Task Brief (`.md`)** | Yes | Authoritative mandate or brief file (e.g., `~/drama-line/AGY-<TASK>-BRIEF.md`) specifying scope, deliverables, and hard spend caps. |
| **Task Class** | Yes | One of the 7 task classes in [`skills/README.md`](../README.md) Model-Tier Routing Table (determines primary model pool and allowed cross-pool substitute). |
| **Deliverable Spec** | Yes | Expected final deliverable path and minimum byte-size floor (e.g., `REPORT.md > 3000 B`, `MEMO.md > 10000 B`, per `run_skillify_g.sh` `ok()`). |
| **Progress Ledger Path** | Yes | Append-only phase ledger file (`~/drama-line/<TASK>_PROGRESS.log`, schema in [progress_ledger_schema.md](progress_ledger_schema.md)). |
| **Hard Spend Caps** | Yes | Explicit limits before dispatch: Flow video pts (`--max-credits`), Colab CU, ElevenLabs chars, and `0 main push` / `0 publish` guardrails. |
| **Prior Logs & Disk State** | On Recovery | Previous `*_RUN_*.log`, `*_PROGRESS.log`, disk artifacts, and live ComfyUI `/history/` if a Colab job was in flight. |

---

## 3. Protocol

1. **Select model pool from the routing table (never blindly single-pin)** — Look up the task class in [`skills/README.md`](../README.md) §2. For Tier 1 / Tier 2 tasks, configure a primary pool AND a documented cross-pool fallback instead of hard-pinning one vendor pool with no exit path *(grounded in `SKILLIFY_RUN_1.log` / `run_skillbuild.sh` → `run_skillify_g.sh` recovery)*.
2. **Require phase-ledger checkpointing in the brief** — Instruct the executing agent to append one structured line (`phase_id`, UTC timestamp, artifacts, spend delta) to `~/drama-line/<TASK>_PROGRESS.log` after every bounded phase *(grounded in `ASSET_PROD_PROGRESS.log`, `FULL_RUN_PROGRESS.log`)*.
3. **Dispatch via bounded resumable wrapper** — Instantiate [run_wrapper.sh.tmpl](run_wrapper.sh.tmpl) with `--print-timeout 3000s`, bounded retry rounds (`1..3`), and deliverable byte-size verification `ok() { [ -f "$1" ] && [ $(stat -c%s "$1" 2>/dev/null || echo 0) -gt $2 ]; }` before advancing or chaining dependent jobs *(grounded in `run_skillify_g.sh`, `run_recovery.sh`, `run_full.sh`)*.
4. **Enforce hardware and spend-cap wrappers on any compute step** — Every Flow video call must pass `--max-credits <N>` (via `tools/run_gflow_helper.py` or `gflow`); every Colab wake/inference sequence must wrap `wake_and_wait()` inside `try...finally` calling `/_gate/stop` with a `360s` wake timeout *(grounded in `demo02_v2/FULL_RUN_REPORT.md` §5 item 5)*.
5. **Handle HTTP 429 (`RESOURCE_EXHAUSTED`) deterministically**:
   - Inspect the exact `AGY_ERROR` payload in `*_RUN_<n>.log`.
   - **Standard 429 re-dispatch rule**: On Gemini / individual quota 429 (`Individual quota reached`), re-dispatch with `--model "Claude Opus 5.5 (Medium)"` if the Anthropic pool has quota, OR if the active pool is rate-limited without cross-pool capacity, run the bounded `PING_OK` probe loop (`1..6` tries, `300s` sleep, `--print-timeout 120s`, per `run_recovery.sh`) before resuming.
   - **Third-party quota 429**: If the error reads `Third-party quota reached. Please switch to Gemini models`, immediately switch the dispatcher to the default Gemini pool (omit `--model` or select Gemini flagship, per `run_skillify_g.sh`) for tasks whose routing row allows cross-pool Tier 1/Tier 2 substitution.
6. **Inspect state on disk & ComfyUI `/history/` before any continuation round** — Never blindly restart from Phase 1. Read `*_PROGRESS.log`, verify already-produced files on disk, and query ComfyUI `GET http://localhost:8080/history/` to rescue any completed remote clip (e.g., `S4.mp4` rescued from `/history/` at `0` extra CU in `demo02_v2/FULL_RUN_REPORT.md` §5 item 4).
7. **Issue a scoped continuation brief** — Populate [continuation_brief.md.tmpl](continuation_brief.md.tmpl) listing ledger-`DONE` phases as strictly read-only (`Do NOT redo anything the ledger marks done`), enumerating only remaining items and preserving original spend caps *(grounded in `AGY-ASSET-PROD-CONTINUATION-BRIEF.md`)*.
8. **Verify completion before chaining** — Confirm the deliverable exists, exceeds the byte floor, contains no unresolved blocker marker, and append `DONE` (or `CONTINUATION_DONE`) to `*_PROGRESS.log` before any downstream script triggers.

---

## 4. Gates & Tools

| Gate / Tool | Invocation / Check | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **Deliverable Size Gate (`ok()`)** | `[ -f "$FILE" ] && [ $(stat -c%s "$FILE") -gt "$MIN_BYTES" ]` | Exit `0` before marking round done or chaining next job | `run_skillify_g.sh` L3 |
| **Quota Readiness Probe (`PING_OK`)** | `/home/hatch/.local/bin/agy --print "Reply with exactly: PING_OK" --print-timeout 120s` | Output contains `PING_OK` within `≤ 6` probes (`300s` interval) | `run_recovery.sh` L4–8 |
| **429 Error Classifier** | `grep -E "RESOURCE_EXHAUSTED|429|Third-party quota|Individual quota" <RUN.log>` | Routes to cross-pool switch or `PING_OK` backoff | `ASSET_PROD_RUN_2.log`, `SKILLIFY_RUN_1.log` |
| **ComfyUI `/history/` Rescue** | `curl -s http://localhost:8080/history/` | Rescues finished remote clip before any re-submission | `demo02_v2/FULL_RUN_REPORT.md` §5 |
| **Colab `try...finally` Stop** | `POST http://localhost:8080/_gate/stop` in `finally:` block (`360s` wake timeout) | Gateway verified `sleeping` after run or failure | `demo02_v2/FULL_RUN_REPORT.md` §5 |
| **Ledger Gate** | `grep -qE "^(DONE|CONTINUATION_DONE)$" <TASK>_PROGRESS.log` | Present before dependent dispatcher starts | `run_skillbuild.sh` L3, `ASSET_PROD_PROGRESS.log` |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **Mechanical dispatch, `PING_OK` probing, ledger verification, ComfyUI `/history/` rescue** | **Tier 3 (Bash / Python)** — 0 LLM judgment | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) or Flash invoking wrapper templates verbatim | Automated gate pass (`ok()` + `DONE` marker + spend cap unchanged). |
| **Authoring a continuation brief after mid-flight interruption** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) | Cross-pool **Tier 1** (`Claude Opus 5.5` / `Gemini Pro High`) | Must preserve exact original spend caps and list every ledger-`DONE` phase as read-only. |
| **Re-scoping a blocked mandate or deciding whether partial completion is acceptable** | **Tier 1 Frontier** (`Claude Opus 5.5` or `Gemini Pro High`) | **Tier 2** draft + **Muse** independent review | **Any spend-cap increase or scope drop requires Creator sign-off.** |

- **Forbidden-Alone**: Silent tier downgrade of an upstream judgment task onto Flash without adding independent cross-check; silent retry loops that ignore `429` or double-spend Flow/Colab credits.

---

## 6. Evidence

This workflow is **proven across 18+ `run_*.sh` dispatches and 3 live recovery incidents on `workhorse-90d` (2026-11-28)**:

1. **CLI 50-minute timeout rescue (`DEMO02_v2`, 2026-11-28 `07:19Z–08:46Z`)**: `run_full.sh` Round 1 timed out while Colab L4 `S4.mp4` was at `240.6s / 286.0s`. Round 2 read `FULL_RUN_PROGRESS.log`, rescued `S4.mp4` (`prompt_id=a1fc4e31-90be-47ee-a462-57bd3385867a`) from ComfyUI `/history/` with `0` wasted CU, fixed `wake_and_wait()` inside `try...finally`, and completed `demo02_v2/FULL_RUN_REPORT.md`.
2. **Individual quota HTTP 429 recovery (`EP-01 Asset Prod + SYS-01 Patch`, 2026-11-28 `12:33Z–13:45Z`)**: `ASSET_PROD_RUN_2.log` / `RUN_3.log` hit `RESOURCE_EXHAUSTED (code 429): Individual quota reached... Resets in 20m32s` after Batch 4. `run_recovery.sh` ran `PING_OK` probes + dispatched `AGY-ASSET-PROD-CONTINUATION-BRIEF.md` against `ASSET_PROD_PROGRESS.log`, completing Batch 5 + repo sync `857e719` + `ASSET_PROD_REPORT.md` + `SYS01_DIRECTION_PATCH_REPORT.md` (`1bd6712`) without redoing a single Batch 1–4 asset (`RECOVERY_PROGRESS.log`).
3. **Third-party Anthropic quota HTTP 429 cross-pool recovery (`Skillify Map`, 2026-11-28 `14:02Z–14:29Z`)**: `run_skillify.sh` and `run_skillbuild.sh` pinned `--model "Claude Opus 5.5 (Medium)"` / `"Claude Sonnet 5.5 (Medium)"` and failed immediately with `Third-party quota reached... Resets in 4h28m31s` (`SKILLIFY_RUN_1.log`). Re-dispatching via `run_skillify_g.sh` onto the Gemini pool completed `SKILLIFY_MAP_AGY_MEMO.md` cleanly.

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **HTTP 429 — Individual / Gemini Quota Exhausted** | `RESOURCE_EXHAUSTED (code 429): Individual quota reached` in `*_RUN_<n>.log` | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (cross-pool switch to Anthropic Tier 1) when Anthropic quota is available. If both pools are throttled or same-pool wait is required, run `run_recovery.sh` `PING_OK` probe loop (`300s` sleep, max `6` tries) and resume via [continuation_brief.md.tmpl](continuation_brief.md.tmpl) reading `*_PROGRESS.log`. |
| **HTTP 429 — Third-Party (Anthropic) Quota Exhausted** | `RESOURCE_EXHAUSTED (code 429): Third-party quota reached. Please switch to Gemini models` (`SKILLIFY_RUN_1.log`) | Switch dispatcher immediately to the default Gemini flagship pool (omit `--model`, per `run_skillify_g.sh`) for any task class whose routing row permits cross-pool substitution. If the task is strictly human/Creator-only, stop and escalate. |
| **CLI `--print-timeout` Mid-Flight** | Exit after `3000s` with missing final report (`FULL_RUN_1.log`) | Do **not** rerun completed phases. Inspect `*_PROGRESS.log`, check files on disk, query `http://localhost:8080/history/` for finished ComfyUI outputs, and launch Round 2 continuation brief. |
| **Colab Allocation Hang (`allocating > 360s`)** | Gateway stuck in `allocating` (`DEMO02_v2` `S3b` Take 2 retry) | `try...finally` auto-calls `POST http://localhost:8080/_gate/stop` on `360s` timeout; confirm gateway state is `sleeping` before retrying once. Do not brute-force retries; escalate after 2 failed wakes. |
| **Truncated / Empty Report File** | Report file exists (`0–500 B`) so `[ -f ]` falsely passes | Always gate completion with `ok <file> <min_bytes>` (`stat -c%s`) rather than bare `[ -f ]` (`run_skillify_g.sh` L3). |
| **Silent Double-Spend on Retry** | Re-running Round 2 regenerates already-locked images/clips | Continuation brief MUST explicitly quote `*_PROGRESS.log` completed phases and forbid re-running any `LOCKED` or `DONE` item (`AGY-ASSET-PROD-CONTINUATION-BRIEF.md`). |
