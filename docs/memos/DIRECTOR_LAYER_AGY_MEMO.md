# 導演層規格（Director's Layer）工程討論備忘錄（agy 立場文件）

> **文件定位**：書面工程討論備忘錄（只討論，不改任何規格本體、不生產、不 push）  
> **撰寫日期**：2026-11-27  
> **審閱標的**：`DIRECTOR-LAYER-SPEC-DRAFT.md`、`DEMO02-DIRECTOR-STATEMENT.md`  
> **對照基準**：`STORYBOARD-SPEC-V2.md`（v2.0 FINAL＋附錄 A 運鏡控制）、`DESIGN.md`（v1.4）、`CAMERA_WORKFLOW_AGY_MEMO.md`、`COSTUME_REGISTRY.md`，以及實查 `demo01/` 成品影格、首幀與音檔實測數據（`sys.mp3` = **5.41s**、`fanli.mp3` = **2.12s**、clips = **7.93s / 720×1280 / 24fps**）。

---

## 零、單一結論（先亮底牌）

**有條件同意併入 `STORYBOARD-SPEC-V2`（升 v2.1）與 `DESIGN`（升 v1.5），但不可照草案原樣直併，須先完成六項工程修訂**：
1. **欄位去冗餘與層級歸位**：`light_lock_id` 上移至 `segments[]`（鏡級不重填）；`world_reaction` 改為段級預設＋條件必填（並補 `public_exposure`/`anomaly_level` 使 V12c 可程式化）；`performance_beat` 結構化為 `{from, trigger, to, deliberate_hold}` 避免與既有 `start_pose`/`end_state` 雙重抄寫；`vfx_beat` 改為陣列 `vfx_beats[]` 並標註執行層（`gen_prompt`/`post_ffmpeg`/`hybrid`）。
2. **V12a 成片端降為「半自動標記＋人工終判」**：遵循 `DESIGN.md` §7.1 鐵律，嚴禁腳本全自動駁回（否則 S3 藍光彈窗與 S4 膚色特寫必遭誤殺），且光線檢查主防線須前移至 **QC-1 首幀門**。
3. **補齊 `camera_psychology` 引擎邊界**：取消自由文字後綴（如「`handheld_anxiety 稍緩`」改以 `movement.amplitude: small` 控制），並明訂 Veo/H3 做不到的「失焦再合焦」與「過穩補抖」改走 ffmpeg 後製。
4. **統一階段編號與快線豁免**：對齊 `DESIGN.md` v1.4，導演闡述改列為 **階段 0.5（上游分鏡封板前置）** 而非會撞號的 Stage 2.5；快線（3.5h SLA）走 3 分鐘極簡導演卡。
5. **精準化 QC-D 落點**：**反對**把 QC-D 放在 `DESIGN.md` 的 QC-2（Stage 5 挑片）之前；改為「QC-2 挑片內嵌單鏡導演篩」＋「**Stage 6A 極速粗剪 →【QC-D 導演閘】→ Stage 6B 精修封裝／Stage 7 社群包／QC-3 技術終審**」，才能在不破壞 10 秒 `auto_tech_qc` 的前提下真正省去後續技術精修工時。
6. **DEMO-02 開拍前必先修正 S3 結構矛盾與超時**：`sys.mp3` 實長 5.41s，按原稿 6 秒＋B 幀首幀烘焙彈窗會同時撞爆 Veo 8s 上限與「從無到有閃入」邏輯，須拆為 `S3a`＋`S3b`（跨切點 glitch 閃入）並搭配 L-cut。

---

## 一、Q1–Q6 逐題答覆

### Q1 欄位落點與填表量評估

#### 1. 六欄逐項落點裁決（對齊 v2.0 兩層制 × 雙檔分離原則）

`STORYBOARD-SPEC-V2.md` 已確立兩條架構原則：**「共用上移，禁止同場重複抄寫」**與**「上游 `script_pack.json` 核准後鎖 SHA256，執行期可變狀態一律放 `plan/production_state.json`」**。六欄依此原則歸位如下：

| 草案欄位 | 原定位置／必填 | 工程審查問題 | 修訂落點與必填性 |
| :--- | :--- | :--- | :--- |
| **`light_lock_id`** | `shots[]` ● | 違反 v2 共用上移原則；與 `segments[].lighting_base` 形成雙重真相；20 鏡重複抄寫徒增人誤 | **上移至 `segments[]`（● 必填）**；鏡級預設繼承、不重填，僅劇情光變事件於既有的 `shots[].lighting_state` 覆寫並註記理由 |
| **`world_reaction`** | `shots[]` ● | 本劇常線 60–75% 為室內戲或 2.5D 圖卡，逐鏡必填 `none`＋理由為純冗餘；且 DEMO-02 S2 已出現複數值（`double_take＋filming`） | **拆層**：`segments[]` 補 `public_exposure` ●、`anomaly_level` ●、`world_reaction_default` ●；`shots[]` 改為 **條件必填 ◐**（僅偏離段預設或高異常公開鏡填寫），值域改為結構化物件含 `types[]` 陣列 |
| **`shot_intent`** | `shots[]` ● | 屬鏡級創作契約，落 `shots[]` 合理 | **保留 `shots[]`（● 必填）**，限 ≤20 字一句話（`cpu_card` 填資訊目的） |
| **`performance_beat`** | `shots[]` ● | 與既有 `start_pose`／`action`／`end_state` 高度重疊，散文並存極易雙重抄寫或互相矛盾；且「起→觸發→迄」易與 V6（動詞轉折 ≤1）定義混淆；`cpu_card`/純空鏡不適用 | **保留 `shots[]`（◐ 僅 AI 人物鏡必填）**，改為精簡結構 `{from, trigger, to, deliberate_hold, hold_intent?}`——僅補 v2 真正缺的「**狀態標籤＋觸發因**」，細節姿勢仍歸 `start_pose`/`end_state` |
| **`camera_psychology`** | `shots[]` ● | 同一 segment 內確實會逐鏡演進（如 DEMO-02 四鏡由慌轉穩），放 `shots[]` 合理；但 `cpu_card` 應豁免，且禁自由文字後綴（如「稍緩」） | **保留 `shots[]`（◐ 非 `cpu_card` 必填）**；`segments[]` 另記段級弧線文字（導演闡述）；強弱調節一律走既有 `movement.amplitude` |
| **`vfx_beat`** | `shots[]` ○ | DEMO-02 S3 已用複數值（`glitch_in＋sound_drop`），單一標量枚舉裝不下；且缺「生成內做 vs 後製做」的分工宣告 | **保留 `shots[]`（○ 選填）**，改為陣列 **`vfx_beats[]`**，每項含 `{type, exec_layer: gen_prompt\|post_ffmpeg\|hybrid, note}` |

