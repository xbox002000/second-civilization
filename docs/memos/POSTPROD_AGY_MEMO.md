# 後製鏈優化——工程討論備忘錄（agy 立場與查證定案）

> **文件日期**：2026-11-28（系統時鐘 2026-11-27 UTC）  
> **性質**：只讀查證與工程設計討論（**未安裝任何套件、未修改 `DESIGN.md`、未 push**）  
> **對齊基準**：`DESIGN.md` v1.4、`STORYBOARD-SPEC-V2.md`（含附錄 A）、`POSTPROD-EDITING-REF.md`、ADR-002（先半自動跑通 EP-01，系統自動化排 Phase 5）與減法紀律  
> **本機 VM 實勘基線（只讀 `lscpu`/`free`/`df`/`node -v`/`ffmpeg -version`/`fc-list`）**：  
> - CPU：`Intel(R) Xeon(R) CPU @ 2.20GHz`，**2 實體核 × 2 執行緒 = 4 vCPU**，指令集至 **AVX2**（**無 AVX-512、無 AMX**），無 GPU  
> - 記憶體與磁碟：15Gi RAM（可用 ~13Gi，無 Swap）／49G 磁碟（剩餘 40G，16% 使用）  
> - 既有工具：`ffmpeg 5.1.9`（含 `libass`/`libx264`/`libfreetype`/`libfontconfig`/`librsvg`/`libzimg`）、`python3 3.11`、Docker、`node v18.20.4`  
> - **現況缺口**：**無 Chromium / Chrome**；系統中文字體目前僅 `WenQuanYi Zen Hei`（文泉驛正黑）、`Droid Sans Fallback`、`Unifont`，**尚未安裝 `Noto Sans TC` / `Source Han Sans`**

---

## 零、單一推薦結論（併入 DESIGN v1.5 定稿建議）

**支持 Muse「不換剪輯器」大方向，對三項初評給出單一收斂方案**：
1. **`edit_manifest.json`（EDL）＋ `ffmpeg` 渲染：立即採納並寫入 DESIGN v1.5**——借鏡 FableCut 的 `revision` 樂觀鎖、`media[]` 媒體註冊表與音視軌分離結構，但裁掉所有瀏覽器／UI／任意關鍵幀欄位，與 `script_pack.json`（上游敘事不可變）及 `production_state.json`（生成歷程可變）建立清晰「三檔分責」；Phase 3 以精簡樣板半自動跑通 EP-01，Phase 5 實作 `manifest_builder.py`＋`drama_assembler.py` 兩段式編譯渲染。
2. **`faster-whisper` 進 QC 工具箱：修正掛點與模型後採納（Phase 5 工具化；Phase 3–4 僅作選用研究腳本）**——實勘本 VM 僅 2 實體核 AVX2，跑 `large-v3` int8（含 `word_timestamps`）達 **RTF 2.5–4.0×**，且本產線已全面改走 ElevenLabs TTS（原生人聲於組裝時捨棄）；**嚴禁掛在全抽卡原生音訊驗對白或用來驗台灣讀音**。定案僅保留兩個高價值掛點：① 時事線對標／新聞參考片逐字稿拆解（預設 **`large-v3-turbo` int8**，重度中英夾雜才升 `large-v3`）；② 僅對 `LIP_SENSITIVE` 入選鏡作口型時序複檢（實際起迄對位優先用 <2 秒的 VAD/`silencedetect`，TTS 字幕逐字對齊優先直接啟用 ElevenLabs `/with-timestamps` API，0 CPU 消耗）。
3. **證據卡／Truth Ledger 卡升級路徑：Phase 3–4 維持 `Pillow + ffmpeg`（優先補裝 `Noto Sans TC` 字體即大幅提質），Phase 5 條件式升級唯一鎖定 `HyperFrames`（Apache-2.0 ＋ Docker 隔離），淘汰 `Remotion`**——避開 Remotion 4 人以上團隊／自動化管線之 Company License 商業條款（Automators $100/月起）與 React 建置鏈稅；若 EP-03 市場驗證後啟動升級，**最小遷移路徑為「先且僅先遷片尾 3.5 秒 Truth Ledger Card」**，若 `Pillow + ffmpeg` 留存已達標則永久維持減法不遷。
4. **其餘 9 項工具**：依減法紀律與 ADR-002，**7 項直接淘汰**（`auto-editor`、`MoviePy`、`Piper`、`Chrome DevTools MCP`、`WeftCut`、`Pireel`、`Editroom`），**2 項列低接觸備援**（`Openverse`、`Impeccable`）。

---

## 一、三項外部查證結果（只讀查證，未安裝）

### 1.1 FableCut（`ronak-create/FableCut`）

| 查證項目 | 查證結果 |
| :--- | :--- |
| **授權** | **MIT License**（無商用或傳染限制）。 |
| **架構定位** | 零 npm 依賴之 Node 伺服器＋瀏覽器 NLE（SSE ~150ms 即時重載），提供 MCP（`npx fablecut mcp`）、REST API 與直接讀寫單檔 `project.json`；匯出採瀏覽器 WebCodecs 合成＋離線混音＋FFmpeg 編碼。 |
| **`project.json` 實際 Schema** | 依官方 `CLAUDE.md` 規格，頂層結構包含：`name`、`width`、`height`、`fps`、**`revision`**（每次寫入遞增的整數版本鎖，防人機並發覆寫）、`tracks[]`、`media[]`、`clips[]`：<br>• `tracks[]`：`[{ id: "V1", kind: "video", name?, locked?, muted?, solo? }, { id: "A1", kind: "audio" }]`（支援多條視訊／音訊軌）。<br>• `media[]`：集中素材註冊表 `[{ id: "m_abc", name, kind: "video|audio|image|svg", src, duration, width, height }]`。<br>• `clips[]`：扁平片段清單，每筆含 `id`、`mediaId`（`text`/`adjust` 層為 `null`）、`kind`、`track`、`start`（時間軸起點秒）、`duration`（時間軸時長秒）、`in`（原始素材裁切起點秒）、`props`（`scale`/`opacity`/位移/調色/濾鏡）、`keyframes`（`{ prop: [{ t, v, ease }] }`，`t` 相對於片段起點）、`transitionIn`／`transitionOut`（`{ type, duration }`）。<br>• 編修模型：提供 `fablecut_patch_project` 原子操作（`addClip`/`updateClip`/`removeClip`/`split`/`rippleDelete`）。 |
| **可借鏡程度（~45%）** | **建議借鏡（5 項）**：① 單一宣告式 JSON＋`revision` 遞增版控；② `media[]` 素材註冊表與時間軸 `clips` 解耦（單一來源避免路徑重複與不一致）；③ 明確分軌（視訊主軌／疊加層／對白／環境聲／SFX／BGM）；④ 片段顯式標註 `source_in_sec`／`timeline_start_sec`／`duration_sec` 與 `transition_in`/`transition_out`；⑤ 支援小幅 JSON patch 重算而不碰上游劇本。<br>**不應照搬（3 項）**：① 瀏覽器 UI 狀態（`locked`/`solo`/SSE/WebCodecs 匯出）；② 任意屬性時間軸 `keyframes` 曲線字典（`ffmpeg filter_complex` 無法廉價表達任意 spline 關鍵幀，我方僅需結構化 L4 運鏡與後製預設）；③ 通用 NLE 的 `null`/`adjust`/`shape` 圖層（我方需要領域語意明確的 `fact_hud`、`truth_ledger`、`master_clean` 雙母帶切換）。 |

