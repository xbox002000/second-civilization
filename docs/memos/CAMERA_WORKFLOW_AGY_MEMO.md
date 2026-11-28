# 運鏡控制工作流定案討論備忘錄（agy 工程查證與推薦方案）

> **文件定位**：只讀查證與工作流收斂備忘錄（不改 `STORYBOARD-SPEC-V2.md` 與 `DESIGN.md` 本體、不安裝任何套件、不 clone 進 skills、不 push）  
> **撰寫日期**：2026-11-27  
> **依據材料**：`H3-CAMERA-CONTROL-REF.md`、`CLAY-PREVIS-TOOLS-REF.md`、`STORYBOARD-SPEC-V2.md`（v2.0 FINAL）、`DESIGN.md`（v1.4）、`DRYRUN-EP01-v0.3.1-BLIND.md`、`STORYBOARD_SPEC_V2_AGY_MEMO.md`  
> **實查來源（全只讀）**：Hugging Face `MiniMaxAI/MiniMax-H3` 官方指南原文（`VIDEO_PROMPT_WRITING_GUIDE_base_en.md`、`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`）、GitHub `MiniMax-AI/MiniMax-H3`（`README.md` 與 `skills/h3-prompt-writing/SKILL.md`）、本機 `comfy-colab-kit` 閘道（`localhost:8080/_gate/status` 與 `/_gate/profiles`，v0.6.0，未喚醒 GPU）及其上游 `FireTable/comfy-colab-kit` 之 `minimax-h3-video` 完整 `profile.yaml` 與工作流 JSON、以及 4 個預演工具＋2 包社群 skill＋`h3lite` 線上只讀稽核。

---

## 一、核心結論（單一推薦方案先亮底牌）

**我方唯一推薦工作流為「四級分層運鏡 × 減法鎖定」**：
- **L1 詞表提示詞（預設主力，65–75% 鏡）**：日常對白、微推拉、鎖機、跟拍一律靠結構化欄位自動衍生**引擎專屬方言**（H3 改走官方三段式／Ref2VA 六段式，Flow 維持電影敘事句，Wan 維持精煉物理動作句）。
- **L2 首尾幀差分（例外級，5–10% 鏡）**：僅用於單調起迄收斂或 Match Cut；待 `comfy-colab-kit` H3 `last_frame` 與 `gflow veo-lite -e` 冒煙驗證通過後始轉常規。
- **L3 白膜預演＋Ref2VA（精準導演級，嚴限每集 0–2 顆 Hero 複雜運鏡，≤10%）**：**單一預設工具定版為 `CozyClay`**（Phase 3 先用 `cozyclay.org/#try` 瀏覽器零安裝試跑；Phase 5 才於 VM 接 `npx cozyclay` ＋ 27 工具 MCP 供 agy 操作，且強制關閉匿名遙測與自動更新）。閘道端**不建新 profile**，僅於既有 `minimax-h3-video` 補一支 4 節點自組工作流 JSON（把 `LoadVideo → GetVideoComponents → ImageScaleToTotalPixels` 接上已存在的 `MiniMaxH3ReferenceToVideo.ref_videos.ref_video_0`），並以已預裝的 **`h3-controlnet`（Depth/Canny）** 作為防灰模材質滲漏雙保險。
- **L4 後製運鏡（CPU `ffmpeg`，15–20% 鏡）**：所有 2.5D 圖卡、新聞證據卡、微幅數碼慢推與 `crash zoom` 後製變速全交 VM CPU，0 GPU、100% 過稿。
- **不導入 Wan 參數化運鏡（Fun-Camera／Uni3C）**、不裝 Blender、不建雙預演工具並行維護，完全對齊減法紀律與 ADR-002。

---

## 二、查證結果與差異清單（對照 Creator 彙整）

### 2.1 MiniMax 官方 H3 提示詞指南核實

對照 Hugging Face `MiniMaxAI/MiniMax-H3/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`（15,736 bytes）、`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`（23,552 bytes）、`MiniMax-AI/MiniMax-H3/README.md` 與 `skills/h3-prompt-writing/SKILL.md`（2,619 bytes），核實結果如下：

1. **官方詞表（完全確認：12 類原語／20 個具體詞）**：
   - 機身不動類：`Zoom In / Zoom Out`、`Pan Left / Pan Right`、`Tilt Up / Tilt Down`。
   - 整機移動類：`Push In / Pull Out`、`Truck Left / Truck Right`、`Pedestal Up / Pedestal Down`、`Arc Shot`、`Tracking Shot`。
   - 機身狀態與視角：`Static Shot`、`Shake Slightly / Shake Strongly`、`POV`、`Roll Clockwise / Roll Counterclockwise`。
2. **幅度／速度寫法（完全確認）**：
   - 公式：`Motion Type + Amplitude + Speed`，中幅常速預設省略，僅有意義時加上：
     - Amplitude：`with small amplitude` / `with large amplitude`
     - Speed：`at slow speed` / `at fast speed`
   - 須自然寫進英文動作句，禁堆疊於句尾作標籤。Creator 彙整中的範例句 `The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.` 與官方文件 **逐字吻合**。
3. **三段式 vs Ref2VA 六段式結構（發現重大遺漏與差異）**：
   - **Base 模式（T2VA / I2VA / FL2VA / L2VA）**：除 T2VA 外，前面都**強制有一行 Part One 對齊指令＋一個空行**，才接三個核心欄（`integrated_multimodal_description`、`overall_soundscape`、`non_diegetic_music`）。
     - I2VA 固定首行：`For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
     - FL2VA 固定首行：`How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.`（`S.SS` 嚴格為兩位小數）。
   - **Ref2VA 全參考模式**：為嚴格**六段式**（不可混用三段式）：`subject_definitions` → `summary`（必以 `[reference generation]` 等方括號任務前綴開頭）→ `retention_analysis`（固定英文狀態值：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`）→ `detailed_description`（注意欄位名**不是** `integrated_multimodal_description`，且整體風格句必須寫在 `[Shot 1]` **之前**）→ `overall_soundscape` → `non_diegetic_music`。
4. **參考影片與輸出限制（官方規格核實）**：
   - **Ref2VA 輸入上限**：參考圖 ≤ 9 張（單張 ≤ 30 MB，JPG/PNG/WEBP/HEIC）；**參考影片 ≤ 3 支，單支 2–15 秒，全部參考影片總時長 ≤ 15 秒**（單支 ≤ 50 MB，MP4/MOV，H.264/AVC 或 H.265/HEVC）；參考音訊 ≤ 3 支（單支 2–15 秒，總長 ≤ 15 秒，≤ 15 MB，WAV/MP3）；混合輸入總檔數 ≤ 12 檔。
   - **輸出規格**：時長 **4–15 秒整數秒**、**24 FPS**（內部對齊 17-frame 時間網格）、預設短邊 768px（明確支援 **9:16**、16:9、3:4 等）、32 kHz 立體聲。
   - **本機 ComfyUI 端額外限制**：開源權重透過 `comfy-colab-kit` 跑本地節點，無 50 MB API 傳輸上限，改受 **GPU VRAM 與「參考影片幀數 × 解析度」乘積**約束（L4 24GB 須壓低參考影片解析度以防 VAE encode OOM）。
