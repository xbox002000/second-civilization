# SM-7A Smoke Test Result — H3 Native 4-Ref Ref2VA vs Single-Ref (DEMO-02 S4)

- **Date**: 2026-11-28
- **Test Shot**: DEMO-02 S4 — Dialogue Close-Up (`CU`), `FANLI-OUTFIT-02` (Spring-Autumn coarse linen robe), `LK-ALLEY-NIGHT`, line: `「……你，怎知我名？」`
- **Spec Basis**: `~/drama-line/H3_CONSISTENCY_CAMERA_AGY_MEMO.md` §四 (SM-7A / §4.3 5-frame method) & `~/drama-line/WORKFLOW_V2_AMENDMENT_AGY_MEMO.md` §三 (Identity-Carrier Table)
- **Gateway & Profile**: `comfy-colab-kit` v0.6.0 (`localhost:8080`) → `minimax-h3-video` on **Colab NVIDIA L4 (24 GB VRAM / 23,034 MiB)**
- **Verdict**: **ADOPT WITH CONDITIONS** — Adopt native 4-ref H3 Ref2VA (`ref_image_size="max"`, `0.5 MP` `544×960` on L4) as the dialogue-CU identity carrier baseline, **strictly gated by QC-1 clean first frames** and **patching the reversed collar (`左衽`) defect discovered in `fanli-master-ancient-45R.jpg`**. **Do NOT escalate to SM-7B RefMod yet** (`ComfyUI-MiniMaxH3Mod` stays `WATCH`).

---

## 1. Experimental Setup & Reusable Workflow Paths

| Item | Group A (Control — 1-Ref) | Group B (Candidate — V3 4-Ref) |
| :--- | :--- | :--- |
| **Workflow JSON (reusable)** | `~/drama-line/sm7a/workflows/h3_r2v_1ref_groupA.json` | **`~/drama-line/sm7a/workflows/h3_r2v_4ref_groupB.json`** |
| **Output Video** | `~/drama-line/sm7a/groupA.mp4` (`1,928,569 B`) | `~/drama-line/sm7a/groupB.mp4` (`1,762,349 B`) |
| **5-Frame Strip** | `~/drama-line/sm7a/stripA.jpg` (`2792×1679`) | `~/drama-line/sm7a/stripB.jpg` (`2792×1679`) |
| **Reference Slots (V3 Order)** | `ref_image_0` (`<Picture 1>`): `demo02/S4/2fc09afe-a604-4aeb-8451-5e646bba63bc_1.jpg` (`768×1376`) — first frame only (per §4.2 SM-7A-1) | `ref_image_0` (`<Picture 1>`): S4 first frame (`768×1376`, composition/light only)<br>`ref_image_1` (`<Picture 2>`): `casting/master/fanli-master-ancient-cu.jpg` (`768×1376`, frontal face/scar/age)<br>`ref_image_2` (`<Picture 3>`): `casting/master/fanli-master-ancient-45.jpg` (`768×1376`, left 45° + left brow scar + `OUTFIT-02`)<br>`ref_image_3` (`<Picture 4>`): `casting/master/fanli-master-ancient-45R.jpg` (`768×798`, right 45° scar-free cheek/brow) |
| **Prompt Structure** | H3 Ref2VA 6-section (`<d>[Chinese] ……你，怎知我名？</d>`, `non_diegetic_music: N/A`, zero bare negations) | H3 Ref2VA 6-section + **Q6 Role-Driven Division of Responsibility** (`<Picture 1>` owns alley light/framing only; `<Picture 2..4>` own identity/age/scar/costume exclusively; positive wording only) |
| **Model & Sampler** | `Sulphur3_10ErosMax_SingularityV2_TriPRISM_TurboFusion_realism_pruned_w6a8_g32.safetensors` (`8 steps`, `euler`, `simple`), `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`, `minimax_h3_video_vae_int8_convrot.safetensors`, `minimax_h3_audio_vae_fp32.safetensors` | Identical |
| **Resolution / FPS / Length** | `544×960` (`9:16 (Portrait Widescreen)`, `0.5 MP`, `multiple=32`), `24 fps`, `124 frames` (`5.17s`) | Identical |
| **`ref_image_size`** | **`"max"`** (exposed by `MiniMaxH3ReferenceToVideo`) | **`"max"`** (exposed by `MiniMaxH3ReferenceToVideo`) |
| **Seed** | `420719` (fixed) | `420719` (fixed — identical noise seed) |
| **Audio Handling** | Native H3 Ref2VA stereo audio (`32 kHz` AAC, generated from `<d>[Chinese] ……你，怎知我名？</d>`). Kept as generated per brief (measurement target is visual identity). | Identical native H3 Ref2VA stereo audio generation. |

