# Second Civilization — Production Skills Registry (`skills/`)

> **Governing Principle (Creator, 2026-11-28)**: Every stabilized workflow is distilled into a version-controlled skill package (`protocol + mechanical gates + proven templates + sign-off rules`) so execution quality stops depending on which model pool happens to have quota. Frontier models remain focused on judgment-heavy nodes and skill authorship; mechanical and gated workflows run safely across model pools.  
> **Blueprint**: `~/drama-line/SKILLIFY_MAP_AGY_MEMO.md` (Phase 1 = Tranche 1: 6 proven skills).

---

## 1. Skill Registry (Phase 1 — Active Skills)

| Skill Name | Trigger | Status | Companion Templates / Checklists | Proven Runs (VM Evidence) |
| :--- | :--- | :---: | :--- | :--- |
| **[`quota-dispatch-and-recovery`](quota-dispatch-and-recovery/SKILL.md)** | Any multi-phase unattended `agy` run, HTTP 429 (`RESOURCE_EXHAUSTED`), CLI `--print-timeout`, or Colab allocation hang | `distilled-from-run` | `run_wrapper.sh.tmpl`, `continuation_brief.md.tmpl`, `progress_ledger_schema.md` | 18+ `run_*.sh` dispatches; 3 live 2026-11-28 recoveries (`FULL_RUN_2` `/history/` rescue, `run_recovery.sh` 429 resume, `run_skillify_g.sh` cross-pool switch) |
| **[`repo-sync-and-hygiene`](repo-sync-and-hygiene/SKILL.md)** | Completed spec update, tool patch, asset-registry lock, smoke report, or skill build ready to sync VM → GitHub `agy/*` | `distilled-from-run` | `vm_to_repo_path_map.yaml`, `sync_checklist.md` | 4 completed syncs (`456b84c`, `9fa587f`, `857e719`, `1bd6712`), `0` binaries, `0 main` pushes, in-clone selftests PASS |
| **[`spec-amendment-and-gate-patch`](spec-amendment-and-gate-patch/SKILL.md)** | Approved Creator ruling, accepted postmortem, or GO smoke-test conditions requiring Spec / YAML / gate-tool updates | `distilled-from-run` | `patch_brief.md.tmpl`, `patch_report.md.tmpl`, `flywheel_promotion_checklist.md` | 6 completed spec amendments (`v2.0 → v2.4.1`; `preflight_gate.py` `15→32→59→64/64 PASS`, `diff_sheet_gen.py` `15/15 PASS`) |
| **[`asset-prod-and-qc1`](asset-prod-and-qc1/SKILL.md)** | Approved Pre-1 asset gap list OR QC-0-passed `script_pack.json` entering Stage 3 first-frame generation | `distilled-from-run` | `prop_qc1_checklist.md`, `loc_qc1_checklist.md`, `waf_batch_policy.md`, `asset_prod_brief.md.tmpl` | 3 completed runs (`MASTER_FACE_DECISION`, `DEMO02_v2` Stage 3 QC-1 `6/6`, `ASSET_PROD_REPORT` `17/17` `nano2` w/ `0 WAF 403`, 9 CPU crops, `0 rm`) |
| **[`scorecard-v2-redteam-eval`](scorecard-v2-redteam-eval/SKILL.md)** | New episode script draft, major Canon refactor, or targeted patch review prior to Creator Gate A3 | `distilled-from-run` | `redteam_brief.md.tmpl`, `blind_score_brief.md.tmpl`, `narrow_recheck_brief.md.tmpl`, `scorecard_v2_rubric.md` | 5 completed eval/recheck cycles on EP-01 dry-run (`DRYRUN_EP01_REDTEAM` → `v02_BLINDSCORE` → `v021_RECHECK` → `v03_REVIEW` → `v031_RECHECK`) |
| **[`smoke-test-protocol`](smoke-test-protocol/SKILL.md)** | Evaluating any untested carrier, model, ComfyUI workflow JSON, or generation mode (`SM-5`, `SM-9`, `SM-7B`) under a spend cap | `distilled-from-run` | `smoke_test_brief.md.tmpl`, `smoke_result_report.md.tmpl` | 3 completed smoke tests (`SM-7A`, `SM-2/3/6` Clay Test, `SM-8` split Carrier PASS / Composition Superseded verdict) |

### Deferred Roadmap (Not Yet Authored — Wait for First Full Live Proof)

Per `SKILLIFY_MAP_AGY_MEMO.md` §3, the remaining 6 candidates are deliberately held out of Phase 1 so untested full-episode / v2.4.1 / multi-carrier assumptions are never codified prematurely:

| Planned Skill Name | Trigger | Status | Why Deferred |
| :--- | :--- | :---: | :--- |
| `voice-audition-and-tts-lock` | New character Pre-1 voice audition OR Stage 1.5 TTS-first duration write-back | `draft — first test: EP-01 Pre-1 (SYS01-VOICE) & Stage 1.5` | Voice Design ran twice (`FANLI-CAND-F`), but Stage 1.5 full-episode TTS duration write-back has `0` runs. |
| `script-pack-compile-and-qc0` | Gate A3 + Stage 0.5 Director Statement entering `script_pack.json` compilation & QC-0 | `draft — first test: EP-01 Stage 1 (Schema 2.4)` | Only 6-shot v2.3 demo ran live; Schema 2.4 (`V14` coverage + 29–30 shots + 3 eras) has `0` live runs. |
| `sys01-manifestation-pipeline` | Segments containing `SYS-01` appearance shots + preceding setup shots | `draft — first test: DEMO-03 S3a/S3b or EP-01 S02–S04a/S19` | Carrier A passed `SM-8`, but v2.4.1 eye-level (`0.90–1.00×`) + `editorial_cut_in` + Pre-Shot Cue Triple + `--mode datacard` has `0` runs. |
| `carrier-video-gen-and-qc2` | QC-0 + QC-1 PASS entering Stage 4 multi-carrier video generation & QC-2 | `draft — first test: EP-01 Stage 4–5 (incl. Wan 2.2 / LTX)` | Flow Omni + H3 4-ref + QC-2 proven on `DEMO02_v2`, but Wan 2.2 / LTX (`[未實測]`) and generalized episode-agnostic runners have `0` runs. |
| `assembly-edl-and-finishing` | QC-2 PASS (Stage 6A rough cut) & Creator QC-D PASS (Stage 6B finishing) | `draft — first test: EP-01 Stage 6A–6B` | Only Stage 6A rough cut ran on `DEMO02_v2`; formal `edit_manifest.json` EDL, `cpu_card`, `.ass` subtitles, HUD, Truth Ledger, and `-14.0 LUFS` mastering have `0` runs. |
| `news-intake-and-script-prep` | Mon/Thu news scan or breaking T2 fast-track event → Gates A1–A3 | `draft — first test: EP-02 live Mon/Thu A1–A3` | EP-01 dry-run skipped formal Mon/Thu shortlist gating (`0` completed live A1→A2→A3 passes). |

---

## 2. Model-Tier Routing Table（模型分層與配額韌性路由表）

> **Build-Phase Note（建置期原則）**：**Skill 撰寫、首版規格修訂（Spec Amendment）與硬閘設計本身屬於最高判斷層（Judgment Tier）工作**——由強模型在建置期寫成具機械閘門與回歸自測的 Skill，目的正是讓日常常態執行能安全下放至中階模型或跨供應商配額池，不再因單一模型 429 停擺。  
> **429 配額切換規則（2026-11-28 實測定案）**：
> - 遇 Gemini／個人配額 `429 (RESOURCE_EXHAUSTED)`：依跨池規則立即改派 **`--model "Claude Opus 5.5 (Medium)"`**；若單池退避則跑 `PING_OK` 探測退避（`300s` × ≤6）＋讀 `*_PROGRESS.log` 續跑。
> - 遇 `Third-party quota reached (429)`（Anthropic 池達上限）：立即改派至具額度之跨池同級模型（Gemini 預設旗艦池）。
> - **嚴禁**在未加掛「獨立交叉複核」簽核條件下，將判斷層節點靜默降級給單次輕量模型獨斷。