### 1.2 `faster-whisper`（SYSTRAN，CTranslate2 後端）

| 查證項目 | 查證結果 |
| :--- | :--- |
| **VM CPU 實際速度量級（4 vCPU / 2 實體核 / AVX2 無 GPU）** | 先統一符號：**RTF（Real-Time Factor）＝ 推論耗時 ÷ 音訊時長**（RTF > 1 代表比即時慢；RTF < 1 代表比即時快）。<br>• **官方參考基準**：SYSTRAN README 以 `small` int8 跑 13 分鐘音檔於桌面級 i7-12700K 耗時 1m42s（RTF ≈ 0.13，RAM ~1.5GB）。<br>• **`large-v3` int8（1.55B 參數、32 層 Decoder、~3.0–3.5GB RAM）於本機 2 核 4 執行緒 Xeon 2.2GHz（僅 AVX2，無 AVX-512/AMX）推估**：因自迴歸 Decoder 逐 token 計算受記憶體頻寬與核心數瓶頸，社群實測落在 **RTF ≈ 2.0–3.5×**（1 秒音訊需 2.0–3.5 秒 CPU）；開 `word_timestamps=True` 另增 **+15%–30%** 開銷，實效 **RTF ≈ 2.5–4.0×**（處理 2 分鐘音訊約需 **5–8 分鐘**）。<br>• **`large-v3-turbo` int8（809M 參數、Decoder 由 32 層剪枝至 4 層、~1.5–2.0GB RAM）**：CPU 解碼提速 **3–5×**，推估 **RTF ≈ 0.6–1.2×**（含 `word_timestamps` 接近即時）；`small` int8 約 **RTF ≈ 0.2–0.4×**。<br>• **誠實標註〔未實測〕**：受雲端 VM 超分搶佔與 Xeon 2.2GHz 單核頻率影響，上述為文獻與同級硬體推估區間，導入前須以 30 秒實檔做 1 次冒煙量測回填。 |
| **中文（台灣國語 `zh-TW`）辨識品質評價** | • **預設偏簡中／陸詞**：未設 prompt 時易吐簡體字與大陸用語（如「信息」「軟件」）。實務**強制**傳入 `language="zh"`＋繁體台灣腔 `initial_prompt`（含當集專有名詞如「范蠡、輝達」），必要時輔以 `OpenCC (s2twp)` 正規化。<br>• **`large-v3` vs `large-v3-turbo`**：`large-v3` 對台灣口語、財經科技中英夾雜（code-switching）準確率最高且幻覺最少；`large-v3-turbo` 因 4 層 Decoder 記憶較短，長音檔偶發飄回簡體或漏詞（WER 略高 +1–2%），但對 3–6 秒短句或搭配 `vad_filter=True` 分段表現接近 `large-v3`。<br>• **關鍵盲區（工程紅線）**：**Whisper 是語意 ASR，不是發音／聲調檢核器**。當 TTS 把「范蠡」誤讀成 `ㄌㄧˋ` 或「垃圾」讀成陸音 `ㄌㄚ ㄐㄧ`，Whisper 語言模型仍會自動還原輸出正確正字「范蠡」「垃圾」→ **無法用來驗台灣讀音，否則會造成「假過關」**。 |
| **`word_timestamps` 取得方式與中文精度** | • **呼叫方式**：`WhisperModel(size, device="cpu", compute_type="int8", cpu_threads=2)`（建議設實體核數 `2` 或實測 `2` vs `4`，避免超執行緒搶快取）搭配 `model.transcribe(audio, language="zh", initial_prompt=..., vad_filter=True, word_timestamps=True)`，從 `segment.words` 讀出 `word.start`／`word.end`／`word.word`。<br>• **底層機制與中文誤差**：由 CTranslate2 對 Cross-Attention 權重跑 **DTW（動態時間規整）** 推估 token 邊界。中文無空白分詞，輸出為單字或雙字子詞粒度，受 attention diffusion 影響，**字級邊界抖動約 ±100–300ms**（句首起聲／句尾收聲相對穩，約 ±80–150ms；若需 <50ms 精準字級對齊須外掛 `WhisperX`＋wav2vec2，不建議在無 GPU VM 引入）。 |

### 1.3 HyperFrames（`heygen-com/hyperframes`）vs Remotion（`remotion-dev/remotion`）