5. **官方 `h3-prompt-writing` skill 查核**：
   - 純 Markdown＋`references/base-en.txt`、`ref-en.txt`，**零外部 API 呼叫、無可疑程式**（`agents/openai.yaml` 僅為可選 UI metadata；但同 repo 其餘 8 個風格 skill 綁定 MiniMax Hub 不可攜）。
   - 授權注意：GitHub `MiniMax-AI/MiniMax-H3` 根目錄**無獨立開源 LICENSE 檔**，整體依 `MiniMax H3 Community License` 規範。

#### 與 Creator 彙整（`H3-CAMERA-CONTROL-REF.md`／`CLAY-PREVIS-TOOLS-REF.md`）不符或遺漏之處

| # | Creator 彙整說法 | 官方文件／實查真相 | 對我方產線影響 |
| :-: | :--- | :--- | :--- |
| **1** | 僅寫三段式結構，未提 Part One 對齊指令行 | I2VA／FL2VA／L2VA **第一行強制要有 `<Picture N>` 對齊指令＋空行**，否則首尾幀對齊弱化 | H3 衍生模板必須自動補入首行指令，且 FL2VA 秒數須為兩位小數 `S.SS` |
| **2** | 第 2 節稱白膜提示詞明示 `"Follow the composition, subject positions, camera path and timing of <Video 1> exactly, frame by frame. Replace materials with ..."` | 此句**非官方指南原文**，屬社群（Stage／Mickmumpitz）實務句式；官方 Ref2VA 要求六段式並於 `retention_analysis` 用固定標記聲明 `<Video 1>` 的保留關係 | L3 應走官方 Ref2VA 六段式骨架，將該社群句作為 `retention_analysis` 與 `detailed_description` 的語意強化，而非單句裸貼 |
| **3** | 稱「每鏡只寫一次主要運鏡」為官方規則 | 官方指南**未設此硬規**（反而支援單次生成多鏡切分 `[Shot 2] At 00:03.500...`）；「每鏡一運鏡」是社群實測收斂與我方 V6 家規 | 維持我方 V6 硬閘不變，但歸因須標明為「我方規則＋社群經驗」而非官方限制 |
| **4** | 漏提官方對白、畫外音閉唇與 `non_diegetic_music` 規範 | 官方明訂：① 畫外音必寫 `says in an off-screen voiceover: <d>[Chinese] ...</d> while his lips remain completely closed.`；② `non_diegetic_music` 禁抽象情緒詞，無配樂必寫 **`N/A`** | **極關鍵**：完美解決 S16b 閉眼畫外音誤張嘴問題；且全線 H3 強制寫 `non_diegetic_music: N/A` 防原片亂生配樂汙染音軌 |
| **5** | `CLAY-PREVIS-TOOLS-REF.md` 將 **`h3lite`** 歸類為「Blender 白膜＋H3 Ref2VA 工作流」 | 實查 `Rimagination/h3lite`（529 stars，MIT）實為「**本地 ComfyUI 硬體感知 H3 生成 Codex skill**」，**不是** Blender 白膜預演工具 | 移除於預演工具候選名單，避免誤導選型 |

---

### 2.2 白膜預演工具只讀評估表（含安全與夾帶稽核）

| 工具（Repo） | 運行方式與硬體需求 | 匯出物與 9:16 支援 | 授權 | 維護活躍度（2026-11-27 實查） | Agent 可操作性 | 安全／可疑夾帶稽核 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CozyClay**<br>`HaD0Yun/CozyClay` | 純瀏覽器（官網 `cozyclay.org/#try` 零安裝）或本機 `npx cozyclay`（Node 22.19+、Chromium，**0 GPU**） | **全套齊全**：Greybox MP4、**首尾幀 PNG**、**Depth/Normal pass**、Prompt、Contact Sheet、OTIO；原生支援 **9:16** | **AGPL-3.0-or-later**<br>（內部使用產出影片**零傳染**；僅對外架設修改版服務需開源） | **極高**<br>2,090 stars／224 forks；v3.3.3；最後 push **2026-11-27** | **極高（全場唯一）**<br>內建 **27 工具 MCP Server**＋`cclay live` CLI；無頭模式可直接擺場/定機位/生 prompt，截圖與出片接 Chromium | **無惡意程式，但有 2 項須顯式關閉**：<br>① 含 `posthog-js` 匿名遙測（`t.cozyclay.org`，`before_send` 已剝除文字與路徑，可用 `cclay telemetry off` 徹底關閉）；<br>② 預設檢查更新（可用 `cclay update --off` 或 `COZYCLAY_NO_UPDATE_CHECK=1` 關閉）；另含選用 Agent panel SDK（不登入免用） |
| **Stage**<br>`aledige63/Stage` | 純前端 SPA（`aledige63.github.io/Stage/` 零安裝，須 Chrome/Edge WebCodecs）或本機 `npm run dev`（Node 20+，**0 GPU**） | **H.264 MP4**（720p/1080p，可帶**靜音 AAC 音軌**）＋ **MiniMax Compiler / Ref2VA 英文 Prompt** ＋ `.stage.json`；支援 **9:16**；**無**首尾幀包與 Depth 通道 | **MIT** | **極早期／個人維運**<br>僅 **1 star**／3 forks；v0.9.0；建於 2026-10-17，最後 push 2026-11-26 | **低**<br>**無 MCP、無 CLI**；僅能人工瀏覽器操作（或由 agent 逆向拼 `.stage.json` 再開瀏覽器手動匯出） | **最乾淨**：僅 5 個 runtime 依賴（`mp4-muxer`、`react`、`react-dom`、`three`、`zustand`），**零遙測、零外部 API、無可疑夾帶** |
| **CodeVideoModel**<br>`code-video-model/CodeVideoModel` | Python + Conda + PyTorch CUDA 12.6 + Playwright Chromium；Previs 半段（`generate_threejs` + `render.py`）技術上可獨立跑無頭瀏覽器出 proxy MP4，但**硬綁 GPT-6 / OpenRouter API** | Three.js 程式碼＋低模 Proxy MP4（預設 **16:9 `1536×864`**）＋ GPT-Image-2 首幀 | **Apache-2.0**（範例素材 CC-BY-4.0） | **中高（研究型）**<br>796 stars／37 forks；最後 push 2026-10-13（Microsoft Research） | **中（CLI）**<br>有 Python CLI，但需外部付費 LLM API（OpenRouter GPT-6）反覆視覺迭代 | **無可疑夾帶**，但會將劇本提示詞送往外部 OpenRouter/GPT API，且重度綁定 Conda 與 CUDA 堆疊 |
| **ComfyUI-Soundstage**<br>`theboord/ComfyUI-Soundstage` | ComfyUI 0.39–0.44 Custom Node＋App（需常駐本地/RunPod GPU ComfyUI 實例） | 內建 3D 擺場直出 **FLUX 3 Klein**（首幀）＋ **LTX-2.5**（影＋音）＋時間軸／AAF；**非針對 H3** | **MIT**（但預設模型 **FLUX 3 Klein 為非商用授權**） | **早期比賽專案**<br>7 stars／1 fork；v0.1.0；最後 push 2026-11-10（`#OpenSourceHiggsfield`） | **低（綁 ComfyUI UI）**<br>無法配合休眠式 `comfy-colab-kit` 閘道 | **無可疑夾帶**，但為取代整條產線的巨型單體工作台，與我方架構與商用授權雙重衝突 |
| **Blender ＋ Mickmumpitz** | 本機 3D DCC 軟體（高學習門檻）＋ ComfyUI 灰模工作流 | 任意白膜／Depth／Normal MP4；9:16 需手動設 | GPL-3.0 | 工業標準（但需專職 3D 人力） | 僅能靠 `bpy` 腳本硬寫（維護成本高） | 無可疑夾帶；與我方「不要求 Creator 學 Blender」直接相違 |

