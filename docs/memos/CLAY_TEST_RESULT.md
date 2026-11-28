# White-Model (Clay) Previs → H3 Ref2VA Smoke Test Result (SM-2 / SM-3 / SM-6)

- **Date**: 2026-11-28
- **Test Shot**: DEMO-02 S1 — Fan Li (`FANLI-OUTFIT-02`) staggers into the narrow night alley (`LOC-ALLEY-NIGHT` / `LK-ALLEY-NIGHT`) and catches himself on the wall; no dialogue, no face CU; handheld anxiety-drift follow camera per `DEMO02-DIRECTOR-STATEMENT.md`.
- **Spec Basis**: `~/drama-line/STORYBOARD-SPEC-V2.md` Appendix A (SM-2, SM-3, SM-6, §A.5–A.6) & `~/drama-line/CAMERA_WORKFLOW_AGY_MEMO.md` (§2.2, §3 Q3, §5).
- **Gateway & Accelerator**: `comfy-colab-kit` v0.6.0 (`localhost:8080`) → `minimax-h3-video` on **Colab NVIDIA L4 (`22.034 GiB` usable VRAM / `52.96 GiB` System RAM, `high_mem: true`)**.
- **Verdict**: **ADOPT WITH CONDITIONS** — Adopt **L3 Clay Previs → Native H3 Ref2VA (`ref_videos.ref_video_0`)** for the **0–2 hero shots per episode** planned in Appendix A, subject to the 4 operational conditions below (VM tooling path for SM-6, mandatory `<Picture 1>` scene anchor for SM-2 anti-leak, L4 resolution/size cap for SM-3 headroom, and MS/LS shot-scale discipline).

---

## 1. SM-6 Verdict: CozyClay Agent Feasibility on This VM

- **Status**: **NOT OPERABLE BY AGENT ON CURRENT VM PROVISIONING** *(tooling/runtime gap, **not** a hosted account/login wall)*.
- **Findings**:
  1. **No hosted login wall for core local 3D staging**: Per `HaD0Yun/CozyClay` docs/CLI design, local `npx cozyclay` (`127.0.0.1:5180/app/`), `cclay live`, and the 27-tool MCP server do not require a CozyClay account (only the optional in-studio AI chat panel uses ChatGPT login or external API keys; no accounts were created and no credentials were requested).
  2. **Hard VM runtime blockers**:
     - Installed Node.js is **`v18.20.4`** (`/usr/bin/node`), whereas CozyClay strictly requires **Node.js `>= 22.19`**.
     - **`npm`, `npx`, and `cclay` are not installed** on this VM (`which npm npx cclay` → none), and no CozyClay MCP server is registered.
     - Hosted `https://cozyclay.org/#try` is a manual browser UI with no VM CLI/MCP bridge.
  3. **Browser note for Phase 5**: Playwright Chromium (`~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`) with SwiftShader software WebGL (`libvk_swiftshader.so`) is already present on disk, so re-testing `npx cozyclay --no-open` + `cclay telemetry off` + `cclay update --off` remains feasible once Node `>= 22.19` and `npm`/`npx` are provisioned.
- **Fallback Renderer Used (Step 2)**:
  - **Pure Python 3D analytic raycast clay renderer** (`numpy` + `Pillow` + `ffmpeg`, zero external installs, zero GPU, zero network): `~/drama-line/claytest/render_clay_previs.py`.
  - Rendered a **genuine 3D matte greybox/clay clip** (`~/drama-line/claytest/previs.mp4`, `544×960` 9:16, `24 fps`, `5.00 s` / `120 frames`, H.264 `yuv420p`, `425 KB`) plus a synchronized inverse-depth clip (`~/drama-line/claytest/previs_depth.mp4`, `338 KB`, ready for `h3-controlnet` fallback if needed).
  - Scene geometry: narrow multi-story alley corridor with protruding balcony/awning/scooter greybox volumes, distant alley end opening & streetlamp pole, one articulated featureless matte-clay mannequin executing the stagger-to-wall catch (`0.0–1.85 s` off-balance stagger left-to-right → `1.85–2.45 s` right-wall hand catch → `2.45–3.75 s` braced breath heave → `3.75–5.0 s` alert freeze), and a 0.35 s lagged handheld anxiety-drift camera (forward track + lateral drift + impact jolt + Dutch roll).

---

## 2. SM-2 / SM-3 Experimental Setup (Gateway Execution)