| 比較維度 | **HyperFrames (`heygen-com/hyperframes`)** | **Remotion (`remotion-dev/remotion`)** | **現行 `Pillow + ffmpeg`（對照組）** |
| :--- | :--- | :--- | :--- |
| **授權條款** | **Apache-2.0**（完全開源免費商用，**無人數上限、無按次渲染費**，擴編團隊零授權懸崖）。 | **Source-Available 雙授權（Company License）**：個人與 **≤3 人組織免費商用**；**達 4 人以上即須付費**——手動創作 Creators `$25/人/月`、**自動化批次管線屬 Automators `$100/月起 ＋ $0.01/次渲染`**。 | **MIT-like (HPND) / GPL CLI**（獨立進程呼叫 ffmpeg，商用完全無限制）。 |
| **編寫模型** | 純 **HTML + CSS + JS**（直接用 `GSAP` / `SVG` / `Lottie` / `Three.js`），單檔可直接在瀏覽器預覽，極適合 AI Agent 讀寫與 Git diff。 | **React + TypeScript** 元件樹＋Webpack/Bundler 專案（有官方 `remotion-dev/skills` 輔助 Agent，但需維護整套 React 專案與依賴樹）。 | Python `Pillow` 繪製 1080×1920 PNG 圖層＋`ffmpeg` `zoompan`/淡入淡出/疊加。 |
| **VM 環境需求（對照本機現況）** | • **Node 22+**（本機僅 `v18.20.4`，須升 Node 或走 Docker）<br>• Headless Chromium（`chrome-headless-shell`，CDP `HeadlessExperimental.beginFrame` 逐幀擷取，~350MB）<br>• CJK 字體（`fonts-noto-cjk` ~250MB）<br>• **官方支援 `npx hyperframes render --docker`**（容器內一次打包 Node 22＋固定版 Chromium＋Noto CJK 字體，本機已有 Docker，映像檔約 **1.5–2.5GB** 磁碟）。 | • **Node 18+**（相容本機 `v18.20.4`，但推薦 20+）<br>• Headless Chromium（Puppeteer 管理，~350MB＋Debian 系統共享函式庫 `libnss3`/`libgbm1` 等）<br>• CJK 字體（`fonts-noto-cjk` 本地安裝，避免無頭渲染抓遠端 Google Fonts 失效）<br>• 可自包 Dockerfile 或裸機安裝（約 **1.2–2.0GB** 磁碟）。 | **零新依賴**（VM 已裝 `python3` + `ffmpeg 5.1.9`，僅需補裝 `fonts-noto-cjk` ~200MB 即可解決現行文泉驛美觀度問題）。 |
| **5 秒 1080×1920 30fps（150 幀）無 GPU VM 渲染耗時推估** | • 輕量證據卡（文字＋色塊＋向量線＋GSAP 滑入，**避開大面積 `backdrop-filter`/`blur`**）：推估 **~10–30 秒／張**（含 Chromium 冷啟 2–4s）。<br>• 重度濾鏡／透明通道（WebM/MOV alpha）：增耗 2–3.5×（**~45–90 秒**）。 | • 輕量卡片（`--concurrency=2` 對齊 2 實體核，JPEG 擷取）：推估 **~5–15 秒／張**。<br>• 中等圖表＋多圖層：**~15–30 秒／張**；重度模糊／Canvas 退回 SwiftShader（`--gl=swangle`）跳升 **30–60 秒+**。 | **~2–4 秒／張**（純 CPU 光柵化＋x264，確定性最高、RAM <300MB）。 |
| **無頭 VM 適配度與風險** | **高**（Docker 隔離直接避開 Debian 12 舊 Node 18 與系統函式庫漂移，跨 VM 90 天遷移完全像素一致；惟框架較新，API 變動風險略高於 Remotion，須鎖定容器版號）。 | **高**（生態最成熟、併發調校文件完整；但 4 人團隊／自動化計費條款形成長期商業鎖定風險，且在 2 實體核 VM 上多 Tab 併發收益有限）。 | **極高**（但複雜動態圖表、逐行高亮時間軸、流暢緩動排版寫成 ffmpeg 表達式維護成本極高）。 |

> *誠實標註〔未實測〕*：HyperFrames 與 Remotion 於本機 2 核 Xeon 2.2GHz 無 GPU 環境之精確秒數與 RAM 峰值尚未實跑，上述為 150 幀無頭軟體光柵化文獻區間；Phase 5 正式遷移前須先做單卡冒煙測試驗證（目標 <45 秒／張、RAM 峰值 <3GB）。

---

## 二、Q1–Q4 工程討論答覆

### Q1：`edit_manifest.json` 規格（可直接併入 DESIGN v1.5）

#### 1. 三檔分責邊界（絕不重複造輪）
為完全對齊 `STORYBOARD-SPEC-V2.md` 的兩層雙檔分離，Stage 6 正式引入第三檔 `edit_manifest.json`，形成嚴格單向流：

| 檔案路徑 | 生命週期與可變性 | 唯一真相範圍（Owns） | 明確**不放**什麼 |
| :--- | :--- | :--- | :--- |
| `episodes/EP{NNN}/input/script_pack.json` | 上游核准後**不可變**（鎖 SHA256） | 敘事契約：`beats[]`、`segments[]`、`shots[]`、`dialogue[]`、`visual_text_overlay[]`、`audio_groups[]`、`trim_policy`、`transition_out`、`control_method`。 | 不放實檔路徑、TTS 實測秒數、抽卡歷程、微調延遲。 |
| `episodes/EP{NNN}/plan/production_state.json` | 階段 1.5–5 **執行期可變** | 生產歷程與選片結果：`shots_state[shot_id]`（`state`、`takes[]`、`selected_take`、TTS 實測秒數與 `audio_ref`、最終引擎與降級紀錄、`previs_artifacts`、`qc_checks`、QC-2 初填之 `audio_offset_ms`）。 | 不放跨鏡剪輯拼接時間軸、調色參數、BGM Ducking、多次 RC 剪輯變體。 |
| `episodes/EP{NNN}/plan/edit_manifest.json`（及變體如 `edit_manifest_cutdown.json`） | 階段 6–7 **可版控遞增（`revision++`）** | **純確定性組裝指令（EDL）**：`media[]` 媒體清單、V1 主視訊軌（入出點／時間軸起迄／L4 運鏡／調色／後製 FX／轉場）、A1–A4 四音軌（含 L-cut/J-cut 與延遲）、V2 疊加層（證據卡／HUD 事實角標／字幕／片尾 Truth Ledger 卡）與輸出規格。 | **不複製** prompt、未入選 takes 歷史、資產譜系（seed/parent_ref）、完整劇本散文（僅以 `shot_id`／`beat_id`／`source_refs` 參照）。 |

> **為何不能直接併進 `production_state.json`？** 同一份 QC-2 核准的 `production_state.json` 須能衍生多份不同剪輯清單——`animatic` 預演、`master_9x16` 正片（`rc1`→`rc2`）、`cutdown_15s`（Threads 15 秒預告）、未來 `zh-CN` 重封裝——分離為獨立 `edit_manifest.json` 才能保證剪輯迭代不汙染上游 QC 狀態檔，且每次修剪都是可 diff 的純文字變更（可直接取代原 `DESIGN.md` §1.2 中未定義規格的 `edl.json`）。