---

### 2.3 社群 Skill 兩包只讀評估（實測可信度與授權）

| Skill 專案 | 規模與活躍度 | 授權 | 安全稽核 | 實測標註可信度與我方採納建議 |
| :--- | :--- | :---: | :--- | :--- |
| **`loopforge0/minimaxh3-shots-skills`** | 23 stars／6 forks；最後 push 2026-10-27；涵蓋 **29 種 named shots**（Part 1: 14＋Part 2: 15） | **MIT**（可安全商用改寫） | **乾淨**：`build_prompt.py` 與 `snap.py` 僅用 Python 標準庫＋`ffmpeg`，無外部遙測或網路夾帶 | **可信度：高（透明誠實）**。附公開成片庫與完整 prompt，老實區分「一次過／2–3 輪過／仍不完美／做不到（bullet time）」，且在程式註解誠實聲明「僅人眼驗證人物主體，非人物詞表屬推演未測」。**建議：不安裝整包，僅合法借鏡其 MIT 英文實證句式與 `snap.py` 後製急推概念，收斂進我方 `bible/camera/named_shots.yaml`**。 |
| **`swan7-py/MiniMax-H3-Skills-Local`**<br>（`h3-camera-motion-lib` ＋ `h3-video-prompt-cn`） | 90 stars／8 forks；最後 push 2026-11-24；46 種中文運鏡句＋LoRA 清單 | **無 LICENSE（All Rights Reserved，不可直接複製使用）** | **乾淨**：全純 Markdown 文字，無可執行腳本 | **可信度：中低（不適用我方 profile）**。作者自述四點重大限制：① **每格單樣本單種子**（結論屬初級）；② 實測為**中文 prompt ＋ 864×480 橫屏／4:3**，非我方 **9:16 直式＋官方英文結構**；③ 480P 只看運鏡不看人臉；④ 依賴多包第三方 Camera LoRA。**建議：不裝、不複製句庫；僅參考其「禁用裸否定詞（正向化原則）」與避坑紀錄**。 |

---

## 三、Q1–Q7 逐題答覆

### Q1 分級設計：運鏡分幾級最合理？

採 **四級分層（L1–L4）** 最合理，完全貼合「9:16 直式短劇每集 20 原子鏡、多數對白＋圖卡、複雜運鏡集中於少數 hero 鏡」的內容分佈：

| 分級 | 名稱與定位 | 典型每集佔比（20 鏡） | 適用鏡型 | 成本量級（相對基準） | 典型失敗模式與緩解 |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **L1** | **詞表提示詞（預設主力）** | **65–75%**<br>（13–15 鏡） | 常規對白鏡（鎖機／慢推）、過肩、反應鏡、簡單平搖／微手持、Wan 動作 B-roll | **0 額外預演工時、0 額外圖**（沿用既有抽卡預算 $N=2\text{–}3$） | ① 複合弧線或精確停位失控；② **TriPRISM 8-step 權重可能壓縮運鏡幅度**；③ 大角度轉頭造成左眉尾傷痕／後腦小尾失憶 → *限單鏡一運鏡、轉頭 ±30° 內、嚴守官方詞表* |
| **L2** | **首尾幀差分（`i2v_first_last`）** | **5–10%**<br>（1–2 鏡；**冒煙通過前列例外**） | 起迄構圖必須精準收斂的單調移動、Match Cut（如 S12 燭火轉場）、道具推進定格 | **+1 張尾幀產圖與 QC-1 審核**（Flow 免費產圖 ~1 分鐘；0 預演學習成本） | ① 與家規「頭尾各剪 0.5s」正面衝突（尾幀被剪掉不入片）→ *須設 `trim_policy: tail_only/none` 與 `chain_trim_override`*；② 中段軌跡線性硬拉變形；③ H3 `TriPRISM` 與 `veo-lite -e` 尚未實測驗證 |
| **L3** | **白膜預演＋Ref2VA（精準導演級）** | **≤10%**<br>（嚴限 **0–2 鏡／集**） | 複雜弧線環繞、空間前景遮擋揭示、人物走位與運鏡嚴格同步、跨集／首尾精準同機位呼應（如 S01↔S16b） | **+5–15 分鐘預演工時**（Muse 瀏覽器或 agy MCP）；若切換 20-step 非蒸餾或跑 `h3-controlnet`，單鏡 CU 增 ~20–40% | ① 灰模第一幀與核准寫實首幀機位不齊，導致畫面跳接；② 灰模塑膠質感／地板網格滲漏進成片；③ 8-step 蒸餾權重忽略白膜軌跡 → *首幀依灰模第 0 幀構圖烘焙、備援走 `h3-controlnet` Depth 通道徹底隔絕灰模 RGB* |
| **L4** | **後製運鏡（CPU `ffmpeg`）** | **15–20%**<br>（3–4 鏡） | 所有 `cpu_card` 新聞／財報證據卡（S05、S11b、S20）、微幅數碼慢推（≤12%）、急推 `crash zoom` 後製變速補救（`snap.py` 思路） | **0 GPU、0 Flow 點、固定 $N=1$、100% 過稿** | 無真實 3D 視差（平面縮放感）→ *嚴限圖卡、插入鏡與極小幅補推，禁用於立體環繞或人物空間移動* |

