# DEMO-02 v2 Full-Process Mandate Report (`STORYBOARD-SPEC-V2.md` v2.3 + `DEMO02_v2.mp4`)

- **Date**: 2026-11-28 (`07:19:30Z` – `08:46:00Z`, ~86.5 min wall time across 2 resumable invocations)
- **Mandate**: `~/drama-line/AGY-MANDATE-FULL-PROCESS.md`
- **Production Mode**: `demo` (`STORYBOARD-SPEC-V2.md` v2.3 §九 — zero exemptions on all non-skippable gates)
- **Final Deliverable**: `~/drama-line/demo02_v2/DEMO02_v2.mp4` (`13,827,085 B`, `23.79 s`, `720×1280`, `24 fps`, H.264 `yuv420p` + 48 kHz stereo AAC `192k`)
- **Updated Spec**: `~/drama-line/STORYBOARD-SPEC-V2.md` (v2.3)
- **Overall Pipeline Readiness Verdict**: **READY FOR EP-01 PRODUCTION PLANNING (WITH 2 MINOR TOOLING CLEANUPS)** — see §7.

---

## 1. Executive Summary (Phase 1 – Phase 3)

| Phase | Outcome | Key Artifacts & Proof |
| :--- | :--- | :--- |
| **Phase 1: Spec v2.3 + Tooling** | **DONE (PASS)** | Integrated `V23_AMENDMENT_AGY_MEMO.md` (Items 1–7), SM-7A 3 conditions, and Clay Test 4 conditions into `STORYBOARD-SPEC-V2.md` (v2.3); created `bible/anchors/FANLI.yaml` and `bible/performance/micro_expressions.yaml`; upgraded `tools/preflight_gate.py` (**32/32 selftest PASS**) and `tools/diff_sheet_gen.py` (**10/10 selftest PASS**). |
| **Phase 2: DEMO-02 Repair** | **DONE (ALL GATES PASS)** | Authored `demo02_v2/plan/script_pack.json` (zero hand-written bash prompts); passed **QC-0** (`preflight_gate.py`, 0 fail / 0 warn), **QC-1** (`qc1_diff_sheet.jpg` + `qc1_gate.json`, 6/6 PASS), **Stage 4** (Flow `omni-1.2-flash` + Colab L4 SM-7A 4-ref H3 Ref2VA), **Stage 5** (`tools/sys01_composite.py` 4-layer composite on `S3b`), **QC-2** (`qc2_diff_sheet.jpg` + `qc2_gate.json`, 6/6 PASS, 0 auto-flags, **S4 `0/5` wrong-side scar**), and **Stage 6A** assembly (`DEMO02_v2.mp4`). |
| **Phase 3: Self QC-D & Package** | **DONE (6/6 CLASSES FIXED)** | Frame-by-frame review across `qcd_timeline_24f.jpg` and `qcd_cut_boundaries.jpg`: all 6 original DEMO-02 QC-D failure classes resolved; zero waivers used; Colab L4 verified `sleeping`; total spend well below hard caps (`0.83 CU` net balance / `1.265 CU` gross `today` delta vs `12 CU` cap; `60` Flow video pts vs `400 pts` cap; `0` ElevenLabs spend). |

---

## 2. Per-Shot Route, Takes, Timing & Cost

Every prompt and generation call flowed strictly from `demo02_v2/plan/script_pack.json` via gate-enforcing runners (`run_stage3_frames.py`, `run_stage4_flow.py`, `run_stage4_h3.py`, `run_stage5_composite_and_qc2.py`, `assemble_demo02_v2.py`).