#### 2. 應拆入 `plan/production_state.json` 與導演闡述的資料
- **`episodes/EP{NNN}/input/director_statement.md`**（核准後併入 `approval_upstream.json` SHA256）：放人類閱讀用的完整敘事闡述（情緒曲線、場景邏輯論證、光線鎖定視覺規格、世界反應與特效拍點設計理由），其結構化鍵值同步寫入 `script_pack.json` 的 `segments[]`。
- **`episodes/EP{NNN}/plan/production_state.json`**（執行期可變，不汙染上游 SHA256）：
  - `v12_lighting_metrics`：每鏡首幀與入選成片之 Lab 抽幀色溫數值、`FLAGGED` 狀態與人工 `override_pass` 備註。
  - `vfx_exec_artifacts`：實際後製參數（如 `sound_drop` 精確秒數區間、疊加 SFX 檔名、`glitch_in` 跨幀時間碼與濾鏡參數）。
  - `qc_d_review`：QC-D 6 項逐項 `PASS/FAIL`、一句證據、退回工位與是否已回寫 `bible/director/playbook.md`。

#### 3. 填表量增幅精算（以 1 集常線＝20 原子鏡、4 segments、含 3 支 `cpu_card`＋2 支空鏡計）

| 版本 | 段級實填格數 | 鏡級上游實填格數 | 單集合計 | 相對 v2.0 增幅 |
| :--- | :---: | :---: | :---: | :---: |
| **現行 v2.0＋附錄 A** | ~24 格 | ~390 格（~19.5 欄/鏡） | **~414 格** | 基準 |
| **原草案直併**（6 欄全放 `shots[]`） | +24 格（闡述） | +110 格（5 必填×20＋`vfx_beat/note`×5） | **~548 格** | **+32.4%**（其中 ~40% 為重複抄寫冗餘） |
| **我方修訂版**（共用上移＋條件必填＋豁免） | +16 格（淨增，整合 `lighting_base`） | +62 格（`shot_intent` 20＋`performance_beat` 15＋`camera_psychology` 17＋覆寫 `world_reaction` 4＋`vfx_beats` 6） | **~492 格** | **+18.8%**（較原草案**省 ~42% 新增填表量**） |

---

### Q2 V12 導演護欄可驗證性與定稿建議

#### 1. V12a 光線硬閘：抽幀色溫比對的具體做法與誤判風險
- **防線前移（最關鍵）**：成片抽卡後才抓到「黃昏跳夜晚」代價太高（Flow 點數與 Colab CU 已燒完）。V12a 視覺比對必須在 **QC-1（Stage 3 首幀門）** 與 **QC-2（Stage 5 挑片門）** 雙站執行，並**直接整合進 `DESIGN.md` §7.1 既有的 `visual_qc_helper.py` 第四維（場景光線色溫）**，不重複建第二套工具。
- **具體演算法（VM 純 CPU：`ffmpeg` ＋ Python/Pillow/NumPy，0 GPU）**：
  1. **抽幀**：QC-1 直接吃核准候選首幀 PNG；QC-2 複用附錄 A.6 的有效區間 `[+0.5s, end-0.5s]`，擴取 5 幀（`0% / 25% / 50% / 75% / 100%`）取**時間維度中位數**，自動濾除 S1 路燈閃爍等瞬態跳動。
  2. **色彩空間與遮罩**：轉為 **CIE Lab**（`L*` 明度、`a*` 紅綠、`b*` 黃藍軸——`b*` 直接表徵色溫冷暖），並排除「極暗像素 `L*<8`」「過曝燈源 `L*>92`」與「中央 40% 主體區（或針對 `CU`/`ECU` 僅取外圍 20% 邊框並排除膚色區）」，僅統計**環境背景區**之 `L*_med`、`b*_med` 與**畫面上 25% 區域亮度 `top25_L*_med`**（專門抓 DEMO-01 鏡 A 黃昏亮天空 vs 鏡 B 黑夜天空的跳變）。
  3. **雙重比對**：
     - 對照該 `light_lock_id` 定義的容許帶（如 `LK-ALLEY-NIGHT`：`L*_med ∈ [15, 42]`、`b*_med ∈ [-18, +4]`、`top25_L*_med < 45`）；
     - 對照同 segment 基準場景空景圖及相鄰前鏡之相對差值：`|ΔL*_med| > 15` 或 `|Δb*_med| > 12` 標記 `LIGHTING_TEMP_SHIFT`。