> **快線紀律**：依 `DESIGN.md` §3.3，**快線（2.5–3.5 小時 SLA）全面禁用 L3（僅走 L1＋L4）**，守住時效紅線。

---

### Q2 預演工具定版（單一預設＋落選者一句話死因）

- **我方唯一預設預演工具定版：`CozyClay`（`HaD0Yun/CozyClay`）**。
  - **為何完全對齊我方條件**：
    1. **唯一同時滿足「人類零安裝試用＋Agent 自動化操作」**：Phase 3 半自動期，Muse 與 Creator 直接開 `https://cozyclay.org/#try` 即可在瀏覽器試排（免裝 Blender、免 GPU）；Phase 5 系統化後，VM 上啟 `npx cozyclay`（Node 22.19+）並掛載其 **27 工具 MCP Server／`cclay live` CLI**，由 agy 直接以結構化指令擺場、定機位、吐出幾何規格與灰模片。
    2. **原生 9:16＋一魚三吃匯出物**：原生支援 **9:16 直式畫幅**，且一次匯出 **Greybox MP4（餵 `h3-r2v` `<Video 1>`）＋ 首尾幀 PNG（校準 Stage 3 首幀構圖）＋ Depth/Normal pass（若 `<Video 1>` 滲漏，直接無縫餵閘道已預裝的 `h3-controlnet`！）**。
    3. **維護活躍度與存續風險最低**：2,090 stars、224 forks、截至 2026-11-27 仍每日迭代；AGPL-3.0 對內部產線生成之 MP4/PNG/prompt **零版權與開源感染**。
    4. **進線強制衛生設定（Phase 5 本機啟用時）**：必執行 `cclay telemetry off` 與 `cclay update --off`（或設 `COZYCLAY_NO_UPDATE_CHECK=1`），徹底關閉 `posthog-js` 匿名遙測與自動更新檢查。
  - **純運鏡零安裝應急備援（不列雙標準維護）**：若 Phase 3 只需 2 分鐘拉一條純剛體運鏡弧線（無角色肢體動作、無須 MCP）且 CozyClay 線上版臨時異常，Muse 可開 **`Stage` 線上版（`aledige63.github.io/Stage/`，MIT、零遙測、直出帶靜音 AAC 的 9:16 H.264 MP4）** 應急；但產線規格、命名與 Phase 5 整合僅對接 **CozyClay** 單一標準。

- **落選者一句話交代死因**：
  - **Stage**：僅 1 star 單人早期專案（v0.9.0）且無 MCP／CLI、無首尾幀包與 Depth 通道，無法接入 agy 自動化管線（僅降格為 Phase 3 零安裝純運鏡應急備援）。
  - **Blender（＋Mickmumpitz 工作流）**：操作門檻過高違反「不要求 Creator 學 Blender」，且 VM 無 GPU 需重度腳本維護，為每集 0–2 鏡導入違反減法紀律。
  - **CodeVideoModel**：Previs 階段硬綁付費外部 API（OpenRouter GPT-6／GPT-Image-2）、重型 Conda/CUDA 堆疊且預設 16:9（`1536×864`），違背零新增付費與減法紀律。
  - **ComfyUI-Soundstage**：僅 7 stars 比賽作品，綁死常駐 ComfyUI 0.39+ 與非商用 FLUX 3 Klein＋LTX-2.5 整套工作台，不支援 H3 亦不相容休眠式 Colab 閘道。
  - **h3lite**：實查為本地 ComfyUI 跑 H3 的硬體感知 Codex skill（非白膜預演工具），不適用我方遠端 `comfy-colab-kit` 架構。

---

### Q3 閘道可行性：`comfy-colab-kit` 的 H3 profile 能否跑 Ref2VA 白膜？

透過只讀查詢本機閘道 `localhost:8080/_gate/profiles`（v0.6.0）並核對上游 `FireTable/comfy-colab-kit/profiles/examples/minimax-h3-video/` 完整 `profile.yaml` 與 6 支工作流 JSON，得出 **100% 確鑿結論**：

1. **現況判定：「底層節點已支援、預設模板未接線」**：
   - 閘道現行 `minimax-h3-video` profile（A100 80G 優先、自動 fallback 至 G4 96G → L4 24G，`high_mem: true`）內建的官方節點 **`MiniMaxH3ReferenceToVideo`**（`video_minimax_h3_r2v.json` Node 136）**原生已具備 `ref_videos.ref_video_0`（IMAGE 序列）與 `ref_video_audios.ref_video_audio_0`（AUDIO）輸入孔**。
   - **缺口所在**：預設 `h3-r2v` 模板只接了 2 個 `LoadImage`（`ref_image_0`、`ref_image_1`），**`ref_videos.ref_video_0` 懸空為 `None`，且圖內未擺放 `LoadVideo` → `GetVideoComponents`**。因此直接呼叫預設 `h3-r2v` **尚無法傳入參考影片**。
   - **隱藏關鍵發現①（雙保險已預裝）**：同一個 profile 內已預裝 **`h3-controlnet`（`video_minimax_h3_fun_controlnet_union.json`，MiniMax-H3-Fun-ControlNet-Union 2.0，Pose/Depth/Canny V2V）**，其圖內已接妥 `LoadVideo → GetVideoComponents → MiniMaxH3FunControlNetApply`，**開箱即可吃白膜 Depth/Canny 影片**！
   - **隱藏關鍵發現②（TriPRISM 8-Step 權重風險）**：`profile.yaml` 的 `model_aliases` 把 `minimax_h3_ref2va_pruned_int8_convrot.safetensors` 與 `fl2va` 預設全數映射到社群合併之 **`TriPRISM TurboFusion 8-Step`**（A100 用 int8、L4 自動降成 `dit-triprism-w6a8`），官方 `dit-official-ref2va-w6a8`（14.89 GB）列為 on-demand 選用模型。8-step 蒸餾權重可能削弱文字運鏡或白膜路徑服從度，須列為頭號冒煙驗證項。
   - **順帶驗證 L2（`end_frame`）**：`video_minimax_h3_i2v.json` 子圖內 `MiniMaxH3ImageToVideo`（Node 104）**已暴露 `first_frame` 與 `last_frame` 雙輸入孔**，但因 `fl2va` 同樣被 alias 到 `TriPRISM`，實際首尾收斂效果待冒煙驗證。
