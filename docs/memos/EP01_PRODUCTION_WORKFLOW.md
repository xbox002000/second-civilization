# EP-01 Production Workflow Runbook（《開關的人》v0.3.2｜討論與設計定案稿）

> **文件狀態**：DISCUSSION & DESIGN DRAFT（2026-11-28，**無開拍、零影片生成、零 TTS 消耗**）  
> **基準劇本**：`DRYRUN-EP01-arrival-v0.3.2.md`（Gate A3 終判版，20 鏡／98.5 秒／三時間層：`春秋`・`2022`・`2026`；本文不改動劇本一字）  
> **規格準據**：`STORYBOARD-SPEC-V2.md`（v2.4.1 FINAL）＋ `DESIGN.md`（v1.4）＋ `demo02_v2/FULL_RUN_REPORT.md`（實測成本與路由基準）  
> **2026-11-28 構圖註記同步（Spec v2.4.1 §C.4｜`SYS01-MANIFESTATION-DIRECTION.md`）**：本輪**僅更新 `SYS-01` 出現鏡（`S03`/`S04a`/`S04b`/`S08`/`S10`/`S19`）與其前導預告鏡（`S02`/`S07`/`S18b`）之構圖與剪輯入場註記**——平視 `0.90–1.00×`、站位主角面前同一地平面、半透明且下身消散落地面附近、前鏡三要素預告＋剪輯硬切入已成場（退役仰視英雄尺度，含 2022 初現）；全表時長、對白與引擎路由維持原樣不動。  
> **生產模式**：`production_mode: "normal"`（Phase 3 半自動端到端執行，零豁免全部 v2.3 硬閘）

---

## 1. 階段映射總覽（DESIGN v1.4 × 分鏡規格 v2.3）

EP-01 為本系列第一支完整常線集數，將 DESIGN v1.4 的 8 階段流水線與分鏡規格 v2.3 新增之 **Stage 0.5 導演闡述**、**QC-1／QC-2 雙門對稱比對**、**AMD-05 後製合成** 與 **QC-D 導演檢核** 完整對齊：

