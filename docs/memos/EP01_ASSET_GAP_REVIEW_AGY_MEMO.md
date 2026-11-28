# EP-01 資產補齊清單 — 工程規格審查備忘錄（AGY REVIEW MEMO）

> **文件狀態**：DISCUSSION & DESIGN REVIEW ONLY（2026-11-28｜agy on `workhorse-90d`｜**零生成、零點數／CU／TTS 消耗、零 repo push、零檔案搬移**）  
> **受審對象**：`~/drama-line/EP01-ASSET-GAP-LIST.md`（v1，Muse 彙整）  
> **交叉核對基準**：`ASSETS_MANIFEST.yaml`（14 條實查）＋ `EP01_PRODUCTION_WORKFLOW.md`（29 顆原子鏡）＋ `DEMO03_TREATMENT.md` ＋ `AMD05_V3_AGY_MEMO.md` ＋ `DRYRUN-EP01-arrival-v0.3.2.md` ＋ v0.3.3 異動（新增 `S00` 夜行按劍：`LOC-TAIHU-NIGHT`＋`PROP-SWORD-01`；`S01` 湖上鏡保留）＋ `COSTUME_REGISTRY.md` ＋ `bible/anchors/FANLI.yaml` ＋ `tools/preflight_gate.py`／`tools/diff_sheet_gen.py` 實碼 ＋ `casting/master/` 磁碟實況。

---

## 0. 總體審查裁決（Verdict by Checklist Section）

Muse 的 v1 清單架構正確（分層、一物一 ID、QC-1 鎖定、不將二進位入 git），但在**跨檔實碼對照**與 **AMD-05 v2→v3 切換點**上存在 **5 處缺漏、3 處規格漂移／命名分歧、1 處手性／連戲陷阱**。逐節裁決如下：

| 清單章節 | 裁決 | 核心理由與必要修訂 |
| :--- | :---: | :--- |
| **A. 道具層（`props` 段）** | **AMEND** | ① 採納 `PROP-{TYPE}-{NN}` 編號體系（覆蓋 `EP01_PRODUCTION_WORKFLOW.md` 舊名 `PROP-YUE-SWORD`／`PROP-BAMBOO-SCROLL`）；② **`PROP-SWORD-01` 須錨定已鎖定之 `fanli-outfit03-45.jpg` 既有越劍**，並修正左腰佩劍之「按劍 vs 出鞘一寸」手性機構（詳 §2.1、§3）；③ `PROP-COIN-01` 維持 P2（EP-01 **0 鏡使用**），但加註 **V9 紅線**：禁裁切 `fanli-modern-charactercard-expressions.png` R2C2（該格錢面有可辨偽字 `通寶`）。 |
| **B. 場景層（LOC 卡）** | **AMEND** | ① **拆分 `LOC-YUE-COURT` 與 `LOC-WENZHONG-GATE`**（原表混併進單一 ID，違背「一物一 ID」並破壞 `S14b`/`S15a` AMD-04 衍生規則）；② 明列常駐景 **`LOC-FANLI-STUDIO-26` 三角度母圖組**（`_desk`/`_window`/`_tabletop`，服侍 12 鏡）與 **`LOC-TAIPEI-STREET-2022` 反打角（`_rev`）**；③ 確認其餘 4 景（`LOC-TAIHU-NIGHT`、`LOC-TAIHU-DAWN`、`LOC-FANLI-STUDIO-26`、`LOC-TAIPEI-STREET-2022`）與已鎖 `LOC-ALLEY-NIGHT` 無重複。 |
| **C. 人物與錨點補完** | **AMEND** | ① **補回重大遺漏（EP-01 Stage 1 阻斷項）**：**`FANLI-OUTFIT-01` 現代單視圖 4 槽母圖組**（CPU 裁切 `cu`＋`45L` ＋ 新產 1 張無疤 `45R`，供 EP-01 7 顆現代 H3 對白鏡）；② **移除「去背」字樣（AMD-05 v2→v3 漂移）**：`SYS-01` 單視圖 refs 改為「**純 CPU 無損矩形裁切（保留乾淨灰棚底、不跑 BiRefNet 去背）**」；③ 大媽定妝＋聲線改為**條件優先級**（跑 DEMO-03 則聲線為 `P0-DEMO03`、視覺沿用 `demo02_v2/frames/S2_first.jpg` 零新圖；跳過 DEMO-03 走街頭版則降為 `DROP/P2`）；④ `OUTFIT-03` 疤修正維持 P2（不擋 EP-01 `S13` 中景）。 |
| **D. 聲音資產** | **AMEND** | ① **`SYS01-VOICE` 拆細優先級**：不擋 `SM-8` 與 `DEMO-03`（DEMO 沿用 `demo01/audio/sys.mp3`），為 **EP-01 Stage 1.5 硬阻斷（`P0-EP01`）**；② **Roomtone 實為「1 既有多用 ＋ 5 條新增」而非 ×4**：`alley_night_wet_48k.wav` 已存在於 `demo02_v2/audio_lib/roomtone/`；Muse 清單**漏列 2 條**——**`taihu_night_reed_48k`（v0.3.3 `S00` 夜岸蘆葦水聲）**與 **`taipei_street_crowd_48k`（`S02–S04c` 2022 台北街頭）**；③ 補列關鍵 CPU/CC0 Foley（`S00` 劍出鞘一寸微擦聲、DEMO-03 空間吸扯／路燈電流／塑膠袋摩擦）。 |
| **E. 登記與衛生** | **AMEND** | ① **`SYS-01` manifest 備註更新須嚴格鎖定時機**：**先過 `SM-8`＋Spec v2.4 正式併入後再一次同步切換**，切勿於驗證前搶改造成規格腦裂（詳 §6.1）；② **`casting/master/` 清理名單漏列 2 個禁用殘留檔**：除 6 個 `tmp_*` 外，尚有 `fanli-master-ancient-45R.v1-flip-defect.jpg`（明令禁用缺陷版）與 `fanli-master-B.jpg`（Seedream 棄用臉），建議一併按「只移不刪」移出 `master/`（詳 §6.2）；③ 修正既有 manifest 中 `FANLI-VOICE-F` 路徑筆誤（寫 `bible/voices/FANLI.yaml`，VM 實存 `voices/FANLI.yaml`）。 |

---

## 1. 完整性總清查（Completeness Sweep）

### 1.1 逐鏡對照（EP-01 29 原子鏡 ＋ v0.3.3 `S00` ＋ DEMO-03）