- **五大誤判風險（為何絕不可做全自動硬閘駁回）**：
  1. **劇情特效光源染色（高發誤殺）**：實測 `demo01/sheetB.jpg` 可見，藍色全息彈窗一出現便把半張臉與背景染成強青藍，`b*` 驟降 15–25；若全自動駁回，DEMO-02 S3 必被誤殺。→ **對策**：含 `vfx_beats` 為 `glitch_in`/`light_shift`/`composite_ui` 的鏡頭自動放寬 `b*` 門檻並僅標提示。
  2. **景別劇變導致膚色佔比扭曲**：MS 背景佔 70%，CU 特寫膚色佔 60%（東亞膚色天生偏暖 `b* > +10`），全圖平均必報「色溫跳暖」。→ **對策**：`CU`/`ECU` 強制切換為外圍 20% 邊框背景採樣。
  3. **雙色溫實景正反打（如台北街頭暖招牌 vs 冷暗巷）**：機位轉 180° 就會因背景光源結構不同造成全圖 `b*` 偏移。
  4. **瞬態閃光（`env_reaction` 路燈閃爍）**：單幀抽樣撞上熄燈瞬間會誤報 `L*` 暴跌。→ **對策**：5 幀中位數平滑。
  5. **假陰性（數值近但體感跳天氣）**：陰天漫射光與室內灰燈可能 `L*`/`b*` 接近，但陰影硬度與反光全異，仍須人眼把關。
- **定稿處置**：遵循 `DESIGN.md` §7.1 鐵律——**靜態層（`segments[].light_lock_id` 存在性）為全自動硬閘；視覺抽幀層為「半自動 `FLAGGED` 提示＋人工終判（支援帶理由 `override_pass`）」，嚴禁腳本自動駁回或自動重算**。

#### 2. V12a–V12e 驗證手段定稿總表

| 規則 | 驗證站點 | 層級 | 驗證手段定稿 | 可形式化規則（機器執行） | 須人工把關項目 |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **V12a 光線護欄** | QC-0 ＋ QC-1 ＋ QC-2 | 規格硬閘／視覺半自動 | 靜態自動＋Lab 背景區抽幀標記＋人工終判 | ① `segment.light_lock_id` 必填且存在於光線表；② 鏡級 `lighting_state` 覆寫須附理由或綁 `light_shift`；③ 背景 Lab `ΔL*`/`Δb*` 與 `top25_L*` 超界標 `LIGHTING_TEMP_SHIFT` | 判斷偏移是否屬合理劇情光源（如彈窗藍光、正反打暖燈）並決定駁回或 `override_pass` |
| **V12b 表演拍完整性** | QC-0（規格）＋ QC-2（動態） | 結構硬閘／語意人工 | 結構全自動＋Muse/LLM 初檢 Advisory | 非 `cpu_card`/空鏡之人物鏡：① `deliberate_hold=false` 時 `from`、`trigger`、`to` 皆非空且 `from != to`；② `deliberate_hold=true` 時 `hold_intent` 非空 | 抓「換詞不換意」假變化（如站著→繼續站著）；確認動作變化在淨秒數內可演且未違反 V6；成片實看有無呆站 |
| **V12c 世界反應合理性** | QC-0 ＋ 導演闡述拍板 | 觸發硬閘／理由人工 | 條件全自動駁回＋豁免理由人工審 | `public_exposure != "private"` **AND** (`anomaly_level == "overt"` 或 `2022/2026` 穿 `OUTFIT-02/03`) **AND** `world_reaction.types == ["none"]` **AND** `exempt_reason` 空 → **自動駁回** | 審查 `exempt_reason` 是否自欺欺人（例如「路人都在低頭滑手機沒看見」一律不放行） |
| **V12d 鏡頭多元性** | QC-0 ＋ QC-1 | Advisory（告警） | 滑動視窗全自動＋拼圖人工目視 | 同 segment 連續 3 鏡 `(shot_size, angle_v, angle_h)` 全同（或 `shot_size`＋`movement.type` 全同）且無 `monotony_exempt_reason` → 發 `WARN_SHOT_MONOTONY`（移除無法形式化之「構圖重心」） | 於 QC-1 首幀聯絡表（contact sheet）一眼檢核構圖重心與視線節奏變化 |
| **V12e 運鏡心理一致性** | QC-0（靜態）＋ QC-D（動態） | 靜態自動告警／動態人工 | 查衝突矩陣全自動（見 Q3 表）＋成片人工驗 | 查 `camera_psychology × movement` 衝突矩陣（如 `handheld_anxiety` 配 `static`、`stable_control` 配 `handheld`）→ 發 `WARN_CAM_PSYCH_MISMATCH`（需填 `camera_override_reason` 豁免） | 實看生成影片動態是否真的達標（AI 常把 `handheld` 偷平滑成穩軌） |

---

### Q3 `camera_psychology` 衍生映射表（可直接併入附錄 A）

#### 1. 關鍵工程前提與引擎能力誠實邊界
- **禁止自由文字後綴**：`camera_psychology` 嚴守 6 個受控枚舉；強弱層次（如 DEMO-02 S2 的「`handheld_anxiety 稍緩`」）一律透過附錄 A.2 既有的 **`movement.amplitude`（`small` / `medium` / `large`）** 表達。
- **現行引擎（Veo 3.1 / MiniMax H3 / Wan 2.2）明確做不到或服從度極低的四件事**：
  1. **「輕微失焦再合焦（focus hunt / rack focus）」**：Veo 3.1 與 H3 皆無對焦參數，I2V 首幀本就清晰，硬寫常被忽略或導致整段糊臉。**對策**：一律交 **ffmpeg 後製**（於起鏡 0.0–0.5s 疊加動態衰減高斯模糊 `gblur`，0 GPU、100% 精準保臉）。
  2. **「不規則手持＋跟拍遲滯半拍（delayed follow lag）」**：Veo 3.1 內建強電影防手震偏向，僅寫 `handheld` 常出 Steadicam 穩鏡；精準「遲滯半拍再追上」服從度低（~20–30%）。**對策**：① 首幀採偏心構圖留出位移空間，prompt 寫具體物理現象（`off-center framing`, `unsteady documentary handheld`）；② 若抽片演技佳但運鏡偏穩，**不報廢重抽**，直接以 ffmpeg 做 4–5% 裁切＋多頻正弦非週期微抖（`crop` 座標疊加不可公約頻率 `sin`）補救。
  3. **「從第三人稱首幀中途鑽入 `subjective_pov`」**：I2V 必崩。**對策**：`subjective_pov` 的 90% 成敗決定於 Stage 3 首幀必須直接畫成主觀視角（`angle_h: POV`、`face_visible: false`）。
  4. **「`predator_stalk` 繞過前景實體遮擋揭示主體」**：L1 文字提示易穿模或主體變臉。**對策**：升級 **L3 CozyClay 白膜**（受 V11 每集 0–2 鏡配額約束）。

