# 分鏡規格 v2.3 修訂討論備忘錄：Seedance 生態方法與電影提示詞工藝收斂案（agy 工程立場）

> **文件定位**：規格修訂工程討論與條文草案（**不直接改動 `STORYBOARD-SPEC-V2.md`、`preflight_gate.py`、`diff_sheet_gen.py` 本體，不執行生成，不推 repo**）  
> **撰寫日期**：2026-11-28  
> **上游拍板前提**：Creator 2026-11-28 裁示「**只借方法，引擎維持 H3（＋Flow Omni 1.2 Flash＋Wan＋LTX＋ffmpeg_card）**」，不導入 Seedance 2.5 付費引擎、不安裝任何外部 skill。  
> **依據材料（本機實讀）**：
> - `~/drama-line/SEEDANCE-25-ECOSYSTEM-REF.md`（§二 1–7 項摘要）
> - `~/drama-line/CINEMATIC-PROMPT-CRAFT-REF.md`（Creator 2026-11-28 提供）
> - `~/drama-line/sm7a/SM7A_RESULT.md`（SM-7A 實測結果：原生 4 槽 H3 Ref2VA `max`／`0.5 MP`／L4 `4.67m`／`1.85 GiB` 餘裕；`<Pic 1>` 靜態缺陷不可覆寫；`45R` 水平翻轉 `左衽` 缺陷）
> - `~/drama-line/claytest/CLAY_TEST_RESULT.md`（L3 白膜實測結果：`ref_video_0 ≤ 0.35 MP`＋`match`＋`<Pic 1>` 場景錨＝`0.19%` 灰像素零滲漏；L4 峰值 `20.727 GiB`／餘 `1.307 GiB` VRAM、硬鎖 `≤5s`）
> - 現行規格與工具：`STORYBOARD-SPEC-V2.md`（v2.2 含附錄 A／B／C）、`tools/preflight_gate.py`、`tools/diff_sheet_gen.py`、`COSTUME_REGISTRY.md`、`MASTER_FACE_DECISION.md`、`FANLI_ALIVENESS.md`、`voices/FANLI.yaml`、`POSTPROD_AGY_MEMO.md`、`demo02/assemble.sh`，並直接目視核驗 `casting/master/fanli-modern-charactercard-main.png`、`fanli-modern-charactercard-expressions.png`、`fanli-master-ancient-45R.jpg` 與 `fanli-master-ancient-45R.v1-flip-defect.jpg`。
> - **資訊邊界誠實聲明**：Muse 側研究副本（`~/workspace/research_seedance/`）不在本機只讀範圍內，本文所有外部方法僅以 `SEEDANCE-25-ECOSYSTEM-REF.md` §二摘要為準；未見原文細節處（例如 woodfantasy `micro-expressions.md` 488 行之確切七分區原文詞條、liyue `multimodal-patterns.md` 原始欄位命名、allenGKC `references.md` 原始維度枚舉）一律標註 **`〔原 repo 細節未見，依我方產線實況收斂〕`**，絕不憑空揣測。

---

## 零、總覽裁決表（Items 1–7｜反對無腦照搬，全部對齊實測數據）

| 項目 | 來源 | 總裁決 | 一句話工程理由與主要反駁點 | 落點檔案 |
| :-: | :--- | :---: | :--- | :--- |
| **1** | 資產鎖定表＋「不繼承」欄（liyue）＋穩定主體數（woodfantasy §二 #7） | **ADAPT** | 採納結構化 `owns[]`／`never_inherit[]` 契約與角色預設值（避免每鏡手填膨脹）；**反對直接輸出裸否定詞進 H3 prompt**——改由編譯器轉為正向排他與正向替換句，並將 L4 實測參考數上限併入護欄。 | `STORYBOARD-SPEC-V2.md` §三 C／§A.4、`preflight_gate.py` |
| **2** | 一維度一權威（allenGKC） | **ADAPT** | 升格為 QC-0 機械規則 **V13**；**反駁「1 維度＝1 檔案」天真口徑**——SM-7A 實測已證同角色同服裝多角度（`cu`＋`45`＋`45R`）須共享單一權威組 `(dimension, scope_target)`，機械攔截跨齡／跨服裝／跨職責衝突與零權威孤兒資產。 | `STORYBOARD-SPEC-V2.md` §六 V13、`preflight_gate.py` |
| **3** | 跨鏡身分錨點清單（woodfantasy） | **ADAPT** | 形式化建立 `bible/anchors/FANLI.yaml` 鎖定四項時代條件錨點（眉疤、方孔錢、髮型剪影、左腕錶）；**反駁於 QC-1/QC-2 新增第 7 個頂層布林鍵**——沿用既有 `scar_side`＋時代參數化 `costume_4pt`＋`age_id`，避免雙重扣分與 schema 膨脹，並加 `preflight_gate.py` 跨時代禁詞硬閘。 | `bible/anchors/FANLI.yaml`、`STORYBOARD-SPEC-V2.md` §C.2、`diff_sheet_gen.py`、`preflight_gate.py` |
| **4** | 微表情詞庫＋L1–L4 強度（woodfantasy 488 行） | **ADAPT** | 依范蠡「低沉內斂」定調與 544×960/720p 可讀性，收斂自建 **4 分區 × ~32 詞條** `bible/performance/micro_expressions.yaml`＋L1–L4 標尺（范蠡常態上限 L3）＋反 AI 假臉衛生表；**反駁整包移植 488 行與 2 秒多段時間軸**（撞 V6 單鏡一轉折與 AI 假笑風險）。 | `bible/performance/micro_expressions.yaml`、`STORYBOARD-SPEC-V2.md` §B.2／§B.3、`preflight_gate.py` |
| **5** | 人物參考預設範圍＋未見側重建規則（liyue） | **ADOPT（並退役 Step 0 翻轉幾何法）** | 明確界定 `role=character` 預設涵蓋完整可見角色（跨時代餵現代基準臉必顯式縮限為 `face_only`）；**依 SM-7A 實勘證據正式退役 Step 0 水平翻轉法**（`45R.v1-flip-defect` 實證翻轉會靜默製造 `左衽` 與錯邊疤），全面改採未見側結構重建規則。 | `STORYBOARD-SPEC-V2.md` §三 C／§C.1、`preflight_gate.py` |
| **6** | 音色綁定句式（liyue／woodfantasy） | **REJECT（影片端無效）／LIGHT ADAPT（TTS 端微調）** | 我方全面走 ElevenLabs 鎖定 TTS、組裝捨棄原聲，在 H3 影片 prompt 做 per-line 音色綁定屬 **no-op 且浪費 token**；音色 ID 永久鎖死於 `bible/voices/*.yaml`（禁鏡級覆寫），僅輕量借鏡表演節奏參數（`pre_pause_sec`／`pace`／`volume`）補進 `dialogue[]`。 | `STORYBOARD-SPEC-V2.md` §三 A／§三 F、`preflight_gate.py` |
| **7a** | 電影優先序編譯規則（光→鏡→動→色→聲） | **ADAPT** | **採納為編譯排序規則**：Flow 直接取代 §五舊 Seedance 順序；H3 **維持官方六段／三段外殼不變**，於 `detailed_description` 內部強制「光→鏡／運鏡→可觀察動作→調色」前移；Wan 維持極簡無聲方言。**明文駁回**參考檔內「單鏡 `[Shot 1]/[Shot 2]` 多切鏡寫法」（違背 v2 原子鏡架構）。 | `STORYBOARD-SPEC-V2.md` §五／§A.4 |
| **7b** | 生成前六點檢查清單 | **ADOPT（去重為 4 項 Advisory `WARN`）** | 同意列為 `preflight_gate.py` **Advisory 警告類（不作硬閘、退碼仍為 0）**；去重已由 V1/V2/V6 硬閘覆蓋的 #2（單運鏡）與 #6（片長匹配），實作 4 項淨增語意提示（光源方向、可觀察動作、克制調色、聲音設計）。 | `STORYBOARD-SPEC-V2.md` §六、`preflight_gate.py` |
| **7c** | 聲音設計缺口（環境底噪／Foley 層） | **ADOPT** | DEMO-02 `assemble.sh` 實勘證實現行做法是「全剝音軌＋硬循環 S1 原音 7%（無段切、無 Foley、無閃避）」，長集跨場必現接縫穿幫。正式於 `script_pack` 與 `edit_manifest` 補齊三源環境層（`library_roomtone` 預設／`retained_native_bed` 嚴限無對白鏡／`generated_sfx_bed`）與校準至 `-14 LUFS` 的 dB 電平規範。 | `STORYBOARD-SPEC-V2.md` §二／§三 F、`edit_manifest.json`（v1.1）、`preflight_gate.py` |
| **7d** | 5–8 秒穩定區間 vs V1 引擎上限 | **ADAPT（確認不放寬＋收緊 L4 子分級）** | 參考檔 5–8s 指**生成總長**，對齊我方 `standard_0.5s` 裁切（+1.0s）即現行 V1 淨長 4.0–6.5s，**不放寬至 8s 淨長**；反依 SM-7A 與 Clay Test 實測（L4 餘裕僅 1.31–1.85 GiB），新增 **L4 算力子護欄**：`L3_clay_ref2v` 硬鎖生成 `≤5.0s`（淨 `≤4.0s`），4 槽 `max` H3 CU 建議生成 `≤5.5s`（淨 `≤4.5s`）。 | `STORYBOARD-SPEC-V2.md` §六 V1、`preflight_gate.py` |

---

## 一、逐項條文草案、Schema／工具增量、成本與裁決

---

### 項目 1｜資產鎖定表＋「不繼承」欄（liyue Scoped Contract）＋穩定主體數參考線

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #1（liyue `multimodal-patterns.md`）與 §二 #7（woodfantasy 穩定主體數經驗值）；實測校準：`claytest/CLAY_TEST_RESULT.md`（Condition 2 防灰模滲漏、Condition 3 L4 上限）與 `sm7a/SM7A_RESULT.md`（4 槽 `max` 實測）。  
> **資訊邊界**：〔原 repo `multimodal-patterns.md` 原始表頭欄位名未見，以下依摘要「來源＋借用特徵＋作用對象／時段＋受保護不變量＋明確不繼承項」收斂為我方 `asset_refs[]` 契約。〕

#### 1. 規格條文草案（可直接併入 `STORYBOARD-SPEC-V2.md` §三 C 與 §A.4）

