# Skill: `asset-prod-and-qc1`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #6 — Asset Production + QC-1 (Pre-1 Masters / Props / Locations / Audio Lib + Stage 3 First Frames)  
> **Companion Files**: [prop_qc1_checklist.md](prop_qc1_checklist.md), [loc_qc1_checklist.md](loc_qc1_checklist.md), [waf_batch_policy.md](waf_batch_policy.md), [asset_prod_brief.md.tmpl](asset_prod_brief.md.tmpl)

---

## 1. Purpose & Trigger

**Purpose**: Produce and gate-verify character single-view references, props, empty-set location masters, 48 kHz CC0 roomtones/SFX, and Stage 3 first frames at `0` Flow video points (`nano2` + CPU) while preventing Google Flow WAF HTTP 403 bans, asymmetric character flip defects (`左衽`/wrong-side scar), V9 stray text, and destructive master-directory hygiene mistakes.

**Trigger**: Invoke when:
- Executing an approved Pre-1 Asset Gap List (`EP01-ASSET-GAP-LIST.md` + engineering review memo).
- Entering Stage 3 first-frame generation after `qc0_preflight.json == PASS`.

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Approved Gap List or `script_pack.json`** | Yes | Pre-1 gap review (`EP01_ASSET_GAP_REVIEW_AGY_MEMO.md`) or QC-0-passed `script_pack.json`. |
| **Asset Manifest & Registries** | Yes | `ASSETS_MANIFEST.yaml`, `COSTUME_REGISTRY.md`, `docs/PROP_REGISTRY.md`, `docs/LOCATION_REGISTRY.md`. |
| **Locked Anchor Bibles** | Yes | `bible/anchors/FANLI.yaml`, `bible/anchors/SYS01.yaml` (single-view refs only; never multi-grid cards). |
| **Hard Spend Caps** | Yes | `0` Flow video pts for stills (`nano2`), `0` Colab CU, `0` ElevenLabs chars (unless voice phase explicitly authorized). |
| **Progress Ledger** | Yes | `~/drama-line/<TASK>_PROGRESS.log` (append after every CPU or WAF batch). |

---

## 3. Protocol

1. **Execute CPU-first derivations & audio library (`0` API calls)** — Perform lossless RGB rectangular single-view crops from approved multi-grid character cards using Pillow (**NO BiRefNet matting**; preserve clean studio grey background `RGB≈(218,219,221)`; exclude known defect cells such as `SYS-01` R2C5 wooden object and `FANLI` modern R2C2 coin cell with fake text; crop out fake ratio numbers). Synthesize/consolidate 48 kHz 16-bit stereo PCM roomtones and Foley via `tools/make_ep01_audio_lib.py` *(grounded in `EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §4.1 & `ASSET_PROD_REPORT.md` §2.1, §2.5)*.
2. **Generate stills via WAF-disciplined `nano2` batches (`0` video pts)** — Invoke `tools/run_gflow_helper.py image --mode i2i|t2i --model nano2 --aspect 9:16` strictly following [waf_batch_policy.md](waf_batch_policy.md):
   - `≤ 3–4` images per batch; `≥ 45–60s` inter-image cooldown (proven at `55–87s` in `ASSET_PROD_REPORT.md` §2.4) with visual check before submitting the next image; `≥ 30–45m` inter-batch break filled with CPU work.
   - Anchor multi-angle locations (`_window`, `_tabletop`, `_rev`) via `i2i` to the primary locked angle; anchor hero props (`PROP-SWORD-01`) to existing locked outfit refs (`fanli-outfit03-45.jpg`).
   - **Never horizontally flip asymmetric character refs** — right-facing `45R` must be generated cleanly with a scar-free anatomical right brow and lowercase-`y` `右衽` collar (`SM7A_RESULT.md` §3, `ASSET_PROD_REPORT.md` §2.2).
   - **On HTTP 403 / exit code 10 (`WafRejectionError`): STOP immediately, log timestamp + incident ID, ZERO retries, ZERO workarounds** (`tools/run_gflow_helper.py` L22–31, L96–100).
3. **Enforce AMD-04 same-location derivation in Stage 3** — Use only the 3 legal paths (`derived_shot` from an approved shot in the same segment, `generated_dual_lock` with `LOC-*` + full character refs, or `l3_clay_frame0`). Never generate a continuing character from a lone `LOC-*` plate (`demo02_v2/run_stage3_frames.py`, `STORYBOARD-SPEC-V2.md` §C.3).
4. **Run automated QC-1 diff sheet & Lab/blowout telemetry** —
   - For Stage 3 shots: `python3 tools/diff_sheet_gen.py --mode qc1 --anchors-dir bible/anchors/ ...` producing `qc1_diff_sheet.jpg` (high-res + 2.5× face/collar zoom + Lab/blowout `AUTO-FLAG`s) and `qc1_gate.json` skeleton (`FULL_RUN_REPORT.md` §3.2).
   - For Pre-1 props & locations: compute `bg_L`, `bg_b`, `whole_L`, `whole_b`, `blowout_pct` (`≤ 5.0%`), multi-angle `|ΔL*| ≤ 15` / `|Δb*| ≤ 12`, SHA256, and generate 2.5× V9 zoom crops (`ASSET_PROD_REPORT.md` §2.3–2.4).
5. **Perform visual 2.5× zoom grading & lock ONLY on full PASS** —
   - Props: grade all **6/6** items in [prop_qc1_checklist.md](prop_qc1_checklist.md); mark `LOCKED` in `docs/PROP_REGISTRY.md` only on 6/6 PASS.
   - Locations: grade all **7/7** items in [loc_qc1_checklist.md](loc_qc1_checklist.md); mark `LOCKED` in `docs/LOCATION_REGISTRY.md` only on 7/7 PASS.
   - Stage 3 first frames: grade all **5 keys** (`age_id`, `scar_side`, `costume_4pt`, `light_lock`, `pose_spatial`) + V9 zero text, fill `qc1_gate.json`, and run `python3 tools/diff_sheet_gen.py --verify qc1_gate.json` (must return PASS).
6. **Execute move-only master hygiene & bump `ASSETS_MANIFEST.yaml`** — Archive any temporary or superseded/defect files out of `casting/master/` using `mv -n` ONLY (**`0 rm`**, never delete), logging source path, destination, SHA256, date, and reason in `casting/archive/ARCHIVE_MANIFEST.txt`. Grep `tools/`, `bible/`, and active episode dirs to verify `0` broken references, then bump `ASSETS_MANIFEST.yaml` *(grounded in `EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §6.2 & `ASSET_PROD_REPORT.md` §2.6)*.

