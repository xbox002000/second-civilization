# 分鏡規格 v2 草案——工程討論備忘錄（agy 立場文件）

> **文件定位**：書面討論備忘錄（只討論，不改 `STORYBOARD-SPEC-V2-DRAFT.md` 本體、不改 `DESIGN.md`、不實作、不 push）  
> **撰寫日期**：2026-11-27  
> **討論對象**：Muse（規格起草與 QC） ↔ agy（產線工程與生成） → 彙整呈交 Creator 定版  
> **依據材料**：`STORYBOARD-SPEC-V2-DRAFT.md`、`STORYBOARD-GAP-ANALYSIS.md`、`DESIGN.md`（v1.4，含 `script_pack` schema 1.3）、`COSTUME_REGISTRY.md`、`EP001_WORKFLOW_DRAFT.md`、`DRYRUN-EP01-v0.3.1-BLIND.md`、`DRYRUN_EP01_v031_RECHECK.md`，以及本機實測 `gflow-cli v0.107.0` 指令面。  
> **版本檔案註記**：工作區 `~/drama-line/` 中未見 `DRYRUN-EP01-arrival-v0.3.2.md`，故試套驗證以工作區現行最新版 `DRYRUN-EP01-v0.3.1-BLIND.md`（含 S11 新聞卡＋對白混合鏡、S16 閃回段落鏡，並參照 `DRYRUN_EP01_v031_RECHECK.md` 複檢結果）進行。

---

## 核心總評（先亮工程底牌）

這份 v2 草案把我們從「散文節拍表」推進到「結構化資產綁定＋攝影拆欄＋雙 prompt 衍生」，方向完全正確。但從我方實際工具鏈（`gflow-cli v0.107.0`、`comfy-colab-kit` 閘道 H3／Wan／LTX、`ffmpeg`、ElevenLabs `eleven_v4` TTS 聲音先行、以及 ADR-002 Phase 3 半自動紀律）檢視，草案有四個會直接卡死生產的結構問題：

1. **與 `DESIGN.md` v1.3/v1.4 的「TTS 聲音先行」與「頭尾各剪 0.5 秒」脫節**：草案仍以舊版 schema 1.0 思維起草，漏掉 `tts_emotion_tags`、`audio_ref`、`duration_from_audio`、`LIP_SENSITIVE`、跨鏡對白分組，且未區分「成片淨時長」與「含 1.0s 緩衝之生成時長」。
2. **「每鏡必填尾幀＋同場預設 `prev_tail` 尾幀鏈」過度理想化**：會把 Stage 3/3.5/4 的平行批次管線打碎成串行鎖鏈、讓首幀產圖與 QC-1 翻倍、與「頭尾各剪 0.5 秒」正面相撞，且 `h3`/`wan` 閘道是否支援首尾幀尚未實測。
3. **`sub_shots` 無法對齊原子生成單元與 LTX 預演**：凡跨場、跨角色或跨引擎的複合鏡（如 S16、S11），`sub_shots` 裝不下獨立資產與首幀，LTX 預演也無從執行。
4. **H 層執行狀態混入上游不可變劇本包**：會直接破壞 `approval_upstream.json` 的劇本 SHA256 核准憑證與 Git review 純度。

以下依序回應 Q1–Q5、進行全欄位體檢、評估驗證規則 V1–V10、實填 S11／S16 找洞，並提出可落地的兩層結構替代案。

---

## 一、草案第七節 Q1–Q5 逐題答覆

### Q1 粒度：「鏡＋`sub_shots` 例外」vs Huobao 式「段（segment）＋子鏡」？EP-01 的 S16 與 S04 哪種比較順？

- **明確建議**：**反對「鏡＋`sub_shots` 例外」，採「輕量場段層（`segments[]`）＋扁平原子生成鏡（`shots[]`）」兩層制**（`shots[]` 保持扁平陣列、透過 `segment_id` 指向所屬場段，不做巢狀樹；完全取消 `sub_shots`）。
- **工程理由**：
  1. 下游所有工具（`gflow`、`comfy-colab-kit`、Stage 3.5 LTX 預演、`review.html`、`yield_log.jsonl`、`ffmpeg` 頭尾裁 0.5s）的最小操作單位都是**「1 支生成影片＝1 張核准首幀＝1 筆 `shot`」**。若 `sub_shots` 內含不同場景／角色（如 S16），不是得把整套 A–H 欄位複製進 `sub_shots` 形成遞迴結構，就是強迫單次 AI 生成跨場硬切（Wan／LTX／H3 必崩）。
  2. 把同場共用屬性（`scene_id`、`time_layer`、`lighting_base`、`atmosphere`、`ambience`、`bgm_cue`、跨鏡畫外音 `audio_groups`）抽到 `segments[]`，既消滅 20 鏡重複抄寫，又讓 `shots[]` 維持扁平好跑迴圈。
  3. **對 EP-01 兩鏡實證**：
     - **S16（兩拍）**：S16a（越宮內侍捧劍）與 S16b（太湖小船閉眼）場景、角色、道具、光線、首幀全不同，拆為同 `segment_id` 下的兩筆扁平原子鏡 `S16a`、`S16b` 並共享一組畫外音 `audio_group_id`，比塞進 `sub_shots` 順十倍。
     - **S04（三輪對白＋反應拍）**：`DRYRUN_EP01_v031_RECHECK.md` 已證實 S04 三輪對白本身就吃滿 6.0s，再硬塞「僵住盯兩秒＋轉身離開」必超長且違反 V6（一鏡一主動作）；拆為同場段下的 `S04a`（對話 5.5s）＋`S04b`（無對白僵住離場 2.0–2.5s），對白速率、表演留白與 V6 一次全解。

---

### Q2 H 層（`state`／`selected_take`）放進 `script_pack.json` 本體，還是獨立的 production tracker 檔？