### Multi-Slot API Binding Verification (H3 Memo §三 Q2 Pitfall #2 Check)
- Confirmed via live `/object_info/MiniMaxH3ReferenceToVideo` (`ComfyUI 0.46.0`, `COMFY_AUTOGROW_V3`) that dotted API keys `"ref_images.ref_image_0"` through `"ref_images.ref_image_3"` are accepted cleanly (`node_errors={}`).
- **Proof all 4 reference images entered inference (not silently dropped)**:
  1. ComfyUI history for Group B (`666cfab7-7d5d-4f88-8604-aeef6450925d`) shows `LoadImage` node `137` cached from Group A, while nodes `139`, `147`, and `148` executed live as active dependencies of `MiniMaxH3ReferenceToVideo` (node `136`).
  2. Even with all 32.8 GB of weights already cached in RAM/VRAM, Group B took **279.9s** vs Group A's **201.0s** (which included cold model loading; ~+110s pure sampling overhead from 4× reference tokens riding every step under `ref_image_size="max"`).
  3. Frame-by-frame pixel difference between Group A and Group B grows steadily across the clip: `MAE_all`: `12.75` (`F1`) → `16.53` (`F2`) → `19.48` (`F3`) → `22.10` (`F4`) → `25.28` (`F5`), with right-side background `MAE_bg_right` reaching `41.22` at `F5`.

---

## 2. Five-Frame Scoring Table (§4.3 Method: `0.5s / 1.5s / 2.5s / 3.5s / 4.5s`)

Reference baseline for comparison: failed DEMO-02 Flow `veo-fast` clip (`~/drama-line/demo02/clips/S4.mp4`, QC-D FAIL).

| Measurement Dimension | Pass Threshold (§4.3 / §4.4) | Group A (1-Ref Control) | Group B (4-Ref V3 + Q6) | A vs B Winner & Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **1. Identity & Age Stability across frames** | `5/5` frames same 38–40 yr old man; zero age regression / person swap | **4.2 / 5.0** — `5/5` frames clearly Fan Li (~38–40 yrs, realistic pores/stubble). Mild late-frame softening on `F4–F5` under push-in + warm rim glare. | **4.7 / 5.0** — `5/5` frames rock-solid Fan Li bone structure & 38–40 yr skin texture; noticeably tighter cheekbone/eye-socket retention at `F4–F5` push-in (`MAE_face=20.8` vs A at `F5`). | **Group B** (cleaner late-frame identity & skin texture under push-in; both vastly beat DEMO-02 baseline). |
| **2. Scar Presence & Anatomical Side** *(canonical: faint scar on anatomical **LEFT** brow tail; S4 faces screen-RIGHT so visible screen-LEFT brow must be scar-free)* | `0/5` frames scar on wrong side (anatomical right brow / screen-left) | **FAIL (`0/5` clean; `5/5` wrong-side scar)** — Inherited the mirrored scar baked into `<Picture 1>` (S4 first frame) on his anatomical right brow tail (screen-left) across all 5 frames. | **FAIL (`0/5` clean; `5/5` wrong-side scar)** — Despite `ancient-45R.jpg` (clean right brow) + `ancient-cu`/`45` (left brow scar) + Q6 wording, the wrong-side scar from `<Picture 1>` remained visible on screen-left in all 5 frames (slightly fainter in `F4–F5`, **not erased**). | **TIE — CRITICAL FINDING** (see §3: `<Picture 1>` pixel-level defect cannot be overridden by 4-ref conditioning). |
| **3. Costume 4 Points (`FANLI-OUTFIT-02`)** | `4/4` items in `5/5` frames | **4.5 / 5.0 — `5/5` PASS**<br>① Collar `右衽` (`y` shape): `5/5` PASS<br>② Matte black cap (`緇布冠`): `5/5` PASS<br>③ Wooden pin (`素木笄`): `5/5` PASS (inherits `<Pic 1>` left-protruding pin)<br>④ Dark brown geometric trim + coarse linen + zero forbidden items: `5/5` PASS (mild softening `F4–F5`). | **4.8 / 5.0 — `5/5` PASS**<br>① Collar `右衽` (`y` shape): `5/5` PASS (outvoted reversed collar in `45R`)<br>② Matte black cap (`緇布冠`): `5/5` PASS<br>③ Wooden pin (`素木笄`): `5/5` PASS<br>④ Dark brown geometric trim + coarse linen + zero forbidden items: `5/5` PASS (sharper weave retention in `F3–F4`). | **Group B** (sharper collar weave preservation; both achieve `5/5` on all 4 items). |
| **4. Lip Movement Plausibility** *(line: `「……你，怎知我名？」`)* | Closed-lip opening; natural articulation; ≥ `3.8 / 5.0` | **4.4 / 5.0 — PASS**<br>Native stereo audio clearly speaks `「你……怎知我名？」` (burst 1: `2.50–3.15s`, pause: `3.25–3.85s`, burst 2: `4.00–4.85s`, zero BGM). Lips closed `0.5–2.4s`, restrained articulation matching both bursts (`2.65–3.05s`, `4.05–4.70s`). | **4.5 / 5.0 — PASS**<br>Native stereo audio clearly speaks `「你……怎知我名？」` on the same two-clause cadence (`2.50–3.15s`, `4.00–4.85s`, zero BGM). Restraint, teeth visibility, and mouth closure during pauses look natural and slightly crisper than A at `4.45–4.70s`. | **Group B (slight edge)** — both easily pass `≥ 3.8 / 5.0` with natural Mandarin lip articulation. |
| **5. Face Morphing & Light Stability** *(bonus V12a check)* | Zero morphing; `|ΔL*| ≤ 12`, `|Δb*| ≤ 10`, blowout `+≤5%` | **3.9 / 5.0** — Zero uncanny morphing; border `dL=-1.3`, `db=+0.1`, blowout `0.00%`. **Defect**: at `F4–F5` (`3.5–4.5s`), hallucinated bright warm streetlamp bokeh erupts in the alley behind his neck/chin, casting warm rim glare onto his cheek. | **4.8 / 5.0** — Zero morphing; border `dL=-3.5`, `db=+1.4`, blowout `0.00%`. Alley stays dark and faithful to `LK-ALLEY-NIGHT` throughout `F1–F5` with **zero hallucinated warm bokeh flare**. | **Group B (decisive win)** — 4-ref conditioning suppressed late-clip background light hallucination. |