```markdown
#### §三 C 增修：`asset_refs[]` 作用域契約（Scoped Reference Contract，v2.3）

1. **欄位結構（向下相容 v2.0）**：`asset_refs` 每筆由 `{asset_id, role}` 擴充為：
   `{asset_id, role, media_kind?, owns?, never_inherit?, scope_target?, scope_window?}`。
   - `role` ●：`scene`／`first_frame`／`character`／`prop`／`previs_video`（依 V3 餵圖序排列：`first_frame/scene → characters → props`；`previs_video` 獨立送 `<Video 1>` 槽）。
   - `owns[]` ○：受控維度枚舉（見 V13），宣告本資產唯一擁有的視覺職權；**未填時自動套用下方角色預設表**，避免常規鏡頭重複填寫。
   - `never_inherit[]` ◐：受控禁止繼承標籤（見下表）；具跨時代參考圖、含烘焙道具之定裝母圖（如手持竹簡之 `ancient-front`）、多格角色卡或 `L3` 灰模影片者**必填**（未填由編譯器按角色預設自動補齊並檢核衝突）。
   - `scope_target` ○：作用對象 ID（如 `FANLI`、`WITNESS-WOMAN-01`、`PROP-COIN`；全鏡維度預設 `"SHOT"`）。
   - `scope_window` ○：作用時段（預設 `"full"`；僅在開場鎖定首幀設 `"opening_only"` 時覆寫）。

2. **角色預設契約表（免手填基準）**：
   | `role` | 預設 `owns[]` | 預設 `never_inherit[]` |
   |---|---|---|
   | `first_frame`（QC-1 首幀） | `["framing_pose", "environment_lighting"]` | `["identity_override", "motion_lock", "overlay_text"]` |
   | `scene`（空景母圖 `LOC-*`） | `["environment_lighting", "style_palette"]` | `["native_audio", "overlay_text"]` |
   | `character`（同時代定裝母圖） | `["identity", "costume"]` | `["studio_backdrop", "source_lighting", "card_layout", "overlay_text", "native_audio"]` |
   | `prop`（獨立道具卡） | `["prop_appearance"]` | `["studio_backdrop", "source_lighting", "overlay_text"]` |
   | `previs_video`（L3 白膜 `<Video 1>`） | `["camera_motion", "blocking_timing"]` | `["clay_material", "environment_lighting", "identity_override", "native_audio"]` |

   *特例強制覆寫*：凡引用自帶非本鏡道具的母圖（如 `fanli-master-ancient-front.jpg` 帶竹簡、而本鏡空手），必於 `never_inherit[]` 顯式加註 `"baked_prop"`；凡引用跨時代角色圖（如古裝鏡餵現代 `userface`），必顯式將 `owns` 縮限為 `["identity"]` 並於 `never_inherit[]` 加註 `"costume"`（見 §三 C 人物參考範圍條款）。

3. **多參考主體與餵圖上限護欄（整合實測與經驗值）**：
   - 單鏡總圖像參考數：Colab L4 24GB 走 H3 `ref_image_size="max"` 硬上限 **≤4 張**（SM-7A 實測餘裕 1.85 GiB）；`L3_clay_ref2v` 走 `ref_image_size="match"` 硬上限 **≤3 張圖＋1 支灰模片**（Clay Test 實測餘裕 1.31 GiB）；A100／G4 建議上限 **≤5 張**（超出 6–8 張進入不穩區、硬上限 9 張）。
   - 單鏡獨立出鏡角色主體建議 **≤2 人**（超出 3 人以上或雙人多動作易串染，應優先拆正反打原子鏡）。

#### §A.4 增修：引擎方言對 `owns[]`／`never_inherit[]` 之編譯規則（v2.3）

- **H3（Ref2VA 六段式／Base 三段式）——嚴禁裸否定詞直出**：
  1. `owns[]` 編譯入 `subject_definitions` 與 `retention_analysis`，採**正向排他句**（`defining ONLY <owns_phrase>`），對齊既有 Q6 槽位分責條款。
  2. `never_inherit[]` **嚴禁直譯為 `do not inherit ... / no clay / no bamboo scroll`**（會誘發 H3 注意力反向聚焦並撞 `PROMPT_HYGIENE_NEGATION`），一律查表轉譯為**正向替換句**寫入 `retention_analysis` 或 `detailed_description`：
     - `clay_material` → `rendering all surfaces in photorealistic live-action textures from <Picture 1> and <Subject 1>`（Clay Test 實測 `0.19%` 灰像素驗證有效）
     - `studio_backdrop` / `source_lighting` → `placing <Subject 1> naturally into the environment and lighting exclusively defined by <Picture 1>`
     - `baked_prop` → `with empty hands`（或明寫本鏡實際持物，Clay Test 實測零竹簡殘留驗證有效）
     - `native_audio` → 依 `voice_mode` 與 `non_diegetic_music: N/A` 處理，不於視覺段提及原音
     - `overlay_text` / `card_layout` → `clean natural live-action frame with unobstructed surfaces`
- **Flow（Omni 1.2 Flash）**：
  - `owns[]` 轉為正向主語與場景鎖定語句；`never_inherit[]` 中屬動作／姿態類者轉正向替換（如 `empty hands`），屬純視覺偽影類者（`studio_backdrop`, `card_layout`, `overlay_text`, `clay_material`）併入句尾精簡 `Avoid:` 清單（嚴禁混入任何動作靜止否定詞）。
- **Wan（2.2）**：
  - 維持極簡動作方言，**不將 `owns[]`/`never_inherit[]` 契約句寫入 `video_prompt`**（Wan 僅吃單首幀 `i2v_first` 且對長規則句不敏感）；所有 `never_inherit[]` 規則強制於 **Stage 3 首幀 `image_prompt`** 完成淨化，經 QC-1 攔截後再送 Wan。
```

#### 2. Schema 與工具增量

- **`script_pack.json`（`2.2 → 2.3`）**：
  - `shots[].asset_refs[]` 新增選填鍵：`media_kind`（`"image" | "video"`，預設依 `role` 推導）、`owns`（`string[]`）、`never_inherit`（`string[]`）、`scope_target`（`string`）、`scope_window`（`"full" | "opening_only"`）。
  - 內部編譯器常數表新增 `NEVER_INHERIT_H3_POSITIVE_MAP` 與 `ROLE_DEFAULT_CONTRACTS`。
- **`preflight_gate.py` 新增規則 `ASSET_CONTRACT`**：
  1. `owns ∩ never_inherit != ∅` → `FAIL [ASSET_CONTRACT]`（同一資產不能同時擁有又禁止繼承同一屬性）。
  2. `control_method == "L3_clay_ref2v"` 時：缺 `scene`/`first_frame` 錨點（Clay Test Condition 2）或 `previs_video` 未含 `clay_material` 排除 → `FAIL [ASSET_CONTRACT]`；L4 預設檔下 `len(image_refs) > 3` → `FAIL [REF_COUNT_BUDGET]`。
  3. H3 `ref2v` `ref_image_size="max"`（L4 預設）：`len(image_refs) > 4` → `WARN [REF_COUNT_BUDGET]`（`>9` 為 `FAIL`）。
  4. 資產 ID 命中內建帶道具母圖清單（如 `fanli-master-ancient-front`）而本鏡 `action`/`prop` 未含竹簡且 `never_inherit` 未標 `baked_prop` → `WARN [ASSET_CONTRACT]`；資產 ID 命中多格角色表（`charactercard`）未裁單格直餵 → `FAIL [ASSET_CONTRACT]`（防 `card_layout` 拼貼滲漏）。
  5. 掃描 H3 `video_prompt` 不可出現裸翻譯句（`do not inherit`、`no grey clay`、`no studio background`）→ `FAIL [PROMPT_HYGIENE_NEGATION]`。

#### 3. 成本評估
- **上游填表**：因採「角色預設表＋特例覆寫」，90% 常規鏡頭 **+0 格**；僅跨時代參考、帶道具母圖或 L3 鏡增填 1–2 個標籤（~10 秒／鏡）。
- **工具實作**：`preflight_gate.py` 約 +70 行純 Python（~30 分鐘，0 新套件）。
- **算力／CU**：0 額外 CU；反因強制剔除未裁多格卡與 L4 餵圖超標防呆，避免 OOM 與灰模滲漏重抽。

#### 4. 裁決：**ADAPT**
- **採納核心**：liyue 的「正向職權＋明確不繼承」雙欄契約正好補上我方 Q6 分責條款缺的結構化資料面，並能直接把 Clay Test「強制 `<Pic 1>` 場景錨＋去竹簡替換」程序化。
- **反駁與改寫點**：① **拒絕強制每筆手填**（改為角色預設＋特例覆寫，守住減法紀律）；② **嚴禁把「不繼承」直譯成否定句送進 H3**（對齊我方已驗證的正向替換法則，否則反誘發灰模或背景污染）；③ **Wan 影片端豁免契約散文**，改於 Stage 3 首幀前段清乾淨。

---

### 項目 2｜一維度一權威（allenGKC）作為 QC-0 驗證原則

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #2（allenGKC `references.md`）；實測校準：`sm7a/SM7A_RESULT.md`（Group B 3 張同服裝不同角度角色圖共擔身分／服裝）、`H3_CONSISTENCY_CAMERA_AGY_MEMO.md` §三 Q1（嚴禁跨年齡／跨服裝混包）。  
> **資訊邊界**：〔原 repo `references.md` 的確切英文維度鍵名與實作細節未見，以下對齊我方既有 `script_pack` 維度收斂為 9 維受控枚舉。〕

#### 1. 規格條文草案（可直接併入 `STORYBOARD-SPEC-V2.md` §六新增規則 **V13**）

```markdown
| **V13 一維度一權威** | 單鏡所有參考資產（`asset_refs[]`＋`first_frame`＋`previs_video`＋段級 `bgm_cue`/`ambience`）對每個「`(維度, 作用對象)`」鍵僅允許 **唯一一個邏輯權威組（owner_group）**；同鍵出現 ≥2 個互斥權威即為衝突（硬駁回）；不擁有任何維度之孤兒資產強制移除（硬駁回）。同角色、同鎖定年齡帶、同 `outfit_id` 之多視角母圖（如 `ancient-cu`＋`ancient-45`＋`ancient-45R`）視為**同一權威組**，不計衝突。 | 全自動（QC-0 / `preflight_gate.py`） |
```

**附：V13 九大受控維度與權威組判定表（併入 §六註解或附錄 D）**

| 維度（`dimension`） | `scope_target` | 唯一權威組鍵（`owner_group_key`） | 典型衝突案例（必駁回） |
| :--- | :--- | :--- | :--- |
| `identity` | 角色 ID（如 `FANLI`） | `char_id + age_band`（同人同齡多視角共享 1 組） | 同鏡混餵 `fanli-master-A`（28 歲）與 `fanli-master-B`（38 歲）；或 `first_frame` 與 `character` 同時宣告擁有 `identity` |
| `costume` | 角色 ID | `char_id + outfit_id`（同套多視角共享 1 組） | 同鏡混餵 `OUTFIT-01`（現代西裝）與 `OUTFIT-02`（春秋布衣）且未把前者縮限為 `identity` only |
| `framing_pose` | `"SHOT"` | 單一 `asset_id`（通常為 `first_frame` 或 `ref_shot`） | 同鏡兩張不同構圖圖皆宣稱擁有 `framing_pose` |
| `environment_lighting` | `"SHOT"` | 單一 `asset_id`（`first_frame` 或 `LOC-*` 或 `LOC_rev`） | `first_frame` 與 `LOC-*` 同時擁有 `environment_lighting` 而未明確移交；或 L3 `<Video 1>` 灰模未排除光線權威 |
| `camera_motion` | `"SHOT"` | 單一來源（`L3`: `previs_video`；`L1`: `movement` 欄位；`L2`: `first+last`） | `L3` 白膜鏡同時給出與白膜軌跡矛盾的額外運鏡影片 |
| `blocking_timing` | `"SHOT"` | 單一來源（`L3`: `previs_video`；其餘由 `action`＋`performance_beat` 負責） | 兩支參考片同時控制走位節奏 |
| `prop_appearance` | 道具 ID（如 `PROP-COIN`） | 單一 `asset_id`（或所屬 `outfit_id`） | 獨立銅錢卡與含不同銅錢樣式之角色卡同時擁有 `PROP-COIN` |
| `audio_timbre` | 說話者 ID | 單一 `bible/voices/{speaker}.yaml`（全域鎖定） | 同一角色在單集／單鏡指派兩組聲線 |
| `style_palette` | `"SHOT"` | 段級 `light_lock_id`＋`scene` 母圖（單一來源） | 混入不同色盤／不同畫風之參考圖 |

#### 2. 機械檢查邏輯與錯誤輸出格式（`preflight_gate.py` 規則 `V13_SINGLE_AUTHORITY`）

**機械演算步驟**（輸入僅需 `script_pack.json` ＋ 可選 `assets_manifest.yaml` 元資料）：
1. 對每顆非 `cpu_card` 原子鏡，依 `asset_refs[]`（含展開的角色預設 `owns[]`）與 `first_frame` 建立所有參照項目清單。
2. 透過資產 ID 命名規範或 manifest 查表解析 `(char_id, age_band, outfit_id)`（例：`fanli-master-ancient-45R` → `("FANLI", "B", "FANLI-OUTFIT-02")`；`fanli-master-B-userface` → `("FANLI", "B", "FANLI-OUTFIT-01")`；`fanli-master-A` → `("FANLI", "A", "FANLI-OUTFIT-01")`）。
3. 逐筆檢查：
   - 若某 `asset_ref` 解析後 `len(owns) == 0` → 立即記 **`FAIL [V13_ORPHAN_ASSET]`**。
   - 將每個 `dim ∈ owns` 依 `(dim, scope_target)` 寫入 `authority_map[(dim, scope_target)][owner_group_key].append(asset_id)`。
   - 特例自動消歧：當同一鏡同時帶 `first_frame`（QC-1 已核准首幀，已含該場環境光）與 `role="scene"` 的 `LOC-*` 時，若兩者皆走預設而撞 `environment_lighting`，**強制要求明確擇一**（多圖 H3 鏡由 `<Pic 1>` 首幀擁有 `environment_lighting`、移除冗餘 `LOC-*` 以省 L4 VRAM；L3 白膜無首幀鏡則由 `<Pic 1>` `LOC-*` 擁有 `environment_lighting`）。
4. 遍歷 `authority_map`：凡任一 `(dim, scope_target)` 存在 `len(owner_groups) > 1` → 記 **`FAIL [V13_AUTHORITY_CONFLICT]`**。