- **明確建議**：**必須獨立為 `plan/production_state.json`（以 `shot_id` 外鍵對應），絕對不寫回 `input/script_pack.json` 本體**。唯一保留在 `script_pack.json` 的只有企劃期靜態屬性 `production_mode`（取代 `should_generate`）。
- **工程理由**：
  1. **保護上游核准憑證（SHA256）**：`DESIGN.md` §0.2 規定 `EP{NNN}/input/approval_upstream.json` 鎖定 `script_pack.json` 的 SHA256。一旦生成失敗、重抽或挑片就改寫 `script_pack.json`，上游核准雜湊立刻失效。
  2. **符合 Git 工作流與雙軌協作**：劇本／分鏡修訂（低頻、由 Muse 與 Creator PR/審核）與抽卡狀態更新（高頻、由 agy 每分鐘讀寫）混在同一檔案，會讓 `git diff` 塞滿噪音並製造合併衝突。
  3. **對齊既有目錄設計**：`DESIGN.md` §6.2 已有 `input/script_pack.json`（只讀真相）與 `plan/shot_plan.json`、`selected_takes.json`、`metrics/yield_log.jsonl` 的分層；把 H 層與 Stage 1.5 TTS 回寫值（`audio_ref`、實測秒數）、Stage 3.5 `lip_sensitive` 標記、Stage 4–5 `state`/`takes[]`/`selected_take`/`fail_reason`/`audio_offset_ms` 統一收斂在 `plan/production_state.json`，Phase 3 半自動時期也方便人眼核對與重跑。

---

### Q3 `gen_mode` 的枚舉要對齊各引擎的真實能力：Flow／H3／Wan／LTX 各自支援到什麼程度？是否要按引擎分級？

- **明確建議**：**`gen_mode` 保持「引擎無關」的語意枚舉（不要按引擎命名分級），但須修訂枚舉值並加掛一張「引擎×模式相容驗證表」作為路由降級依據**。建議枚舉改為：
  - `i2v_first`（預設主力：單首幀生影）
  - `i2v_first_last`（首尾幀插值：僅限少數高連戲關鍵鏡，且須宣告降級為 `i2v_first`）
  - `ref2v`（多參考圖保臉生影：僅 H3 Ref2V 或 Flow R2V）
  - `cpu_card`（取代易與被禁 T2V 混淆的 `text_only`：純 CPU 2.5D 圖卡／字卡／聲明卡）
- **各引擎真實能力對照表**（嚴格區分本機實測 vs 文件紀錄 vs 閘道未驗證）：

| 引擎（`engine_route`） | `i2v_first`（首幀生影） | `i2v_first_last`（首尾幀） | `ref2v`（多圖參考生影） | 關鍵限制與查核狀態 |
| :--- | :---: | :---: | :---: | :--- |
| **`flow`**<br>（本機 `gflow-cli v0.107.0` 實機查驗） | ✅ `gflow video i2v -i` | ⚠️ `gflow video i2v -i -e`<br>（`veo-lite` 12/05 後 cohort 支援待登入實測） | ✅ `gflow video r2v --ref`<br>（`veo-lite`/`fast` ≤3 張；`omni-1.2` ≤7 張；**`veo-quality` 拒絕 R2V**） | **關鍵互斥**：`r2v` **不可與 `--initial-frame` 混用**！且 Veo 3.1 僅支援 **4/6/8s**；`veo-fast`/`quality`/`omni-flash` 將於 **2026-12-05 退役**。多圖保臉應在 Stage 3 用免費 `gflow image i2i`（上限 10 張）烘焙進首幀，Stage 4 跑 `i2v_first`。 |
| **`h3`**<br>（`comfy-colab-kit` `minimax-h3-video`） | ✅ 文件確認 | ⚠️ **閘道未驗證**<br>（`BRIEF.md` 僅列 T2V/I2V/Ref2V） | ✅ 文件確認（主力多圖保臉） | 單鏡甜區約 5–6s（扣頭尾 1s 後淨 4–5s）；Ref2V 與首尾幀並用之可行性未驗證；已登錄美區 Colab 地域灰區。 |
| **`wan`**<br>（`comfy-colab-kit` `wan-ltx-video` Wan 2.2） | ✅ 文件確認 | ⚠️ **閘道未驗證**<br>（上游有獨立 FLF2V 權重，但閘道 profile 是否內裝未知） | ❌ 不支援<br>（標準 Wan 2.2 I2V 無多參考；未裝 VACE） | 動作物理最強，但保臉中低，避免主角正臉特寫；單鏡甜區生成 4–6s。 |
| **`ltx`**<br>（`comfy-colab-kit` `wan-ltx-video` LTX） | ✅ 文件確認 | ⚠️ 閘道未驗證（且無實益） | ❌ 不支援 | 正式鏡依 `DESIGN.md` 硬鎖淨長 **≤2.5s**、禁用主角正臉；主力為 Stage 3.5 低清預演（`N=1`）。 |
| **`ffmpeg_card`**<br>（VM CPU Pillow + ffmpeg） | — | — | — | 僅對應 `cpu_card`（0 GPU、0 Flow 點、固定 `N=1`、不做頭尾 0.5s 裁切）。 |

- **為何不按引擎分級枚舉**：12/05 Veo 退役或 Flow 觸發紅燈成本護欄時，`shot_router` 會把英雄鏡自動由 `flow` 降級補位至 `h3`（`DESIGN.md` §2.5、§8.4）。若 `gen_mode` 綁死引擎名稱，降級切換就得改寫劇本包；維持引擎無關語意＋由路由器查相容表（不支援 `i2v_first_last` 時自動降級 `i2v_first` 並發告警），架構最乾淨。

---

### Q4 prompt 衍生：全公式組裝 vs 模板＋人工覆寫，哪一段最容易失真？`prompt_override_reason` 稽核在哪一站做？