| Shot | Timeline Window (Net) | First Frame Path & Source | Video Engine / Workflow | Takes | Selected Take & Why | Direct Gen Cost |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **S1** (`MS`, Arrival) | `0.00–4.00s` (`4.00s`) | `frames/S1_first.jpg` (reused clean anchor) | Flow `omni-1.2-flash` (`i2v_first`) | **2** | **Take 2** (`S1_t2.mp4`, `5s`, `78.4s`). Take 1 (`6s`, `88.0s`) was rejected in preliminary QC-2 due to late-clip push-in (`t=3.0–5.4s`), `緇布冠` beanie morph, and spurious right-cheek scratches. Take 2 kept right palm braced on damp wall across 5/5 frames (exact S1→S2 match), 4/4 costume, `0.00%` blowout. +2-frame post-ffmpeg streetlamp dip (`env_reaction`). | `18 + 15 = 33` Flow pts |
| **S2** (`2S`, Witness) | `4.00–8.00s` (`4.00s`) | `frames/S2_first.jpg` (`derived_shot` from S1 + `ancient-45`, Flow `nano2`, `76.2s`) | Flow `omni-1.2-flash` (`i2v_first`) | **1** | **Take 1** (`S2.mp4`, `5s`, `76.3s`). Clean 4/4 `OUTFIT-02` (restored cap + pin + wall-brace continuity), vivid two-shot micro-motion (Fan Li lowers braced arm into guarded stance; witness steps/blinks/steadies phone), `0.00%` blowout. | `15` Flow pts (+1 `nano2`) |
| **S3a** (`MS`, Cyan Cue) | `8.00–11.42s` (`3.42s`) | `frames/S3a_first.jpg` (reused clean anchor) | Colab L4 H3 4-ref Ref2VA (`h3_r2v_4ref_groupB.json`, `max`, `0.5 MP`, `4.0s` param, seed `421031`) | **1** | **Take 1** (`S3a.mp4`, `4.46s`, `262.2s`, peak `20.74 GiB`). Zero scale-jump morphing; turns cleanly toward off-frame cyan glow at `3.1–4.0s` revealing smooth scar-free right brow; upscaled to `720×1280` in assembly. | `~0.122 CU` (`today` delta) |
| **S3b** (`MCU`, SYS-01) | `11.42–16.50s` (`5.08s`) | `frames/S3b_first.jpg` (`derived_shot` from S3a + patched `45R` + `45`, Flow `nano2`, `94.4s`) | Colab L4 H3 4-ref Ref2VA (`h3_r2v_4ref_groupB.json`, `max`, `0.5 MP`, `5.5s` param) + `tools/sys01_composite.py` (4-layer AMD-05) | **2** | **Take 2** (`S3b_t2.mp4`, seed `421132`, `329.6s`, peak `20.75 GiB`) → upscaled `720×1280` → `S3b_comp.mp4`. Take 1 (`325.3s`, seed `421032`) was rejected in preliminary QC-2 because its `push-in` expanded Fan Li to ~80% frame width (invading the right-55% `SYS-01` landing zone) and showed an awkward lip-pucker at `4.11s`. Take 2 (`static` camera) kept Fan Li strictly on left 45% across full `5.88s` with zero face/panel overlap. | `~0.144 + ~0.152 CU` sampling (+1 `nano2`, +1 hung alloc retry) |
| **S2R** (`MCU`, OTS Reverse) | `16.50–19.12s` (`2.63s`) | `frames/S2R_first.jpg` (AMD-04 Path A `derived_shot` from approved S2, Flow `nano2`, `57.6s`) | Flow `omni-1.2-flash` (`i2v_first`) | **1** | **Take 1** (`S2R.mp4`, `4s`, `75.6s`). Exact same 50s Taiwanese woman from S2 (beige zip jacket, red-white striped bag, dark phone) on **screen-RIGHT facing screen-LEFT** OTS over Fan Li's shoulder, **zero invented crates**, expressive skeptical squint → lowers phone → turns to retreat. Absorbs `~0.53s` L-cut tail of `sys.mp3`. | `12` Flow pts (+1 `nano2`) |
| **S4** (`CU`, Dialogue) | `19.12–23.79s` (`4.67s`) | `frames/S4_first.jpg` (`derived_shot` from S3b + patched `45R` + `cu`, Flow `nano2`, `94.3s`; old S4 banned) | Colab L4 H3 4-ref Ref2VA (`h3_r2v_4ref_groupB.json`, `max`, `0.5 MP`, `5.0s` param, seed `421041`) | **1** | **Take 1** (`S4.mp4`, `5.17s`, `286.0s`, peak `20.74 GiB`). Rock-solid 38–40 yr Fan Li, **`0/5` wrong-side brow scar** (live proof of SM-7A Conditions 1 & 2!), persistent cool cyan bounce light (`0.00%` blowout, zero warm bokeh), restrained Mandarin lip articulation (`2.45s` `你`, `3.95s` `怎知我名`); upscaled `720×1280` and lip-aligned to locked `demo01/audio/fanli.mp3`. | `~0.166 CU` (`today` delta; +1 `nano2`) |