---

## 4. Gates & Tools

| Gate / Tool | Command / Check | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **WAF-Safe Generator** | `python3 tools/run_gflow_helper.py image --mode i2i\|t2i --model nano2 --aspect 9:16 --out <path> --log-json <log>` | Exit `0` (exit `10` = hard WAF 403 stop) | `tools/run_gflow_helper.py` |
| **Audio Library Generator** | `python3 tools/make_ep01_audio_lib.py` | 48 kHz 16-bit stereo PCM, target RMS `-24/-26 dBFS`, `0` clipping | `tools/make_ep01_audio_lib.py`, `ASSET_PROD_REPORT.md` §2.5 |
| **QC-1 Diff Sheet & Token Verify** | `python3 tools/diff_sheet_gen.py --mode qc1 --anchors-dir bible/anchors/ ...` & `--verify qc1_gate.json` | Exit `0`, `0` unresolved `AUTO-FLAG`s, SHA256 verified | `tools/diff_sheet_gen.py`, `FULL_RUN_REPORT.md` §3.2 |
| **PROP-QC-1 / LOC-QC-1** | [prop_qc1_checklist.md](prop_qc1_checklist.md) (6/6) / [loc_qc1_checklist.md](loc_qc1_checklist.md) (7/7) | `6/6` props, `7/7` locations (`blowout ≤ 5%`, `\|ΔL*\| ≤ 15`, `\|Δb*\| ≤ 12`, V9 `0` text, `0` people) | `docs/PROP_REGISTRY.md`, `docs/LOCATION_REGISTRY.md` |
| **Move-Only Hygiene Gate** | `mv -n` + `casting/archive/ARCHIVE_MANIFEST.txt` + `grep` ref audit | `0 rm`, SHA256 logged, `0` broken refs | `ASSET_PROD_REPORT.md` §2.6 |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **CPU cropping, audio synthesis, WAF-paced `run_gflow_helper.py` dispatch, SHA256 & Lab telemetry, move-only archiving** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) driving `tools/*.py` | **Flash / lightweight model** strictly invoking `tools/run_gflow_helper.py` & `tools/diff_sheet_gen.py` | Exit `0`, `0` WAF 403, `0 rm`, `--verify` PASS. |
| **Visual 2.5× zoom QC-1 grading (scar anatomy, `右衽` lapel, V9 stray text, pre-Qin vs Ming-Qing era check)** | **Vision-Capable Tier 1** (`Claude Opus 5.5` or `Gemini Pro High`) + `diff_sheet_gen.py` high-res crops | **Vision-Capable Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) grading against `bible/anchors/*.yaml` + **Muse review** | Zero text-only or `<360px` compressed grading; **permanent character/hero-location `LOCKED` sign-off: Creator**. |