#### 2. 誰產生、誰修改（權責流程）
1. **初版自動編譯（`agy` 產生，禁止人工手刻全檔）**：QC-2 拍板鎖定 `production_state.json` 後，由 `manifest_builder.py`（Phase 5；Phase 3 採極簡 Python 範本腳本）讀取 `script_pack.json` ＋ `production_state.json`，自動呼叫 `ffprobe` 取得每支入選片與 TTS 實長，套用 `trim_policy`（`standard_0.5s` / `tail_only` / `none`）、展開 `audio_groups[]` 為 L-cut/J-cut 音軌、掛入 `beats[]` HUD 角標與 Truth Ledger 卡，產出 `revision: 1` 的 `edit_manifest.json` 並執行預檢驗證。
2. **微調補丁（`Muse` 依 QC-2／QC-3 意見修訂，`agy` 驗證重算）**：Muse 不手寫整份 EDL，僅針對具體問題（如「S04 開口慢 120ms」「S03b 尾音 L-cut 延入 S04 0.7s」「S02 色溫微暖對齊 S01」「S11b 卡片延長 0.4s」）修訂對應欄位（或提供 patch 給 `agy` 套用並遞增 `revision`），隨即重跑預檢與 `ffmpeg` 輸出 `rc{N+1}`（<60 秒）。
3. **階段 3.5 / 快線複用**：同一 schema 支援 `profile: "animatic"`（LTX 低清＋TTS＋鏡號浮水印）與 `profile: "storyboard_still"`（靜態首幀＋TTS），避免維護兩套不互通的剪輯設定。

#### 3. 可直接併入 DESIGN v1.5 的 `edit_manifest.json` Schema 草案（`schema_version: "1.0"`）

```json
{
  "schema_version": "1.0",
  "revision": 1,
  "episode_id": "EP001",
  "track": "regular",
  "profile": "master_9x16",
  "source_refs": {
    "script_pack_path": "episodes/EP001/input/script_pack.json",
    "script_pack_sha256": "<sha256>",
    "production_state_path": "episodes/EP001/plan/production_state.json",
    "production_state_sha256": "<sha256>"
  },
  "output": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "pix_fmt": "yuv420p",
    "video_codec": "libx264",
    "crf": 18,
    "audio_sample_rate": 48000,
    "audio_lufs": -14.0,
    "true_peak_dbtp": -1.5,
    "emit_clean_master": true,
    "clean_master_path": "episodes/EP001/out/EP001_REG_master_clean.mp4",
    "final_output_path": "episodes/EP001/out/EP001_REG_master_9x16_rc1.mp4",
    "region_profile": "zh-TW"
  },
  "media": [
    {
      "media_id": "m_s01_vid",
      "kind": "video",
      "path": "episodes/EP001/clips_raw/EP001_REG_S01_veo_v1_t02.mp4",
      "probe_duration_sec": 6.0,
      "probe_fps": 24.0,
      "has_audio": true
    },
    {
      "media_id": "m_s01_tts",
      "kind": "audio",
      "path": "episodes/EP001/audio_tts/EP001_REG_S01_tts_v1.wav",
      "probe_duration_sec": 4.42
    },
    {
      "media_id": "m_s11b_card",
      "kind": "card_video",
      "path": "episodes/EP001/cards/S11b_evidence_card.mp4",
      "probe_duration_sec": 3.2
    },
    {
      "media_id": "m_roomtone_studio",
      "kind": "audio",
      "path": "audio_lib/roomtone/studio_night_48k.wav",
      "probe_duration_sec": 60.0
    },
    {
      "media_id": "m_bgm_suspense",
      "kind": "audio",
      "path": "audio_lib/bgm/01_Suspense_Investigation_01.wav",
      "probe_duration_sec": 140.0
    }
  ],
  "video_track": [
    {
      "clip_id": "v_S01",
      "shot_id": "S01",
      "segment_id": "SEG-01",
      "beat_id": "B03",
      "media_id": "m_s01_vid",
      "trim_policy_applied": "standard_0.5s",
      "source_in_sec": 0.50,
      "source_out_sec": 5.50,
      "timeline_start_sec": 0.00,
      "duration_sec": 5.00,
      "speed": 1.0,
      "scale_mode": "lanczos_cover",
      "l4_motion": null,
      "color_grade": {
        "lut_path": null,
        "eq": { "brightness": 0.0, "contrast": 1.03, "saturation": 0.96, "gamma": 1.0 },
        "color_temp_shift": 0
      },
      "post_fx": [
        { "type": "focus_hunt_gblur", "start_sec": 0.0, "end_sec": 0.4, "sigma_start": 3.5, "sigma_end": 0.0 }
      ],
      "transition_in": { "type": "cut", "duration_sec": 0.0 },
      "transition_out": { "type": "cut", "duration_sec": 0.0 }
    },
    {
      "clip_id": "v_S11b",
      "shot_id": "S11b",
      "segment_id": "SEG-03",
      "beat_id": "B05",
      "media_id": "m_s11b_card",
      "trim_policy_applied": "none",
      "source_in_sec": 0.00,
      "source_out_sec": 3.20,
      "timeline_start_sec": 5.00,
      "duration_sec": 3.20,
      "speed": 1.0,
      "scale_mode": "exact",
      "l4_motion": { "type": "ken_burns", "zoom_start": 1.0, "zoom_end": 1.06, "pan_x": 0.0, "pan_y": -0.02, "easing": "ease-in-out" },
      "color_grade": null,
      "post_fx": [],
      "transition_in": { "type": "dissolve", "duration_sec": 0.20 },
      "transition_out": { "type": "cut", "duration_sec": 0.0 }
    }
  ],
  "audio_tracks": {
    "dialogue": [
      {
        "clip_id": "a_dlg_S01",
        "media_id": "m_s01_tts",
        "shot_ids": ["S01"],
        "audio_group_id": null,
        "timeline_start_sec": 0.25,
        "source_in_sec": 0.0,
        "duration_sec": 4.42,
        "offset_ms": 0,
        "cut_style": "sync",
        "lead_in_sec": 0.0,
        "tail_over_sec": 0.0,
        "gain_db": 0.0,
        "voice_preset_ref": "bible/voices/FANLI.yaml"
      },
      {
        "clip_id": "a_dlg_AG_S16",
        "media_id": "m_ag_s16_tts",
        "shot_ids": ["S16a", "S16b"],
        "audio_group_id": "AG-S16",
        "timeline_start_sec": 74.30,
        "source_in_sec": 0.0,
        "duration_sec": 5.10,
        "offset_ms": -100,
        "cut_style": "l_cut",
        "lead_in_sec": 0.0,
        "tail_over_sec": 0.70,
        "gain_db": 0.0,
        "voice_preset_ref": "bible/voices/FANLI.yaml"
      }
    ],
    "ambience": [
      {
        "clip_id": "a_amb_S01",
        "source_type": "roomtone_file",
        "media_id": "m_roomtone_studio",
        "timeline_start_sec": 0.00,
        "source_in_sec": 0.00,
        "duration_sec": 5.00,
        "gain_db": -22.0,
        "fade_in_sec": 0.2,
        "fade_out_sec": 0.2,
        "duck_by_dialogue_db": -6.0,
        "native_voice_verified_clean": false
      }
    ],
    "sfx": [
      {
        "clip_id": "a_sfx_glitch",
        "media_id": "m_sfx_glitch_01",
        "anchor_shot_id": "S03b",
        "timeline_start_sec": 12.40,
        "source_in_sec": 0.0,
        "duration_sec": 0.45,
        "gain_db": -4.0
      }
    ],
    "bgm": [
      {
        "clip_id": "a_bgm_01",
        "bgm_cue": "01_Suspense_Investigation",
        "media_id": "m_bgm_suspense",
        "timeline_start_sec": 0.00,
        "source_in_sec": 0.00,
        "duration_sec": 120.0,
        "gain_db": -16.0,
        "fade_in_sec": 1.0,
        "fade_out_sec": 2.5,
        "duck_by_dialogue_db": -12.0
      }
    ]
  },
  "overlays": {
    "card_overlays": [
      {
        "overlay_id": "ov_lower_01",
        "type": "lower_third",
        "renderer": "pillow_ffmpeg",
        "beat_id": "B01",
        "media_id": "m_ov_lower_01_png",
        "timeline_start_sec": 1.20,
        "duration_sec": 2.80,
        "placement": { "x": 54, "y": 1420 },
        "fade_in_sec": 0.2,
        "fade_out_sec": 0.2
      }
    ],
    "fact_hud": [
      {
        "beat_id": "B01",
        "fact_tier": "FACT",
        "hud_label": "2026.11 公開財報數據",
        "timeline_start_sec": 5.00,
        "full_display_sec": 3.00,
        "collapse_to_dot": true,
        "end_sec": 14.50,
        "placement": { "x": 54, "y": 140 }
      }
    ],
    "subtitles": {
      "enabled": true,
      "format": "ass",
      "path": "episodes/EP001/out/subtitles.ass",
      "style_template": "templates/subtitles_zh_tw.ass",
      "timing_source": "dialogue_track"
    },
    "end_card": {
      "enabled": true,
      "type": "truth_ledger",
      "renderer": "pillow_ffmpeg",
      "media_id": "m_endcard_truth",
      "duration_sec": 3.50,
      "transition_in": { "type": "fade_black", "duration_sec": 0.30 },
      "payload": {
        "fact_anchors": ["2026.11 Q3 公開財報：單季資本支出年增 62%"],
        "disclaimer_text": "本片角色「范蠡」與人物對話屬世界觀戲劇演繹（FICTION）；結構與利益分析屬推論／假說（INFERENCE / HYPOTHESIS），不構成投資或法律建議。",
        "lab_url": "lab.example/ep001"
      }
    }
  },
  "qc_notes": [
    { "rev": 1, "by": "agy", "note": "auto-compiled from production_state.json after QC-2" }
  ]
}
```