- **明確建議**：**採「結構模板產生初稿＋引擎方言適配＋受控人工／LLM 精修」，反對機械式純字串拼接**。`prompt_override_reason` 僅在**改變敘事／構圖／資產語意**時必填（純中翻英與引擎語氣壓縮免填），**主稽核站設在 Stage 3（QC-1 首幀門，由 Muse 連同首幀一起核對）**；若 Stage 4 抽卡重試微調 `video_prompt`，則記回 `production_state.json` 並於 Stage 5（QC-2）備查。
- **最容易在實作上失真的 4 個環節**：
  1. **從動態 `action` 切出靜態首幀起始姿勢（最致命）**：草案公式寫「`action` 的起始姿勢」，但程式無法從中文動態句（如 S04「聽完僵住、盯屏幕、隨後轉身離開」）自動截出 `t=0` 定格姿態；整句餵進 `image_prompt` 會害出圖模型畫出轉身背影或動作殘影。**解法**：新增短欄 `start_pose` 專供 `image_prompt`。
  2. **中譯英與解剖方位空間幾何（已實戰踩雷）**：`COSTUME_REGISTRY.md` 紀錄顯示，`fanli-outfit03-45.jpg` 第 1 次生成正是因人物朝向偏右導致**解剖學左眉尾傷痕（正面畫面右側）與左腰佩劍**被遮擋而失敗，直到改寫明確英文朝向描述才過關。單靠 `angle_h: three-quarter` 無法自動衍生出正確空間語句。
  3. **I2V `video_prompt` 逐字塞入定妝與服裝全文導致提示詞稀釋**：I2V 已經把人物臉與服裝畫在首幀圖裡了；若 `video_prompt` 又把角色卡＋服裝卡逐字拼接成 300+ 字肥大文本，Wan 2.2／LTX／H3 的動作與運鏡權重會被嚴重稀釋。`video_prompt` 應只帶短 `subject_anchor`（1–2 句識別特徵）＋動態／運鏡／收尾狀態。
  4. **各引擎方言差異大**：Veo／H3 吃電影敘事句，Wan 2.2 吃精煉「主體＋物理動作＋鏡頭移動」，LTX 吃超短直白英文（長 prompt 容易崩潰），同一套純公式字串直出給四個引擎必然水土不服。

---

### Q5 併入 DESIGN 後，Stage 1 與 Stage 2 契約要改哪些？schema 升 2.0 的遷移成本？

- **先對齊階段編號（防溝通錯位）**：草案 Q5 所稱「Stage 1（分鏡包產出）／Stage 2（資產／首尾幀）」，對應現行 `DESIGN.md` v1.4 §1.1 實際為：**上游封板（`second-civilization` 產出 `script_pack.json`）→ 階段 1（QC-0 入口驗證與資產／聲線鎖定）→ 階段 1.5（TTS 聲音先行）→ 階段 2（路由與企劃 `shot_plan.json`）→ 階段 3（首幀與 QC-1）**。另外 `DESIGN.md` v1.4 §0.2 的現行 schema 版本已是 **`1.3`**（不是 1.0）。
- **各站契約須修訂項目**：
  1. **上游封板 → 階段 1（QC-0 入口契約）**：
     - `script_pack.json` 升版 `schema_version: "2.0"`，新增 `segments[]`、升級扁平 `shots[]`。
     - **明確劃清上下游填欄責任（核心契約變更）**：上游（編劇／Muse）**只填敘事與靜態規格層（A–F 層、`asset_refs`、`outfit_id`、`priority`、`production_mode`、結構化 `visual_text_overlay`）**；下游工程層（最終 `engine_route`、英文 `image_prompt`/`video_prompt`、`first_frame`/`last_frame` 實檔、TTS 實測秒數與 H 層狀態）全由下游階段 1.5～5 寫入 `plan/shot_plan.json` 與 `plan/production_state.json`，不要求上游編劇在封板前填死。
     - QC-0 檢核清單併入可自動／半自動之 V1–V10 硬閘（對白速率、資產 ID 存在於 `assets_manifest.yaml` 且 `LOCKED`、FACT 來源綁定、零生成文字紅線）。
  2. **階段 1.5（TTS 聲音先行）契約**：
     - 因 v2 將 `dialogue` 升級為多句陣列 `[{line_id, speaker, line, tts_emotion_tags, delivery_mode, pause_after_sec}]`，`tts_batch_runner`（Phase 3 為單支腳本）須支援「同鏡多輪逐句生成 → 按 `pause_after_sec` 拼接為 `EP{NNN}_{TRACK}_{SHOT}_tts_v{V}.wav`」以及「跨鏡 `audio_group_id` 單一畫外音檔」兩種輸出，並將實測總秒數寫入 `production_state.json`。
  3. **階段 2（路由企劃）＆ 階段 3（首幀／尾幀）契約**：
     - 階段 2：讀取 `production_state.json` 的 TTS 實測秒數重新校核 V1，依引擎×`gen_mode` 相容表決定路由與 `gen_sec = target_net_sec + 1.0s`（2.5D 卡不加緩衝），生成英文雙 prompt 初稿。
     - 階段 3（QC-1）：**尾幀改為僅 `i2v_first_last` 鏡才生成**（避免產圖量與 QC-1 審圖量無謂 ×2）；首幀產圖順序正式消費 `asset_refs` 之 `scene→characters→props` 固定排序。
- **schema 升 2.0 的遷移成本評估**：
  - **程式碼遷移成本＝趨近於零**：依 ADR-002 與 `DESIGN.md` v1.4，Phase 5 的 8 支 P0 框架腳本目前皆尚未開發，且尚無已完工集數需要轉換，**現在（EP-01 開拍前）是升 2.0 成本最低的唯一黃金窗口**。
  - **真正要防的是「每集人工填表維護成本」**：若照草案原表每鏡填 30+ 欄，一集 20 鏡就是 600+ 格手工維護；必須靠「場段層繼承（減 ~35–40% 重複欄位）」＋「上下游分責（上游不填下游工程欄）」把填表成本壓到可控範圍。

---

## 二、欄位體檢（全表增刪改建議＋三項專題深檢）

### 2.1 三項指定專題深檢

1. **`gen_mode` 與各引擎真實能力**（詳見 Q3 對照表）：
   - 現行枚舉最大問題有二：① `text_only` 與被家規禁止的 T2V 撞名，且裝不下 S11 這類「實拍＋2.5D 疊加」混合鏡；② `multi_ref` 沒區分「**Stage 3 產首幀吃多圖**（Flow `nano2` 免費 10 張）」與「**Stage 4 生影片吃多圖**（僅 H3 Ref2V / Flow R2V，且 Flow R2V **禁帶首幀**）」。