| Task Class（任務類別） | Preferred Model（首選） | Acceptable Substitute（可接受替代＋簽核規則） | Forbidden-Alone（嚴禁單獨承擔） |
| :--- | :--- | :--- | :--- |
| **1. Skill Authorship, Spec Amendment & Architecture Memos** *(建置期 Skill 撰寫、規格增修、HARD/ADVISORY 分級、路由架構)* | **Tier 1 Frontier** (`Claude Opus 5.5` 或 `Gemini Pro High`) | 另一供應商 **Tier 1**（互為跨池備援）；或 **Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) 草稿 ＋ **Tier 1／Muse 獨立審查** ＋ `--selftest` 全過 | 任何單次未複核之 Tier 2／Flash 模型；無回歸自測之規則改動 |
| **2. Script Red Team, Blind Scorecard v2 & Causal/Fact Audit** *(劇本盲評、紅隊挑錯、史料／事實硬閘查核)* | **Tier 1 Frontier** (`Claude Opus 5.5` 或 `Gemini Pro High`，附網路查核) | **Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) 盲評草稿 ＋ **第二位獨立評審（跨模型或 Muse）交叉核對**（落差 >5 強制裁決） | 單一 Tier 2／Flash 獨斷；作者自審；**任何 LLM 獨斷維度 6（驚奇）或代簽 Gate A3** |
| **3. Creative Direction, Stage 0.5 Director Statement & News→Script Synthesis** *(時事結構破題、范蠡對白、導演闡述與情緒弧線)* | **Muse ＋ Tier 1 Frontier**（Creator 掌 Gate A1–A3） | 跨池 **Tier 1** 協作起草 ＋ **Muse 定稿** ＋ Creator 閘門拍板 | 任何 Flash／輕量模型獨寫定稿；未過 Gate A2 直接寫逐字稿 |
| **4. `script_pack.json` Compilation & Cinematic Prompt Craft** *(原子拆鏡、Schema 2.4 編譯、H3/Flow 方言轉換)* | **Tier 1 Frontier**（首集／新 Schema）或 **Tier 2**（依已驗證 Skill） | **Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) 依 Skill 編譯 ＋ **`preflight_gate.py` `0 FAIL`** ＋ Muse 抽檢對白與 `fact_tier` | 任何跳過 `preflight_gate.py` 之手寫散文／bash prompt；無閘門驗證之 Flash 模型 |
| **5. Visual QC-1 / QC-2 Grading & Smoke-Test Forensic Scoring** *(2.5× 臉領放大核驗、錯邊疤／右衽／V9 判讀、Take 1 敗因診斷)* | **Vision-Capable Tier 1** ＋ `diff_sheet_gen.py` 高解析總表 | **Vision-Capable Tier 2** 依 `bible/anchors/*.yaml` 清單初檢 ＋ **Muse 複核**（英雄鏡／新母圖必呈 Creator） | 無視覺能力之純文字模型；壓縮糊圖（寬 <360px）；任何 LLM 繞過 `diff_sheet_gen.py --verify` |
| **6. Mechanical Execution, Asset Batching, Stage 4/6A Dispatch & Repo Sync** *(跑 `gflow`/`Colab`、WAF 分批、CPU 裁切、ffmpeg 粗剪、`agy/*` 同步)* | **Tier 2** (`Sonnet 5.5` / `Gemini Pro Std`) 驅動確定性工具腳本 | **Flash / 輕量模型** 嚴格照 Skill 步驟呼叫 `tools/*.py`（所有安全邊界由腳本硬閘鎖死：WAF exit-10、`--max-credits`、SHA256 `--verify`、`try...finally` 停機、禁推 `main`） | 任何模型手動繞過工具腳本直接敲無護欄 API／`git push main`／`rm` 刪除母圖 |
| **7. Taiwan Voice Audition, Pronunciation Veto, QC-D Ruling & Final Publish** *(台灣讀音、腔調演技、導演六檢、開拍與發布終審)* | **Human Only（Creator ＋ Muse）** | **無任何模型可替代**（agy 僅產出客觀遙測與聯絡表，明文禁止對台灣讀音或發布下合格判定） | **全部 LLM 與 Whisper ASR**（Whisper 會自動糾正誤讀正字導致假過關） |

---

## 3. NEVER-Skillify Boundary (Permanent Human / Judgment Calls)

The following decision classes must **never** be reduced to an automated skill checklist:
1. **Creator Gates (`A1`, `A2`, `A3`, `Pre-1` locks, `QC-1.5`, `QC-D` 6-dim ruling, `QC-3` publish)** — mechanical perfection ≠ watchable drama (`DEMO02_v2` & `SM-8` proof).
2. **Canon & World-Building Forks** (`ADR-005`, `ADR-011`, Fan Li's memory boundary, `SYS-01` season mystery).
3. **Taiwan Mandarin Voice Pronunciation & Acting Nuance** — permanently Human Only (LLMs & Whisper ASR are blind to tone/accent errors).
4. **Original Dramatic Authorship & Directorial Intent** — V14 enforces coverage floors, never artistic ceilings.
5. **Scorecard v2 Dimension 6 (Surprise) Solo Grading** — LLM may act only as a documented third vote.
6. **Architectural Pivots, Spend-Cap Increases & First-Time Skill Authorship** — require Tier 1 reasoning + Creator sign-off.