**具體報錯範例**：
```text
FAIL [V13_AUTHORITY_CONFLICT] shot=S4: (dimension='costume', target='FANLI') has 2 competing owners: {'FANLI:FANLI-OUTFIT-01': ['fanli-master-B-userface'], 'FANLI:FANLI-OUTFIT-02': ['fanli-master-ancient-45', 'fanli-master-ancient-45R']}. Narrow 'fanli-master-B-userface' owns[] to ['identity'] and add 'costume' to never_inherit[].
FAIL [V13_AUTHORITY_CONFLICT] shot=S3a: (dimension='identity', target='FANLI') has 2 competing owners: {'FANLI:A': ['fanli-master-A'], 'FANLI:B': ['fanli-master-B-userface']}. Mixing age bands is forbidden.
FAIL [V13_ORPHAN_ASSET] shot=S1: asset_ref 'LOC-ALLEY-NIGHT' owns 0 dimensions after overrides; remove dead reference to preserve L4 VRAM/attention budget.
```

#### 3. 成本評估
- **上游填表**：**+0 格**（完全複用項目 1 的 `asset_refs[]`＋資產命名規則）。
- **工具實作**：`preflight_gate.py` 約 +90 行＋新增 4 個 `--selftest` 案例（~40 分鐘，純標準庫）。
- **算力／CU**：0 CU；機械清除孤兒參考圖可直接節省 L4 單鏡 ~35 秒取樣時間與 VRAM（SM-7A 實測 4 圖比 1 圖多 ~110s 取樣）。

#### 4. 裁決：**ADAPT**
- **反駁點**：allenGKC 原句若直譯為「每維度只能塞 1 張參考圖」，會**直接打死 SM-7A 已驗證的 4 槽 H3 Ref2VA 基線**（3 張同套服裝不同角度共鎖 `identity+costume`），也會打死 `2S` 雙人鏡。
- **收斂方案**：改為 **`(dimension, scope_target)` → 唯一邏輯權威組（`owner_group_key`）**，既保住 SM-7A 多視角互補，又能 100% 機械抓出跨齡、跨服裝、首幀＋空景重複餵圖、孤兒資產四大真實病灶。

---

### 項目 3｜跨鏡身分錨點清單（woodfantasy）與 QC-1／QC-2 鍵位映射

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #3（woodfantasy `multimodal-references.md`）；對齊本機 `MASTER_FACE_DECISION.md`、`COSTUME_REGISTRY.md`、`FANLI_ALIVENESS.md`、`tools/diff_sheet_gen.py`（現行 `QC1_CHECK_KEYS` 5 鍵、`QC2_CHECK_KEYS` 6 鍵），並經目視實勘 `casting/master/fanli-modern-charactercard-main.png` 與 `fanli-modern-charactercard-expressions.png`。

#### 1. 實圖勘驗關鍵發現（必載入錨點聖經）
目視檢查 Creator 新進現代角色卡（`fanli-modern-charactercard-main.png`、`fanli-modern-charactercard-expressions.png`）後確認兩處細節：
1. **左腕舊銅錶**：正面全身與左側全身清楚顯示**解剖學左腕**配戴舊銅圓殼、素白／米黃無字錶盤、深棕皮帶極簡腕錶（與 `COSTUME_REGISTRY.md` `FANLI-OUTFIT-01` 100% 一致）。
2. **方孔錢文字風險警示**：`fanli-modern-charactercard-expressions.png` 底部特寫格的古銅方孔錢表面出現了清晰擬古字跡（類「通寶」字樣），與我方 `COSTUME_REGISTRY.md`（錢面字跡磨淡不可讀）及 **V9 文字紅線**衝突——錨點聖經須明確規定「正式生成鏡以**磨損不可讀包漿面**為準，角色卡錢面特寫格不可原樣直接餵入特寫鏡」。
3. **小痣不升格為硬錨點**：表情卡唇部特寫見下巴微小黑點，但在 `544×960`／`720p` 壓縮下屬次像素雜訊，不列跨鏡硬錨點（避免虛假 FAIL）。

#### 2. 聖經檔案草案：`bible/anchors/FANLI.yaml`（正式形式化）

```yaml
# bible/anchors/FANLI.yaml — 范蠡跨鏡身分錨點唯一準據（v2.3）
# 對應身分基準：MASTER_FACE_DECISION.md｜對應服裝：COSTUME_REGISTRY.md
char_id: FANLI
status: LOCKED
canonical_age_band: B   # 38-40 歲（A=~28, C=~60 僅限顯式跨齡鏡）
identity_master: casting/master/fanli-master-B-userface.png

anchors:
  - anchor_id: ANC-FANLI-01
    name: 左眉眉尾淡舊斜疤
    category: permanent_anatomical
    applies_to_eras: ["春秋", "2022", "2026"]
    applies_to_outfits: ["FANLI-OUTFIT-01", "FANLI-OUTFIT-02", "FANLI-OUTFIT-03", "FANLI-OUTFIT-04"]
    spec:
      anatomical_side: left_eyebrow_outer_tail
      screen_side_frontal: viewer_right
      length_cm: "1.2-1.5"
      appearance: "陳年癒合淡膚色微斜舊痕，輕微切斷眉尾毛流；嚴禁紅腫新鮮傷或跨臉頰刀疤"
    visibility_by_scale:
      required_visible: ["CU", "ECU", "MCU"]   # 僅當 subject_facing ∈ {front, left}
      clean_opposite_required: ["CU", "ECU", "MCU"]  # subject_facing == right 時，畫面左側右眉必 100% 無疤
      optional_in: ["MS", "LS", "ELS", "2S", "OTS"]
    qc_gate_key: scar_side
    prompt_en_positive: "faint 1.5cm old healed diagonal scar at the outer tail of his anatomical left eyebrow (viewer's right), anatomical right eyebrow completely clean"

  - anchor_id: ANC-FANLI-02
    name: 時代條件髮型剪影
    category: era_conditioned_silhouette
    variants:
      modern:
        applies_to_eras: ["2022", "2026"]
        applies_to_outfits: ["FANLI-OUTFIT-01"]
        spec: "自然黑長髮後收露額、前額／右鬢留 1-2 縷細軟垂絲、頸後低於耳垂線啞光黑繩低束 5-8cm 短小髮尾"
        forbidden_in_variant: ["古裝束髻", "緇布冠", "高冠", "木笄", "玉簪", "高馬尾", "厚齊劉海"]
        prompt_en_positive: "black hair swept back exposing forehead, one or two fine loose strands by the right temple, tied low at the nape into a neat 6cm short low tail"
      ancient_outfit02:
        applies_to_eras: ["春秋"]
        applies_to_outfits: ["FANLI-OUTFIT-02"]
        spec: "全髮上收緊貼束髻頭頂，戴素面啞光黑緇布冠、貫素木笄、垂黑布組纓；零額前碎髮與低馬尾"
        forbidden_in_variant: ["現代低馬尾", "額前垂絲", "朝服高冠", "玉簪", "明清辮子"]
        prompt_en_positive: "hair gathered cleanly into a topknot under a matte black cloth cap secured by a plain wooden hairpin with hanging black cloth ties"
      ancient_outfit03:
        applies_to_eras: ["春秋"]
        applies_to_outfits: ["FANLI-OUTFIT-03"]
        spec: "全髮上收束髻，戴挺括立體摺紋黑色正式高冠、貫淡青白玉簪、垂黑絲冠纓"
        forbidden_in_variant: ["現代低馬尾", "額前碎髮", "素木笄", "布衣緇布冠"]
        prompt_en_positive: "hair gathered into a topknot under a structured pleated black formal court cap secured by a pale jade hairpin"
    qc_gate_key: costume_4pt   # 對應服裝四項之第 ② 項（冠飾與髮型）；跨齡銀髮比另受 age_id 檢核

  - anchor_id: ANC-FANLI-03
    name: 古銅方孔錢（現代限定信物）
    category: era_conditioned_prop
    allowed_eras: ["2022", "2026"]
    allowed_outfits: ["FANLI-OUTFIT-01"]
    forbidden_eras: ["春秋"]
    forbidden_outfits: ["FANLI-OUTFIT-02", "FANLI-OUTFIT-03", "FANLI-OUTFIT-04"]
    spec:
      handedness: "anatomical_right_hand（或平壓於桌面紙本合約角）"
      diameter_cm: "3.8-4.5"
      surface_rule: "暗褐古銅包漿、圓廓厚邊、方孔清晰、錢面字跡磨淡至完全不可辨讀（覆寫角色卡特寫格擬古字樣，嚴守 V9）"
      presence_rule: "現代戲僅於劇本指定思考／決斷／收尾鏡入鏡，非每鏡強制出現；春秋古裝戲 100% 硬禁（春秋晚期尚未出現方孔圓錢）"
    qc_gate_key: costume_4pt   # 對應第 ③ 項配件／第 ④ 項時代禁則
    prompt_en_positive: "substantial 4cm antique dark aged-bronze round coin with crisp square center hole and heavily worn unreadable surface"

  - anchor_id: ANC-FANLI-04
    name: 舊銅殼極簡腕錶（現代限定・左腕）
    category: era_conditioned_accessory
    allowed_eras: ["2022", "2026"]
    allowed_outfits: ["FANLI-OUTFIT-01"]
    forbidden_eras: ["春秋"]
    forbidden_outfits: ["FANLI-OUTFIT-02", "FANLI-OUTFIT-03", "FANLI-OUTFIT-04"]
    spec:
      anatomical_side: "anatomical_left_wrist（正面視角畫面右側手腕）"
      appearance: "氧化舊銅圓殼、極簡素面米白錶盤（無可讀品牌標誌）、深棕皮錶帶"
      presence_rule: "現代戲凡左腕露框時必在位且不得換到右腕；春秋古裝戲 100% 硬禁"
    qc_gate_key: costume_4pt   # 對應第 ③ 項配件／第 ④ 項時代禁則
    prompt_en_positive: "minimalist oxidized aged-bronze wristwatch with plain unbranded cream dial and dark brown leather strap on his anatomical left wrist"
```

#### 3. 規格條文草案（併入 `STORYBOARD-SPEC-V2.md` §C.2）

```markdown
#### §C.2 增補：身分錨點與 QC-1／QC-2 鍵位映射規則（v2.3）

1. **單一準據**：主要角色（首期 `FANLI`）須於 `bible/anchors/{CHAR_ID}.yaml` 登錄 3–4 項永久或時代條件可視錨點，標明解剖側別、景別可見門檻、時代允許／禁則與對應 QC 鍵。
2. **不新增 QC 頂層鍵（維持 5 鍵／6 鍵減法結構）**：`qc1_gate.json`（5 鍵：`age_id`, `scar_side`, `costume_4pt`, `light_lock`, `pose_spatial`）與 `qc2_gate.json`（6 鍵：另加 `expression_lip`）**不增設獨立 `anchors` 頂層鍵**，避免與 `scar_side`／`costume_4pt` 重疊扣分。四項錨點精確映射如下：
   - **左眉尾淡疤（`ANC-FANLI-01`）** → 直接鎖死於 **`scar_side`**。
   - **時代髮型剪影（`ANC-FANLI-02`）** → 併入 **`costume_4pt` 第 ② 項（髮型與冠飾）**，年齡髮色比並入 **`age_id`**。
   - **現代方孔錢（`ANC-FANLI-03`）與左腕舊銅錶（`ANC-FANLI-04`）** → 併入 **`costume_4pt` 第 ③ 項（配件／左右手位置）與第 ④ 項（時代禁則）**——現代 `OUTFIT-01` 驗「左腕錶／右手無字方孔錢（露手時）／零古裝」；春秋 `OUTFIT-02/03` 驗「零方孔錢／零腕錶／交領右衽 `y` 形／冠笄玉佩」。
3. **視覺表自動帶出**：`diff_sheet_gen.py` 讀取 `bible/anchors/{char_id}.yaml`，依該鏡 `time_layer`＋`outfit_id`＋`subject_facing` 於 Col 0／Col 2 自動印出「本鏡必現錨點 vs 時代禁則清單」，人工審表零查表翻頁成本。
```