2. **尾幀鏈（`prev_tail` ＋ 每鏡必填 `last_frame`）在 H3／Wan 上的可實作性**：
   - **兩種實作路線在我們產線都有硬傷**：
     - **路線 A（動態抽上一鏡實拍尾幀作下一鏡首幀）**：技術上用 `ffmpeg` 對 H3／Wan／Flow 產出抽幀都做得到，但會造成三個災難——① **打斷平行管線**：Shot N+1 必須等 Shot N 跑完 Stage 4 抽卡＋Stage 5 創作者挑片才能做首幀，Stage 3.5 LTX 全集預演直接癱瘓；② **畫質代際衰減**：影片抽出的 PNG 帶壓縮與臉部微漂，連鏈 3 鏡范蠡左眉尾傷痕必糊；③ **與「頭尾各剪 0.5 秒」家規衝突**：抽 `t = end - 0.5s` 當下鏡首幀，下鏡頭又剪 0.5s，接點仍跳掉 0.5 秒動作（除非為連鏈鏡開特例免裁頭）。
     - **路線 B（預先生成靜態尾幀圖跑 `i2v_first_last`）**：產圖量與 QC-1 審圖量直接 **×2**，且 `comfy-colab-kit` 的 `h3` 與 `wan` profile **尚未驗證**暴露 `end_frame` 參數。
   - **工程結論**：`prev_tail` 與 `last_frame` **絕不可設為同場預設或每鏡必填**，只保留給極少數偽長鏡／Match Cut（如 S12 燭火轉場），並標明需特例處理裁切與接受串行。
3. **`sub_shots` 與 Stage 3.5 LTX 預演的關係**：
   - `DESIGN.md` §1.3 的 LTX 預演是「每鏡 1 張核准首幀 → 1 次 LTX 低清生成（`N=1`）→ 掛正式 TTS 驗全集節奏與景別切換」。
   - 若一鏡內包 `sub_shots`（如 S16a 越宮捧劍＋S16b 太湖閉眼），因 `sub_shots` 沒有獨立首幀與資產，LTX 無法在單次生成內完成跨場硬切；若要正確預演，LTX 仍得把子鏡拆開各跑一支——等同宣告 `sub_shots` 在執行期必須被展平成獨立 `shot`。**直接廢除 `sub_shots`、改為扁平原子 `shots[]` 才是根本解**。

### 2.2 欄位增刪改建議總表

| 處置 | 層級／欄位 | 現況問題（對照實際下游工具） | 具體建議 |
| :---: | :--- | :--- | :--- |
| **刪** | E 層 `sub_shots` | 裝不下跨場／跨角／跨引擎子鏡；破壞 LTX 預演、首幀 1:1 與 `yield_log` | 刪除；改由 `segments[]` 場段層＋扁平原子 `shots[]`（如 `S16a`/`S16b`）表達 |
| **降** | B 層 `lens_hint` | 下游引擎無焦段參數，僅進 prompt 文字 | 降為選填 `camera_notes` 備註，不設獨立欄 |
| **降** | D 層 `screen_dir` | 落差分析已確認業界不設欄，我方多數鏡不適用 | 降為 `continuity_notes` 備註；改補實戰急需的 `subject_facing` |
| **降** | C 層 `last_frame` | 標為 ● 必填會讓產圖與 QC-1 翻倍，且 H3/Wan 閘道未驗證、頭尾剪 0.5s 使尾幀不入成片 | 降為 ◐ 條件必填（僅 `gen_mode=i2v_first_last` 時填） |
| **降** | C 層 `chain_break_reason` | 同場景反打／換景別本來就不該用 `prev_tail`，強填理由淪為廢話 | 隨 V4 方向反轉降為選填備註；改為僅啟用 `prev_tail` 時註明 `chain_trim_override` |
| **改** | D 層 `continuity_in` | 每鏡重複抄上鏡 `end_state`，改稿極易失同步自造 V5 錯 | 改為選填 `continuity_override`（僅跳場／刻意變化時填，其餘自動繼承上鏡 `end_state`） |
| **上移** | A/D/F 層 `scene_id`、`time_layer`、`atmosphere`、`ambience`、`bgm_cue` | 同場連續多鏡高度重複，且 `atmosphere` 與 `ambience` 聲音底色職責重疊 | 上移至 `segments[]` 作為段預設（`atmosphere` 純視覺、`ambience` 純聲音）；鏡級僅覆寫時選填 |
| **移出** | H 層 `state`、`fail_reason`、`selected_take`、`qc_checks` | 執行期高頻變動，寫入 `script_pack.json` 會破壞上游核准 SHA256 | 移至 `plan/production_state.json`；僅將 `should_generate` 改名 `production_mode` 留於規格 |
| **改** | C 層 `first_frame.source` | 僅 `generated / prev_tail / text_only`，裝不下 S16b 呼應 S01 的非相鄰鏡複用 | 改為 `generated / ref_shot / prev_tail / none_cpu_card`（`ref_shot` 可指定 `S01` 構圖複用或微調基底） |
| **改** | E 層 `duration_sec` | 未區分成片淨長 vs 含 1.0s 裁切緩衝之生成長；未對接 TTS 聲音先行 | 改名 **`target_net_sec`**（明定為成片淨秒數），並補 `duration_from_audio`（bool）與 `trim_policy`（`standard_0.5s / none / tail_only`） |
| **改** | F 層 `audio_mode` | 單選 `tts/native/post/silent` 無法表達「TTS 對白＋捨棄原片人聲＋後製 Room Tone/SFX」 | 拆為 **`voice_mode`**（`tts / none`）＋ **`ambient_source`**（`native_keep / post_roomtone / silent`） |
| **改** | G 層 `gen_mode` | `text_only` 與被禁 T2V 撞名；`multi_ref` 混淆產圖與生影 | 改為 `i2v_first / i2v_first_last / ref2v / cpu_card` |
| **改** | G 層 `visual_text_overlay` | 純字串陣列無法表達 S05 三連卡、S06 屏幕定位字、S11 兩段新聞卡進場時序，範例甚至混入「不重複」備註 | 升級為結構化陣列 `[{type, text, placement, start_sec, end_sec, fact_tier_override}]` |
| **補** | A 層 `dialogue[]` 內部欄位 | 缺 ElevenLabs v4 情緒標籤、露臉／畫外音區分、多輪換句停頓秒數 | 升級元素為 `{line_id, speaker, line, tts_emotion_tags[], delivery_mode: on_camera/off_camera/voiceover, pause_after_sec}` |
| **補** | A 層 `beat_ids`（或 `overlay_beat_id`） | S11 同鏡含 INFERENCE 台詞＋FACT 新聞卡，單一 `beat_id` 必撞 V10 或誤標事實層 | 保留主 `beat_id`（畫面敘事），並允許 `visual_text_overlay[]` 單獨綁定 `beat_id`（繼承該新聞卡之 FACT 來源與角標） |
| **補** | A 層 `priority` | 草案放回 beat 層，但同 beat 內英雄特寫（Flow）與過渡鏡（H3/Wan）路由不同，`shot_router` 讀不到 | **加回鏡級**（`hero / standard / insert`），對齊 `DESIGN.md` §2.4 |
| **補** | B/C 層 `start_pose`、`subject_facing`、`face_visible` | ① `image_prompt` 沒靜態起手式會失真；② 缺左右朝向曾害范蠡左眉尾傷痕翻車；③ V8 無法自動判定有無露臉 | 補 `start_pose`（● 必填，AI 鏡）、`subject_facing`（◐ 角色鏡填 `front/left/right/back`）、`face_visible`（● bool） |
| **補** | E 層 `reaction_hold_sec`、`audio_group_id` | ① V2 扣除反應拍卻無對應欄位；② S16 畫外音跨鏡與 J/L-cut 需群組對齊 `.ass` 字幕 | 補 `reaction_hold_sec`（預設 0，供 V2 自動算）與 `audio_group_id`（跨鏡共用 TTS 群組，對齊 `DESIGN.md` §5.1） |
| **補** | G/追蹤層 `lip_sensitive` | `DESIGN.md` v1.4 V1.4-03 規定於 Stage 3.5 標記正臉特寫開口鏡 | 補 `lip_sensitive`（bool，初值可由 `face_visible && on_camera && shot_size in [MCU,CU,ECU]` 自動預標，QC-1.5 人工定案寫入追蹤檔） |