| 階段 | 名稱（對齊 DESIGN v1.4 ＋ Spec v2.3） | 負責者 | 核心工具 / 產出 | 閘門與放行條件 |
| :--- | :--- | :--- | :--- | :--- |
| **Pre-1** | **開拍前資產補齊與聲線定版** | agy＋Muse；**Creator 拍板** | 新場景母圖、SYS-01 定妝＋專屬聲線、OUTFIT-01 單視圖裁切、道具卡、客串聲線 | **Gate Pre-1**：`SYS-01` 視覺＋聲線 `LOCKED`、全部 EP-01 `LOC-*` `LOCKED`（見 §3） |
| **0.5** | **導演闡述（Director Statement）** *(Spec v2.3 §B.1)* | Muse 主撰＋agy 工程複核；Creator 審閱 | `episodes/EP01/plan/DIRECTOR_STATEMENT.md`（必先讀 `bible/director/playbook.md`；逐段定情緒曲線、`light_lock_id`、`camera_psychology`、特效拍點與三時間層色溫對比） | **Gate A3（劇本）＋ 導演闡述簽核** |
| **1** | **入口驗證、原子鏡轉譯與資產鎖定確認** *(DESIGN §1.1)* | agy 轉譯＋自動驗證；Muse 驗收 | 依 v0.3.2 鑄造 `episodes/EP01/input/script_pack.json`（schema 2.3，20 劇本鏡→29 原子鏡）；跑 `tools/preflight_gate.py --mode normal` | **QC-0 硬閘**：`0 FAIL`（V1–V13＋AMD-01/04/05/07 全過） |
| **1.5** | **TTS 聲音先行與鏡長鎖定** *(DESIGN §1.1／§4.4)* | agy（VM 直呼 ElevenLabs v4 API，0 GPU）；Muse 盲聽抽檢 | `audio_tts/EP01_REG_{SHOT}_tts_v1.wav`；`ffprobe` 量測實長回寫 `production_state.json`（`duration_from_audio: true`）；重跑 `preflight_gate.py` 覆驗 V1／V2 | **QC-1.0（音訊驗收）**：專名（范蠡 ㄌㄧˇ、輝達、Altman、文種）0 誤讀；S04 拆鏡秒數定案 |
| **2** | **分鏡路由、成本護欄與批次排程** *(DESIGN §1.1／§8.4)* | agy | `gflow credits user --json` 實機查額＋Colab CU 快照→產出 `plan/shot_plan.json`、`comfy_jobs.json`、`gflow_batch.json`（H3 採用 `run_stage4_h3.py` 含 `try...finally` 自動停機範本） | 成本護欄綠燈（Flow >300 點、Colab >60 CU） |
| **3** | **逐鏡專屬首幀生成與跨鏡比對** *(DESIGN §1.1 ＋ Spec §C.2/C.3)* | agy（Flow `nano2` 0 點產圖，嚴守 AMD-04 Path A/B/C）；Muse 初檢＋**Creator 審新場／英雄鏡** | `frames_approved/*.jpg`；執行 `tools/diff_sheet_gen.py --mode qc1 --anchors-dir bible/anchors/` 產出各場段 `qc1_diff_sheet.jpg`＋`qc1_gate.json` | **QC-1 硬閘**：`diff_sheet_gen.py --verify qc1_gate.json` PASS（全鏡 5 鍵 PASS、零錯邊疤／反領／時代穿幫） |
| **3.5** | **低成本動態分鏡預演（Animatic）** *(DESIGN §1.3)* | agy（Colab L4 LTX `384×672`/`512×896` N=1＋正式 TTS＋`cpu_card` 草稿）；**Creator 3 分鐘審節奏** | `episodes/EP01/previs/EP01_animatic.mp4`（**不驗口型**；僅驗三時間層節奏、TTS 語速、S01↔S16b 首尾呼應、確認 `lip_sensitive` 清單） | **QC-1.5 硬閘**：Creator 簽核節奏與 `lip_sensitive` 清單（快檢選項見 §6 Q2） |
| **4** | **雙引擎並行批量影片抽卡** *(DESIGN §1.1 ＋ Spec §C.1)* | agy（4A Colab L4：H3 4-ref Ref2VA ＋ L3 Clay Ref2VA ∥ 4B `gflow video`：Omni 1.2 Flash） | `clips_raw/EP01_REG_{SHOT}_*.mp4`（頭尾預留緩衝；H3 標準化 `544×960` 8-step TriPRISM `max`；L3 硬鎖 `ref_video_0 ≤0.35MP`＋`match`＋`≤5s`） | 入口強制通過 `qc1_gate.json` SHA256 驗簽 |
| **5** | **AMD-05 後製合成、預篩與跨鏡成片驗收** *(DESIGN §1.1 ＋ Spec §C.2/C.4)* | agy（`tools/sys01_composite.py` 採新預設 `ry=0.21` 處理 6 鏡 SYS-01 彈窗；跑 `diff_sheet_gen.py --mode qc2 --anchors-dir bible/anchors/`）；Muse 初篩＋**Creator 挑片拍板** | `clips_comp/`、`qc2_diff_sheet.jpg`、`qc2_gate.json`、`selected_takes.json`、回寫 `metrics/yield_log.jsonl` | **QC-2 硬閘**：`diff_sheet_gen.py --verify qc2_gate.json` PASS（6 鍵全過、0 錯邊疤、0 灰模滲漏、口型起迄 ±0.3s） |
| **6A** | **粗剪組裝（Rough Assembly）** *(Spec §B.5)* | agy（`ffmpeg` 頭尾各裁 0.5s、H3 升頻至 `1080×1920` 24/30fps、四軌混音：A1 TTS／A2 段級 `library_roomtone` `-24dBFS`＋0.25s crossfade／A3 Foley／A4 選配 BGM、先不含精修角標） | `episodes/EP01/edit/EP01_rough_cut.mp4`＋`qcd_timeline.jpg`＋`qcd_cut_boundaries.jpg` | 入口強制通過 `qc2_gate.json` SHA256 驗簽 |
| **QC-D** | **導演檢核閘（Director QC）** *(Spec §B.5 — 位於 6A 後、6B 前)* | Muse＋agy 逐切點抽幀自檢；**Creator 審粗剪** | 六檢（合理性／情緒可讀／鏡頭多元／光線連續／運鏡心理／特效拍點）＋寫入新條目至 `bible/director/playbook.md` | **QC-D 硬閘**：零結構性跳軸／情緒斷裂／姿勢接點斷層 |
| **6B** | **精修母帶、字幕與事實分層疊加** *(DESIGN §7.2)* | agy（以 TTS 音軸生成繁中 `.ass` 字幕、疊加 FACT/INFERENCE/FICTION 動態角標、`S05`/`S11b`/`S20` 圖卡與片尾 Truth Ledger、`-14.0 LUFS` / `≤ -1.5 dBTP`） | `master_clean.mp4`（無字無標乾淨母帶）＋ `EP01_master_9x16_rc1.mp4` | 自動音訊電平與字幕零超窗驗證 |
| **7** | **社群封裝與通路素材** *(DESIGN §0.3／§1.1)* | agy 草稿；Muse 校對 | IG 獨立新帳號封面、Threads 15–20s 鉤子預告＋分層串文、YT Shorts 文案、Personal Lab Episode Dossier `.md` | 對齊 ADR-007 獨立帳號規範（零 `@chao.and.nao`、零 Collab） |
| **8** | **終審簽核、成本回報與歸檔交接** *(DESIGN §1.1)* | **Creator 終審簽核並手動發布**；agy 打包歸檔 | `approval_final.json`、`cost_report.md`、`manifest_sha256.txt`、MVP 校準表 `mvp_calibration.json`（48h 內回填） | **QC-3 硬閘**：創作者終審簽核（嚴禁自動發布） |

---

## 2. 分場設計與逐鏡路由草表（v0.3.2 20 劇本鏡 → 29 原子鏡）

### 2.1 五場段劃分（`segments[]`）

| `segment_id` | 涵蓋鏡號 | `time_layer` | `scene_id` | `light_lock_id`（暫定） | `ambience`（§2.1 `library_roomtone`） | 服裝 |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **SEG-01** | `S01` | `春秋` | `LOC-TAIHU-DAWN` | `LK-TAIHU-MIST`（冷灰藍晨霧漫射光） | `taihu_dawn_water_48k`（水聲、遠岸霧靜） | `FANLI-OUTFIT-02` |
| **SEG-02** | `S02`–`S04c` | `2022` | `LOC-TAIPEI-STREET-2022` | `LK-TAIPEI-DUSK22`（冷青灰都會陰天／傍晚街燈） | `taipei_street_crowd_48k`（車流與低聲人流） | `FANLI-OUTFIT-02`（穿越著古裝抵現代！） |
| **SEG-03** | `S05`–`S12` | `2026` | `LOC-FANLI-STUDIO-26`（＋`S05`/`S11b` 卡片） | `LK-STUDIO-NIGHT26`（室內冷桌燈＋窗外巨幕偏冷青反光） | `studio_night_hum_48k`（室內靜＋窗外微弱城市低鳴） | `FANLI-OUTFIT-01`（現代丁案） |
| **SEG-04** | `S13`–`S16b` | `春秋` | `LOC-YUE-COURT` / `LOC-WENZHONG-GATE` / `LOC-TAIHU-DAWN` | `LK-COURT-TORCH`（暖琥珀燭火高反差）→ `LK-TAIHU-MIST` | `ancient_hall_torch_48k` → `taihu_dawn_water_48k` | `FANLI-OUTFIT-03`（S13）→ `OUTFIT-02`（S16b） |
| **SEG-05** | `S17a`–`S20` | `2026` | `LOC-FANLI-STUDIO-26`（＋`S20` 卡片） | `LK-STUDIO-NIGHT26`（切回 2026 冷調，S18b/S19 壓暗收斂） | `studio_night_hum_48k`（S19 抽空切黑） | `FANLI-OUTFIT-01` |