**關鍵設計重點說明**：
- **L-cut / J-cut 顯式建模**：在 `audio_tracks.dialogue[]` 以 `cut_style`（`sync` / `j_cut` / `l_cut`）＋ `lead_in_sec`（J-cut 聲音提前進前鏡的秒數）＋ `tail_over_sec`（L-cut 聲音延入下鏡的秒數）＋ 實際 `timeline_start_sec`（含 `offset_ms` 微調）雙重記錄；`ffmpeg` 執行時只看最終計算好的 `timeline_start_sec + offset_ms/1000`，而 `cut_style`/`lead_in_sec`/`tail_over_sec` 讓 Muse 審查與預檢驗證器一眼讀懂剪輯意圖並檢核不超出相鄰鏡邊界。
- **乾淨母帶強制雙出（`emit_clean_master: true`）**：編譯器採**兩段式渲染**——Stage 6-A 只讀 `video_track`＋`audio_tracks` 產出 `master_clean.mp4`；Stage 6-B 以 `master_clean.mp4` 為輸入疊加 `overlays`（`card_overlays`、`fact_hud`、`subtitles`、`end_card`）產出 `master_9x16_rc{N}.mp4`。未來換簡中或調整字體僅重跑 Stage 6-B（<20 秒）。
- **預留卡片渲染器切換插槽**：`card_overlays[].renderer` 與 `end_card.renderer` 枚舉為 `"pillow_ffmpeg" | "hyperframes"`，Phase 5 遷移 Truth Ledger 卡時只需改此欄與預先產出卡片檔，組裝器本體零大改。
- **預留導演層後製勾子**：`video_track[].post_fx[]` 採封閉類型列表（如 `focus_hunt_gblur`、`handheld_micro_shake`、`glitch_in`、`light_flicker`），與 `DIRECTOR_LAYER_AGY_MEMO.md` 提案的 `post_ffmpeg` 補救路徑無縫對接。

#### 4. `ffmpeg` 渲染器的 8 大失敗模式與驗證法