2. **限制為何**：
   - 模型上限：參考影片 2–15s（總長 ≤15s）、24fps；目標輸出 4–15s 整數秒。
   - 閘道資源限制：L4（24GB VRAM）自動套用 `0.4 MP`（約 `544×960` 等級）以防 OOM，A100 預設 `0.8 MP`（約 `768×1344` 等級）；餵入白膜 MP4 前須壓在 24fps、≤720p 並經 `ImageScaleToTotalPixels` 控管像素量。
3. **補法建議（最小工程量，不動手、只評估）**：
   - **不需新建 Colab profile、不需新增任何 custom node**。
   - **方案（自組單支 4 節點 API 工作流 JSON：`h3_r2v_clay.json`）**：以 `video_minimax_h3_r2v.json` 為底，僅補接 `LoadVideo → GetVideoComponents → ImageScaleToTotalPixels` 連至 `MiniMaxH3ReferenceToVideo.ref_videos.ref_video_0`（同時保留 `ref_image_0/1` 鎖首幀與范蠡定妝圖）；喚醒 `minimax-h3-video` 後，由 agy 上傳灰模 MP4 並 POST 該 JSON 至 ComfyUI `/prompt`。
   - **即時備援（0 改圖）**：若冒煙發現 `TriPRISM` 吃 `<Video 1>` 易材質滲漏或跑偏，① 在同一支 JSON 把 `UNETLoader` 切為 profile 已宣告之 `dit-official-ref2va-w6a8`（20-step）；或 ② 直接改走已預裝的 `h3-controlnet` 吃 CozyClay 匯出的 **Depth/Canny 通道**（物理隔離灰模 RGB）。

---

### Q4 H3 prompt 結構：與 Seedance 公式是否衝突？各引擎怎麼寫？

- **結論：明確衝突！H3 路由鏡必須改用 H3 官方結構衍生，不可直餵 Seedance 扁平公式。**
- **衝突原因**：
  1. Seedance 公式（`format → subject → action → environment → camera → look → timing → audio → preserve → avoid`）為單段散文且尾端帶 `avoid` 負面詞；H3 的 `Qwen3-VL-32B` 編碼器高度依賴官方鍵值標籤（Base 三段式＋Part One 對齊指令／Ref2VA 六段式＋`<Picture N>`/`<Subject N>`/`<Video N>`），且 H3 對裸否定詞敏感（易反向生成禁物）。
  2. 我方 TTS 聲音先行規範下，H3 的官方畫外音閉唇語句（`says in an off-screen voiceover: ... while his lips remain completely closed.`）與 `non_diegetic_music: N/A` 是防止閉眼張嘴與亂生 BGM 的剛性契約，Seedance 單段式無從精準表達。
- **定版衍生策略（上游 `script_pack.json` 維持引擎無關；下游階段 2 依 `engine_route × gen_mode` 套方言模板）**：

| 引擎路由 × 模式 | 衍生結構定版 | 關鍵約束 |
| :--- | :--- | :--- |
| **H3 × `i2v_first` / `i2v_first_last`**（L1/L2） | **H3 官方 Base 三段式**（Part One `<Picture N>` 對齊指令＋`integrated_multimodal_description`＋`overall_soundscape`＋`non_diegetic_music`） | 英文主體、僅 `<d>[Chinese] ...</d>` 留中文台詞；`movement` 轉成官方自然英文句；畫外音強制加 `while his lips remain completely closed.`；`non_diegetic_music: N/A`；**零裸否定詞** |
| **H3 × `ref2v`**（L1 多圖保臉 / L3 白膜） | **H3 官方 Ref2VA 六段式**（`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`） | 風格句置於 `[Shot 1]` 前；`<Subject 1>` 全段一致回指；L3 明確於 `retention_analysis` 標註 `<Video 1>` 僅保留構圖／運鏡／時序、`fully_preserved` 歸 `<Subject 1>`；`non_diegetic_music: N/A` |
| **Flow（Veo 3.1）** | **維持精煉 Seedance 電影敘事公式** | 英文電影敘事句，含景別、動作、鏡頭句、光影、結尾狀態與簡短正向禁字約束；保留台詞表演提示取口型節奏 |
| **Wan 2.2（5B TI2V）** | **精煉物理動作＋鏡頭句公式**（60–90 詞） | 只帶 1 句簡短 `subject_anchor`（不貼長定妝文避免稀釋動作）＋物理動作＋簡潔運鏡＋收尾狀態；不帶音訊段 |
| **LTX（階段 3.5 預演／≤2.5s 快切）** | **極短直白單句**（≤40 詞） | 主體＋動作＋景別／運鏡，不塞修飾詞與音訊描述 |

---

### Q5 Wan 參數化運鏡（Fun-Camera／Uni3C）還需要嗎？

- **結論：直接不導入（堅守減法紀律）。**
- **四條工程依據**：
  1. **與現行閘道規格不匹配**：實查 `comfy-colab-kit` 的 `wan-ltx-video` profile 僅內裝 **Wan 2.2 5B TI2V**（16.89 GB），不含 14B 權重；而 `Wan2.2-Fun-A14B-Control-Camera` 需獨立 14B 權重與專用節點（`WanCameraEmbedding`），Uni3C 亦需額外深度／相機軌跡節點，導入等於另建重型 Colab profile，在 L4 24GB 上極易觸發 offloading 拖垮吞吐。
  2. **功能完全被 H3 L3 覆蓋且邊際效益低**：我方 `minimax-h3-video` 已同時擁有 `ref_video_0` 與預裝 `h3-controlnet`，且 H3 保臉高、帶環境聲；Wan 僅負責背影／遠景／無臉動作 B-roll，為此維護第二套 3D 運鏡控制鏈路完全不划算。
  3. **Wan 2.2 原生文字運鏡已足夠應付 B-roll**：相較 Wan 2.1，Wan 2.2 對基礎推拉搖移英文句服從度已顯著提升，L1 足以覆蓋 95% 動作 B-roll；偶有需要精準路徑的無臉英雄鏡，直接升級路由至 H3 L3 即可。
  4. **唯一重評逃生閥**：未來 Phase 5+ 若進入大規模春秋戰場／複雜物理動作群戲，且 H3 L3 與 Wan 5B 連續 2 集過稿率 <25% 並改常駐 A100 時，始重啟評估 `Wan2.2-Fun-A14B-Control-Camera`。

---

### Q6 規格附錄形狀建議（不改規格本體，作為 `STORYBOARD-SPEC-V2` 運鏡附錄定稿草案）

#### 1. `movement` 擴充（100% 向後相容 v2.0 既有 `{type, speed}`）

```json
"movement": {
  "type": "push-in",
  "direction": "none",
  "speed": "slow",
  "amplitude": "small",
  "end_shot_size": "MCU",
  "easing": "ease-in-out",
  "named_shot": "slow-push-verdict"
}
```