> **時代錨點特別注意（已驗證於 `tools/diff_sheet_gen.py --anchors-dir bible/anchors/`）**：`SEG-02`（`2022` 入場段 `S02`–`S04c`）雖屬 `2022` 時間層，但范蠡剛穿越仍著 `FANLI-OUTFIT-02`——因此 **硬禁** `ANC-FANLI-03`（方孔錢）與 `ANC-FANLI-04`（舊銅腕錶），且髮型鎖定 `ancient_outfit02`（緇布冠＋素木笄）。`SEG-03`／`SEG-05` 著 `FANLI-OUTFIT-01` 時才啟用現代低馬尾＋左腕舊銅錶。

### 2.2 V2 對白速率預檢關鍵發現（不改劇本，於原子拆鏡層化解）

依 Spec v2.3 §6.1 V2 公式（可用時長 $= \text{target\_net\_sec} - \text{reaction\_hold\_sec} - 0.35\text{s} \times \text{換人輪數}$；上限純字 $\le 5.0$ 字/秒、含標點 $\le 5.5$ 字/秒；英文詞 1 詞 $= 2$ 漢字）：
- **19/20 劇本鏡原始估算 PASS**；全集總字數精算為 **236 純字**（含標點 **292 字**，原文串 294 字元）。
- **唯一 V2 硬閘警示 — `S04`**：原文 3 句（系統 12 字 → 范蠡 2 字 → 系統 12 字；合計 24 純字／33 含標點、2 次換人扣 `0.70s`、反應拍 `1.50s`）。在原始 `6.5s` 單鏡下，可用時長僅 `4.30s`，速率達 **5.58 純字/秒（含標點 7.67）→ `FAIL_V2`**；且單鏡 `6.5s` 淨長（生成 `7.5s`）亦超過 Colab L4 H3 4-ref 硬上限（`gen ≤ 6.5s`）。
- **V1 時長包絡與原子鏡拆解方案（遵循 Spec v2.3 §一／§七／§B.7）**：
  1. **`S04` 拆三原子鏡**（`S04a` 3.0s 系統句 1 → `S04b` 3.8s 范蠡「免費？」＋系統「范蠡先生」→ `S04c` 1.8s 無聲僵住轉身反應拍；合計 8.6s，三鏡各自 PASS V1 與 V2；可於 Stage 1.5 依實測 TTS 秒數微調其他空景 1.5–2.0s 維持總片長 ~99–100s）。
  2. **`S11` 依 Spec §七拆三**（`S11a` H3 對白 ＋ `S11b` `cpu_card` Altman 2023 卡 ＋ `S11c` H3 對白）。
  3. **`S14` 拆二**（`S14a` 朝堂空座 ＋ `S14b` 竹簡信送至文種門前，綁共用音組 `AG-S14`，杜絕單鏡跨空間跳切）。
  4. **`S15` 拆二**（`S15a` 文種背影讀信 ＋ `S15b` 朝堂空座，遵守 Spec §一禁止單鏡多切鏡）。
  5. **`S16` 依 v0.3.2／Spec §七拆二**（`S16a` 捧劍手部特寫 ＋ `S16b` 太湖閉眼 `ref_shot: S01`，共用音組 `AG-S16`）。
  6. **`S17` 與 `S18` 依 §B.7 #1 拆成「短引鏡＋主對白 CU」**（`S17a` 1.5s＋`S17b` 4.5s；`S18a` 1.8s 抬手放下＋`S18b` 4.5s），確保每顆 H3 4-ref 對白 CU 淨長嚴守 `≤ 5.0s`（生成 `≤ 6.0s`），穩落 Colab L4 建議包絡內。

### 2.3 逐鏡路由與驗證草表（全 29 顆原子鏡）

> 縮寫：`H3-4Ref`＝Colab L4 原生 4 槽 Ref2VA（`h3_r2v_4ref_groupB.json`，`544×960` 8-step `max`）；`L3-Clay`＝白膜預演＋H3 Ref2VA（`h3_r2v_clay.json`，`≤5s` `match`）；`Flow-Omni`＝Google Flow Omni 1.2 Flash（`i2v_first`）；`AMD-05`＝`tools/sys01_composite.py` 後製四層合成（新預設 `ry=0.21`）。V2 欄顯示「純字數／可用秒數＝純字速率（含標點速率）」。