| 鏡段／專案 | 鏡號範圍 | 所需資產（LOC / PROP / CHAR / AUDIO） | 現況與缺口檢定 |
| :--- | :--- | :--- | :--- |
| **SM-8（AMD-05 v3 門票）** | 單鏡 4s 驗證 | `LOC-ALLEY-NIGHT`（已鎖）＋ `OUTFIT-02`（`45R`/`45` 已鎖）＋ `sys01-ref-34L-smile.png`（CPU 裁切） | **0 新產場／道具**；只需 CPU 裁圖＋`SYS01.yaml` |
| **DEMO-03（若獨立跑）** | `S0`, `S1a`, `S1b`, `S2_new`, `S3a`, `S3b`, `S2R_new`, `S4` | `LOC-ALLEY-NIGHT`（已鎖）、**`LOC-TAIHU-DAWN`（缺）**、`OUTFIT-02`（已鎖）、`S2_first.jpg` 婦人延用、**`WITNESS-DEMO03-VOICE` 或 10s 真人乾錄（缺）**、`alley_night_wet_48k`（已有）、**`taihu_dawn_water_48k`（缺）** | 僅缺 `LOC-TAIHU-DAWN`、婦人聲音與太湖晨霧底噪 |
| **EP-01 v0.3.3 新增段** | **`S00`**（夜行按劍／出鞘一寸） | **`LOC-TAIHU-NIGHT`（缺，P0）**、**`PROP-SWORD-01`（缺，P0）**、`OUTFIT-02`（已鎖）、**`taihu_night_reed_48k`（缺，Muse 漏列！）**＋出鞘 Foley | 補列 `taihu_night_reed_48k`；劍型須與 `OUTFIT-03` 協調 |
| **SEG-01** | `S01` | **`LOC-TAIHU-DAWN`（缺，P0）**、`OUTFIT-02`（已鎖）、**`taihu_dawn_water_48k`（缺）** | 與 DEMO-03 `S0` 及 `S16b` 共用 |
| **SEG-02** | `S02`–`S04c`（6 鏡） | **`LOC-TAIPEI-STREET-2022` ＋ `_rev`（缺，P1）**、`OUTFIT-02`（已鎖）、`sys01-ref-34L-smile`（CPU 裁）、**`SYS01-VOICE`（缺，P0-EP01）**、**`taipei_street_crowd_48k`（缺，Muse 漏列！）** | 注意：2022 著 `OUTFIT-02` 仍硬禁方孔錢與腕錶 |
| **SEG-03 & SEG-05** | `S05`–`S12`、`S17a`–`S20`（14 鏡，含 3 CPU 卡） | **`LOC-FANLI-STUDIO-26` 三角度（缺，P0）**、**`FANLI-OUTFIT-01` 單視圖組（`cu`/`45L` CPU 裁 ＋ `45R` 新產，Muse 遺漏！）**、`sys01-ref-front`/`34L-neutral`/`R1C1`/`R1C5`（CPU 裁）、`FANLI-VOICE-F`（已鎖）、`SYS01-VOICE`、**`studio_night_hum_48k`（缺）** | **重大遺漏捕獲**：7 顆現代 H3 鏡無 `OUTFIT-01` `45R` 無疤單視圖必觸發 `ASSET_CONTRACT` 或錯邊疤！ |
| **SEG-04** | `S13`–`S16b`（7 鏡） | **`LOC-YUE-COURT`（缺，P1）**、**`LOC-WENZHONG-GATE`（Muse 漏拆，P1）**、`LOC-TAIHU-DAWN`、`OUTFIT-03`/`02`（已鎖）、**`PROP-BAMBOO-01`（缺，P1）**、**`PROP-SWORD-01` 或 `PROP-SWORD-02`（S16a，見 §3）**、**`GOUJIAN-VOICE`／`WENZHONG-VOICE`（缺，P1）**、**`ancient_hall_torch_48k`（缺）** | 拆出 `LOC-WENZHONG-GATE`；`S14a/b`、`S15a/b`、`S16a` 皆 `face_visible=false` |

### 1.2 遺漏、過度列項與 ID 衝突盤點

1. **五項實質遺漏（MUST ADD）**：
   - **`FANLI-OUTFIT-01` 單視圖 4 槽母圖組（P1，擋 EP-01 Stage 1）**：`EP01_PRODUCTION_WORKFLOW.md` §3 已明列，Muse 清單漏抄。現有 `fanli-master-B-userface.png` 傷痕鏡像、`fanli-master-B-45.jpg` 手持方孔錢（空手鏡污染風險）、`fanli-modern-charactercard-*.png` 屬多格卡被 `preflight_gate.py` L1017 硬攔；**必須 CPU 裁出 `fanli-modern-ref-cu.png`、`fanli-modern-ref-45L.png`，另以 `nano2` 補 1 張無疤 `fanli-modern-ref-45R.jpg`**。
   - **`LOC-WENZHONG-GATE` 獨立建卡（P1）**：自 `LOC-YUE-COURT` 拆出，避免朝堂大殿（`S13/S14a/S15b`）與文種府門內室（`S14b/S15a`）共用同 `scene_id` 違反 AMD-04。
   - **2 條遺漏 Roomtone（P1，純 CPU/CC0）**：`taihu_night_reed_48k.wav`（v0.3.3 `S00`）與 `taipei_street_crowd_48k.wav`（`SEG-02`），加補 `S00` 出鞘微擦聲與 DEMO-03 環境 Foley。
   - **多角度 LOC 子規格**：`LOC-FANLI-STUDIO-26` 須列 3 角度（`_desk`、`_window`、`_tabletop`）；`LOC-TAIPEI-STREET-2022` 須列反打角 `_rev`。
   - **2 個未列入衛生清單之禁用殘留檔**：`casting/master/fanli-master-ancient-45R.v1-flip-defect.jpg` 與 `casting/master/fanli-master-B.jpg`（詳 §6.2）。
2. **確認無須過度開卡之靜物（DO NOT CREATE PROP CARDS）**：
   - `S06` 套房毛筆／紙本／鈔票／桌上小屏（寫入 `LOC-FANLI-STUDIO-26` 環境陳設，V9 全空白無字）；`S01`/`S16b` 小舟（寫入 `LOC-TAIHU-DAWN`）；`S02`/`S03` 現代無標手機（泛用道具，沿用 `PROPS_EP001.md` 無 Logo 規範）；DEMO-03 婦人紅白菜袋（綁定婦人外觀）。
3. **規格漂移修正（REMOVE OVER-SPEC）**：
   - Section C `SYS-01` refs 移除「**去背**」（AMD-05 v3 全面廢除 BiRefNet 去背貼片；純 CPU 矩形裁切保留淺灰棚底，避免 PNG 透明預乘黑邊）。
   - Section D `alley_night_wet_48k` 已存在，改標「既有沿用／移至共用 `audio_lib/roomtone/`」，不重複製作。
4. **ID 衝突與命名統一（對照 `ASSETS_MANIFEST.yaml` 既有 14 條與舊檔）**：
   - **零硬碰撞**：所有新 ID 均不與既有 14 條 ID 衝突。
   - **三處跨檔命名分歧須統一**：
     1. 道具 ID：`EP01_PRODUCTION_WORKFLOW.md` 寫 `PROP-YUE-SWORD`／`PROP-BAMBOO-SCROLL`；Muse 寫 `PROP-SWORD-01`／`PROP-BAMBOO-01`。**建議採納 Muse 版 `PROP-{TYPE}-{NN}`**（與 `FANLI-OUTFIT-01..04` 對齊，且預留 `PROP-SWORD-02` 空間，並與非 Canon 舊檔 `casting/props/PROPS_EP001.md` 的 `PROP-EP001-*` 區隔）。
     2. 聲線 ID：既有 manifest 用 `{CHAR}-VOICE[-TAG]`（`FANLI-VOICE-F`、`SYS01-VOICE`），Muse 寫 `VOICE-GOUJIAN`／`VOICE-WENZHONG`。**建議統一為 `GOUJIAN-VOICE`、`WENZHONG-VOICE`（及選配 `WITNESS-DEMO03-VOICE`）**，維持全表單一命名慣例。
     3. `SYS-01` vs `SYS01` 連字號：manifest 與劇本用 `SYS-01`，檔名與聲線用 `SYS01.yaml`／`SYS01-VOICE`；工具端一律以去連字號正規化比對（詳 §4.3）。

---

## 2. 道具卡（PROP）與場景卡（LOC）凍結欄位規格與 QC-1 驗收標準

比照 `COSTUME_REGISTRY.md`（一卡一 ID、凍結形制、禁則、參考圖路徑與逐張 QC 表）並對齊 `STORYBOARD-SPEC-V2.md` §二／§三.C（`asset_refs` 預設契約與 `light_lock_id`）：

### 2.1 PROP 卡凍結欄位規格（建議落地檔案：`docs/PROP_REGISTRY.md`，二進位放 `casting/props/{prop_id}/`）