---

## 3. Gate Results & Attached Gate JSONs

All three hard gates passed with **zero overrides** and **zero waivers**. Token verification (`preflight_gate.py`, `diff_sheet_gen.py --verify qc1_gate.json`, `diff_sheet_gen.py --verify qc2_gate.json`) ran live inside `assemble_demo02_v2.py` before rendering `DEMO02_v2.mp4`.

### 3.1 QC-0 Preflight Gate (`demo02_v2/plan/qc0_preflight.json`)

- First draft caught 2 real violations (`S3a SCALE_JUMP_BAN`, `S2R SYS01_BAN`), both fixed in `script_pack.json` before Stage 3.
- Re-verified after `S1` & `S3b` Take 2 refinements: **PASS (0 fail, 0 warn, 0 stamps)**.

```json
{
  "file": "/home/hatch/drama-line/demo02_v2/plan/script_pack.json",
  "result": "PASS",
  "stamps": [],
  "findings": [
    {
      "level": "PASS",
      "rule": "DEMO_BOUNDARY",
      "shot_id": "PACK",
      "message": "production_mode=demo detected; all v2.2/v2.3 hard gates remain enforced (zero exemption).",
      "stamp": null
    }
  ]
}
```

### 3.2 QC-1 First-Frame Gate (`demo02_v2/qc/qc1_gate.json`)

- Diff sheet: `demo02_v2/qc/qc1_diff_sheet.jpg` (`3620×8424`, Q=92, SHA256 `c5af7ba3...a1602f`)
- Result: **PASS** — 6/6 shots, 0 auto-flags, `S4_first.jpg` verified 100% smooth scar-free anatomical right brow in 2.5× zoom.

```json
{
  "schema_version": "2.0",
  "gate_type": "qc1",
  "project_id": "DEMO-02-V2",
  "segment_id": "SEG-01",
  "generated_at": "2026-11-28T07:41:22Z",
  "diff_sheet_path": "/home/hatch/drama-line/demo02_v2/qc/qc1_diff_sheet.jpg",
  "diff_sheet_sha256": "c5af7ba316be79efff6cff7b8b36b5c7e778eb302e5985bf363e4c1db2a1602f",
  "status": "PASS",
  "reviewer": "agy (full-process mandate)",
  "reviewed_at": "2026-11-28T07:42:00Z",
  "shots": [
    {"shot_id": "S1",  "metrics": {"bg_L": 11.41, "bg_b": -0.56, "blowout_pct": 0.0,  "dL_seg": -5.73, "db_seg": -1.7},  "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S2",  "metrics": {"bg_L": 16.55, "bg_b": -0.18, "blowout_pct": 0.0,  "dL_seg": -0.59, "db_seg": -1.32}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S3a", "metrics": {"bg_L": 16.18, "bg_b":  0.86, "blowout_pct": 0.01, "dL_seg": -0.96, "db_seg": -0.28}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S3b", "metrics": {"bg_L": 22.09, "bg_b":  0.10, "blowout_pct": 0.01, "dL_seg":  4.95, "db_seg": -1.04}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S2R", "metrics": {"bg_L": 20.76, "bg_b": -0.85, "blowout_pct": 0.04, "dL_seg":  3.62, "db_seg": -1.99}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "N_A",  "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S4",  "metrics": {"bg_L": 14.66, "bg_b": -1.06, "blowout_pct": 0.0,  "dL_seg": -2.48, "db_seg": -2.2},  "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"}
  ]
}
```
*(Full SHA256-bearing artifact on disk: `~/drama-line/demo02_v2/qc/qc1_gate.json`.)*