- `type`（● 必填）：對齊官方 H3 12 類原語——`static` / `push-in` / `pull-out` / `zoom-in` / `zoom-out` / `pan` / `tilt` / `truck` / `pedestal` / `arc` / `track` / `handheld` / `roll` / `pov`（v2 原有 7 值全數相容）。
- `direction`（◐ 條件必填）：僅 `pan`/`tilt`/`truck`/`pedestal`/`arc`/`roll` 時填 `left / right / up / down / cw / ccw`。
- `speed`（● 必填）：`slow / standard / fast`（衍生 H3 時 `standard` 省略）。
- `amplitude`（○ 選填，預設 `medium`）：`small / medium / large`（衍生 H3 時 `medium` 省略，其餘轉 `with small/large amplitude`）。
- `end_shot_size`（○ 選填）：值域同 `shot_size`，標定鏡尾收束景別（同時服務 L1 語句收尾、L2 尾幀構圖、L3 白膜終點與 QC 抽幀比對）。
- `easing`（○ 選填，預設 `ease-in-out`）：`linear / ease-in / ease-out / ease-in-out`——**僅供 L3 CozyClay 與 L4 `ffmpeg` 消費，禁止寫進 L1 純文字 prompt**。
- `named_shot`（○ 選填）：指向 `bible/camera/named_shots.yaml` 的受控 ID。

#### 2. `control_method` 枚舉與 L3 欄位分責

- `script_pack.json`（上游靜態契約）新增兩欄：
  - `control_method`（● 必填，預設 `L1_prompt`）：`L1_prompt` / `L2_flf` / `L3_clay_ref2v` / `L3_clay_controlnet` / `L4_post_25d`。
  - `previs_brief`（◐ 僅 L3 必填）：1–2 句空間走位與起迄機位要點（給 Muse／agy 排 CozyClay 用）。
- `plan/production_state.json`（下游執行實態，不汙染上游 SHA256）新增：
  - `previs_artifacts`：`{tool: "cozyclay", project_file, ref_video_path, depth_video_path?, extracted_frame0_path?, approved_at}`。
- 新增驗證規則建議 **V11（運鏡分級護欄）**：單集 `control_method ∈ {L3_*}` 超過 3 鏡發出減法告警；快線出現 `L3_*` 直接硬閘駁回；`L2_flf` 必須與 `gen_mode = i2v_first_last` 一致且附降級目標 `L1_prompt`。

#### 3. 各級 QC 驗收法（統一於有效成片區間 `[+0.5s, end-0.5s]` 取 `f_0 / f_mid / f_end` 三幀）

| 分級 | 抽幀／比對對象 | 合格標準（QC-2 硬門檻） | 不達標處置 |
| :---: | :--- | :--- | :--- |
| **L1** | 有效區間 `f_0 / f_mid / f_end` 三幀＋動態播放 | ① 運鏡方向與型別正確（未逆向、未鎖死靜止）；② 景別推進與 `end_shot_size` 方向一致（主體高度佔比誤差 ≤ ±20%）；③ 主角臉部與解剖左右基準不翻轉 | 調 `amplitude/speed` 重抽；連抽 2 輪仍偏離路徑則升級 L2 或 L3 |
| **L2** | `f_0` 對首幀、`f_end`（或未裁尾末幀）對尾幀、`f_mid` 驗過渡 | ① 首尾幀構圖與角色一致；② 中段無瞬移、無雙重殘影或肢體扭斷；③ 裁切特例（`chain_trim_override`）銜接自然 | 降級 `L1_prompt` 或拆成兩顆原子鏡以剪輯化解 |
| **L3** | 成片 `f_0 / f_mid / f_end` 與 CozyClay 灰模同時間碼三幀 **50% 疊合比對** | ① 主體螢幕位置偏差 ≤ 15% 畫寬／高，視差與弧線方向一致；② **零灰模材質滲漏**（無塑膠灰感、無網格線、無關節接縫）；③ 臉部與服裝維持 QC-2 門檻 | 若滲漏→切 `L3_clay_controlnet`（Depth）；若軌跡被蒸餾壓扁→切 `dit-official-ref2va-w6a8`（20-step） |
| **L4** | 全段抽幀＋9:16 平台安全區遮罩檢核 | ① 繁中文字 100% 清晰零裁切、避開 IG/Shorts UI 區；② `zoompan` 平滑無抖動鋸齒、無黑邊、鎖定 30fps | 修正 `ffmpeg` 參數立即重算（<10 秒，0 GPU） |

#### 4. `named shots` 庫建立方式（`bible/camera/named_shots.yaml`）

- **不整包安裝外部 skill**，改在 `bible/camera/named_shots.yaml` 維護本劇精選 **8–10 個高頻 9:16 實戰鏡型**（初期清單：`steady-dialogue-lock`、`slow-push-verdict`、`subtle-pull-reveal`、`handheld-jolt`、`ots-push-tension`、`arc-reveal-90`、`low-angle-authority`、`match-cut-bridge`、`crash-zoom-post`、`ken-burns-card`）。
- 英文實證句式合法改寫自 MIT 授權之 `loopforge0/minimaxh3-shots-skills` 並嚴格對齊官方 12 原語；每筆強制含 `verified_9x16_status`（初期一律標 `UNTESTED`，隨 EP-01 起按實跑回填 `PASS / PARTIAL / FAIL`）與 `known_pitfalls`。

---

### Q7 EP-01 試套驗證（S01、S02、S17）

依據 `DRYRUN-EP01-v0.3.1-BLIND.md` 實套本工作流，檢驗最難三鏡是否完全裝得下：

#### 1. S01（0–4s｜淨 4s／生成 5s｜湖上冷開場・HOOK）
- **原劇本難點**：晨霧太湖小舟，范蠡（`OUTFIT-02`）獨坐望向對面空座（文種位）緩緩閉眼；且必須與 **S16b 構成精準首尾呼應（`ref_shot: S01`）**。原表預估 Wan，但作為開片 4 秒 HOOK 且帶主角正面微表情閉眼，Wan 5B 保臉與前景空座空間鎖定風險過高。
- **定版方案**：**L3（`L3_clay_ref2v` → CozyClay 白膜 → H3 `h3_r2v_clay.json`）**；若 L3 冒煙未過，降級為 **L1（Flow Veo 3.1 `i2v_first` 慢推）**。
- **結構化欄位**：`shot_size: MS` → `end_shot_size: MCU`，`movement: {type: "arc", direction: "left", speed: "slow", amplitude: "small", easing: "ease-in-out", named_shot: "arc-reveal-90"}`（附小幅前推感），`control_method: "L3_clay_ref2v"`，`face_visible: true`，`voice_mode: "none"`。
- **CozyClay 預演排布（5 分鐘）**：
  - 設 **9:16、24fps、5.0s**（涵蓋頭尾各 0.5s 裁切緩衝）。
  - 場景：長木舟方體＋前景左下空木座方塊＋對側坐姿假人（代表范蠡）＋低平面水面。
  - 鏡頭軌跡：`0.0s` 越過左下空座中景起手 → `0.5s–4.5s` `ease-in-out` 沿小弧線向左輕繞 ~20° 並緩慢逼近至 `MCU`（確保空木座始終保留在左下前景邊緣、范蠡維持前三分之四朝向左側露傷痕）→ `4.5s–5.0s` 穩停。
  - **一魚兩吃**：同份 CozyClay 專案直接存檔複用於 **S16b**（僅反轉或微調遠處使者小船入畫），鎖死 100% 首尾呼應機位！
  - 匯出：灰模 MP4（`<Video 1>`）＋第 0 幀構圖圖（送免費 Flow `gflow i2i` 烘焙寫實首幀 `<Picture 1>`）＋Depth pass（備援 `h3-controlnet`）。