```yaml
# PROP Card Frozen Schema (v1.0)
prop_id: "PROP-SWORD-01"                # 唯一 ID：PROP-{TYPE}-{NN}
name: "范蠡春秋青銅越劍"
tier: "hero"                            # hero | recurring | insert
status: "DRAFT"                         # DRAFT | CANDIDATE | LOCKED | SUPERSEDED
used_in_episodes: ["EP-01:S00", "EP-01:S13(OUTFIT-03)", "EP-01:S16a(TBD)"]
linked_outfits: ["FANLI-OUTFIT-02", "FANLI-OUTFIT-03"]  # 若已出現在鎖定服裝卡，必列為視覺基準

# 時代與禁用硬閘（可由 preflight_gate.py 自動讀入）
allowed_eras: ["春秋"]                  # 例：PROP-COIN-01 則為 ["2022", "2026"]
forbidden_eras: ["2022", "2026"]        # 例：PROP-COIN-01 則為 ["春秋"]
forbidden_outfits: ["FANLI-OUTFIT-01"]  # 例：PROP-COIN-01 禁 OUTFIT-02/03/04

# 物理與尺度規格（凍結）
dimensions_cm: "全長約 58–62 cm；劍身 46–50 cm；劍柄 10–12 cm；鞘寬 4.5–5 cm"
scale_reference: "劍柄長度約成年男子單掌寬 1.15 倍；收鞘斜佩左腰時，鞘尾止於左大腿中段，絕不拖及膝下"
materials_and_finish: "暗舊氧化青銅（零亮金／零鏡面不鏽鋼）、啞光深褐黑髹漆木鞘配舊銅劍珌與雙銅箍"
silhouette_key_parts:                   # 3–5 個跨態不變視覺點
  - "圓首素柄（錨定 fanli-outfit03-45.jpg，可選極薄暗麻細纏）"
  - "緊湊舊銅窄劍格（無大型浮雕龍虎護手）"
  - "暗啞髹漆直鞘＋舊銅劍珌"
  - "無銘文雙刃青銅劍身（菱形脊、自然氧化霧光）"

# 人體工學與握持規格（防 AI 扭手）
wear_side: "anatomical_left_hip"        # anatomical_left_hip | tabletop | handheld_only
hold_hand:
  press_or_steady: "anatomical_left_hand"   # S00 按劍／呼應 S02/S03 左手按空腰間
  draw_1inch: "left_thumb_push_guard OR two_hand_cross_draw(L-scabbard + R-hilt)"
required_states:                        # 必備參考圖狀態（皆須統一外型）
  - state: "sheathed_hip"               # 佩掛左腰全形（錨定 fanli-outfit03-45.jpg）
  - state: "hand_on_hilt_ecu"           # 左手按劍柄／護格 ECU
  - state: "unsheathed_1inch"           # 出鞘一寸特寫（露暗舊青銅刃口、零文字）

# V9 與時代禁則
forbidden_elements:
  - "任何劍身銘文、篆字、漢字、數字、浮水印（V9 硬紅線）"
  - "漢代長鐵環首刀、唐橫刀、明清龍紋護手、劍穗流蘇、亮銀不鏽鋼、亮金塗裝"
  - "現代服裝／2022–2026 場景出現實劍（僅限按空腰間）"

# Spec v2.3 §3.C.1 參照契約
asset_contract:
  role: "prop"
  default_owns: ["prop_appearance"]
  default_never_inherit: ["studio_backdrop", "source_lighting", "overlay_text"]
zh_prompt_anchor: "春秋晚期短制暗舊青銅越劍，圓首素柄、窄銅格、啞光深褐黑髹漆劍鞘配舊銅珌，無銘文無劍穗"

ref_images: []                          # LOCKED 後填入 {state, path, resolution, seed, sha256}
qc1_record: []                          # 逐張 QC-1 6 項核對表
```

#### PROP-QC-1 六項驗收門檻（6/6 PASS 方可轉 `LOCKED`）
1. **`era_accuracy`（時代考據）**：春秋晚期器物形制正確（劍＝短青銅劍非漢唐長刀或仙俠劍；竹簡＝素竹麻繩非線裝書；方孔錢＝嚴守現代線專用、春秋全禁）。
2. **`scale_and_proportion`（人體尺度）**：與手掌／腰胯比例合理（劍柄 ~1.15 掌寬；方孔錢 3.8–4.5 cm 非掌心大銅盤；竹簡片寬 ~1 cm）。
3. **`handedness_and_wear_side`（手性與佩掛位）**：左腰斜向後下佩掛、按劍手／執幣手解剖正確，**零六指、零反腕扭曲**。
4. **`state_completeness`（多態一致）**：同卡所有 `required_states` 參考圖（如越劍三態、竹簡二態）的圓首、劍格、鞘色／竹色 100% 連貫，不出現「換了一把劍」。
5. **`v9_zero_text`（V9 零字紅線 — 一票否決）**：2.5× 放大檢視劍身、簡面、錢面、背景，**出現任一可辨字符、擬古偽篆或標誌即 FAIL**（特別防範 `PROP-COIN-01` 錢面長字與 `PROP-BAMBOO-01` 亂碼墨字）。
6. **`material_lighting_neutrality`（棚光中性）**：中性均勻漫射棚光、無重度偏色或強反光高光（確保餵圖時 `never_inherit: source_lighting` 不汙染實拍光線鎖）。

---

### 2.2 LOC 卡凍結欄位規格（建議落地檔案：`docs/LOCATION_REGISTRY.md`，二進位放 `casting/scenes/{loc_id}/`）

```yaml
# LOC Card Frozen Schema (v1.0)
loc_id: "LOC-FANLI-STUDIO-26"           # 唯一 ID：LOC-{PLACE}-{TIME/ERA}
name: "范蠡 2026 台北深夜小套房"
time_layer: "2026"                      # 春秋 | 2022 | 2026
recurrence: "series_hq"                 # series_hq | multi_episode | single_episode
status: "DRAFT"                         # DRAFT | CANDIDATE | LOCKED | SUPERSEDED
used_in_episodes: ["EP-01:S06-S12", "EP-01:S17a-S19"]

# 光線鎖與色度遙測基準（直連 Spec §二 segments[] 與 diff_sheet_gen.py）
light_lock_id: "LK-STUDIO-NIGHT26"      # 例：LK-TAIHU-NIGHT / LK-TAIHU-MIST / LK-TAIPEI-DUSK22 / LK-COURT-TORCH
key_light_spec: "室內桌面偏冷低照度檯燈（4800–5200K，壓暗周圍牆面）＋右後方大窗透入都會巨幕偏冷青散焦反光（6000–6500K）"
target_lab_range:                       # LOCKED 時實測回寫，作為同段 dL_seg / db_seg 錨點
  bg_L_range: [10.0, 24.0]
  bg_b_range: [-8.0, 1.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["暗炭黑室內牆", "冷青藍都會夜光", "極克制低飽和紙白／舊木"]

# 空間動線、固定陳設與留白區（防跨鏡空間漂移）
spatial_anchors:
  - "左前／中景：暗木書桌，置毛筆、空白紙本、幾張模糊紙鈔與無字息屏小顯示器"
  - "右後背景：落地／寬幅窗戶，窗外高樓巨幕新聞強散焦（完全不可讀）"
  - "右側中景暗區：刻意保留乾淨暗牆與空間負形，供 SYS-01 全息投影站立（conversation_eyeline）及 S08 後製資料側卡"
aspect_ratio: "9:16"
usable_angles:                          # 一卡多角統一歸檔於同 LOC，命名 {loc_id}_{angle_id}
  - angle_id: "desk"                    # 主正面／微側書桌角（S06, S07, S08, S09, S10, S11a, S11c, S18a/b）
    camera_axis: "平視 35–50mm，書桌居下三分之一、右側留暗區"
    purpose_shots: ["S06", "S07", "S08", "S09", "S10", "S18a"]
  - angle_id: "window"                  # 窗前背側／望向巨幕角（S12, S17a）
    camera_axis: "平視 35mm，窗外散焦巨幕佔上中景"
    purpose_shots: ["S12", "S17a"]
  - angle_id: "tabletop"                # 桌面近景／小屏與毛筆留白角（S06 備用、S19 暗虛化背景）
    camera_axis: "微俯 50–85mm 淺景深"
    purpose_shots: ["S06", "S19"]

# 音景綁定（Spec v2.3 §2.1）
default_roomtone_id: "studio_night_hum_48k"
acoustics_profile: "small_room_dry_distant_city_hum"

# 硬禁則（無人物規則＋V9＋考據）
no_people_rule: true                    # 100% 空景母圖，嚴禁任何人影、剪影、手部或路人
forbidden_elements:
  - "任何人物、人影、背影、手部（含遠景追兵剪影——LOC-TAIHU-NIGHT 只許遠處火把光點，人影不入母圖）"
  - "任何可讀中文／英文／數字、招牌、匾額、巨幕新聞字樣、螢幕 UI（V9 硬紅線）"
  - "過曝白光面積 >5%、豪華網美風裝潢／RGB 電競燈"

# Spec v2.3 §3.C.1 參照契約
asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "2026 深夜台北極簡狹小暗色單人套房空景，暗木書桌置毛筆與空白紙本，右後寬窗外遠處都會巨幕強烈散焦冷青反光，右側保留深暗牆面空間"

ref_images: []                          # LOCKED 後填入 {angle_id, path, resolution, seed, bg_L, bg_b, blowout_pct, sha256}
qc1_record: []                          # 逐張 LOC-QC-1 7 項核對表
```