#### 2. `camera_psychology` 完整衍生映射表（附錄 A 增補定稿草案）

> 註：★ 標記為建議於 `bible/camera/named_shots.yaml` 增補之 4 個受控鏡型 ID（全部初標 `UNTESTED`，隨實跑回填）。

| `camera_psychology` | 對應 `movement` 建議值（`type` / `speed` / `amplitude`） | 推薦 `named_shot` | H3 官方方言句式（嵌入 `integrated_multimodal_description` / `detailed_description`，零裸否定詞） | Flow（Veo 3.1）Seedance 句式 | Wan 2.2 極簡句式（限無正臉鏡） | V12e 衝突矩陣（觸發告警） | 引擎盲區與後製／分級補救 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`stable_control`**<br>冷靜掌控／自制收束 | `static` 或 `push-in`<br>`speed: slow`<br>`amplitude: small` | `steady-dialogue-lock`<br>`slow-push-verdict`<br>`low-angle-authority` | `Static Shot, locked tripod framing holding steady on <Subject 1>.` 或 `The camera pushes in with small amplitude at slow speed toward <Subject 1>'s eyes.` | `Locked-off steady cinema camera, rock-solid framing.` 或 `Controlled, ultra-smooth slow dolly push-in tightening onto his eyes.` | `Static locked camera, minimal motion.` | `type ∈ {handheld, roll, pov}` 或 `speed == fast` 或 `amplitude == large` | H3 8-step 若推幅過小幾乎全靜，可於 L4 ffmpeg 補 ≤8% 極慢數碼推 |
| **`handheld_anxiety`**<br>慌亂失控／高度緊繃 | `handheld`（可搭 `track` / `pull-out`）<br>`speed: standard/fast`<br>`amplitude: large`（慌亂）或 `small`（緊繃稍緩） | `handheld-jolt` | **large**：`Handheld camera shakes strongly as it tracks <Subject 1> moving unevenly through the frame.`<br>**small**：`Handheld camera shakes slightly, holding tense framing on <Subject 1>.` | **large**：`Raw documentary-style unsteady handheld camera with nervous breathing jitter and abrupt micro-corrections, slightly off-center framing chasing his stumble.`<br>**small**：`Tense, restrained handheld camera with subtle nervous micro-shake.` | `Shaky handheld tracking shot following sudden stumble.` | `type == static` 或 (`type ∈ {push-in, pull-out}` 且 `speed == slow` 且無手持標記) | ① **失焦再合焦**→改 ffmpeg `gblur` 0.4s 後製；<br>② **Veo 過穩**→ffmpeg 4% crop 非週期抖動補救，勿白燒點數重抽 |
| **`subjective_pov`**<br>第一人稱主觀視角 | `pov`（常配微晃或小幅 `pan`/`tilt`）<br>`speed: standard`<br>`amplitude: small/medium` | ★ `pov-handheld-scan` | `First-person POV shot; the camera shakes slightly with walking rhythm and pans [direction] with small amplitude.` | `First-person POV handheld perspective seen directly through the character's eyes, natural head-turn sway scanning the space.` | `First-person POV moving forward through the alley, natural sway.` | `angle_h != POV` 或 `face_visible == true`（照鏡除外）或 `type ∈ {arc, pedestal}` | **首幀硬約束**：Stage 3 首幀必為主觀視角（無主角正臉）；禁止單鏡內從第三人稱切入 POV |
| **`predator_stalk`**<br>逼近壓迫／獵食尾隨 | `track` / `truck` / `arc` / `push-in`<br>`speed: slow/standard`<br>`amplitude: medium/large`<br>（常配 `angle_v: low`） | `ots-push-tension`<br>`arc-reveal-90`<br>★ `stalk-track-fg` | `Tracking Shot moving steadily behind foreground edges, closing in on <Subject 1> at slow speed.` 或 `Arc Shot curving [left/right] with small amplitude at slow speed around <Subject 1>.` | `Creeping low-angle tracking camera gliding deliberately past foreground obstacles, closing the distance with oppressive weight.` | `Low-angle tracking shot gliding slowly forward past dark walls.` | `type ∈ {static, pull-out, zoom-out}` | 需精準繞過前景遮擋物揭示主體時，L1 易穿模→升格 **L3 CozyClay**（受 V11 配額限） |
| **`cold_observe`**<br>冷酷旁觀／監控疏離 | `static` / `pull-out` / `pan`<br>`speed: slow`<br>`amplitude: small`<br>（常配 `LS`/`MS`、`angle_v: high`） | `subtle-pull-reveal`<br>★ `cold-static-observe` | `Static Shot from a detached high-angle vantage, holding completely still as <Subject 1> moves below.` 或 `The camera pulls out with small amplitude at slow speed.` | `Detached, motionless observational wide frame on a locked tripod, clinical surveillance stillness.` | `Locked high-angle wide static shot, detached observation.` | `type ∈ {handheld, roll, pov}` 或 `speed == fast` | 避用裸否定詞（禁寫 `do not shake`），正向寫 `locked tripod remaining stationary` |
| **`intimate_drift`**<br>緩慢貼近／呼吸壓迫 | `push-in` / `arc`（微幅）<br>`speed: slow`<br>`amplitude: small`<br>（常配 `MCU`/`CU`） | `slow-push-verdict`<br>★ `intimate-drift-close` | `The camera pushes in with small amplitude at slow speed, drifting smoothly closer to <Subject 1>'s face with gentle handheld breathing sway.` | `Gentle floating handheld push-in creeping closer to his face, soft breathing drift as tension tightens.` | *(不建議路由 Wan；正臉改走 Flow/H3)* | `speed == fast` 或 `amplitude == large` 或 `type ∈ {roll, zoom-out, pull-out}` | H3 8-step 若壓扁漂移感，於 L4 ffmpeg 補 ≤8% 慢推＋0.5% 慢正弦呼吸漂移 |