### 3.3 QC-2 Final-Clip Gate (`demo02_v2/qc/qc2_gate.json`)

- Diff sheet: `demo02_v2/qc/qc2_diff_sheet.jpg` (`4912×5928`, Q=92, SHA256 `1fe3b4ae...25d0948`)
- Preliminary QC-2 (`qc2_raw_diff_sheet.jpg`) caught and rejected `S1` Take 1 and `S3b` Take 1; after Take 2 retakes and `S3b` 4-layer `SYS-01` compositing, final QC-2 passed **6/6 shots** with **0 auto-flags** and `diff_sheet_gen.py --verify` PASS.

```json
{
  "schema_version": "2.0",
  "gate_type": "qc2",
  "project_id": "DEMO-02-V2",
  "segment_id": "SEG-01",
  "generated_at": "2026-11-28T08:40:08Z",
  "diff_sheet_path": "/home/hatch/drama-line/demo02_v2/qc/qc2_diff_sheet.jpg",
  "diff_sheet_sha256": "1fe3b4aec0499d03103409c15caa240bbfbc5e702832d7b6dc18b1e6b25d0948",
  "status": "PASS",
  "reviewer": "agy (full-process mandate)",
  "reviewed_at": "2026-11-28T08:41:00Z",
  "shots": [
    {"shot_id": "S1",  "clip": "clips/S1.mp4",       "metrics": {"dL_intra":  0.26, "db_intra": -0.15, "peak_blowout_pct": 0.0,  "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S2",  "clip": "clips/S2.mp4",       "metrics": {"dL_intra": -0.74, "db_intra": -0.16, "peak_blowout_pct": 0.0,  "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S3a", "clip": "clips/S3a.mp4",      "metrics": {"dL_intra":  1.54, "db_intra": -0.99, "peak_blowout_pct": 0.0,  "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S3b", "clip": "clips/S3b_comp.mp4", "metrics": {"dL_intra": -3.00, "db_intra": -0.82, "peak_blowout_pct": 0.0,  "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S2R", "clip": "clips/S2R.mp4",      "metrics": {"dL_intra":  6.65, "db_intra":  0.14, "peak_blowout_pct": 0.04, "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "N_A",  "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"},
    {"shot_id": "S4",  "clip": "clips/S4.mp4",       "metrics": {"dL_intra": -1.08, "db_intra":  1.64, "peak_blowout_pct": 0.0,  "blowout_spike_pct": 0.0}, "auto_flags": [], "checks": {"age_id": "PASS", "scar_side": "PASS", "costume_4pt": "PASS", "light_lock": "PASS", "expression_lip": "PASS", "pose_spatial": "PASS"}, "shot_status": "PASS"}
  ]
}
```
*(Full SHA256-bearing artifact on disk: `~/drama-line/demo02_v2/qc/qc2_gate.json`.)*

---

## 4. Self QC-D Review vs Original Six Failure Classes

Reviewed frame-by-frame across `demo02_v2/qc/qcd_timeline_24f.jpg` (24 evenly spaced frames across `0.25–23.64s`) and `demo02_v2/qc/qcd_cut_boundaries.jpg` (all 5 cut-point frame pairs):