- **Reusable Workflow JSON**: `~/drama-line/claytest/workflows/h3_r2v_clay.json`
  - Built directly on `minimax-h3-video` (`ComfyUI` live-verified `MiniMaxH3ReferenceToVideo` with `COMFY_AUTOGROW_V3` dotted keys `"ref_videos.ref_video_0"` and `"ref_images.ref_image_0..2"` — zero new profiles or custom nodes).
  - Added 3 video-ingest nodes per `CAMERA_WORKFLOW_AGY_MEMO.md` §3 Q3: `LoadVideo (clay_previs.mp4)` → `GetVideoComponents` → `ImageScaleToTotalPixels (0.35 MP, lanczos, resolution_steps=32)` → `MiniMaxH3ReferenceToVideo.ref_videos.ref_video_0`.
- **Reference Inputs (V3 Order: `scene → characters` + `<Video 1>`)**:
  - `<Video 1>` (`ref_videos.ref_video_0`): `clay_previs.mp4` (`544×960` downscaled to `0.35 MP`, 120 frames @ 24 fps) — **owns camera path, framing scale, corridor perspective, stagger-to-wall blocking, and timing ONLY**.
  - `<Picture 1>` (`ref_images.ref_image_0`): `demo02/loc/e3a9ae98-2106-4fc2-8e30-2bbaf65e4491_1.jpg` (`LOC-ALLEY-NIGHT`) — **owns nocturnal Taipei alley materials, textures, and `LK-ALLEY-NIGHT` lighting ONLY**.
  - `<Picture 2>` (`ref_images.ref_image_1`): `casting/master/fanli-master-ancient-front.jpg` — **owns Fan Li identity & `OUTFIT-02` frontal costume (prompted empty-handed to override bamboo scroll)**.
  - `<Picture 3>` (`ref_images.ref_image_2`): `casting/master/fanli-master-ancient-45.jpg` — **owns Fan Li 45° likeness, brow scar anatomy, & `OUTFIT-02` drape**.
- **Prompting**: H3 Ref2VA 6-section structure (`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music: N/A`) with explicit positive division-of-responsibility replacement wording (every grey clay surface and dummy volume in `<Video 1>` completely replaced by live-action night alley textures from `<Picture 1>` and live-action `<Subject 1>` from `<Picture 2..3>`).
- **Model & Generation Settings**: `Sulphur3_10ErosMax_SingularityV2_TriPRISM_TurboFusion_realism_pruned_w6a8_g32.safetensors` (`8 steps`, `euler`, `simple`), `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`, `minimax_h3_video_vae_int8_convrot.safetensors`, `minimax_h3_audio_vae_fp32.safetensors`; output `544×960` (`0.5 MP`, `9:16`), `24 fps`, `124 frames` (`5.17 s`), `ref_image_size="match"`, fixed seed `420801`.
- **`h3-controlnet` Decision**: Verified preinstalled live (`MiniMaxH3FunControlNetApply` available), **not triggered** because Run 1 native `ref_videos.ref_video_0` achieved **0.0% visual grey leakage (`0.19%` mid-grey low-sat pixels)** and tight camera/blocking adherence on the first pass — saving CU and keeping `h3-controlnet` (Depth) strictly as the documented anti-leak fallback per Appendix A §A.5.

---

## 3. Five-Frame Evaluation (`0.5 / 1.5 / 2.5 / 3.5 / 4.5 s` — `compare_strip.jpg`)

Inspect `~/drama-line/claytest/compare_strip.jpg` (4 rows: Previs Clay | H3 Ref2VA Output | 50% QC-2 L3 Overlay | 2.1× Face & Costume Zoom).