- **Forbidden-Alone**: Text-only models grading images; bypassing `diff_sheet_gen.py --verify`; running unthrottled `for`-loop `nano2` calls; using `rm` on `casting/master/`.

---

## 6. Evidence

This workflow is **proven across 3 major completed runs (+ 1 clean WAF-403 stop) on `workhorse-90d`**:

1. **Master Face & Costumes (`MASTER_FACE_DECISION.md`, `COSTUME_REGISTRY.md`, 2026-11-27)**: Locked Fan Li master face and `OUTFIT-01..04` registries.
2. **`DEMO02_v2` Stage 3 First Frames + QC-1 (`demo02_v2/run_stage3_frames.py`, `FULL_RUN_REPORT.md` §3.2, 2026-11-28)**: 4 `nano2` i2i derivations (`0` WAF 403), `qc1_diff_sheet.jpg` (`3620×8424`), `qc1_gate.json` **6/6 PASS**, eliminating the wrong-side `S4` brow scar pre-Stage 4 (`0/5` wrong-side scar in final clip).
3. **EP-01 Asset Production Mandate (`ASSET_PROD_REPORT.md`, 2026-11-28)**: **17/17 `nano2` stills with `0 WAF 403`** (`fanli-modern-ref-45R` + 6 prop refs `6/6` + 9 location masters `7/7` + 1 SM-8 first frame), 9/9 `SYS-01` + 2/2 `OUTFIT-01` lossless CPU crops, `SYS01.yaml`, `docs/PROP_REGISTRY.md`, `docs/LOCATION_REGISTRY.md`, 6 roomtones + 3 SFX via `make_ep01_audio_lib.py`, `ASSETS_MANIFEST.yaml` v2, and 8 move-only archive operations (`0 rm`, `0` broken refs).
4. **Clean WAF-403 Stop Precedent (`EP01_PREP_REPORT.md` §3, 2026-11-28 `09:06Z`)**: Unthrottled `gen_candidates.py` hit `WafRejectionError` on image #2 → immediate stop, zero retry, directly proving the need for [waf_batch_policy.md](waf_batch_policy.md).

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **Google Flow WAF HTTP 403 (`WafRejectionError`)** | `tools/run_gflow_helper.py` exits with code `10` (`WAF_403_STOP`, `PUBLIC_ERROR_UNUSUAL_ACTIVITY`) | **STOP immediately. ZERO automatic retries, ZERO proxy/header/CAPTCHA bypass.** Log timestamp + incident text into progress ledger and report to Creator (wait cooldown window or let Creator generate in visible browser UI). |
| **Wrong-Side Scar or Reversed Collar (`左衽`)** | 2.5× zoom shows scar on anatomical right brow or `\` lapel (`SM-7A` `45R` defect) | Reject in QC-1; never pass into Stage 4 hoping 4-ref H3 will erase it (`SM7A_RESULT.md` §3). Archive defect via `mv -n` to `casting/archive/defects/` and regenerate cleanly without horizontal flipping. |
| **V9 Stray Text / Fake Seal Script / Ming-Qing Anachronism** | 2.5× zoom reveals glyphs on blade/slips/coin/signage or red-wall yellow-tile palace | Auto-FAIL under `v9_zero_text` / `era_accuracy`. Strengthen positive material/pre-Qin architecture phrasing and explicit blank-surface anchor; regenerate. |
| **Ghost People in Location Master** | Distant silhouette, hand, or reflection in `LOC-*` plate | Auto-FAIL under `no_people_rule`. Never use a populated plate as `<Pic 1>`; regenerate as 100% empty set (`LOC-TAIHU-NIGHT` permits only tiny far-shore torch dots, zero silhouettes). |
| **Multi-Angle Location Light/Palette Drift** | `\|ΔL*\| > 15` or `\|Δb*\| > 12` between `_main` and `_rev`/`_window` | Re-generate secondary angle using `i2i --ref <primary_locked_angle>` (proven to hold `\|Δbg_L\| = 0.87–1.34`, `\|Δbg_b\| = 0.48–0.52` in `ASSET_PROD_REPORT.md` §2.4). |
| **HTTP 429 Model Quota Exhaustion Mid-Batch** | `RESOURCE_EXHAUSTED (code 429)` during asset mandate (`ASSET_PROD_RUN_2.log`) | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (or cross-pool Gemini flagship if third-party quota is exhausted, or `PING_OK` backoff per `quota-dispatch-and-recovery`). Resume strictly from the next uncompleted batch in `*_PROGRESS.log` — never regenerate `LOCKED` assets. |