#### 4. Schema 與工具增量
- **新增檔案**：`bible/anchors/FANLI.yaml`（repo 與本機同步）。
- **`diff_sheet_gen.py`**：新增可選參數 `--anchors-dir bible/anchors/`；**`QC1_CHECK_KEYS` 與 `QC2_CHECK_KEYS` 保持完全不變**（100% 向下相容既有 `demo02_qc1_gate.json`／`demo02_qc2_gate.json`）；僅於 `Col 0`／`Col 2` 標籤欄動態渲染該鏡時代的 4 項錨點摘要，並於 `qc*_gate.json` 單鏡層增選填 `failed_anchor_ids: []` 供退回定位。
- **`preflight_gate.py` 新增規則 `ERA_ANCHOR_CONFLICT`（硬閘 `FAIL`）**：
  - 依 `segments[].time_layer` 與 `shots[].outfit_id` 讀取 `bible/anchors/FANLI.yaml` 的 `forbidden_eras`/`forbidden_outfits`/`forbidden_in_variant`：
    - 春秋／`OUTFIT-02`/`03` 鏡之 `action`/`image_prompt`/`video_prompt` 出現 `方孔錢`、`銅錢`、`square-hole coin`、`腕錶`、`手錶`、`wristwatch`、`低馬尾`、`low ponytail`（排除 `avoid:` 區塊後）→ `FAIL [ERA_ANCHOR_CONFLICT]`。
    - 現代 `2022`/`2026` 穿 `OUTFIT-01` 出現 `緇布冠`、`木笄`、`topknot`、`交領深衣`（排除 `avoid:` 區塊）→ `FAIL [ERA_ANCHOR_CONFLICT]`。
    - 現代鏡提及腕錶寫成 `right wrist`／`右腕` 或方孔錢提及可讀字跡 → `FAIL [ERA_ANCHOR_CONFLICT]`。

#### 5. 成本評估
- **上游填表**：**+0 格**（完全靠既有 `time_layer`、`outfit_id`、`subject_facing` 查表）。
- **工具實作**：建 `FANLI.yaml`（15 分鐘）＋`preflight_gate.py` 約 +55 行＋`diff_sheet_gen.py` Col 2 文字掛鉤約 +35 行（總計 ~1 小時）。
- **算力／CU**：0 CU。

#### 6. 裁決：**ADAPT**
- **明確回答「`costume_4pt` 夠不夠，需不需要獨立 `anchors` 鍵？」**：**`scar_side` ＋ 時代參數化 `costume_4pt` ＋ `age_id` 完全足夠，反對新增第 7 個頂層 QC 鍵。** 原因：① 四項錨點在既有鍵位已有 1 對 1 歸宿，新增鍵會造成「漏錶算 `costume_4pt` 還是 `anchors` FAIL」的稽核歧義；② 現行 `diff_sheet_gen.py` 與 gate JSON 剛完成交付驗收，零破壞性擴充（動態印出時代錨點提示＋`preflight` 時代禁詞硬閘）的投資報酬率遠高於改動 gate schema。

---

### 項目 4｜微表情詞庫＋強度分級（woodfantasy `micro-expressions.md`，488 行）

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #5（woodfantasy `micro-expressions.md`，488 行：七分區、L1→L4、2 秒時間軸、反 AI 假臉禁忌詞）；對齊我方 `voices/FANLI.yaml`（*calm and inward-looking, restrained emotion, speaks softly but every word lands, minimal inflection*）、`FANLI_ALIVENESS.md`（慢眨眼、停頓半拍、久視、對螢幕光微瞇眼）與 `DIRECTOR_LAYER_AGY_MEMO.md`（`performance_beat`＋720p 20px 虹膜物理極限）。  
> **資訊邊界**：〔原 repo `micro-expressions.md` 488 行全文未見，不猜測或照搬其原詞表；以下完全按我方范蠡定調、實測解析度（`544×960`／`720p`）與引擎特性，自建有界詞表，比照 `bible/camera/named_shots.yaml` 先例。〕

#### 1. 裁剪論證（為何絕不整包移植 488 行）
1. **裁掉 7 分區中的 3 個低訊噪比／易穿幫分區**（臉頰鼓動、鼻翼細節、全臉誇張肌肉群）：在 Colab L4 `544×960` 與 `720p` 下，鼻翼微張 1mm 或瞳孔細微擴縮屬次像素細節，寫進 prompt 只會誘發模型擅自拉近景別或扭曲五官（已由 `preflight_gate.py` Rule g `SCALE_JUMP_BAN` 封殺）；且過度牽動左眉肌肉會撕裂 1.2cm 左眉淡疤錨點。**收斂為 4 個高可讀分區**：`Z1 眼瞼與視線`、`Z2 眉心與眉弓`、`Z3 唇線與下顎`、`Z4 呼吸與肩頸`（Z4 在 `MS`/`2S` 依然清晰可讀，直接支撐 `TWO_SHOT_MICRO_MOTION`）。
2. **裁掉「單鏡內 2 秒精度多段情緒時間軸」**：直接與我方 **V6（單鏡動詞轉折 ≤1 次）** 與 **4–5.5s 有效鏡長**衝突。在單顆 5s AI 鏡裡硬排 3 個 2 秒表情翻轉，只會讓 H3/Flow 演成鬼畜抽搐。我方維持「**單鏡僅 1 次 `from → trigger → to` 狀態位移**」，多段弧線交給剪輯跨鏡推進。
3. **裁掉 L4 戲劇爆發詞表（哭嚎、大笑、怒目咆哮、張嘴錯愕）**：與范蠡「兩千五百年商聖、低沉內斂」聲線（`FANLI.yaml`）根本違背，且大張嘴／露齒大笑是 AI 影片最容易破相（六顆門牙、假牙釉質反光）的失敗模式。L4 僅保留為**配角／對手專用檔位**，范蠡常態硬鎖 **L1–L2**、極端危機上限 **L3**。

#### 2. 自建有界詞表草案：`bible/performance/micro_expressions.yaml`（精簡 4 分區 × 24 核心詞條）

```yaml
# bible/performance/micro_expressions.yaml — 表演微表情有界詞表（v2.3）
# 比照 bible/camera/named_shots.yaml 自建原則：全正向可觀察物理句，零裸否定詞
version: "2.3"

intensity_scale:
  L1:
    label: 極克制・內斂微動（Baseline Restrained）
    zones_active: 1
    fanli_budget: "預設主力（~70% 鏡頭）；適用 deliberate_hold=true、stable_control、cold_observe"
    min_shot_size: "MS"
  L2:
    label: 克制轉折・可讀訊號（Controlled Shift）
    zones_active: "1-2"
    fanli_budget: "交鋒／反問／判讀主力（~25% 鏡頭，如 DEMO-02 S4、EP-01 S06/S17）"
    min_shot_size: "MCU"
  L3:
    label: 壓抑張力・危機臨界（Contained Tension）
    zones_active: "2-3（含 Z4 呼吸肩頸）"
    fanli_budget: "范蠡上限（≤5% 鏡頭，僅限穿越失重／突發異象如 DEMO-02 S1/S3a/S3b）"
    min_shot_size: "MS"
  L4:
    label: 外放情緒・明確失控（Overt Outburst）
    zones_active: "3-4"
    fanli_budget: "范蠡預設禁用（觸發 preflight WARN，須填 intensity_override_reason）；僅供目擊者／對手配角使用"
    min_shot_size: "MS"

zones:
  Z1_gaze_eyelids:
    - id: z1_slow_blink
      level: L1
      min_shot_size: MCU
      zh: 緩慢深眨眼（約 0.4 秒，時間感比旁人慢半拍）
      en: "unhurried slow deliberate blink, eyelids closing calmly and reopening without haste"
    - id: z1_steady_hold
      level: L1
      min_shot_size: MCU
      zh: 沉靜久視（對方講完仍不移開目光）
      en: "heavy steady gaze resting calmly forward, upper eyelids slightly relaxed and unbothered"
    - id: z1_object_to_person
      level: L2
      min_shot_size: MCU
      zh: 先看物再只抬眼看人（不急著抬頭）
      en: "eyes held on the object for a beat before slowly lifting only his gaze to meet the speaker"
    - id: z1_glare_squint
      level: L2
      min_shot_size: MCU
      zh: 對冷白螢幕或強光極輕微瞇眼
      en: "brief subtle narrowing of the eyelids against the bright glare before shifting gaze smoothly"
    - id: z1_sharp_lock
      level: L2
      min_shot_size: CU
      zh: 眼神定住收束（聽見關鍵詞時警覺凝神）
      en: "eyes subtly focusing and locking forward with quiet guarded sharpness"
    - id: z1_startled_snap
      level: L3
      min_shot_size: MS
      zh: 驟然側目轉頭盯向異光源（轉幅守 ±30° 內）
      en: "head turns briskly within thirty degrees toward the sudden light source, eyes alert and guarded"

  Z2_brow_glabella:
    - id: z2_hairline_knit
      level: L1
      min_shot_size: CU
      zh: 眉心極輕微收攏（不破左眉尾疤線）
      en: "faint tension gathering briefly between the inner brows while keeping the outer brow line natural"
    - id: z2_brow_settle
      level: L1
      min_shot_size: CU
      zh: 眉骨緩沉鬆回（看穿局勢後的平靜）
      en: "inner brows gradually softening and settling into quiet composure"
    - id: z2_skeptical_furrow
      level: L2
      min_shot_size: CU
      zh: 審視性微蹙眉（冷靜質疑，非憤怒皺眉）
      en: "restrained analytical furrow between the brows, eyes narrowed slightly in quiet skepticism"
    - id: z2_alert_tension
      level: L3
      min_shot_size: MCU
      zh: 戒備繃眉（遇未知威脅）
      en: "brows drawing tighter with tense alertness, face taut under the alley light"

  Z3_mouth_jaw_chin:
    - id: z3_closed_still_lips
      level: L1
      min_shot_size: MS
      zh: 雙唇自然閉合（無對白／畫外音必鎖）
      en: "lips resting naturally and completely closed with relaxed mouth corners"
    - id: z3_jaw_clench
      level: L2
      min_shot_size: CU
      zh: 下顎微收緊（壓住情緒不發作）
      en: "jawline tightening faintly for a moment as he keeps his lips closed"
    - id: z3_chin_tuck
      level: L2
      min_shot_size: MCU
      zh: 下巴微收半寸（開口反問前壓穩氣場，DEMO-02 S4 簽名）
      en: "chin dipping slightly inward half an inch as he steadies himself before speaking"
    - id: z3_quiet_part_speak
      level: L2
      min_shot_size: CU
      zh: 唇線小幅度克制開啟吐字（配合 <d> 對白本文）
      en: "lips parting slightly with restrained, minimal articulation as he speaks quietly"
    - id: z3_swallow_hold
      level: L2
      min_shot_size: MCU
      zh: 輕微吞嚥喉結微動後定神
      en: "subtle swallow along his throat, jaw settling back into calm stillness"

  Z4_breath_neck_shoulders:
    - id: z4_calm_breath
      level: L1
      min_shot_size: MS
      zh: 胸肩平緩極微起伏（雙人鏡／靜止反應必備活人感）
      en: "subtle slow rise and fall of his chest and shoulders with calm measured breathing"
    - id: z4_pre_line_exhale
      level: L1
      min_shot_size: MCU
      zh: 開口前極輕緩吐氣半拍、雙肩微沉
      en: "quiet measured exhale with shoulders settling a fraction lower before speaking"
    - id: z4_weight_shift
      level: L1
      min_shot_size: "2S"
      zh: 站姿重心極微轉移（打破 2S 蠟像僵直）
      en: "subtle barely perceptible shift of weight across his stance while breathing steadily"
    - id: z4_heavy_heave
      level: L3
      min_shot_size: MS
      zh: 失衡扶牆後的急促喘息肩部起伏（DEMO-02 S1）
      en: "chest and shoulders heaving visibly with ragged, rapid breathing while bracing against the wall"
    - id: z4_back_brace
      level: L3
      min_shot_size: MS
      zh: 肩背驟繃貼牆、手臂警戒收緊（DEMO-02 S3b）
      en: "shoulders drawing back firmly against the damp wall with taut breathing"

  supporting_L4_only:
    - id: z_sup_double_take_retreat
      level: L4
      min_shot_size: MS
      allowed_speakers: ["SUPPORTING", "WITNESS"]
      zh: 目擊者明顯驚愣、後退半步、急促眨眼舉手機
      en: "eyes widening briefly in shock, stepping back half a pace with rapid nervous blinks and tense breathing"

anti_ai_face_hygiene:
  # 禁出現在上游 microexpression / prompt 的「假臉／過演／空泛情緒詞」
  banned_overacting_en:
    - "exaggerated gasp"
    - "jaw drops wide open"
    - "wide toothy grin"
    - "radiant smile"
    - "commercial smile"
    - "maniacal"
    - "dramatic tears"
    - "porcelain skin"
    - "flawless airbrushed skin"
    - "beauty filter"
    - "overly symmetrical model face"
  banned_abstract_only_zh:
    - "感到難過"
    - "很生氣"
    - "非常震驚"
    - "表情複雜"
    - "內心掙扎"
    - "露出微笑"   # 對范蠡發 WARN（常誘發廣告假笑）
  # 編譯端輸出對策（分引擎）
  compiler_flow_avoid: "plastic airbrushed skin, beauty filter, exaggerated theatrical expression, stiff wax-figure stare, wide commercial smile"
  compiler_h3_positive_guard: "authentic natural skin texture with subtle pores, restrained understated facial movement, lifelike subtle breathing"
```