#### LOC-QC-1 七項驗收門檻（7/7 PASS 方可轉 `LOCKED`）
1. **`no_people_rule`（絕對空景 — 一票否決）**：畫面內 **0 人物、0 剪影、0 肢體**（防止母圖作 `<Pic 1>` 時長出多餘幽靈路人；`LOC-TAIHU-NIGHT` 僅許遠岸微小橘紅火把光點，禁止人形）。
2. **`light_lock_and_lab`（光線鎖與 Lab 基準）**：光源方向、色溫與 `light_lock_id` 吻合；`blowout_pct ≤ 5.0%`；同 LOC 多角度母圖彼此差值 **`|ΔL*| ≤ 15`、`|Δb*| ≤ 12`**。
3. **`blocking_and_negative_space`（調度物與留白區驗收）**：劇本剛性站位與空間地標齊備——`LOC-FANLI-STUDIO-26` 右側具足夠暗區容納 `SYS-01` 與 `S08` 側卡；`LOC-TAIHU-DAWN` 小舟明確呈現「對面空座」構圖；`LOC-TAIPEI-STREET-2022` 具路柱＋長椅空間；`LOC-TAIHU-NIGHT` 具岸邊蘆葦＋暗水面＋遠岸火把光點。
4. **`v9_zero_readable_text`（V9 零字 — 一票否決）**：街景招牌、窗外巨幕、宮殿匾額、桌上紙本與小屏 **0 可讀字元、0 品牌 Logo**。
5. **`era_and_geography_accuracy`（時代與地理考據）**：`LOC-YUE-COURT`／`LOC-WENZHONG-GATE` 嚴守春秋先秦低矮素樸木構與席地矮几燭火（**嚴禁明清紅牆黃瓦雕龍、高腳椅與匾額**）；`LOC-TAIPEI-STREET-2022` 具真實台北街景肌理（騎樓柱、柏油、低飽和冷陰天，非東京／紐約／上海）。
6. **`aspect_and_composition_9x16`（豎屏構圖）**：原生 9:16 構圖，前景／中景／遠景層次清楚，具人物頭頂留白，可直接送入 `nano2 i2i` 或 L3 Clay `<Pic 1>`。
7. **`angle_continuity`（多角度連戲，單角填 `N_A`）**：同 LOC 下 `_desk`／`_window` 或 `_main`／`_rev` 的建材、牆色、地面材質與主光方向高度一致。

---

## 3. S16 賜劍設計問題：`PROP-SWORD-01` 同卡 vs 獨立 `PROP-SWORD-02`

> **Canon 實查備註**：`DRYRUN-EP01-arrival-v0.3.2.md` §二（L32）已明載「**原典《史記·越王句踐世家》，賜劍不名屬鏤**」（屬鏤為吳王夫差賜伍子胥之劍，後世偶混稱越王賜文種劍），且劇本 S16a 僅為 **3.0 秒無正臉手與劍 `INSERT` 鏡**（`內侍捧劍而至，只拍手與劍`）。同時須注意：**已鎖定之 `fanli-outfit03-front.jpg`／`45.jpg` 左腰已有一把越國青銅短劍**（暗舊鑄銅圓首素柄、窄銅格、啞光深色髹漆鞘）。

### 3.1 工程與視覺利弊對照

| 評估維度 | 方案 A：同一把劍（`PROP-SWORD-01` 兼用於 S00 ＋ S16a） | 方案 B：兩張獨立道具卡（`PROP-SWORD-01` 范蠡自佩越劍 vs `PROP-SWORD-02` 越王賜劍） |
| :--- | :--- | :--- |
| **邊際產製成本** | 基準（`PROP-SWORD-01` 3 張 `nano2` 圖） | **僅多 +1 張 `nano2` 靜態圖**（`0` Flow 影片點、`0 CU`、約 **+3 分鐘**、**P1 不擋任何 P0**） |
| **9:16 3 秒特寫辨識度** | **有誤讀風險**：若 S00 剛看過范蠡握這把素柄劍、S16a 又見內侍雙手捧「一模一樣的素柄劍」，短劇觀眾（3 秒內）可能誤讀為「范蠡的劍被沒收／轉交」，而非「越王賜死禮劍」。 | **視覺語意 100% 零歧義**：范蠡自佩（S00/S13）為素樸暗銅實戰短劍；賜文種（S16a）為內侍雙手橫托於玄黑帛布上之**越王禮制青銅賜劍**（較精緻暗紋銅格、深漆禮鞘、仍嚴守無銘文無亮金），一眼讀出「君王賜死」。 |
| **與 `OUTFIT-03` 連戲** | 若 S00、S13（`OUTFIT-03`）、S16a 三處全用同劍，反削弱賜劍的權力位階反差。 | `PROP-SWORD-01` 緊密錨定 `fanli-outfit03-45.jpg`（范蠡同一把隨身劍貫穿 S00 逃亡與 S13 朝堂）；`PROP-SWORD-02` 專責 S16a 賜死意象，兩條視覺線條互不打架。 |
| **敘事／象徵意涵** | **具強烈隱喻張力**：暗示「同一種越國青銅劍——能護范蠡脫身，也能殺文種；權力的刀從頭到尾是同一把」。 | 偏重寫實層級區分（臣子佩劍 vs 君王賜死之劍），不強綁「同一把劍」的字面關聯。 |

### 3.2 交給 Creator 的純淨決策基礎

**工程結論：兩案成本差距趨近於零（僅 1 張 0 點靜態圖、約 3 分鐘、且屬 P1 完全不擋 P0）。因此本題不應以「省一卡」為考量，100% 歸屬 Creator 敘事取捨：**
- 若 Creator **刻意追求象徵呼應**（「S00 護身之劍與 S16 殺友之劍是同一形制的越劍，暗示同源的權力工具」）→ 選 **方案 A（同卡 `PROP-SWORD-01`）**，僅須於 S16a 構圖加襯深色託帛拉開「內侍捧賜」語境。
- 若 Creator **優先確保 9:16 三秒特寫零誤讀**（一眼分清「范蠡自佩」與「勾踐賜死」）→ 選 **方案 B（拆出 `PROP-SWORD-02`｜工程微推薦）**。

---

## 4. `SYS-01` 裁切清單、`bible/anchors/SYS01.yaml` 規格與閘門接線（AMD-05 v3 §5.3）

### 4.1 精確裁切清單（100% 純 CPU Pillow，**不做去背**，保留乾淨淺灰棚底）

> **關鍵修訂**：Muse 原表寫「裁切去背」屬 AMD-05 v2 殘留；在 **AMD-05 v3 生成主導路線**下，餵給 `nano2`／H3 的參考圖應為**無損 RGB 矩形裁切 PNG**（保留原卡極均勻淺灰棚底 `RGB≈(218,219,221)`，無 Alpha 透明邊緣黑暈風險，純 CPU 10 秒內完成）。

