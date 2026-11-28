# MiniMax H3 官方規格對照本地部署包絡備忘錄（agy 工程對賬與決策依據）

> **文件性質**：DISCUSSION & DESIGN ONLY（2026-11-28｜**零圖片／影片生成、零 API／CU 消耗、零 repo push**）  
> **撰寫角色**：agy（`workhorse-90d`，《第二次文明》短劇產線工程端）  
> **對照基準**：Creator 提供之 [`H3-OFFICIAL-SPECS-REF.md`](file:///home/hatch/drama-line/H3-OFFICIAL-SPECS-REF.md)（官方／主流平台規格） vs 2026-11-27 實查之 Hugging Face `MiniMaxAI/MiniMax-H3` 指南（記於 [`CAMERA_WORKFLOW_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_WORKFLOW_AGY_MEMO.md) §2.1） vs 我方本地部署實態（`comfy-colab-kit` v0.6.0 `minimax-h3-video` on Colab NVIDIA L4 24GB、`TriPRISM TurboFusion w6a8` 8-step、[`live_node_schemas.json`](file:///home/hatch/drama-line/claytest/live_node_schemas.json)、[`h3_r2v_4ref_groupB.json`](file:///home/hatch/drama-line/sm7a/workflows/h3_r2v_4ref_groupB.json)、[`h3_r2v_clay.json`](file:///home/hatch/drama-line/claytest/workflows/h3_r2v_clay.json)、SM-7A／Clay Test／DEMO-02 v2 實測遙測）。  
> **誠實標註紀律**：凡取自本機實測檔與 live schema 者標為 **`[實測]`**；依數學縮放與系統架構推演者明標 **`[推論]`**；只讀來源未獨立核實或未經實機測試者明標 **`[未驗證]`**。

---

## 0. 一頁執行摘要（TL;DR）

1. **為何官方規格與我方本地邊界看起來不同？** 因為四個層級的限制常被混在一起談：**模型原生能力（Model）**、**官方平台政策（API Policy）**、**ComfyUI 節點實作（Local Node）** 與 **Colab L4 24GB 硬體現實（Our VRAM/RAM Reality）**。官方規格表上大多數上限（9 圖／3 影／3 音／15s／24fps／32kHz 立體聲／首尾幀與 Ref2VA 互斥）與我方 2026-11-27 實查的 HF 指南一致，但實際卡住我方 L4 產線的不是模型能力，而是 **32.8 GB 總權重在 22.03 GiB L4 上已全面啟用動態 CPU Offload（VRAM 貼頂 20.73–20.76 GiB、Clay Test 系統 RAM 僅餘 2.64 / 52.96 GiB）**。
2. **三個最關鍵的新發現（工程稽核實獲）**：
   - **隱藏陷阱 #1（EP-01 短鏡跌破 H3 4 秒官方下限）**：官方規格下限為 **4 秒**，ComfyUI `MiniMaxH3ReferenceToVideo` 節點註解亦明言 **`trained range is ~124-362`（~5.17–15.08s）**，我方本地最低實測驗證僅至 `4.0s` 參數（`107f = 4.46s`，`DEMO02_v2 S3a`）。但 [`EP01_PRODUCTION_WORKFLOW.md`](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md) 將 `S04c`（生成 `2.8s` → `73f`）與 `S11c`（生成 `3.0s` → `73f`）直接路由給 H3-4Ref——本地節點雖不報錯，卻落在未驗證的訓練分佈外（且若切官方 API 會直接拒收）。建議凡 H3 鏡一律**最小生成 `4.0s`（`107f`）再於粗剪裁切**。
   - **隱藏陷阱 #2（17-frame 時間網格進位跳級）**：我方工作流節點 `131` 以公式 `5 + 17k` 向上對齊幀數。`EP-01 S07` 排生成 `6.2s` 原以為守在 `6.5s` 硬頂內，實際進位為 **`158f = 6.583s`**（跨入我方 L4 **尚未實測**的下一時間塊；目前最高已測僅 `S3b` 之 `141f = 5.875s`，`a ≤ 5.8s`）。
   - **隱藏漏洞 #3（`preflight_gate.py` 漏檢首尾幀與 Ref2VA 互斥）**：官方與 ComfyUI 節點層（`MiniMaxH3ImageToVideo` vs `MiniMaxH3ReferenceToVideo`）100% 禁止混用 `i2v_first_last` 與 `ref2v`；我方現行已執行工作流（含 L3 白膜）**皆未誤混**，但 Spec §四漏寫 H3 互斥聲明，且 [`tools/preflight_gate.py`](file:///home/hatch/drama-line/tools/preflight_gate.py) **完全未驗證 `last_frame` 與 `gen_mode=ref2v`／`L2_flf` 衝突**，須於 v2.4 補上機械硬閘。
3. **既有決策審計結論**：
   - **AMD-05 v3 否決雙人 H3（范蠡＋`SYS-01`）**：**依然成立**，且不單是 L4 VRAM 因素——即使切到 9 槽 A100 或官方 API，「實心棚拍人像卡 vs 半透明全息」的材質互斥與體積光動感劣勢依然存在（僅需在文字上將「4 槽上限」明確限定為 L4 `max` 包絡，並區分未來「兩名實心真人」雙人戲的適用性）。
   - **Spec V1 H3 `≤5.5s` 建議／`≤6.5s` 硬頂**：確認為**品質漂移＋豎屏短劇節奏＋L4 穩定度家規**，非 H3 的 15s 模型上限。低動態峰值對白 `6–8s` 值得跑一次低成本 **SM-9A 冒煙（~0.5 CU）** 驗證實測邊界，但不建議全面放寬短劇預設 ASL。

---

## 1. 逐條規格對照表（官方規格表 vs 11-27 HF 指南 vs 我方本地部署）

> **層級代碼**：`Model`＝模型架構與訓練能力、`API`＝官方／託管平台服務策略、`Node`＝本機 ComfyUI `comfy_extras.nodes_minimax_h3` 節點實作（[`live_node_schemas.json`](file:///home/hatch/drama-line/claytest/live_node_schemas.json)）、`L4-VRAM`＝我方 Colab L4 24GB（`22.034 GiB` VRAM / `52.96 GiB` RAM，`TriPRISM w6a8` 8-step）實測物理包絡。

| # | 官方規格項目（[`H3-OFFICIAL-SPECS-REF.md`](file:///home/hatch/drama-line/H3-OFFICIAL-SPECS-REF.md)） | 與 2026-11-27 實查 HF 指南一致？ | 對我方 LOCAL 部署約束程度 | 限制所在層級 | 本地 ComfyUI 實況與實測數據（含差異說明） |
| :-: | :--- | :---: | :---: | :--- | :--- |
| **1** | **影片時長**：標準 **4–15 秒（整數秒）**；多數平台 **5–15 秒**；單次上限 **15 秒**（更長須尾幀或參考延續） | **一致** `[實測]`<br>（11-27 確認 4–15s 整數秒、對齊 17 幀網格） | **部分約束** | **整數秒**：`API`<br>**~5–15s 訓練窗**：`Model`<br>**`5+17k` 幀格**：`Node`<br>**≤5.0–6.5s 穩態**：`L4-VRAM`＋品質 | `MiniMaxH3ReferenceToVideo.length`：`min=5, max=3600, step=17`，tooltip 明註 **`trained range is ~124-362`（5.17–15.08s）** `[實測]`。本地節點**不限制整數秒亦不硬擋 15s**，但工作流節點 `131` 強制向上對齊 `5+17k`（如 `4.0s→107f=4.46s`、`5.0s→124f=5.17s`、`5.5s→141f=5.88s`、`6.2s→158f=6.58s`）。L4 已測至 `141f`（`5.88s`，0 OOM）；`>15s`（`>362f`）屬訓練外推易崩壞。 |
| **2** | **參考圖片**：最多 **9 張**；單張 **≤30 MB**；邊長 **256–5760px** | **數量與 30MB 一致** `[實測]`<br>（256–5760px 屬平台輸入校驗 `[未於 11-27 摘錄獨立複核]`） | **部分約束** | **≤9 張**：`Model`＋`Node`<br>**≤30MB／256–5760px**：`API`<br>**≤4 張 (`max`)**：`L4-VRAM` | 節點 `ref_images`（`COMFY_AUTOGROW_V3`）硬鎖 **`min: 0, max: 9`**（`ref_image_0..8`）`[實測]`；`LoadImage` 不受 30MB 或 5760px API 校驗限制。節點內建縮放：`ref_image_size="max"` 僅在短邊 `>2048px` 時下縮（永不放大），`"match"` 下縮至生成面積。我方 4 張 `768×1376`（合計 `4.23 MP`）於 `max` 在 L4 已貼頂 `20.74–20.76 GiB`；L3 白膜硬鎖 `≤3` 張 (`match`)。 |
| **3** | **參考影片**：最多 **3 段**；每段 **2–15 秒**；**總時長 ≤15 秒** | **一致** `[實測]`<br>（11-27 確認 ≤3 段、單段 2–15s、總長 ≤15s、API ≤50MB） | **部分約束** | **≤3 段／2–15s**：`Model`＋`Node`<br>**≤50MB／容器**：`API`<br>**≤1 段・≤5s・≤0.35MP**：`L4-VRAM` | 節點 `ref_videos` 硬鎖 **`min: 0, max: 3`**（tooltip：`Reference video frames at 24 fps (2-15s)`），配對 `ref_video_audios` 亦為 `max: 3` `[實測]`。本地以 `LoadVideo → GetVideoComponents` 解碼為 `IMAGE` 張量送入，無 50MB API 上限；但單支 `0.35 MP × 120f (5.0s)` 白膜已把 L4 推至 **`20.727 GiB` VRAM＋僅餘 `2.64 GiB` RAM（95% 滿載）** `[實測]`，故 L4 實務遠緊於 3 段／15s。 |
| **4** | **參考音訊**：最多 **3 段**；每段 **2–15 秒**；總長 **≤15 秒**；**不能單獨使用**（必搭 ≥1 圖或 ≥1 影） | **數量與秒數一致** `[實測]`<br>（不可單獨使用符合 Ref2VA 視覺定位邏輯 `[未單獨實機測試]`） | **部分約束（現未啟用）** | **≤3 段**：`Model`＋`Node`<br>**≤15MB／單獨拒收**：`API`<br>**不用原聲對白**：我方產線政策 | 節點 `ref_audios` 硬鎖 **`min: 0, max: 3`**（獨立於 `ref_video_audios`）`[實測]`。我方工作流已載入 `minimax_h3_audio_vae_fp32.safetensors` 並接入 `audio_vae`，技術上本地可接 `ref_audio_0`，但因全劇強制 **ElevenLabs `eleven_v4` TTS（ADR-006，MiniMax 台灣讀音 0/4 淘汰）**，目前全部留空未使用。 |
| **5** | **總檔案數**：最多 **12 個** | **一致** `[實測]`<br>（11-27 確認混合總檔數 ≤12） | **L4 上實際不觸發（VRAM 先卡死）** | **≤12 總和**：`API`（＋模型注意力預算；Python 節點內部是否硬擋 `sum>12` `[未查 Colab 源碼]`） | ComfyUI 節點各槽上限相加為 `9+3+3=15`（不含配對的 3 條 `ref_video_audios`）`[實測]`。但在 L4 上我們早在 **4 個檔**（4 圖 `max` 或 3 圖＋1 影 `match`）就觸及 VRAM/RAM 邊界，遠低於 12；僅在 A100/G4 或官方 API 才會接近 12 檔上限。 |
| **6** | **首尾幀模式（FL2VA）與參考模式（Ref2VA）不能混用** | **一致** `[實測]`<br>（11-27 確認 Base 三段式＋Part One 對齊行 vs Ref2VA 六段式為完全分離管線） | **100% 硬約束** | **`Model`＋`Node`（架構級互斥）**＋`API` | **雙層鐵律**：ComfyUI 明確拆為兩顆互斥節點——[`MiniMaxH3ImageToVideo`](file:///home/hatch/drama-line/claytest/live_node_schemas.json#L669)（具 `first_frame`/`last_frame`，**無**任何 `ref_*` 孔）vs [`MiniMaxH3ReferenceToVideo`](file:///home/hatch/drama-line/claytest/live_node_schemas.json#L2-L150)（具 `ref_images`/`ref_videos`/`ref_audios`，**無** `first_frame`/`last_frame` 孔）`[實測]`。*註：我方把 QC-1 首幀放進 `<Picture 1>` (`ref_image_0`) 屬於純 Ref2VA 軟參考，不是 FL2VA 混用。* |
| **7** | **解析度**：**768P** 或 **原生 2K**（部分平台有 480P） | **768P 一致** `[實測]`<br>（11-27 確認預設短邊 768px；原生 2K 屬官方託管／高階管線） | **API 預設檔位不適用；2K 無法於 L4 單段直出** | **768P 訓練甜區**：`Model`<br>**480P/768P/2K 檔位**：`API`<br>**32 倍數任意寬高**：`Node`<br>**`544×960`（0.5MP）**：`L4-VRAM` | 節點 `width`/`height` 接受 `32–16384`（`step=32`，預設 `1344×768` = `1.03 MP`）`[實測]`。本機已載入 `MiniMaxH3LatentUpscaleWithModel` 節點名但**未掛載於 L4 工作流**。`comfy-colab-kit` 在 L4 自動降配 `0.4–0.5 MP`（`544×960`）防 OOM（`0.8 MP` 留給 A100/G4）；我方採 **`544×960` 生成＋`ffmpeg` Lanczos 升頻 `720×1280`／`1080×1920`** `[實測]`。 |
| **8** | **幀率**：**24 fps** | **一致** `[實測]` | **100% 硬約束** | **`Model`＋`Node`** | 節點 `length` 固定以 24 fps 換算，工作流 `CreateVideo.fps=24`；本機 `ffprobe` 實測全 5 支 H3 輸出片（`groupB`/`S3a`/`S3b_t2`/`S4`/`h3_out`）皆為 **`24/1 fps`** `[實測]`。 |
| **9** | **畫幅比例**：21:9、16:9、4:3、1:1、3:4、9:16、**adaptive** | **標準比例一致** `[實測]`（含 9:16） | **API 選單與 `adaptive` 不適用** | **枚舉＋`adaptive`**：`API`<br>**顯式像素寬高**：`Node` | 本地 `MiniMaxH3ReferenceToVideo` 無 `adaptive` 自動推斷，改由上游 `ResolutionSelector` 顯式輸出 `9:16` 32 倍數寬高（`544×960`）`[實測]`。我方全線鎖死 9:16，無影響。 |
| **10** | **音訊**：**原生立體聲（32kHz）**，同步生成對白、音效、環境音 | **一致** `[實測]` | **100% 硬約束（於生成層）** | **`Model`＋`Node`**（組裝層由我方覆寫） | 本機 `ffprobe` 實測全 5 支本地 H3 成片音軌皆為 **`32000Hz 2ch AAC`** `[實測]`；`SM-7A` 亦證實原生對白可清晰說出 `<d>[Chinese]` 台詞且 `non_diegetic_music: N/A` 有效。但我方組裝層依 ADR-006 **刻意丟棄原生對白音軌**，改掛 48kHz ElevenLabs TTS＋CC0 roomtone。 |
| **11** | **提示詞長度**：最多約 **7000 字元** | `[未於 11-27 指南摘錄中獨立核對精確字元上限]` | **不硬約束（API 欄位上限）** | **~7000 字元硬截斷**：`API`<br>**Qwen3-VL token 上下文**：`Model`＋`Node` | 本地使用 `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`，`PrimitiveStringMultiline` 無 7000 字元硬攔截 `[實測]`。我方實跑六段式提示詞約 `2,500–3,200` 字元，遠低於 7000 字元，無論本地或 API 皆不構成瓶頸。 |
| **12** | **支援語言對白**：**11 種穩定語言**（中、英、日、韓、法、德、西等） | **與官方 `<d>[Chinese]` 標籤一致**（11 語種總數屬官方發布規格 `[未於 11-27 逐語種核列]`） | **適用（模型能力）** | **`Model`** | 開源權重繼承多語對白與中文唇形驅動能力（`SM-7A` 與 `DEMO02_v2 S4` 實測中文口型評分 `4.5/5.0` `[實測]`）。*注意：「支援中文」不等於「台灣腔讀音零錯字」，最終成片配音仍仰賴 ElevenLabs `eleven_v4`。* |
| **13** | **支援生成模式**：T2V / 首幀 I2V / 首尾幀 FL2V / 多模態 Ref2VA | **一致** `[實測]` | **部分驗證（僅 Ref2VA 已實測）** | **四模式節點**：`Model`＋`Node`<br>**`TriPRISM` 8-step 映射**：`comfy-colab-kit` profile | 本地已具 `EmptyMiniMaxH3LatentAV`、`MiniMaxH3ImageToVideo`、`MiniMaxH3ReferenceToVideo` 全套節點 `[實測]`。但閘道預設將 `ref2va` 與 `fl2va` 一併 alias 至社群合併蒸餾權重 **`TriPRISM w6a8`（8-step）**；目前**僅 Ref2VA 通過 SM-7A／Clay Test**，**FL2V（`last_frame`）在 8-step 下仍屬未驗證（SM-4 待辦）**。 |

---

## 2. 本地 Colab L4 包絡餘裕分析（實測 vs 推論 ＋ 選跑 SM-9 設計）

### 2.1 已實測遙測基準（為何「20.74 GiB 平頂」具有欺騙性）

彙整 `sm7a`、`claytest` 與 `demo02_v2` 全部 **6 筆本地 Colab L4 實機數據**（NVIDIA L4：`22.034 GiB` 可用 VRAM、`52.96 GiB` System RAM、`high_mem: true`、`1.71 CU/h`；總權重 `~32.8 GB`；`544×960` `0.522 MP`；8 steps `euler`/`simple`）：

| 實測案例 | 參考配置（實測解析度與總像素） | `ref_image_size` | 參數秒數 → 實際幀數（實長） | 實測耗時（快取狀態） | 峰值 VRAM / 最小剩餘 VRAM | 最小剩餘 System RAM | 結果 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SM-7A Group A** | 1 圖（`768×1376` = `1.06 MP`） | `max` | `5.0s` → `124f`（`5.17s`） | `201.0s`（含冷載） | `~20.18 GiB`（後測） | 未採樣 | **PASS（0 OOM）** |
| **SM-7A Group B** | 4 圖（`3×1.06 + 0.61` = `3.79 MP`） | `max` | `5.0s` → `124f`（`5.17s`） | **`279.9s`**（已快取） | `~20.18 GiB`（後測） | 未採樣 | **PASS（0 OOM）** |
| **DEMO02_v2 S3a** | 4 圖（`4×768×1376` = `4.23 MP`） | `max` | `4.0s` → `107f`（`4.46s`） | `262.2s`（含冷載） | **`20.738 GiB`** / `1.30 GiB` | 未採樣 | **PASS（0 OOM）** |
| **DEMO02_v2 S4** | 4 圖（`4×768×1376` = `4.23 MP`） | `max` | `5.0s` → `124f`（`5.17s`） | `~280–286s`（已快取） | **`20.739 GiB`** / `1.30 GiB` | 未採樣 | **PASS（0 OOM）** |
| **DEMO02_v2 S3b T1/T2** | 4 圖（`4×768×1376` = `4.23 MP`） | `max` | `5.5s` → `141f`（`5.88s`） | **`325.3 / 329.6s`**（已快取） | **`20.762 / 20.754 GiB`** / `1.27 GiB` | 未採樣 | **PASS（0 OOM）** |
| **Clay Test Run 1** | 3 圖（`1.57 MP`）＋1 影（`0.35 MP × 120f`） | `match` | `5.0s` → `124f`（`5.17s`） | **`430.5s`**（含冷載） | **`20.727 GiB`** / `1.307 GiB`（貼平 304s） | **`2.64 GiB`**（`95.0%` 滿載！） | **PASS（緊繃）** |

**關鍵系統診斷（為什麼不能把「只差 0.03 GiB」誤判成「還有很多餘裕」）**：
1. **ComfyUI 已在全面動態 Offload**：H3 整套權重共 `~32.8 GB`，遠大於 L4 的 `22.034 GiB`。[`telemetry_run1_r2v.json`](file:///home/hatch/drama-line/claytest/telemetry_run1_r2v.json) 顯示 VRAM 在 `t=94s–398s` 整個採樣期**死死貼平在 `20.727 GiB`**（留 `~1.30 GiB` 給 PyTorch 啟用值），多出來的權重已卸載在 System RAM 中逐層流式換入。因此 `107f`（`20.738 GiB`）→ `141f`（`20.762 GiB`）幾乎不變，**不是**因為加幀不吃顯存，而是顯存預算早已貼頂！
2. **本地 L4 真正會觸發崩潰的三道陡崖（Sharp Cliffs）**：
   - **陡崖 ① — System RAM OOM-Killer（`SIGKILL`）**：Clay Test 跑 `124f`＋`0.35 MP` 參考片時，系統 RAM 已用到 `50.32 / 52.96 GiB`（僅餘 **`2.64 GiB`** `[實測]`）。再加大參考幀數或解碼快取極易直接被 Linux OOM-Killer 殺掉 worker。
   - **陡崖 ② — 未分塊 3D Video VAE 解碼峰值（CUDA OOM）**：Clay Test 實測 `VAEDecode` 單獨吃掉 **`19.45 GiB`**（於 `544×960 × 124f`）`[實測]`；我方現行工作流用的是未分塊 `VAEDecode`（Node 122），其顯存峰值隨 `width × height × frames` 線性放大。
   - **陡崖 ③ — DiT 3D 全注意力二次擴張（時間與啟用值雙殺）**：實測從 `124f` 增至 `141f`（幀數 `+13.7%`），快取耗時由 `280s` 跳至 `325–330s`（`+45–50s` = **`+16–18%`** `[實測]`），且 `SM-7A` 實測加 3 張 `max` 參考圖多耗 **`~+110s`** `[實測]`——符合 3D 注意力 $O((N_{\text{gen}} + N_{\text{ref}})^2)$ 的超線性特徵。

### 2.2 三項餘裕問題逐一剖析（實測基礎＋誠實推論）

| 探索維度 | 情境 | 參考／生成量級變化 | 預估耗時／CU（單抽，快取） | VRAM / RAM / OOM 風險 | 畫質與工程判斷 |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **① 參考圖 `> 4` 張** | **5–6 張 @ `ref_image_size="max"`**<br>（假設每張皆 `768×1376` `1.06 MP`，`544×960`, `124f`） | 總參考像素 `5.3–6.4 MP`（較 4 槽 `+25–50%`） | `[推論]` **`~340–410s`**<br>（`5.7–6.8 min`, `~0.16–0.20 CU`） | **中風險**（`Qwen3-VL` 視覺 token 與 DiT 啟用值墊高，迫使更多 DiT 層 offload 進 RAM；若輸入圖達 `2048px` 短邊則單張即等於 4–6 張我方圖，**必爆 OOM**） | **邊際收益低於風險**：單角色 4 槽已達 `0/5` 錯邊疤；僅對雙實心真人鏡有意義，且須先以 SM-9B 驗證 RAM 剩餘量。 |
| **① 參考圖 `> 4` 張** | **6–8 張 @ `ref_image_size="match"`**<br>（`544×960` `0.522 MP`, `124f`） | 總參考像素 `3.1–4.2 MP`（**竟然 ≤ 現行 4 槽 `max` 的 `4.23 MP`！**） | `[推論]` **`~245–300s`**<br>（`4.1–5.0 min`, `~0.12–0.14 CU`） | **低–中風險**（DiT 視覺 token 總數不超過已實證的 4 槽 `max`；僅多出少量 Qwen3-VL／RAM 預編碼負擔） | **畫質代價已實測暴露**：Clay Test (`match`) 實測顯示 `0.5 MP` 參考會讓范蠡肌理減齡（~33–37 歲）並在 `t=3.5s` 短暫閃出 `左衽` 翻領 `[實測]`。故**用 `match` 換槽數會犧牲我方上 H3 的核心目的（微特徵保真）**。 |
| **② 短邊拉至 `768`**<br>（`768×1344`, `1.03 MP`） | **4 張圖（`max` 或 `match` 等價，因 `1.03≈1.06 MP`）**, `124f` | 生成潛空間 token **`1.98×`**；生成自注意力約 **`~3.9×`**；VAE 解碼張量 **`~2×`** | `[推論]` **`~600–850s`**<br>（**`10–14 min`**, `~0.30–0.40 CU`，超 SM-7 `≤10 min` 紅線） | **極高 OOM 風險**（未分塊 `VAEDecode` 在 `544×960` 已吃 `19.45 GiB`，面積翻倍極易於採樣或 VAE 解碼直接 CUDA OOM；這正是 `comfy-colab-kit` 在 L4 自動降 `0.4–0.5 MP` 的原因） | **L4 上不划算**：即使改用 `VAEDecodeTiled` 並砍到 2–3 圖勉強不 OOM，單鏡耗時與重抽成本也暴增 `2.5–3×`，且失去 4 槽防錯邊疤護城河。**`768×1344` 應歸屬 A100/G4，L4 維持 `544×960`＋Lanczos 升頻**。 |
| **③ 時長 `> ~6s`**<br>（4 圖 `max`, `544×960`） | **`6.0–6.5s` → `158f (6.58s)`** | 較 `S3b` (`141f`) 多 1 時間塊（`+12%` 幀） | `[推論]` **`~375–395s`**<br>（`6.3–6.6 min`, `~0.18–0.19 CU`） | **低–中 OOM 風險**（最可能於 L4 穩定過關） | **最務實的邊界**：EP-01 `S07`（`6.2s`）實際就會落在此格，建議確認。 |
| **③ 時長 `> ~6s`**<br>（4 圖 `max`, `544×960`） | **`7.0–8.0s` → `175f–192f (7.29–8.00s)`** | 較 `S3b` (`141f`) 多 2–3 時間塊（`+24–36%` 幀）；VAE 解碼 `1.41–1.55×` | `[推論]` **`~440–540s`**<br>（`7.3–9.0 min`, `~0.21–0.26 CU`） | **中–高 OOM 風險**（未分塊 `VAEDecode` 逼近 22 GiB 紅線；若換 `VAEDecodeTiled` 應可解硬體瓶頸，但**晚幀漂移風險**高於硬體風險） | **值得 SM-9A 低成本實測**：若低動態峰值對白 `7.3–8.0s` 不 OOM 且無晚幀漂移，可解鎖「單鏡長對白＋後製切入反應插鏡 L-cut」母帶拍法。 |
| **③ 時長 `> ~6s`**<br>（4 圖 `max`, `544×960`） | **`10–15s` → `243f–362f`** | 較 `124f` 多 `2–3×` 幀；DiT 注意力 `4–9×` | `[推論]` **`~15–30+ min`** | **極高 OOM 風險（VRAM＋RAM 雙爆）** | **明確不適用 L4**，且違背豎屏短劇節奏與長鏡漂移規律；僅屬 A100/G4 或官方 API 範疇。 |
| **③ 時長 `> ~6s`**<br>（**L3 白膜 `ref_video_0`**） | **`> 5.0s`（如 `141f / 5.88s`）** | 同時拉長參考影與生成影雙序列 | `[推論]` **`> 9–11 min`** | **極高 RAM OOM 風險**（`5.17s` 已僅剩 **`2.64 GiB` RAM** `[實測]`） | **維持 Clay Test Condition 3 硬鎖 `≤ 5.0s`**，絕不於 L4 上探。 |

### 2.3 選跑冒煙設計：**SM-9（L4 本地 H3 包絡探測 — 僅設計、不執行）**

若 Creator 希望用實測數據取代上述 `[推論]`，可於**單次 Colab L4 Session（僅付 1 次冷啟動）**執行分階段 **SM-9**，總預算 **`≤ 1.3 CU`**（佔月配額 200 CU `< 0.7%`，0 Flow 點，0 TTS 字）：

- **SM-9A（最高 ROI｜低動態對白時長探測，~0.50–0.55 CU，~16–18 min 含冷啟動）**：
  - **標的**：沿用已過 QC-1 的乾淨 `DEMO02_v2/frames/S4_first.jpg` ＋ `OUTFIT-02` 三視角（`h3_r2v_4ref_groupB.json`，4 槽 `max`、`544×960`、8-step、固定種子、`static` 或極緩 `slow push-in`），搭配一段 ~26–30 字克制雙子句中文台詞。
  - **測點**：① 測 **`dur_param = 7.0`（`175f / 7.29s`）**；若 `0 OOM`、耗時 `< 9 min` 且 `min_ram_free > 3.5 GiB`，再順測 ② **`dur_param = 8.0`（`192f / 8.00s`）**（若 `VAEDecode` 階段報 OOM，記錄為硬頂，不強試）。
  - **觀測指標**：每 10s 採樣 `/system_stats`（同 Clay Test 腳本，記錄 `peak_vram` 與 `min_ram_free`）、總耗時、以及 **7 幀 QC-2 抽檢**（`0.5 / 1.5 / 2.5 / 3.5 / 4.5 / 5.5 / 6.5–7.5s`）：臉齡、左眉疤／右眉潔淨度、`OUTFIT-02` 四點、晚幀光線漂移、雙子句口型同步度。
- **SM-9B（選跑｜6 槽參考圖餘裕與 `match` vs `max` 對照，僅追加 ~0.35–0.45 CU，~12–15 min 快取熱跑）**：
  - **觸發條件**：僅當 Creator 預期未來 EP 會有「雙實心真人 H3 同框」或「多道具 5–6 槽」需求時加測。
  - **測點**：同 session 內以 `124f (5.17s)`、`544×960` 跑 ① **6 圖 `ref_image_size="match"`** vs ② **6 圖 `ref_image_size="max"`**（全部 `768×1376`）。記錄 OOM、`min_ram_free`、相較 4 槽（`280s`）耗時增幅，及 `match` 於 CU 尺幅是否仍出現 Clay Test 的肌理軟化或翻領漂移。
- **為何 SM-9 不測 `768×1344` on L4**：依計算量已可預見 `10–14 min/take` 且未分塊 `VAEDecode` 極高機率 OOM，單位投資報酬率低於現行已過 QC-D 的 `544×960`＋Lanczos 升頻。若未來想比較原生 `768P` 畫質，應另開 **A100 單鏡 A/B**，而非硬壓 L4。

---

## 3. 既有決策影響稽核（含文件精準修訂清單）

### (a) AMD-05 v3 否決雙人 H3 Ref2VA（[`AMD05_V3_AGY_MEMO.md`](file:///home/hatch/drama-line/AMD05_V3_AGY_MEMO.md) §1.1–1.2）

- **在本地路線下是否依然成立？** **100% 依然成立。**
- **其論述是否正確限定在本地路線範疇？** **大致正確，但須補一條關鍵邊界釐清**：
  - [`AMD05_V3_AGY_MEMO.md`](file:///home/hatch/drama-line/AMD05_V3_AGY_MEMO.md#L57-L63) §1.2 標題與第 1 點已明確寫明「**在 Colab L4 上**……跑 4 槽 `max` 已吃掉 `20.18–20.75 GiB`」，並正確援引 `preflight_gate.py` L1166（L4 逾 4 槽發 `WARN`，而非模型硬上限）。
  - **關鍵拆層（必須補寫進文件）**：AMD-05 v3 否決雙人 H3 其實有**兩層彼此獨立的理由**——
    1. **本地 L4 硬體層（僅綁 L4）**：4 槽 `max` VRAM/時間已近天花板，無法同時容納范蠡 3 視角＋`SYS-01` 2–3 視角＋首幀（6–7 槽 `max`）。
    2. **模型本質與美學層（即使上 A100 或官方 API 9 槽仍成立！）**：§1.2 第 3 點的 **「實心棚拍女像卡 vs 半透明全息首幀」注意力互斥**（易把 `SYS-01` 拉回實心肉身或把掃描線串染到范蠡），加上 Flow Omni `i2v_first` 具備 **0 點 `nano2`＋QC-1 2.5× 像素鎖定 Frame 0** 與**更自然的體積光塵／掃描線流動**，以及 `S04b` 讓 `SYS-01` 退為畫外聲本身就是更強的戲劇調度。
  - **對未來集數的重要區分**：若是「**范蠡＋全息 `SYS-01`**」，即使有 9 槽也仍由 Flow Omni 勝出；但若未來出現「**兩名實心真人對白同框**（如范蠡＋勾踐／文種）」，則 L4 4 槽限制屬於**硬體包絡而非 H3 模型限制**——切 A100、走 `match`（待 SM-9B 驗證）或走官方 API 即可解鎖 6–9 槽。

### (b) Spec V1 H3 `≤5.5s` 建議／`≤6.5s` 硬頂 vs 官方 15s 上限

- **定性確認**：[`STORYBOARD-SPEC-V2.md`](file:///home/hatch/drama-line/STORYBOARD-SPEC-V2.md#L236) §6.1 V1 與 [`V23_AMENDMENT_AGY_MEMO.md`](file:///home/hatch/drama-line/V23_AMENDMENT_AGY_MEMO.md#L722-L738) 所訂之 H3 `≤5.5s` 建議（淨 `≤4.5s`）／`≤6.5s` 硬頂（淨 `≤5.5s`），**100% 是「畫質抗漂移＋豎屏短劇節奏＋L4 硬體穩態」的產線規則，絕非 H3 模型 15 秒（362 幀）規格上限**。
  - 三層成因必須分開寫明：① **品質漂移規則**（SM-7A Group A 於 `3.5–4.5s` 現晚幀暖光幻覺；`DEMO02_v2 S3b` T1 於 `4.11s` 現唇部皺縮與畫面推擠）；② **豎屏短劇剪輯節奏**（[`CAMERA_COVERAGE_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_COVERAGE_AGY_MEMO.md#L17-L22) 鎖定 `ASL 1.8–2.6s`、`dead_air ≤3.5s`）；③ **L4 實測包絡**（`141f = 5.88s` 已需 `5.5 min`；L3 白膜 `5.17s` 已僅餘 `2.64 GiB` RAM，屬真實 L4 硬體紅線）。
- **低動態對白 `6–8s` 是否值得測試？** **值得，但僅作為「受控特例」而非鬆綁日常節奏。**
  - *值得測的原因*：在少數靜態／極緩推峰值獨白鏡（如 `S17b`/`S18b` 級別），若 L4 能穩定產出 `7.3–8.0s` 零漂移母鏡，剪輯端即可在不中斷 H3 連續口型與微表情呼吸的前提下，中段插切 `1.2–1.5s` 細節 `ECU` 或聽者反應鏡走 **L-cut**，省去拆兩顆 H3 鏡之間的接點落差。以 **SM-9A（~0.5 CU）** 一次性定生死非常划算。
  - *不可全面鬆綁的原因*：即使 SM-9A 過關，豎屏短劇常態對白仍應鎖死 `2.5–4.8s` 淨長（`CAMERA_COVERAGE_AGY_MEMO.md` 表 B），`6–8s` 僅限標記 `emotional_peak` 或「L-cut 主對白母片」的單集 0–1 顆例外。

### (c) 首尾幀（FL2VA）與參考模式（Ref2VA）互斥稽核

1. **對 [`STORYBOARD-SPEC-V2.md`](file:///home/hatch/drama-line/STORYBOARD-SPEC-V2.md#L205-L215) §四 `gen_mode` 表之稽核**：
   - 表中 `flow × ref2v` 欄位明寫了「`R2V 禁與 i2v 混用`」，但 **`h3 × i2v_first_last` 與 `h3 × ref2v` 兩欄漏寫 H3 官方與節點層的 100% 互斥限制**！
   - 更嚴重的工具缺口：實查 [`tools/preflight_gate.py`](file:///home/hatch/drama-line/tools/preflight_gate.py) 全檔，**完全沒有檢查 `last_frame` 欄位或 `L2_flf` 與 `ref2v` 的互斥關係**！若有人在 `script_pack.json` 把一顆 H3 鏡同時填上 `gen_mode="ref2v"`（附 4 張參考圖）與 `last_frame`（或 `control_method="L2_flf"`），`preflight_gate.py` 會直接放行 `PASS`，直到下游送進 `MiniMaxH3ReferenceToVideo` 時才發現根本沒有 `last_frame` 接口。
   - **架構連動提醒**：因 AMD-01 `ROUTING_LOCK` 強制 `lip_sensitive=true` 或 `face_lock_level=strict` 之 `CU/MCU` 走 `gen_mode="ref2v"`，這意味著 **H3 單鏡不可能同時具備「L2 首尾幀鎖定（`i2v_first_last`）」與「多圖保臉（`ref2v`）」**——兩者天生互斥；若某無對白鏡（如 `S19`）必須首尾鎖定，應走 Flow `i2v_first_last`（待 SM-5）或拆雙鏡。
2. **對 L3 白膜路線之稽核（[`h3_r2v_clay.json`](file:///home/hatch/drama-line/claytest/workflows/h3_r2v_clay.json)、Spec §A.5、[`CAMERA_WORKFLOW_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_WORKFLOW_AGY_MEMO.md)）**：
   - **現行已實跑工作流**：**100% 乾淨、零混用**。`h3_r2v_clay.json` 全程只用 `MiniMaxH3ReferenceToVideo`（`ref_image_0..2`＋`ref_video_0`），完全不碰 `MiniMaxH3ImageToVideo` 或 `last_frame`。
   - **潛在文案誤導點須封堵**：[`CAMERA_WORKFLOW_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_WORKFLOW_AGY_MEMO.md#L104) 稱讚 CozyClay 匯出「Greybox MP4＋**首尾幀 PNG**」。須於 Spec §A.5 補註一條明確禁令：**L3 `h3_r2v_clay` 中，CozyClay 首幀 PNG 僅可用於 Stage 3 輔助產出寫實圖再作為 Ref2VA `<Picture 1>`（軟參考）；尾幀 PNG 絕不可作為 H3 `last_frame` 混進 Ref2VA 工作流**（尾幀 PNG 在 L3 僅供離線 QC-2 疊圖驗收，或於放棄 `<Video 1>`＋多圖、改走純 L2 `MiniMaxH3ImageToVideo` 時單獨使用）。

### (d) 覆蓋備忘錄（Schema 2.4 草案）、EP-01 工作流與現行規格之錯誤假設清查

經逐檔比對 [`CAMERA_COVERAGE_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_COVERAGE_AGY_MEMO.md)、[`EP01_PRODUCTION_WORKFLOW.md`](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md)、[`STORYBOARD-SPEC-V2.md`](file:///home/hatch/drama-line/STORYBOARD-SPEC-V2.md)、[`DESIGN.md`](file:///home/hatch/drama-line/DESIGN.md) 與 [`tools/preflight_gate.py`](file:///home/hatch/drama-line/tools/preflight_gate.py)，抓出 **6 處確切的假設落差與須修訂文案**：

| # | 文件與精確位置 | 現有寫法／隱含假設 | 真相與風險 | 建議修訂內容（v2.4／EP-01 同步時落實） |
| :-: | :--- | :--- | :--- | :--- |
| **1** | [`EP01_PRODUCTION_WORKFLOW.md`](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md#L71) `S04c`（`1.8s` 淨→`2.8s` 生）與 [L80](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md#L80) `S11c`（`2.0s` 淨→`3.0s` 生）＋[L78](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md#L78) `S11a`（`2.6s`→`3.6s`） | 假設 H3 生成下限為 `3.0s`（註記「若生成 `<3.0s` 以 `tail_only` 或延至 `2.2s` 避短鏡 WARN」） | **重大落差**：官方 H3 標準下限為 **`4s`**，本地節點明註訓練窗 **`~124–362f`（5.17–15.08s）**，我方本地最低僅驗證過 **`4.0s`（`107f = 4.46s`，`S3a`）**。`2.8–3.0s` 會落到未驗證的 **`73f (3.04s)`**（低於訓練窗 41%），且官方 API 會直接報錯拒收！ | 訂立 **H3 生成下限保護規則**：凡路由至 H3 且 `net+trim < 4.0s` 的短反應／短對白鏡（`S04c`、`S11a`、`S11c`），`run_stage4_h3.py` 一律**自動墊高生成參數至 `4.0s`（`107f / 4.46s`）**，於 Stage 6A 精準裁取所需淨秒數（CU 耗費僅 ~0.12 CU，同 `S3a`）。 |
| **2** | [`EP01_PRODUCTION_WORKFLOW.md`](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md#L74) `S07`（`5.2s` 淨→`6.2s` 生） | 寫稱「壓至 `≤5.2s` 淨長（生成 `6.2s`）守住 L4 H3 `6.5s` 硬上限」 | **17-frame 進位盲點**：代入 `h3_r2v_4ref_groupB.json` Node `131` 公式，`a=6.2s` → `round(149)` → 向上進位為 **`158f = 6.583s`**！實質跨出已驗證的 `141f (5.88s)` 桶（上限 `a ≤ 5.8s`），也超過 `6.5s` 硬頂 `0.083s`。 | 在 `preflight_gate.py` 與 `EP-01` 排程中改以 **`5 + 17k` 實算幀長**檢核 H3 時長：`a ≤ 5.8s` 才穩落已測 `141f (5.88s)`；`S07` 要嘛壓淨長至 `≤4.8s`（或 `tail_only` 淨 `≤5.3s`），要嘛經 SM-9A 驗證 `158f`。 |
| **3** | [`CAMERA_COVERAGE_AGY_MEMO.md`](file:///home/hatch/drama-line/CAMERA_COVERAGE_AGY_MEMO.md#L207) 表 B 與 [L413](file:///home/hatch/drama-line/CAMERA_COVERAGE_AGY_MEMO.md#L413) §4.2 | 稱 `5.5s` 淨／`6.5s` 生為「`V1 H3 硬頂`」「`引擎物理上限`」；[L416](file:///home/hatch/drama-line/CAMERA_COVERAGE_AGY_MEMO.md#L416) 短鏡豁免未區分 H3 4 秒生成下限 | 混淆「產線品質／L4 穩態帽」與「引擎物理上限（15s）」；且 `is_short_coverage_ok` 若套用在 H3 `CU` 反應鏡上（生成 `2.0–3.0s`），會誤導送出 `<107f` 請求。 | 改措辭為「**V1 產線品質與 L4 穩態上限（非 H3 15s 模型硬頂）**」；並在 `is_short_coverage_ok` 旁加註「僅豁免剪輯淨長，H3 生成端仍自動墊至 `≥4.0s (107f)` 再裁切」。 |
| **4** | [`STORYBOARD-SPEC-V2.md`](file:///home/hatch/drama-line/STORYBOARD-SPEC-V2.md#L207-L214) §四 與 [`tools/preflight_gate.py`](file:///home/hatch/drama-line/tools/preflight_gate.py) | §四僅註明 Flow R2V 禁與 i2v 混用，**漏寫 H3 FL2V 與 Ref2VA 互斥**；`preflight_gate.py` **零檢查** `last_frame`／`L2_flf` vs `ref2v`；[L1383](file:///home/hatch/drama-line/tools/preflight_gate.py#L1383) `gen_sec > 6.5` 不分 L4/A100 一律 FAIL | 無法機械攔截錯誤混填；且在 `accelerator="A100"` 時仍被 L4 品質帽寫死。 | ① §四補上 H3 `i2v_first_last` 與 `ref2v` 互斥紅線；② `preflight_gate.py` 新增 `H3_MODE_EXCLUSION`（`gen_mode=ref2v` 禁帶 `last_frame` 或 `control_method=L2_flf`）與 `H3_MIN_DURATION`（`<4.0s` 提示墊幀）；③ V1 區分 `L4` 與 `A100/SM9` 上限語意。 |
| **5** | [`AMD05_V3_AGY_MEMO.md`](file:///home/hatch/drama-line/AMD05_V3_AGY_MEMO.md#L57-L63) §1.2 | 已標註 Colab L4，但未顯式區分「全息雙人」vs「雙實心真人」在 9 槽算力下的差異 | 易讓後續讀者誤以為 H3 本身永遠只能跑 4 槽單人。 | 補一句範疇聲明：4 槽屬 **Colab L4 `max` 硬體上限（H3 原生 9 槽）**；全息雙人於任何算力仍受限材質互斥，但雙實心真人若切 A100/API 可解鎖 6–9 槽。 |
| **6** | [`DESIGN.md`](file:///home/hatch/drama-line/DESIGN.md#L936) §9.1（v1.4 舊殘留） | 仍寫「12/05 補位由 H3 Ref2V（**`768×1344`**、$N=4$）接手」 | 該句為 SM-7A 實測前的預估；於 Colab L4 上 `768×1344` 極高機率 OOM 且單抽 `10–14 min`。 | DESIGN 升 v1.5 時同步更正為「L4 走 **`544×960`（`0.5 MP`，SM-7A 實證）＋Lanczos 升頻**；僅切 A100/G4 時始開 `768×1344`」。 |

---

## 4. 官方 API／主流託管平台路線之客觀決策依據（中立呈現，不做推薦）

> **立場聲明**：是否導入官方 API／託管平台完全由 Creator 拍板；以下僅做「**若改走官方 API，哪些既有技術結論會改變、實質代價是什麼**」的乾淨對照，**不作贊成或反對推薦**。

### 4.1 哪些結論會改變 vs 哪些結論不變？

| 議題／既有結論 | 若切官方 H3 API／主流託管平台 | 結論是否改變？ | 說明 |
| :--- | :--- | :---: | :--- |
| **9 張參考圖（含雙實心真人 H3 同框）** | 直接解鎖最多 **9 圖／3 影／3 音／總計 12 檔**，無 L4 VRAM／RAM 瓶頸 | **改變（解鎖）** | 兩名實心真人（各給 3 視角防錯邊疤＋首幀＋道具＝8 槽）可安全同框跑 H3 Ref2VA；亦不再受 L3 白膜 `≤0.35 MP / ≤5s` 記憶體硬鎖。 |
| **AMD-05 v3 雙人 H3 否決（范蠡＋全息 `SYS-01`）** | 槽數壓力消失，但**實心棚拍卡 vs 半透明全息材質互斥**仍為模型本質特性 | **核心不變（仍須實測）** | 即使開 9 槽，Flow Omni `i2v_first` 仍有「0 點 `nano2`＋QC-1 鎖首幀＋較佳體積光塵」優勢；全息雙人仍不自動轉 H3。 |
| **解析度（`544×960`＋升頻 → 原生 `768P`／`2K`）** | 可直出原生 **`768P` 或 `2K`**，且走官方完整權重（非社群 `TriPRISM` 8-step `w6a8` 蒸餾） | **改變（顯著升級）** | 徹底免除 `544×960 → 1080×1920` 放大軟化，特寫毛孔、1.2cm 眉尾疤、粗麻織紋與眼角反光更銳利；且無 8-step 蒸餾對運鏡幅度的潛在壓縮（實際 9:16 差距 `[未實測]`）。 |
| **單鏡時長（`4–15s` 整數秒）** | 移除 L4 OOM 上限，可跑 `6–15s`；但 **`<4s` 請求會被 API 拒收** | **硬體邊界改變；剪輯／品質原則不變** | 可拍 6–10s 低動態長獨白母鏡供 L-cut；但豎屏短劇快節奏（`ASL 1.8–2.6s`）、V2 語速與長鏡漂移檢核仍維持。 |
| **首尾幀（FL2V）與 Ref2VA 互斥** | 官方規格同樣**嚴禁混用** | **不變** | 無法同時鎖尾幀又餵多張角色參考圖。 |
| **SM-7A 條件 1（QC-1 乾淨首幀）與全面 TTS（ADR-006）** | 多圖仍無法擦除髒首幀缺陷；原生 32kHz 中文對白仍非台灣腔鎖定聲線 | **不變** | QC-1、QC-2 與 ElevenLabs `eleven_v4` TTS 全數維持原狀。 |
| **執行延遲與維運穩定性** | 免除 Colab 冷啟動（`~90s`）、偶發分配卡死（如 `DEMO02_v2 S3b` 600s 逾時）與 `5–7 min/take` 排隊 | **改變（吞吐改善）** | 改為標準 HTTP API 非同步輪詢，批次併發更容易控管。 |

### 4.2 官方 API／託管平台路線之實質代價（In-Kind Costs）

| 代價維度 | 本地 Colab L4 開源權重路線（現況） | 官方 H3 API／主流託管平台路線 |
| :--- | :--- | :--- |
| **1. 直接現金支出（Paid API）** | 已涵蓋於既有 Colab Pro 月配額（`200 CU/月`）；EP-01 全集 9 顆 H3＋1 顆 L3 僅耗 `~4.3 CU`（**2.2% 配額、$0 新增現金**）`[實測推算]`。 | **按秒／按解析度計費之新增現金支出**（原生 `2K`、較長秒數與 `1.6–2.3×` 重抽倍率會直接放大每集現金成本；且須另建付費帳號與金鑰管理。*註：本只讀任務未連網查現時 API 牌價，不猜測單價*）。 |
| **2. 資料外流與肖像治理（Data Egress）** | 影像與提示詞僅經 Google Flow（現有通路）與我方臨時掛載之 Colab worker（休眠即銷毀實例磁碟），不送進 MiniMax 或第三方聚合商持久雲端。 | 范蠡定妝照源自 **Creator 本人肖像原型**（[`DESIGN.md`](file:///home/hatch/drama-line/DESIGN.md#L7) §V1.4-02 治理條款）。走官方／第三方 API 代表將**肖像衍生母圖與未公開劇本提示詞跨境送往外部商業影片平台**，須接受該平台之資料留存、內容審查（可能誤殺古裝刀劍／時事題材）與模型訓練退出條款。 |
| **3. H3 授權與地域條款（對照 Creator 2026-11-27 台灣裁示）** | 適用 **`MiniMax H3 Community License` Section V.4**（排除 **US / EU / UK / 南韓**含產出使用）。**台灣不在排除清單**，但 Colab 實例常配發美區 GPU，構成已登錄之實務灰區；Creator 已於 2026-11-27 拍板維持原設計（「我是台灣不是美區沒事的」，見 [`DESIGN.md`](file:///home/hatch/drama-line/DESIGN.md#L935) §9.1 與 [`WORKFLOW_OPT_DISCUSSION.md`](file:///home/hatch/drama-line/WORKFLOW_OPT_DISCUSSION.md#L29)）。 | 託管雲端商業 API 改受官方 API 服務條款約束，**不適用開源權重 Section V.4 的美／歐／英／韓地域排除**（[`WORKFLOW_OPT_DISCUSSION.md`](file:///home/hatch/drama-line/WORKFLOW_OPT_DISCUSSION.md#L29) 實查「託管雲端 API 全球可用」），因此**反倒消除了美區 Colab GPU 的開源條款灰區**，代價則轉移為上述現金費、內容審查與跨境資料外流。 |
| **4. 工程接入與切換成本** | 現有 `h3_r2v_4ref_groupB.json`、`h3_r2v_clay.json` 與 `run_stage4_h3.py` 已完整打通並通過 `DEMO02_v2` 驗收（0 新增開發）。 | 須新增 API client 轉接層（金鑰保管、30MB／256–5760px／12 檔／整數秒 `4–15s` 前置校驗、重試與計費帳本），並遵守 API 專屬速率限制。 |

---

## 5. 待 Creator 拍板問題（限 3 題）

1. **是否授權執行低成本 SM-9 本地餘裕冒煙（Colab L4，不超過 `1.3 CU`）？**
   - 選項 A：只跑 **SM-9A**（`~0.55 CU`），一次測清 `7.29s (175f)` 與 `8.00s (192f)` 低動態 4 槽對白是否 OOM 或晚幀漂移（同步確認 EP-01 `S07` 跨過 `158f` 的安全性）。
   - 選項 B：跑 **SM-9A ＋ SM-9B**（`~1.0–1.3 CU`），一併測清 6 槽 `match` vs `max` 的 VRAM/RAM 與畫質取捨。
   - 選項 C：**不跑 SM-9**，直接鎖死已實證的 `≤ 5.88s (141f)` 與 `≤ 4 槽 max` L4 包絡進 EP-01。
2. **EP-01 短 H3 鏡（`S04c`/`S11a`/`S11c`）與 `S07` 17-frame 進位處置定案**：
   - 是否同意將所有淨＋緩衝 `< 4.0s` 的 H3 鏡在 `run_stage4_h3.py` **自動墊至 `4.0s`（`107f / 4.46s`）生成再於粗剪裁切**（對齊官方 4s 下限與 `S3a` 已測安全點），同時將 `S07` 壓進已驗證的 `≤ 5.8s`（`141f`）桶（除非 SM-9A 先行驗證 `158f+`）？
3. **官方 H3 API／A100 升階政策定位（產線文件怎麼寫）**：
   - 依 §4 中立對照，您希望將 Phase 3–4 的 H3 路由在文件上**單純鎖定「本地 Colab L4（`544×960`＋升頻），A100 僅作手動例外」**，抑或同時在架構文件中**預留「官方 H3 API（768P／2K／9 槽）條件式按量備援槽位」**（限定僅於未來「雙實心真人英雄鏡／2K 旗艦鏡」且經您逐案簽核肖像跨境條款後始啟用）？