#### 3. 規格條文草案（併入 `STORYBOARD-SPEC-V2.md` §B.2 與 §B.3 V12b）

```markdown
#### §B.2／§B.3 V12b 增修：微表情強度標尺與詞庫綁定（v2.3）

1. **`performance_beat` 欄位擴充（向下相容）**：
   `performance_beat: {from, trigger, to, deliberate_hold, intensity?: "L1"|"L2"|"L3"|"L4", lexicon_ids?: string[], intensity_override_reason?: string}`。
   - `intensity` ○：未填時 `deliberate_hold=true` 預設 `L1`，其餘預設 `L2`。
   - **角色上限紀律**：范蠡常態鎖定 `L1`（約 70%）與 `L2`（約 25%），危機拍點上限 `L3`（≤5%）；`L4` 僅供配角／目擊者使用，若標於范蠡須經導演特批並填 `intensity_override_reason`。
   - `lexicon_ids[]` ○：可選填 `bible/performance/micro_expressions.yaml` 受控 ID（單鏡最多 2–3 項，對應 `from`／`to` 兩端，嚴禁在單鏡內硬塞多時間點情緒翻轉）。
2. **景別耦合規則**：凡 `lexicon_ids` 含 `min_shot_size: CU/MCU` 之詞條（如 `z2_hairline_knit`、`z3_jaw_clench`），不得配發於 `MS/LS/ELS` 鏡（防誘發跨尺幅變形）；`2S` 雙人鏡優先必選至少一項 `Z4` 詞條（`z4_calm_breath`／`z4_weight_shift`）以自動滿足 §B.8-5。
3. **反 AI 假臉衛生**：`microexpression` 與衍生 prompt 嚴禁出現美顏塑膠肌、商業假笑與誇張過演詞（見詞庫 `anti_ai_face_hygiene`）；Flow 編譯入 `Avoid:`，H3 編譯為正向膚質與克制動態護欄句。
```

#### 4. Schema 與工具增量
- **新增檔案**：`bible/performance/micro_expressions.yaml`（~24–30 條，輕量可維護）。
- **`script_pack.json`**：`shots[].performance_beat` 增選填 `intensity`、`lexicon_ids[]`、`intensity_override_reason`。
- **`preflight_gate.py` 新增規則 `PERF_LEXICON_GATE`**：
  - `deliberate_hold == true` 且 `intensity ∈ {"L3", "L4"}` → `FAIL [PERF_INTENSITY_CONFLICT]`（定格留白與高張力爆發語意衝突）。
  - `intensity == "L4"` 且鏡頭主角為 `FANLI` 且無 `intensity_override_reason` → `WARN [PERF_INTENSITY_CEILING]`。
  - `lexicon_ids[]` 命中未定義 ID → `FAIL [PERF_LEXICON_UNKNOWN]`；命中 `min_shot_size > shot_size`（例 `MS` 鏡用 `CU` 詞條）→ `FAIL [SCALE_JUMP_BAN]`（直接匯入既有 Rule g！）。
  - `microexpression`/`image_prompt`/`video_prompt` 命中 `banned_overacting_en`（美顏塑膠肌／商業笑／誇張張嘴）→ `FAIL [AI_FACE_TABOO]`；命中 `banned_abstract_only_zh` 且缺乏具體物理動詞 → `WARN [ADVISORY_CRAFT_ACTION]`（與 7b 整合）。

#### 5. 成本評估
- **上游填表**：選填（未填沿用既有 `microexpression`＋預設 `L1/L2`）；填 `intensity`＋1–2 個 `lexicon_ids` 約 +15 秒／鏡，卻能直接取代反覆手寫英文微表情句的時間（淨工時持平甚至下降）。
- **工具實作**：建 YAML（25 分鐘）＋`preflight_gate.py` 約 +65 行（30 分鐘）。
- **算力／CU**：0 CU；直接緩解 DEMO-02 雙人僵直與 AI 假笑返工。

#### 6. 裁決：**ADAPT**
- 借其「分區物理詞彙＋強度分級＋反 AI 假臉衛生」核心骨架，**堅決拒絕整包 488 行移植與 2 秒多段單鏡時間軸**，收斂為貼合范蠡低沉克制人設與 `544×960` 解析度現實的 4 分區輕量詞表。

---

### 項目 5｜人物參考預設範圍＋未見側重建規則（liyue）與 Step 0 翻轉幾何法處置

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #4（liyue 人物參考預設與未見側重建）；實測鐵證：`sm7a/SM7A_RESULT.md` §3 Discovery #2（`fanli-master-ancient-45R.v1-flip-defect.jpg` 水平翻轉導致 `左衽` 反領缺陷）與目視對比已修補之 `casting/master/fanli-master-ancient-45R.jpg`。

#### 1. 對 Step 0 翻轉幾何法（Flip-Geometry）的實證覆盤與裁決
實勘 `casting/master/tmp_flip45.jpg` → `fanli-master-ancient-45R.v1-flip-defect.jpg` → `fanli-master-ancient-45R.jpg`（06:42 修補版）已證明：
- 水平翻轉 `ancient-45.jpg` 雖可快速把頭向轉往畫面右側，但因影像水平鏡像會**無差別反轉所有左右非對稱物理結構**，在我方產線上同時踩爆四大紅線：
  1. **春秋交領 `右衽`（小寫 `y` 形，左襟壓右襟）被鏡像翻成忌諱的 `左衽`（`\` 形）**——SM-7A 實戰已踩中！
  2. **解剖學左眉尾淡疤**被翻到解剖學右眉；
  3. **現代左腕腕錶與右手方孔錢**左右互換；
  4. **朝服左腰佩劍（`OUTFIT-03`）**翻到右腰。
- 因此，**Step 0 的水平翻轉法必須正式退役（RETIRE）**，不得作為任何首幀或角色定裝圖的直接生成方法；改以 liyue「未見側結構重建規則」取代。

#### 2. 規格條文草案（可直接併入 `STORYBOARD-SPEC-V2.md` §三 C 與 §C.1）

```markdown
#### §三 C／§C.1 增補：人物參考預設範圍與未見側重建規則（v2.3）

1. **人物參考預設範圍（Person-Ref Scope Default）**：
   - 凡 `asset_refs[]` 中 `role = "character"` 之參考圖，預設涵蓋**完整可見角色（`full_character`：身分骨相＋臉部傷痕＋髮型剪影＋體型＋當圖服裝與配飾）**。
   - **顯式縮限強制條款**：僅當本鏡須借用「他套服裝或他時代母圖」的臉部身分時（例：春秋布衣鏡餵入現代 `fanli-master-B-userface.png`），必須顯式設 `owns: ["identity"]`、`never_inherit: ["costume", "studio_backdrop", "source_lighting"]`；編譯器自動輸出縮限句（`reference ONLY facial bone structure, age, and anatomical left-brow scar from <Picture k>; render attire exclusively from the locked costume reference`），杜絕西裝領口或現代碎髮串染進古裝鏡。

2. **未見側結構重建規則（Unseen-Side Reconstruction Rule）**：
   - 當鏡頭視角為母圖未直接拍攝之角度（如純側面、背影、或非主參考側之 45° 臉），生成端必須嚴格依據同套母圖已可見之**剪裁結構、布料材質、滾邊紋樣、色彩與穿戴方式**一致推演重建未見側，**嚴禁另行發明新配件、新紋樣或新結構**。
   - **非對稱不變量強保留（手性鎖定）**：未見側重建時，凡具左右手性之結構一律按真實三維解剖與禮制重建，**絕不隨視角翻轉而鏡像**：
     - 春秋深衣（`OUTFIT-02/03/04`）：任何角度皆嚴守**交領右衽**（角色左襟壓右襟，正面視覺小寫 `y` 形）；
     - 臉部傷痕：永遠僅存於**解剖學左眉尾**，露右臉鏡（`subject_facing: right`）之解剖學右眉必 100% 無疤；
     - 配件左右側：現代腕錶永鎖左腕、方孔錢主歸右手、朝服短劍永鎖左腰。

3. **Step 0 水平翻轉法正式退役（Retire Flip-Geometry）**：
   - 鑑於 SM-7A 實證 `tmp_flip45.jpg` 水平翻轉直接導致 `fanli-master-ancient-45R` 領襟反轉為 `左衽`，**全面退役水平翻轉法**——嚴禁將水平鏡像圖作為 Stage 3 首幀或 Stage 4 影片之任何參考槽輸入。
   - 日後補拍新服裝（如 `OUTFIT-03` 或 `OUTFIT-04`）之右側 45°／背影母圖，一律以未翻轉之 `userface`＋該套正面／左側 45° 母圖直接以文字重建視角，並經 QC-1 2.5× 臉領放大核對「無疤右眉＋`y` 形右衽」後方得鎖庫。
```

#### 3. Schema 與工具增量
- **`script_pack.json`**：沿用項目 1 的 `asset_refs[].owns[]`／`never_inherit[]`（零新增欄位）。
- **`preflight_gate.py` 新增三道檢查**：
  1. `CROSS_ERA_CHAR_SCOPE`（`FAIL`）：本鏡 `outfit_id` 與 `asset_refs` 內角色圖所屬服裝不符（如 `FANLI-OUTFIT-02` 鏡餵 `fanli-master-B-userface`）卻未顯式把該圖 `owns` 縮限為 `["identity"]` → 硬駁回。
  2. `FLIP_ASSET_BAN`（`FAIL`）：`asset_refs[].asset_id` 或路徑檔名含 `flip`、`mirror`、`v1-flip-defect` → 硬駁回（物理封殺翻轉圖混入產線）。
  3. `UNSEEN_SIDE_GUARD`（`WARN` / CU 升 `FAIL`）：`FANLI` 露右臉（`subject_facing == "right"`）之 `CU`/`MCU` 鏡，若既未綁定右側無疤母圖（`45R`）、又未在 `image_prompt` 載明「右眉無疤＋交領右衽（古裝時）」重建句 → 硬駁回（防 DEMO-02 S4 重演）。

#### 4. 成本評估
- **上游填表**：**+0 格**（與項目 1 共用欄位）。
- **工具實作**：`preflight_gate.py` 約 +45 行（~20 分鐘）。
- **算力／CU**：0 CU；避免像 SM-7A 一樣事後返工修補 `45R` 母圖。

#### 5. 裁決：**ADOPT（並退役 Step 0 翻轉幾何法）**
- 完美契合我方實測教訓：liyue 的「預設完整角色＋未見側按結構重建」正是根治跨時代服裝污染與水平翻轉 `左衽` 翻車的正面立法。

---

### 項目 6｜音色綁定句式（liyue／woodfantasy）

> **來源依據**：`SEEDANCE-25-ECOSYSTEM-REF.md` §二 #6（每句對白綁定角色＋音色來源＋時段＋保留特徵）；對齊我方 `STORYBOARD-SPEC-V2.md` §二 `audio_groups[]`／§三 A `dialogue[]`／§三 F `voice_mode: tts`、`voices/FANLI.yaml`（ElevenLabs `eleven_v4` 鎖定聲線）與 `POSTPROD_AGY_MEMO.md`（組裝捨棄原生人聲）。

#### 1. 工程診斷：在我方全面 TTS 路線下，逐句音色綁定是冗餘還是增量？
- **在影片生成端（H3／Flow `video_prompt`）——明確為 NO-OP（不採用）**：
  - Seedance 2.5 需要逐句寫「角色＋`@Audio 1` 音色來源＋音高呼吸」是因為它要**原生輸出可交付成片人聲**。
  - 我方路線是 **100% ElevenLabs TTS 聲音先行**，影片原生人聲於組裝時完全捨棄（`POSTPROD_AGY_MEMO.md` F7）。把 `@Audio` 音色描述硬塞進 H3 `video_prompt` 既不改變成片音色，反而擠佔 H3 `detailed_description` 的視覺表演 token 預算。
  - *附註*：SM-7A §1 曾提及未來可選測 `ref_audios.ref_audio_0` 作為口型對時輔助，但該用途屬**時序驅動（timing driver）**而非音色保存，不構成逐句音色綁定條款的理由。
- **在音訊組裝與 TTS 層（`dialogue[]`／`audio_groups[]`）——僅有微小增量，絕不可把 `voice_id` 下放到每句**：
  - `voices/FANLI.yaml` 明訂：「同一角色嚴禁混用其他引擎或聲線」，`voice_id`、`model_id`、`stability`、`similarity_boost` 必須**單點鎖定在 `bible/voices/{SPEAKER}.yaml`**（對齊 V13 一維度一權威！）。若允許在 `script_pack.json` 逐句填音色來源，反而破壞單點真相。
  - 現行 `audio_groups[]`（`{group_id, speaker, delivery_mode, lines[]}`）與 `dialogue[]`（`{line_id, speaker, line, tts_emotion_tags[], delivery_mode, pause_after_sec}`）真正只少一個小顆粒度：**開頭停頓（`pre_pause_sec`，對應 `FANLI_ALIVENESS.md` #5「說話前固定停頓半拍」）與簡式演繹強度（`pace`／`volume`）**，用以指導 ElevenLabs TTS 與口型留白對拍。

#### 2. 規格條文草案（輕量微修 `STORYBOARD-SPEC-V2.md` §三 A `dialogue[]` 與 §三 F）

```markdown
#### §三 A／§三 F 微修：TTS 聲線單點鎖定與演繹參數（v2.3）