---

## 三、驗證規則 V1–V10 可行性與衝突檢討

| 規則 | 檢核內容摘要 | 自動化可行性 | 衝突／過嚴／缺口診斷 | 修訂建議 |
| :---: | :--- | :---: | :--- | :--- |
| **V1** | 時長 ≤6.5s；`sub_shots` 總和相符 | **可全自動** | ① 未區分淨長 vs 生成長（淨 6.5s＝生成 7.5s，已超出 H3/Wan 甜區）；② 漏掉 LTX 正式鏡 **≤2.5s** 硬鎖；③ 聲音先行後實測秒數會覆蓋預估值 | 拆為兩段驗證：上游驗預估淨長（且依引擎別設上限：LTX ≤2.5s、H3/Wan 建議 ≤5.5s、Flow ≤6.5s）；Stage 1.5 後依 `D_tts + 0.4s` 重跑 V1 |
| **V2** | 對白速率（含標點 ≤5.5、純字 ≤5.0 字/秒），扣反應拍 | **補欄後可自動** | ① 引用了**不存在的欄位**（反應拍秒數）；② 未扣多輪換人停頓（S04 三輪壓線實拍必爆）；③ 未定中英數（如 `Altman`、`9,520`）計字規則 | 補 `reaction_hold_sec`；每增 1 輪換人自動扣 `0.35s`；明訂英文字按音節或固定折算（例 1 英文詞 ≈ 2 漢字） |
| **V3** | `asset_refs` ≥1（或 `text_only`），順序 `scene→characters→props` | **可全自動** | ① `text_only` 應改 `cpu_card`；② 未連動檢查 `asset_id` 是否已登錄於 `bible/assets_manifest.yaml` 且 `LOCKED` | 維持自動硬閘，並於 QC-0 連動查核 `assets_manifest.yaml` 與 `bible/voices/*.yaml`（`LOCKED`） |
| **V4** | 同場同層相鄰鏡須 `prev_tail`，否則必填 `chain_break_reason` | 格式可自動／理由需人工 | **嚴重過嚴且與產線衝突**：同場 80% 是正反打與換景別，強制 `prev_tail` 不只逼人寫廢話，還會打斷 Stage 3/3.5/4 平行批次、引發畫質衰減、與頭尾剪 0.5s 打架 | **反轉方向**：預設 `generated`（獨立首幀＋繼承段光線與上鏡色溫比對）；僅當 `transition_out.type = continuous/match-cut` 時才啟用 `prev_tail` 或 `i2v_first_last` |
| **V5** | `continuity_in` 與上鏡 `end_state` 不得矛盾 | **只能人工**（可輔以 LLM 初檢） | 純文字語意比對，確定性腳本做不到；且重複填寫易生雜訊 | 改為人工／LLM 語意審核提示項（Advisory），搭配 `continuity_override` 減少無謂抄寫 |
| **V6** | 一鏡一主動作、一鏡一運鏡 | **半自動**（運鏡可自動；主動作只能人工／LLM） | 草案自己的 **S04 範例就違反 V6**（單鏡寫了「聽完僵住→盯屏幕→轉身離開」三個動作） | 運鏡維持 schema 硬閘；主動作由人工／LLM 審核（建議限制動詞轉折 ≤1 次，超過即拆鏡） |
| **V7** | `end_state` 非空且不得只寫情緒 | 非空可自動／語意需人工 | 純字卡鏡（S05、S20）無人物道具狀態，硬套易誤報 | 允許 `cpu_card` 填固定枚舉 `card_hold` 或豁免；AI 鏡維持非空硬閘＋情緒詞警示 |
| **V8** | 有臉可見而 `microexpression` 為空＝不過 | **補欄後可自動** | 現行欄位沒有 `face_visible` 布林值，腳本無法精確判斷背影／遠景／手部特寫有沒有臉 | 補 `face_visible: bool` 即可全自動；並明訂「有臉但不開口（如 S16b 閉眼＋畫外音）」仍須填微表情但 `delivery_mode=voiceover` |
| **V9** | `visual_text_overlay` 以外文字需求一律駁回 | **半自動**（關鍵字告警＋人工終審） | 與 `DESIGN.md` §2.2 既有 `qwen-image`「產繁中文字畫面」條文存在潛在規範衝突 | 腳本掃描 `action`/`prompt` 敏感詞（字樣、標題、顯示、日期）發告警，並驗證 `avoid` 必含禁字詞；同步於 DESIGN v1.5 收斂 `qwen-image` 用途 |
| **V10** | FACT 層鏡的 `beat_id` 必連有來源綁定的 beat | **可全自動** | 單鏡混合「INFERENCE 台詞＋FACT 新聞卡」（如 S11）時，單一 `beat_id` 無法兼顧 | 擴充 V10：同時驗證 `shot.beat_id` 與 `visual_text_overlay[].beat_id`，任一指涉 FACT 者其 beat 必具非空 `source_ids` |