- **H3 Ref2VA 六段式重點**：`subject_definitions` 綁 `<Subject 1>`（范蠡，外觀取 `<Picture 1>` 與 `<Picture 2>` 定妝）＋ `<Video 1>`（僅作構圖、視差與運鏡路徑參考）；`retention_analysis` 標明 `<Subject 1>: fully_preserved`、`<Video 1>: partially_preserved - preserve camera arc, framing and timing only, replace all greybox surfaces with photorealistic misty Lake Taihu wooden boat and linen robes`；`detailed_description` 描寫霧氣流動、他望著空座緩緩閉眼；`non_diegetic_music: N/A`。

#### 2. S02（4–9s｜淨 5s／生成 6s｜2022 抵達・SETUP）
- **原劇本難點**：睜眼切入 2022 台北街頭，路人對手機說話，他踉蹌扶柱、**手按向空腰間（驚）**。這顆的核心是「爆發性肢體表演＋情緒張力」，**非複雜 3D 軌道**——硬套白膜反而會限制 Veo 的自然肢體與微表情演技。
- **定版方案**：**L1（`L1_prompt`）走 Flow（Veo 3.1 `i2v_first`，6s 檔位）**；後製字卡 `2022.11.30 ChatGPT 誕生` 嚴格走 **L4 `visual_text_overlay`**。
  - *風險緩解*：若單鏡 5s 塞「睜眼＋踉蹌扶柱＋摸空腰間」觸發 V6 動作過密或表演掉拍，於 QC-1.5 拆為兩顆原子鏡（`S02a` 睜眼驚愕 2s＋`S02b` 踉蹌扶柱按空腰 3s），均維持 L1。
- **結構化欄位**：`shot_size: MCU` → `end_shot_size: MS`，`angle_h: three-quarter`，`subject_facing: left`（確保右手跨按左腰空處清晰可見），`movement: {type: "pull-out", speed: "standard", amplitude: "small", named_shot: "handheld-jolt"}`（附輕微手持感），`control_method: "L1_prompt"`。
- **Flow 衍生 Prompt 關鍵句（電影敘事方言）**：
  > `6-second 9:16 vertical live-action cinematic single shot. Beginning from the first frame of Fan Li in Spring-Autumn linen robe standing stunned on a bustling 2022 Taipei street at dusk, his eyes snap wide open in shock. The camera pulls out with small amplitude and subtle handheld shake from a medium close-up to a medium shot as modern pedestrians walk past talking into smartphones; Fan Li staggers back half a step, bracing one hand on a concrete pillar while his right hand instinctively reaches across to his empty left waist where a sword should hang, freezing in disbelief. End state: gripping the pillar, hand hovering over his empty left waist, eyes wide. Natural street lighting, shallow depth of field, no readable signs or text.`

#### 3. S17（80–86s｜淨 6s／生成 6–7s｜判讀金句・PAYOFF）
- **原劇本難點**：28 字核心金句吃滿 5.8s，且屬 **`face_visible: true` + `lip_sensitive: true`** 正臉近景。絕不可走 L3 白膜（會僵化口型與眼神演技），亦不可做大角度旋轉（防傷痕與口型穿幫）。
- **定版方案**：**L1（`L1_prompt`）走 H3 `h3-r2v`（多圖保臉，無參考影片）**，套用 `slow-push-verdict`；若生成 7s 出現尾段漂移或口型超窗，依 DESIGN v1.4 於 QC-1.5 插入 1.5s 手指停筆／窗外巨幕冷光空鏡切開（L1+剪輯拆解），並可於 L4 補 +5% 極慢數碼微推強化壓迫感。
- **結構化欄位**：`shot_size: MS` → `end_shot_size: MCU`，`subject_facing: left`（微側正臉，左眉尾傷痕穩定入鏡），`movement: {type: "push-in", speed: "slow", amplitude: "small", named_shot: "slow-push-verdict"}`，`control_method: "L1_prompt"`，`lip_sensitive: true`。
- **H3 官方 Ref2VA 六段式衍生關鍵段**：
  ```text
  subject_definitions:
  <Subject 1> is the composed late-20s East Asian man from <Picture 1> and <Picture 2>, wearing the dark modern coat (OUTFIT-01), with a faint scar at his left eyebrow tail and a low small ponytail at the nape.
  <Picture 1> is the first frame of [Shot 1], framing <Subject 1> in a dimly lit Taipei apartment facing the cold blue glow of an outdoor giant screen through the window.

  summary:
  [reference generation + keyframe completion] Starting from <Picture 1>, <Subject 1> delivers a calm, sharp verdict while the camera slowly pushes in toward his eyes.

  retention_analysis:
  <Subject 1> (appears in [Shot 1]): fully_preserved - maintain exact facial features, left eyebrow-tail scar, hairstyle, and dark coat across all frames.
  <Picture 1> ([Shot 1] first frame): fully_preserved - match opening framing, apartment layout, and warm-interior versus cold-blue window lighting.

  detailed_description:
  Live-action, cinematic, restrained dark-thriller realism in 9:16 vertical framing.
  [Shot 1] Opening from <Picture 1>, <Subject 1> stands in a dimly lit modern apartment looking toward the cold blue glow outside the window. The camera pushes in with small amplitude at slow speed from a medium shot to a tight medium close-up on <Subject 1>'s eyes, keeping his face steadily angled three-quarter left so the faint scar at his left brow tail remains visible. <Subject 1> (S1), a calm, measured late-20s Taiwanese Mandarin male, says: <d>[Chinese] 空了十一天，又全票請回——不是他握著開關，是飛鳥還沒打盡。</d> On the final phrase he lowers his chin slightly and holds an unwavering gaze without blinking.

  overall_soundscape:
  Quiet late-night apartment room tone with faint distant city rumble outside the glass.

  non_diegetic_music:
  N/A
  ```