1. **音色單點鎖定（不採逐句音色綁定）**：本系列全面採 TTS 合成對白、組裝端捨棄生成片原生人聲，故**不於影片 `video_prompt` 或 `dialogue[]` 逐句重複綁定音色來源**。說話者 `speaker` 唯一映射至 `bible/voices/{SPEAKER}.yaml`（須為 `LOCKED`，如 `FANLI`）；嚴禁在 `script_pack.json` 內覆寫 `voice_id` 或 `voice_settings`（守 `FANLI.yaml` 紅線與 V13 音色單一權威）。
2. **每句演繹參數輕量擴充（選填）**：`dialogue[]` 保留既有欄位，增選填 `delivery?: {pre_pause_sec?: number, pace?: "slow"|"measured"|"urgent", volume?: "whisper"|"low"|"normal"}`（未填時繼承角色聲線聖經預設；`FANLI` 預設為 `{pre_pause_sec: 0.5, pace: "measured", volume: "low"}`）。
3. **`audio_groups[]` 維持精簡**：段層 `audio_groups[]` 維持 `{group_id, speaker, delivery_mode, lines[]}` 結構不膨脹；群組內各句演繹差異仍歸於 `lines[]` 各自之 `tts_emotion_tags[]`、`delivery` 與 `pause_after_sec`。
```

#### 3. Schema 與工具增量
- **`script_pack.json`**：`dialogue[]` 僅增選填物件 `delivery`（3 個選填鍵）；`audio_groups[]` **零改動**。
- **`preflight_gate.py` 新增規則 `VOICE_AUTHORITY_LOCK`**：
  - 凡 `dialogue[]` 或 `audio_groups[]` 內出現 `voice_id`／`model_id` 覆寫鍵 → `FAIL [VOICE_AUTHORITY_LOCK]`（禁止鏡級私換聲線）。
  - 檢查所有 `speaker` 對應之 `bible/voices/{speaker}.yaml` 存在且 `status == "LOCKED"`（對齊既有 V3，現僅 `FANLI` 鎖定，`SYS-01` 標 `PENDING_LOCK` 時在 `demo` 降為 `WARN`、正式集數為 `FAIL`）。

#### 4. 成本評估
- **上游填表**：**+0 格**（常態全走角色預設，僅特殊氣音／急促句選填 `delivery`）。
- **工具實作**：`preflight_gate.py` 約 +25 行（~10 分鐘）。
- **算力／CU**：0 CU。

#### 5. 裁決：**REJECT（影片端音色綁定＝No-op）／LIGHT ADAPT（TTS 端僅收斂 `delivery` 預設）**
- 堅守減法紀律：不為「與 Seedance 生態對齊」而硬搬我方 TTS 架構根本不消費的逐句音色綁定語法。

---

### 項目 7｜電影質感提示詞工藝（`CINEMATIC-PROMPT-CRAFT-REF.md`）四項增量裁決

> **重疊項目先剝離（不重複立法）**：
> - 拒堆砌 `cinematic/masterpiece/8K/epic` → 併入 7b 語意告警；
> - 單鏡單運鏡 → 既有 **V6 ＋ 附錄 A §A.2** 已硬鎖；
> - 參考素材分工 → 併入項目 1／項目 2（`owns[]`/`never_inherit[]`＋V13）；
> - 微表情與呼吸 → 併入項目 4（`bible/performance/micro_expressions.yaml`＋§B.8-5）；
> - **明確駁回「多鏡頭寫法（`[Shot 1]`、`[Shot 2] At 00:03.500`）」**：直接違背 `STORYBOARD-SPEC-V2.md` §一 原則 1「**原子鏡制（1 筆＝1 首幀＝1 支片，已廢除 `sub_shots`）**」，且 LTX 預演、QC-1/QC-2 Diff 表與 `edit_manifest` 皆綁死單鏡原子模型，**絕不回頭在單支生成片內硬塞多切鏡時間碼**。

以下僅針對四大真實增量 `(a)–(d)` 逐項裁決：

---

#### 7(a) 顯式優先序（光線 → 鏡頭／運鏡 → 可觀察動作 → 調色 → 聲音）作為引擎方言編譯排序規則

##### 1. 規格條文草案（修訂 `STORYBOARD-SPEC-V2.md` §五 與 §A.4）

```markdown
#### §五／§A.4 修訂：電影優先序編譯排序規則（Light-First Compilation Order，v2.3）

引擎方言編譯器將結構化欄位轉譯為英文 `image_prompt` 與 `video_prompt` 時，依引擎分流套用「**光線最高優先（Light → Lens/Camera → Observable Action → Restrained Palette → Sound）**」排序，取代 v2.0 舊 Seedance 順序（舊序將光線置於第 6 位，易在長提示詞中被稀釋）：

1. **Flow（Omni 1.2 Flash）——全面採用電影優先序**：
   - `image_prompt`（定格於 `start_pose`）：`9:16 vertical live-action frame. [1. 光源方向＋光質＋色溫 (light_lock/lighting_base)] → [2. 焦段感＋景別＋角度＋主體與 start_pose/subject_facing] → [3. 場景環境與服裝/錨點細節] → [4. 有限調色盤與材質肌理 (atmosphere)] → [Avoid: 精簡視覺禁詞，必含 no readable text]`。
   - `video_prompt`：`Live-action cinematic, [生成秒數]s 9:16 single shot. [1. 明確光源方向與光質] → [2. 焦段感＋景別＋單一主運鏡＋幅度/速度] → [3. 主體可觀察物理動作＋微表情＋物理真實細節（布料/呼吸）＋鏡尾 end_state] → [4. 有限克制調色盤與材質] → [5. Sound: 環境音＋物理音效；無對白/無配樂明示] → [Avoid: 精簡視覺禁詞，禁裸否定靜止詞]`。

2. **H3（Ref2VA 六段式／Base 三段式）——保留官方外殼、內部強制前移**：
   - 外層段序嚴格維持 §A.4 官方格式（`subject_definitions → summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music`），**不得打亂外層六段**（避免破壞官方對齊與 `_check_h3_dialect`）。
   - 於 **`detailed_description`（或 Base 之 `integrated_multimodal_description`）段落內部**強制套用電影優先序：
     - **首句**：段級光線方向與光質（`light_lock`）＋景別／焦段感＋單一官方原語運鏡句；
     - **中句**：依時間順序之可觀察物理動作、微表情（`performance_beat`＋`lexicon_ids`）、物理真實細節（布料慣性／呼吸），若 `lip_sensitive=true` 嵌 `<d>[Chinese] 台詞</d>`（`voiceover` 則套官方閉唇句）；
     - **尾句**：有限克制調色盤／材質質感＋鏡尾 `end_state` 停留狀態；
     - **獨立段 5–6**：`overall_soundscape`（環境底噪＋物理音效）與 `non_diegetic_music: N/A`（或指定 cue）。

3. **Wan（2.2）——極簡動作無聲方言**：
   - 採 `[1. 光線短語], [2. 景別＋單一主運鏡] of [3. 主體＋可觀察物理動作], [4. 克制色調]` 單至兩句；**不輸出 `Sound:` 段**（Wan 無音訊輸出，免浪費 token）。
```

##### 2. Schema／工具增量、成本與裁決
- **Schema**：零新增欄位（純編譯器欄位重排）。
- **工具**：後續 Phase 5 `prompt_compiler.py` 直接依此順序輸出；Phase 3 `preflight_gate.py` 可增輕量 `WARN` 檢查 Flow/H3 `detailed_description` 前 30 詞是否含光線或運鏡線索（併入 7b）。
- **成本**：填表 **+0 格**；編譯規範調整 0 工時稅。
- **裁決**：**ADAPT**（採納光線優先排序取代舊 Seedance 順序，但**保留 H3 官方六段外殼**並**豁免 Wan 聲音段**）。

---

#### 7(b) 生成前六點檢查清單作為 QC-0 Advisory（`WARN` 類，非硬閘）

##### 1. 與現行硬閘去重對照

| 清單項 | 現行覆蓋狀態 | v2.3 處置 |
| :--- | :--- | :--- |
| ① 有明確光源方向嗎？ | **缺口**（僅驗 `light_lock_id` 非空，未驗描述有無方向／光質或禁空泛詞） | **新增 `WARN [CRAFT_LIGHT_SPECIFICITY]`** |
| ② 只有一個主運鏡嗎？ | **已由 V6 硬閘覆蓋**（`movement.type` 單一受控枚舉） | **不重複告警**（維持 V6 硬閘） |
| ③ 動作是可觀察的物理描述嗎？ | **半覆蓋**（V7 僅查 `end_state`，未查 `action`/`microexpression` 空泛情緒詞） | **新增 `WARN [CRAFT_OBSERVABLE_ACTION]`** |
| ④ 調色有限且克制嗎？ | **缺口**（未掃描 `cinematic color grade`/`masterpiece`/`8K`/`epic` 空泛堆砌詞） | **新增 `WARN [CRAFT_PALETTE_NO_FLUFF]`** |
| ⑤ 聲音有被設計嗎？ | **缺口**（現行允許 `ambience`、`sfx` 全空且未檢核 H3 `overall_soundscape`） | **新增 `WARN [CRAFT_SOUND_DESIGNED]`** |
| ⑥ 時間線與片長匹配嗎？ | **已由 V1＋V2 硬閘覆蓋** | **不重複告警**（維持 V1/V2 硬閘） |

##### 2. 規格條文草案（併入 `STORYBOARD-SPEC-V2.md` §六 Advisory 表）

```markdown
#### §六增補：QC-0 提示詞工藝 Advisory 檢查（`WARN` 級，不阻斷放行，v2.3）