---

### Q4 `vfx_beat` 落地路徑與分工（Flow 生成 vs ffmpeg 後製）

#### 1. 三類核心拍點實現路徑、成本與可靠性對照

| `vfx_beat` | 建議執行層（`exec_layer`） | 生成端（Flow / H3）要做什麼 | 後製端（VM CPU `ffmpeg`）要做什麼 | 邊際成本 | 單次命中率／可靠性 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`env_reaction`**<br>（燈閃、防盜器、犬吠、風物） | **`hybrid`**<br>（景物微動生成＋燈閃雙保險＋聲音全後製） | 首幀必須把觸發光源／物體擺進構圖（如巷口路燈）；`video_prompt` 寫明路燈閃爍 2 下與濕地反光微變，提供真實光影反射 | ① **音效 100% 後製疊加**：從 CC0 音庫（`03_Audio_Library/BGM_SFX/`）掛載電流滋聲、機車防盜器雙鳴、遠處犬吠，毫秒對齊幀點；<br>② **燈閃補救（省抽卡）**：若演技過關但路燈沒閃，用 `ffmpeg eq=brightness=-0.22:enable='between(t,t1,t1+0.08)+between(t,t2,t2+0.10)'` 打兩次 2–3 幀瞬態暗閃 | **0 額外 GPU / 0 Flow 點**；音庫首次蒐集 ~10 分鐘後跨集永久複用 | 生成原生準確閃兩下 ~30–50%；**加後製雙保險達 95%+** |
| **`sound_drop`**<br>（事件前 0.3s 聲場抽空） | **`post_ffmpeg`**<br>（100% 後製，**禁寫進影片 prompt**） | **不做任何事**（對白鏡原音本就捨棄；無須靠 AI 影片生靜音） | 在觸發點 `t0` 前 `0.30–0.35s` 對 Room Tone／BGM 軌下 `volume='if(between(t,t0-0.35,t0),0.03,1)'`（壓至 `-30dB` 防數位死靜爆音，前後加 20ms 極短斜坡），於 `t0` 同步觸發低頻 sub-drop / 電磁脈衝 SFX 後進對白 | **0 GPU / 0 Flow 點**；ffmpeg 處理 <2 秒 | **100% 確定性可控**，情緒張力 ROI 全場最高 |
| **`glitch_in`**<br>（系統彈窗閃入） | **`hybrid`**（首選）或 **`post_ffmpeg`**（純透明 UI 疊加） | **禁要求 AI 直接畫數位馬賽克 glitch**（極易崩臉）。採**路徑 A（首選）**：拆 `S3a`（無彈窗＋臉部突然受青藍打光）→ `S3b`（含無字幾何彈窗首幀，保真實臉部藍光反射）；或**路徑 B**：全程無彈窗生成、保留身側空位 | **路徑 A**：於 `S3a→S3b` 剪輯接點 4–6 幀（0.15–0.20s）用 `rgbashift=rh=-12:bh=12`＋水平切條錯位＋1 幀青白高光閃（`eq`）＋2 幀 AB 交錯閃現，配數位電流 SFX；<br>**路徑 B**：Pillow 產透明無亂碼 UI PNG，用 `ffmpeg overlay`＋縮放展開＋`rgbashift` 入場（需配合緩推做線性微放大防浮貼感） | **0 額外 GPU**（若採路徑 A 拆鏡多 1 支短鏡，增 1 鏡 Flow/H3 抽卡）；後製腳本 <10 秒 | 路徑 A **90%+**（兼得真實臉光與 100% 閃入感）；路徑 B **85%**（100% 守 V9 但臉部反光需模擬）；純生成硬賭 <25% |
| *（補）`light_shift` / `composite_ui`* | `hybrid` / `post_ffmpeg` | `light_shift` 需生成端算臉部光影變化（否則後製全局調色太假）；`composite_ui` 如含可讀字一律 **V9 紅線交後製** | `composite_ui` 眼部倒映類在 720p CU 不可行（見 Q5 S4），改為生成端瞳孔青色 catchlight | 同上 | 視實作路線定 |

#### 2. DEMO-02 兩個特效拍點可行性總判
- **拍點 ①（S1 路燈閃爍＋防盜器鳴）**：**完全可行**。以「首幀置入路燈＋prompt 寫閃爍＋ffmpeg 暗閃備援＋後製防盜器/犬吠 SFX」即可低成本穩定落地。
- **拍點 ②（S3 彈窗 glitch 閃入＋前 0.3s 聲場抽空）**：`sound_drop` **100% 可行**；但 **`glitch_in` 按原稿「單鏡套 DEMO-01 B 幀＋補兩幀閃爍」不可行**（會變成「原已掛著的彈窗閃一下」，非從無到有閃入），必須改走 **路徑 A（拆 S3a/S3b 跨接點 glitch）** 或 **路徑 B（無彈窗生成＋ffmpeg 透明 UI 疊加）**。

