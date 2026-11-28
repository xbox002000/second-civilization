# Skill: `smoke-test-protocol`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #13 — Smoke Testing (`SM-*` single-shot carrier/workflow verification)  
> **Companion Files**: [smoke_test_brief.md.tmpl](smoke_test_brief.md.tmpl), [smoke_result_report.md.tmpl](smoke_result_report.md.tmpl)

---

## 1. Purpose & Trigger

**Purpose**: Verify any untested video carrier, model, ComfyUI workflow JSON, or generation mode on `N = 1–2` representative shots under a strict spend cap, producing reproducible 5-frame + 2.5× zoom + pixel-telemetry evidence and a split **Carrier/Tech vs Creative/Composition** verdict before committing full-episode budget.

**Trigger**: Invoke before adopting any new or unverified pipeline capability, including:
- `SM-5` (Flow Omni `i2v_first_last`).
- `SM-9` (Colab L4 Wan 2.2 / LTX `wan-ltx-video` for non-face ancient/B-roll shots).
- `SM-7B` (`ComfyUI-MiniMaxH3Mod` RefMod — only if triggered by a clean-first-frame turning CU failure).
- Any new carrier, ComfyUI profile, or prompt/reference conditioning pattern added to `STORYBOARD-SPEC-V2.md` §A.9.

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Hypothesis & 5–6 Criterion Rubric** | Yes | Clear pass/fail criteria with numeric thresholds (e.g., `dL* ≤ 12`, `blowout < 5%`, `V9 = 0/5`, VRAM headroom, latency `≤ 10 min`). |
| **Hard Spend Caps** | Yes | Explicit Flow pts cap (`--max-credits`), Colab CU cap (`≤ 0.5–2.0 CU`), `0` TTS chars, `0` repo push during smoke test. |
| **Test Shot & Baseline Assets** | Yes | Locked anchor refs (`casting/master/`), clean QC-1 first frame (or intentional crime-scene baseline if testing defect retention like `SM-7A`), fixed noise seed. |
| **Reusable Workflow Path** | Yes | Target directory `~/drama-line/<sm_id>/workflows/<workflow>.json` for reproducibility. |
| **Smoke Test Brief** | Yes | Instantiated from [smoke_test_brief.md.tmpl](smoke_test_brief.md.tmpl). |

---

## 3. Protocol

1. **Pre-check live schemas & deprecated models BEFORE waking paid compute** — Inspect live `gflow` CLI options or ComfyUI `/object_info/<NodeName>` (e.g., verifying `COMFY_AUTOGROW_V3` dotted keys `"ref_images.ref_image_0..3"` and `ref_image_size="max"` in `SM7A_RESULT.md` §1; confirming zero deprecated models like `veo_3_1_fast`/`quality` retiring 2026-12-05). If a third-party tool (e.g., CozyClay in `SM-6`) hits a VM runtime blocker or login wall, STOP that path immediately and document the exact fallback without creating accounts or bypassing access controls (`CLAY_TEST_RESULT.md` §1).
2. **Freeze minimal `N = 1–2` matrix with fixed seed & reusable workflow JSON** — Define control vs candidate (if A/B like `SM-7A`) or single carrier probe (`SM-8`, `CLAY_TEST`) using a fixed seed (e.g., `420719`, `420801`) and save the exact executable API workflow under `~/drama-line/<sm_id>/workflows/` so any passing test becomes immediately reusable in production (`h3_r2v_4ref_groupB.json`, `h3_r2v_clay.json`).
3. **Execute under hard spend & auto-stop guardrails** —
   - Flow: invoke via `tools/run_gflow_helper.py` with `--max-credits <CAP>` (enforcing WAF exit-10 stop) and snapshot `gflow credits user --json` before/after.
   - Colab L4: wrap `wake_and_wait()` + inference inside `try...finally` calling `POST http://localhost:8080/_gate/stop` (`360s` wake timeout); log wall time, cold-start time, peak VRAM, min free System RAM, OOM count, and exact CU before/after (`SM7A_RESULT.md` §4, `CLAY_TEST_RESULT.md` §4). Never brute-force retries on failure.