**試套結論**：三顆 EP-01 最難鏡頭各歸其位（S01 → **L3**、S02 → **L1 Flow ＋ L4 字卡**、S17 → **L1 H3 六段式**），四級分層與欄位擴充完全裝得下，無需任何例外補丁。

---

## 四、單一推薦工作流總覽（定版）

```text
[script_pack.json (v2.0 + 運鏡附錄)]
   │  每鏡宣告 movement + control_method (L1 / L2 / L3 / L4)
   │  硬閘：V11（每集 L3 ≤ 2 鏡；快線禁 L3；L2 必綁 i2v_first_last）
   ▼
┌─────────────────────┬──────────────────────┬───────────────────────┬──────────────────────┐
│ L4_post_25d (15-20%)│ L1_prompt (65-75%)   │ L2_flf (5-10% 例外)   │ L3_clay_ref2v (0-2鏡)│
│ 證據卡／微幅數碼推  │ 日常對白／微推／B-roll│ 單調起迄收斂／MatchCut│ 複雜弧線／首尾同機位 │
└──────────┬──────────┴──────────┬───────────┴───────────┬───────────┴──────────┬───────────┘
           │                     │                       │                      │
           │                     │                       │                      ▼
           │                     │                       │             [CozyClay 9:16 24fps]
           │                     │                       │             Phase3: 瀏覽器零安裝
           │                     │                       │             Phase5: VM MCP(關遙測)
           │                     │                       │             匯出: 灰模MP4+首幀構圖+Depth
           │                     │                       │                      │
           ▼                     ▼                       ▼                      ▼
     [VM CPU ffmpeg]    [引擎方言衍生器]        [產首幀＋尾幀]        [依灰模第0幀烘焙首幀]
     (0 GPU, N=1)       • H3 → 官方3段/6段      (Flow 免費產圖)       → 進 h3_r2v_clay.json
                        • Flow → Seedance句     → H3 i2v / Veo -e     (ref_video_0 + ref_img)
                        • Wan → 精煉動作句      (冒煙未過前禁常規)    備援: h3-controlnet(Depth)
           │                     │                       │                      │
           └─────────────────────┴───────────────────────┴──────────────────────┘
                                             │
                                             ▼
                  [QC-2 有效區間 [+0.5s, end-0.5s] 三幀運鏡驗收 + 疊圖檢核]
                  → 入選回寫 bible/camera/named_shots.yaml 實測狀態
```

---

## 五、未驗證事項與開拍前冒煙測試清單（供開工前逐項實測）

以下 **6 項** 均屬「只讀查證無法取代實機」之未驗證事項，建議在正式開拍 EP-01 前以 **1 次 Colab A100/L4 Session（預估 < 2 CU）＋ 1 次 Flow 測試** 一次測完：

| # | 未驗證事項 | 風險影響 | 冒煙測試方法（最小成本） | 通過判準 |
| :-: | :--- | :--- | :--- | :--- |
| **SM-1** | **`TriPRISM 8-Step` 對 L1 官方詞表運鏡的服從度** | 若 8-step 蒸餾嚴重壓縮運鏡幅度，L1 慢推／平搖會變成近似靜止 | 用 `h3-r2v` 跑 2 支 9:16 5s 測試片（`slow-push-verdict` 與 `pan-right`），對照 `TriPRISM 8-step` vs `dit-official-ref2va-w6a8`（20-step） | `TriPRISM` 在 3 抽內 ≥2 支運鏡方向與幅度肉眼清晰；否則 L1 運鏡鏡切 `dit-official-ref2va-w6a8` |
| **SM-2** | **自組 `h3_r2v_clay.json` 接 `ref_video_0` 之白膜跟隨與防滲漏表現** | 決定 L3 主路徑走 `ref_video_0` 還是直接走已預裝的 `h3-controlnet` | 用 CozyClay 線上版匯出 1 支 9:16 5s 24fps S01 灰模 MP4＋Depth MP4，各跑 1 輪 `h3_r2v_clay.json` 與 `h3-controlnet`（帶范蠡首幀） | 有效區間三幀疊合偏差 ≤15% 且**零灰模塑膠感／網格線殘留**；擇優鎖定為 L3 預設實作 |
| **SM-3** | **Colab L4（24GB）執行 L3（`ref_image`＋`ref_video_0`）是否 OOM 與單鏡耗時** | 若 L4 必 OOM，則 L3 鏡須於路由層強制鎖定 A100/G4，不可 fallback 至 L4 | 於 L4 24GB 以 `0.4 MP` 與 `0.5 MP` 跑 SM-2 同輸入，記錄峰值 VRAM 與耗時 | 0 OOM 且單鏡 <10 分鐘；若 OOM 則於路由器寫死「L3 鏡鎖 A100」 |
| **SM-4** | **`h3-i2v`（`MiniMaxH3ImageToVideo.last_frame`）在 `TriPRISM` 下的實際收斂能力** | 決定 L2 `i2v_first_last` 能否在 H3 轉正（現行 `profile.yaml` 將 `fl2va` alias 至 `TriPRISM`） | 給 `h3-i2v` 餵 S02 或燭火首尾兩幀跑 1 支 5s 測試片 | 末幀收斂至尾幀構圖且中段無瞬移；不通過則 H3 禁用 L2（或另掛原生 `FL2VA` 權重） |
| **SM-5** | **Flow `veo-lite`（12/05 後留存模型）對 `-e`（end-frame）與 L1 鏡頭句的服從度** | 12/05 `veo-fast`/`quality` 退役後，影響 S02 等 Flow 英雄鏡能否穩扛 L1/L2 | 登入 `gflow` 後以 `--model veo-lite --aspect 9:16` 實跑 1 支 `i2v`（L1）與 1 支 `i2v -e`（L2） | 畫質與運鏡通過 QC-2；若 `-e` 不支援則 Flow L2 維持停用 |
| **SM-6** | **CozyClay 在無 GPU Debian 12 VM 上的無頭出片路徑（Phase 5 前置）** | 確認 agy 未來於 VM 透過 MCP 除生成場景 JSON 外，能否靠無頭 Chromium 軟體 WebGL 穩定匯出 MP4 | Phase 5 啟動前於 VM 測試 `npx cozyclay --no-open` + 無頭 Chromium 匯出 5s 9:16 MP4（本階段**不安裝、不測**） | 若軟體 WebGL 出片過慢或失敗，定調「agy MCP 寫場景檔 → Muse 本機瀏覽器一鍵匯出 MP4」分工 |
