# H3 人物一致性與電影運鏡方法查證與取捨備忘錄（agy 工程評估）

> **文件定位**：只讀查證與取捨備忘錄（不改動 `STORYBOARD-SPEC-V2.md` 與 `DESIGN.md` 本體、不安裝任何套件或 custom node、不喚醒 GPU 實跑、不 push 進 repo）  
> **撰寫日期**：2026-11-28  
> **觸發背景**：DEMO-02（Flow `veo-fast` 單首幀 `i2v` 路線，見 `demo02/gen_clips.sh`）於導演 QC（QC-D，見 `STORYBOARD-SPEC-V2.md` §B.8）判定**不過**，核心病灶為**跨鏡身分與年齡漂移**（S3a 成片退化成另一名年輕男子）、**服裝細節逐鏡變形**（領邊／髮簪／玉佩／束帶）與**特寫傷痕位置遷移**。我方規格已將口型敏感核心對白鏡路由至 `minimax-h3-video`（Ref2VA），但 H3 路線尚未經過人物一致性冒煙實測。  
> **依據材料（本機只讀）**：`H3-CONSISTENCY-CAMERA-REF.md`、`STORYBOARD-SPEC-V2.md`（v2.1 含附錄 A／B）、`CAMERA_WORKFLOW_AGY_MEMO.md`、`MASTER_FACE_DECISION.md`、`COSTUME_REGISTRY.md`、`DESIGN.md`（v1.4）、`DEMO02-DIRECTOR-STATEMENT.md`、`demo02/gen_clips.sh`、`casting/master/` 實檔盤點。  
> **外部一手查證來源（全只讀）**：GitHub `Luisacaotica/ComfyUI-MiniMaxH3Mod`、`NyckM/3d-Camera-control-H3-Minimax`、`Comfy-Org/embedded-docs`（`MiniMaxH3ReferenceToVideo`）、`FireTable/comfy-colab-kit`（`minimax-h3-video` profile 與 `video_minimax_h3_r2v.json`）、Hugging Face `MiniMaxAI/MiniMax-H3`（`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`）、`akatz-ai/MiniMax-H3-Character-Swap-LoRA`、`Alissonerdx/Minimax-H3-ComfyUI`、Stable Yogi（`stableyogi.com`／Civitai／`comfy.icu`）。  
> **無法從只讀來源實證的項目**：文內一律以 **`[未驗證／須實機冒煙]`** 明示標註，絕不假裝已知。

---

## 一、總結裁決表（Per-Item Verdict｜減法紀律優先）

> **減法判準**：凡既有產線元件已可承擔、或無明確授權、或必須破壞「零新 profile／休眠式閘道」架構者，除非實測證明現有基線不達標，一律不導入。