4. **Extract standardized 5-frame strip, 2.5× zoom strip, & objective pixel telemetry** — Sample 5 evenly spaced frames (`0.5s / 1.5s / 2.5s / 3.5s / 4.5s` for 5s clips, or `0.50 / 1.25 / 2.00 / 2.75 / 3.50s` for 4s clips per `SM8_RESULT.md` §2), generate side-by-side comparison strips + `2.5×` face/costume zoom crops, and compute `bg_L`, `bg_b`, intra-clip `dL*`/`db*` span, `blowout_pct (>245)`, SHA256 hashes, and task-specific metrics (e.g., clay grey-leak pixel % & phase correlation in `CLAY_TEST_RESULT.md` §3).
5. **Score every criterion honestly with a split Carrier vs Creative verdict** — Write `~/drama-line/<sm_id>/<SM_ID>_RESULT.md` using [smoke_result_report.md.tmpl](smoke_result_report.md.tmpl). Explicitly separate **Carrier / Technical Verdict** from **Creative / Composition Verdict** (the `SM-8` lesson: `CARRIER PASS | COMPOSITION SUPERSEDED`). Issue one of: **`ADOPT`**, **`ADOPT WITH CONDITIONS`**, **`HOLD`**, or **`FAIL`**, list exact adoption conditions, and hand off approved conditions to [`spec-amendment-and-gate-patch`](../spec-amendment-and-gate-patch/SKILL.md).

---

## 4. Gates & Tools

| Gate / Tool | Command / Check | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **Live Schema Probe** | `curl -s http://localhost:8080/object_info/<Node>` / `gflow --help` | Required input keys & models verified live (`node_errors={}`) | `SM7A_RESULT.md` §1, `CLAY_TEST_RESULT.md` §2 |
| **Spend & WAF Guard** | `tools/run_gflow_helper.py` (`--max-credits`, WAF exit `10`) + Colab `try...finally` `/_gate/stop` | Actual spend `≤` cap; gateway verified `sleeping` post-run | `SM8_RESULT.md`, `CLAY_TEST_RESULT.md` §4 |
| **5-Frame + 2.5× Zoom + Lab Telemetry** | `ffmpeg` frame extraction + Pillow strip + Lab/blowout/anti-leak script | `intra dL* ≤ 12`, `blowout < 5%`, `V9 = 0/5`, SHA256 recorded | `SM7A_RESULT.md` §2, `SM8_RESULT.md` §2 |
| **VRAM / Latency Gate (Colab L4)** | Gateway telemetry during inference | `0` OOM, `≤ 10 min` runtime, free VRAM headroom logged | `SM7A_RESULT.md` §4, `CLAY_TEST_RESULT.md` §4 |
| **Reusable Workflow Artifact** | Saved JSON under `~/drama-line/<sm_id>/workflows/*.json` | Executable directly in Stage 4 without reverse-engineering | `SM7A_RESULT.md` §6, `CLAY_TEST_RESULT.md` §2 |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **Schema check, gateway execution, 5-frame strip & Lab telemetry extraction, SHA256 logging** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) driving deterministic Python/gateway scripts | **Flash / lightweight model** running pre-written smoke runner script | Spend `≤` cap, `0` OOM, gateway verified `sleeping`, strips generated. |
| **Visual rubric scoring, forensic root-cause discovery (e.g., `<Pic 1>` scar lock, `45R` `左衽`), & formulating adoption conditions** | **Vision-Capable Tier 1** (`Claude Opus 5.5` or `Gemini Pro High`) inspecting high-res 2.5× zoom strips | **Vision-Capable Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) + **Muse cross-check** | Honest defect reporting required; never force a FAIL to PASS. |
| **Production Adoption / Creative Composition GO Ruling** | **Human Only (Creator)** | **None** | Tech `CARRIER PASS` does NOT override Creator creative/composition review (`SM-8` precedent). |