**小結**：V1–V10 中，修補缺欄後有 **5 條可全自動硬閘**（V1、V2、V3、V8、V10）、**3 條半自動／需人工語意審**（V6、V7、V9）、**1 條只能人工或 LLM 輔助**（V5）、**1 條建議反轉降級**（V4）。

---

## 四、試套驗證：以 EP-01 的 S11 與 S16 實填 v2 欄位找洞

> 依據 `DRYRUN-EP01-v0.3.1-BLIND.md` 逐欄硬填草案 v2 格式，所有「填不下去、被迫塞散文、或直接撞規則」的欄位以 `⚠️ [洞 #N]` 標註，文末彙整清單。

### 4.1 試套一：S11（新聞卡＋對白混合鏡）

- **劇本原文**（L63、L97–100）：`49–55s｜6s｜H3＋2.5D｜范蠡起身：「這齣戲，三年前演過一次。」她的屏幕切出 2023 新聞卡：2023 OpenAI 董事會解職 Altman→五天後 復職・董事會改組（FACT）。范蠡：「演員不同。開關一樣。」｜21 字／約 4.4s`

```json
{
  "shot_id": "S11",
  "scene_id": "LOC-FANLI-STUDIO-2026",
  "time_layer": "2026",
  "beat_id": "B-2023-PRECEDENT",        // ⚠️ [洞 #2] 台詞屬 INFERENCE、新聞卡屬 FACT(F5)，單一 beat_id 二擇一必違事實分層或撞 V10
  "beat_function": "TURN",
  "action": "范蠡起身望向屏幕說第一句；系統屏幕切出 2023 新聞卡；范蠡接說結論", // ⚠️ [洞 #5] 含起身＋切卡＋結論三段事件，直接違反 V6 一鏡一主動作
  "microexpression": "范蠡：眼神冷靜銳利、說『開關一樣』時眉心微收；系統：畫面切為新聞卡無臉",
  "dialogue": [
    {"speaker": "FANLI", "line": "這齣戲，三年前演過一次。"},
    // ⚠️ [洞 #3] 無法標註兩句之間要留 1.5s 給新聞卡進場！也無 tts_emotion_tags、無 delivery_mode（後句是切回臉還是壓在新聞卡上畫外音？）
    {"speaker": "FANLI", "line": "演員不同。開關一樣。"}
  ],
  "end_state": "范蠡已起身站立於書桌旁，眼神鎖定屏幕；系統屏幕停在 2023 新聞卡『董事會改組』頁",
  "shot_size": "MS",
  "angle_v": "eye",
  "angle_h": "three-quarter",           // （漏左右朝向：范蠡左眉尾傷痕朝哪側不明）
  "movement": {"type": "push-in", "speed": "slow"},
  "asset_refs": [
    {"asset_id": "LOC-FANLI-STUDIO-2026", "role": "scene"},
    {"asset_id": "FANLI", "role": "character"},
    {"asset_id": "SYS-01", "role": "character"}
  ],
  "outfit_id": {"FANLI": "FANLI-OUTFIT-01"},
  "first_frame": {"source": "generated", "ref_id": "S11-first.png", "status": "planned"},
  "last_frame": {"ref_id": "S11-last.png", "status": "planned"}, // H3 未驗證首尾幀，且尾幀被剪 0.5s 不會播
  "chain_break_reason": "上鏡 S10 為系統屏幕特寫，本鏡反打切回范蠡起身，無法繼承尾幀", // ⚠️ [洞 #5] 同場正常反打竟被迫填斷鏈理由（V4 過嚴）
  "continuity_in": "承 S10：范蠡原坐於書桌前聽完系統回答，屏幕亮於桌上",
  "lighting_state": "深夜套房暖暗室光＋窗外巨幕與桌面屏幕冷藍光，match_prev: true",
  "duration_sec": 6.0,                  // 未標明是淨長（生成需 7s，超 H3 甜區）還是生成長
  "transition_out": {"type": "cut", "trigger": "action"},
  "ambience": "深夜室內靜音、窗外遠處城市低頻",
  "sfx": ["屏幕切換資訊卡的清脆提示音"],
  "bgm_cue": "none",
  "audio_mode": "tts",                  // 無法同時表達「TTS 人聲＋捨棄原片人聲＋後製提示音與底噪」
  "engine_route": "h3",                 // ⚠️ [洞 #1] 劇本寫「H3＋2.5D」，單選枚舉塞不下混合引擎，下游漏跑 2.5D 卡
  "gen_mode": "first_only",             // ⚠️ [洞 #1] 無「實拍底片＋後製動態卡合成」模式
  "face_lock_level": "strict",
  "visual_text_overlay": [
    "2023 OpenAI 董事會解職 Altman",
    "五天後 復職・董事會改組（FACT）"    // ⚠️ [洞 #4] 純字串陣列無法區分「屏幕內透視貼圖 vs 全屏硬切 2.5D 卡」，也無兩段出現時間碼與 FACT 角標綁定
  ]
}
```

### 4.2 試套二：S16（閃回段落鏡）

- **劇本原文**（L68、L110、備註⑤）：`74–80s｜6s｜Wan｜S16a（3s）內侍捧劍而至，只拍手與劍。S16b（3s）湖上，使者的小船靠近，范蠡聽完死訊，閉眼——與 S01 同一瞬間（以同一構圖呼應）。畫外：「他信了。他只是走不了。」｜10 字／約 2.1s`