| 項目 | 建議裁決 | 核心理由（一句話） | 主要查證來源 |
| :--- | :---: | :--- | :--- |
| **原生多圖 H3 Ref2VA（零新工具：自組 4–5 槽 JSON＋`ref_image_size: max`）** | **ADOPT（優先基線）** | 閘道內建 `MiniMaxH3ReferenceToVideo` 原生即支援最多 **9 張參考圖**，僅預設模板只接了 2 槽；免裝新節點、免改 profile、零新授權風險，應先列為 **SM-7A** 立即驗證。 | [Comfy-Org/embedded-docs](https://github.com/Comfy-Org/embedded-docs)（`MiniMaxH3ReferenceToVideo`）；`CAMERA_WORKFLOW_AGY_MEMO.md` §三 Q3 |
| **角色／鏡頭提示詞分工原則（按 V3 角色槽位化改寫）** | **ADOPT（進附錄 A）** | 零工具成本，直接止血「多圖混責／灰模滲漏／身分漂移」；但須改寫為**與 V3 餵圖序（`scene → characters → props`）一致的角色分責**，不可硬寫死 `<Picture 1>` 歸身分。 | `STORYBOARD-SPEC-V2.md` §三 C／§六 V3／§A.4；[MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` |
| **RefMod（`Luisacaotica/ComfyUI-MiniMaxH3Mod`）** | **WATCH（條件升階｜SM-7B）** | **真存在、MIT 授權、免訓練**（3D VAE 預編碼 1.1–1.6 MB 潛空間包，且支援 `identity`／`clothing` 分拆）；但閘道未預裝此 custom node，且對 **`TriPRISM w6a8` 8-step 相容性未經一手實證**。須等原生多圖 Ref2VA（SM-7A）實測失敗或 L4 VRAM 吃緊時再啟動 SM-7B 驗證。 | [Luisacaotica/ComfyUI-MiniMaxH3Mod](https://github.com/Luisacaotica/ComfyUI-MiniMaxH3Mod)（MIT，~640+ stars） |
| **Camera H3（`NyckM/3d-Camera-control-H3-Minimax`）** | **REJECT（減法駁回）** | **無標準開源 LICENSE**（預設保留全部權利＋綁 Viggle Meridian 條款）、硬綁互動式 ComfyUI 畫布（喚醒 Colab GPU 燒 CU 才能拖關鍵幀）、提示詞模式不如我方 L1 結構化派生、Depth Warp 模式重度拖入 MoGe＋Meridian 權重，全面輸給已鎖定的 **CozyClay（0 GPU＋MCP＋AGPL-3.0）**。 | [NyckM/3d-Camera-control-H3-Minimax](https://github.com/NyckM/3d-Camera-control-H3-Minimax)（無 LICENSE 檔） |
| **Stable Yogi 11 Camera Shots** | **REJECT（不導入工作流、不複製原文）** | 本體為標準 H3 Ref2VA 工作流＋11 招基礎運鏡測試包，**未查到明確 MIT/Apache/CC0 商用授權**，且 11 招內容（Push/Pull/Pan/Truck/Tilt/Pedestal/Static/Tracking/Orbit）與官方 12 原語及已核准改寫的 MIT `loopforge0/minimaxh3-shots-skills`（29 招）高度重疊。僅可借鏡其「非著作權經驗觀察」（如 L1 自由 Orbit 易變殘弧），不導入工作流亦不抄錄提示詞。 | [stableyogi.com](https://stableyogi.com)；Civitai `MiniMax H3 Camera Shots - 11 Tested Prompt Moves v1.0` |
| **Character Swap LoRA（Akatz Labs／Alissonerdx）** | **REJECT（嚴格判為 Out of Scope）** | 兩套權重皆真實存在且可下載，但解決的是「真人實拍表演片換角」，非我方 AI 原生短劇跨鏡漂移痛點；導入須自拍表演底片破壞快線 SLA、古裝寬袖／冠飾與現代體態輪廓不匹配、且標準 H3 LoRA 掛在閘道 `w6a8` 權重上已知有 `lora key not loaded` 掉鍵風險。 | [akatz-ai/MiniMax-H3-Character-Swap-LoRA](https://huggingface.co/akatz-ai/MiniMax-H3-Character-Swap-LoRA)；[Alissonerdx/Minimax-H3-ComfyUI](https://huggingface.co/Alissonerdx/Minimax-H3-ComfyUI) |

---

## 二、與社群彙整（`H3-CONSISTENCY-CAMERA-REF.md`）之實查差異核對

| # | 社群彙整說法 | 一手查證真相 | 對我方產線的影響 |
| :-: | :--- | :--- | :--- |
| **1** | RefMod「像 LoRA 一樣載入」 | **操作體驗像 LoRA，底層不是 LoRA 權重**：RefMod 產出的是 3D Video VAE 預編碼的 **Reference Latent Adapter**（`.safetensors` ~1.1–1.6 MB，含 latent＋metadata＋`concept_type`），透過 `CONDITIONING` 與外層取樣 hook 注入，**不改寫 DiT 線性層權重**。 | **好消息**：理論上避開傳統 LoRA 在 `w6a8` 量化層上的 `lora key not loaded` 掉鍵問題（但仍須實機驗 `TriPRISM w6a8`）。 |
| **2** | 用 4–10 張角色圖直接做成一個 RefMod | `ComfyUI-MiniMaxH3Mod` 支援將 **`identity`（臉部身分）與 `clothing`（服裝）分開製作並疊加**。我方 `casting/master/` 的 9 張鎖定圖橫跨 **3 個年齡（28／38–40／60）× 3 套服裝（OUTFIT-01／02／03）**——若 9 張全塞同一個 RefMod，會觸發年齡與古今服裝互相汙染。 | 必須嚴格遵循我方 2026-11-27 **身分層／服裝層分拆原則**，不可把 9 張混包；單一服裝目前僅 2–3 張，古裝缺背影與特寫。 |
| **3** | 提示詞分工：`<Picture 1>` 只負責身份，`<Video 1>` 只負責運鏡 | 與我方 **`STORYBOARD-SPEC-V2.md` §六 V3 規則衝突**：V3 規定 `asset_refs` 餵圖順序固定為 **`scene → characters → props`**。若該鏡有場景或 QC-1 首幀圖，`<Picture 1>` 是首幀／場景（管構圖與光線鎖定），角色圖落在 `<Picture 2..K>`。 | 附錄 A 不可照抄「`<Picture 1>` 歸身分」，須寫成**依 V3 角色槽位自動綁定**的分責條文（見 Q6 草案）。 |
| **4** | Camera H3 是「拖曳設關鍵幀，自動生成 H3 運鏡提示詞」的編輯器 | 半對：早期版本確實是提示詞編譯器（`RETURN_TYPES = ("STRING",)`，社群明言複雜路徑仍易被 H3 自由發揮），後續迭代則綁進 **MoGe 深度估算＋Viggle Meridian Depth Warp 影片管線**；且 repo **無開源 LICENSE 檔**。 | 兩個模式都輸給我方既有設計（文字模式輸 L1 結構化衍生；幾何模式輸 0-GPU CozyClay＋已預裝 `h3-controlnet`）。 |
| **5** | Character Swap LoRA 資源列為「Alissonerdx／Akatz Labs」 | 兩者實為**兩套獨立發布的權重與授權**：Akatz Labs（~148 MB，繼承 MiniMax H3 社群條款含美歐英韓地域排除）；Alissonerdx（BFS v1.1 ~80 MB SVD 動態秩，`mixed-asset-licenses` 禁架 API/SaaS、年營收 >100 萬美元須署名）。 | 兩者皆與我方 AI 原生產線目標錯配，且有 `w6a8` LoRA 掉鍵風險，直接駁回。 |

---

## 三、Q1–Q6 逐題工程查證與答覆

### Q1｜RefMod 現實查核（`ComfyUI-MiniMaxH3Mod`）

1. **是否存在與維護度**：**確定存在**。GitHub 倉庫為 [`Luisacaotica/ComfyUI-MiniMaxH3Mod`](https://github.com/Luisacaotica/ComfyUI-MiniMaxH3Mod)（作者 Luisa Caótica／`luisacaotica`），屬 MiniMax H3 社群主流自訂節點包之一（GitHub 約 640+ stars、ComfyUI Registry 數萬次下載；Stable Yogi、RunComfy 等社群工作流皆以它為標準 RefMod 實作）。
2. **授權條款**：節點程式碼為 **MIT License**（商業內部使用零傳染；底層 MiniMax H3 模型權重與 VAE 仍受 `MiniMax H3 Community License` 約束）。
3. **產出物本質與 Ref2VA 載入方式**：
   - **產出物**：不是 LoRA 權重，也不是純文字 embedding，而是 **Reference Latent Adapter（`.safetensors`，約 1.1–1.6 MB）**——由 `Create H3 RefMod`／`Extract H3 RefMod` 節點呼叫 MiniMax H3 原生 **3D Video VAE** 對輸入參考圖／影／音做**一次性離線編碼**，將壓縮後的潛空間張量（latents）連同結構化 metadata 與 **`concept_type`** 標籤（`identity`、`clothing`、`pose_motion`、`background`、`style`）封裝成檔。**零訓練迴圈、零梯度計算**。
   - **載入與接線方式**：
     1. 檔案置於 `ComfyUI/models/refmods/*.safetensors`。
     2. 以 **`MiniMaxH3RefModsLoader`** 載入（支援最多 **8 個可疊加槽位**，各自獨立調整 `strength_1..8` 強度與 `copies_1..8` token 重複倍率，可同時掛載 1 個 `identity` RefMod＋1 個 `clothing` RefMod 而避免 token 衝突）。
     3. 經 **`MiniMaxH3RefModApply`**（可選串接 Step Curve 控制 `concept_at_start / middle / ends` 去噪時程權重）接在 Conditioning 階段與 Guider／Sampler 之間——底層同時橋接 **`CONDITIONING`** 與透過 ComfyUI 公開外層取樣 hook 複製的 **`MODEL`**，在採樣前將預編碼參考束注入去噪管線。
     4. 另有 **`Inspect H3 RefMod`** 檢視內部 token 消耗與參考預覽。
4. **Colab L4（24GB）建置成本（時間／VRAM）**：
   - **時間**：免訓練、純 VAE 編碼。社群實測數十張參考幀約 **15–20 秒**；依此推估我方 3–6 張靜態圖在 L4 上約 **5–15 秒**即可產出 `.safetensors`（一次產出永久複用，無須每鏡重編碼）。**`[未驗證／須實機冒煙]`**：尚無 Colab L4 實測精確秒數。
   - **VRAM**：建置期僅需載入 H3 3D Video VAE 編碼器（不跑 15GB DiT 與反傳），理論上遠低於 24GB 上限；推論期相較每輪即時對多張高解析參考圖跑 VAE 編碼，反而**減少即時 VAE 峰值記憶體與前處理延遲**（但參考 token 仍計入 DiT attention 記憶體）。**`[未驗證／須實機冒煙]`**：L4 建置與推論峰值 VRAM 精確 GB 數待 SM-7B 實測。
5. **與我方閘道 `minimax-h3-video` 權重之相容性**：
   - **既有 profile 現況（查自 `CAMERA_WORKFLOW_AGY_MEMO.md` §三 Q3）**：本機 `comfy-colab-kit` 的 `minimax-h3-video` profile（A100 80G 優先、自動 fallback 至 G4 96G → L4 24G）預設把 `ref2va` 與 `fl2va` alias 至社群合併蒸餾權重 **`TriPRISM TurboFusion 8-Step`**（A100 跑 `int8`，L4 自動降為 **`dit-triprism-w6a8`**），另宣告官方 20-step **`dit-official-ref2va-w6a8`**（14.89 GB）為 on-demand 權重。
   - **工程硬門檻①（未預裝節點）**：`FireTable/comfy-colab-kit` 的 `minimax-h3-video` profile **目前並未預裝 `ComfyUI-MiniMaxH3Mod`**。若要啟用，必須修改 Colab worker 啟動設定以 `git clone` 該 repo、安裝其 `requirements.txt` 並同步 `.safetensors` 至 `models/refmods/`——這違反「零 profile 改動」原則，必須有實測數據支撐才值得做。
   - **工程風險②（`TriPRISM w6a8` 8-step 相容性）**：
     - *正面研判*：RefMod 使用標準 H3 Video VAE 預編碼，並透過 `CONDITIONING` 與外層 hook 注入，**不對量化 DiT 線性層做矩陣合併**，因此理論上比傳統 LoRA 更有希望相容 `int8`／`w6a8`。
     - **`[未驗證／須實機冒煙]`**：一手資料中**未查到 `ComfyUI-MiniMaxH3Mod` 與 `dit-triprism-w6a8`（6-bit 權重＋8-step 蒸餾）組合的正式驗證紀錄**。8-step 蒸餾模型對 Step Curve 衰減極敏感，且 `w6a8` 張量型別是否與 `MiniMaxH3RefModApply` 的外層 hook 衝突，必須實機測過才能定論。
6. **我方鎖定范蠡 Master 全套（`casting/master/`，~9 張）是否足夠？**
   - **實盤清單（排除已封存之舊 Seedream `fanli-master-B.jpg` 與 `superseded-seedream/`）**：

     | 檔案 | 時代／服裝卡 | 年齡層 | 視角 | 露臉／左眉疤 |
     | :--- | :--- | :---: | :--- | :---: |
     | `fanli-master-B-userface.png` | `FANLI-OUTFIT-01`（現代丁案） | B（38–40） | 正面半身 | ● 有臉有疤 |
     | `fanli-master-B-45.jpg` | `FANLI-OUTFIT-01` | B（38–40） | 45° 左側半身 | ● 有臉有疤 |
     | `fanli-master-B-back.jpg` | `FANLI-OUTFIT-01` | B（38–40） | 正背影半身 | ○ 無臉（鎖低束短髮尾） |
     | `fanli-master-A.jpg` | `FANLI-OUTFIT-01` | **A（~28）** | 正面半身 | ● 有臉有疤 |
     | `fanli-master-C.jpg` | `FANLI-OUTFIT-01` | **C（~60 銀灰髮）** | 正面半身 | ● 有臉有疤 |
     | `fanli-master-ancient-front.jpg` | `FANLI-OUTFIT-02`（春秋布衣） | B（38–40） | 正面半身（持竹簡） | ● 有臉有疤 |
     | `fanli-master-ancient-45.jpg` | `FANLI-OUTFIT-02` | B（38–40） | 45° 左側半身 | ● 有臉有疤 |
     | `fanli-outfit03-front.jpg` | `FANLI-OUTFIT-03`（上大夫朝服） | B（38–40） | 正面半身（扶劍） | ● 有臉有疤 |
     | `fanli-outfit03-45.jpg` | `FANLI-OUTFIT-03` | B（38–40） | 45° 左側半身 | ● 有臉有疤 |

   - **關鍵判斷（不可把 9 張整包塞進單一 RefMod！）**：
     1. **嚴禁跨年齡與跨服裝混包**：若把 9 張混成 1 顆 RefMod，60 歲的銀灰髮皺紋（`C`）、28 歲青澀感（`A`）與現代西裝／春秋布衣／朝服玉組佩將混在同一組 latent 內，直接破壞我方 `MASTER_FACE_DECISION.md` 的**身分層／服裝層分拆紀律**，極易造成年齡漂移與古今穿幫。
     2. **拆成「身分 RefMod ＋ 各服裝 RefMod」才是正解**：
        - **身分組（Age B，6 張）**：取 6 張 **38–40 歲露臉圖**（`B-userface`、`B-45`、`ancient-front`、`ancient-45`、`outfit03-front`、`outfit03-45`；排除 `A`、`C`、`B-back`）建立 `identity` RefMod——6 張剛好跨 3 套服裝，反有助於讓模型把「不變量」鎖在臉型骨相與左眉尾傷痕上。**現有缺口**：6 張全是同深灰棚光半身像，缺**大特寫臉部（CU）**與**右側 45° 臉（教模型右眉無疤）**。
        - **服裝組（每套僅 2–3 張，偏少）**：`OUTFIT-01` 3 張、`OUTFIT-02` 僅 2 張、`OUTFIT-03` 僅 2 張，低於社群建議的 4–10 張／包。對 DEMO-02 翻車的 `OUTFIT-02`，無論走原生多圖 Ref2VA 或 RefMod，皆建議日後以免費 Flow `nano2` 補齊 1–2 張（`ancient-back` 冠緌背影＋領襟／玉璧近景，同經 QC-1 鎖定）。
- **Q1 裁決**：**WATCH（列為 SM-7B 條件升階候選）**。先用閘道免安裝的原生多圖 Ref2VA 跑 SM-7A；僅在原生多圖保臉／保服裝不達標、或 L4 吃 4–5 張即時圖導致 VRAM／速度超標時，才啟動 SM-7B 評估安裝 `ComfyUI-MiniMaxH3Mod`。

---

### Q2｜現行閘道多圖 Ref2VA 能力盤點與最小冒煙測試設計

1. **閘道現行 H3 Ref2VA 到底能吃幾張參考圖？**
   - **預設模板（開箱即用）**：僅接線 **2 張**。依前次對本機 `localhost:8080/_gate/profiles` 與上游 `FireTable/comfy-colab-kit/profiles/examples/minimax-h3-video/video_minimax_h3_r2v.json` 的實查（`CAMERA_WORKFLOW_AGY_MEMO.md` §三 Q3），預設 `h3-r2v` 模板只放了 2 個 `LoadImage` 連到 `MiniMaxH3ReferenceToVideo`（Node 136）的 `ref_image_0` 與 `ref_image_1`。
   - **底層節點原生上限（免改 profile、自組 JSON 即開通）**：ComfyUI 核心節點 `MiniMaxH3ReferenceToVideo`（見 [`Comfy-Org/embedded-docs`](https://github.com/Comfy-Org/embedded-docs)）的 `ref_images` 為動態擴展槽，**原生支援最多 9 張參考圖**（`ref_image_0` .. `ref_image_8`，對齊 MiniMax H3 官方 Ref2VA 上限：圖 ≤9、影 ≤3 總長 ≤15s、音 ≤3、混合總數 ≤12）。因此，agy 只需自組一支 `h3_r2v_multiref.json`（擴充至 4–5 個 `LoadImage`）直接 POST 至 ComfyUI `/prompt`，**不需改動閘道 profile、不需安裝任何 custom node**。
   - **兩項關鍵工程避坑（一手查證發現）**：
     1. **`ref_image_size` 參數**：`MiniMaxH3ReferenceToVideo` 預設為 `"match"`（將參考圖降解析度加速），社群與文件明確指出切換為 **`"max"`**（保留最高 2048px 短邊細節）對保臉與微細節（如 1.2–1.5cm 淡舊眉尾疤）提升顯著；但在 L4 24GB 上拉高參考解析度會推升 VAE／VRAM 壓力，須納入冒煙觀測。
     2. **ComfyUI HTTP API 巢狀欄位坑**：以程式 POST `/prompt` 呼叫 `MiniMaxH3ReferenceToVideo` 時，巢狀字典鍵 `ref_images.ref_image_0..N` 必須遵守 ComfyUI 的 dotted-key 展開格式（`_io.build_nested_inputs()`），格式寫錯時 ComfyUI 可能**靜默丟棄多餘參考圖而不報錯**！冒煙首輪必須檢查 worker log 確認 4 張圖皆實際進入推論。
2. **最小冒煙測試設計（不執行，完整規格見下方第五節「SM-7 計畫書」）**：
   - 鎖定 **同一顆口型敏感特寫對白鏡（DEMO-02 S4：`「……你，怎知我名？」`，CU、4s 淨／5s 生成、`OUTFIT-02`）**，與已失敗的 Flow `veo-fast` 單首幀成片（`demo02/clips/S4.mp4`）直接橫向對照。
   - 採 **三組對照＋一條件組**：`既有失敗基線（Flow I2V）` vs `SM-7A-1（H3 單圖首幀）` vs `SM-7A-2（H3 V3 四圖一致性全套：首幀＋userface＋ancient-front＋ancient-45）` vs `條件組 SM-7B（RefMod：身分＋OUTFIT-02 雙槽疊加）`。
   - 於有效區間 `[+0.5s, 4.5s]` 等距抽 **5 幀**（`0.5s / 1.5s / 2.5s / 3.5s / 4.5s`，貫徹 §B.8「成片幀驗收，不以首幀為準」），量化／半量化檢核：**跨幀臉與年齡漂移**、**解剖學左眉尾傷痕側別與穩定率**、**`OUTFIT-02` 四項服裝細節逐幀核對表**、**既有 TTS 對嘴落差（±0.3s）**、**L4 峰值 VRAM 與單鏡耗時**。

---

### Q3｜Camera H3（`NyckM/3d-Camera-control-H3-Minimax`）評估

1. **是否存在**：**確定存在**。GitHub 倉庫為 [`NyckM/3d-Camera-control-H3-Minimax`](https://github.com/NyckM/3d-Camera-control-H3-Minimax)（由 Bruxos do VFX 開發，節點名 `bruxosdovfx • Camera H3`／H3 Camera Control v3）。
2. **授權條款**：**高風險——倉庫根目錄無標準開源 `LICENSE` 檔（無 MIT／Apache／GPL）**。依著作權預設，該自訂節點程式碼屬「保留全部權利（All Rights Reserved）」；README 僅提醒模型權重受原作者條款約束（明列 **MiniMax H3** 與 **Viggle Meridian**）。相較我方已核定之 CozyClay（AGPL-3.0，內部使用產出零傳染）與 Stage（MIT），法律明確度顯著較差。
3. **輸出物為何（Prompt 文字、控制影片，或兩者皆有）？**
   - **兩者皆有（分屬兩條管線模式）**：
     - **模式 1（核心 UI 節點 `Camera H3` ＋ `prompt_compose.py`）**：輸出 **`STRING` 軌跡提示詞與參數 metadata**（`RETURN_TYPES = ("STRING",)`），把使用者在 3D 球面畫布拖曳的 azimuth／elevation／distance 關鍵幀編譯成 H3 運鏡文字指令。**局限**：社群實測明確指出此模式本質只是「文字提示詞編譯器」，不具硬性幾何約束，複雜弧線仍常被 H3 模型自由發揮。
     - **模式 2（後續版本整合之幾何重控管線）**：對首幀或源片跑 **MoGe**（單圖／影片 3D 幾何深度估算）→ 依 Camera H3 虛擬相機路徑做 **Depth Warp 影片重投影** → 搭配 **Viggle Meridian**（`Meridian INT8` 或 `Meridian LoRA`）工作流驅動 MiniMax H3。
4. **對照附錄 A 已鎖定之 CozyClay（＋Stage 備援）——依減法紀律裁決**：

   | 評估維度 | CozyClay（現行 L3 唯一預設） | Camera H3（`NyckM`） | 勝負 |
   | :--- | :--- | :--- | :---: |
   | **硬體與閘道相容性** | **0 GPU**（Phase 3 瀏覽器零安裝；Phase 5 本機 `npx`＋27 工具 MCP） | 綁 ComfyUI 前端畫布，須**喚醒 Colab GPU 線上拖關鍵幀**（空轉燒 CU） | CozyClay 完勝 |
   | **場景擺位與前景遮擋** | 完整 3D 擺場（可排 S01 小舟＋空座前景＋人物走位＋首尾複用專案） | 僅圍繞單張底圖做球面相機／MoGe 深度變形，**無法擺設多物件前景與走位** | CozyClay 完勝 |
   | **額外模型負擔** | 零新模型（直出灰模 MP4＋首尾幀 PNG＋Depth 餵既有 `ref_video_0`／`h3-controlnet`） | 幾何模式須另裝 **MoGe ＋ Viggle Meridian 權重／LoRA**（爆 L4 VRAM＋多一層授權） | CozyClay 完勝 |
   | **H3 原生運鏡語言優勢？** | 附錄 A §A.2／§A.4 已由 `script_pack.json` 結構化欄位確定性衍生 H3 官方 12 原語英文句 | 靠人工滑鼠拖 UI 產出文字，**不可版控、不可自動化**，且複雜軌道文字仍不敵白膜幾何 | 我方 L1 完勝 |
   | **開源授權清晰度** | AGPL-3.0（明確、產出零傳染）；備援 Stage 為 MIT | **無 LICENSE 檔**＋額外牽涉 Viggle Meridian 條款 | CozyClay 完勝 |

- **Q3 裁決**：**REJECT（減法駁回）**。既不擊敗 CozyClay，也不構成互補——文字模式與我方 L1 結構化派生器重疊且無法自動化，幾何模式則比 CozyClay 重得多、鎖死 ComfyUI UI 且無清楚授權。堅守附錄 A 的 **L1 詞表＋L3 CozyClay（Stage 應急）** 單一標準。

---

### Q4｜Stable Yogi 11 Camera Shots 評估

1. **實質內容是「可收割的 Prompt 清單」還是「須導入的工作流」？**
   - 實查 Civitai（`MiniMax H3 Camera Shots - 11 Tested Prompt Moves v1.0`）、`stableyogi.com`、`comfy.icu` 與其 YouTube 實測說明：
     - 其包裝形式為「**一支標準 H3 Ref2VA ComfyUI JSON（`stableyogi-h3-reference-camera-shots.json`，1–2 張人物參考圖、8 秒輸出、低清 ~736×416 試跑）＋ 11 招實測運鏡提示詞與避坑紀錄**」。
     - 工作流本體**沒有任何特殊自訂節點或技術突破**——我方閘道現行 `h3-r2v` 完全等價，**絕無導入其工作流 JSON 的必要**。
     - 11 招實測運鏡涵蓋 `Push In`、`Pull Out`、`Pan Left/Right`、`Truck Left/Right`、`Tilt Up/Down`、`Pedestal Up/Down`、`Static`、`Tracking` 與 `Orbit` 測試——**全部屬於 MiniMax 官方 12 類原語的基礎子集**，且我方附錄 A §A.7 已核准從 MIT 授權的 `loopforge0/minimaxh3-shots-skills`（29 招複合鏡型，含完整成片驗證）合法改寫進 `bible/camera/named_shots.yaml`。
2. **授權與署名限制（關鍵紅線）**：
   - **`[未驗證／無明確商用授權]`**：經查 `stableyogi.com`、Civitai 與 `comfy.icu` 頁面，該資源包**未檢出 MIT、Apache-2.0 或 CC0 等明確開源商用授權宣告**（一般社群教學免費檔預設適用站方條款或僅供個人非商用實驗）。
   - 依我方附錄 A §A.7 對待無授權 `h3-camera-motion-lib` 的相同紀律：**嚴禁複製或改寫其提示詞原文進入 `bible/camera/named_shots.yaml`**。
3. **唯一可合法吸納的非著作權工程觀察（僅作原則驗證，零複製）**：
   - ① 實測證實純文字 `Orbit` 易退化為半殘弧線或形變 → 再次佐證我方將複雜弧線移交 L3 CozyClay 之正確性（可於 `arc-reveal-90` 的 `known_pitfalls` 註記）。
   - ② 先低清（~736×416 等級）驗運鏡方向再升頻 → 與我方 `DESIGN.md` v1.4 §V1.4-03（先 `544×960` 挑片再放大）完全同向。
- **Q4 裁決**：**REJECT（不導入工作流、不收割提示詞原文）**。我方 `bible/camera/named_shots.yaml` 維持以「官方 12 原語＋MIT `loopforge0/minimaxh3-shots-skills` 合法改寫＋我方實拍回填 `verified_9x16_status`」為唯一潔淨來源。

---

### Q5｜Character Swap LoRA（Alissonerdx／Akatz Labs）嚴格審查

1. **是否存在與權重可用性**：**兩套皆真實存在，權重均公開託管於 Hugging Face**：
   - **Akatz Labs**：[`akatz-ai/MiniMax-H3-Character-Swap-LoRA`](https://huggingface.co/akatz-ai/MiniMax-H3-Character-Swap-LoRA)（如 `h3_character_swap_v1.5.safetensors`、`h3_character_swap_pro4500_1000.safetensors` 約 **148 MB**，社群常見 rank-16；另有靜態換人版 `akatz-ai/MiniMax-H3-Image-Character-Swap-LoRA`）。
   - **Alissonerdx**：[`Alissonerdx/Minimax-H3-ComfyUI`](https://huggingface.co/Alissonerdx/Minimax-H3-ComfyUI)（**BFS Character Swap LoRA**：v1.0 約 620 MB → **v1.1 經 SVD 壓縮至約 80 MB**，每層動態秩 4–34、中位數 7；常搭配 `ComfyUI-BFSNodes` 切段工作流）。
2. **授權條款查核**：
   - **Akatz Labs**：標示為 **`minimax-h3-community-license-agreement`**（非 MIT／Apache；繼承 MiniMax H3 社群授權之**美／歐／英／韓地域限制**與 `NOTICE` 聲明義務）。
   - **Alissonerdx**：標示為 **`mixed-asset-licenses`**——其中 BFS Character Swap LoRA 允許免費及**商業影視使用**，但明訂：① 合併年總營收超過 **100 萬美元**須署名 `Alissonerdx` 與 `BFS Character Swap LoRA`；② **嚴禁作為遠端 API／SaaS 服務提供**；③ 倉庫內其餘衍生資產另受 MiniMax H3 社群條款約束。
3. **Colab L4（24GB）VRAM 適配與閘道相容性**：
   - **VRAM**：LoRA 檔本體僅 80–148 MB，靜態增幅極小；社群多在 24GB（RTX 4090）搭配 INT8／動態卸載實跑（宣稱極限可壓至 8GB 走 RAM offload）。但因推論時須**同時送入整段源影片 `<Video 1>` ＋ 目標角色圖 `<Picture 1>`**，在 L4 24GB 跑 9:16 `768×1344` 仍有高度 offload／OOM 風險（同 SM-3）。
   - **量化權重與蒸餾衝突（重大實務地雷）**：一手 ComfyUI 社群回報指出，在 MiniMax H3 的 **`w6a8`／`int8` 裁剪量化權重**上直接載入標準 LoRA 常出現 `[WARNING] lora key not loaded: blocks.*.adaln_proj.linear.lora_A.weight` 等掉鍵警告，導致 LoRA 效果大幅削弱或失效，往往須另掛相容層節點；且將換臉／換角 LoRA 疊在閘道預設的 **`TriPRISM TurboFusion 8-Step`** 合併權重上是否崩壞，屬 **`[未驗證]`** 高風險區。
4. **嚴格檢視：在我方產線有無正當定位？**
   - **嚴格判定：無（Out of Scope）**。五條理由：
     1. **解錯題**：DEMO-02 翻車是因為 Flow 單首幀 I2V 跨鏡漂移，而非「缺少真人表演底片換成范蠡」。我方目標是 AI 原生半自動／自動化短劇產線（快線 T2 須守 2.5–3.5 小時 SLA），**不假設 Creator 或演員每鏡實拍表演片**。
     2. **古裝輪廓與體態硬衝突**：Character Swap LoRA 會鎖住源片演員的體型輪廓、衣料擺動與光影。拿現代人實拍片（或外部素材）硬換成春秋深衣交領右衽＋高冠木笄／玉組佩（`OUTFIT-02`／`03`），極易在衣袖、冠飾與領襟處嚴重穿幫；且外部底片另生版權與肖像權風險。
     3. **無法保證微特徵與對嘴紅線**：換角 LoRA 並不解決解剖學左眉尾 1.2cm 淡舊疤痕或中文 TTS ±0.3s 精準口型問題。
     4. **結構重複**：若需純走位／運鏡傳遞，附錄 A 已鎖定 **CozyClay L3 白膜＋`ref_video_0`／`h3-controlnet`**；若需保臉，應走 **H3 多圖 Ref2VA（SM-7A）** 或條件升階 **RefMod（SM-7B）**。
     5. **唯一極端例外（不預裝、不進規格）**：僅在未來 Phase 5+ 若 Creator 明確決定「親自實拍一段現代服裝短獨白／特定肢體表演，再換臉成范蠡作為特別企劃片頭」時，才另開獨立一次性實驗，且須改走 A100＋非 TriPRISM 權重。
- **Q5 裁決**：**REJECT（嚴格判為 Out of Scope）**。

---

### Q6｜角色與運鏡提示詞分工原則（與 V3 餵圖順序一致之附錄 A 增修草案）

#### 1. 為什麼不能照抄社群句「`<Picture 1>` 只負責身份」？
- 依 `STORYBOARD-SPEC-V2.md` **§三 C 與 §六 V3**：`asset_refs` 的有序陣列與餵圖順序**永久鎖定為 `scene → characters → props`**。
- 依我方產線流程，多數 AI 鏡頭都有 QC-1 核准的 **首幀圖（`first_frame`，屬場景／開場定格錨點）** 接在 `ref_image_0`（即 **`<Picture 1>`**），角色定妝一致性圖接在 `ref_image_1..K`（即 **`<Picture 2..K>`**），道具接在更後槽位；只有在不送場景／首幀圖、純靠多張角色圖起算的鏡型中，角色圖才從 `<Picture 1>` 起編。
- 若規格硬寫「`<Picture 1>` 只負責身分」，當 `<Picture 1>` 實際是 QC-1 首幀時，會指令模型忽略核准好的場景構圖、段級光線鎖定（`light_lock_id`）與 `start_pose`，造成直接衝突！
- **正確寫法**：採 **「V3 槽位驅動分責（Role-Driven Division of Labor）」**，在 H3 官方 Ref2VA 六段式的 **`subject_definitions`** 與 **`retention_analysis`** 兩段中，依實際餵入槽位**顯式宣告每一輸入的唯一職權邊界**，並全程使用**正向保留語句**（嚴禁裸否定詞，符合 H3 特性與 §A.7 原則）。

#### 2. 建議增補至 `STORYBOARD-SPEC-V2.md` 附錄 A（§A.4「引擎 prompt 方言」H3 項下）之精準規格條文草案

> 以下為可直接貼入 `STORYBOARD-SPEC-V2.md` §A.4（緊接於現行 H3 Ref2VA 條文之後）的定稿文字草案：

```markdown
  - **Ref2VA 多參考分責條款（與 V3 `scene → characters → props` 順序一致）**：凡走 H3 Ref2VA（含 L1 多圖保臉鏡與 L3 白膜鏡），`ref_images` 餵圖順序嚴格繼承 V3（首幀／場景 → 角色一致性組 → 道具；若無首幀／場景圖則由角色組自 `<Picture 1>` 起順編），且衍生 prompt 必須於 `subject_definitions` 與 `retention_analysis` 兩段**顯式宣告各輸入之單一職權，禁止跨責混用**：
    1. **首幀／場景槽（`<Picture s>`，有首幀或 `role=scene` 時固定為 `<Picture 1>`）**：僅負責開場構圖、場景佈局、段級光線鎖定（`light_lock_id`）與起手姿勢（`start_pose`）；`retention_analysis` 標註 `partially_preserved`（保留開場構圖與光線基底，不鎖死後續表情與運鏡）。
    2. **角色身分槽（`<Picture c1..cN>`，`role=character`，一般為 `<Picture 2..K>`；無場景槽時為 `<Picture 1..K>`）**：**僅負責角色身分（臉部骨相、鎖定年齡、解剖學左眉尾傷痕、髮型剪影）與當鏡 `outfit_id` 服裝細節**，不負責運鏡、背景或站位；`retention_analysis` 強制標註 `fully_preserved`（且嚴禁混入他齡或他套服裝參考圖）。
    3. **道具槽（`<Picture p1..pM>`，`role=prop`，選填）**：僅負責指定道具外觀與材質（`attribute_transfer` 或 `fully_preserved`）。
    4. **參考影片槽（`<Video 1>`，僅 L3 白膜鏡使用）**：**僅負責運鏡軌跡、景別變化、視差與時間節奏**，不負責人物身分、服裝或灰模材質；`retention_analysis` 強制標註 `partially_preserved`，並以正向語句明示以寫實材質與角色身分槽外觀替換灰模表面（禁用裸否定詞）。
```

#### 3. 對應 H3 Ref2VA 六段式衍生句型範本（L1 多圖對白鏡 vs L3 白膜鏡）

- **L1 多圖保臉對白鏡（4 圖：`<Picture 1>` 首幀＋`<Picture 2..4>` 范蠡身分與 `OUTFIT-02`）**：
  ```text
  subject_definitions:
  <Picture 1> is the opening frame of [Shot 1], defining ONLY the night alley environment, cold-blue streetlamp lighting (LK-ALLEY-NIGHT), opening close-up framing, and starting posture.
  <Subject 1> is the late-30s East Asian man defined ONLY for facial identity, age, faint oblique scar at his anatomical left eyebrow tail (viewer's right), hairstyle, and Spring-Autumn coarse linen robe (OUTFIT-02) across <Picture 2>, <Picture 3>, and <Picture 4>.

  retention_analysis:
  <Subject 1> (from <Picture 2>, <Picture 3>, <Picture 4>): fully_preserved - maintain exact facial bone structure, 38-40 age appearance, faint scar on his anatomical left eyebrow tail (viewer's right), matte black cloth cap with plain wooden hairpin, and cross-collar y-shaped dark linen robe across every frame; identity and costume authority belong exclusively to <Picture 2>, <Picture 3>, and <Picture 4>.
  <Picture 1> ([Shot 1] opening frame): partially_preserved - preserve opening framing, dark wet alley background, and cold streetlamp lighting only while allowing natural facial micro-expressions, subtle breathing, and slow camera push-in.
  ```

- **L3 白膜運鏡鏡（多圖＋`<Video 1>` CozyClay 灰模）**：
  ```text
  subject_definitions:
  <Picture 1> is the realistic frame-0 reference defining ONLY the misty Lake Taihu environment, lighting, and photorealistic surface palette.
  <Subject 1> is the late-30s East Asian man defined ONLY for identity, anatomical left eyebrow-tail scar, hairstyle, and OUTFIT-02 linen robe from <Picture 2> and <Picture 3>.
  <Video 1> is the 3D greybox previs clip defining ONLY the camera arc trajectory, parallax, subject blocking, and timing.

  retention_analysis:
  <Subject 1> (from <Picture 2>, <Picture 3>): fully_preserved - carry facial identity, scar placement, and linen robe details exclusively from <Picture 2> and <Picture 3> across all frames.
  <Picture 1>: partially_preserved - supply photorealistic lighting, water mist, and natural wood textures.
  <Video 1>: partially_preserved - follow the exact camera trajectory, framing progression, parallax, and timing of <Video 1> only, rendering all surfaces in photorealistic live-action textures from <Picture 1> and <Subject 1>.
  ```

---

## 四、開拍前新增冒煙測試計畫：**SM-7 候選（H3 人物一致性與 RefMod 對照冒煙）**

> 銜接 `STORYBOARD-SPEC-V2.md` §A.9 既有清單（SM-1 至 SM-6），新增 **SM-7** 專責驗證 H3 路線之**跨幀人物保真、傷痕側別、服裝細節與口型貼合度**。**本階段僅設計、不執行**；開跑時建議與 **SM-1** 共用同一次 Colab session 以省下一次冷啟動開銷。

### 4.1 測試標的（單一高壓基準鏡）
- **選定鏡頭**：**DEMO-02 S4**（`「……你，怎知我名？」`｜特寫 CU｜`face_visible: true`、`lip_sensitive: true`｜`FANLI-OUTFIT-02` 春秋布衣｜入夜藍調巷弄 `LK-ALLEY-NIGHT`｜淨長 4s／生成 **5s**、24fps、9:16｜運鏡：`slow-push` 極緩推、`stable_control`）。
- **選鏡理由**：
  1. **已有失敗對照組（0 CU）**：`~/drama-line/demo02/clips/S4.mp4`（Flow `veo-fast` 單首幀 I2V）已於 QC-D 曝露臉／年齡漂移、傷痕移位、服裝細節變形與口型落差；首幀（`demo02/S4/2fc09afe-a604-4aeb-8451-5e646bba63bc_1.jpg`）與對白 TTS 皆已在磁碟就緒。
  2. **最嚴苛壓力場**：特寫 CU＋古裝高難度細節（交領右衽＋黑緇布冠＋素木笄）＋開頭閉唇後開口講中文台詞，能一次檢驗全部 DEMO-02 痛點。
- **固定不變量**：全部對照組鎖定相同 **2 組隨機種子（Seed A / Seed B）**、相同 5s／24fps／9:16 輸出、相同 H3 官方 Ref2VA 六段式提示詞（含 Q6 分責條款、`<d>[Chinese] ……你，怎知我名？</d>` 與 `non_diegetic_music: N/A`）。

### 4.2 實驗組設計（兩階段閘門，貫徹減法）

| 組別 | 執行條件 | 輸入配置（嚴守 V3 順序） | 閘道與權重設定 | 抽數 | 目的 |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Baseline** | 已有實檔 | Flow `veo-fast` 單首幀（`demo02/clips/S4.mp4`） | 已有失敗基準 | 0 | 對照起點（QC-D FAIL） |
| **SM-7A-1（單圖 H3）** | **必跑** | `<Picture 1>` = `S4` 首幀（1 張） | `minimax-h3-video` 預設 `TriPRISM` 8-step（L4 `w6a8`）、`ref_image_size = max`、L4 `0.4–0.5 MP`（`544×960`） | 2 | 驗證單換 H3 引擎、不加多參考圖是否仍漂移 |
| **SM-7A-2（原生四圖 H3）** | **必跑** | 自組 `h3_r2v_multiref.json`（免改 profile）：<br>`<Picture 1>` = `S4` 首幀（場景／光線）<br>`<Picture 2>` = `fanli-master-B-userface.png`（臉／疤／年齡）<br>`<Picture 3>` = `fanli-master-ancient-front.jpg`（OUTFIT-02 正面）<br>`<Picture 4>` = `fanli-master-ancient-45.jpg`（OUTFIT-02 45°＋左眉疤）<br>*（刻意排除 A/C 年齡與 OUTFIT-01/03 防汙染）* | 同上；**開跑必查 worker log 確認 `ref_image_0..3` 四槽皆綁定未被 API 靜默丟棄**；若 `ref_image_size=max` 觸發 L4 OOM，加測 `match` | 2 | **核心驗證**：免新工具靠原生多圖 Ref2VA 能否一次過 QC-D |
| **SM-7A-3（20-step 歸因）** | **條件（僅 7A-2 漂移時跑）** | 同 SM-7A-2 四圖輸入 | 切換同 profile 既宣告之 **`dit-official-ref2va-w6a8`**（20-step 非蒸餾） | 1 | 隔離「TriPRISM 8-step 蒸餾壓傷臉部」vs「原生多圖架構極限」 |
| **SM-7B（RefMod 升階）** | **條件（僅 7A-2＋7A-3 仍不過關，或 L4 吃 4 圖 OOM／超時 >10 分鐘時始啟動）** | 臨時於實驗 worker 安裝 `ComfyUI-MiniMaxH3Mod`（MIT），建兩顆分離 RefMod：<br>① `fanli_id_B.safetensors`（`identity`，6 張 Age-B 露臉圖）<br>② `fanli_outfit02.safetensors`（`clothing`，`ancient-front`＋`ancient-45`）<br>推論時 `MiniMaxH3RefModsLoader` 雙槽疊加＋`<Picture 1>`（S4 首幀） | 先測預設 `TriPRISM w6a8` 確認 hook 相容性；若異常切 `dit-official-ref2va-w6a8` | 2 | 驗證 RefMod 是否顯著擊敗原生多圖並相容閘道權重；過關才准將 `ComfyUI-MiniMaxH3Mod` 升格為 ADOPT |

### 4.3 驗收量測表（貫徹 §B.8「成片抽幀驗收，首幀過關不算數」）

對每支 5s 生成片，於有效剪輯區間 `[+0.5s, 4.5s]` 等距抽 **5 幀**（`0.5s / 1.5s / 2.5s / 3.5s / 4.5s`）逐項評分：

| 量測維度 | 驗收方式 | 合格門檻（SM-7 PASS 判準） |
| :--- | :--- | :--- |
| **1. 跨幀臉與年齡漂移** | 5 幀與 `fanli-master-B-userface.png` 並排目視盲比（若本機有 InsightFace 可輔跑 ArcFace 餘弦相似度紀錄）；檢查 `f_0 → f_end` 內漂移 | **5/5 幀**明顯為同一名 **38–40 歲**男子；零「換人／突然變年輕（如 DEMO-02 S3a）」現象 |
| **2. 解剖學左眉尾傷痕** | 逐幀標註傷痕位置（解剖左側＝正面畫面右側）與型態 | **≥4/5 幀**於角色解剖學左眉尾清晰可見 ~1.2–1.5cm 淡舊斜疤；**0/5 幀**遷移至右眉、臉頰或誇張紅腫 |
| **3. `OUTFIT-02` 服裝細節對照（§B.8 條款 1）** | 逐幀核對 4 項：① 交領右衽小寫 `y` 形＋深褐暗紋滾邊；② 啞光黑緇布冠＋素木笄（零現代低馬尾／額前垂絲／朝服玉簪）；③ 粗麻啞光肌理；④ 零禁則（零盤扣／紅金／手錶／文字） | **4/4 項**於 **5/5 幀**全數吻合，無逐幀變形或憑空生出配件 |
| **4. 對嘴與微表情貼合度** | 掛載既有 DEMO-01/02 中文 TTS 音檔 `「……你，怎知我名？」` 檢視起迄開口與神情 | 起段閉唇呼吸自然；起迄開口與 TTS 誤差 **≤ ±0.3s**；句末凝視穩住不僵硬；視覺口型評分 ≥ **3.8 / 5.0** |
| **5. 工程與資源遙測** | 記錄 Colab GPU 類型、峰值 VRAM（GB）、單鏡耗時（秒）、`ref_image_0..3` worker log 綁定確認、L4 是否 OOM | L4 24GB **0 OOM** 且單鏡 **≤ 10 分鐘**（否則對齊 SM-3 決策：H3 多圖特寫鎖 A100 或降 `544×960`＋後製放大） |

### 4.4 算力與時間成本預估

> 換算基準沿用本機 `BRIEF.md`（Colab 200 CU／月 ≈ 117 小時 L4 → **L4 ≈ 1.71 CU／小時**；A100 約 **11–13 CU／小時**）與 `DESIGN.md`（L4 單次 H3 暫估 ~5 分鐘；實際隨參考圖數量與步數波動，標註合理區間）。

| 階段 | 執行項目 | Colab L4（24GB）預估時間／CU | 若改跑 A100（80GB）預估時間／CU | 佔月額度（200 CU） |
| :--- | :--- | :---: | :---: | :---: |
| **冷啟動** | 喚醒 `minimax-h3-video`＋載入權重（與 SM-1 共用可攤提） | 5–8 分鐘（~0.15–0.23 CU） | 5–8 分鐘（~1.0–1.7 CU） | ~0.1%（L4） |
| **SM-7A 核心** | 7A-1（1 圖×2 抽）＋ 7A-2（4 圖×2 抽），共 4 支 5s 片 | 22–32 分鐘（~0.65–0.95 CU） | 8–12 分鐘（~1.5–2.5 CU） | **~0.4–0.6%（L4）** |
| **SM-7A-3（選跑）** | `dit-official-ref2va-w6a8` 20-step 歸因（1 抽） | ＋12–18 分鐘（~0.35–0.50 CU） | ＋4–6 分鐘（~0.8–1.3 CU） | ＋0.25%（L4） |
| **SM-7A 小計** | **零安裝原生多圖驗證總計** | **30–58 分鐘（~0.8–1.7 CU）** | **15–26 分鐘（~3.3–5.5 CU）** | **< 1%（L4）** |
| **SM-7B（條件）** | 臨時裝 `ComfyUI-MiniMaxH3Mod`＋建 2 顆 RefMod（~30 秒）＋跑 2 抽 | ＋20–25 分鐘（~0.6–0.8 CU）＋人工改設定 ~20 分鐘 | ＋10–14 分鐘（~2.0–3.0 CU） | ＋0.4%（L4） |

---

## 五、未驗證事項總表（明確揭露只讀查證邊界）

1. **`MiniMaxH3ReferenceToVideo` API 多槽傳遞**：透過 `comfy-colab-kit` POST 自組 4 槽 JSON（`ref_images.ref_image_0..3`）時，ComfyUI 是否完整接收全部 4 張圖而非靜默丟棄 → **列入 SM-7A 首項檢查**。
2. **`ref_image_size = "max"` 在 Colab L4 24GB 4 圖輸入下是否 OOM**：官方／社群建議開 `"max"` 保細節，但 L4 24GB（`0.4–0.5 MP`）疊 4 張 768×1376 參考圖的實際峰值 VRAM 未知 → **列入 SM-7A 實測**。
3. **`TriPRISM TurboFusion 8-Step`（`dit-triprism-w6a8`）對多圖保臉與口型的壓縮效應**：8-step 蒸餾權重是否比 20-step 官方權重更容易丟失 1.2cm 眉尾傷痕或服裝細節 → **列入 SM-7A-3 歸因對照**。
4. **`ComfyUI-MiniMaxH3Mod` 與 `dit-triprism-w6a8` 之實機相容性及 L4 建置／推論峰值 VRAM**：一手文檔未見該量化合併權重之實測回報 → **列入 SM-7B 條件驗證**。
5. **Stable Yogi 11 Camera Shots 授權原文**：僅能確認公開頁未附 MIT／Apache／CC0 商用授權，故從嚴採取不複製原文策略。

---

## 六、給 Creator 的下一步建議（決策點）

1. **拍板採納 Q6 分責條款**：將本備忘錄第三節 Q6 之「Ref2VA 多參考分責條款（對齊 V3 順序）」併入 `STORYBOARD-SPEC-V2.md` 附錄 A §A.4。
2. **拍板減法駁回清單**：確認將 **Camera H3（`NyckM`）**、**Stable Yogi 11 Shots 工作流／原文**、**Character Swap LoRA（Akatz Labs／Alissonerdx）** 列為不導入；**RefMod（`ComfyUI-MiniMaxH3Mod`）** 維持 **WATCH**（待 SM-7A 數據定奪）。
3. **核准將 SM-7 納入開拍前冒煙清單（§A.9）**：與 SM-1 合併於單次 L4 Session（合計 ~1.5–2.5 CU）一次測完「H3 運鏡服從度＋原生 4 圖人物／傷痕／服裝一致性」；若 SM-7A-2 直接過關，則**零新增工具、零 profile 改動**即可讓 H3 接手全部口型與臉部敏感對白鏡。