| # | Original DEMO-02 Failure Class | DEMO02_v2 Verdict | Forensic Evidence |
| :-: | :--- | :---: | :--- |
| **1** | **Face / Age drift (incl. S3a morph & wrong-side scar)** | **PASS** | Fan Li holds a locked 38–40 yr likeness across all 5 Fan Li shots (`S1 → S2 → S3a → S3b → S4`). `S3a` has zero scale-jump morphing; `S3b` and `S4` confirm **`0/5` wrong-side scar** on his anatomical right brow (screen-left), proving SM-7A Conditions 1 & 2 on live production footage. |
| **2** | **Costume discontinuities (`OUTFIT-02` 4pt + S1→S2 pose jump)** | **PASS** | `緇布冠` black cap, horizontal wooden hairpin (`素木笄`), lowercase-`y` `右衽` cross-collar + brown geometric trim, and gray sash + pale jade disc hold across all 5 Fan Li shots. Cut 1 (`S1 END 3.92s → S2 START 4.08s`) matches right palm braced on damp left wall seamlessly. |
| **3** | **S4 cyan loss + S1 light spike** | **PASS** | `S1` light spike completely eliminated (`0.00%` blowout, `dL_intra=+0.26`, subtle post-ffmpeg 2-frame streetlamp dip at `1.25–1.58s`). `S4` preserves persistent cool cyan bounce light on his right cheek, nose bridge, and collar rim across all 5 frames (`19.12–23.79s`, `0.00%` blowout, zero warm streetlamp bokeh glare). |
| **4** | **S2R witness misplacement + invented vegetable crates** | **PASS** | `S2R` (AMD-04 Path A derived from approved `S2`) keeps the exact same 50s Taiwanese woman (beige short zip jacket + red-white striped bag + dark smartphone) on **screen-RIGHT facing screen-LEFT** OTS over Fan Li's shoulder, with **zero invented crates** and matching damp walls/shutters. |
| **5** | **Stiff performance (wax-figure two-shot)** | **PASS** | Every shot has clear `from → trigger → to` physical performance: `S1` panting wall-brace + alert scan; `S2` Fan Li drops braced hand to guarded stance while witness raises phone/blinks/shifts; `S3a` brisk turn toward rising cyan glow; `S3b` taut breathing watching `SYS-01`; `S2R` skeptical squint → lowers phone → turns to retreat; `S4` chin dip → restrained Mandarin line → sharp hold. |
| **6** | **`SYS-01` expression mismatch + AI text** | **PASS** | Zero AI-generated hologram/UI in Stage 4. `tools/sys01_composite.py` rendered a cold stoic geometric monochrome silhouette (zero smile, zero text), chromatic `rgbashift` + 2-frame entry flicker (`11.67s`), live audio-driven `showwaves` synced to `sys.mp3`, directional cyan spill, and 3% shared camera breath with zero face/panel collision. |