| 輸出檔名（存於 `casting/master/`） | 來源母卡（皆 `2047×1152`） | 實測精確裁切座標 `(x0, y0, x1, y1)` | 尺寸 (px) | 用途與鏡頭對應 |
| :--- | :--- | :---: | :---: | :--- |
| **`sys01-ref-front.png`** | `sys01-charactercard-main.png`（左格） | `(0, 0, 700, 1152)` | `700×1152` | **主身分高解析基準**；SM-8、`S19`、全片 `diff_sheet_gen.py` Col 1 `master_face_ref` |
| **`sys01-ref-full-front.png`** | `sys01-charactercard-main.png`（中左格） | `(730, 0, 1180, 1152)` | `450×1152` | 全身正面站姿（黑大衣＋黑褲＋黑靴），供 `S08`/`S10` `conversation_eyeline` |
| **`sys01-ref-full-profileL.png`** | `sys01-charactercard-main.png`（中右格） | `(1210, 0, 1540, 1152)` | `330×1152` | 朝畫面左側全側身站姿，供側站並肩／過肩預備 |
| **`sys01-ref-full-back.png`** *(順手)* | `sys01-charactercard-main.png`（右格） | `(1580, 0, 2047, 1152)` | `467×1152` | 背面站姿（未來過她肩反打范蠡，0 額外成本） |
| **`sys01-ref-expr-R1C1-smile.png`** | `sys01-charactercard-expressions.png` R1C1 | `(41, 72, 330, 456)` | `289×384` | 正面標準禮貌微笑（**徹底裁除下方 `y=468..480` 假比例數字 `300:140`**）；`S19` 起始表情錨 |
| **`sys01-ref-34L-neutral.png`** | `sys01-charactercard-expressions.png` R1C2 | `(372, 72, 665, 456)` | `293×384` | 3/4 朝畫面左側平靜中性無笑（裁除 `250:360`）；`S08`/`S10` 高壓問答／未來對峙 |
| **`sys01-ref-34L-smile.png`** | `sys01-charactercard-expressions.png` R1C4 | `(1040, 72, 1330, 456)` | `290×384` | **微 3/4 朝畫面左側溫和微笑**（裁除 `570:360`）；**SM-8、DEMO-03 `S3b`、EP-01 `S03`/`S04a` 首選主 ref**（與左下角范蠡天然眼神對位） |
| **`sys01-ref-expr-R1C5-hesitate.png`** | `sys01-charactercard-expressions.png` R1C5 | `(1372, 72, 1660, 456)` | `288×384` | 正面笑意收斂平靜凝視（裁除 `730:360`）；**EP-01 `S19` 0.5 秒微笑遲疑目標表情錨** |
| **`sys01-ref-expr-R1C6-downcast.png`** *(備選)* | `sys01-charactercard-expressions.png` R1C6 | `(1703, 72, 2006, 456)` | `303×384` | 微垂眼思索淡笑（裁除 `890:1150`）；`S19` 備案／EP-02+ 破防參考 |

> **工程護欄兩條**：
> 1. **嚴禁單獨餵 `290×384` 表情格拍特寫**：`R1C1`／`R1C5`／`34L-smile` 皆為小格（~290px 寬），作 `nano2`／H3 特寫參考（如 `S19`）時**必與高解析 `sys01-ref-front.png`（`700×1152`）雙配輸入**，由 `front` 鎖皮膚五官銳度、由 `R1C1`/`R1C5` 鎖表情變化。
> 2. **硬禁來源名單**：`sys01-charactercard-main.png`、`sys01-charactercard-expressions.png`、**R2C5（`640:280` 異常手持木錐格）**、以及含亂碼面板之 `sys01-projection-look-ref.png`，永不直接餵入任何生成模型。
> 3. **同批次順手補裁 `FANLI-OUTFIT-01`（+5 秒 CPU）**：自 `fanli-modern-charactercard-main.png` 裁 `(0, 0, 766, 1152)` → `fanli-modern-ref-cu.png`（疤已在解剖學左眉尾／畫面右側！）；自 `fanli-modern-charactercard-expressions.png` R1C2 裁 `(342, 0, 680, 634)` → `fanli-modern-ref-45L.png`（無方孔錢！）。

### 4.2 `bible/anchors/SYS01.yaml` 凍結欄位規格

完全相容 `tools/diff_sheet_gen.py` 現行 `load_anchors_dir()` 結構（比照 `bible/anchors/FANLI.yaml`），並零破壞映射至既有 5/6 頂層 QC 鍵（AMD-05 v3 §5.3）：

```yaml
# bible/anchors/SYS01.yaml — SYS-01 跨鏡身分與全息投影錨點唯一準據（v2.4 / AMD-05 v3）
char_id: SYS01
aliases: ["SYS-01"]
status: LOCKED
identity_master: casting/master/sys01-ref-front.png
expression_refs:
  front_smile: casting/master/sys01-ref-expr-R1C1-smile.png
  angle_34L_smile: casting/master/sys01-ref-34L-smile.png
  angle_34L_neutral: casting/master/sys01-ref-34L-neutral.png
  hesitate_R1C5: casting/master/sys01-ref-expr-R1C5-hesitate.png
  downcast_R1C6: casting/master/sys01-ref-expr-R1C6-downcast.png
forbidden_source_assets:
  - "sys01-charactercard-main.png"
  - "sys01-charactercard-expressions.png"
  - "sys01-projection-look-ref.png"
  - "expressions_R2C5_wooden_object"

anchors:
  - anchor_id: ANC-SYS01-01
    name: 臉部對卡一致＋自然膚色＋黑色齊下巴短鮑伯頭
    category: permanent_anatomical
    applies_to_eras: ["2022", "2026"]
    spec:
      age_band: "20多歲東亞年輕女性"
      hair: "齊下巴自然微層次黑色短鮑伯頭，自然微偏分露額角"
      skin_protection: "保留 82–88% 原生自然溫潤膚色、清亮深棕眼眸與清晰唇線；嚴禁整臉染成單色藍鬼或塑膠美顏肌"
    forbidden_in_anchor: ["單色藍臉鬼", "塑膠美顏肌", "換臉", "長髮", "馬尾", "誇張露齒大笑"]
    qc_gate_key: age_id
    prompt_zh_positive: "20多歲東亞年輕女性，齊下巴自然黑色短鮑伯頭、清亮深棕眼眸、保留自然溫潤膚色與清晰五官"

  - anchor_id: ANC-SYS01-02
    name: 簽名服裝（素面黑色羊毛大衣＋深紅色粗針織圍巾）
    category: permanent_costume
    applies_to_eras: ["2022", "2026"]
    spec:
      coat: "素面啞光黑色羊毛翻領大衣（無條紋、無徽章、無科幻發光線條）"
      scarf: "深紅色（暗酒紅）粗針織圍巾繞頸自然垂落（畫面核心低飽和暖色視覺錨點）"
    forbidden_in_anchor: ["灰底細條紋西裝外套", "現代科幻緊身衣", "無紅圍巾", "淺色外套"]
    qc_gate_key: costume_4pt
    prompt_zh_positive: "穿素面黑色羊毛大衣，頸圍深紅色粗針織圍巾"

  - anchor_id: ANC-SYS01-03
    name: 全息投影光學五要素（AMD-05 v3）
    category: projection_optics
    applies_to_eras: ["2022", "2026"]
    required_prompt_terms_min: 2
    canonical_prompt_terms_zh:
      - "全息投影"
      - "半透明"
      - "掃描線"
      - "藍色輪廓光"
      - "粒子消散"
      - "下身光塵化"
    spec:
      optics_5pt:
        - "半透明軀幹（非實心肉身站立）"
        - "水平細密藍色掃描線集中於肩衣與軀幹（臉部極淡豁免）"
        - "柔和冰藍色輪廓光包覆髮絲與肩線"
        - "胸腹／腰下自然半透明下身光塵化，化作漂浮藍色光塵融於霧氣／暗景"
        - "對現場霧氣與范蠡臉側／衣領自然回打柔和冷青微光（爆光 <5%）"
    forbidden_in_anchor: ["實心真人站立", "粗糙白邊去背貼紙", "矩形軟體視窗外框", "音訊波形條", "過曝閃白"]
    qc_gate_key: light_lock
    prompt_zh_positive: "半透明全息投影，冰藍色輪廓光，水平細密藍色掃描線覆於肩衣（臉部極淡），胸腹以下下身光塵化為漂浮藍色粒子消散，柔和冷青光映照范蠡臉側"

  - anchor_id: ANC-SYS01-04
    name: V9 零文字／零浮動面板／零圓形 HUD 光環（一票否決）
    category: hard_ban_v9
    applies_to_eras: ["2022", "2026"]
    auto_fail_on_single_frame: true
    forbidden_in_anchor:
      - "任何漢字／英文字母／數字／偽文字"
      - "浮動小面板／懸浮數據視窗"
      - "圓形雷達光環／HUD介面框"
      - "豆包／品牌標誌／任務啟動字樣"
    qc_gate_key: pose_spatial
    prompt_zh_avoid: "任何文字、漢字、英文字母、數字、浮動小面板、懸浮數據視窗、圓形雷達光環、HUD介面框、品牌標誌、浮水印、音訊波形條"

  - anchor_id: ANC-SYS01-05
    name: 尺度調度與微表情可讀性（sys01_scale_mode）
    category: scale_and_expression
    variants:
      manifestation_hero:
        applies_to_scale_modes: ["manifestation_hero"]
        spec: "右上懸浮半身投影，頭肩約范蠡 1.25–1.45×，胸腹以下光塵化；范蠡居左下仰角 20–35° 注視（S03/S04a）"
        forbidden_in_variant: ["等高硬擠窄框", "同場無故縮放 >±10%"]
      conversation_eyeline:
        applies_to_scale_modes: ["conversation_eyeline"]
        spec: "並肩或前後景深錯位，頭高約范蠡 0.90–1.00×、眼平 ±5°（S08/S10；S08 預留暗區給後製無框側卡）"
        forbidden_in_variant: ["巨人懸浮壓頂", "同場無故縮放 >±10%"]
      solo_cu:
        applies_to_scale_modes: ["solo_cu"]
        spec: "85mm 正面胸上特寫；S19 必於 360px 手機縮圖下清晰辨識 R1C1 禮貌微笑 → R1C5 半秒嘴角微收 1–2mm 凝滯遲疑"
        forbidden_in_variant: ["掃描線遮蓋眼唇", "過度悲傷皺眉流淚", "大轉頭"]
    qc_gate_key: expression_lip
```