### Audio Timing Note (Native Audio vs Locked ElevenLabs TTS)
- Both Group A and Group B generated intelligible, restrained, deep male Mandarin speech (`「你……怎知我名？」`) with zero background music (`non_diegetic_music: N/A` honored).
- Locked ElevenLabs TTS (`~/drama-line/demo01/audio/fanli.mp3`, `FANLI-CAND-F`, `2.12s`) has two bursts (`0.00–0.45s` `你`, pause `0.50–0.70s`, `0.75–1.95s` `怎知我名`). H3's native speech spans `2.50–4.85s` (`2.35s` total with the exact same two-clause pause structure), so replacing audio with locked `fanli.mp3` in assembly only requires aligning onset (~`2.45s` offset + minor pause trim) or testing `ref_audios.ref_audio_0` in a future pass.

---

## 3. Critical Forensic Discoveries

1. **Multi-Ref Ref2VA Is a *Retention Stabilizer*, NOT a First-Frame Defect Eraser (Proves Dual-Gate QC-1)**:
   - Because `<Picture 1>` (`demo02/S4/2fc09afe..._1.jpg`) already matches the target close-up framing and head pose 1:1, H3's attention locks onto `<Picture 1>`'s pixel-level facial marks at `t=0` and carries `<Picture 1>`'s **mirrored wrong-side scar (anatomical right brow / screen-left)** through all 5 frames even when `<Picture 4>` (`ancient-45R.jpg`) is scar-free and the Q6 prompt explicitly restricts `<Picture 1>` to environment/lighting only.
   - This directly confirms `WORKFLOW_V2_AMENDMENT_AGY_MEMO.md` D1: **QC-1 (first-frame static invariant gate) cannot be downgraded**. Neither 4-ref Ref2VA nor RefMod (which also injects via `CONDITIONING`) should be relied on to fix a broken `<Picture 1>`.