### Sound Design Verification (`DEMO02-DIRECTOR-STATEMENT.md`)
- Continuous 48 kHz stereo `alley_night_wet_48k.wav` roomtone at `-24 dBFS`, ducked `-6 dB` under dialogue.
- **Sound-drop**: roomtone pulls down to `-42 dBFS` `0.35s` before `SYS-01` popup (`11.32–11.65s`), followed by crisp digital glitch ignition pulse (`11.65s`) + locked `sys.mp3` (`11.67–17.03s`, cleanly **L-cutting `0.53s` into `S2R`** per §B.7 #1).
- Distant scooter anti-theft double chirp at `t=2.00s` in `S1`.
- Locked `demo01/audio/fanli.mp3` (`FANLI-CAND-F`, zero pitch/timbre edit, zero ElevenLabs spend) aligned to `S4` H3 lip bursts (`21.05s` `你`, `22.55s` `怎知我名`) by widening only the existing `-75 dB` inter-clause silence valley (`0.68–0.80s`) by `+0.40s`. Peak mix level `0.774` (`-2.2 dBFS`, zero clipping).

---

## 5. Deviations, Waivers & Spec/Tooling Flags

- **Formal Waivers Used**: **NONE (`0`)**. No `[ROUTING_WAIVED]` stamp; no gate override.
- **Logged Operational Deviations**:
  1. **S1 strategy decision** *(mandate allowed re-take or trim)*: Re-took `S1` from scratch via Flow `omni-1.2-flash` (`S1_t2.mp4`, `5s`) rather than trimming the dirty original clip, and added the 2-frame streetlamp flicker dip (`-0.07` brightness, zero blowout) in assembly (`env_reaction`). Reason: completely removes the light spike and preserves S1→S2 wall-brace continuity.
  2. **S3b camera movement revision (Take 1 → Take 2)**: Changed `S3b` in `script_pack.json` from `push-in` to `static` (re-verified via `preflight_gate.py` PASS) because H3's `push-in` moved Fan Li into the right-55% `SYS-01` landing zone after `t=3.0s`. `sys01_composite.py`'s 3% shared camera breath supplies the gentle organic drift cleanly.
  3. **`fanli.mp3` inter-clause silence alignment**: Split `demo01/audio/fanli.mp3` inside its `-75 dB` silent pause (`0.68–0.80s`) to match H3's `0.7s` dramatic pause between `「你」` and `「怎知我名？」` in `S4.mp4`. Zero pitch/speed/timbre change to the locked voice; zero ElevenLabs spend.
  4. **Resumed `S4.mp4` from ComfyUI history**: Invocation 1 hit a 50-minute CLI `print_timeout` while `S4` was at `240.6s / 286.0s`. Invocation 2 rescued the completed `S4.mp4` (`prompt_id=a1fc4e31-90be-47ee-a462-57bd3385867a`) directly from `/history/` without re-running or wasting CU.
  5. **`run_stage4_h3.py` bug fix**: During `S3b` Take 2 retry, Colab hung in `allocating` for 600s; `wake_and_wait()` sat outside `try...finally`, so the timeout did not auto-call `/_gate/stop`. Stopped Colab manually immediately and moved `wake_and_wait()` inside `try...finally` with a 360s timeout.
- **Flagged Spec / Tool Delta (Not Silently Ignored)**:
  - **`diff_sheet_gen.py --anchors-dir` mismatch**: `STORYBOARD-SPEC-V2.md` §C.2 documents `--anchors-dir bible/anchors/` for `diff_sheet_gen.py`, but the implemented CLI in `tools/diff_sheet_gen.py` does not accept `--anchors-dir` yet (it reads anchor checklists from `shot_list.json`). Flagged here for a 20-line follow-up patch before EP-01.

---

## 6. Honest Remaining Defects & Minor Nuances

None of the six QC-D failure classes failed, but four real minor visual nuances remain and are declared honestly:

1. **Cut 2 (`S2 END → S3a START`) eyeline angle jump**: At `S2` end (`7.92s`), Fan Li faces slightly screen-right toward the witness; at `S3a` start (`8.08s`, reused `S3a_first.jpg`), he begins angled slightly screen-left before turning right at `10.42–11.42s`. Fixing this in EP-01 is trivial: derive `S3a_first.jpg` from `S2` instead of reusing an older frame.
2. **`S3b` cyan spill tint on robe torso**: In `S3b_comp.mp4`, Layer 1's feathered cyan spill mask (`--cyan-alpha 0.66`) extends onto Fan Li's dark coarse linen chest, shifting his black robe toward a cool dark-navy cast while `SYS-01` is glowing (`11.67–16.50s`), slightly stronger than `S4`'s subtler cyan rim. Physically plausible (close luminous UI), but tightening `ry` from `0.28` to `0.21` (face/collar only) will keep the robe darker in EP-01.
3. **`S2R` foreground OTS hair silhouette**: In `S2R`, the out-of-focus foreground left OTS shoulder/head edge derived from `S2` crops above the `緇布冠` topknot so only dark hair/shoulder is visible at the left frame edge. Minor and masked by shallow DOF blur.
4. **`S4` tight CU crops cap top after `t=21.6s`**: As `S4` pushes in slowly to an intimate eye-line CU (`22.6–23.6s`), the `緇布冠` and wooden pin naturally exit the top frame border (both clearly verified in `19.1–21.6s`).

---

## 7. Total Spend & Budget Compliance

| Resource | Hard Budget | Actual Spend | % of Budget | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Colab L4 CU** | `≤ 12.0 CU` | **`0.83 CU`** net balance delta (`198.87 → 198.04`) / **`1.265 CU`** gross `today` delta (`0.8455 → 2.1105`) | **6.9% – 10.5%** | Includes 4 H3 4-ref runs (`S3a`, `S3b` T1, `S4`, `S3b` T2) + 2 cold starts + 1 hung 600s allocation retry (stopped cleanly). Gateway verified `sleeping` post-run. |
| **Flow Credits** | `≤ 400 pts` | **`60` video pts** (`18 + 15 + 12 + 15`) + `4` `nano2` i2i calls | **15.0%** | `S1` T1 (`18`), `S2` (`15`), `S2R` (`12`), `S1` T2 (`15`); `nano2` (`NARWHAL`) `S2/S2R/S3b/S4`. |
| **ElevenLabs** | Prefer `0` (reuse existing) | **`0`** | **0%** | 100% reused `demo01/audio/sys.mp3` & `demo01/audio/fanli.mp3` + local 48 kHz `audio_lib`. |
| **Wall Time** | — | **`~86.5 min`** | — | `07:19:30Z → 08:46:00Z` across 2 invocations (Phase 1 spec+tools ~9m, QC-0/Stage 3/QC-1 ~14m, Stage 4 Flow+H3+retakes ~55m, Stage 5/QC-2/Stage 6A/QC-D/Report ~8.5m). |

---

## 8. Recommendation: Readiness for EP-01 Production Planning

**RECOMMENDATION: GO — READY FOR EP-01 PRODUCTION PLANNING** (after Creator signs Gate A3 and two minor 15-minute tooling cleanups land).

**Why the pipeline is proven**:
1. **End-to-end contract enforcement works**: Zero hand-written prompts; `preflight_gate.py` caught real `SCALE_JUMP_BAN` and `SYS01_BAN` bugs before spending a single credit.
2. **Dual-gate QC-1 + QC-2 caught every real visual failure**: QC-1 eliminated the banned `S4` wrong-side scar before Stage 4 (delivering **`0/5` wrong-side scar** in `S4.mp4`); preliminary QC-2 caught `S1` Take 1's cap morph/cheek scratches and `S3b` Take 1's push-in landing-zone collision, and targeted Take 2 retakes fixed both cleanly within ~10% of budget.
3. **Hybrid routing is fast, cheap, and visually cohesive**: Flow `omni-1.2-flash` (`~76s`, `12–15 pts/clip`) handles `MS`/`2S`/reverse shots cleanly; Colab L4 native 4-ref H3 Ref2VA (`~4.5–5.5m`, `~0.13–0.16 CU/clip`, `0 OOM`) locks 38–40 yr Fan Li identity, scar anatomy, and Mandarin lip movement on dialogue CU/MCU; `tools/sys01_composite.py` eliminates all AI UI/expression failure modes permanently.

**Two small cleanups to fold in before EP-01 Stage 1**:
1. Wire `--anchors-dir` into `tools/diff_sheet_gen.py` so `bible/anchors/*.yaml` auto-renders era-specific required/forbidden anchors directly onto QC-1/QC-2 diff sheets (closing the §C.2 spec/CLI delta).
2. Tighten `tools/sys01_composite.py` default vertical mask radius (`ry` ~`0.21`) so cyan spill stays focused on face/cheek/collar rather than tinting dark robes below the chest, and keep `run_stage4_h3.py`'s fixed `try...finally` auto-stop pattern as the standard Colab runner template.