| # | 失敗模式 | 根因 | 預檢（Pre-Flight Validator）與渲染防呆 | 後驗（Post-Render Check） |
| :--- | :--- | :--- | :--- | :--- |
| **F1** | `xfade` 崩潰或影音緩慢漂移 | Veo（24fps）、H3（24fps）、Wan（16/24fps）、圖卡（30fps）的 `time_base`/FPS/SAR 不一致 | 每條視訊入濾鏡前強制統一：`fps=30,scale=1080:1920:...:flags=lanczos,crop=1080:1920,setsar=1,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS` | `ffprobe` 驗成片總長與預期總長差 **≤ ±0.05s**、恆定 30fps |
| **F2** | `xfade` 重疊導致字幕／角標／音軌集體前移 | 每個 `dissolve`（時長 $d$）會使總片長縮短 $d$，若未扣減會造成累加錯位 | 預檢強制驗算 `timeline_start_sec[i] == timeline_start_sec[i-1] + duration_sec[i-1] - transition_in[i].duration_sec`，不符直接中止 | 抽檢轉場後首句字幕與音檔起聲時間差 |
| **F3** | 無音軌片段造成 `concat`/`amix` 失敗 | Wan/LTX/圖卡常無音訊串流 | 視訊主軌完全不帶音訊合併；音訊以 `anullsrc` 48kHz 立體聲底床＋每段 `adelay`＋`amix=normalize=0` 獨立混音 | `ffprobe` 驗成片具 `1 video + 1 stereo 48kHz audio` |
| **F4** | `amix` 音量莫名減半或單次 `loudnorm` 呼吸抽吸 | `amix` 預設 `normalize=1` 會除以軌數；單 pass `loudnorm` 在靜音開場後拉爆底噪 | 鎖死 `amix=inputs=N:duration=longest:dropout_transition=0:normalize=0`；全片採 **two-pass `loudnorm`** 並於對白軌對 BGM/環境聲掛 `sidechaincompress` | 跑 `ffmpeg -af ebur128` 驗整合響度 **`-14.0 ± 1.0 LUFS`**、True Peak **`≤ -1.0 dBTP`** |
| **F5** | 超長指令爆 `ARG_MAX` 或 16GB VM 記憶體 OOM | 20+ 鏡單次超大 `filter_complex` 緩衝過多解碼影格 | 永遠走 `-filter_complex_script graph.txt`（不拼超長 CLI）；採**兩段式渲染**（先拼 `master_clean.mp4` 再疊 `overlays`），必要時每 8–10 鏡分段輸出無損/高碼率中間檔 | 監控渲染退碼 `0` 與峰值 RSS；驗證無殘留 tmp 檔爆 40GB 碟 |
| **F6** | 裁切越界或負延遲（J-cut 於 t=0） | `source_out_sec > 實檔秒數` 或 `timeline_start_sec + offset_ms/1000 < 0` | 預檢逐筆比對 `ffprobe` 實長，強制 `0 <= source_in_sec < source_out_sec <= probe_dur - 0.02` 且所有音軌實算起點 `>= 0` | 檢查 `ffmpeg` stderr 不含 `Invalid duration` / `Past duration too large` |
| **F7** | 原生人聲漏音造成雙重人聲殘影 | 誤把帶台詞提示的 Veo/H3 鏡原音接進 `ambience` | 預檢跨查 `script_pack.json`：凡 `voice_mode == "tts"` 之鏡，禁止 `ambience` 採 `native_clip_audio`（除非顯式設 `native_voice_verified_clean: true`） | QC-3 關字幕盲聽抽檢對白鏡起迄點 |
| **F8** | 繁中字體靜默退回醜字或豆腐塊（`□□□`） | 本機尚缺 `Noto Sans TC`，libass 靜默退回 `WenQuanYi` 或缺字 | 預檢呼叫 `fc-match "Noto Sans TC"` 確認字體實際命中（未安裝直接告警阻斷），並檢查 `.ass` UTF-8 BOM 與安全區邊界 | 自動抽取 4 張關鍵驗證幀（首字幕、各 HUD 切換、證據卡、片尾 Truth Ledger）輸出聯絡表供 QC-3 目視簽核 |

---

### Q2：`faster-whisper` 掛點與 VM CPU 成本估算

#### 1. 掛點評估矩陣（明確區分「值」與「不值」）

| 候選掛點 | 判定 | 工程理由（對齊 DESIGN v1.3/v1.4 聲音策略） | 建議引擎／替代方案 |
| :--- | :--- | :--- | :--- |
| **① 時事線／常線對標影片與新聞素材拆解逐字稿** | **✅ 最值（主要掛點）** | 外部新聞、訪談、對標短劇沒有現成劇本；轉出含時間戳逐字稿可大幅加速上游拆解鉤子節奏、擷取 FACT 原話與時間戳來源。 | VM 跑 `faster-whisper` **`large-v3-turbo` int8**（遇大量中英財經詞或重口音再切 `large-v3`；若單支 >15 分鐘改送 Colab L4 幾秒跑完）。 |
| **② TTS 與口型時差量測（估計 `audio_offset_ms` 進 `edit_manifest.json`）** | **⚠️ 有限條件導入（只掛入選 `LIP_SENSITIVE` 鏡，不掛全抽卡）** | **核心技術澄清**：Whisper **看不到嘴唇**，只能把「生成片原生音訊的說話區間」當作「畫面開口時間」的代理指標去對比 `audio_tts/*.wav`。① 若只量起迄時間差（算 `audio_offset_ms`），**`Silero VAD` 或 `ffmpeg silencedetect` 只要 <2 秒**，且無 Whisper DTW ±100–300ms 字級抖動；② Whisper 僅在 `LIP_SENSITIVE` 正臉近景入選鏡（約 4–6 鏡）有額外價值：用來驗證生成片原生說話是否「唸完該句長度」（排除中途閉嘴或亂唸多字）並標記 `LIP_DRIFT_SUSPECT` 給 Muse。 | **兩層配合**：全對白入選鏡先跑 `VAD / silencedetect`（<2 秒）算初值 `audio_offset_ms`；僅對 `LIP_SENSITIVE` 入選鏡（~25–35 秒音訊）加掛 `faster-whisper` `large-v3-turbo` 覆檢。 |
| **③ 正式 TTS 音檔（`audio_tts/*.wav`）轉寫取時間戳驅動 `.ass` 字幕切句** | **🟡 僅列備援（ElevenLabs 主力不需掛 Whisper）** | `DESIGN.md` §5.1 現行以字數比例（char-weighted）切分單鏡多段字幕，遇停頓易漂移。但 **ElevenLabs API 原生提供 `/with-timestamps` 端點**，生成語音當下即可**零額外 CPU、毫秒級**拿回字元對齊時間戳！只有未來切換至無內建字元時間戳的備援 TTS（CosyVoice 3 等）時，才需要用 `faster-whisper` 補字級時間戳。 | **首選**：Phase 5 `tts_batch_runner.py` 改呼 ElevenLabs `/with-timestamps`（0 VM CPU）；`faster-whisper` 僅作備援 TTS 對齊工具。 |
| **④ 生成片全部抽卡候選（QC-2 約 39 takes）原生音訊轉寫驗對白內容** | **❌ 不值得（明確淘汰）** | ① DESIGN v1.3 已拍板**對白 100% 用 TTS、組裝時捨棄原生人聲**——驗證原生人聲唸得對不對是在驗「會被丟進垃圾桶的音軌」；② Veo/H3 偶有原生口齒含糊但口型節奏完全可用的好畫面，用 ASR 篩片反而誤殺；③ 39 條抽卡 ≈ 3.6 分鐘音訊，在 2 核 VM 跑 `large-v3` 會吃滿 CPU **9–14 分鐘**，拖慢互動挑片。 | **不掛**；QC-2 技術初篩維持 `ffprobe`＋`freezedetect`＋`volumedetect`。 |
| **⑤ 用 `faster-whisper` 驗 ElevenLabs TTS 台灣讀音（如「范蠡 ㄌㄧˇ」「垃圾」）** | **❌ 不值得（明確淘汰／假安全感）** | Whisper 語意解碼器會把誤讀的 `ㄌㄧˋ` 或大陸音 `ㄌㄚ ㄐㄧ` 自動修成正字「范蠡」「垃圾」，完全抓不到讀音漂移。 | **不掛**；維持 `bible/voices/*.yaml` 人工盲聽四詞驗收＋`pronunciation_rules`。 |
| **⑥ 快線（3.5 小時 SLA）強制全集跑 `large-v3`** | **❌ 不值得（明確淘汰）** | 2 核無 GPU VM 滿載會與 `ffmpeg` 搶資源並吃掉 15–25 分鐘黃金時效。 | 快線預設跳過片內 Whisper；外部新聞片若需轉寫一律鎖 **`large-v3-turbo` int8**（或直轉 Colab）。 |