2. **Latent Defect Found in Locked Step-0 Asset `fanli-master-ancient-45R.jpg`**:
   - Direct visual inspection of `~/drama-line/casting/master/fanli-master-ancient-45R.jpg` shows its collar is **reversed (`左衽`, wearer's right lapel crossing over left lapel, `\` instead of lowercase `y`)** — likely inherited from horizontal flipping (`tmp_flip45.jpg`).
   - In SM-7A Group B, the other three `右衽` images (`S4`, `ancient-cu`, `ancient-45`) outvoted `45R` (`3 vs 1`), so `groupB.mp4` kept a clean `右衽` collar in `5/5` frames. However, `fanli-master-ancient-45R.jpg` **must be patched to `右衽`** before it is ever used as a primary right-facing i2i anchor for QC-1 first frames.
3. **L4 Hardware Feasibility Confirmed Beyond Expectations**:
   - `ref_image_size="max"` with 4 high-res references at `0.5 MP` (`544×960`) ran with **0 OOM** on Colab L4 24GB (`~20.18 GiB / 22.03 GiB` resident VRAM post-run, `1.85 GiB` headroom), finishing in **4.67 minutes** — well within the `≤ 10 min` SM-7 acceptance gate!

---

## 4. Resource & Cost Telemetry

| Metric | Measured Value |
| :--- | :--- |
| **Colab Accelerator** | `NVIDIA L4` (`23,034 MiB` VRAM, `53.0 GiB` RAM, `1.71 CU/h`) |
| **Cold Start (allocate + deps + 32.8 GB download + boot)** | `~100.1s` (`~0.057 CU`) |
| **Group A Execution (1-ref, `max`, incl. cold weight load)** | `201.0s` (`3.35 min`, `~0.095 CU`) |
| **Group B Execution (4-ref, `max`, weights cached)** | `279.9s` (`4.67 min`, `~0.133 CU`) |
| **OOM / Retries** | `0` OOM, `0` retries |
| **Total Session CU Spend (incl. schema/log checks + stop)** | **`0.4558 CU`** (22.8% of 2.0 CU budget; remaining balance `199.29 CU`) |
| **Gateway State After Run** | `sleeping` (`stopped by dev@localhost`) |

---

## 5. Final Verdict & Actionable Conditions

### Verdict: **ADOPT WITH CONDITIONS** (Native 4-Ref H3 Ref2VA as Dialogue-CU Carrier Baseline)

Do **not** escalate to **SM-7B RefMod** (`ComfyUI-MiniMaxH3Mod` stays `WATCH`). Native 4-ref H3 Ref2VA requires **zero new custom nodes**, **zero profile changes**, runs cleanly on Colab L4 at `ref_image_size="max"` (`0.5 MP`, `4.67 min`, `0 OOM`, `~0.13 CU/clip`), and demonstrably outperforms both the failed DEMO-02 Flow baseline and 1-ref H3 Group A on late-frame identity stability, collar weave sharpness, and `LK-ALLEY-NIGHT` background light discipline.

### Three Required Conditions for Production Adoption
1. **Condition 1 — Mandatory QC-1 Clean First Frame Before Stage 4**:
   - Never feed a first frame with a wrong-side scar, reversed collar, or missing pin into H3 Ref2VA expecting `<Picture 2..4>` to "fix" it. Before re-shooting DEMO-02 S4, regenerate S4's first frame via Path A (`derived_shot`) with a **100% scar-free anatomical right brow** verified by `diff_sheet_gen.py --mode qc1` (`qc1_gate.json == PASS`).
2. **Condition 2 — Patch `fanli-master-ancient-45R.jpg` Collar to `右衽` & Confirm Clean-First-Frame Scar Pass**:
   - Fix the reversed `左衽` collar on `~/drama-line/casting/master/fanli-master-ancient-45R.jpg` (so all 4 `OUTFIT-02` anchors agree on lowercase-`y` `右衽`), then verify `0/5` wrong-side scar in QC-2 on the regenerated DEMO-02 S4 (or first EP-01 dialogue CU).
3. **Condition 3 — L4 Resolution + Upscale & Audio Alignment**:
   - Standardize L4 dialogue-CU generation on `~/drama-line/sm7a/workflows/h3_r2v_4ref_groupB.json` (`544×960`, `0.5 MP`, `ref_image_size="max"`, `8 steps`, `TriPRISM w6a8`), followed by final upscale to `720×1280` / `1080×1920` (per `DESIGN.md` v1.4 §V1.4-03). Keep SM-7B RefMod strictly as a fallback trigger **only** if a clean-first-frame turning CU (`>30°` yaw revealing an unseen face side) still drifts under 4-ref Ref2VA.

---

## 6. Reusable Workflow Usage Guide

- **Canonical Reusable 4-Ref API Workflow JSON**: `~/drama-line/sm7a/workflows/h3_r2v_4ref_groupB.json`
- **To reuse on any future Dialogue CU / MCU shot**:
  1. Upload up to 4 V3-ordered reference images via `POST /upload/image` (`Pic 1` = QC-1 clean first frame, `Pic 2..4` = same-age / same-outfit character masters).
  2. Update filenames in `LoadImage` nodes `"137"` (`ref_image_0`), `"139"` (`ref_image_1`), `"147"` (`ref_image_2`), `"148"` (`ref_image_3`).
  3. Update the Q6 6-section prompt in node `"138"` (`PrimitiveStringMultiline`), target seconds in `"132"` (`PrimitiveFloat`), seed in `"129"` (`RandomNoise`), and output prefix in `"92"` (`SaveVideo`).
  4. POST `{"prompt": <json>}` to `http://localhost:8080/prompt` (after waking `minimax-h3-video` on `L4`).