### 4.3 接線至 `preflight_gate.py` 與 `diff_sheet_gen.py` 之實碼異動點（重要實碼抓錯！）

經逐行審閱 `tools/diff_sheet_gen.py`（L75–250、L1083–1187、L1344–1405）與 `tools/preflight_gate.py`（L852–870、L989–1165），發現 **3 項關鍵實碼限制**須於 SM-8 通過後一併補齊（共約 90–120 行純 CPU 改動）：

1. **`tools/diff_sheet_gen.py` 多角色解析缺口（關鍵捕獲！）**：
   - 現況：`resolve_shot_anchors()`（L121–145）透過 `_infer_char_id()`（L107–118）**每鏡僅回傳單一 `char_id`**！在雙人鏡（`S03`、`S04a`、`S08`、`S10`、SM-8）中，`outfit_id="FANLI-OUTFIT-02"` 會只載入 `FANLI.yaml`，**`SYS01.yaml` 會被完全靜默忽略**！且 `_infer_char_id` 以 `"-"` 切字，若傳 `SYS-01` 會切成 `"SYS"` 找不到鍵值。
   - 修法：改為 `_infer_char_ids(shot, anchors_db) -> List[str]`，正規化鍵名（去連字號 `SYS-01` ↔ `SYS01`），合併偵測 `outfit_id` 前綴＋`char_ids[]`＋`sys01_in_frame: true`＋`asset_refs` 中 `SYS01/SYS-01`，並將多個角色的 `required_lines`／`forbidden_lines` 依序串接印上 Col 0 與 Col 2。
2. **`tools/diff_sheet_gen.py` `sys01_scale_mode` 變體與雙臉 2.5× 放大**：
   - 擴充 Case 1 變體比對（L170–197）支援 `applies_to_scale_modes`（對齊 `shot.get("sys01_scale_mode")`），使 `ANC-SYS01-05` 自動依該鏡模式印出對應尺度門檻。
   - 雙人同框鏡（`FANLI`＋`SYS01`）：Col 1 上下分欄並排范蠡基準臉與 `sys01-ref-front.png`；Col 4 支援選填 `sys01_face_box` 同時呈現雙人 2.5× 臉部檢視；`solo_cu`（`S19`）Col 1 並列 `R1C1` vs `R1C5`，並於 QC-2 補印 360px 手機縮圖寬度預覽塊驗 `expression_lip`。
3. **`tools/preflight_gate.py` AMD-05 v3 雙閘接線（§5.2）**：
   - 退役舊 `SYS01_BAN`（L166–178、L854–869），拆為：
     - **`SYS01_TEXT_PANEL_BAN`（`FAIL`）**：硬禁正文中出現浮動面板／HUD 圓環／可讀文字／豆包品牌詞，並驗 `避免：` 段必含禁字禁面板詞。
     - **`SYS01_PROJECTION_ANCHOR_REQ`（`FAIL`）**：凡 `sys01_in_frame: true` 鏡，直接對照 `SYS01.yaml` 強制驗收：`≥2` 項全息光學詞＋`黑羊毛大衣`/`紅圍巾`/`自然膚色`＋合法 `sys01_scale_mode`。
   - 擴充既有 `ASSET_CONTRACT`（L1017 已攔 `charactercard`）：追加硬攔 `sys01-projection-look-ref` 與 `R2C5` 檔名。
   - 放寬 `PROMPT_HYGIENE_DIALECT`（L719–731）允許 Flow／`nano2` 使用繁體中文提示詞（房規對齊）；選配追加 `PROP_ERA_BAN`（讀 PROP 卡 `forbidden_eras`/`forbidden_outfits` 自動封殺春秋出現 `PROP-COIN-01`）。

---

## 5. 生產順序、WAF 防護批次與工時估算

### 5.1 Flow `nano2` WAF 403 冷卻模式復盤與安全分批紀律

對照實機紀錄（`demo02_v2/run_stage3_frames.py` vs `EP01_PREP_REPORT.md` §3）：
- **安全先例**：`DEMO-02 v2` Stage 3 循序執行 **4 張 `nano2` i2i**（每張 ~58–94 秒），**0 次 WAF 403**。
- **觸發成因**：同日 `09:06Z` 在高密度 DEMO-02 v2 影片批次剛結束後，由 `gen_candidates.py` 以 **0 秒間隔**連續自動提交 `t2i`，第 2 張即觸發 `WafRejectionError`（HTTP 403 `PUBLIC_ERROR_UNUSUAL_ACTIVITY`, gRPC 7, exit 10）。
- **四條防觸發分批紀律（嚴守零繞過原則）**：
  1. **單次 session 硬上限 `≤ 3–4 張` `nano2` 靜態圖**（鎖死在 DEMO-02 v2 已驗證安全水位內）。
  2. **張間冷卻 `≥ 45–60 秒`＋人工目視初檢**：每產 1 張先做肉眼檢查／寫紀錄再送下一張，**嚴禁無停頓 `for` 迴圈連發**。
  3. **跨 session 間隔 `≥ 30–45 分鐘`**：在兩組 `nano2` 批次間穿插純 CPU 工項（裁圖、YAML、音訊、文件、工具補丁）或 ElevenLabs API（非 Flow 通道，零耦合），且**不緊接在重型 Flow 影片批次之後跑 `nano2`**。
  4. **遇 403 立即停機（Zero-Retry / Zero-Bypass）**：一旦觸發任何 WAF 403，立刻停止批次並回報 Creator（由 Creator 改以可見瀏覽器 UI 手動補產或擇時再跑，絕不自動重試或繞過）。

### 5.2 分階段關鍵路徑排程與逐項工時表

將原清單 P0 細分為 **`P0-CPU` → `P0-SM8` → `P0-DEMO03` → `P0-EP01` → `P1-EP01` → `P2`**，確保最快解鎖 `SM-8` 與 `DEMO-03`，且零浪費算力：