#### 2. VM CPU 每集成本估算（Intel Xeon 2.20GHz，2 實體核 / 4 vCPU，AVX2，`int8`，含 `word_timestamps=True`）

> 基準假設（對齊 `DESIGN.md` §8.2 常線 2 分鐘 / 20 鏡）：① `large-v3` int8 含 word timestamps **RTF ≈ 2.5–4.0×**；② `large-v3-turbo` int8 含 word timestamps **RTF ≈ 0.6–1.2×**；③ 每次模型冷載入約 +5–10 秒（批次單進程共用模型即可攤平）。

| 使用場景（每集音訊總量） | `large-v3` int8 耗時（分鐘／集） | `large-v3-turbo` int8 耗時（分鐘／集） | 建議採用 |
| :--- | :---: | :---: | :--- |
| **A. 僅片內 `LIP_SENSITIVE` 入選鏡**（5 鏡 × 5s ≈ **25 秒**） | **1.0 – 1.7 分鐘** | **0.3 – 0.5 分鐘** | **✅ 推薦（Phase 5 預設）** |
| **B. 全部入選對白鏡（13 鏡 ≈ 70 秒）** | **2.9 – 4.7 分鐘** | **0.7 – 1.4 分鐘** | 可選（僅當需全鏡時序校核） |
| **C. 備援：正式 TTS 音檔轉時間戳（≈ 90 秒）** | **3.8 – 6.0 分鐘** | **0.9 – 1.8 分鐘** | 僅備援（ElevenLabs 用 `/with-timestamps` = **0 分鐘**） |
| **D. 外部對標／時事參考影片逐字稿（1–2 支，共 5 分鐘）** | **12.5 – 20.0 分鐘** | **3.0 – 6.0 分鐘** | **✅ 推薦（按需觸發，預設 turbo）** |
| **⚠️ 反面示範：誤掛全部 39 條抽卡原生音訊（≈ 215 秒）** | **9.0 – 14.3 分鐘** | **2.2 – 4.3 分鐘** | **❌ 禁止掛載（白燒 CPU）** |
| **★ 推薦組合合計（A ＋ D，約 5.5 分鐘音訊／集）** | **~13.5 – 22 分鐘／集** | **~3.3 – 6.5 分鐘／集** | **單一推薦：VM 預設 `large-v3-turbo` int8（~3.5–6.5 分／集）**；僅重度中英夾雜參考片手切 `large-v3` |

> **工程落地備忘**：模型檔磁碟佔用——`large-v3-turbo` int8 約 **~0.8–1.0GB**、`large-v3` int8 約 **~1.6–1.8GB**（存放於 VM 本地快取，不進 Git，佔 40GB 可用碟 <5%）。

---

### Q3：卡片渲染升級路徑（HyperFrames vs Remotion vs 維持 ffmpeg）

#### 1. 單一決策：**Phase 3–4 維持 `Pillow + ffmpeg`；Phase 5 條件式升級唯一選擇 `HyperFrames`（淘汰 `Remotion`）**

**為何二選一鎖定 `HyperFrames` 而非 `Remotion`？**
1. **授權零隱患（決定性勝出）**：HyperFrames 採 **Apache-2.0**，永久免費商用、不限人數與渲染次數。Remotion 雖然目前 ≤3 人免費，但一旦《第二次文明》擴編至 4 人以上（含兼職剪輯／外包設計）或部署為自動化批次渲染管線，即觸發 Company License（Automators `$100/月起 ＋ $0.01/次`）；兩套系統前期都要花相同的環境建置成本，沒有理由把核心模板綁在有規模懸崖的授權上。
2. **更貼合 AI Agent 產線與單檔維護**：HyperFrames 直接寫標準 HTML＋CSS＋GSAP（單檔或極簡資料夾），`agy` 與 Muse 不必維護 React/TypeScript/Webpack 套件地獄，且任何模板檔在 Creator 本機瀏覽器點開即可即時看排版。
3. **無頭 VM 環境隔離最乾淨**：本 VM 目前為 Debian 12 ＋ `Node v18.20.4` ＋ 無 Chromium ＋ 無 `Noto Sans TC`，但**已預裝 Docker**。HyperFrames 官方原生支援 `npx hyperframes render --docker`（容器內固定 Node 22＋Pinned Chromium＋`fonts-noto-cjk`），完全不汙染宿主 VM、不受 Node 18 限制，且符合 DESIGN §6.1「90 天可拋棄 VM 無痛遷移」原則（重拉同一 Docker image 即可 100% 像素復現）。

#### 2. 維持 `Pillow + ffmpeg`（不升級）的明確條件
以下任一條件成立時，**不遷移至 HyperFrames（維持減法紀律）**：
- **Phase 3–4（EP-01～EP-03，30 天市場驗證期間）**：一律維持 `Pillow + ffmpeg`（**唯獨建議立即補裝免費的 `fonts-noto-cjk` / `Noto Sans TC` 字體**，解決目前僅有文泉驛正黑的質感上限，0 架構改動）。
- **Phase 5 驗證門檻未觸發**：若 EP-01～EP-03 市場復盤顯示，以 `Pillow` 高清排版圖＋`Noto Sans TC`＋`ffmpeg` 2.5D Ken Burns／淡入淡出製作的證據卡與 Truth Ledger 卡，在 3 秒完播留存與「紀錄片高級感」體感上已達標，且每集無須複雜動態圖表（折線成長動畫、時間軸逐點點亮、數據跳動計數），則**永久停留在 `Pillow + ffmpeg`**，不為技術美感硬加 2GB Chromium 容器依賴。