| Dimension | Score | Pass / Gate | Evidence & Forensic Notes |
| :--- | :---: | :---: | :--- |
| **(a) Camera-path follow vs clay clip** | **4.5 / 5.0** | **PASS** | 50% overlay (`Row 3`) shows corridor walls, narrow sky slot, and vanishing point aligned across `5/5` frames. Background top-30% phase correlation confirms matching horizontal handheld drift on the three main motion intervals (`0.5→1.5 s`: previs `+123 px` vs H3 `+110 px`; `1.5→2.5 s`: `-47 px` vs `-61 px`; `2.5→3.5 s`: `+72 px` vs `+37 px`), including matching Dutch-angle roll at `t=1.5 s` and forward push-in toward the far alley opening. Late-shot counter-sway (`3.5→4.5 s`) softened into a tense breathing hold — natural and well within the Appendix A §A.6 `≤ 15%` gate. |
| **(b) Blocking / action follow** | **4.7 / 5.0** | **PASS** | Remarkably tight spatial & temporal adherence across all 5 beats: `t=0.5 s` enters screen-left reaching right; `t=1.5 s` peak off-balance lunge with natural motion blur and palm slapping the right concrete wall; `t=2.5 s` wide-stance braced recovery right-of-center; `t=3.5–4.5 s` braced arm on right wall, free hand dropping to hip/waist, alert freeze. Head/torso/arm silhouette sits directly over the clay dummy (`~3–8%` frame deviation, well inside `≤ 15%`). |
| **(c) Grey / material leakage (anti-leak)** | **5.0 / 5.0** | **PASS (ZERO LEAK)** | **Zero clay, plastic, grey-wall, or grid leakage** in `5/5` frames. Quantitative telemetry confirms full photorealistic material replacement: clay-like mid-grey low-saturation pixels (`S<0.08`, `L∈[100,215]`) dropped from **`99.0%`** (`previs.mp4`) to **`0.19%`** avg (`0.09–0.32%`, lower than `LOC-ALLEY-NIGHT` `0.78%`); mean saturation **`0.5475`** (vs `LOC-ALLEY-NIGHT` `0.5171`, clay `0.0287`); mean luminance **`45.28`** (`LK-ALLEY-NIGHT` `53.71`); max streetlamp blowout **`0.004%`** (`<< 5%` V12a gate). |
| **(d) Identity plausibility at MS scale** | **4.1 / 5.0** | **PASS (with 1 note)** | `Row 4` (2.1× zoom) confirms consistent East Asian male Fan Li across `5/5` frames with believable alarmed expression, matte black cloth cap (`緇布冠`) + horizontal wooden pin (`素木笄`) in `5/5`, dark linen robe + brown trim in `5/5`, waist sash + pale jade disc visible in `2.5–4.5 s`, and **0 bamboo-scroll hallucination** (empty-handed override succeeded). **Minor note**: at `ref_image_size="match"` (`544×960` MS), face looks slightly smoother/younger (~33–37 yrs) than SM-7A's `max`-size CU, and the cross-collar lap briefly flips to `左衽` at `t=3.5 s` before returning to `右衽` at `t=4.5 s`. |
| **(e) Colab L4 memory headroom (SM-3)** | **4.0 / 5.0** | **PASS (tight)** | **0 OOM, 0 retries** on L4 24 GB (`22.034 GiB` usable). Peak VRAM **`20.727 GiB`** (**`1.307 GiB` free headroom**, `94.1%` used) steady across all 8 steps; minimum System RAM **`2.64 GiB` free / `52.96 GiB`** (`95.0%` used). Total Run 1 time **`430.54 s` (`7.18 min`)** incl. cold load (`≤ 10 min` SM-3 gate). |

### Audio Sanity Note
- `h3_out.mp4` (`2,656,147 B`, `5.17 s`, `544×960` 24 fps H.264 + AAC stereo) generated realistic low-level ambient audio (`mean_volume: -25.3 dB`, `max_volume: -0.3 dB`) with no dialogue and no unwanted music (`non_diegetic_music: N/A` honored).

---

## 4. Resource, VRAM & CU Telemetry (SM-3)

| Metric | Measured Value |
| :--- | :--- |
| **Colab Accelerator** | `NVIDIA L4` (`22.034 GiB` usable VRAM, `52.96 GiB` System RAM, `high_mem: true`, `1.71 CU/h`) |
| **Cold Start (allocate + install + download + boot)** | `85.1 s` (`~0.057 CU`) |
| **Run 1 (`h3_r2v_clay.json`, incl. cold model load)** | `430.54 s` (`7.18 min`, `~0.210 CU`; `cu_today: 0.5758 → 0.7857`) |
| **Peak VRAM / Min Free VRAM Headroom** | **`20.727 GiB` / `1.307 GiB` free** (`94.1%` utilization; Qwen3-VL peak `13.41 GiB`, DiT peak `20.73 GiB`, VAE decode `19.45 GiB`) |
| **Min Free System RAM** | **`2.64 GiB` free** / `52.96 GiB` (`95.0%` utilization — `high_mem: true` required) |
| **OOM / Retries** | `0` OOM, `0` retries |
| **Total Clay Test Session CU Spend** | **`0.3897 CU`** (`cu_today: 0.4558 → 0.8455`; 19.5% of `2.0 CU` budget; balance `198.87 CU`) |
| **Gateway State After Run** | `sleeping` (`stopped cleanly`) |