| 階段／批次 | 類別 | 工項明細 | 載體／張數 | 主動工時 | 解鎖目標 |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Phase 0（純 CPU 先行）** | **CPU** | ① `casting/master/` 衛生搬移（6 `tmp_*` ＋ 2 禁用殘留 → `casting/archive/`）<br>② Pillow 無損裁圖：`SYS-01` 7–9 張單視圖 ＋ `FANLI-OUTFIT-01` 2 張（`cu`/`45L`）<br>③ 撰寫 `bible/anchors/SYS01.yaml`<br>④ 建立 `PROP_REGISTRY.md`／`LOCATION_REGISTRY.md` 骨架與 manifest `PENDING` 登記 | **100% CPU**<br>(`0 pts / 0 CU / 0 TTS`) | **45–55 min** | 全域無風險地基；直通 SM-8 |
| **Phase 1（Session B1）** | **P0-SM8** | `SM-8` 單鏡驗證（用既有 `S3a_first.jpg`＋`OUTFIT-02`＋`sys01-ref-34L-smile`）：`1–3` 張 `nano2` 首幀 → QC-1 → `1–2` 支 4s Flow Omni | `nano2` 1–3 張 (`0 pts`) ＋ Flow Omni **`12–24 pts`** | **20–25 min** | **AMD-05 v3 過關門票**（決定是否合併 Spec v2.4） |
| **Phase 1.5（純 CPU 穿插）** | **CPU** | *（SM-8 GO 後執行）* 合併 Spec v2.4 §C.4、修補 `preflight_gate.py` 與 `diff_sheet_gen.py`（含 `--selftest` 全過）、同步更新 manifest `SYS-01` 備註；同步整理 5 條新 48kHz Roomtone＋關鍵 Foley 進 `audio_lib/` | **100% CPU**<br>(`0 pts / 0 CU`) | **60–70 min** | 滿足 B1→B2 間 ≥45m WAF 間隔；工具與音庫就位 |
| **Phase 2（Session B2）** | **P0-DEMO03 / EP01** | `LOC-TAIHU-DAWN`（1–2 張挑 1）＋ `LOC-TAIHU-NIGHT`（1–2 張挑 1）＋ LOC-QC-1 | `nano2` 3–4 張 (`0 pts`) | **20–25 min** | **解鎖 DEMO-03 `S0`** ＋ **EP-01 `S00`/`S01`/`S16b`** |
| **Phase 2（穿插：ElevenLabs）** | **P0-EP01 / DEMO03** | ① `SYS01-VOICE` Voice Design 抽樣＋四詞／「范蠡先生」驗收稿（供 Creator 試聽）<br>② *（若跑 DEMO-03 且選 TTS）* `WITNESS-DEMO03-VOICE` 客串快篩（或等 Creator 10s 真人乾錄） | ElevenLabs API<br>(`~2,000–2,500 字`，非 Flow) | **25–30 min** *(不含異步試聽)* | 滿足 B2→B3 WAF 間隔；解鎖 DEMO-03 與 EP-01 Stage 1.5 |
| **Phase 2（Session B3）** | **P0-EP01** | `PROP-SWORD-01` 三態（`sheathed_hip`/`hand_on_hilt_ecu`/`unsheathed_1inch`，錨定 `fanli-outfit03-45.jpg`）＋ **`fanli-modern-ref-45R.jpg`**（補齊現代無疤右 45°）＋ QC-1 | `nano2` 4 張 (`0 pts`) | **25–30 min** | 解鎖 v0.3.3 `S00` 劍戲 ＋ EP-01 7 顆現代 H3 鏡 |
| **Phase 2（Session B4）** | **P0-EP01** | `LOC-FANLI-STUDIO-26` 三角度（`_desk`／`_window`／`_tabletop`，同鎖 `LK-STUDIO-NIGHT26`＋`SYS-01` 右側暗區）＋ LOC-QC-1 | `nano2` 3–4 張 (`0 pts`) | **20–25 min** | 解鎖 EP-01 12 鏡常駐主場（`S06–S12, S17–S19`） |
| **Phase 3（Session B5）** | **P1-EP01** | `LOC-TAIPEI-STREET-2022`（`_main`＋`_rev`）＋ `PROP-BAMBOO-01`（展開／半捲二態）＋ QC-1 | `nano2` 3–4 張 (`0 pts`) | **20–25 min** | 解鎖 `S02–S04c`、`S14b`/`S15a` |
| **Phase 3（Session B6）** | **P1-EP01** | `LOC-YUE-COURT` ＋ `LOC-WENZHONG-GATE` ＋ *（若選方案 B）* `PROP-SWORD-02`（1 張賜劍特寫）＋ QC-1；並以 ElevenLabs Voice Library 快鎖 `GOUJIAN-VOICE`／`WENZHONG-VOICE`（10 min） | `nano2` 3–4 張 (`0 pts`) ＋ ElevenLabs `~500 字` | **30–35 min** | **EP-01 全資產 100% LOCKED**，可進 Stage 1 |
| **Phase 4（延後）** | **P2** | `PROP-COIN-01`（再生無字磨損面，嚴禁裁 R2C2）；`FANLI-OUTFIT-03` 正面傷痕補修（可選） | `nano2` 2 張 (`0 pts`) | **15 min** | EP-01 後續集數補完（**不擋本輪**） |

### 5.3 工時與資源總結

| 範圍 | 主動工程工時 | 含 WAF 冷卻間隔之牆鐘跨度 | Flow 影片點數 | Colab CU | ElevenLabs 字符 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **純 CPU 工項合計（Phase 0 + 1.5）** | **`~1.8–2.1 hr`** | `~1.8–2.1 hr` | `0` | `0.00` | `0` |
| **P0 全齊（含 SM-8 + B2–B4 + `SYS01-VOICE` 準備）** | **`~3.5–4.2 hr`** | `~4.5–5.5 hr`（跨 4 次 `nano2` 批次） | **`12–24 pts`** *(僅 SM-8)* | `0.00` | `~2,000–2,500 字` |
| **EP-01 P0＋P1 全資產補齊總計** | **`~4.5–5.3 hr`** | `~6.0–7.5 hr`（跨 6 次 `nano2` 批次，建議分 2 日或上／下午段執行） | **`12–24 pts`** *(僅 SM-8)* | `0.00` | `~2,500–3,300 字` (`<8.5%` 月額) |

---

## 6. Manifest 變更與 `casting/master/` 衛生清理機制

### 6.1 `ASSETS_MANIFEST.yaml` 精確異動規格與更新時機

1. **新增頂層 `props:` 段**（待執行時 bump `version: 2`）：
   ```yaml
   props:
     - id: PROP-SWORD-01
       desc: 范蠡春秋青銅越劍（圓首素柄、窄銅格、暗啞髹漆鞘、無銘文；佩左腰；三態：佩掛全形／手按劍柄 ECU／出鞘一寸）
       status: PENDING
       location: VM ~/drama-line/casting/props/PROP-SWORD-01/ (規格見 docs/PROP_REGISTRY.md)
       note: 錨定 fanli-outfit03-45.jpg 既有越劍外型；僅春秋線使用（S00；S16 是否共用見 Creator 拍板）
     - id: PROP-SWORD-02   # 僅於 Creator 採方案 B（賜劍獨立卡）時加入
       desc: 越王賜文種青銅禮劍（雙手橫托於深色帛布上之無銘文禮制青銅劍；僅 S16a 特寫）
       status: PENDING
       location: VM ~/drama-line/casting/props/PROP-SWORD-02/
     - id: PROP-BAMBOO-01
       desc: 春秋無字素面竹簡（展開／半捲二態，文字一律後製）
       status: PENDING
       location: VM ~/drama-line/casting/props/PROP-BAMBOO-01/
     - id: PROP-COIN-01
       desc: 古銅方孔圓錢（直徑 3.8–4.5cm、右手持、錢面磨損不可讀；僅現代線，春秋古裝嚴禁）
       status: PENDING  # P2；嚴禁裁切 fanli-modern-charactercard-expressions.png R2C2（含可讀偽字）
       location: VM ~/drama-line/casting/props/PROP-COIN-01/
   ```