- **Forbidden-Alone**: Text-only model scoring visual strips; brute-force retrying past spend cap; promoting an unreviewed smoke test directly into `STORYBOARD-SPEC-V2.md` without Creator sign-off.

---

## 6. Evidence

This workflow is **proven across 3 completed smoke tests on `workhorse-90d` (all 2026-11-28)**:

1. **`SM-7A` (`sm7a/SM7A_RESULT.md`)**: H3 native 4-ref vs 1-ref Ref2VA on `DEMO-02 S4` (`0.4558 / 2.0 CU`, `4.67 min`, `0` OOM, reusable `sm7a/workflows/h3_r2v_4ref_groupB.json`). Verdict: **`ADOPT WITH CONDITIONS`** — uncovered two critical forensic findings (`<Pic 1>` scar lock proving QC-1 cannot be downgraded; reversed `左衽` collar in `fanli-master-ancient-45R.jpg`), directly powering Spec v2.3 and `DEMO02_v2` (`0/5` wrong-side scar).
2. **`SM-2 / SM-3 / SM-6` (`claytest/CLAY_TEST_RESULT.md`)**: L3 Clay Previs → H3 Ref2VA on `DEMO-02 S1` (`0.3897 / 2.0 CU`, `7.18 min`, peak `20.727 GiB` VRAM, `0` OOM, `0.19%` clay-grey pixels = `0` leak, reusable `claytest/workflows/h3_r2v_clay.json` + Python raycast fallback `render_clay_previs.py`). Verdict: **`ADOPT WITH CONDITIONS`** (0–2 hero shots/ep; `SM-6` honestly logged Node `v18.20.4 < 22.19` blocker without bypassing).
3. **`SM-8` (`sm8/SM8_RESULT.md`)**: AMD-05 v3 Carrier A (`nano2` 0 pts + Flow Omni `i2v_first`, `12 / 24 pts`, `0.00 CU`, `dL* span = 2.70`, `max blowout = 0.19%`, `V9 = 0/5`). Verdict: **`CARRIER PASS (6/6) | COMPOSITION SUPERSEDED`** — established the split-verdict rule when Creator approved the holographic carrier optics while retiring the floating low-angle framing into Spec v2.4.1.

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **Colab OOM or Allocation Hang** | VRAM exhaustion or `allocating > 360s` | `try...finally` auto-stops gateway (`/_gate/stop`). Lower `ref_image_size` (`max` → `match`) or downscale `<Video 1>` to `0.35 MP` (`CLAY_TEST_RESULT.md` §2); never brute-force loops past the CU cap. |
| **Third-Party Tool / VM Runtime Blocker (e.g., `SM-6`)** | Missing Node `>= 22.19` / `npx` or login wall | STOP that sub-path immediately (zero account creation, zero auth bypass), declare `NOT OPERABLE` honestly in §1, and execute the pre-approved local fallback (`render_clay_previs.py`) so downstream carrier questions still get answered. |
| **Google Flow WAF HTTP 403** | `tools/run_gflow_helper.py` exits with code `10` | STOP immediately, log timestamp + incident ID, zero retries (`waf_batch_policy.md`). |
| **Conflating Tech PASS with Creative GO** | Carrier passes 6/6 metrics (`SM-8`) but framing/staging reads uncanny | Record an explicit split verdict (`CARRIER PASS | COMPOSITION SUPERSEDED`), preserve carrier approval, and route composition changes through `spec-amendment-and-gate-patch`. |
| **Unreproducible Ad-Hoc Run** | Output video exists but prompt/seed/workflow JSON wasn't saved | Always write exact API workflow JSON to `<sm_id>/workflows/`, fixed seed, and SHA256 hashes before calling inference. |
| **HTTP 429 Model Quota Exhaustion During Smoke Run** | `RESOURCE_EXHAUSTED (code 429)` in `*_RUN_*.log` | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (or switch to Gemini flagship pool if Anthropic third-party quota is exhausted, per `quota-dispatch-and-recovery`). Check `<sm_id>/` on disk and ComfyUI `/history/` before resuming so the smoke clip is never generated twice. |