---

### Q5 DEMO-02 可行性審查（逐鏡挑毛病、翻車排行與備案）

> **跨鏡共通前置（解 DEMO-01 光線跳變病灶）**：動工四鏡前，必先以免費 `gflow` 產出 **1 張鎖定的入夜藍調窄巷空景母圖（`LOC-ALLEY-NIGHT`）**（濕地柏油反光、左側舊牆＋停放機車、遠處巷口一盞暖鈉燈路燈與店家餘光、無大字招牌），S1–S4 所有首幀一律以 **`[LOC-ALLEY-NIGHT, 人物參考圖]`**（嚴守 V3 `scene→character` 順序）跑 `gflow i2i`，才能保證四鏡在同一條巷子、同一色溫下。

#### 逐鏡體檢表

| 鏡號（原稿） | 風險等級 | 具體工程毛病（對照 `demo01/` 與 `casting/master/` 實況） | 修訂做法與備案 |
| :--- | :---: | :--- | :--- |
| **S1（5s）抵達**<br>MS，手持跟隨踉蹌入畫 | 🟡 **中** | 1. **古裝定裝 `i2i` 四重風險**：鎖定圖 `fanli-master-ancient-front.jpg` 為抱竹簡正立棚拍，直接 `i2i` 容易①拉回呆站（如 `demo01/A`）、②殘留竹簡、③深灰棚光洩漏變貼圖感、④玄黑粗麻＋黑冠融進黑巷死黑、⑤**交領右衽／左眉尾傷痕鏡像翻車（`demo01/B` 已實戰發生一次！）**。<br>2. **動作超載撞 V6**：5s 塞「撞入畫→扶牆喘息→四下張望→聽聲響→僵住」＝3 次轉折；再疊遲滯手持＋失焦合焦＋路燈閃兩下，Veo 極易糊臉或手穿牆。 | **修訂**：① 優先餵無竹簡的 `fanli-master-ancient-45.jpg`＋`LOC-ALLEY-NIGHT`；② `start_pose` 定為靜態可讀失衡姿（前傾 20° 右手扶牆、頭微偏左露左眉尾傷痕與 `y` 形右衽，巷口暖路燈勾肩冠輪廓光）；③ 動作減法為 **1 次轉折**（扶牆喘息→燈閃聲響→猛然抬頭僵住）；④ 失焦再合焦改 ffmpeg `gblur` 0.4s，燈未閃則 ffmpeg 兩幀暗閃補位。 |
| **S2（4s）目擊**<br>兩人同框 MS，婦人前景側背＋他中景 | 🟠 **中高**<br>*(翻車候選 #2)* | 1. **未定裝角色跨鏡變臉**：婦人須連戲出現在 S2、S3（邊緣）與 S4（背影），無視覺鎖定圖必每鏡換人。<br>2. **4s 雙人四動作必崩**：4 秒內要同時演「婦人入畫→愣住→後退半步→舉手機」＋「他貼牆→按左腰空處」，動作密度破表。<br>3. **前景舉手機＋菜籃高發翻車**：易現反拿手機、六指、與「提竹編菜籃」誘發古裝村婦/黑衣串染（Concept Bleeding）。 | **修訂**：① 菜籃改現代「**紅白塑膠袋／環保袋＋淺米色短外套短髮婦人**」（明暗色彩與范蠡玄黑袍拉開，防古今串染）；② 首幀讓婦人**已在前景停步舉半起手機**（省去入畫 1.5s），4s 只演「她微退舉穩手機＋他猛按左腰空處」；③ S2 核准首幀直接兼作 S3 婦人外觀參考。<br>**翻車備案**：2 抽仍崩手／串染 → **拆正反打兩鏡**（`S2a` 1.5s 婦人獨鏡停步舉手機＋`S2b` 2.5s 范蠡獨鏡警覺按左腰），零串染且更緊湊。 |
| **S3（6s）系統現身**<br>MCU 緩推，B 幀生成彈窗＋補兩幀 glitch | 🔴 **極高**<br>*(最大翻車鏡 #1)* | 1. **致命超時撞爆 V1 與 Veo 8s 上限**：實測 `demo01/audio/sys.mp3` 長 **5.41s**！加上「盯婦人（0.8s）＋抽空 glitch（0.5s）＋轉頭貼牆穩定（0.7s）＋尾拍（0.3s）」＝**淨長 ≥7.7s**，加頭尾 1.0s 裁切緩衝需 **8.7s**，直接超出 Veo 8s 硬頂與 V1（flow ≤6.5s）！<br>2. **首幀烘焙彈窗與「glitch 閃入」邏輯互斥**：實看 `demo01/B`，彈窗 `t=0` 已存在，無法演「先盯婦人→彈窗從無到有閃入→轉頭」。<br>3. **9:16 MCU 三元素擁擠崩臉**：豎屏 MCU 裡主角佔 60%＋彈窗佔 35%，塞不下邊緣「放下手機且表情困惑的婦人」（角落 80px 臉必崩且被平台 UI 遮擋）。<br>4. **V9 紅線風險**：`demo01/B` 彈窗內滿是 AI 亂碼假字。 | **首選修訂（拆鏡＋跨接點 glitch＋L-cut）**：<br>① **`S3a`（2.0s，無彈窗、無台詞）**：他盯著婦人方向 → 聲場抽空 0.3s → 右側驟亮青藍反光打臉、他微縮瞳孔起勢轉頭；<br>② **剪輯接點（ffmpeg 4–6 幀 `glitch_in`）**：`rgbashift`＋掃描線錯位＋青白閃＋電磁 SFX 硬閃切入；<br>③ **`S3b`（6.0s，含「純幾何＋頭像剪影、零文字」彈窗守 V9）**：他猛然轉頭貼牆，`sys.mp3` 起聲，**尾句 0.6–0.8s 以 L-cut 延入 S4 開頭**；<br>④ **「婦人看不見」的鉤**：不在 MCU 邊緣硬塞小臉，改在背景極遠失焦處模糊離去，或增補 1 顆 **1.5s 婦人獨鏡反打**（看他對空牆發呆、困惑放下手機快走）。<br>**4 鏡不拆備案**：改走 Q4 路徑 B（無彈窗生成 8s 採 `tail_only` 裁切＋ffmpeg 透明 UI 疊加動畫）。 |
| **S4（4s）反問**<br>CU 特寫，極緩推，眼中倒映彈窗 | 🟡 **中** | 1. **「彈窗眼中倒映」像素上不可行**：`720×1280` 的 CU 全頭特寫中，單眼虹膜直徑僅 **~18–26px**，硬塞彈窗倒影必成青白噪點或毀掉眼神與雙瞳。<br>2. **正臉特寫開口（`LIP_SENSITIVE`）時序空檔**：`fanli.mp3` 僅 **2.12s**，4.0s 鏡餘 1.88s 空檔；若未於 prompt 寫明「前 1.4s 閉唇壓息、後半才開口」，Veo 會在 `t=0` 搶先張嘴導致對嘴穿幫。<br>3. **背景冗餘風險**：CU 淺景深下硬寫「婦人模糊背影」易在主角耳側長出詭異黑影。 | **修訂**：<br>① 眼中倒映改為「**瞳孔清晰青藍反光點（cyan catchlight）＋半臉微弱青藍輝光**」（100% 可達且保眼神演技；若堅持看清倒影，須另拆 1.2s ECU 單眼特寫＋ffmpeg 疊圖）；<br>② 節奏精排：`0.0–0.7s` 承接 S3b L-cut 尾音閉唇凝視 → `0.7–1.4s` 呼吸放緩下巴微收 → `1.4–3.52s` 開口反問「……你，怎知我名？」→ `3.52–4.0s` 銳利定格；<br>③ 背景改純粹 `dark blue wet alley bokeh`，刪去婦人背影描述。 |

---

### Q6 流程銜接（階段編號、工時模型與 QC-D 落點）

#### 1. 導演闡述落點：修正 Stage 2.5 編號錯位＋補快線規則
- **編號撞車診斷**：草案寫「Stage 2（編劇）與 Stage 3（分鏡）之間插入 Stage 2.5，Gate A3 後」，此為上游 `second-civilization` 的編號體系；但本產線 **`DESIGN.md` v1.4** 的 Stage 2 是「分鏡企劃與工具路由」、Stage 3 是「首幀生成」。若把 Stage 2.5 直接搬進 `DESIGN.md`，會變成「`script_pack` 已鎖定、TTS 已配完才寫導演闡述」，徹底倒置！
- **定稿對齊**：
  - 上游 `second-civilization` 端維持稱 **Stage 2.5**（Gate A3 劇本文字定稿後、分鏡包封裝與 SHA256 鎖定前）；
  - 併入 `DESIGN.md` v1.5 時定名為 **階段 0.5（上游分鏡封板前置：導演闡述拍板，為 QC-0 入口硬門檻之一）**，絕不佔用 `DESIGN.md` 內部 Stage 2–3 編號。
- **快線（2.5–3.5h SLA）必設減壓規則**：常線跑完整導演闡述（Muse 15–25m＋Creator 5–10m）；**快線改走「3 分鐘極簡導演卡」**（4 行：情緒弧線／引用常駐工作室光線鎖 ID／運鏡基調／有無特效拍點），隨劇本一次簽核，絕不拖慢快線時效。

#### 2. 對 `DESIGN.md` §1.4 創作者人工工時模型的影響

| 環節 | DESIGN v1.4 常線 | 導入導演層後常線 | 導入導演層後快線 | 工程評估 |
| :--- | :---: | :---: | :---: | :--- |
| 既有 QC-1 / QC-1.5 / QC-2 / QC-3 | 31–50 分鐘 | 31–50 分鐘 | 20–33 分鐘 | 維持不變 |
| **新增：階段 0.5 導演闡述拍板** | — | **+5–10 分鐘**（Muse +15–25m） | **+1–2 分鐘**（極簡卡，Muse +3–5m） | 提前鎖死光線與場景邏輯，阻斷整段返工 |
| **新增：QC-D 導演閘終判** | — | **+5–8 分鐘**（Muse +10–15m） | **+2–3 分鐘**（併入粗剪快檢） | 攔截失敗品進入 Stage 6B/7 精修封裝 |
| **創作者單集總人工工時** | **31–50 分鐘** | **41–68 分鐘**（+~30%） | **23–38 分鐘**（+~15%） | 只要 3 集內少踩 1 次 DEMO-01 級整段重拍即大幅回本 |

#### 3. QC-D 放 QC-2 之前？明確反對，並提出精準落點定案
- **先釐清草案自相矛盾**：草案 §四寫「粗剪後獨立一關」、§六寫「掛在 QC-2 之後（QC-D 不過則技術 QC 不啟動）」、討論題問「放在 QC-2 之前是否同意」。根因在於把 `DESIGN.md` 的 **QC-2（Stage 5 抽卡挑片＋10 秒自動刪廢片）** 與 **QC-3（Stage 8 精剪成片技術終審）** 混為一談。
- **反對放 QC-2 之前的三條工程理由**：
  1. **QC-2 之前沒有「粗剪」**：Stage 4 產出的是 40–50 支未挑的原始散片（含黑幀、凍結、多指），無法評審跨鏡情緒曲線、節奏呼吸與光線連續。
  2. **不該擋住 `auto_tech_qc`**：Stage 5 第一段的 `auto_tech_qc` 是 0 人工、<10 秒 CPU 的自動濾壞檔工具；先刪掉壞檔再給人眼看才省工，倒過來會浪費 Muse/Creator 眼力。
  3. **真正吃工時、該被 QC-D 擋掉的是「Stage 6B 精修封裝＋Stage 7 社群包＋Stage 8 QC-3 技術終審」**（繁中字幕精校、四色事實角標、-14 LUFS 混音母帶、IG/Threads/Personal Lab 轉製）。
- **定案落點（三點嵌入，對齊 `DESIGN.md` 流水線）**：
  ```text
  Stage 3 [QC-1 首幀門]      → 提前預警 V12a 光線跳變 & V12d 景別單調（省掉 100% 抽卡浪費）
        ▼
  Stage 3.5 [QC-1.5 預演門]  → 提前確認全集節奏與鏡頭呼吸
        ▼
  Stage 5 [QC-2 挑片門]      → auto_tech_qc(10s刪壞檔) → 挑片頁並排顯示 shot_intent/beat/psychology，單鏡級初篩鎖 selected_takes
        ▼
  Stage 6A 極速粗剪          → ffmpeg <30s 自動裁頭尾0.5s拼接＋掛 TTS/關鍵SFX（另吐一版「無對白純畫面粗剪」供驗 QC-D #2）
        ▼
  ★【QC-D 導演閘】★          → Muse 6項「過/不過＋一句證據」初評 → Creator 終判；
                               任一不過 → 退回對應工位，Stage 6B / 7 / QC-3 一律不啟動（真正省工！）
        ▼（通過後）
  Stage 6B 精修封裝 → Stage 7 社群轉製 → Stage 8 [QC-3 技術與法務終審] → 手動發布
  ```

---

## 二、併入 v2.1 之欄位與規則修訂定稿建議（可直接採納）

### 2.1 `script_pack.json`（schema `2.0` → `2.1`）增量結構

```json
{
  "segments": [
    {
      "segment_id": "SEG-01",
      "scene_id": "LOC-ALLEY-NIGHT",
      "time_layer": "2022",
      "light_lock_id": "LK-ALLEY-NIGHT",
      "lighting_base": "入夜藍調，濕地反光，巷口暖鈉燈路燈＋店家餘光勾肩冠輪廓",
      "public_exposure": "semi_public",
      "anomaly_level": "overt",
      "world_reaction_default": { "types": ["ambient"], "detail": "路燈閃爍、遠處犬吠" },
      "director_arc": "驚醒失重→慌亂自保→被目擊警戒→系統錯愕→強自鎮定反問"
    }
  ],
  "shots": [
    {
      "shot_id": "S01",
      "segment_id": "SEG-01",
      "shot_intent": "讓觀眾跟他一起失重——這不是觀光，是墜落",
      "performance_beat": {
        "from": "失衡扶牆喘息",
        "trigger": "巷口路燈閃爍兩下與機車防盜器短鳴",
        "to": "猛然抬頭僵住細聽警戒",
        "deliberate_hold": false
      },
      "world_reaction": {
        "types": ["ambient"],
        "detail": "路燈閃爍兩下、防盜器短鳴、遠處犬吠",
        "exempt_reason": null
      },
      "camera_psychology": "handheld_anxiety",
      "movement": {
        "type": "handheld",
        "speed": "standard",
        "amplitude": "large",
        "named_shot": "handheld-jolt"
      },
      "vfx_beats": [
        {
          "type": "env_reaction",
          "exec_layer": "hybrid",
          "note": "路燈閃爍兩下（生成為主、ffmpeg暗閃備援）＋後製防盜器短鳴SFX"
        }
      ]
    }
  ]
}
```

### 2.2 導演手記（`bible/director/playbook.md`）工程補充
- 同意建立 `bible/director/playbook.md` 累積制，並建議每條目補一個 **`enforce_layer`** 欄（`upstream_prompt`／`validator_rule`／`qc_d_checklist`／`post_ffmpeg`），避免手記越積越長最後淪為沒人讀的備忘錄——凡可下沉為 `V12` 規則或 `named_shots.yaml` 避坑項者，每 5 集收斂一次進規格，手記本體控制在 30 條以內高訊噪比。

---

## 三、待 Creator 拍板的三道收斂點（供併入 v2.1 前一次確認）

1. **DEMO-02 鏡數微調**：是否同意將 S3 拆為 **`S3a`（2s 無彈窗受青光）＋ `S3b`（6s 彈窗閃入＋`sys.mp3` 尾句 L-cut 進 S4）**（總片 5 鏡，或在 S3b 中段再補 1.5s 婦人看不見彈窗之反打鏡為 6 鏡），以根治 `sys.mp3` 5.41s 超時與首幀烘焙彈窗的矛盾？
2. **S4 眼中倒映降載方案**：是否同意改為 **CU 瞳孔清晰青藍反光點＋半臉微光**（保眼神與口型），而非在 720p CU 20px 虹膜內硬塞彈窗圖案？
3. **V12a 與 QC-D 定案**：是否同意 ① `light_lock_id` 上移 `segments[]` 且成片 V12a 採「半自動標記＋人工終判」；② QC-D 設於 **Stage 6A 極速粗剪之後、Stage 6B 精修封裝／QC-3 技術終審之前**（快線走 3 分鐘極簡導演卡）？