2. **擴充 `locations:` 段**（新增 6 條，初始狀態皆 `PENDING`，通過 LOC-QC-1 並回填 `light_lock_id` 與檔案路徑後方可改 `LOCKED`）：
   - `LOC-TAIHU-NIGHT`（`LK-TAIHU-NIGHT`，`S00`，`casting/scenes/LOC-TAIHU-NIGHT/`）
   - `LOC-TAIHU-DAWN`（`LK-TAIHU-MIST`，`DEMO-03 S0`／`EP-01 S01, S16b`，`casting/scenes/LOC-TAIHU-DAWN/`）
   - `LOC-FANLI-STUDIO-26`（`LK-STUDIO-NIGHT26`，3 角度 `_desk`/`_window`/`_tabletop`，`S06–S12, S17a–S19`，`casting/scenes/LOC-FANLI-STUDIO-26/`）
   - `LOC-TAIPEI-STREET-2022`（`LK-TAIPEI-DUSK22`，`_main`＋`_rev`，`S02–S04c`，`casting/scenes/LOC-TAIPEI-STREET-2022/`）
   - `LOC-YUE-COURT`（`LK-COURT-TORCH`，`S13, S14a, S15b`，`casting/scenes/LOC-YUE-COURT/`）
   - `LOC-WENZHONG-GATE`（`LK-COURT-TORCH`，`S14b, S15a`，`casting/scenes/LOC-WENZHONG-GATE/`）
3. **更新既有 `characters:` 與 `voices:` 條目**：
   - `FANLI-CHARCARD-MODERN`：補記 CPU 裁切單視圖 `fanli-modern-ref-cu.png`／`-45L.png` 與新補無疤 `fanli-modern-ref-45R.jpg` 路徑（`OUTFIT-01` H3 4 槽基準）。
   - `voices:` 新增 `GOUJIAN-VOICE`（`PENDING`）、`WENZHONG-VOICE`（`PENDING`）與條件項 `WITNESS-DEMO03-VOICE`；並**修正 `FANLI-VOICE-F` 既有路徑落差**（manifest L52 寫 `bible/voices/FANLI.yaml`，VM 實際位置為 `~/drama-line/voices/FANLI.yaml`，建議同步建 symlink 或統一記註 repo vs VM 雙路徑）。
   - 選配新增精簡 `audio_beds:` 段追蹤 `audio_lib/roomtone/`（1 既有 `alley_night_wet_48k` ＋ 5 新增）。
4. **`SYS-01` 備註更新時機與 Spec v2.4 同步鐵律**：
   - **禁止於 SM-8 通過前提前改寫 `SYS-01` 備註為「v3 生成主導」**——否則會出現「manifest 說 v3、Spec v2.3 與 `preflight_gate.py` 仍強制 v1 貼片」的規格分裂。
   - **兩階段鎖定節奏**：
     - *Stage A（Phase 0，SM-8 前）*：只補登 CPU 裁切之 `sys01-ref-*.png` 單視圖路徑（v2/v3 皆有效），並在 `SYS-01` 原備註尾附註 1 句 `「AMD-05 v3 生成主導方案待 SM-8 驗收與 Spec v2.4 併入後切換」`。
     - *Stage B（SM-8 GO 後，單一原子同步）*：`STORYBOARD-SPEC-V2.md`（§C.4 v3 → v2.4）＋ `tools/preflight_gate.py` ＋ `tools/diff_sheet_gen.py` ＋ `ASSETS_MANIFEST.yaml`（正式改寫 `SYS-01` 備註）＋ `PROJECT_STATUS.md` 五檔**同批一次更新**。

### 6.2 `casting/master/` 清理機制（只移不刪、零斷鏈驗證）

經實查磁碟與 `grep` 全數 `tools/`、`demo02_v2/`、`bible/` 程式碼，**以下 8 項非鎖定檔均無任何現行執行腳本引用**（僅 `preflight_gate.py` 禁用正則與單元測試提及 `v1-flip-defect` 字串）：

| 來源路徑（目前位於 `casting/master/`） | 類別與大小 | 建議移入留檔目的地（位於 `master/` 之外，避免 glob 誤掃） | 說明 |
| :--- | :--- | :--- | :--- |
| `tmp_45R/`、`tmp_45R2/`、`tmp_45Rfix/`、`tmp_CU/`、`tmp_CU2/` | 5 個工作暫存目錄（共 ~3.1 MB） | `~/drama-line/casting/archive/20261128_master_tmp/` | 其中 `tmp_45Rfix` 與 `tmp_CU2` 內圖與已鎖定 `45R`/`cu` 逐位元組相同 |
| `tmp_flip45.jpg` | 禁用水平翻轉中間檔（40 KB） | `~/drama-line/casting/archive/20261128_master_tmp/` | 退役 Step-0 水平翻轉法殘留 |
| `fanli-master-ancient-45R.v1-flip-defect.jpg` *(Muse 漏列)* | 缺陷禁用版（85 KB） | `~/drama-line/casting/archive/defects/` | 避免留在 `master/` 遭手動或腳本誤選；同步更新 manifest L15 路徑註記 |
| `fanli-master-B.jpg` *(Muse 漏列)* | 棄用 Seedream 5.5 臉（163 KB） | `~/drama-line/casting/master/superseded-seedream/`（或 `casting/archive/superseded-seedream/`） | 其 4 個同批檔案已在 `superseded-seedream/`；僅移前須於 `MASTER_FACE_DECISION.md` 附 1 行搬移紀錄 |

**執行安全協議**（核准執行時）：① 全程使用 `mv -n`（no-clobber），**絕對零 `rm`**；② 於 `~/drama-line/casting/archive/ARCHIVE_MANIFEST.txt` 記錄每檔原路徑、目標路徑、SHA256、搬移日期與原因；③ 搬移後以 `ls casting/master/` 覆核，確保該目錄僅剩 `LOCKED` 資產（主臉／古裝／朝服／角色卡原檔／裁切單視圖）及既有留檔子夾。

---

## 7. 待 Creator 拍板（共 3 題，已壓至最小集）

1. **S16 賜劍是否獨立開卡（`PROP-SWORD-01` 共用 vs 新增 `PROP-SWORD-02`）？**  
   工程邊際成本幾乎為零（僅 +1 張 `0` 點 `nano2` 圖、約 3 分鐘，屬 P1 不擋任何 P0），純屬敘事取捨：**方案 B（獨立 `PROP-SWORD-02` 越王禮制賜劍，確保 3 秒特寫一眼區分「君王賜死」與「范蠡自佩」，工程微推薦）**，還是 **方案 A（同卡共用 `PROP-SWORD-01`，強調「救他與殺友的是同一把越劍」之象徵呼應）**？
2. **執行路線（先獨立 DEMO-03 vs 直進 EP-01）與目擊大媽資產去留？**  
   - 若先跑 **DEMO-03**：`LOC-TAIHU-DAWN` 與大媽聲音（請擇：**ElevenLabs 客串 TTS ~300 字** 或 **10 秒台灣真人乾錄 0 字**；視覺直接沿用 `S2_first.jpg` 零新圖）升級為 `P0-DEMO03`，緊接 `SM-8` 後即產；  
   - 若跳過 DEMO-03 **直進 EP-01**：維持 `LOC-TAIPEI-STREET-2022` 街頭版，大媽定妝＋聲線改列 `DROP/P2`，直衝 EP-01 全套 P0/P1。
3. **`PROP-SWORD-01` 握柄細節與 `S00`「出鞘一寸」手勢定調？**  
   已鎖定之 `fanli-outfit03-front.jpg`／`45.jpg` 左腰越劍為「暗舊鑄銅圓首素柄（無厚纏繩）」。請確認：① `PROP-SWORD-01` 是否**錨定 `OUTFIT-03` 既有劍型**（素柄或極薄低調暗麻細纏）以保 S00↔S13 連戲；② `S00`「出鞘一寸」ECU 採 **左手拇指頂劍格出鞘一寸**（單手左腰構圖最自然，直接呼應 S02/S03 左手按空腰間）還是 **左手按鞘、右手跨腰抽出一寸**（標準雙手反拔）？