```json
{
  "shot_id": "S16",
  "scene_id": "LOC-YUE-MANOR + LOC-TAIHU-BOAT", // ⚠️ [洞 #6] 兩拍場景完全不同，父層單一 scene_id 根本填不下去！
  "time_layer": "春秋",
  "beat_id": "B-WENZHONG-DEATH",
  "beat_function": "PAYOFF",
  "action": "內侍捧劍入畫；切湖上使者小船靠近，范蠡聽完死訊緩緩閉眼",
  "microexpression": "S16a 無（不露臉）；S16b 范蠡聽訊後喉結微動、緩緩閉眼不語", // ⚠️ [洞 #8] 一拍無臉一拍有臉，V8 自動驗證直接崩潰
  "dialogue": [
    {"speaker": "FANLI", "line": "他信了。他只是走不了。"} // ⚠️ [洞 #8] 缺 delivery_mode=voiceover 與跨子鏡範圍！下游會誤導 S16b 讓閉眼的范蠡張嘴唸台詞
  ],
  "end_state": "范蠡在太湖小舟上閉目定格，對面空座，與 S01 首幀構圖重合", // （S16a 自己的 end_state 無處可放）
  "shot_size": "INSERT",                // ⚠️ [洞 #6] S16a 是 INSERT、S16b 是 MS，父層硬填其一必錯
  "angle_v": "eye",
  "angle_h": "three-quarter",
  "movement": {"type": "static", "speed": "slow"},
  "asset_refs": [
    // ⚠️ [洞 #6] 兩拍無關資產被迫混成一鍋：餵圖會把越宮賜劍跟太湖小舟融在一起！
    {"asset_id": "LOC-YUE-MANOR", "role": "scene"},
    {"asset_id": "LOC-TAIHU-BOAT", "role": "scene"},
    {"asset_id": "FANLI", "role": "character"},
    {"asset_id": "PROP-YUE-SWORD", "role": "prop"}
  ],
  "outfit_id": {"FANLI": "FANLI-OUTFIT-02"},
  "first_frame": {"source": "generated", "ref_id": "S16a-first.png", "status": "planned"}, // ⚠️ [洞 #6/#7] ① S16b 沒位置放自己的首幀；② S16b 必須呼應 S01 構圖，source 卻沒有 ref_shot: "S01"
  "last_frame": {"ref_id": "S16b-last.png", "status": "planned"},
  "continuity_in": "承 S15：越國朝堂文種空座（S16a 切至文種府門賜劍，S16b 再切太湖）",
  "lighting_state": "S16a 室內陰冷廊光／S16b 太湖晨霧冷灰柔光，match_prev: false", // ⚠️ [洞 #6] 單欄被迫硬塞兩套光線
  "duration_sec": 6.0,                  // ⚠️ [洞 #9] 若拆兩支 Wan 實拍須各 +1.0s（4s＋4s＝8s 原始生成）；寫成父層 6s 會誤路由為單支 7s 影片，爆掉 Wan 甜區且切不了場
  "sub_shots": [
    {
      "sub_id": "S16a",
      "duration_sec": 3.0,
      "action": "內侍雙手捧青銅賜劍緩步遞出（只拍手與劍，不露臉）",
      "camera": {"shot_size": "INSERT", "angle_v": "high", "angle_h": "front", "movement": {"type": "push-in", "speed": "slow"}}
    },
    {
      "sub_id": "S16b",
      "duration_sec": 3.0,
      "action": "晨霧太湖，遠處使者小船划近；舟上范蠡聽完死訊緩緩閉眼（與 S01 同構圖）",
      "camera": {"shot_size": "MS", "angle_v": "eye", "angle_h": "three-quarter", "movement": {"type": "static", "speed": "standard"}}
    }
  ],
  "transition_out": {"type": "hard-cut", "trigger": "sound"},
  "ambience": "S16a 死寂衣袂聲／S16b 晨霧太湖輕波水聲",
  "sfx": ["劍鞘輕置木案聲", "木槳輕撥水聲"],
  "bgm_cue": "03_Historical_Echo",
  "audio_mode": "tts",
  "engine_route": "wan",
  "gen_mode": "first_only",
  "face_lock_level": "standard",        // ⚠️ [洞 #6] S16a 應為 none、S16b 應為 strict/standard，父層衝突
  "visual_text_overlay": []
}
```

### 4.3 試套發現的規格洞彙整（共 **9 處**）

| 編號 | 試套鏡 | 規格洞摘要 | 生產實務後果 |
| :-: | :-: | :--- | :--- |
| **#1** | S11 | `engine_route` 與 `gen_mode` 無法表達「實拍影片＋2.5D 新聞卡」混合鏡 | 路由器只送 H3、漏掉 CPU 2.5D 卡生成或後製合成指令 |
| **#2** | S11 | 單一 `beat_id` 裝不下「`INFERENCE` 台詞＋`FACT` 新聞卡」混合事實分層 | 要嘛丟掉 F5 來源綁定撞 V10，要嘛把推論誤標為 FACT 踩紅線 |
| **#3** | S11 | `dialogue[]` 缺句間停頓（`pause_after_sec`）、`tts_emotion_tags` 與 `delivery_mode` | TTS 把兩句連唸完，中段新聞卡無處插隊；口型與情緒無依歸 |
| **#4** | S11 | `visual_text_overlay` 純字串陣列裝不下「屏幕內貼圖 vs 全屏插卡」與分段進場時碼 | 下游 `ffmpeg`／`fact_card_renderer` 無法消費，且兩種做法工程成本差十倍 |
| **#5** | S11 | 單鏡塞三段動作撞 V6；同場正常反打卻被 V4 逼填 `chain_break_reason` | 規則與實際短劇剪輯節奏打架，製造大量填表雜訊 |
| **#6** | S16 | `sub_shots` 缺場景、資產、服裝、首尾幀、光線、保臉等級 | 父層被迫混裝兩場景資產（餵圖融怪圖），LTX 預演與 Wan 批次完全無法執行 |
| **#7** | S16 | `first_frame.source` 缺少「引用非相鄰前鏡構圖（`ref_shot: S01`）」 | S01↔S16b 首尾呼應（Bookend）只能寫在散文備註，失去機器契約 |
| **#8** | S16 | 畫外獨白跨子鏡＋不露臉/閉眼無 `voiceover` 與 `face_visible` 標記 | `video_prompt` 誤讓閉眼范蠡張嘴說話毀戲；V8 自動檢查無法運作 |
| **#9** | S16 | `duration_sec` 未區分淨長與每支獨立裁切緩衝（`+1.0s`） | 6s 段落鏡被誤算為 7s 單支影片（爆 Wan 甜區），而非兩支各 4s 獨立生成再各裁 1s |

---

## 五、結構替代案與取捨：輕量兩層制 × 雙檔分離

我不只批評，以下直接給出可落地的替代結構（建議作 `schema_version: "2.0"` 基準），把上述 **9 個洞一次填平**。

### 5.1 替代架構概覽