---

## 5. Final Verdict & Four Adoption Conditions

### Verdict: **ADOPT WITH CONDITIONS** (Adopt L3 Clay → H3 Ref2VA for 0–2 Hero Shots / Episode)

The white-model route **works dramatically well** on H3 Ref2VA (`TriPRISM w6a8` 8-step) even on Colab L4: camera drift, Dutch roll, corridor perspective, and stagger-to-wall blocking followed the 3D greybox tightly (`~3–8%` deviation, passing Appendix A §A.6 `≤ 15%`), while material replacement was 100% clean (**0 grey leakage**) without needing `h3-controlnet`.

### Required Conditions for Production Adoption
1. **Condition 1 — SM-6 Previs Authoring Path (VM vs Browser)**:
   - Because this VM currently has `node v18.20.4` and no `npm`/`npx`/`cclay`, CozyClay agent automation is **blocked until Node `>= 22.19` + `npm`/`npx` are provisioned** (and headless SwiftShader export is validated with `cclay telemetry off` and `cclay update --off`).
   - Until then, keep Appendix A's Phase 3 split (**Muse/Creator exports 9:16 24 fps clay MP4 from `cozyclay.org/#try`**) OR use the verified zero-dependency Python 3D clay generator (`render_clay_previs.py`) for simple corridor/blocking agent tests.
2. **Condition 2 — Mandatory `<Picture 1>` Scene Anchor + Division-of-Responsibility Prompt (Anti-Leak)**:
   - Always feed a locked location image (`LOC-*`) in `<Picture 1>` (V3 `scene → characters` order) alongside character masters (`<Picture 2..3>`) and explicit positive replacement wording stating `<Video 1>` owns camera/blocking only while `<Picture 1>` owns all environment materials/lighting. Do **not** feed grey clay `<Video 1>` + grey-backdrop studio character cards alone without a scene anchor. Keep preinstalled `h3-controlnet` (Depth) on standby strictly as fallback if any future shot shows grey material bleed.
3. **Condition 3 — Strict Colab L4 Memory Envelope (SM-3)**:
   - On L4 24 GB (`high_mem: true`), lock L3 runs to **`ref_video_0 ≤ 0.35 MP`** (via `ImageScaleToTotalPixels`), **`ref_image_size="match"`**, **output `0.5 MP` (`544×960`)**, and **duration `≤ 5 s`** (`1.31 GiB` VRAM / `2.64 GiB` RAM headroom). Any L3 hero shot requiring `> 5 s`, `0.8 MP`, or `ref_image_size="max"` must route to A100/G4 instead of L4.
4. **Condition 4 — Shot-Scale Discipline & QC-2 Costume Gate**:
   - Limit L3 clay strictly to **0–2 MS/LS non-dialogue blocking/camera hero shots per episode** (never dialogue face CUs, per Appendix A §A.8; never Fast-Track T2). Because `ref_image_size="match"` showed one brief `t=3.5 s` collar-lap flip (`左衽`), keep QC-2 4-point costume verification mandatory across sampled frames (or bake a QC-1-approved opening frame into `<Picture 1>` when an exact opening pose/collar lock is required).

---

## 6. Deliverables Index (`~/drama-line/claytest/`)

- **Clay Previs Clip (9:16, 24 fps, 5.0 s)**: `~/drama-line/claytest/previs.mp4` (`425 KB`)
- **Synchronized Depth Pass (standby for ControlNet)**: `~/drama-line/claytest/previs_depth.mp4` (`338 KB`)
- **H3 Ref2VA Output Clip (9:16, 24 fps, 5.17 s)**: `~/drama-line/claytest/h3_out.mp4` (`2.66 MB`)
- **5-Frame Comparison & QC-2 Overlay Strip**: `~/drama-line/claytest/compare_strip.jpg` (`1396×1894`)
- **Reusable H3 Clay Ref2VA API Workflow JSON**: `~/drama-line/claytest/workflows/h3_r2v_clay.json`
- **Fallback 3D Clay Renderer Script**: `~/drama-line/claytest/render_clay_previs.py`
- **Raw VRAM/CU Telemetry & Metrics**: `~/drama-line/claytest/telemetry_run1_r2v.json`, `~/drama-line/claytest/metrics_run1_r2v.json`