`preflight_gate.py` 於全部硬閘（V1–V13、AMD-01/04/05/07）之後執行 4 項淨增工藝檢查（去重既有 V1/V2/V6），任一命中僅輸出 `WARN` 提示供 Muse／編劇送出前快速自檢，**不使退出碼轉為非零**（避免關鍵字啟發式誤殺有效簡潔鏡）：
1. **`CRAFT_LIGHT_SPECIFICITY`**：`lighting_base`/`lighting_state` 與 `image_prompt` 皆缺乏光源方向或光質詞（如 left/right/top/back/side/window/lamp/soft/hard/cool/warm 或對應中文），或出現空泛詞 `cinematic lighting`。
2. **`CRAFT_OBSERVABLE_ACTION`**：`action`/`microexpression` 含純抽象情緒標籤（如 `feels sad`/`looks angry`/`感到難過`/`很生氣`/`內心掙扎`）而未配對身體部位或物理動作，或含空泛詞 `epic`/`masterpiece`/`8K`/`stunning`。
3. **`CRAFT_PALETTE_NO_FLUFF`**：段級 `atmosphere` 與鏡級 prompt 皆缺克制色盤／材質線索，或含空泛詞 `cinematic color grade`。
4. **`CRAFT_SOUND_DESIGNED`**：非 `cpu_card` 鏡既無段級 `ambience` 規格、亦無 `sfx`，且 H3 `overall_soundscape` 空白或僅填 `N/A`。
```

##### 3. 成本與裁決
- **工具實作**：`preflight_gate.py` 約 +55 行（已具 `Finding(level="WARN", ...)` 支援！`format_report` 已只對 `FAIL` 回傳退碼 1，零架構改動）。
- **成本**：填表 **+0 格**；實作 ~20 分鐘；0 CU。
- **裁決**：**ADOPT（同意列 `WARN` Advisory、非硬閘，並去重 #2 與 #6 防止重複噪音）**。

---

#### 7(c) 聲音設計缺口：於 `script_pack` 與 `edit_manifest` 正式建立環境音／Foley 層

##### 1. 實檔鑑識：為何現行做法「不夠用」
實讀 `~/drama-line/demo02/assemble.sh` 第 7 行與第 17 行證實：
- 第 7 行以 `-an` **無差別剝光 S1–S4 全部原音**；
- 第 17 行硬把 `S1.mp4` 的 7.9 秒原音無限循環（`-stream_loop -1`）壓到 `volume=0.07` 當整段底噪，另硬寫 `between(t,10.8,11.35)` 壓至 `0.03` 做聲場抽空；
- **三大實務破洞**：① 跨 2 分鐘、3–4 場段（現代辦公室 → 台北暗巷 → 春秋湖面）無法靠循環單支 7.9 秒片原音撐全集，必現循環接縫與場景音場錯亂；② 物理音效（扶牆拍手聲、腳步聲、銅錢輕響、紙頁翻動、路燈電流、防盜器短鳴、glitch 電流）在現行流程全靠手工臨時找或直接漏掉；③ 未依 `-14 LUFS` 標準化前硬套線性 `volume=0.07`，在不同原片底噪音量下結果不可預測（例如 Clay Test `h3_out.mp4` 實測 `mean_volume: -25.3 dB`，再乘 `0.07` 會跌到 `-48 dB` 徹底消失！）。

##### 2. 規格條文草案（修訂 `STORYBOARD-SPEC-V2.md` §二 `ambience`、§三 F，並同步升級 `edit_manifest.json` `1.0 → 1.1`）

```markdown
#### §二／§三 F 增修：分層環境音與物理 Foley 規格（Sound Design Layer，v2.3）

1. **段級環境底噪（`segments[].ambience`，預設主力層）**：
   每場段強制指定一條連續環境底床（跨場段切換時以 0.25s 交叉淡化銜接，嚴禁全集硬循環單一短片原音）：
   `ambience: {source: "library_roomtone" | "retained_native_bed" | "generated_sfx_bed" | "silent", asset_id?: string, target_db?: number, note?: string}`（向下相容舊版純字串，字串自動視為 `note` 並預設 `library_roomtone`）。
   - **`library_roomtone`（預設首選）**：使用 `audio_lib/roomtone/` 之 CC0 連續實錄底噪（如 `alley_night_wet_48k.wav`、`office_night_hvac_48k.wav`、`lake_mist_wind_48k.wav`）——零循環接縫、零人聲外洩、跨引擎一致。
   - **`retained_native_bed`（嚴格受限）**：僅允許用於 **`voice_mode == "none"`** 且（若為 H3）`non_diegetic_music: N/A` 之純動作／空景／白膜鏡（如 Clay Test 實測無樂音純環境聲），且必先通過 `edit_manifest` **F7 檢核（`native_voice_verified_clean: true`）**，鏡間強制 0.20–0.30s crossfade；凡 `voice_mode == "tts"` 之對白鏡**100% 禁止**抽取該鏡原生音軌作底噪。
   - **`generated_sfx_bed`（選配／Phase 5）**：由音效生成 API 或純環境生成片抽出之定製底噪，須先入庫 `audio_lib/roomtone/` 跨鏡複用，不得每抽重算。

2. **鏡級物理 Foley 與拍點音效（`shots[].sfx[]`）**：
   每場段精選 **2–4 個關鍵物理觸點**（腳步、扶牆掌擊、衣料摩擦、紙頁翻動、古銅錢輕扣、防盜器短鳴、glitch 電磁脈衝），以結構化陣列登錄（不追求每鏡密鋪）：
   `sfx: [{cue: string, timing_sec?: number, level_class: "subtle_foley" | "accent_sfx", source?: "library" | "native_extract" | "generated", asset_id?: string}]`。

3. **混音電平基準表（校準至 `edit_manifest.json` 母帶 `-14.0 LUFS`／`True Peak ≤ -1.5 dBTP`）**：
   | 音軌 | 來源 | 無對白基準電平 | 對白期間閃避（Sidechain／Duck） | `sound_drop` 特效拍點（0.30–0.35s） |
   | :--- | :--- | :---: | :---: | :---: |
   | **A1 對白（TTS）** | `bible/voices/*.yaml` 鎖定 TTS | 基準 `0 dB`（幹聲歸一 `-16 ± 1 LUFS`） | — | 靜默待觸發後起聲 |
   | **A2 環境底床（Ambience）** | 段級 `library_roomtone`（或合規 `retained_native_bed`） | **`-24 dBFS`**（容許 `-22 ~ -26 dBFS`） | 再降 **`-6 dB`**（落 `-28 ~ -32 dBFS`） | 壓至 **`-38 dBFS`**（20ms 斜坡，禁數位死靜爆音） |
   | **A3 物理 Foley / SFX** | `audio_lib/sfx/` 庫（按 `timing_sec` 對位） | `subtle_foley`：**`-16 dBFS`**（`-14 ~ -18`）<br>`accent_sfx`：**`-8 dBFS`**（`-6 ~ -10`，限幅 `≤ -3 dBTP`） | `subtle_foley` 遇對白降 `-4 dB`；`accent_sfx` 錯開起聲 | `glitch_in` 於抽空結束瞬間觸發 `accent_sfx` |
   | **A4 配樂（BGM，選配）** | `audio_lib/bgm/`（預設 `none`） | **`-20 dBFS`**（`-18 ~ -22`） | 再降 **`-10 ~ -12 dB`** | 同 A2 壓至 `-38 dBFS` |
```

##### 3. `edit_manifest.json`（`1.0 → 1.1`）與 `preflight_gate.py` 增量
- **`edit_manifest.json`**（直接擴充 `POSTPROD_AGY_MEMO.md` 既有 `audio_tracks.ambience[]` 與 `audio_tracks.sfx[]`，零破壞）：
  - `audio_tracks.ambience[]` 新增：`segment_id`、`source_type` 明確枚舉為 `"library_roomtone" | "retained_native_bed" | "generated_sfx_bed"`、`crossfade_sec`（預設 `0.25`）、`sound_drop_windows?: [{start_sec, end_sec, floor_db: -38.0, ramp_ms: 20}]`、`target_lufs_or_dbfs`（取代裸相對增益猜測，渲染前先依 `volumedetect` 實測值計算補償 `gain_db`，徹底根治 DEMO-02 `volume=0.07` 在不同素材上音量亂飄的問題！）。
  - `audio_tracks.sfx[]` 新增：`level_class`（`"subtle_foley" | "accent_sfx"`）、`duck_by_dialogue_db`（`subtle_foley` 預設 `-4.0`、`accent_sfx` 預設 `0.0`）。
- **`preflight_gate.py` 新增規則 `AUDIO_BED_HYGIENE`**：
  - 若 `shot.ambient_source == "native_keep"` 且 `shot.voice_mode == "tts"` → **`FAIL [AUDIO_BED_HYGIENE]`**（把 `POSTPROD_AGY_MEMO.md` F7 前移至 QC-0 硬攔，徹底杜絕原生人聲漏音）。
  - 若 `shot.sfx[]` 有項目但缺 `level_class` → 自動預設 `subtle_foley` 或提示補齊；若 `vfx_beats` 含 `sound_drop` 但段級 `ambience.source == "silent"` → `WARN [AUDIO_BED_HYGIENE]`（底噪本就靜音則 `sound_drop` 無效果）。

##### 4. 成本與裁決
- **上游填表**：每 segment 填 1 行 `ambience`（+10 秒），全集補 4–8 個關鍵 `sfx`（+1 分鐘）；一次性建置 5–8 條免費 CC0 Room Tone＋基礎 Foley 音庫（`audio_lib/`，~15 分鐘，跨集永久複用）。
- **算力／CU**：0 GPU、0 CU；ffmpeg 多軌混音增時 <2 秒。
- **裁決**：**ADOPT**（補上從 `script_pack` 到 `edit_manifest` 真正落地聲音設計的最後一哩路，結束 DEMO-02 式手刻 `volume=0.07` 拼湊）。

---

#### 7(d) 5–8 秒穩定區間 vs V1 引擎時長上限

##### 1. 與實測數據核對（必守 SM-7A 與 Clay Test 鐵律）
- `CINEMATIC-PROMPT-CRAFT-REF.md` 的「5–8 秒單鏡比 15 秒穩」談的是**影片模型單次生成的原始秒數**。
- 我方 V1 規則計的是**成片淨長（`target_net_sec`）**，加上常規 `standard_0.5s` 頭尾各裁 0.5 秒（`+1.0s` 緩衝）後：
  - 現行 Flow 淨 `≤ 6.5s` ＝ **生成 `≤ 7.5s`**（正好落在 5–8s 區間上緣）；
  - 現行 H3／Wan 淨 `≤ 5.5s` ＝ **生成 `≤ 6.5s`**（正好落在 5–8s 區間中段）。
- **但實測數據顯示 Colab L4 不可放寬、反而必須在 H3 之下細分 L4 子上限**：
  - **Clay Test Condition 3**：L3 白膜在 L4 24GB 跑 `5.17s`（124 幀）峰值 VRAM 已達 `20.727 GiB`（僅剩 `1.307 GiB`）、System RAM 僅剩 `2.64 GiB`，**實測已硬鎖 L4 跑 L3 生成秒數 `≤ 5.0s`**（對應 `standard_0.5s` 淨長 `≤ 4.0s` 或 `tail_only` 淨長 `≤ 4.5s`），超過 5s 必轉 A100/G4！
  - **SM-7A**：4 槽 `max` H3 對白 CU 跑 `5.17s` 餘裕 `1.85 GiB`、耗時 `4.67 分鐘`，且對照組在 `3.5–4.5s` 已出現晚幀光影漂移趨勢；故 4 槽 `max` 建議鎖在生成 `≤ 5.5s`（淨 `≤ 4.5s`），超出則依 §B.7 #1 拆「反應鏡＋主鏡＋L-cut」而非硬撐 7–8 秒。

##### 2. 規格條文草案（修訂 `STORYBOARD-SPEC-V2.md` §六 **V1**）

```markdown
| **V1 時長（v2.3 實測細分版）** | 以「生成總長＝淨長＋裁切緩衝」對齊 5–8s 物理穩定窗與 Colab L4 實測記憶體上限（絕不放寬至 8s 淨長）：<br>• **`ltx`（預演／快切）**：淨長 `≤ 2.5s`<br>• **`h3`（`L3_clay_ref2v` on L4）**：**生成長硬上限 `≤ 5.0s`**（`standard_0.5s` 淨 `≤ 4.0s`／`tail_only` 淨 `≤ 4.5s`；超時須改路由 A100/G4，對齊 Clay Test Condition 3）<br>• **`h3`（4 槽 `max` 對白 CU on L4）**：**建議淨長 `≤ 4.5s`（生成 `≤ 5.5s`）**、硬上限淨長 `≤ 5.5s`（生成 `≤ 6.5s`；長台詞一律走 §B.7 拆鏡＋L-cut）<br>• **`wan`**：建議淨長 `≤ 5.0s`（生成 `≤ 6.0s`）<br>• **`flow`（Omni 1.2 Flash）**：淨長 `≤ 6.5s`（生成 `≤ 7.5s`）〔Omni 1.2 Flash 單次硬頂秒數待首次實跑回填確認〕<br>• **下限提示（Advisory）**：非 `INSERT`/短反打之 AI 鏡生成長 `< 3.0s`（淨 `< 2.0s`）發 `WARN`；聲音先行定版後全線以 `D_tts + 0.4s` 重跑驗證。 | 全自動（兩段：`preflight_gate.py`） |
```

##### 3. 工具增量、成本與裁決
- **`preflight_gate.py` 新增規則 `V1_DURATION_ENVELOPE`**：依 `engine_route`＋`control_method`＋`trim_policy`＋`target_net_sec` 自動算 `gen_sec`，硬攔 `L3_clay_ref2v`（L4 預設）`gen_sec > 5.0`、H3 `gen_sec > 6.5`、Flow `gen_sec > 7.5`、LTX `net > 2.5`，並對 4 槽 `max` H3 `gen_sec > 5.5` 與短鏡 `gen_sec < 3.0` 發 `WARN`。
- **成本**：填表 **+0 格**；實作 ~35 行（~15 分鐘）；避免 L4 跑 6–8 秒白膜直接 OOM 燒掉冷啟動 CU。
- **裁決**：**ADAPT（確認不放寬＋按 SM-7A／Clay Test 實測收緊 L4 子門檻）**。

---

## 二、`preflight_gate.py` v2.3 增量檢查總表（集中檢視）

| 規則 ID | 層級 | 對應項目 | 觸發條件（全機械可檢） |
| :--- | :---: | :---: | :--- |
| `ASSET_CONTRACT` | `FAIL` / `WARN` | Item 1 | `owns ∩ never_inherit != ∅`；L3 缺 `<Pic 1>` 場景錨或未排除 `clay_material`；未裁多格 `charactercard` 直餵；帶道具母圖空手鏡未標 `baked_prop`（`WARN`）；H3 prompt 滲漏裸否定詞（`FAIL`）。 |
| `REF_COUNT_BUDGET` | `FAIL` / `WARN` | Item 1（§二 #7） | L4 `L3_clay_ref2v` 圖數 `>3`（`FAIL`）；L4 H3 `max` 圖數 `>4`（`WARN`）；任一 H3 鏡圖數 `>9`（`FAIL`）。 |
| `V13_AUTHORITY_CONFLICT` / `V13_ORPHAN_ASSET` | `FAIL` | Item 2 | 同 `(dimension, scope_target)` 存在 ≥2 個互斥 `owner_group_key`（跨齡／跨服裝／跨職責）；或某 `asset_ref` 解析後擁有 0 維度。 |
| `ERA_ANCHOR_CONFLICT` | `FAIL` | Item 3 | 春秋／`OUTFIT-02/03` 出現方孔錢／腕錶／低馬尾；現代 `OUTFIT-01` 出現緇布冠／木笄；腕錶寫錯右腕或方孔錢要求可讀文字。 |
| `PERF_INTENSITY_CONFLICT` / `AI_FACE_TABOO` | `FAIL` / `WARN` | Item 4 | `deliberate_hold=true` 配 `L3/L4`（`FAIL`）；`FANLI` 標 `L4` 無特批（`WARN`）；`lexicon_ids` 違反 `min_shot_size`（併入 `SCALE_JUMP_BAN` `FAIL`）；美顏塑膠肌／過演詞（`FAIL`）。 |
| `CROSS_ERA_CHAR_SCOPE` / `FLIP_ASSET_BAN` / `UNSEEN_SIDE_GUARD` | `FAIL` | Item 5 | 跨服裝參考角色圖未縮限 `owns=["identity"]`；資產路徑含 `flip`/`mirror`/`v1-flip-defect`；露右臉 CU 既無 `45R` 又無重建護欄句。 |
| `VOICE_AUTHORITY_LOCK` | `FAIL` / `WARN` | Item 6 | `dialogue[]`／`audio_groups[]` 擅自覆寫 `voice_id`/`model_id`（`FAIL`）；`speaker` 聲線檔未 `LOCKED`。 |
| `CRAFT_LIGHT_SPECIFICITY` / `OBSERVABLE_ACTION` / `PALETTE_NO_FLUFF` / `SOUND_DESIGNED` | `WARN`（Advisory） | Item 7b | 4 項淨增電影工藝提示（去重 V1/V2/V6），僅提示不阻斷退碼。 |
| `AUDIO_BED_HYGIENE` | `FAIL` / `WARN` | Item 7c | `voice_mode == "tts"` 且 `ambient_source == "native_keep"`（`FAIL`，前移 F7）；`sound_drop` 配 `silent` 底床（`WARN`）。 |
| `V1_DURATION_ENVELOPE` | `FAIL` / `WARN` | Item 7d | L4 `L3_clay_ref2v` 生成 `>5.0s`（`FAIL`）；H3 生成 `>6.5s`（`FAIL`）；4 槽 `max` 生成 `>5.5s`（`WARN`）；Flow 生成 `>7.5s`（`FAIL`）；LTX 淨 `>2.5s`（`FAIL`）。 |

**整套 v2.3 實作總成本預估**：
- 新增 2 份輕量 YAML 聖經檔（`bible/anchors/FANLI.yaml`、`bible/performance/micro_expressions.yaml`）：~40 分鐘；
- `preflight_gate.py` 增量約 +380 行（含對應 `--selftest` 斷言）：~2.5 小時（0 新套件，純 Python 3.11 標準庫）；
- `diff_sheet_gen.py` Col 0／Col 2 掛入時代錨點提示：約 +35 行（~20 分鐘，不更動既有 5/6 鍵）；
- `STORYBOARD-SPEC-V2.md` 升版 v2.3＋`edit_manifest.json` 升 v1.1 文件整合：~45 分鐘；
- **總工程成本 ~4 小時，0 GPU，0 CU，上游常規鏡頭填表淨增趨近於 +0 格**（全部採角色／時代／聲線預設繼承，只在特例與衝突點強制填寫）。

---

## 三、整合後 `STORYBOARD-SPEC-V2.md` v2.3 完整目錄（Integrated TOC）

> **架構收斂說明**：不另疊「附錄 D」造成閱讀碎片化——v2.3 全部條文按職責**原地併入正文對應章節與既定附錄 A／B／C**，並增列「聖經索引表（Bible Index）」對接外部受控 YAML 檔，維持整份規格單一線性可查。

```markdown
# 分鏡規格 v2.3（整合定版目錄）