```text
episodes/EP001/
├── input/script_pack.json          # 【不可變真相・鎖上游 SHA256】
│   ├── episode metadata + event_anchor + beats[]
│   ├── segments[]                  # ① 場段層：scene_id, time_layer, lighting_base, atmosphere, ambience, bgm_cue, audio_groups[]
│   └── shots[]                     # ② 扁平原子鏡層：1 筆 = 1 張首幀 = 1 支生成片（刪 sub_shots，經 segment_id 繼承場段預設）
│
└── plan/production_state.json      # 【執行期可變檔・不汙染上游 SHA256】
    └── shots_state[shot_id]        # TTS 實測秒數與 audio_ref、最終路由與降級、英文雙 prompt+override_reason、
                                    # 首尾幀實檔、lip_sensitive、H 層（state/takes[]/selected_take/fail_reason/audio_offset_ms）
```

### 5.2 兩鏡在替代案下的落地寫法（極簡示意）

- **S11（新聞卡＋對白混合鏡）——推薦「剪輯結構拆鏡法」（0 動態追蹤成本）**：
  - 同屬 `segment_id: "SEG-04"`（2026 深夜套房），在扁平 `shots[]` 拆為 3 顆原子鏡，乾淨解決洞 #1～#5：
    - `S11a`（淨 2.0s，`h3`，`i2v_first`，`beat_id: B-INF-2023`）：范蠡起身「這齣戲，三年前演過一次。」
    - `S11b`（淨 2.2s，`ffmpeg_card`，`cpu_card`，`trim_policy: none`，`beat_id: B-FACT-F5`）：全屏高質感 2.5D 新聞卡兩段顯示（自動帶青綠色 `FACT` 角標、自動驗證 F5 來源），0 GPU 零穿幫！
    - `S11c`（淨 1.8s，`h3`，`i2v_first`，`beat_id: B-INF-2023`）：切回范蠡中近景（或 L-cut 接尾音）「演員不同。開關一樣。」
  - *（若導演堅持新聞卡必須嵌在半透明系統屏幕框內不切全屏，則保留單鏡 `h3` 底片＋結構化 `visual_text_overlay` 標記 `placement: diegetic_screen`＋`beat_id: B-FACT-F5`，但須接受後製需加做透視合成與追蹤工時。）*

- **S16（閃回段落鏡）——扁平雙原子鏡＋共享 `audio_group`**：
  - 同屬 `segment_id: "SEG-06"`（春秋尾聲），在 `SEG-06.audio_groups` 定義 `AG-S16`（`FANLI`、`delivery_mode: voiceover`、「他信了。他只是走不了。」），`shots[]` 放兩筆獨立原子鏡，乾淨解決洞 #6～#9：
    - `S16a`（淨 3.0s／生成 4.0s，`wan`，`i2v_first`，`scene_id: LOC-YUE-MANOR`，`face_visible: false`，`audio_group_id: AG-S16`）：內侍雙手捧劍特寫。
    - `S16b`（淨 3.0s／生成 4.0s，`wan`，`i2v_first`，`scene_id: LOC-TAIHU-BOAT`，`first_frame: {source: "ref_shot", ref_shot_id: "S01"}`，`face_visible: true`，`microexpression: "閉目不語"`，`audio_group_id: AG-S16`）：太湖小船靠近，范蠡閉眼與 S01 同構圖呼應，因屬 `voiceover` 不驅動口型！

### 5.3 三方案取捨對照表

| 評估維度 | 方案 A：草案原案<br>（單層＋`sub_shots`＋H 層內嵌） | **方案 B：本備忘錄推薦**<br>（`segments[]`＋扁平原子 `shots[]`＋雙檔分離） | 方案 C：Huobao 全重型<br>（巢狀 `segments[].shots[]`＋強尾幀鏈） |
| :--- | :--- | :--- | :--- |
| **每集填表量（20 鏡）** | 高（~600 格，同場屬性重複抄） | **最低**（共用屬性上移段層，減 35–40%） | 中高（每鏡仍需維護尾幀與巢狀層級） |
| **下游工具相容度**<br>（LTX 預演／TTS／雙引擎／ffmpeg） | 低（`sub_shots` 與混合鏡需大量特判） | **最高**（1 筆 `shot`＝1 首幀＝1 支片，零遞迴） | 中（巢狀結構需展平，強尾幀鏈卡死平行批次） |
| **Phase 3 半自動友善度**<br>（對齊 ADR-002） | 中（手工核對易漏改重複欄位） | **高**（上下游分責，人工檢核清單直觀） | 低（無 UI 工作台時手工維護巢狀 JSON 痛苦） |
| **上游核准 SHA256 與 Git Diff** | 破防（H 層執行態會改寫劇本包） | **100% 乾淨**（輸入不可變、狀態獨立檔） | 視實作（通常狀態混入資料庫，不合 Git） |
| **主要代價／取捨** | 改動最少，但實拍必在 S04/S11/S16 撞牆 | 劇本總鏡數視覺上會微增（如 20 邏輯鏡 → 23–24 原子鏡），編劇需習慣把複合拍拆成原子鏡（用 `S16a`/`S16b` 編號即可維持閱讀直覺） | 僅在導入重型桌面／Web 工作台時划算，違反我方減法紀律 |

---

## 六、建議下一步（不改原檔，供 Muse 與 Creator 拍板）

若 Muse 與 Creator 認可上述方向，建議按三步定版 v2：
1. **拍板兩項架構原則**：① 採「`segments[]`＋扁平原子 `shots[]`」取消 `sub_shots`；② H 層＋TTS 實測＋路由實態獨立為 `plan/production_state.json`。
2. **拍板兩項規格修訂**：① 反轉 V4（預設獨立首幀、尾幀改條件選填）；② 補齊 TTS 聲音先行欄位（`tts_emotion_tags`、`delivery_mode`、`pause_after_sec`、`reaction_hold_sec`、`audio_group_id`）、結構化 `visual_text_overlay`、`start_pose`、`subject_facing`、`face_visible` 與鏡級 `priority`。
3. 定版後由 Muse 修訂 `STORYBOARD-SPEC-V2-DRAFT.md` → 同步升版 `DESIGN.md` `script_pack` 契約至 schema 2.0 → 直接套入 EP-01 正式分鏡包開拍。
