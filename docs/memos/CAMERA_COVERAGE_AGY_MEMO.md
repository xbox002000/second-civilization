# 導演鏡頭覆蓋與豎屏短劇節奏工作流修訂案（`CAMERA_COVERAGE_AGY_MEMO.md`）

> **文件性質**：DISCUSSION & DESIGN ONLY（2026-11-28｜**零圖片／影片生成、零 API／CU 消耗、零 repo push**）  
> **撰寫角色**：agy（`workhorse-90d`，《第二次文明》短劇產線工程端）  
> **定位區隔**：本文件專攻 **「導演級景別覆蓋（Shot-Size Coverage）、鏡數密度、單鏡秒數控制與豎屏短劇高張力快節奏」**（目標併入 `STORYBOARD-SPEC-V2.md` v2.3 → **v2.4 附錄 D**），**非**舊版 2026-11-27 運鏡執行四級分層備忘錄（`CAMERA_WORKFLOW_AGY_MEMO.md`，已併入附錄 A）。  
> **平行議題交叉參照**：抵達因果重構（`S0` 太湖前態／前衝撞牆向量）、目擊婦人有聲化與 `SYS-01` 真人虛擬投影方案（AMD-05 v2）已於平行文件 [`DEMO03_TREATMENT.md`](file:///home/hatch/drama-line/DEMO03_TREATMENT.md) 討論，本文不重複其敘事處方，僅標示「鏡頭覆蓋 × 因果呈現」之介面耦合點。  
> **依據準據**：`STORYBOARD-SPEC-V2.md`（v2.3 FINAL）、`CINEMATIC-PROMPT-CRAFT-REF.md`、`H3-CAMERA-CONTROL-REF.md`、`DEMO02-DIRECTOR-STATEMENT.md`、`demo02_v2/FULL_RUN_REPORT.md`、`EP01_PRODUCTION_WORKFLOW.md`、`HIT_STRUCTURE.md`、`DIRECTOR_LAYER_AGY_MEMO.md`、`tools/preflight_gate.py`。

---

## 0. 問題診斷：為何 `DEMO02_v2` 技術閘門全綠，卻在「導演鏡頭語言與短劇張力」上失格？

`demo02_v2/DEMO02_v2.mp4`（`23.79 s`，6 鏡）以 **0 FAIL / 0 WARN / 0 Waiver** 通過 QC-0、QC-1、QC-2 並修復了全部 6 類技術病灶，卻被 Creator 指出「缺特寫、景別單調、節奏偏慢、不像豎屏短劇」。將 `demo02_v2/plan/script_pack.json` 與 `FULL_RUN_REPORT.md` 量化拆解後，病灶一目了然：

| 指標 | `DEMO02_v2` 實測（6 鏡 / `23.79 s`） | 豎屏高張力短劇目標帶 | 失格診斷 |
| :--- | :---: | :---: | :--- |
| **平均鏡長（ASL）** | **`3.97 s`** | **`1.8–2.6 s`**（開場／衝突段） | 過緩；落入傳統長鏡頭／預告片均勻節拍 |
| **每 10 秒鏡數** | **`2.52 鏡 / 10s`** | **`3.8–5.5 鏡 / 10s`** | 密度不足；資訊與情緒切換頻率太低 |
| **前段同尺幅停滯** | `S1(MS 4.0s) → S2(2S 4.0s) → S3a(MS 3.42s)` | 連同尺幅 **`≤ 2 鏡`** | 前 **11.42 s（48% 片長）** 全停在中景尺幅（`SHOT_SIZE_RANK == 3`） |
| **首顆特寫（CU/ECU）出現時間** | **`t = 19.12 s`**（`S4`） | **`≤ 3–8 s`**（首 10 秒必有 CU/ECU） | **80.4% 片長過去才見到第一顆特寫**；手機 6 吋螢幕細節全失 |
| **細節插鏡（ECU / INSERT）** | **`0 鏡`** | **每 10–12 s 至少 1 鏡** | 零手部／眼神／物證切點；失去豎屏強注意力重設工具 |
| **最長靜止空轉（Dead Air）** | `S3b` **`5.08 s`** `static` `MCU` | **`≤ 2.5–3.5 s`** 無視覺事件 | 為防 `push-in` 撞入 `SYS-01` 區而改 `static`，整段 5 秒無切反應或細節 |
| **景別分布** | `MS/2S × 3`、`MCU × 2`、`CU × 1`、`WS/MLS/ECU = 0` | 每段 ≥ 3 有效景別＋含 CU/ECU | 視覺重心嚴重鎖死在中景帶 |

**為何現行 Spec v2.3 與 `preflight_gate.py` 放行了這份覆蓋？三個結構漏洞：**
1. **Stage 0.5 導演闡述是散文而非數據契約**：`DEMO02-DIRECTOR-STATEMENT.md` 寫「`MS→雙人 MS→MCU→CU，四鏡四樣`」，沒有逐鏡覆蓋表、沒有秒數配額、也沒有轉成 `script_pack.json` 可驗證欄位（違背 AMD-07「數據優先」精神）。
2. **`shot_size` 枚舉混雜「景別距離」與「構圖角色」**：Spec v2.3 §3.B 把 `2S`、`OTS`、`INSERT` 和 `LS/MS/MCU/CU/ECU` 塞進同一欄，導致 `MS → 2S → MS` 在字面上看似「有變化」，實質全是中景；且 `V12d` 只抓「連 3 鏡 `(size, angle_v, angle_h)` 全同」，極易被繞過。
3. **`V1` 只卡上限、反而懲罰短鏡**：`preflight_gate.py` §1420 對所有生成長 `< 3.0s` 的非 `INSERT`/非 `reverse` 鏡發 `WARN`，無意中把撰寫者推向「每鏡都寫 4–5 秒」的平緩節拍。

**核心工程結論**：鏡頭覆蓋與短劇張力不能靠 Stage 4 抽卡祈禱，也不能等到 QC-D 才重拍。必須在 **Stage 0.5（導演闡述覆蓋表）→ Stage 1（`script_pack.json` Schema 2.4 數據化）→ QC-0（`preflight_gate.py` 硬閘）** 三層鎖死，並在 **不爆預算** 的前提下，以「低成本非口型插鏡／反應鏡／圖卡」買出豎屏高密度節奏。

---

## 1. 覆蓋表 Schema 設計（Stage 0.5 → `script_pack.json` Schema 2.4）

遵循 Spec v2.3「**共用上移**」與 AMD-07「**覆蓋是資料，不是散文**」原則，Stage 0.5 導演闡述新增標準化 **逐鏡覆蓋表（Coverage Table）**，其每一欄精確映射至 `script_pack.json`（schema `2.4`，向下相容 `2.0–2.3`）。

### 1.1 解耦 `shot_size` 距離尺度與構圖旗標（根治 v2.3 欄位混載）

現行 v2.3 將距離（`MS`/`CU`）與構圖關係（`2S`/`OTS`/`INSERT`）混在同一枚舉，無法精準計算景別跨度與反打結構。Schema 2.4 將其拆分為**純距離枚舉 `shot_size`** ＋ **構圖旗標物件 `framing_flags`**：

1. **`shot_size`（必填 ●，純景別距離枚舉，6 級視覺尺幅＋`CARD`）**：

| 枚舉值 | 尺度秩（`SCALE_RANK`） | 9:16 豎屏構圖定義 | 向下相容別名（自動正規化） |
| :---: | :---: | :--- | :--- |
| **`WS`** | `1` | 遠景／定場全景（環境占 ≥65%，人物全身含周圍空間；建立因果與地理） | `ELS`、`LS` → `WS` |
| **`MLS`** | `2` | 中全景／牛仔景（膝上至全身略裁；9:16 最適合交代踉蹌走位、腰間佩劍位與空間距離） | — |
| **`MS`** | `3` | 中景（腰上；雙人對峙、肢體互動與手勢主戰場） | `2S` → `MS` + `is_two_shot=true` |
| **`MCU`** | `4` | 中近景（胸上；對白、壓迫推進、過肩反打主力） | `OTS` → `MCU` + `is_ots=true` |
| **`CU`** | `5` | 特寫（頭肩／全臉或緊密主體；微表情、情緒峰值、關鍵台詞必用） | — |
| **`ECU`** | `6` | 極近特寫（眼部、手部動作、方孔錢、空腰間、手機鏡頭、劍柄；模式中斷與細節衝擊） | `INSERT` → `ECU` + `is_insert=true` |
| **`CARD`** | `0` *(免計尺幅)* | `gen_mode == "cpu_card"` 專屬（新聞證據卡、時間線字卡、片尾聲明卡） | — |

2. **`framing_flags`（v2.4 新增，於 `shots[]`；未填時全預設 `false`）**：
   - `is_ots: bool` — 含前景過肩遮擋元素（Over-The-Shoulder）。
   - `is_reverse: bool` — 承接前鏡 180° 軸線之反打鏡（Reverse Angle）。
   - `is_two_shot: bool` — 雙人同框（含實拍雙人或 AMD-05 v2 虛擬真人投影並肩同框；觸發 `TWO_SHOT_MICRO_MOTION`）。
   - `is_insert: bool` — 細節插鏡／切出（手、眼、道具、環境物證；不推主線空間走位，專司節奏打斷與資訊放大）。

> **相容性設計**：舊版 schema 2.0–2.3 的 `shot_size: "2S" / "OTS" / "INSERT" / "LS" / "ELS"` 由 `preflight_gate.py` 載入時自動正規化映射至上表，零破壞既有封包。

### 1.2 `movement.motivation` 動機詞表（與 `camera_psychology` 強耦合）

在附錄 A.2 既有 `movement` 物件（`{type, direction?, speed, amplitude?, end_shot_size?, easing?, named_shot?}`）新增 **`motivation`（v2.4 必填 ●，非 `CARD` 鏡）**，以 6 枚舉杜絕「為了動而動」或「無理由全靜」：

| `movement.motivation` | 導演語意 | 合法配對之 `camera_psychology` | 典型 `movement.type` 與 `named_shot` | 衝突組合（觸發 `COVERAGE_MOVE_MOTIVATION` WARN） |
| :--- | :--- | :--- | :--- | :--- |
| **`emotional_intensify`** | 情緒加壓、貼近內心轉折或心理逼問 | `intimate_drift`、`stable_control`、`predator_stalk` | `push-in`（慢/中）、微 `arc`；`slow-push-verdict`、`intimate-drift-close`、`push-escalation-mcu` | 配 `pull-out` / `zoom-out` 或 `cold_observe` |
| **`spatial_reveal`** | 揭露環境因果、目擊者、新威脅或空間孤立感 | `cold_observe`、`predator_stalk`、`handheld_anxiety` | `pull-out`、`pan`、`tilt`、`arc`、`truck`；`subtle-pull-reveal`、`arc-reveal-90` | 配 `ECU` 緊密靜鏡且無位移揭露 |
| **`subjective_instability`** | 失重墜落、恐慌警戒、主觀呼吸晃動 | `handheld_anxiety`、`subjective_pov` | `handheld`、`pov`、`roll`；`handheld-jolt`、`pov-handheld-scan` | 配 `stable_control` / `cold_observe` 或 `static` |
| **`action_follow`** | 跟隨身體位移、視線轉向或道具遞交動量 | `handheld_anxiety`、`predator_stalk`、`subjective_pov` | `track`、`truck`、`pan`、`tilt`、`handheld`；`stalk-track-fg` | 配 `static` 且 `action` 含大幅位移 |
| **`power_lock`** | 刻意定鏡或微推進建立冷靜掌控、威壓或冰冷凝視 | `stable_control`、`cold_observe` | `static`、極慢小幅 `push-in`；`steady-dialogue-lock`、`low-angle-authority`、`cold-static-observe` | 配 `handheld_anxiety` 或 `amplitude: large` |
| **`rhythm_jolt`** | 拍點反轉衝擊、模式中斷、視聽急煞 | `handheld_anxiety`、`predator_stalk`、`intimate_drift` | 快速小幅 `push-in`、`zoom-in`、L4 `crash-zoom-post`／`whip-cut-anchor` | 配 `release_bridge` 段且無 `JOLT`/`TURN`/`CLIFF` 拍點 |

### 1.3 `named_shots.yaml` 增補建議（配合覆蓋規格，誠實標註狀態）

實查 `~/drama-line/bible/camera/named_shots.yaml` 尚未建檔（Spec §0 標註「規劃／受控」）。在原有附錄 A.7 的 10 個鏡型＋`DIRECTOR_LAYER_AGY_MEMO.md` Q3 增補的 4 個鏡型外，建議建檔時一併納入 **4 個豎屏短劇覆蓋高頻鏡型**（全部初標 `verified_9x16_status: UNTESTED`，隨實跑回填）：
- `ecu-detail-insert`（`ECU`, `is_insert=true`, `1.0–1.8s`, Flow/Wan，微推或微手持，專供手／眼／道具中斷切鏡）
- `ots-reverse-cu`（`CU`/`MCU`, `is_ots=true, is_reverse=true`, `1.5–2.8s`, Flow/H3，雙人對白過肩反打）
- `push-escalation-mcu`（`MCU → CU`, `Δrank=1`, `2.2–3.5s`, Flow/H3/L4，高張力跨一級尺幅慢推，100% 合規 `SCALE_JUMP_BAN`）
- `whip-cut-anchor`（`MS`/`MCU`, L4 post-ffmpeg 3–4 幀動態模糊接點轉場，專供高張力跳切而不消耗 AI 抽卡賭甩鏡）

### 1.4 覆蓋表欄位總覽與 `script_pack.json`（Schema 2.4）精確映射

#### A. 場段層新增欄位（`segments[]`）
| 欄位 | 必填 | 值域與規則 | 用途 |
| :--- | :---: | :--- | :--- |
| **`segment_pacing_profile`** | ● *(2.4)* | `hook` \| `escalation` \| `confrontation` \| `revelation` \| `climax` \| `release_bridge` \| `chase_tension` | 決定該場段的目標 ASL、每 10 秒鏡數帶、非對白上限與 Dead-Air 門檻 |
| **`axis_plan`** | ◐ *(≥2 人物鏡必填)* | `{"<CHAR_ID>": {"screen_side": "left\|center\|right", "default_facing": "left\|right\|front\|back"}}` | 鎖定場段 180° 軸線與正反打視線基準（防 `DEMO02_v2` `S2→S3a` 視線跳向） |
| **`target_shot_density_per_10s`** | ○ | `[min, max]` 數值對；未填則依 `segment_pacing_profile` 查預設表 | 允許導演明示覆寫段級節奏帶（須記於導演闡述） |

#### B. 原子鏡層新增／對齊欄位（`shots[]`）
| Stage 0.5 覆蓋表欄位 | `script_pack.json` 落點 | 型別／枚舉 | 必填 | 說明 |
| :--- | :--- | :--- | :---: | :--- |
| `Shot` | `shots[].shot_id` | `S##` / `S##a` | ● | 既有欄位 |
| `Size` | `shots[].shot_size` | `WS\|MLS\|MS\|MCU\|CU\|ECU\|CARD` | ● | 純距離尺幅（向下相容舊枚舉） |
| `Flags` | `shots[].framing_flags` | `{is_ots, is_reverse, is_two_shot, is_insert}` | ○ *(默認全 false)* | 構圖關係旗標 |
| `Named Shot` | `shots[].movement.named_shot` | `named_shots.yaml` ID | ◐ *(非 CARD 建議必填)* | 受控鏡型 ID |
| `Sec` | `shots[].target_net_sec` | `float`（淨秒數） | ● | 既有欄位；`gen_sec = target_net_sec + trim_buf` |
| `Move + End` | `shots[].movement.{type,speed,amplitude,end_shot_size}` | 附錄 A.2 結構 | ● | `end_shot_size` 用於 R3 與 `SCALE_JUMP_BAN` 聯檢 |
| `Motivation` | `shots[].movement.motivation` | 6 枚舉（§1.2） | ● *(非 CARD)* | 運鏡心理動機（連 `camera_psychology`） |
| `Psych` | `shots[].camera_psychology` | 6 枚舉（附錄 B.4） | ◐ *(非 CARD)* | 既有欄位 |
| `Beat / Role` | `shots[].beat_function` ＋ **`coverage_role`** ＋ **`emotional_peak`** | `coverage_role`: `establish\|action\|speaker\|reaction\|insert_detail\|turn_jolt\|peak_hold\|card_evidence`；`emotional_peak: bool` | ● *(2.4)* | 精準區分「說話鏡 vs 反應鏡 vs 細節插鏡 vs 情緒峰值鏡」 |
| `Axis / Facing` | `shots[].subject_facing` ＋ **`screen_side`** ＋ **`axis_turn_trigger?`** | `left\|right\|front\|back`；`left\|center\|right`；`string?` | ◐ *(人物鏡)* | 執行 180° 軸線與視線連貫檢核 |
| `Dial / Lip` | `shots[].dialogue[]` ＋ **`dialogue_mode`** ＋ `lip_sensitive` | `dialogue_mode`: `none\|on_camera\|off_camera\|voiceover\|l_cut_carry` | ● | 明確區分「無對白」「正面開口」「畫外／L-cut 延音」（決定 R3／R4／路由成本） |
| `Event / Hold` | **`shots[].internal_event_sec?`** ＋ **`hold_justification?`** | `float[]`；`dread\|peak_emotion\|held_reaction` | ◐ *(長鏡必填)* | 支撐 No-Dead-Air 與長停頓豁免之機器驗證 |

#### C. Stage 0.5 覆蓋表 Markdown 範本與 `script_pack.json` 映射實例（零散文重複）

Stage 0.5 `DIRECTOR_STATEMENT.md` 必附以下精簡表（即使 Demo / 快線 T2 跳過長散文，**此表與 `axis_plan` 永不可跳**，寫完約 2–3 分鐘）：

```markdown
### SEG-01 Coverage Table（profile: `hook`｜axis: `FANLI=left→right, WITNESS=right→left, SYS-01=right→left`）
| Shot | Size | Flags | Named Shot | Net(s) | Move (spd/amp→end) | Motivation | Psych | Beat / Role / Peak | Dial / Lip | Event(s) / Note |
|---|---|---|---|---:|---|---|---|---|---|---|
| S1a | MLS | — | handheld-jolt | 1.8 | handheld (fast/lg) | subjective_instability | handheld_anxiety | HOOK / establish | none / F | t=0.2 lamp flicker |
| S1b | ECU | insert | ecu-detail-insert | 1.2 | handheld (std/med) | rhythm_jolt | handheld_anxiety | JOLT / insert_detail | none / F | palm slams wet wall |
```

Stage 1 轉譯進 `script_pack.json`（Schema 2.4 片段）：
```json
{
  "schema_version": "2.4",
  "segments": [
    {
      "segment_id": "SEG-01",
      "segment_pacing_profile": "hook",
      "axis_plan": {
        "FANLI":   { "screen_side": "left",  "default_facing": "right" },
        "WITNESS": { "screen_side": "right", "default_facing": "left"  },
        "SYS-01":  { "screen_side": "right", "default_facing": "left"  }
      }
    }
  ],
  "shots": [
    {
      "shot_id": "S1b",
      "segment_id": "SEG-01",
      "shot_size": "ECU",
      "framing_flags": { "is_ots": false, "is_reverse": false, "is_two_shot": false, "is_insert": true },
      "target_net_sec": 1.2,
      "trim_policy": "tail_only",
      "coverage_role": "insert_detail",
      "emotional_peak": false,
      "beat_function": "JOLT",
      "dialogue_mode": "none",
      "lip_sensitive": false,
      "face_visible": false,
      "camera_psychology": "handheld_anxiety",
      "movement": {
        "type": "handheld",
        "speed": "standard",
        "amplitude": "medium",
        "named_shot": "ecu-detail-insert",
        "motivation": "rhythm_jolt"
      }
    }
  ]
}
```

---

## 2. 鏡頭覆蓋規則體系（R1–R5 強化版 ＋ 導演級增補 R6–R9）

每條規則明確標註為 **HARD（`preflight_gate.py` 由 `script_pack.json` 全自動硬閘，退碼非零）** 或 **ADVISORY（`preflight` `WARN` 及／或 QC-D 人工把關）**，並處理極短場段、圖卡與 `SCALE_JUMP_BAN` 邊界條件。

### 2.1 Muse 草案五條（R1–R5）之工程強化與分類

| 規則 | Muse 草案 | 短劇實戰與工程修訂定稿 | 強制力 | 驗證方法與豁免邊界 |
| :--- | :--- | :--- | :---: | :--- |
| **R1a**<br>段內景別多元 | 每段 ≥ 3 景別 | 非微場段（非卡總長 `≥ 8.0s` 或非卡鏡數 `≥ 4`）內須具 **≥ 3 個相異正規化 `shot_size`**（計於 6 級純距離尺幅，**不被 `MS`+`2S` 混充騙過**），且 **至少含 1 顆 `CU` 或 `ECU`**。 | **HARD**<br>*(3 鏡/6–8s 段發 WARN；≤2 鏡/<6s 微場段豁免)* | `preflight_gate.py`：`COVERAGE_SCALE_VARIETY`。避免誤殺 1–2 鏡冷開場（如 EP-01 `SEG-01`）。 |
| **R1b**<br>情緒峰值特寫 | 情緒峰值鏡必為 CU/ECU | 任一 `emotional_peak == true` 之鏡，其 `shot_size` 必為 `CU`/`ECU`，**或**起始為 `MCU` 且 `movement.end_shot_size == "CU"`（Δrank=1）。每個非 `release_bridge`、總長 `≥ 8.0s` 場段必標記 **≥ 1 顆 `emotional_peak: true`**。 | **HARD** | `preflight_gate.py`：`COVERAGE_PEAK_CLOSEUP`。把「峰值放哪一鏡」從口頭討論變成結構契約。 |
| **R1c**<br>禁同尺幅停滯 *(升級 V12d)* | *(增補)* | 同段非卡鏡頭不可連續 **`> 2` 鏡**落於相同 `SCALE_RANK`（除非 `is_reverse == true` 屬正反打對切）；即便正反打對切，連 4 鏡同尺幅發 `WARN`、連 5 鏡發 `FAIL`（除非填 `monotony_exempt_reason`）。 | **HARD** | `preflight_gate.py`：`COVERAGE_SCALE_STAGNATION`。直接封殺 `DEMO02_v2` 的 `S1(MS)→S2(2S)→S3a(MS)`。 |
| **R2**<br>細節切鏡節奏 | 每 10 秒 ≥ 1 顆 CU/ECU 細節切鏡（眼／手／道具） | **雙層檢核**：① 段內任一連續 **`≥ 10.0s`** 非卡滑動視窗內，至少含 **1 顆 `CU` 或 `ECU`**（防長段無近景）；② 段長 **`≥ 12.0s`** 者，平均每 **`12.0s`** 至少含 **1 顆非對白細節／反應特寫**（`shot_size ∈ {CU, ECU}` 且 `is_insert == true` 或 `coverage_role ∈ {insert_detail, reaction}`）。 | **HARD** *(hook/escalation/confrontation/climax)*<br>**WARN** *(revelation/release_bridge)* | `preflight_gate.py`：`COVERAGE_DETAIL_CADENCE`。區分「純說話大頭 CU」與「手／眼／物證／反應切鏡」，防止對白大頭撐滿 10 秒就過關。 |
| **R3**<br>非對白鏡長上限與跨級規則 | 非對白鏡 `≤ 4s`，除非鏡內跨景別（`MS→CU` 算） | **關鍵安全修訂（避撞 `SCALE_JUMP_BAN`！）**：<br>• 無對白非卡鏡（`dialogue_mode == "none"`）上限：`hook`/`escalation`/`climax`/`chase_tension` 場段 **`≤ 3.5s`**；其餘場段 **`≤ 4.0s`**。<br>• **有條件展延至 `≤ 5.0s`** 僅限二擇一：① 鏡內跨 **恰好 1 級相鄰尺幅**（`｜rank(end) − rank(start)｜ == 1`，如 `WS→MLS`、`MLS→MS`、`MS→MCU`、`MCU→CU`）——**明文駁回草案 `MS→CU`（Δrank=2），因 `i2v_first` 跨兩級推臉必觸發變臉與 `SCALE_JUMP_BAN`！** ② `deliberate_hold == true` 且具非空 `hold_justification`（`dread`／`peak_emotion`／`held_reaction`），上限 `4.5s`（仍須滿足 §2b No-Dead-Air）。 | **HARD** | `preflight_gate.py`：`COVERAGE_NON_DIALOGUE_CAP` ＋ `SCALE_JUMP_BAN` 聯檢。 |
| **R4**<br>雙人對白反打 | 雙人對白必含 OTS 或反打 CU | 任一場段含 **≥ 2 名發聲角色**（含 `FANLI + SYS-01`、`FANLI + WITNESS`）且總對白輪次 `≥ 2` 時，段內必須同時滿足：① 含至少 1 顆 `is_ots == true` **或** `is_reverse == true`；② 含至少 1 顆單人 `CU`/`MCU`（`is_two_shot == false`）；③ 不可連續 `> 1` 顆有對白之 `is_two_shot == true` 鏡頭。 | **HARD** | `preflight_gate.py`：`COVERAGE_TWO_PERSON_DIALOGUE`。強迫放棄「雙人中景互講」的 9:16 災難構圖。 |
| **R5**<br>有動機運鏡與動靜地板 | 每段 ≥ 1 有動機運鏡；禁全靜止場段 | ① **R5a（動能地板）**：`≥ 3` 顆非卡鏡之場段，嚴禁 100% 為 `movement.type == "static"`（至少 1 鏡具主動運鏡或明示 L4 後製運鏡）；在 `hook`/`escalation`/`climax` 段，主動運鏡佔比 `< 50%` 發 `WARN`。② **R5b（動機強制）**：每顆非卡鏡必填 `movement.motivation`，且 `(camera_psychology, movement.type, movement.motivation)` 須通過相容矩陣。 | **R5a: HARD**（0% 靜止） / **WARN**（<50%）<br>**R5b: HARD**（缺失） / **WARN**（矩陣衝突） | `preflight_gate.py`：`COVERAGE_SEGMENT_KINETIC` ＋ `COVERAGE_MOVE_MOTIVATION`（擴充 V12e）＋ QC-D 驗實片動態強度。 |

### 2.2 導演層增補四條（R6–R9：真正讓覆蓋像導演語言的關鍵）

| 規則 | 規則內容 | 強制力 | 驗證方法 |
| :--- | :--- | :---: | :--- |
| **R6**<br>五類節拍景別弧線（Shot-Size Arc Patterns） | 覆蓋表不是隨機湊滿 3 種景別，須按場段功能選用對應景別弧線：<br>1. **抵達／失重（Arrival）**：`WS/MLS（空間因果）→ ECU（物理觸點）→ MCU（驚覺）→ MS 2S（外來威脅）→ OTS/CU（壓迫收束）`<br>2. **對峙對白（Confrontation）**：`MS/2S 定場（≤2.5s）→ OTS MCU → 反打 CU → ECU（手／眼細節中斷）→ 更緊 CU 判詞`<br>3. **揭露／翻盤（Revelation）**：`MCU 鋪陳 → ECU／CARD 物證插鏡（1.5–2.5s）→ CU 靜默反應 → 慢推 CU 結論`<br>4. **情緒收束／懸念鉤（Emotional Close / Cliff）**：漏斗收斂弧 `MS → MCU → 慢推 CU → ECU 眼神／異常閃拍（1.0–1.8s）→ 硬切黑`<br>5. **追逐／極高張力（Chase / Tension）**：碎片化動能 `MLS 跟拍 → 連切 ECU（1.0–1.5s）→ 手持 MS → L4 甩切／急推 → CU 急喘` | **ADVISORY** *(QC-D 主檢)* | Stage 0.5 覆蓋表設計模板 ＋ **QC-D #3a** 人工審核弧線是否服務情緒推進。 |
| **R7**<br>單集節奏曲線與反節拍器原則（Episode Rhythm Curve） | 對齊 `HIT_STRUCTURE.md` §3.1 60–100 秒五段公式：<br>• **① 開場鉤（0–5s）**：全集 **最密或次密**（`4.5–6.5 鏡/10s`，ASL `1.5–2.2s`），首 `1.5s` 必有視覺變故。<br>• **② 加壓（5–25s）**：明快建立利害（`3.5–4.5 鏡/10s`，ASL `2.2–2.8s`）。<br>• **③ 第一次翻轉（25–45s）**：物證／圖卡／ECU 切點打斷（`3.0–4.0 鏡/10s`，ASL `2.5–3.3s`）。<br>• **④ 升溫與高潮（45–80s）**：加速衝高（`4.0–5.5 鏡/10s`），並於最高張力點安插 **1 顆「對比長停頓」**（`3.5–4.8s` 慢推 `CU`）形成重錘反差。<br>• **⑤ 集尾鉤（末 5–12s）**：急煞收口（`4.5–6.0 鏡/10s`，1–2s 異變特寫後硬切黑）。<br>• **反節拍器（Anti-Metronome）**：全集鏡長變異係數 `CV = stdev(target_net_sec) / mean(target_net_sec) ≥ 0.25`（禁止 4s-4s-4s-4s 機械等長）。 | **ADVISORY** *(Preflight WARN + QC-D)* | `preflight_gate.py`：`COVERAGE_PACE_ENVELOPE`（印出各段 ASL、每 10s 鏡數與全集 CV，超帶或 `CV < 0.25` 發 `WARN`）。 |
| **R8**<br>ECU 配給紀律（ECU Rationing） | 過多 `ECU` 會摧毀空間感、稀釋衝擊力並推高 AI 手眼偽影率：<br>• 單段（`≥ 4` 非卡鏡）`ECU` 佔比：**`> 30%` 鏡數** 或 **`> 20%` 段總時長** 發 `WARN`；**`> 40%` 鏡數** 發 **`FAIL`**。<br>• 連續 `ECU` 上限：**`≤ 2` 鏡**（`chase_tension` 放寬至 `≤ 3`），超標 **`FAIL`**。<br>• **臉部／眼部 ECU** 建議保留給 `TURN / JOLT / CLIFF / emotional_peak`（用於 `SETUP`/`BRIDGE` 發 `WARN`）。 | **HARD**（>40% 或連切 >2）<br>**WARN**（>30% 鏡數／>20% 時長） | `preflight_gate.py`：`COVERAGE_ECU_RATIONING`。 |
| **R9**<br>180° 軸線與視線紀律（Axis & Eyeline） | 杜絕 `DEMO02_v2` `Cut 2 (S2 END → S3a START)` 視線無故反轉：<br>• 同段 `≥ 2` 人物鏡必填 `segments[].axis_plan` 與鏡級 `subject_facing`、`screen_side`。<br>• **硬檢核**：`is_reverse == true` 回答前鏡對看角色時，雙方 `subject_facing` 必須相向（`left` 對 `right`）；若同向（皆 `left` 或皆 `right`）直接 **`FAIL`**。<br>• **軟檢核**：同一角色在同段相鄰兩鏡間 `subject_facing` 左右翻轉（`left ↔ right`）且未填 `axis_turn_trigger` 或 `continuity_override` → 發 **`WARN`**。 | **HARD**（反打同向）<br>**WARN**（同人未觸發翻向）<br>＋ **QC-D #3d** 實片驗 | `preflight_gate.py`：`COVERAGE_AXIS_DISCIPLINE` ＋ QC-1/QC-D 視線接點對照。 |

### 2.3 量化參數參考表（場段節奏帶 × 景別時長指南）

#### 表 A：各場段類型目標密度與 ASL（`segment_pacing_profile`）
| `segment_pacing_profile` | 目標 ASL（淨秒） | 每 10 秒鏡數目標帶 | 非對白單鏡硬上限（R3） | Dead-Air 軟／硬上限（§2b） | 備註 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`hook`**（0–5s 開場鉤） | **`1.5 – 2.2 s`** | **`4.5 – 6.5`** | `3.5 s` | `2.0 s` / `2.5 s` | 首 1.5s 必有視覺變故；禁慢起手空景 |
| **`chase_tension`**（動作／極高危） | **`1.4 – 2.2 s`** | **`4.5 – 7.0`** | `3.0 s` | `1.8 s` / `2.5 s` | 允許連 3 鏡 ECU 碎片；多用 Wan＋L4 |
| **`climax`**（高潮／集尾對決） | **`1.8 – 2.6 s`** | **`3.8 – 5.5`** | `3.5 s` | `2.0 s` / `2.5 s` | 允許 1 顆 `3.5–4.8s` 對比峰值 CU 停頓 |
| **`escalation`**（加壓／衝突升溫） | **`2.0 – 2.8 s`** | **`3.5 – 5.0`** | `3.5 s` | `2.5 s` / `3.5 s` | 每 10–12s 必插細節／反應切鏡 |
| **`confrontation`**（雙人交鋒對白） | **`2.2 – 3.0 s`** | **`3.3 – 4.5`** | `4.0 s` | `2.5 s` / `3.5 s` | 靠 OTS＋聽者反應＋L-cut 拉動速度，不靠硬壓語速 |
| **`revelation`**（物證揭露／回顧） | **`2.4 – 3.2 s`** | **`3.1 – 4.2`** | `4.0 s` | `3.0 s` / `4.0 s` | 穿插 `CARD`／`ECU` 證據卡維持節奏 |
| **`release_bridge`**（短暫呼吸／轉場） | **`2.8 – 3.8 s`** | **`2.6 – 3.5`** | `4.0 s` | `3.5 s` / `4.5 s` | 單集累計呼吸段不超過 10s |

#### 表 B：各景別單鏡淨時長指南（對齊 V1／V2 與豎屏閱讀速度）
| `shot_size` | 典型用途 | 建議淨時長 | 絕對下限／上限（淨秒） | 備註 |
| :--- | :--- | :---: | :---: | :--- |
| **`ECU`** | 眼、手、道具、物證中斷切鏡 | **`1.0 – 2.0 s`** | `0.8 s` / `2.5 s` | 超過 2.5s 易失空間感且放大 AI 偽影 |
| **`CU`**（無對白反應） | 驚愕、壓抑、微表情定格 | **`1.2 – 2.5 s`** | `1.0 s` / `3.5 s` *(對比停頓 ≤4.5s)* | 適合 `lip_sensitive=false` 閉唇反應鏡 |
| **`CU`**（對白／峰值） | 核心台詞、質問、判詞 | **`2.5 – 4.8 s`** | `1.8 s` / `5.5 s` *(V1 產線品質帽與 L4 穩態上限，非 H3 15s 模型物理硬頂)* | 必過 V2 速率；超過 4.5s 建議用 L-cut 切插鏡分攤 |
| **`MCU`** | 過肩對白、推進蓄勢、單人陳述 | **`2.0 – 4.0 s`** | `1.5 s` / `5.0 s` | 最常作為 `MCU→CU` 跨一級慢推起點 |
| **`MS`** | 雙人對峙、物理動作、空間交接 | **`2.0 – 3.5 s`** | `1.5 s` / `4.0 s` *(跨 1 級 ≤5.0s)* | 雙人 `2S` 僅作定場與對峙建立，勿長停 |
| **`MLS`** | 進場動量、踉蹌走位、站姿全身感 | **`1.8 – 3.0 s`** | `1.5 s` / `4.0 s` | 9:16 豎屏取代橫屏傳統長鏡頭之關鍵景別 |
| **`WS`** | 定場空景、環境孤立感、時間跳切 | **`1.5 – 2.5 s`** | `1.2 s` / `3.0 s` *(跨 1 級 ≤4.0s)* | 豎屏小螢幕細節小，**定場嚴守 ≤2–2.5s**，除非具 L3 運鏡推進 |
| **`CARD`** | 證據卡、時間戳卡、Truth Ledger | **`1.5 – 3.0 s`** | `1.2 s` / `3.5 s` | 按文字閱讀量計（≤8 字 1.5s；三連新聞卡 2.5–3.0s） |

---

## 2b. 豎屏短劇節奏與張力校準（Creator 明確強調軸線）

> **核心定位**：我們不是在拍電影節慢節奏長鏡頭，我們是在 **IG Reels / Threads / YT Shorts 豎屏資訊流** 裡，用 6 吋手機螢幕和靜音自動播放搶前 1.5 秒停指率。如 [`HIT_STRUCTURE.md`](file:///home/hatch/drama-line/HIT_STRUCTURE.md) 所證，2025–2026 億級 AI 短劇（《斬仙台真人 AI 版》單集 30–40 切、均長 2–3s；《安徽小木匠》均長 72s 靠手部細節快切；《奶團太后》靠 OS＋短反應定格）之所以勝出，正是把 **高切鏡密度＋短特寫衝擊＋資訊視覺化** 當成基本語法，而不是事後加快 1.2× 播放速度。

### 2b.1 鏡長節奏定位與「長停頓是香料，不是常態」原則

- **高張力段基準（`hook` / `escalation` / `climax`）**：ASL 鎖定 **`1.5–2.6 s`**（比 `DEMO02_v2` 的 `3.97 s` 快 nearly **2×**）。
- **長停頓（`3.5–4.8 s`）何時合法？必須同時滿足「三要件測試」**：
  1. **明確的內部戲劇行為（What is it DOING?）**：只能服務三種張力功能之一——
     - **`peak_emotion`**：核心判詞＋微表情從壓抑到銳利的完整狀態轉換（如 `DEMO-02 S4`「……你，怎知我名？」、`EP-01 S09`「會死多少人？」、`S18b` 終極質問）；
     - **`dread_compression`**：恐懼／壓迫持續收緊（必配慢推 `push-in` 或環境異常漸強）；
     - **`held_reaction`**：沉默本身就是反轉（如 `EP-01 S19` `SYS-01` 微笑首次遲疑 0.5 秒）。
  2. **前後速度反差（Contrast Framing）**：長停頓前後至少一側須緊鄰 `≤ 2.0 s` 快切或插鏡；**嚴禁兩顆 `> 3.5 s` 的靜態長停頓緊鄰連播**。
  3. **仍須遵守內部視覺事件紀律**：停頓內不可出現超過 2.5 秒的「無表情、無運鏡、無聲畫事件」死畫面。

### 2b.2 以覆蓋製造張力的五大手法（含各引擎誠實可行性矩陣）

1. **推進（Push-In）作為升溫訊號**：在 `MCU→CU`（Δrank=1）或 `CU` 內微幅慢推，視覺上強制觀眾逼近角色的壓力中心。
2. **切在「聽者反應」，而非只盯「說話者」**：任何超過 `3.5 s` 的單人長台詞（特別是 `SYS-01` 說明句或對手施壓句），善用 Spec §2 `audio_groups[]` 與 §B.7 #1 **J/L-cut**，在 `t = 2.5–3.2 s` 切往 **1.2–1.8 s 聽者閉唇反應 `CU` 或物證 `ECU`**，台詞不斷、張力翻倍，且聽者鏡為 `lip_sensitive=false` 更省算力！
3. **轉折拍點的模式中斷插鏡（Pattern-Interrupt `ECU`）**：每隔 `10–15 s`（精準落在 `JOLT`／`TURN` 拍點），用 `1.0–1.5 s` 的物理特寫（手拍濕牆、指尖按向空腰間、瞳孔閃過青光、翻動方孔錢、壓在紅筆條款上的食指）重設手機觀眾的多巴胺與注意力曲線。
4. **運鏡幅度隨張力遞增（Amplitude Escalation）**：以 `movement.amplitude`（`small → medium → large`）對應場段情緒階梯（例：冷靜對峙 `small` → 異象逼近 `medium` → 抵達失重衝擊 `large` → 最後一問突煞回 `stable_control + small` 形成冰冷反差）。
5. **急推／甩鏡轉場（Snap / Whip / Crash Zoom）——各載體誠實能力邊界表**：

| 張力鏡頭手法 | Flow Omni 1.2 Flash | H3 4-Ref (`544×960` 8-step) | H3 L3 Clay Ref2VA | Wan 2.2 | **L4 後製 (`ffmpeg`)** | 工程建議落點 |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **慢推升溫（`push-in` small/med）** | **佳**（但守 Δrank≤1） | **中**（偶壓扁幅度；`SYS-01` 景易撞安全區） | **極佳**（MS/LS ≤5s） | 中（限無臉） | **100% 可控**（≤12% zoompan） | 常規靠 Flow/H3；`SYS-01` 底板與微推補救走 **L4** |
| **焦慮手持（`handheld`）** | **中**（內建防抖常過穩） | **中弱**（大幅晃易漂臉） | **佳**（預演可控） | **佳**（無臉動感） | **100% 可控**（4–5% 多頻正弦裁切抖） | Flow 主拍＋過穩時 **L4 補抖**，勿重抽 |
| **手／道具 `ECU` 模式中斷** | **極佳**（`3s` 僅 9 點） | 過度殺雞用牛刀 | 不適用 | **極佳**（0 Flow 點） | `CARD` 證據插鏡 **0 成本** | **Flow `tail_only` / Wan 2.2 / `cpu_card`** |
| **甩鏡轉場（Whip Pan Cut）** | **差**（易糊臉與殘影） | **差**（破身份鎖） | 中（耗配額） | 中（限無臉） | **100% 可控**（接點 3–4 幀定向模糊＋位移） | **嚴禁 AI 硬生，一律 L4 剪輯接點製作** |
| **急推衝擊（Crash Zoom）** | **差**（常失控變形） | **差** | 不建議 | 差 | **100% 可控**（4–6 幀 1.0×→1.25× 急推） | **一律 L4 後製**（對齊附錄 A.1 `crash-zoom-post`） |
| **失焦合焦（Rack Focus）** | **差**（無對焦參數） | **差** | 不適用 | 差 | **100% 可控**（起鏡 0.4s `gblur` 衰減） | **一律 L4 後製**（對齊 `DIRECTOR_LAYER_AGY_MEMO` Q3） |
| **空間撕裂／Glitch 閃入** | **禁**（易出假字崩臉） | **禁** | 不適用 | **禁** | **100% 可控**（`rgbashift`＋2 幀閃＋`sound_drop`） | **100% L4 / AMD-05** |

### 2b.3 無死氣規則（No-Dead-Air Rule — 視覺事件密度上限）

定義一次合法的 **視覺事件（Visual Event）** 為以下五者之一：
1. **切鏡**（切換至下一顆原子鏡）；
2. **可見景別或運鏡推進**（`movement.type != "static"` 且幅度肉眼可辨，或 L4 `zoompan ≥ 8%`）；
3. **模式中斷／VFX 拍點**（`vfx_beats[]`：`glitch_in`、`env_reaction` 燈閃、`light_shift`、`composite_ui` 投影現身或數值變化）；
4. **後製視覺圖文層出現或切換**（`visual_text_overlay[]` 登場／翻頁）；
5. **顯著物理動作／微表情轉折點**（於 `shots[].internal_event_sec[]` 顯式宣告之可觀察觸發時碼，如 `t=1.8s` 猛然抬頭盯路燈、`t=1.2s` 放下手機轉身）。

**硬約束公式**：任一鏡頭若 `movement.type == "static"` 且無 `vfx_beats[]`、無 `visual_text_overlay[]`，則其連續無事件區間（相鄰 `internal_event_sec` 間隔，起點 `0`、終點 `target_net_sec`）不可超過表 A 之 **Dead-Air 門檻**：
- `hook` / `climax` / `chase_tension`：**軟警 `2.0 s` ／ 硬駁回 `2.5 s`**；
- `escalation` / `confrontation`：**軟警 `2.5 s` ／ 硬駁回 `3.5 s`**；
- `revelation`：**軟警 `3.0 s` ／ 硬駁回 `4.0 s`**；
- `release_bridge`：**軟警 `3.5 s` ／ 硬駁回 `4.5 s`**。

### 2b.4 成本感知節奏工程（如何把鏡數拉高 +65–85%，成本卻只增 +15–25%？）

若天真地「把每顆鏡頭都切短重跑英雄模型」，會立刻撞上兩大成本陷阱：① **裁切緩衝稅**——把 1 顆 `5s` 淨長（`6s` 生成＝`18 pts`）Flow 鏡硬拆成 2 顆 `2.5s`（各 `3.5s→4s` 生成＝`24 pts`），光 `standard_0.5s` 緩衝就多付 **+33%**；② **H3 單鏡時間稅**——多加 1 顆 Colab L4 `H3-4Ref` 對白 CU 就要多花 `~0.16–0.26 CU` 與 `~5 分鐘`。

**五條「低價買密度」的產線實戰槓桿（以 `demo02_v2`／`EP-01` 實測單價校準）**：

| 槓桿 | 做法 | 單鏡成本 | 為何不損品質 |
| :--- | :--- | :---: | :--- |
| **1. 用「無正臉／無口型 `ECU` 插鏡」買密度** | 手拍牆、摸空腰間、轉方孔錢、舉手機、捧古劍、竹簡落門——`face_visible=false` 或 `lip_sensitive=false`，全走 **Flow `3s` 或 Colab Wan 2.2** | Flow **`9 pts`**（重抽僅 `1.1×`）或 Wan **`0 Flow 點` / `~0.04 CU`** | 無臉部鎖定壓力，一次過稿率高達 85–90%，卻是豎屏最強的節奏引擎 |
| **2. 短插鏡與短反打改用 `trim_policy: "tail_only"`** | 因 QC-1 已鎖乾淨 `nano2` 首幀，短插鏡前 0.2s 本就穩定，省去開頭 `0.5s` 緩衝（生成長從 `淨+1.0s` 降至 `淨+0.5s`） | 每顆短 Flow 鏡省 **`1.5–3.0 pts`** | 保留 H3 對白與複雜動作的 `standard_0.5s`；僅對 `is_insert`／短反應放行 `tail_only` |
| **3. 善用 `cpu_card` 與 AMD-05 數據／文字插鏡** | 時間戳、新聞證據卡、系統狀態閃幀、2.5D 矩陣圖 | **`0 pts` / `0 CU`** | 100% 過稿、零亂碼（V9），是 `HIT_STRUCTURE.md` 驗證的最高 ROI 模式中斷 |
| **4. 單次抽片雙切回收（Clip Harvesting）** | 1 支 `4s` 乾淨的聽者反應或目擊反應成片，可於 `edit_manifest.json` 切成 `Beat A [0.5–1.9s]` ＋ `Beat B [2.2–3.5s]`（甚至 L4 `1.15×` 裁切推近一級）穿插於對白之間 | 第二切 **`0 pts` / `0 CU`** | 適合雙人對白 ping-pong 反應鏡；1080p Flow 源片裁切 ≤15% 零明顯降質 |
| **5. 嚴守「新增鏡數零追加 H3-4Ref」紀律** | 把原本 `5.2s` 的 H3 對白鏡（如 `EP-01 S07`）中間切入 1 顆 `1.5s` 無臉手部/道具插鏡（L-cut），H3 對白鏡反而**縮短至 `3.7s`**（更穩、更省重抽） | **H3 總鏡數 `+0`、重抽率反降** | 用便宜載體切開昂貴對白鏡，同時解掉 V1 穩定上限與 Dead-Air 兩大痛點 |

**成本對比模型（以 EP-01 ~100 秒全集計，基準來自 `EP01_PRODUCTION_WORKFLOW.md` §4.2）**：

| 方案 | 原子鏡數 | 非卡 ASL | Flow 影片點數（預期） | Colab L4 CU（預期） | 結論 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **原 29 鏡基線**（`EP01_PRODUCTION_WORKFLOW.md`） | 29 鏡（26 非卡） | `3.52 s` | `~346 pts` | `~4.3 CU` | 多段不符覆蓋與短劇節奏規則 |
| **天真全英雄快切**（全加 Flow 5s＋加 H3 反應 CU） | 42 鏡（39 非卡） | `2.35 s` | `~590 pts` (`+71%`) | `~6.8 CU` (`+58%`) | 浪費點數於冗餘緩衝與高價反應鏡 |
| **本案：成本感知混合快切**（`+13` 鏡全為 `3s tail_only` Flow / Wan 插鏡＋零新增 H3-4Ref） | **42 鏡（39 非卡）** | **`2.35 s`** | **`~425 pts`（`+23%`；若 6 顆無臉插鏡轉 Wan 僅 `~345 pts` 幾乎持平！）** | **`~4.6 CU` (`+7%`)** | **鏡數密度 `+45%`、ASL 快 `-33%`，穩落月配額 33%–40% 內** |

---

## 3. 實戰重排示範（證明工作流修訂確實改變產出）

### 3.1 示範 A：重排 `DEMO-02` 抵達段（維持 ~24.0 s 同片長，從 6 鏡升至 11 鏡）

> **跨文件對接說明**：本表精準對齊 `DEMO02_v2` 的 **`24.0 s`** 巷弄抵達包絡（方便與已出貨之 `23.79 s` 6 鏡版本做蘋果對蘋果對照）。若與平行提案 [`DEMO03_TREATMENT.md`](file:///home/hatch/drama-line/DEMO03_TREATMENT.md) 合併，只需在 `S1a` 前直接前置其 `S0`（`1.5s` 太湖閉眼前態＋4 幀空間撕裂，總長 `25.5 s ≤ 30 s`），且本表 `S1a/S1b`（高撐左牆＋左臂外展）、`S2a/S2R`（婦人有聲化＋背口遮唇）與 `S3b`（AMD-05 v2 真人虛擬投影）皆已 100% 介面相容。

#### 新舊版本總指標對照
| 維度 | 已出貨 `DEMO02_v2`（舊流程） | 新規則重排版（Coverage v2.4） | 差異說明 |
| :--- | :---: | :---: | :--- |
| **總鏡數／總淨長** | `6 鏡` / `23.79 s` | **`11 鏡` / `24.0 s`** | 同片長內鏡數 **`+83%`** |
| **ASL / 每 10 秒鏡數** | `3.97 s` / `2.52 鏡/10s` | **`2.18 s` / `4.58 鏡/10s`** | 精準落入豎屏 `hook`/`escalation` 目標帶 |
| **景別分佈（R1a）** | `MS/2S×3, MCU×2, CU×1`（3 級，偏中景） | **`MLS×1, MS×2, MCU×3, CU×2, ECU×3`（5 級）** | 零連續同尺幅鏡；視覺節奏高低起伏分明 |
| **首顆特寫落點（R2）** | `t = 19.12 s`（80% 後） | **`t = 1.8 s`（`ECU`）＆ `t = 8.8 s`（`CU`）** | 細節插鏡落於 `1.8s / 7.6s / 16.0s`（間距全 `< 10s`） |
| **ECU 配給（R8）** | `0 / 6` (`0%`) | **`3 / 11` (`27.3%` 鏡數 / `15.4%` 時長)** | 精準落於 `≤ 30%` 鏡數且 `≤ 20%` 時長安全帶 |
| **180° 軸線（R9）** | `S2→S3a` 視線跳翻（Honest Defect #1） | **范蠡恆鎖 `left→right`、婦人／SYS-01 `right→left`** | 零跳軸、零視線反轉 |
| **預估首輪生成花費** | Flow `45 pts` ＋ H3 `~0.44 CU` | **Flow `54–72 pts`（2 顆手部 ECU 轉 Wan 僅 `54 pts`）＋ H3 `~0.42 CU`** | **H3 花費持平略降；Flow 僅增 `+9~27 pts` 換近雙倍張力** |

#### 完整 11 鏡覆蓋表（`SEG-01`｜profile: `hook`｜axis: `FANLI=left→right, WITNESS=right→left, SYS-01=right→left`）

| Shot | 時段（淨秒） | Size / Flags | Named Shot | Move（spd/amp→end）＋ Motivation | Psych | Beat / Role / Peak | Dial / Lip | 關鍵畫面、視覺事件與載體路由（成本） |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`S1a`** | `0.0–1.8s` (**`1.8s`**) | **`MLS`**<br>`angle_v: low` | `handheld-jolt` | `handheld` (fast/lg)<br>`subjective_instability` | `handheld_anxiety` | `HOOK` / `establish` | `none` / `F` | 范蠡失重斜衝過濕柏油巷道撲向左牆，右臂高舉、左臂外展平衡；`t=0.2s` 路燈電壓驟閃（`env_reaction`）。**Flow `3s tail_only`（9 pts）** |
| **`S1b`** | `1.8–3.0s` (**`1.2s`**) | **`ECU`**<br>`insert` | `ecu-detail-insert` | `handheld` (std/med)<br>`rhythm_jolt` | `handheld_anxiety` | `JOLT` / `insert_detail` | `none` / `F` | 濕掌重重拍上粗糙水泥牆（肩高），水珠震落；遠處機車防盜器雙鳴。`face_visible=false` → **Wan 2.2（0 Flow 點）或 Flow `3s`（9 pts）** |
| **`S1c`** | `3.0–5.2s` (**`2.2s`**) | **`MCU`**<br>`left→up` | `push-escalation-mcu` | `push-in` (slow/sm **→`CU`**)<br>`emotional_intensify` | `handheld_anxiety` | `SETUP` / `action` | `off_camera` / `F` | 劇烈喘息（`z4_heavy_heave`）→ `t=0.5s` 路燈餘閃滋啪，下巴驟抬 15° 盯電燈（`z1_startled_snap`）→ `t=1.8s` 右側畫外 J-cut 袋聲＋婦人驚呼「欸——！」，雙眼急轉右。**Δrank=1 合規 `SCALE_JUMP_BAN`**。**Flow `3.5s`（12 pts）** |
| **`S2a`** | `5.2–7.6s` (**`2.4s`**) | **`MS`**<br>`two_shot` | `steady-dialogue-lock` *(微手持)* | `handheld` (slow/sm)<br>`action_follow` | `handheld_anxiety` | `ESCALATION` / `establish` | `on_camera`*(遮口)* / `F` | 鎖定雙人軸線：范蠡左站右視、50 歲婦人剛自右巷口急停（後側 3/4 遮口位發聲質問，見 `DEMO03_TREATMENT` §2.4）。微動作齊全。**Flow `3.5s`（12 pts）** |
| **`S2b`** | `7.6–8.8s` (**`1.2s`**) | **`ECU`**<br>`insert` | `ecu-detail-insert` | `push-in` (std/sm)<br>`rhythm_jolt` | `predator_stalk` | `ESCALATION` / `insert_detail` | `l_cut_carry` / `F` | 范蠡左手五指本能猛按向左外側空腰間（無劍柄——招牌動作！），背景失焦處婦人深色手機正在抬起。`face_visible=false` → **Wan 2.2（0 Flow 點）或 Flow `3s`（9 pts）** |
| **`S2c`** | `8.8–10.6s` (**`1.8s`**) | **`CU`**<br>`ots, reverse` | `ots-reverse-cu` | `handheld` (slow/sm)<br>`action_follow` | `handheld_anxiety` | `ESCALATION` / `reaction` | `none` / `F` | 過范蠡左肩反打婦人特寫（`right→left`）：她收起試探笑意、眼神驚疑後退半步、舉穩手機對準他。**（首顆人臉 CU 提早至 `8.8s`！）Flow `3s tail_only`（9 pts）** |
| **`S3a`** | `10.6–12.6s` (**`2.0s`**) | **`MCU`**<br>`left→right` | `intimate-drift-close` | `push-in` (slow/sm)<br>`emotional_intensify` | `intimate_drift` | `TURN` / `turn_jolt` | `none` / `F` | 承接 `S2a/S2c` 軸線（范蠡仍朝右看，零跳軸！）；`t=1.65s` 聲場抽空（`sound_drop -38dBFS`）＋右側驟亮冷青回光打上右頰，他瞳孔微縮。**H3-4Ref `3.0s tail_only`（~0.12 CU；可重用舊 `S3a` 裁後段 0 CU！）** |
| **`S3b`** | `12.6–16.0s` (**`3.4s`**) | **`MS`**<br>`two_shot`*(投影)* | `subtle-pull-reveal` | `static`＋**L4 6% 微拉/呼吸**<br>`spatial_reveal` | `intimate_drift` | `TURN` / `speaker` | `on_camera`*(SYS-01)* / `F` | `t=0.1s` `glitch_in`／AMD-05 v2 投影於右側 55% 顯影，`sys.mp3` 起聲（前 3.2s）；范蠡背貼左牆緊繃盯視（閉唇）。**3.4s 即切出，徹底消滅舊版 5.08s 死氣！H3-4Ref 乾淨底板（~0.14 CU；可複用舊 `S3b_t2` 0 CU！）＋AMD-05** |
| **`S3c`** | `16.0–17.3s` (**`1.3s`**) | **`ECU`**<br>`insert` | `ecu-detail-insert` | `push-in` (slow/sm)<br>`emotional_intensify` | `intimate_drift` | `JOLT` / `reaction` | `l_cut_carry`*(SYS 喚其名)* / `F` | 極近眼部特寫：冷青反光點映在范蠡瞳孔（守 §B.7 #2 降載規），聽見系統喚出真名瞬間眉心微鎖（`z2_hairline_knit`）。`lip_sensitive=false` → **Flow `derived_shot` `3s tail_only`（9 pts）或 L4 裁推（0 pts）** |
| **`S2R`** | `17.3–19.6s` (**`2.3s`**) | **`MCU`**<br>`ots, reverse` | `ots-reverse-cu` | `handheld` (slow/sm)<br>`spatial_reveal` | `cold_observe` | `PAYOFF` / `reaction` | `l_cut_carry`→`off_cam` / `F` | 婦人反打（`right→left`）：承 `sys.mp3` 尾音 0.9s，她皺眉看著范蠡對空無一人的潮濕空氣緊繃對峙 → `t=1.2s` 垂下手機、搖頭轉身背口嘟囔快走（見 `DEMO03_TREATMENT` §2.4）。**Flow `3.5s`（12 pts）** |
| **`S4`** | `19.6–24.0s` (**`4.4s`**) | **`CU`**<br>**`★ PEAK`** | `slow-push-verdict` | `push-in` (slow/sm)<br>`power_lock` | `stable_control` | `CLIFF` / `peak_hold` / **`PEAK`** | `on_camera`*(范蠡)* / **`T`** | **全段唯一長停頓（ earned contrast hold）**：前 10 鏡緊湊鋪壓後，機位驟穩慢推；范蠡垂目吸氣壓下恐懼、抬眼銳利低問「……你，怎知我名？」→ 鎖定冷冽眼神硬切黑。**H3-4Ref `5.4s`（~0.16 CU；可 100% 複用舊 `S4.mp4` 0 CU！）** |

> **時間加總驗算**：`1.8 + 1.2 + 2.2 + 2.4 + 1.2 + 1.8 + 2.0 + 3.4 + 1.3 + 2.3 + 4.4 = 24.0 s`（精準吻合）。全 11 鏡經逐條檢驗：**R1a/b/c PASS、R2 PASS、R3 PASS、R4 PASS、R5a/b PASS、R8 PASS（3/11=27.3%、3.7/24.0=15.4%）、R9 PASS、`SCALE_JUMP_BAN` PASS、V1/V2 PASS**。

---

### 3.2 示範 B：`EP-01` 29 顆原子鏡路由表之覆蓋健檢與不改台詞修補案

依 [`EP01_PRODUCTION_WORKFLOW.md`](file:///home/hatch/drama-line/EP01_PRODUCTION_WORKFLOW.md) §2.1 & §2.3（`20` 劇本鏡 → `29` 原子鏡，總長 `100.2 s`，**嚴守零改動劇本一字對白**），逐場段與逐鏡標註新規則判定與最小手術方案：

#### A. 五場段覆蓋健檢總表

| 場段 | 現行鏡數／非卡長／ASL | 場段類型（`profile`） | 新規則判定 | 具體違規項 | 修補後鏡數／非卡 ASL（不改台詞、總長不變） |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **`SEG-01`** (`S01`) | `1 鏡` / `4.0s` / `4.00s` | `hook` | **FAIL（節奏）** | R1a 微場段豁免，但 `4.0s` 單鏡太湖空景撞爆 `hook` ASL (`≤2.2s`) 與首 1.5s 視覺鉤 | **`2 鏡` / `2.00s`**（`S01` 拆 `S01a` WS→MLS + `S01b` CU 閉眼空間撕裂） |
| **`SEG-02`** (`S02–S04c`) | `5 鏡` / `19.1s` / **`3.82s`** | `escalation` | **FAIL（4 項）** | ① `R2` 前 13.5s 無 CU/ECU；② `R3` `S02` 5.0s 無對白 MS；③ `R4` 雙人對白無 OTS/反打；④ `DEAD_AIR` `S02`/`S03` | **`9 鏡` / `2.12s`**（`S02` 拆 3、`S03` 拆 3、`S04a` 改 OTS；0 新增 H3） |
| **`SEG-03`** (`S05–S12`) | `10 鏡`（8 非卡 `31.1s`）/ **`3.89s`** | `confrontation` | **FAIL（3 項）** | ① `R2` 全段 31.1s 零細節插鏡；② `R4` 雙人對白無 OTS/反打；③ `DEAD_AIR` `S07(5.2s)/S08(5.0s)/S10(5.0s)` 連三鏡 ~5s 無切鏡 | **`14 鏡`（12 非卡）/ `2.59s`**（補 4 顆無臉/閉唇插鏡與 OTS 改位；`S07` H3 反而縮短至 `3.7s`！） |
| **`SEG-04`** (`S13–S16b`) | `7 鏡` / `22.0s` / `3.14s` | `revelation` | **FAIL（4 項）** | ① `R1b` 全段無 CU 峰值鏡；② `R1c` `S13→S14a→S14b` 連 3 鏡 `MS`；③ `R2` 前 16s 零 CU/ECU；④ `R3` `S13` 5.0s MS | **`10 鏡` / `2.20s`**（`S13` 拆 WS+CU、`S14b` 拆 MLS+ECU、`S16a` 縮 2.0s、`S16b` 拆 WS+CU 呼應 S01） |
| **`SEG-05`** (`S17a–S20`) | `6 鏡`（5 非卡 `15.3s`）/ `3.06s` | `climax` | **WARN / 小修** | 結構最優；缺 1 顆 `ECU` 細節呼應（`S18a` 停在 MCU 浪費第三拍招牌動作），且 `S19` 結尾可推至 `ECU` 拉滿懸念鉤 | **`7 鏡`（6 非卡）/ `2.55s`**（`S18a` 升格 `ECU`；`S19` 拆 `1.8s CU` + `1.2s ECU` 眼顫閃「蠡」） |
| **全集總計** | **`29 鏡`（26 非卡 `91.5s`）/ `3.52s`** | 5 段 | **4 FAIL / 1 WARN** | 29 鏡原案僅 1 顆 INSERT、0 顆 ECU、0 顆對白 OTS | **`42 鏡`（39 非卡 `91.5s`）/ `2.35s`（`4.26 鏡/10s`）**；**0 新增 H3-4Ref、總長維持 `100.2s`！** |

#### B. 29 顆原原子鏡逐鏡覆蓋裁決與精準修補表（不改劇本台詞）

| 原原子鏡 | 原秒數／景別 | 裁決 | 違規／診斷 | 不改台詞修補方案（新鏡號、秒數、景別與低價載體） |
| :--- | :---: | :---: | :--- | :--- |
| **S01** | `4.0s` LS→MS | **SPLIT (1→2)** | `hook` 4s 單鏡過緩、首 1.5s 無強鉤 | **`S01a`**(`2.2s` `WS→MLS` L3-Clay 晨霧空座) ＋ **`S01b`**(`1.8s` `CU` 范蠡閉眼＋4 幀空間撕裂切 2022；兼作 `S16b_2` 呼應基準；Flow `3s tail_only`) |
| **S02** | `5.0s` MS | **SPLIT (1→3)** | **FAIL R3**（無對白 >3.5s）、**FAIL DEAD_AIR**、浪費招牌動作 1 | **`S02a`**(`2.2s` `MLS` 墜落入畫＋L4 `2022.11.30` 字卡，Flow) ＋ **`S02b`**(`1.3s` `ECU` `insert` 手按空腰間招牌動作 1，Wan/Flow) ＋ **`S02c`**(`1.5s` `CU` 瞳孔掃現代街景霓虹，Flow) |
| **S03** | `5.5s` MS | **SPLIT (1→3)** | **FAIL DEAD_AIR**（5.5s MS 靜聽 SYS-01 18 字）、**FAIL R2** | **`S03a`**(`3.2s` `MS` `two_shot` AMD-05 SYS-01 顯影＋台詞前半，Flow) ＋ **`S03b`**(`1.3s` `ECU` `insert` 退半步再按空腰間招牌動作 2，L-cut 承台詞中段，Wan/Flow) ＋ **`S03c`**(`1.0s` `CU` 范蠡警覺眼部＋2 幀「蠡」閃，Flow) |
| **S04a** | `3.0s` MCU | **REFRAME** | **FAIL R4**（雙人對白無 OTS） | 改為 **`MCU` `is_ots=true, is_reverse=true`**（過范蠡肩看 SYS-01 投影說「免費的」，Flow 底板＋AMD-05） |
| **S04b** | `3.8s` CU | **PASS** | 符合 V1/V2 與 R4 單人 CU | 保留 `H3-4Ref`（`lip_sensitive=true`）；注意軸線與 `S04a` 相向 |
| **S04c** | `1.8s` CU | **PASS** | 優秀短反應拍 | 標記 **`emotional_peak: true`**（`SEG-02` 峰值鏡，閉唇銳利凝視→轉身） |
| **S05** | `3.0s` CARD | **PASS** | 優秀轉場證據卡 | 保留 `cpu_card`（L4 `zoompan` 節奏切入三連新聞卡） |
| **S06** | `3.5s` MS | **SPLIT (1→2)** | 補 `SEG-03` 首顆細節插鏡（**R2**） | **`S06a`**(`1.8s` `MS` 套房書桌與窗外巨幕定場，Flow) ＋ **`S06b`**(`1.7s` `ECU` `insert` 毛筆紙本鈔票＋後製疊 `1,454 天` 桌面小屏，Wan/Flow) |
| **S07** | `5.2s` MCU | **SPLIT (1→2)** | **FAIL DEAD_AIR**（5.2s 單鏡）且逼近 H3 建議上限 | **`S07a`**(`3.7s` `MCU` H3-4Ref 范蠡主說) ＋ **`S07b`**(`1.5s` `ECU` `insert` 范蠡指尖轉動現代方孔錢／壓住書案，L-cut 承台詞中後段，Wan/Flow）——**同時把 H3 鏡壓回 3.7s 黃金穩定區！** |
| **S08** | `5.0s` MS | **SPLIT (1→2)** | **FAIL R4**（缺 OTS）、**FAIL DEAD_AIR**（5.0s 單鏡） | **`S08a`**(`3.2s` `MCU` `is_ots=true` 過范蠡肩看 SYS-01＋後製側欄圖解，Flow＋AMD-05) ＋ **`S08b`**(`1.8s` `CU` 范蠡閉唇眼神掃讀數據反應拍，L-cut 承尾音，Flow） |
| **S09** | `4.8s` CU | **PASS（峰值停頓）** | 合法對比長停頓（`slow-push-verdict`） | 標記 **`emotional_peak: true`**、**`hold_justification: "peak_emotion"`**；因前後已被快切包夾，4.8s「會死多少人？」慢推壓迫感倍增 |
| **S10** | `5.0s` MS | **SPLIT (1→2)** | **FAIL DEAD_AIR**（5.0s 單鏡） | **`S10a`**(`3.2s` `MS` `is_ots=true` SYS-01 平靜回覆，Flow＋AMD-05) ＋ **`S10b`**(`1.8s` `ECU` `insert` 左腕舊銅錶與微低眉眼 `z4_calm_breath`，L-cut 承尾音，Flow/Wan） |
| **S11a** | `2.6s` MCU | **PASS** | 節奏俐落 | 保留 `H3-4Ref` 起身對白（加 `movement: pedestal up` 或微 `push-in`） |
| **S11b** | `2.2s` CARD | **PASS** | 模範模式中斷證據卡 | 保留 `cpu_card`（2023 Altman 新聞卡，0 成本） |
| **S11c** | `2.0s` CU | **PASS** | 短促重拳判詞 | 保留 `H3-4Ref`（採 `tail_only` 2.5s 生成；依 §4 V1 放寬不再誤報短鏡 WARN） |
| **S12** | `3.0s` CU | **PASS** | 暖光 Match Cut 橋接佳 | 保留 `H3-4Ref`（微 `push-in` 接燭火閃切） |
| **S13** | `5.0s` MS | **SPLIT (1→2)** | **FAIL R1c**（連 MS 起頭）、**FAIL R1b/R2**（全段無 CU）、**FAIL R3** | **`S13a`**(`2.8s` `WS` 越國慶功大殿與勾踐畫外起音，Flow/可選 L3) ＋ **`S13b`**(`2.2s` `CU` 范蠡朝服 `OUTFIT-03` 側後神色轉冷 `z1_sharp_lock`，`lip_sensitive=false` 走 Flow！) |
| **S14a** | `2.5s` MS | **PASS** | 朝堂空座＋燭火微搖 | 保留 `MS`（前接 `S13b` CU，打破 3 連 MS！） |
| **S14b** | `3.5s` MS | **SPLIT (1→2)** | **FAIL R1c**（與 S14a 同為 MS）＋ 補物證細節 | **`S14b_1`**(`2.0s` `MLS` 文種門庭快步送書，Wan/Flow) ＋ **`S14b_2`**(`1.5s` `ECU` `insert` 無字竹簡信落地／置門檻，Wan/Flow） |
| **S15a** | `3.2s` OTS | **PASS** | 合規 `MCU` `is_ots=true` | 保留 `MCU` `is_ots=true` 文種背影展簡（Wan/Flow） |
| **S15b** | `1.8s` LS | **PASS** | 精準短空景對照 | 正規化為 `WS`（`1.8s` 朝堂文種空座，守 WS ≤2.5s 紀律） |
| **S16a** | `3.0s` INSERT | **TRIM (`3.0→2.0s`)** | 3.0s 靜態道具插鏡偏長（表 B 建議 ≤2.0s） | 壓至 **`2.0s`** `ECU` `is_insert=true`（微 `push-in` 內侍雙手捧青銅古劍，Wan/Flow）；騰出 `1.0s` 給 `S16b` 雙鏡收束 |
| **S16b** | `3.0s` MS | **SPLIT (1→2, `4.0s`)** | 單鏡 `MS` 同時演小舟靠近＋閉眼微表情易失焦 | **`S16b_1`**(`2.2s` `WS` `ref_shot: S01a` 使者小舟逼近太湖獨舟，Flow) ＋ **`S16b_2`**(`1.8s` `CU` **`emotional_peak: true`** `ref_shot: S01b` 范蠡閉眼 `z3_closed_still_lips`，Flow）——與 `S01a/S01b` 完美首尾閉環！ |
| **S17a** | `1.5s` MS背側 | **PASS** | 極佳 J-cut 短引鏡 | 保留 `1.5s` `MS`（Flow） |
| **S17b** | `4.5s` CU | **PASS** | 核心判讀句（`slow-push-verdict`） | 保留 `H3-4Ref`；具 `push-in`（`small`）故無 Dead-Air |
| **S18a** | `1.8s` MCU | **UPGRADE SIZE** | `MCU` 放手部招牌動作 3 不夠刺眼，缺 `SEG-05` `ECU` | 升格為 **`1.8s` `ECU` `is_insert=true`**（手抬起又緩緩放下、不再按向腰間——與 `S02b`／`S03b` 兩次 `ECU` 形成三拍視覺閉環！`face_visible=false` 走 Flow/Wan） |
| **S18b** | `4.5s` CU | **PASS（峰值停頓）** | 全集最高張力質問 | 標記 **`emotional_peak: true`**（`H3-4Ref`，`slow-push-verdict`；Stage 1.5 依實長鎖 4.5–4.8s） |
| **S19** | `3.0s` CU | **SPLIT (1→2)** | 結尾懸念可再壓緊一級至 `ECU` | **`S19a`**(`1.8s` `CU` `SYS-01` 微笑首次遲疑 0.5s，Flow/雙圖) ＋ **`S19b`**(`1.2s` `ECU` 眼部極近特寫＋L4 急推 12%＋2 幀邊緣「蠡」閃＋硬切黑！0 額外點數走 L4 裁推或 1 鏡短切) |
| **S20** | `3.5s` CARD | **PASS** | 片尾鉤＋Truth Ledger | 保留 `cpu_card` |

---

## 4. `preflight_gate.py` 與 QC-D 整合設計

### 4.1 新增 Preflight 規則清單（`tools/preflight_gate.py` v2.4 增量規格）

沿用現行 `Finding(level, rule, shot_id, message, stamp)` 與 `validate_script_pack()` 架構（見 `tools/preflight_gate.py` §530），在既有的逐鏡迴圈後新增 **`_validate_coverage_rules(pack, seg_map, shots, findings)`** 場段彙總段。

- **版本門檻與 Demo 零豁免**：
  - `schema_version >= "2.4"`（含 `production_mode: "demo"`）：全部 `HARD` 規則發 **`FAIL`**（阻斷送出）。
  - `schema_version < "2.4"`（舊包回放）：預設降為 `WARN`，加傳 CLI 旗標 `--coverage-strict` 時升為 `FAIL`。

| Rule ID | 對應規則 | 依賴欄位 | `FAIL` 條件（HARD） | `WARN` 條件（ADVISORY） | 豁免條件 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`COVERAGE_SCALE_VARIETY`** | R1a | `shot_size`, `framing_flags`, `target_net_sec` | 非卡段長 `≥8.0s` 或非卡鏡 `≥4` 時，相異正規化 `shot_size < 3` **或** 無 `CU`/`ECU` | 3 鏡／`6–8s` 段相異景別 `< 2` 或無 `CU`/`ECU` | 非卡鏡 `≤2` 且 `<6.0s` 之微場段、`release_bridge` |
| **`COVERAGE_PEAK_CLOSEUP`** | R1b | `emotional_peak`, `shot_size`, `movement.end_shot_size` | `emotional_peak=true` 但非 `CU`/`ECU`（且非 `MCU→CU`）；或非橋接段 `≥8.0s` 卻無任何 `emotional_peak=true` | — | 純 `CARD` 段、`release_bridge`、`<8.0s` 微段 |
| **`COVERAGE_SCALE_STAGNATION`** | R1c *(升 V12d)* | `shot_size`, `framing_flags.is_reverse`, `monotony_exempt_reason` | 連 `>2` 顆非反打同 `SCALE_RANK` 鏡；或連 `>4` 顆反打同尺幅且無豁免理由 | 連 `4` 顆反打同尺幅無豁免理由 | `CARD` 不計入連續鏈 |
| **`COVERAGE_DETAIL_CADENCE`** | R2 | `shot_size`, `framing_flags.is_insert`, `coverage_role`, `target_net_sec`, `segment_pacing_profile` | 在 `hook`/`escalation`/`confrontation`/`climax` 段：① 任一連續 `≥10.0s` 非卡滑窗無 `CU`/`ECU`；② 段長 `≥12.0s` 卻低於每 `12.0s` 1 顆細節／反應 `CU`/`ECU` | 同條件於 `revelation` / `release_bridge` 段觸發 | 非卡段長 `<10.0s`（僅免滑窗） |
| **`COVERAGE_NON_DIALOGUE_CAP`** | R3 | `dialogue_mode`, `dialogue[]`, `target_net_sec`, `shot_size`, `movement.end_shot_size`, `performance_beat.deliberate_hold`, `hold_justification` | 無對白非卡鏡逾 `3.5s`（高張力段）或 `4.0s`（一般段），且未符合「`Δrank==1`（`≤5.0s`）」或「`deliberate_hold+hold_justification`（`≤4.5s`）」 | 展延至 `4.0–5.0s` 且未標 `internal_event_sec` | `CARD` 鏡；有對白／L-cut 鏡（走 V1/V2） |
| **`COVERAGE_TWO_PERSON_DIALOGUE`** | R4 | `dialogue[].speaker`, `framing_flags.{is_ots,is_reverse,is_two_shot}`, `shot_size` | 段內 `≥2` 說話者且 `≥2` 輪次，但缺 `is_ots`/`is_reverse`、或缺單人 `CU`/`MCU`、或連 `>1` 顆有對白 `is_two_shot` | 僅 1 輪雙人發聲且全為 `2S` | 單人獨白／純畫外旁白段 |
| **`COVERAGE_SEGMENT_KINETIC`** | R5a | `movement.type`, `control_method`, `segment_pacing_profile` | `≥3` 顆非卡鏡場段 100% 為 `static`（且無 L4 後製運鏡宣告） | `hook`/`escalation`/`climax` 主動運鏡鏡數 `<50%` | `≤2` 鏡微段 |
| **`COVERAGE_MOVE_MOTIVATION`** | R5b *(擴 V12e)* | `movement.motivation`, `movement.type`, `camera_psychology`, `camera_override_reason` | Schema 2.4+ 非卡鏡缺少 `movement.motivation` 或不在 6 枚舉內 | `(camera_psychology, movement.type, motivation)` 違反 §1.2 相容矩陣且無 `camera_override_reason` | `CARD` 鏡 |
| **`COVERAGE_DEAD_AIR`** | §2b.3 | `target_net_sec`, `movement.type`, `vfx_beats[]`, `visual_text_overlay[]`, `internal_event_sec[]` | 靜鏡且無 VFX／無疊字／無 `internal_event_sec`，最大無事件間隔超表 A **硬上限**（`2.5 / 3.5 / 4.0 / 4.5s`） | 超表 A **軟上限**（`2.0 / 2.5 / 3.0 / 3.5s`） | `CARD` 鏡 |
| **`COVERAGE_ECU_RATIONING`** | R8 | `shot_size`, `target_net_sec`, `beat_function`, `segment_pacing_profile` | 段內（`≥4` 非卡鏡）`ECU` 鏡數 `>40%`；或連 `>2` 顆 `ECU`（`chase_tension` 上限 `3`） | `ECU` 鏡數 `>30%` 或時長 `>20%`；或有臉 `ECU` 用於 `SETUP`/`BRIDGE` | `<4` 鏡微段免佔比檢 |
| **`COVERAGE_AXIS_DISCIPLINE`** | R9 | `segments[].axis_plan`, `subject_facing`, `screen_side`, `framing_flags.is_reverse`, `axis_turn_trigger` | `is_reverse=true` 與所回應前鏡之 `subject_facing` 同為 `left` 或同為 `right`（同向看而非對看） | 同角色於同段連鏡 `left ↔ right` 翻轉且無 `axis_turn_trigger`/`continuity_override`；或 `≥2` 人物鏡段缺 `axis_plan` | `face_visible=false` 純手／道具插鏡豁免 |
| **`COVERAGE_PACE_ENVELOPE`** | R7 | `target_net_sec`, `segment_pacing_profile` | *(不發 FAIL)* | 段 ASL 超出表 A 目標帶 `+0.5s` 以上；或全集 `≥6` 非卡鏡時 `CV < 0.25`（節拍器警告） | `<3` 鏡微段免算 ASL |

### 4.2 與既有規則的精準組合契約（`SCALE_JUMP_BAN` × `V1` × `V2`）

覆蓋多元規則絕不可反向破壞已實證的技術護欄，三組規則依以下優先與組合契約協作：

1. **與 `SCALE_JUMP_BAN` 的安全組合（核心衝突化解）**：
   - `preflight_gate.py` 現行 `SCALE_JUMP_BAN`（§958）禁止在 `i2v_first`／`i2v_first_last` 上跨兩級以上推臉（如 `LS→CU`、`MS→ECU`），且 Spec §C.1 禁臉框放大 `>1.8×`。
   - **組合規則**：
     - **鏡內推進（In-shot Move）**：R3 的跨景別展延 **硬限 `｜rank(end_shot_size) − rank(shot_size)｜ == 1`**（`WS↔MLS`、`MLS↔MS`、`MS↔MCU`、`MCU↔CU`）。凡寫 `MS→CU`（`Δrank == 2`）於 `i2v_first` 露臉鏡，直接由 `SCALE_JUMP_BAN`（同步升級至抓 `Δrank >= 2`）**硬駁回**！
     - **跨幅景別切換（Cut Across Scales）**：`MS → CU` 或 `MS → ECU` 的強烈視覺對比，一律透過 **切至下一顆獨立原子鏡**（遵循 AMD-04 Path A `derived_shot` 首幀衍生）達成——這是標準電影剪輯語法，同時 100% 避開 I2V 變臉魔咒。
   - **正效應**：新增 `CU`/`ECU` 原子鏡後，原本在 `MS` 被 `SCALE_JUMP_BAN` 封殺的 `z1_sharp_lock`、`z2_hairline_knit`、`z3_jaw_clench` 微表情詞條全面合法解鎖！

2. **與 `V1_DURATION_ENVELOPE` 的協同修訂**：
   - **上限不變**：V1 所有引擎之產線品質帽與 L4 穩態上限（`LTX ≤2.5s`、`H3 L3 ≤5.0s gen`、`H3 4-ref ≤6.5s gen`〔為品質抗漂移與 L4 穩態產線品質帽，非 H3 15s 模型物理上限〕、`Wan ≤6.0s gen`、`Flow ≤7.5s gen`）100% 保留；短劇快節奏把單鏡往短拉，反而讓成片穩落引擎最高良率窗。
   - **下限 `WARN` 必須校準**：現行 `preflight_gate.py` §1420 寫 `if gen_sec < 3.0 and shot_size != "INSERT" and angle_h != "reverse": WARN`。在 Schema 2.4 快節奏下，此行改為（**註：僅豁免剪輯淨長，H3 生成端仍依 `H3_MIN_DURATION` 自動墊至 `≥4.0s (107f)` 再於 Stage 6A 裁切**）：
     ```python
     is_short_coverage_ok = (
         flags["is_insert"]
         or flags["is_reverse"]
         or shot_size == "ECU"
         or coverage_role in {"insert_detail", "reaction", "turn_jolt"}
     )
     if gen_sec < 2.0 or (gen_sec < 3.0 and not is_short_coverage_ok):
         # emit WARN [V1_DURATION_ENVELOPE]
     ```
     *(註：API 端如 Flow 最低計費步階為 `3s`/`4s`，於 `edit_manifest.json` 依 `target_net_sec` 精準裁切即可，不會誤發 preflight 假警報。)*

3. **與 `V2`（對白速率）的協同原則**：
   - **永不為了衝短 ASL 而硬壓對白秒數去撞 V2**（純字 `≤5.0`／含標點 `≤5.5 字/秒`）。
   - 正確解法是 **「音軌不斷、畫面切開（J/L-cut + `audio_groups[]`）」**：將 `5.0s` 連續對白拆為 `speaker CU (3.2s)` ＋ `listener CU / prop ECU (1.8s)`，V2 依連續 `audio_group_id` 總可用時長核算（寬鬆 PASS），同時視覺 ASL 從 `5.0s` 驟降至 `2.5s`！

### 4.3 `preflight_gate.py --selftest` 新增 14 組單元測試（`32 → 46` 條）

| Test ID | 測試情境 | 預期結果 |
| :---: | :--- | :--- |
| **T33** | 完整合規 Schema 2.4 封包（對照重排版 DEMO-02 11 鏡） | `PASS (0 FAIL, 0 WARN)` |
| **T34** | 舊 `DEMO02_v2` 風格（6 鏡、3 連 MS、無 ECU、5.08s 靜鏡）標為 `2.4` | `FAIL`（命中 `SCALE_STAGNATION` + `DETAIL_CADENCE` + `DEAD_AIR`） |
| **T35** | 1 鏡 `4.0s` 微場段（冷開場） | `PASS`（`COVERAGE_SCALE_VARIETY` 正確豁免，零誤殺） |
| **T36** | `emotional_peak=true` 配 `shot_size="MS"`（未推至 CU） | `FAIL [COVERAGE_PEAK_CLOSEUP]` |
| **T37** | (a) 3 連非反打 `MS`；(b) 3 連 `is_reverse=true` `CU` | (a) `FAIL [COVERAGE_SCALE_STAGNATION]`；(b) `PASS` |
| **T38** | 無對白 `4.5s` `MS`：(a) `static`；(b) `end_shot_size="MCU"` (`Δ=1`)；(c) `end_shot_size="CU"` (`Δ=2`, `i2v_first`) | (a) `FAIL [NON_DIALOGUE_CAP]`；(b) `PASS`；(c) `FAIL [SCALE_JUMP_BAN]` |
| **T39** | 無對白 `4.2s` `CU` 配 `deliberate_hold=true` + `hold_justification="dread"` + `push-in` | `PASS` |
| **T40** | 雙說話者場段全為 `is_two_shot=true` 無 OTS／無單人 CU | `FAIL [COVERAGE_TWO_PERSON_DIALOGUE]` |
| **T41** | 4 鏡場段全為 `movement.type="static"`（無 L4 運鏡） | `FAIL [COVERAGE_SEGMENT_KINETIC]` |
| **T42** | (a) Schema 2.4 缺 `movement.motivation`；(b) `handheld_anxiety` 配 `power_lock` | (a) `FAIL [COVERAGE_MOVE_MOTIVATION]`；(b) `WARN [COVERAGE_MOVE_MOTIVATION]` |
| **T43** | `hook` 場段 `3.0s` `static` 無 VFX／無 `internal_event_sec` | `FAIL [COVERAGE_DEAD_AIR]` |
| **T44** | (a) 3 連 `ECU` 於 `confrontation`；(b) 5 鏡中 3 顆 `ECU` (`60%`) | (a) & (b) 皆 `FAIL [COVERAGE_ECU_RATIONING]` |
| **T45** | (a) `is_reverse=true` 雙方皆 `subject_facing="left"`；(b) 同角連鏡無觸發詞翻向 `left→right` | (a) `FAIL [COVERAGE_AXIS_DISCIPLINE]`；(b) `WARN [COVERAGE_AXIS_DISCIPLINE]` |
| **T46** | `1.2s` `ECU` `is_insert=true` `trim_policy="tail_only"`（`gen_sec=1.7s` 或 `2.5s`） | `PASS`（不誤觸 `V1_DURATION_ENVELOPE` 短鏡 WARN） |

### 4.4 QC-D 導演檢核閘增補條款（覆蓋 Advisory 餘項，不破壞 6 鍵結構）

沿用 Spec §B.5 六檢結構（避免打斷既有的 `qc_d_review` 6 鍵 JSON），將第 ③ 檢「鏡頭多元」正式升格為 **「③ 鏡頭覆蓋與短劇節奏（Coverage & Short-Video Pacing）」**，下掛四項強制人工確認子句（Muse 逐條寫「過／不過＋一句證據」，Creator 終審）：

- **③a 景別弧線與峰值對位（R6）**：本段景別變化是否隨情緒／資訊形成明確弧線（抵達／對峙／揭露／收束），而非隨機切景別？情緒峰值是否真的落在最緊的 `CU`/`ECU`？
- **③b 短劇張力與首 3 秒留存（R7 / §2b）**：靜音觀看前 1.5–3 秒是否立刻出現視覺變故？全段有無「拖戲死氣」或等長節拍器感？每顆 `> 3.5s` 的長鏡是否真的在累積壓迫／情緒（而非單純等台詞唸完）？
- **③c 反應切點與細節克制（R2 / R8）**：雙人戲是否切在聽者微反應與手／眼細節，而非對著講話者念稿？`ECU` 是否克制且精準落於轉折拍點？
- **③d 180° 軸線與視線連貫（R9）**：跨切點（對照 `qcd_cut_boundaries.jpg`）人物視線方向與左右空間關係是否自然銜接，無無故跳軸或轉向突兀？

---

## 5. 可直接貼入規格之修訂草案（建議定為 **新附錄 D**）

### 5.1 架構落點論證：為何獨立為「附錄 D」優於塞進附錄 B？

1. **職責邊界清晰，對齊既有 A/B/C 分層**：
   - **附錄 A**＝運鏡執行與引擎方言（**怎麼動**，L1–L4、`movement`、`named_shots`）；
   - **附錄 B**＝導演美學意圖與表演（**演什麼感覺**，光線鎖、`performance_beat`、微表情、`camera_psychology`、QC-D）；
   - **附錄 C**＝生產管線契約與硬閘（**怎麼防崩**，AMD-01..07、QC-1/2、AMD-05）；
   - **附錄 D（本案）**＝鏡頭覆蓋文法、短劇節奏配額與張力規則（**怎麼切、切多快、幾秒切什麼景別**）。
2. **低侵入維護**：正文僅需於 **§3.B**（補 `framing_flags`、`movement.motivation`、`coverage_role`、`emotional_peak`）、**§6.1**（增列 `V14 鏡頭覆蓋與短劇節奏閘`）、**§9.2 #1**（明示 Demo 不可跳過 Stage 0.5 覆蓋表）與 **§B.1／§B.5** 加 4 處單行指標連結，其餘完整規格獨立置於附錄 D，供 Muse 填覆蓋表與 `preflight_gate.py` 對照實作，不膨脹附錄 B。

---

### 5.2 可直接貼入 `STORYBOARD-SPEC-V2.md`（升 **v2.4**）之完整規格文本

> 以下文字格式、符號（`●`／`○`／`◐`）與術語 100% 對齊 `STORYBOARD-SPEC-V2.md` 現有風格，待 Creator 拍板後 Muse 可直接合併。

#### 【正文四處短連結修補】

1. **§二 場段層 `segments[]` 增補三欄**：
   - `segment_pacing_profile` ●（v2.4）：`hook`／`escalation`／`confrontation`／`revelation`／`climax`／`release_bridge`／`chase_tension`（對接附錄 D.2 節奏帶）。
   - `axis_plan` ◐（v2.4，≥2 人物鏡段必填）：`{char_id: {screen_side, default_facing}}`（180° 軸線鎖，配 R9）。
   - `target_shot_density_per_10s` ○：`[min, max]` 覆寫段級預設節奏帶。
2. **§三.B 攝影層修訂與增補**：
   - `shot_size` ●（v2.4 純距離枚舉）：`WS`／`MLS`／`MS`／`MCU`／`CU`／`ECU`／`CARD`（向下相容 2.0–2.3：`ELS`/`LS`→`WS`、`2S`→`MS`+`is_two_shot`、`OTS`→`MCU`+`is_ots`、`INSERT`→`ECU`+`is_insert`）。
   - `framing_flags` ○（v2.4）：`{is_ots, is_reverse, is_two_shot, is_insert}`（未填預設全 `false`）。
   - `movement` ●：擴充必填子欄 **`motivation`**（6 枚舉，見附錄 D.1.2）。
   - `coverage_role` ●（v2.4）：`establish`／`action`／`speaker`／`reaction`／`insert_detail`／`turn_jolt`／`peak_hold`／`card_evidence`；`emotional_peak` ●（bool）；`dialogue_mode` ●（`none`/`on_camera`/`off_camera`/`voiceover`/`l_cut_carry`）；`screen_side` ◐（`left`/`center`/`right`）；`axis_turn_trigger` ○；`internal_event_sec` ○（`float[]`）；`hold_justification` ◐（`dread`/`peak_emotion`/`held_reaction`）。
3. **§6.1 硬閘總表增補一行**：
   - **V14 鏡頭覆蓋與短劇節奏閘（v2.4，附錄 D）**：`COVERAGE_SCALE_VARIETY`（R1a）、`COVERAGE_PEAK_CLOSEUP`（R1b）、`COVERAGE_SCALE_STAGNATION`（R1c，取代舊 V12d 弱檢）、`COVERAGE_DETAIL_CADENCE`（R2）、`COVERAGE_NON_DIALOGUE_CAP`（R3，與 `SCALE_JUMP_BAN` 聯檢限 Δrank=1）、`COVERAGE_TWO_PERSON_DIALOGUE`（R4）、`COVERAGE_SEGMENT_KINETIC`／`COVERAGE_MOVE_MOTIVATION`（R5a/b，擴充 V12e）、`COVERAGE_DEAD_AIR`（無死氣上限）、`COVERAGE_ECU_RATIONING`（R8）、`COVERAGE_AXIS_DISCIPLINE`（R9）；另有 Advisory `COVERAGE_PACE_ENVELOPE`（R7）。
4. **§9.2 Demo 永不可跳 #1 補句** 與 **§B.1／§B.5 連結**：
   - §9.2 #1：「…Stage 0.5 雖可省去長散文，但**逐鏡覆蓋表（附錄 D.1）與結構化覆蓋欄位永不可跳過**，並須通過 V14 覆蓋硬閘。」
   - §B.5 #3：「**③ 鏡頭覆蓋與短劇節奏**（詳見附錄 D.5 QC-D 四項子檢）。」

---

#### 【新增附錄 D 全文（Paste-Ready）】

```markdown
---

# 附錄 D：導演鏡頭覆蓋與豎屏短劇節奏規格（v2.4 新增）

> **立法目的**：在導演層（Stage 0.5）與前置閘門（QC-0）把「景別覆蓋、鏡數密度、單鏡秒數與豎屏高張力節奏」從口頭散文升格為可驗證數據契約，根除「技術全過、但全段平緩中景缺特寫」的失格成片；同時嚴守引擎物理邊界（`SCALE_JUMP_BAN`、V1/V2）與成本紀律。

## D.1 Stage 0.5 逐鏡覆蓋表契約（數據優先，Demo／快線不可跳過）

每場段於 Stage 0.5 `DIRECTOR_STATEMENT.md` 必附 **逐鏡覆蓋表**，並於 Stage 1 1:1 映射入 `script_pack.json`（schema 2.4）：
- **場段級必填**：`segment_pacing_profile`（`hook`／`escalation`／`confrontation`／`revelation`／`climax`／`release_bridge`／`chase_tension`）與 `axis_plan`（≥2 人物鏡段鎖定各角色 `screen_side` 與 `default_facing`）。
- **鏡級核心欄**：`shot_size`（純距離 6 級：`WS(1) < MLS(2) < MS(3) < MCU(4) < CU(5) < ECU(6)` ＋ `CARD(0)`）、`framing_flags`（`{is_ots, is_reverse, is_two_shot, is_insert}`）、`movement.named_shot`、`target_net_sec`、`movement.{type,speed,amplitude,end_shot_size,motivation}`、`camera_psychology`、`coverage_role`、`emotional_peak`、`dialogue_mode`、`lip_sensitive`、`screen_side`、`internal_event_sec[]`、`hold_justification`。

### D.1.1 運鏡動機受控詞表 `movement.motivation`（與 `camera_psychology` 聯動）

| `motivation` | 導演功能 | 合法 `camera_psychology` |
|---|---|---|
| `emotional_intensify` | 情緒加壓、逼近心理轉折 | `intimate_drift` / `stable_control` / `predator_stalk` |
| `spatial_reveal` | 揭露環境因果、目擊者或威脅 | `cold_observe` / `predator_stalk` / `handheld_anxiety` |
| `subjective_instability` | 失重墜落、警戒晃動、主觀焦慮 | `handheld_anxiety` / `subjective_pov` |
| `action_follow` | 跟隨身體動量或視線引導 | `handheld_anxiety` / `predator_stalk` / `subjective_pov` |
| `power_lock` | 刻意定鏡或極緩推建立威壓自制 | `stable_control` / `cold_observe` |
| `rhythm_jolt` | 拍點反轉衝擊、模式中斷（常配 L4 急推／甩切） | `handheld_anxiety` / `predator_stalk` / `intimate_drift` |

## D.2 豎屏短劇節奏帶與景別時長基準

| `segment_pacing_profile` | 目標 ASL | 每 10 秒鏡數 | 無對白上限（R3） | 無死氣軟／硬上限 |
|---|---:|---:|---:|---:|
| `hook`（0–5s 開場鉤） | `1.5–2.2s` | `4.5–6.5` | `3.5s` | `2.0s` / `2.5s` |
| `chase_tension`（高危動作） | `1.4–2.2s` | `4.5–7.0` | `3.0s` | `1.8s` / `2.5s` |
| `climax`（高潮／集尾） | `1.8–2.6s` | `3.8–5.5` | `3.5s` | `2.0s` / `2.5s` |
| `escalation`（加壓升溫） | `2.0–2.8s` | `3.5–5.0` | `3.5s` | `2.5s` / `3.5s` |
| `confrontation`（雙人交鋒） | `2.2–3.0s` | `3.3–4.5` | `4.0s` | `2.5s` / `3.5s` |
| `revelation`（揭露／回顧） | `2.4–3.2s` | `3.1–4.2` | `4.0s` | `3.0s` / `4.0s` |
| `release_bridge`（短暫呼吸） | `2.8–3.8s` | `2.6–3.5` | `4.0s` | `3.5s` / `4.5s` |

- **景別建議淨長**：`ECU` `1.0–2.0s`（絕對 `0.8–2.5s`）；`CU` 無對白反應 `1.2–2.5s`、對白／峰值 `2.5–4.8s`（守 V1/V2）；`MCU` `2.0–4.0s`；`MS` `2.0–3.5s`；`MLS` `1.8–3.0s`；`WS` 定場 **`≤ 2.5s`**（跨 1 級推進 ≤4.0s）；`CARD` `1.5–3.0s`。
- **長停頓紀律（香料非預設）**：`> 3.5s` 單鏡僅限承載 `peak_emotion`、`dread_compression` 或 `held_reaction`（須填 `hold_justification`），前後至少一側須配 `≤ 2.0s` 快切形成速度反差，嚴禁連播兩顆 `> 3.5s` 靜止鏡。
- **無死氣原則（No-Dead-Air）**：凡 `movement.type == "static"` 且無 `vfx_beats[]`／無 `visual_text_overlay[]` 之鏡，其相鄰 `internal_event_sec[]` 間隔不得逾上表「無死氣硬上限」。

## D.3 V14 鏡頭覆蓋規則（HARD 硬閘 vs ADVISORY 軟檢）

1. **R1a 景別多元（HARD：`COVERAGE_SCALE_VARIETY`）**：非卡長 `≥ 8.0s` 或非卡鏡 `≥ 4` 之場段，須含 **≥ 3 種相異 `shot_size`** 且 **≥ 1 顆 `CU`/`ECU`**（≤2 鏡/<6s 微場段與 `release_bridge` 豁免）。
2. **R1b 情緒峰值特寫（HARD：`COVERAGE_PEAK_CLOSEUP`）**：非橋接段 `≥ 8.0s` 必標 ≥1 顆 `emotional_peak: true`，且該鏡必為 `CU`/`ECU` 或 `MCU→CU`（Δrank=1）。
3. **R1c 禁同尺幅停滯（HARD：`COVERAGE_SCALE_STAGNATION`）**：非反打不可連 `> 2` 鏡同 `SCALE_RANK`；正反打對切連 4 鏡發 `WARN`、連 `> 4` 鏡無 `monotony_exempt_reason` 發 `FAIL`。
4. **R2 細節切鏡節奏（HARD 高張力段／WARN 其餘：`COVERAGE_DETAIL_CADENCE`）**：任一連續 `≥ 10.0s` 非卡滑窗內至少 1 顆 `CU`/`ECU`；段長 `≥ 12.0s` 者每 `12.0s` 至少 1 顆非對白細節／反應 `CU`/`ECU`（`is_insert` 或 `coverage_role ∈ {insert_detail, reaction}`）。
5. **R3 無對白鏡長上限（HARD：`COVERAGE_NON_DIALOGUE_CAP`）**：無對白非卡鏡須 `≤ 3.5s`（高張力段）或 `≤ 4.0s`（一般段）；僅於 **鏡內跨恰好 1 級相鄰尺幅**（`Δrank == 1`，≤5.0s）或 **`deliberate_hold=true`＋`hold_justification`**（≤4.5s）得展延。**嚴禁以 `Δrank ≥ 2`（如 `MS→CU`）推臉繞過（由 `SCALE_JUMP_BAN` 硬駁回）；跨多級必拆原子鏡切鏡**。
6. **R4 雙人對白反打（HARD：`COVERAGE_TWO_PERSON_DIALOGUE`）**：段內 `≥ 2` 說話者且 `≥ 2` 輪次，必含 ≥1 顆 `is_ots`/`is_reverse`、≥1 顆單人 `CU`/`MCU`，且不可連 `> 1` 顆有對白 `is_two_shot`。
7. **R5 運鏡動能與動機（HARD：`COVERAGE_SEGMENT_KINETIC`／`COVERAGE_MOVE_MOTIVATION`）**：`≥ 3` 顆非卡鏡段禁 100% 靜鏡（高張力段主動運鏡 `< 50%` 發 `WARN`）；每鏡必填 `movement.motivation`，與 `camera_psychology` 衝突發 `WARN`。
8. **R6 景別弧線模板（ADVISORY｜QC-D #3a）**：依場段選用對應弧線——抵達（`WS/MLS→ECU→MCU→MS 2S→OTS/CU`）、對峙（`MS/2S≤2.5s→OTS MCU→反打 CU→ECU 中斷→緊 CU`）、揭露（`MCU→ECU/CARD 證據→CU 反應`）、懸念收束（`MS→MCU→慢推 CU→ECU 異變→黑`）、追逐（`MLS→連切 ECU→手持 MS→L4 甩切→CU`）。
9. **R7 單集節奏曲線與反節拍器（ADVISORY：`COVERAGE_PACE_ENVELOPE`）**：對齊 60–100s 五段曲線（開場與高潮最密、高潮配 1 顆對比峰值停頓、集尾急煞）；全集鏡長變異係數 `CV < 0.25` 發 `WARN`。
10. **R8 `ECU` 配給紀律（HARD >40% 或連切 >2／WARN >30% 鏡數或 >20% 時長：`COVERAGE_ECU_RATIONING`）**：節制使用以保衝擊力（`chase_tension` 連切放寬至 ≤3）；有臉 `ECU` 保留予 `TURN`/`JOLT`/`CLIFF`/`emotional_peak`。
11. **R9 180° 軸線與視線紀律（HARD 反打同向／WARN 無因翻向：`COVERAGE_AXIS_DISCIPLINE`）**：`is_reverse=true` 與所回應前鏡之 `subject_facing` 必相向；同角連鏡左右翻轉須明示 `axis_turn_trigger`。

## D.4 與 V1／V2／`SCALE_JUMP_BAN` 及成本紀律的組合

1. **短插鏡 V1 豁免**：`is_insert`/`is_reverse`/`ECU`/`reaction`/`turn_jolt` 鏡頭生成長落於 `2.0–3.0s`（或 `trim_policy: "tail_only"`）不觸發 `V1_DURATION_ENVELOPE` 短鏡 `WARN`。
2. **長台詞用 L-cut 降 ASL，禁硬壓 V2**：超過 `3.5s` 之對白優先以 `audio_groups[]` 走 L-cut 切入 `1.2–1.8s` 聽者反應或無臉細節插鏡，兼顧 V2 語速與豎屏快節奏。
3. **成本感知買密度**：新增節奏鏡優先配發 **無正臉 `ECU` 插鏡（Flow `3s tail_only` 或 Wan 2.2）**、**`cpu_card`（0 成本）**、**L4 剪輯接點特效（甩鏡／急推／微推／補抖）**與**同片雙切反應回收**，嚴控 `H3-4Ref` 對白 CU 總鏡數不膨脹。

## D.5 QC-D 第 ③ 檢細化（鏡頭覆蓋與短劇節奏）

Stage 6A 粗剪後於 QC-D 第 ③ 檢逐一確認（過／不過＋一句證據）：
- **③a 景別弧線**：景別變化服務情緒遞進，峰值穩落最緊 `CU`/`ECU`；
- **③b 豎屏張力**：前 1.5–3s 靜音即有視覺變故，無空轉死氣與機械等長感，長停頓皆具明確張力動機；
- **③c 反應與細節**：切在聽者反應與手／眼細節，非純盯說話者念稿；`ECU` 節制打在轉折拍點；
- **③d 軸線視線**：跨切視線與左右空間自然連貫，無無故跳軸。
```

---

## 6. 決策收斂點（供 Muse 與 Creator 拍板後進入實作）

1. **落點確認**：是否同意將本案作為 **Spec v2.4 新附錄 D**（正文僅 4 處單行掛鉤），並將 Stage 0.5 逐鏡覆蓋表列入 §9.2 **Demo／快線永不可跳清單**？
2. **R3 × `SCALE_JUMP_BAN` 定案**：是否同意駁回「單鏡內 `MS→CU` 跨兩級推臉」並改為「**鏡內推進硬限 Δrank=1；跨多級必拆原子鏡切鏡**」？
3. **EP-01 覆蓋升版路徑**：是否同意在 **不改劇本台詞一字** 的前提下，於 Stage 1 鑄造 `EP-01` `script_pack.json`（v2.4）時直接套用 §3.2 方案（`29 → 42` 原子鏡，ASL `3.52s → 2.35s`，`0` 新增 H3-4Ref，6 顆無臉細節插鏡交 Wan 2.2／Flow `tail_only` 控費）？
4. **下一步工程落地（拍板後才啟動）**：① 更新 `STORYBOARD-SPEC-V2.md` 至 v2.4；② 建檔 `bible/camera/named_shots.yaml`（18 受控鏡型，全標實測狀態）；③ 升級 `tools/preflight_gate.py` 納入 V14 全部 12 條覆蓋規則＋14 條 selftest（`32 → 46` PASS）。