| 原子鏡 | 原鏡／時段 | 淨秒數(估) | 景別／時代／服裝 | 主載體與後製層 | 首幀路徑（AMD-04） | 對白話者＆V2 密度檢核 | `lip_sensitive` | 控制級＆工程備註 |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **S01** | S01 (0–4s) | 4.0s | LS→MS / 春秋 / `OUTFIT-02` | **L3-Clay** *(備援 Flow-Omni)* | `l3_clay_frame0`（Path C，`LOC-TAIHU-DAWN` 作 `<Pic 1>`） | 無對白（PASS） | `false` | **L3 候選 #1**（Spec §A.8）；首幀為 `S16b` 呼應基準 |
| **S02** | S02 (4–9s) | 5.0s | MS / 2022 / `OUTFIT-02` | **Flow-Omni** ＋ L4 字卡 | `generated`（`LOC-TAIPEI-STREET-2022` 段首錨鏡） | 無對白（PASS） | `false` | L1；後製疊 `2022.11.30 ChatGPT 誕生`；簽名動作 1（驚・按空腰間）；**〔v2.4.1 前導構圖〕尾段設前鏡三要素預告組（范蠡臉側冷青光閃＋`sound_drop`＋眼平視線轉向正前方長椅側預定位，非仰視半空），硬切導入 `S03`** |
| **S03** | S03 (9–15s) | 5.5s | MS / 2022 / `OUTFIT-02` | **Flow-Omni**（底板）＋ **AMD-05** | `derived_shot`（Path A，承 `S02`） | SYS-01：18字/5.5s = **3.27**（3.82）PASS | `false` | L1；范蠡不開口；簽名動作 2（懼・退半步再按空）；後製「蠡」閃 2 幀；**〔v2.4.1 構圖定調〕退役 2022 仰視英雄尺度，採剪輯硬切入已成場（`editorial_cut_in`）——硬切瞬間 `SYS-01` 已半透明、平視（`0.90–1.00×`、`eye_level_in_front`）站位於范蠡面前同一地平面、下身粒子消散點落於地面附近（絕非懸空漂浮）；首幀以 `nano2`（0 點）重組** |
| **S04a** | S04 拆 1 | 3.0s | MCU / 2022 / `OUTFIT-02` | **Flow-Omni**（底板）＋ **AMD-05** | `derived_shot`（Path A，承 `S03`） | SYS-01：12字/3.0s = **4.00**（5.00）PASS | `false` | L1；范蠡沉默聆聽；SYS-01 說「有問題…免費的」；**〔v2.4.1 構圖定調〕`already_present` 延續 `S03`——`SYS-01` 半透明、平視（`0.90–1.00×`、`eye_level_in_front`）站位於范蠡面前同一地平面、下身消散落地面附近（嚴禁仰視懸浮），首幀 `nano2` 對齊 `S03`** |
| **S04b** | S04 拆 2 | 3.8s | CU / 2022 / `OUTFIT-02` | **H3-4Ref**（底板）＋ **AMD-05** | `derived_shot`（Path A，承 `S04a`＋修補版 `45R`/`cu`） | 范蠡2字＋SYS12字（1換人-0.35s）→ 14/3.45 = **4.06**（5.51*） | **`true`** | L1；*TTS 實測若 >3.8s 則放至 4.0s（含標點降至 5.21 PASS）；**〔v2.4.1 構圖定調〕范蠡平視 CU 視線對向正前方同高之 `SYS-01`（非仰視半空），臉側承接前方眼平冷青回光** |
| **S04c** | S04 拆 3 | 1.8s | CU / 2022 / `OUTFIT-02` | **H3-4Ref**（閉唇反應鎖） | `derived_shot`（Path A，承 `S04b`） | 無對白（反應拍 1.8s，PASS） | `false` | L1；僵住→銳利盯視→轉身離去（H3 生成端依 `H3_MIN_DURATION` 自動墊至 `4.0s / 107f` 再於 Stage 6A 裁切） |
| **S05** | S05 (21.5–24.5s) | 3.0s | CARD / 2026 / — | **`cpu_card`**（Pillow＋ffmpeg） | `none_cpu_card` | 無對白（PASS） | `false` | L4（0 GPU / 0 點）；`2026.11.23`＋輝達三連新聞卡（綁 F1–F3 FACT） |
| **S06** | S06 (24.5–28s) | 3.5s | MS / 2026 / `OUTFIT-01` | **Flow-Omni** ＋ 後製待機字幕層 | `generated`（`LOC-FANLI-STUDIO-26` 段首錨鏡） | 無對白（PASS） | `false` | L1；毛筆紙本鈔票＋窗外巨幕；桌上小屏待機字樣 `1,454 天` **後製疊入**（V9） |
| **S07** | S07 (28–34s) | 5.2s | MCU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S06`＋`OUTFIT-01` 單視圖） | 范蠡：19字/5.2s = **3.65**（4.42）PASS | **`true`** | L1；注意 17-frame 進位：生成 `6.2s` 實進位 `158f = 6.583s`（跨出已測 `141f / 5.88s` 桶），Stage 1 應以 `tail_only` 壓至 `≤5.8s` 或依 v2.4 覆蓋拆為 `S07a (3.7s) + S07b (1.5s ECU)`；**〔v2.4.1 前導構圖〕尾段設前鏡三要素預告組（臉側冷青光閃＋`sound_drop`＋眼平視線轉向書桌正前方預定位），硬切導入 `S08`** |
| **S08** | S08 (34–39s) | 5.0s | MS / 2026 / `OUTFIT-01` | **Flow-Omni**（底板）＋ **AMD-05** | `derived_shot`（Path A，承 `S07`） | SYS-01：19字/5.0s = **3.80**（4.60）PASS | `false` | L1；側欄圖解由後製合成進預留暗區（V9 禁 AI 畫圖表）；**〔v2.4.1 構圖定調〕承 `S07` 三要素預告剪輯硬切入已成場（`editorial_cut_in`）——`SYS-01` 半透明、平視（`0.90–1.00×`、`eye_level_in_front`）站位於范蠡書桌面前同一地平面、下身粒子消散點落於地面附近（絕非懸空漂浮）；首幀 `nano2` 0 點重組** |
| **S09** | S09 (39–44s) | 4.8s | CU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S07`/`S08`） | 范蠡：14字/4.8s = **2.92**（3.75）PASS | **`true`** | L1；「會死多少人？」慢推壓迫（`slow-push-verdict`） |
| **S10** | S10 (44–49s) | 5.0s | MS / 2026 / `OUTFIT-01` | **Flow-Omni**（底板）＋ **AMD-05** | `derived_shot`（Path A，承 `S08`） | SYS-01：20字/5.0s = **4.00**（4.80）PASS | `false` | L1；系統平靜回覆，范蠡低頭不語（`z4_calm_breath`）；**〔v2.4.1 構圖定調〕`already_present` 承 `S08`——`SYS-01` 半透明、平視（`0.90–1.00×`、`eye_level_in_front`）站位於范蠡面前同一地平面、下身消散落地面附近（非懸空）** |
| **S11a** | S11 拆 1 | 2.6s | MCU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S09`） | 范蠡：10字/2.6s = **3.85**（4.62）PASS | **`true`** | L1；起身：「這齣戲，三年前演過一次。」（H3 生成端自動墊至 `4.0s / 107f` 再裁切） |
| **S11b** | S11 拆 2 | 2.2s | CARD / 2023痕跡 / — | **`cpu_card`**（Pillow＋ffmpeg） | `none_cpu_card` | 無對白（PASS） | `false` | L4（0 GPU / 0 點）；2023 Altman 新聞卡（綁 F5 FACT 角標） |
| **S11c** | S11 拆 3 | 2.0s | CU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S11a`） | 范蠡：8字/2.0s = **4.00**（5.00）PASS | **`true`** | L1；「演員不同。開關一樣。」（H3 生成端依 `H3_MIN_DURATION` 自動墊至 `4.0s / 107f` 再於 Stage 6A 裁切） |
| **S12** | S12 (55–58s) | 3.0s | CU / 2026 / `OUTFIT-01` | **H3-4Ref** *(若拍燭火剪影側臉可改 Flow)* | `derived_shot`（Path A，承 `S11c`） | 范蠡：10字/3.0s = **3.33**（4.33）PASS | **`true`** | L1；低聲收句＋Match Cut 暖光過渡（剪輯端以短疊化／閃火銜接 S13） |
| **S13** | S13 (58–63s) | 5.0s | MS / 春秋 / `OUTFIT-03` | **Flow-Omni** *(可選 L3-Clay #2)* | `generated`（`LOC-YUE-COURT` 場段首鏡） | 勾踐畫外：11字/5.0s = **2.20**（2.60）PASS | `false` | L1；文種僅背影、勾踐不露臉；范蠡立側後神色轉冷（不張口） |
| **S14a** | S14 拆 1 | 2.5s | MS / 春秋 / — | **Flow-Omni** | `derived_shot`（Path A，承 `S13` 朝堂空座） | 范蠡畫外（`AG-S14` 前半）：8字/2.5s = **3.20** PASS | `false` | L1；`face_visible=false`；空座定鏡＋燭火微搖 |
| **S14b** | S14 拆 2 | 3.5s | MS / 春秋 / — | **Flow-Omni** *(可切 Wan 2.2 省點)* | `generated`（`LOC-WENZHONG-GATE` 新門庭景） | 范蠡畫外（`AG-S14` 後半）：9字/3.5s = **2.57** PASS | `false` | L1；`face_visible=false`；竹簡信送至門前（`PROP-BAMBOO-SCROLL`） |
| **S15a** | S15 拆 1 | 3.2s | OTS背影 / 春秋 / — | **Flow-Omni** *(可切 Wan 2.2 省點)* | `derived_shot`（Path A，承 `S14b` 內室延伸） | 文種背影：12字/3.2s = **3.75**（4.69）PASS | `false` | L1；`face_visible=false`；背影展竹簡讀信 |
| **S15b** | S15 拆 2 | 1.8s | LS / 春秋 / — | **Flow-Omni** | `derived_shot`（Path A，承 `S13`/`S14a` 朝堂） | 無對白／L-cut 尾音（PASS） | `false` | L1；`face_visible=false`；朝堂上文種空座（稱病不朝） |
| **S16a** | S16 拆 1 | 2.0s | INSERT / 春秋 / — | **Flow-Omni** *(可切 Wan 2.2 省點)* | `generated`（道具特寫 `PROP-SWORD-02` 越王賜劍） | 范蠡畫外（`AG-S16` 前半）：3字/2.0s = **1.50** PASS | `false` | L1；`face_visible=false`；內侍雙手橫托玄黑帛布奉青銅賜劍（不露臉；依 Creator 2026-11-28 插鏡時長紀律由 3.0s 縮至 2.0s，合規 `INSERT_ECU_DURATION ≤2.0s`） |
| **S16b** | S16 拆 2 | 3.0s | MS / 春秋 / `OUTFIT-02` | **Flow-Omni** *(若改 MCU 則切 H3-4Ref)* | **`ref_shot`（鎖定 `S01` 同構圖！）** | 范蠡畫外（`AG-S16` 後半）：6字/3.0s = **2.00** PASS | `false` | L1；使者小舟靠近、范蠡閉眼（`z3_closed_still_lips`），與 S01 同構呼應 |
| **S17a** | S17 拆 1 | 1.5s | MS背側 / 2026 / `OUTFIT-01` | **Flow-Omni** | `derived_shot`（Path A，承 `S06` 窗前機位） | 范蠡（J-cut 起音 10字跨至 S17b） | `false` | L1；切回 2026 窗外巨幕，為 S17b 減壓至 L4 H3 安全秒數 |
| **S17b** | S17 拆 2 | 4.5s | CU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S09`/`S11c`） | 范蠡：14–18字/4.5s = **3.11–4.00**（4.67）PASS | **`true`** | L1（Spec §A.8 定案 H3 六段式 4-ref）；全集核心判讀句 |
| **S18a** | S18 拆 1 | 1.8s | MCU / 2026 / `OUTFIT-01` | **Flow-Omni** | `derived_shot`（Path A，承 `S17b` 轉向桌面） | 無對白（靜拍 1.8s，PASS） | `false` | L1；簽名動作 3（手抬起又放下、不按腰間）——獨立成鏡確保動作清晰 |
| **S18b** | S18 拆 2 | 4.5s | CU / 2026 / `OUTFIT-01` | **H3-4Ref** | `derived_shot`（Path A，承 `S18a`） | 范蠡：21字/4.5s = **4.67**（5.78*→給 4.8s 降為 5.42 PASS） | **`true`** | L1；全集最高張力質問句；*Stage 1.5 依 TTS 實長鎖 4.8–5.0s；**〔v2.4.1 前導構圖〕尾段范蠡眼平盯向正前方桌面側＋冷青光微回打＋環境聲抽空收束，硬切導入 `S19`** |
| **S19** | S19 (92–95s) | 3.0s | CU / 2026 / SYS-01 | **Flow-Omni**（`i2v_first` 實景原生全息）＋ **AMD-05 v3 後製精修** *(備援：雙全息靜幀微過渡)* | 核准之 `SYS-01` 全息正面特寫（R1C1→R1C5 雙鎖；**零 UI／零文字**） | 無對白（PASS） | `false` | L1＋後製；**微笑首次遲疑 0.5 秒**→後製邊緣「蠡」閃 2 幀→硬切黑（`hold_justification`: **final image / hesitation beat** — 終鏡季線反轉定格，保留 3.0s）；**〔v2.4.1 構圖定調〕`solo_cu` 平視 85mm 正面胸上特寫（承 `S18b` 硬切入已成場 `editorial_cut_in`，眼平對齊范蠡面前同地平面站位、半透明、絕非仰視懸浮）** |
| **S20** | S20 (95–98.5s) | 3.5s | CARD / 片尾 / — | **`cpu_card`**（Pillow＋ffmpeg） | `none_cpu_card` | 無對白（PASS） | `false` | L4（0 GPU / 0 點）；下集預告字卡＋完整 Truth Ledger 聲明卡 |

**路由彙總（29 原子鏡，總淨長約 ~100–102s，Stage 1.5 TTS 定長後收束至 98.5–101s）**：
- **Colab L4 H3 4-ref Ref2VA**：**9 鏡**（`S04b`、`S04c`、`S07`、`S09`、`S11a`、`S11c`、`S12`、`S17b`、`S18b`；含 `S04b` 後製疊 SYS-01）
- **Colab L4 L3 Clay＋H3 Ref2VA**：**1 鏡**（`S01`；`S13` 列為可選第 2 顆，嚴守 0–2 鏡／集）
- **Flow Omni 1.2 Flash（`i2v_first`）**：**16 鏡**（含 5 鏡 SYS-01 乾淨底板：`S03`/`S04a`/`S08`/`S10`/`S19`；其中 `S14b`/`S15a`/`S16a` 3 顆無正臉古裝鏡可視 Flow 餘額改走 Colab Wan 2.2）
- **CPU 圖卡（`cpu_card`）**：**3 鏡**（`S05`、`S11b`、`S20`，0 GPU、0 Flow 點）
- **AMD-05 SYS-01 後製合成層**：共觸及 **6 鏡**（`S03`、`S04a`、`S04b`、`S08`、`S10`、`S19`），一律經 `tools/sys01_composite.py`（新預設 `ry=0.21`）處理。

---

## 3. Stage 1 前必補資產缺口清單（Just-In-Time 最小集）

對照 `ASSETS_MANIFEST.yaml` 與 `casting/master/` 現況，目前僅有 `LOC-ALLEY-NIGHT` 一張場景母圖，其餘 EP-01 所需資產缺口與產製方式如下：

| 類別 | 缺口資產 ID | 用途鏡號 | 現況 | 產製方法與成本 | 鎖定門檻 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **角色／UI** | **`SYS-01` 定妝人像**（含常態微笑＋遲疑 0.5 秒表情基準） | `S03/04a/04b/08/10/19` | `PENDING_DESIGN`（本輪產 3 方向×2 張候選） | Flow `nano2` 0 點產圖（本輪已完成 6 張候選，見 `SYS01_DESIGN_PROPOSAL.md`）；定案後補拍 1 張「微遲疑」基準圖 | **Creator Gate 拍板** |
| **角色聲線** | **`SYS01-VOICE`**（`bible/voices/SYS01.yaml`） | `S03/04a/04b/08/10` | `PENDING` | ElevenLabs Voice Design（`eleven_v4`，依 `SYS01_DESIGN_PROPOSAL.md` §5 規格抽樣＋四詞一票否決驗收） | **Creator 試聽鎖定** |
| **客串聲線** | **`GOUJIAN`（勾踐）／`WENZHONG`（文種）** | `S13`（11字）／`S15a`（12字） | 缺件（各 1 句畫外／背影） | ElevenLabs Voice Library 篩選 2 組成熟男聲（Starter 10 槽額度內，~500 試聽字）或單次 Voice Design，記輕量 YAML | Muse 驗音＋Creator 確認無大陸腔 |
| **主角現代母圖** | **`OUTFIT-01` 單視圖 4 槽母圖組**（正面 CU＋左 45°＋**右 45° 無疤**） | `S07/09/11a/11c/12/17b/18b`（7 鏡 H3 4-ref） | 僅有 `fanli-modern-charactercard-*.png`（多格卡，Spec §3.C.1 **硬禁未裁切直接餵圖**）與鏡像 `userface.png` | 裁切／經 Flow `nano2` 以未翻轉 `userface`＋`OUTFIT-01` 重建 3 張單視圖（左眉疤修正回解剖左眉、右眉 100% 無疤），經 QC-1 2.5× 核驗鎖庫 | Muse＋agy QC-1 驗簽（**禁水平翻轉**） |
| **主角朝服確認** | **`FANLI-OUTFIT-03` 正面傷痕確認** | `S13`（MS 側後方） | `LOCKED`（註記正面傷痕偏淡） | `S13` 為中景（`ANC-FANLI-01` 屬 `OPT`），不需為 EP-01 阻塞；由 Creator 決定是否順手補修 1 張 `nano2`（0 點） | 見 §6 Open Question #5 |
| **場景母圖** | **`LOC-TAIHU-DAWN`**（晨霧太湖與獨舟空座） | `S01`、`S16b` | 缺件 | Flow `nano2`（0 點）生成 9:16 空景母圖（2–3 張挑 1）；如 `S01` 走 L3，另備 `render_clay_previs.py` 或 `cozyclay.org/#try` 4s 灰模片 | Muse＋Creator 審光線基調 |
| **場景母圖** | **`LOC-TAIPEI-STREET-2022`**（台北街頭・柱子與長椅） | `S02`、`S03`、`S04a–c` | 缺件（EP-01 v0.3.2 抵達場為街頭＋長椅，非 DEMO-02 窄巷） | Flow `nano2`（0 點）生成 9:16 台北傍晚街頭空景（無可讀招牌文字，保留路柱與長椅空間）＋反打角 `LOC-TAIPEI-STREET-2022-REV` | Muse＋Creator 確認無違規文字 |
| **場景母圖** | **`LOC-FANLI-STUDIO-26`**（范蠡 2026 小套房：書桌＋窗外巨幕） | `S06`–`S12`、`S17a`–`S18b`（12 鏡主場！） | 缺件（最關鍵常駐景） | Flow `nano2`（0 點）生成 3 角度固定空景（書桌正面／窗外巨幕側景／桌面俯角），毛筆紙本留白、窗外巨幕模糊無字（V9） | **Creator 核准（常駐多集共用）** |
| **場景母圖** | **`LOC-YUE-COURT`**（春秋越國大殿慶功／空座）＋ **`LOC-WENZHONG-GATE`**（文種門庭） | `S13`、`S14a/b`、`S15a/b` | 缺件 | Flow `nano2`（0 點）生成春秋先秦素樸木構燭火空景（嚴禁明清宮殿紅牆雕龍與漢字匾額） | Muse 考據檢核＋鎖定 |
| **道具特寫卡** | **`PROP-BAMBOO-SCROLL`**（無字竹簡信）＋ **`PROP-YUE-SWORD`**（春秋青銅古劍，素樸無銘文） | `S14b`、`S15a`、`S16a` | 缺件 | Flow `nano2`（0 點）各產 1 張無字特寫參考卡（V9 禁可讀篆字） | Muse 核對無亂碼文字 |
| **環境音底床** | 4 條 48kHz CC0 `roomtone`（太湖晨霧／台北街頭／深夜室內／先秦燭火大殿）＋關鍵 Foley | 全集 A2／A3 音軌 | 現僅有 `alley_night_wet_48k.wav` | 自免版稅／CC0 音效庫整理或本地合成 48kHz 無縫底噪歸檔至 `audio_lib/roomtone/`（0 元） | agy `volumedetect` 驗淨 |

---

## 4. 預算與工時估算（以 DEMO-02 v2 實測數據為準）

### 4.1 實測單價與重抽倍率假設（明示）

基準來源：`demo02_v2/FULL_RUN_REPORT.md` §2＆§7（DEMO-02 v2 實測重抽倍率為 `8 takes / 6 shots = 1.33×`）：
- **Flow Omni 1.2 Flash 影片**：實測 **`3.0 點／生成秒`**（`4s=12點`、`5s=15點`、`6s=18點`），耗時 ~**76–88 秒／take**。
- **Flow `nano2` 首幀／資產產圖**：**`0` 影片點數**，耗時 ~**60–95 秒／張**。
- **Colab L4 H3 4-ref Ref2VA**（`544×960` 8-step `max`）：實測 **`0.122–0.166 CU／take`**（均取 **`0.16 CU`** 推論＋20% 冷啟動攤提≈**`0.20 CU／take`**），耗時 ~**4.5–5.5 分鐘／take**。
- **Colab L4 L3 Clay＋H3 Ref2VA**（`h3_r2v_clay.json`，`≤5s` `match`）：實測 `7.18 分／take` ≈ **`0.24 CU／take`**（含冷啟動≈**`0.28 CU`**）。
- **EP-01 重抽倍率假設**（首支跨三時代全集，高於單場 DEMO-02）：
  - **預期情境（Expected）**：Flow **`1.5×`**、H3 4-ref **`1.6×`**、L3 Clay **`2.0×`**、首幀 `nano2` **`1.6×`**、TTS **`2.5×`**。
  - **保守上限（Conservative Stress）**：Flow **`2.2×`**、H3 4-ref **`2.3×`**、L3 Clay **`3.0×`**、TTS **`3.5×`**。

### 4.2 EP-01 全集資源預算總表

| 資源項目 | 計算明細（預期情境） | 預期實耗 | 保守上限 | 月度配額佔比（預期） |
| :--- | :--- | :---: | :---: | :---: |
| **Google Flow 影片點數** | 16 鏡 Flow Omni（均生成長 `4.8s` × `3.0 點/s` = `14.4 點/take`）× `1.5×`（24 takes）<br>*（若將 `S14b/S15a/S16a` 3 鏡改走 Wan 2.2，預期再省 ~65 點 → **~280 點**）* | **~346 點** | **~507 點** | **33.0%**（上限 1,050 點） |
| **Google Flow 產圖（`nano2`）** | Pre-1 新資產 ~18 張 ＋ Stage 3 首幀 26 鏡 × `1.6×` ≈ ~60 張 | **0 點** | **0 點** | **0%**（免費） |
| **Colab L4 CU** | • H3 4-ref：9 鏡 × `1.6×`（14.4 takes）× `0.16 CU` = `2.30 CU`<br>• L3 Clay：1 鏡 × `2.0×`（2 takes）× `0.24 CU` = `0.48 CU`<br>• Stage 3.5 LTX 預演（26 鏡 `N=1`）= `0.60 CU` *(若採 0 GPU 靜態板則為 0)*<br>• 冷啟動與異常重試緩衝（3–4 次喚醒）= `0.90 CU` | **~4.3 CU** | **~7.5 CU** | **2.2%–3.8%**（上限 200 CU） |
| **ElevenLabs TTS 字符** | • 正片 14 句原文 **294 字** × `2.5×`（含情緒調整／糾音）= **~735 字**<br>• *(另計一次性 Pre-1 聲線定版：`SYS-01`＋2 客串試聽約 ~2,000–3,000 字)* | **~735 字**<br>（API 等值 **~$0.06**） | **~1,030 字**<br>（不含 Pre-1 試聽） | **1.8%**（Starter 40,000 字/月；含 Pre-1 試聽 <10%） |
| **主動工程牆鐘時間** *(不含 Creator 異步等待)* | • Pre-1 補齊新資產（不含聲線試聽等待）：~2.5–3.5 hr<br>• Stage 0.5＋1（QC-0）＋1.5（TTS）：~1.0–1.5 hr<br>• Stage 2＋3（`nano2` 首幀＋QC-1 總表）：~1.5–2.0 hr<br>• Stage 3.5（LTX 預演＋QC-1.5）：~0.5 hr<br>• Stage 4（Flow 24 takes ~32m ∥ Colab H3+L3 ~90m 並行）：~2.0–2.5 hr<br>• Stage 5（AMD-05 6 鏡＋QC-2）＋6A/6B/7/8：~1.5–2.0 hr | **~6.5–8.5 hr** *(Stage 0.5–8)*<br>＋ ~3 hr Pre-1 | **~11–13 hr** | **Creator 主動審片估 45–60 分鐘**（分散於 5 個短檢核點） |

---

## 5. 閘門檢查點與 Creator 決策節點地圖

```text
[Gate A3：劇本 v0.3.2 終判] ──▶ [Gate Pre-1：SYS-01 定妝＋聲線＋常駐場景鎖定]
        │
        ▼
[Stage 0.5 導演闡述審閱] ──▶ [QC-0 preflight_gate.py (0 FAIL)] ──▶ [Stage 1.5 TTS 驗音]
        │
        ▼
[QC-1 首幀跨鏡比對門]（Creator 審新場／英雄鏡；diff_sheet_gen --anchors-dir --verify PASS）
        │
        ▼
[QC-1.5 預演節奏門]（Creator 3 分鐘審全集節奏與 lip_sensitive 清單；不驗口型）
        │
        ▼
[Stage 4 雙引擎並行抽卡] ──▶ [Stage 5 AMD-05 合成＋QC-2 成片抽幀驗收門]（Creator 挑片拍板）
        │
        ▼
[Stage 6A 粗剪] ──▶ [QC-D 導演檢核門]（Creator 審六維；寫入 playbook.md）
        │
        ▼
[Stage 6B 精修＋事實角標] ──▶ [Stage 7 社群包] ──▶ [QC-3 終審簽核] ──▶【Creator 手動發布】
```

---

## 6. Open Questions for Creator（僅限真正決策，共 5 題）

1. **`S04` V2 對白超速與原子拆鏡取捨**：依 Spec v2.3 V2 精算，`S04`（24 純字／2 換人／1.5s 反應拍）在 `6.5s` 單鏡下達 `5.58 純字/秒`（超標），建議改為 `S04a`（3.0s）＋`S04b`（3.8s）＋`S04c`（1.8s 反應拍），全片微增 ~2 秒至 ~100.5 秒（或由 `S03`/`S14` 微修 1.5 秒守 98.5s）——**同意不改劇本台詞、採三原子鏡拆法並以 Stage 1.5 TTS 實測秒數定長嗎？**
2. **Stage 3.5 預演形式（LTX GPU 預演 vs 0 GPU 靜態首幀＋TTS 板）**：EP-01 採標準常線跑 LTX 低清動態預演（多耗 ~0.6 CU＋30 分鐘），或因首集已有多鏡重度依賴對白與圖卡、改以「核准首幀＋正式 TTS」0 GPU 靜態動態板完成 QC-1.5？
3. **`S01`（太湖冷開場）與 `S13`（越國慶功）是否啟用 L3 白膜預演**：建議 **`S01` 跑 1 顆 L3 白膜**（由 `cozyclay.org/#try` 或 Python 3D 灰模產 4s 慢推弧線，驗收 L3 正式上線；`S13` 留走 L1 Flow Omni 控工時）——**確認 `S01` 上 L3（1 鏡）、還是 EP-01 全片先走 L1＋L4？**
4. **`S19`（SYS-01 首次遲疑 0.5 秒）製作路線**：選 **Route A**（Flow Omni 對乾淨定妝人像跑 3s 微表情變化，再包進 `sys01_composite.py` 疊掃描線與「蠡」字閃現，最生動、耗 ~12–18 點）還是 **Route B**（純 CPU 雙定妝圖「微笑→遲疑」0.5s 精準微變＋故障閃爍，0 點且 100% 可控）？
5. **`FANLI-OUTFIT-03` 正面傷痕偏淡與兩位春秋客串聲線（勾踐／文種）**：`S13` 中景屬 `OPT`，可不重修 `OUTFIT-03` 直接開拍（或花 2 分鐘 0 點補 1 張修正圖）；勾踐／文種各僅 1 句畫外／背影，**同意以 ElevenLabs 聲音庫篩 2 組台灣／中性成熟男聲快鎖（不走主角級多輪 Voice Design）嗎？**