#### 3. 遷移時機與最小遷移路徑（Phase 5 觸發時）
- **遷移時機**：**Phase 5（EP-03 與 30 天市場驗證復盤之後）**，絕不在現在（開拍前）或 EP-01 剛跑完就動工（嚴守 ADR-002）。
- **最小遷移路徑（單卡切入、漸進驗證）**：
  1. **Step 1（先且僅先遷 1 張卡）：片尾 3.5 秒「Truth Ledger 事實分層聲明卡」**
     - *原因*：① 結構 100% 固定（`fact_anchors[]` 條列＋四色分層圖例＋免責聲明＋Personal Lab 網址），1 份 HTML 模板套用全系列每一集，複用率最高；② 固定接在全片最尾端，**無須與主畫面做透明疊加或口型同步**，工程耦合度為零；③ 每集僅渲染 1 張 3.5 秒（105 幀，預估 10–20 秒），對 4 vCPU VM 壓力極小；④ `edit_manifest.json` 的 `end_card.renderer` 直接由 `"pillow_ffmpeg"` 切為 `"hyperframes"` 即可完成無縫對接並做 A/B 視覺檢核。
  2. **Step 2（Step 1 實測渲染 <30 秒且質感顯著提升後再擴）**：升級全屏 `evidence_card`（`fullscreen_card`：新聞截圖高亮標註、財報條形/折線動畫、多事件時間軸推進）。
  3. **永不遷移（留 `ffmpeg`/`libass`）**：左上角 `fact_hud` 角標（`corner_badge`）與全片繁中字幕（`.ass`）——單純為了小角標開 Chromium 吐透明 Alpha 影片（耗時暴增 2–3.5×）純屬過度工程。

---

### Q4：其餘 9 項工具處置確認（對齊減法紀律與 ADR-002）

| 工具 | 授權 | 處置 | 一句話理由 |
| :--- | :--- | :---: | :--- |
| **`auto-editor`** | The Unlicense | **淘汰** | 本劇每鏡淨長由 TTS 實測秒數與戲劇留白（`reaction_hold_sec`）精控，自動剪無聲會破壞節奏與頭尾 0.5s 家規，單句頭尾修剪用既有 `ffmpeg silenceremove` 已足。 |
| **`MoviePy`** | MIT | **淘汰** | 在 Python 之上再套一層 FFmpeg 封裝只增加記憶體拷貝與除錯黑箱，遠不如 `drama_assembler.py` 直接由 `edit_manifest.json` 編譯確定性 `ffmpeg filter_complex_script` 穩定透明。 |
| **`Piper`** (`OHF-Voice/piper1-gpl`) | GPL-3.0 | **淘汰** | 聲音策略已於 DESIGN v1.3 定案鎖定 ElevenLabs v4 主力＋三層商用備援梯隊，Piper 缺台灣國語自然度與戲劇演技控制且新版採 GPL-3.0，不重複造輪。 |
| **`Openverse`** | CC / PD 搜尋 API | **列備援** | 僅作偶發無人物歷史／財經公開領域輔助圖音素材的**人工檢索備援**（須逐筆核對 CC0/CC-BY 授權與出處），Phase 3–4 不接入自動化主鏈，防法務與審核膨脹。 |
| **`Impeccable`** (`pbakaus/impeccable`) | Apache-2.0 | **列備援** | 定位為前端 UI 設計審查詞彙，Phase 3–4 無前端頁面且卡片走 `Pillow + ffmpeg` 不必安裝；待 Phase 5 若啟用 HyperFrames 寫 HTML 證據卡時，再借鏡其去 AI 味審查清單即可。 |
| **`Chrome DevTools MCP`** | Apache-2.0 | **淘汰** | 本機 VM 無 Chromium 且依 ADR-002 不建大型 Web 後台；即便 Phase 5 用 Docker 跑 HyperFrames 卡片，也以無頭抽幀圖片做 QC 即可，不需引入瀏覽器即時 MCP 控制面。 |
| **`WeftCut`** (`WeftCut/WeftCut`) | MIT | **淘汰** | 雖跨平台支援 Linux＋MCP，但本質是圖形化桌面 NLE 剪輯器，無法在無頭無 GPU VM 取代確定性 CLI 批次封裝，且與 `script_pack`／`production_state` 契約重疊造輪。 |
| **`Pireel`** (`pireel/pireel`) | AGPL-3.0（外掛 Apache-2.0） | **淘汰** | 偏向瀏覽器口播型畫布剪輯器，不符合本劇多鏡劇情短劇與無頭 VM 批次封裝架構，且核心採 AGPL-3.0 較無導入誘因。 |
| **`Editroom`** (`robbietilton/Editroom`) | MIT | **淘汰** | 僅支援 macOS Apple Silicon，與我方 Debian 12 Linux x86_64 無頭 VM 執行環境完全不相容，直接排除。 |

---

## 三、併入 DESIGN v1.5 的落地切分（對齊 ADR-002）

| 階段 | 建議納入範圍（僅規格定案，本回合未動實作） |
| :--- | :--- |
| **DESIGN v1.5 規格升版（立即併入文件）** | ① §1.2／§5.1／§6.2 將原 `edl.json` 正式定名為 **`plan/edit_manifest.json`**，併入本備忘錄 Schema v1.0、三檔分責表與 FFmpeg 8 大預檢／後驗規則；<br>② §5.1 增列 `faster-whisper`（預設 `large-v3-turbo` int8）作為 **Phase 5 P1 輔助工具**並明文載明「禁用於全抽卡原音與台灣讀音驗收」紅線，同時於 `tts_batch_runner.py` 規格註記優先採用 ElevenLabs `/with-timestamps`；<br>③ §2.3／§5.1 `fact_card_renderer.py` 註記「Phase 3–4 走 `Pillow + ffmpeg`（須補裝 `Noto Sans TC`）、Phase 5 條件式升級唯一候選為 `HyperFrames`（Docker 隔離，先遷 Truth Ledger 卡），淘汰 Remotion」。 |
| **Phase 3（EP-01 半自動跑通）** | 不裝 Whisper、不裝 HyperFrames、不建整套 `manifest_builder.py`；僅依本 Schema 精簡填寫 EP-01 組裝清單交單次兩段式 `ffmpeg` 執行，並於環境整備時補裝 `fonts-noto-cjk` 確保繁中字體美觀。 |
| **Phase 5（EP-03 市場驗證後）** | ① 實作 `manifest_builder.py`＋`drama_assembler.py` 兩段式渲染與 8 項自動預檢；<br>② 啟用 `tts_batch_runner.py` 之 ElevenLabs `/with-timestamps`；<br>③ 實測 `faster-whisper` (`large-v3-turbo` int8) 30 秒冒煙基準後上線「對標影片逐字稿＋`LIP_SENSITIVE` 輔助校對」；<br>④ 依 EP-03 留存復盤決定是否觸發 `HyperFrames --docker` 遷移片尾 Truth Ledger 卡（先做單卡耗時／RAM 冒煙測試）。 |