## 零、版本沿革、紅線與聖經索引（Bible Index｜v2.3 新增索引）
- 0.1 版本沿革（v2.0 雙檔原子鏡 → v2.0+A 運鏡控制 → v2.1+B 導演層 → v2.2+C 工作流修訂與 Demo 邊界 → v2.3 提示詞契約、錨點、表演詞表與聲音設計）
- 0.2 不可動搖紅線（V9 畫面禁字、事實分層繼承、seed 不入鏡級、正向編譯／零裸否定詞、全面 TTS 路線）
- 0.3 受控聖經檔案索引：
  - `bible/anchors/FANLI.yaml`（v2.3 新增：跨鏡身分與時代條件錨點）
  - `bible/performance/micro_expressions.yaml`（v2.3 新增：4 分區微表情有界詞表、L1–L4 標尺與反 AI 假臉衛生）
  - `bible/camera/named_shots.yaml`（v2.0+A：受控 9:16 鏡型庫）
  - `bible/voices/FANLI.yaml`（LOCKED 聲線唯一準據）
  - `bible/director/playbook.md`（v2.1+B：累積制導演手記）
  - `COSTUME_REGISTRY.md`／`MASTER_FACE_DECISION.md`（服裝與身分基準）

## 一、架構：兩層制 × 三檔分離（`script_pack.json`／`production_state.json`／`edit_manifest.json`）
- 原子鏡原則（明文駁回單鏡多切鏡 `[Shot 1]/[Shot 2]` 寫法）、共用上移、prompt 衍生制、連戲繼承制

## 二、場段層 `segments[]`
- 基礎欄位（`segment_id`、`scene_id`、`time_layer`、`lighting_base`、`atmosphere`、`bgm_cue`、`audio_groups[]`）
- 導演層段級欄位（`light_lock_id`、`public_exposure`、`anomaly_level`、`world_reaction_default`）
- **§2.1 段級環境音底床規格 `ambience`（v2.3 升級：`library_roomtone`／`retained_native_bed`／`generated_sfx_bed`／`silent`）**

## 三、原子鏡層 `shots[]`（schema 2.3）
- A 敘事（含 v2.3 `dialogue[].delivery` 輕量演繹預設、單點聲線鎖定）
- B 攝影（連結附錄 A.2 擴充 `movement`）
- **C 參照綁定（v2.3 擴充：`asset_refs[]` 作用域契約 `owns[]`/`never_inherit[]`、角色預設表、人物參考預設範圍、未見側重建規則、Step 0 水平翻轉法正式退役、L4 餵圖上限）**
- D 連戲
- E 時間
- **F 聲音（v2.3 擴充：結構化 `sfx[]`、`ambient_source` 與 F7 防漏音硬約束、`-14 LUFS` 四軌混音電平基準表）**
- G 生成（`engine_route`、`gen_mode`、`face_lock_level`、`lip_sensitive`、`visual_text_overlay[]`）
- H 生產狀態（位於 `plan/production_state.json`）

## 四、引擎 × 模式相容表（同步 SM-7A／Clay Test 實測回填＋Omni 1.2 Flash 口徑）

## 五、prompt 衍生公式（v2.3 升級：電影優先序編譯規則 Light → Lens/Camera → Observable Action → Palette → Sound）

## 六、驗證規則總表（QC-0／`preflight_gate.py`）
- 硬閘規則：**V1（v2.3 細分 L4 子上限）**、V2、V3（含聲線單點鎖）、V4、V6、V7、V8、V9、V10、V11（運鏡分級）、V12a–c（導演硬閘）、**V13（v2.3 新增：一維度一權威＋孤兒資產清除）**，以及 AMD-01/04/05/07 與 v2.3 契約／時代錨點／反翻轉／音床防漏硬斷言
- Advisory 警告類（`WARN`，不阻斷放行）：V5、V12d–e、**v2.3 電影工藝四項自檢（`CRAFT_LIGHT_SPECIFICITY`／`OBSERVABLE_ACTION`／`PALETTE_NO_FLUFF`／`SOUND_DESIGNED`）**、范蠡 `L4` 強度警戒、4 槽 `max` 長鏡與短鏡提示

## 七、範例（EP-01 拆鏡＋DEMO-02 S4 依 v2.3 作用域契約與電影優先序編譯實例）

## 八、銜接、分責與跨檔契約（對接 `edit_manifest.json` v1.1 與 DESIGN v1.5）

## 九、Demo／試拍模式邊界條款（v2.2 維持零豁免紅線）

---

## 附錄 A：運鏡控制與引擎方言
- A.1 四級分層（L1–L4）與快線紀律
- A.2 `movement` 欄位擴充
- A.3 `control_method`、V11 與 `previs_artifacts`
- **A.4 引擎 prompt 方言（v2.3 整合：H3 外殼保留＋內部電影優先序＋`never_inherit[]` 正向替換表＋Q6 V3 槽位分責；Flow 電影優先序；Wan 極簡無聲方言）**
- A.5 L3 工具定版（CozyClay＋Clay Test 實測 L4 四條件：`<Pic 1>` 場景錨、`ref_video_0 ≤ 0.35 MP`、`match`、`≤5s`、無 GPU VM 備援路徑）
- A.6 運鏡 QC 驗收
- A.7 `named_shots.yaml` 受控鏡型庫
- A.8 EP-01 試套定案
- A.9 開拍前冒煙測試清單（回填 SM-2/3/6/7A 實測結論，SM-1/4/5 待辦，SM-7B RefMod 維持 WATCH）

## 附錄 B：導演層（v2.1＋v2.3 微表情收斂）
- B.1 導演闡述（階段 0.5）
- **B.2 欄位落點（v2.3 擴充：`performance_beat` 加入 `intensity` L1–L4 與 `lexicon_ids[]`）**
- **B.3 V12 導演護欄（v2.3 擴充：V12b 耦合 `micro_expressions.yaml` 景別門檻與反 AI 假臉衛生）**
- B.4 `camera_psychology` 衍生與引擎盲區後製補救
- B.5 QC-D 導演 QC 閘
- B.6 導演手記（`bible/director/playbook.md`）
- B.7 Creator 定案三點
- B.8 QC-D 首例裁決與常規五條

## 附錄 C：工作流修訂 AMD-01～07（v2.2＋v2.3 實測與錨點銜接）
- **C.1 AMD-01 身份載體分工（納入 SM-7A 4 槽 `max` 實測基線、未見側重建規則與退役翻轉法）**
- **C.2 AMD-02＋03 雙門對稱 QC（v2.3 整合：不增第 7 鍵，明訂 `FANLI.yaml` 四錨點映射至 `scar_side`＋時代參數化 `costume_4pt`＋`age_id`，由 `diff_sheet_gen.py` 動態列印）**
- C.3 AMD-04 同場景衍生規則（Path A／B／C）
- C.4 AMD-05 `SYS-01` 彈窗四層後製合成化
- C.5 AMD-06＋07 入口契約與 `preflight_gate.py` 強制力
```
