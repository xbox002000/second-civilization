# 《第二次文明》場景資產登記表（Location Registry）

> **文件狀態**：現行有效（場景層唯一權威規格文件，v1.0，2026-11-28）  
> **對齊規格**：`EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §2.2、`STORYBOARD-SPEC-V2.md`（v2.4）§二／§3.C.1、`COSTUME_REGISTRY.md`  
> **管理原則**：一景一 ID（`LOC-{PLACE}-{TIME/ERA}`），同景多角度統一歸檔於 `{loc_id}_{angle_id}`；僅通過 LOC-QC-1 七項全數驗收後方得轉 `LOCKED`；二進位母圖存於生產 VM `~/drama-line/casting/scenes/{loc_id}/`（既有 `LOC-ALLEY-NIGHT` 保留於 `~/drama-line/demo02/loc/`），不進 git repo。

---

## 總覽索引

| Loc ID | 名稱 | 時間層 | 複用層級 | 光線鎖 ID | 狀態 | 母圖數 | 預設 Roomtone |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`LOC-ALLEY-NIGHT`** | 藍調入夜窄巷（DEMO-02 既有） | `2022` | `single_episode` | `LK-ALLEY-NIGHT` | **LOCKED** | 1 張 | `alley_night_wet_48k` |
| **`LOC-TAIHU-NIGHT`** | 太湖夜岸蘆葦水濱（S00 夜行按劍） | `春秋` | `single_episode` | `LK-TAIHU-NIGHT` | **LOCKED** | 1 張 | `taihu_night_reed_48k` |
| **`LOC-TAIHU-DAWN`** | 太湖晨霧獨舟空座（S01 / S16b / DEMO-03 S0） | `春秋` | `multi_episode` | `LK-TAIHU-MIST` | **LOCKED** | 1 張 | `taihu_dawn_water_48k` |
| **`LOC-TAIPEI-STREET-2022`** | 2022 台北陰天傍晚街頭騎樓＋長椅（正反打） | `2022` | `single_episode` | `LK-TAIPEI-DUSK22` | **LOCKED** | 2 張（`_main`/`_rev`） | `taipei_street_crowd_48k` |
| **`LOC-FANLI-STUDIO-26`** | 范蠡 2026 台北深夜小套房（常駐主場三角度） | `2026` | `series_hq` | `LK-STUDIO-NIGHT26` | **LOCKED** | 3 張（`_desk`/`_window`/`_tabletop`） | `studio_night_hum_48k` |
| **`LOC-YUE-COURT`** | 春秋晚期越國朝堂大殿空座 | `春秋` | `multi_episode` | `LK-COURT-TORCH` | **LOCKED** | 1 張 | `ancient_hall_torch_48k` |
| **`LOC-WENZHONG-GATE`** | 春秋晚期越國大夫文種府門與門內玄關 | `春秋` | `single_episode` | `LK-COURT-TORCH` | **LOCKED** | 1 張 | `ancient_hall_torch_48k` |

---

## 逐卡凍結規格與 LOC-QC-1 紀錄

### 卡片 00（既有）：`LOC-ALLEY-NIGHT` — 藍調入夜窄巷

```yaml
loc_id: "LOC-ALLEY-NIGHT"
name: "藍調入夜窄巷（DEMO-02 / SM-8 基準場景）"
time_layer: "2022"
recurrence: "single_episode"
status: "LOCKED"
used_in_episodes: ["DEMO-02", "DEMO-02-V2", "SM-8", "DEMO-03(optional)"]
light_lock_id: "LK-ALLEY-NIGHT"
default_roomtone_id: "alley_night_wet_48k"
aspect_ratio: "9:16"
no_people_rule: true
ref_images:
  - angle_id: "main"
    path: "~/drama-line/demo02/loc/e3a9ae98-2106-4fc2-8e30-2bbaf65e4491_1.jpg"
```

---

### 卡片 01：`LOC-TAIHU-NIGHT` — 太湖夜岸蘆葦水濱

```yaml
loc_id: "LOC-TAIHU-NIGHT"
name: "太湖夜岸蘆葦水濱"
time_layer: "春秋"
recurrence: "single_episode"
status: "LOCKED"
used_in_episodes: ["EP-01:S00"]

light_lock_id: "LK-TAIHU-NIGHT"
key_light_spec: "冷藍清寒夜月漫射天光（6500K）覆蓋暗墨水面與岸邊蘆葦，僅遠處對岸隱約透出數點極微小暗橘紅追兵火把光點（絕不入人影、絕不過曝）"
target_lab_range:
  bg_L_range: [6.0, 20.0]
  bg_b_range: [-10.0, 1.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["深墨夜湖藍黑", "冷青灰夜霧與濕泥蘆葦", "極遠岸微弱暗橘紅火點"]

spatial_anchors:
  - "前景左右岸緣：自然叢生之枯褐暗影蘆葦與濕潤暗泥岸線"
  - "中景：深沉靜謐泛微弱月光的暗黑太湖水面與薄夜霧"
  - "遠景對岸：低平遠山輪廓與 3 點極遠微弱橘紅火把光點（零人形剪影）"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "平視 35mm，岸邊蘆葦前景、中景水面開闊留白供范蠡夜行按劍調度"
    purpose_shots: ["S00"]

default_roomtone_id: "taihu_night_reed_48k"
acoustics_profile: "open_lakeside_night_reeds_gentle_water_lap"

no_people_rule: true
forbidden_elements:
  - "任何人物、追兵剪影、船夫、手部（遠岸僅許微小火把光點）"
  - "任何現代路燈、電線桿、高樓反光、現代遊船或水泥護岸"
  - "任何文字、浮水印、過曝亮白反光（blowout > 5%）"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "春秋晚期深夜太湖冷寂荒涼湖岸空景，前景暗影蘆葦濕岸、中景深墨月光湖面與薄霧、遠岸僅三點微弱橘紅火把光點，無人物無現代物"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/LOC-TAIHU-NIGHT/loc-taihu-night.jpg"
    resolution: "768x1376"
    seed: 407816067
    bg_L: 12.10
    bg_b: -3.72
    whole_L: 11.56
    whole_b: -3.51
    blowout_pct: 0.00
    sha256: "89148d44c216295e86700bbacc135bd444c1ae589ed953b1eb6cd5183b86e259"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: N_A
    notes: "bg_L=12.10, bg_b=-3.72, blowout=0.00%; 0 people, 3 tiny far-shore torch dots only, authentic wild reeds & dark Taihu shore."
```

---

### 卡片 02：`LOC-TAIHU-DAWN` — 太湖晨霧獨舟空座

```yaml
loc_id: "LOC-TAIHU-DAWN"
name: "太湖晨霧獨舟空座"
time_layer: "春秋"
recurrence: "multi_episode"
status: "LOCKED"
used_in_episodes: ["EP-01:S01", "EP-01:S16b", "DEMO-03:S0"]

light_lock_id: "LK-TAIHU-MIST"
key_light_spec: "破曉前冷灰藍柔和漫射晨霧天光（6800–7500K），水面平靜泛冷灰銀反光，遠山隱沒於厚重水墨感實拍白青晨霧，零直射日光與過曝"
target_lab_range:
  bg_L_range: [40.0, 58.0]
  bg_b_range: [-14.0, -4.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["冷青灰水墨晨霧", "暗濕舊木船身深褐", "蒼白微冷湖面銀灰"]

spatial_anchors:
  - "中前景：一艘春秋樸素暗舊無漆實木小舟（烏篷以外之開放木舟），清楚呈現對面空無一人的橫木空座（供 S01／S16b 呼應構圖）"
  - "中遠景：遼闊平靜太湖湖面、層疊淡青灰遠山剪影與厚實晨霧"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "舟內略低平視 35mm，船頭與對面空座居下中景，上方大面積留白晨霧與遠山"
    purpose_shots: ["S01", "S16b", "DEMO-03:S0"]

default_roomtone_id: "taihu_dawn_water_48k"
acoustics_profile: "open_lake_dawn_still_water_distant_mist"

no_people_rule: true
forbidden_elements:
  - "任何船夫、人物、人影、手部或衣物遺留"
  - "任何現代機動船、現代救生衣、塑膠桶、鐵橋或高樓天際線"
  - "任何文字、浮水印、過曝刺眼日出白光（blowout > 5%）"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "春秋晚期破曉太湖冷藍灰晨霧空景，前景素樸暗舊實木獨舟明確呈現對面空座，平靜湖面與遠山沒入清冷濃霧，無人無現代物"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/LOC-TAIHU-DAWN/loc-taihu-dawn.jpg"
    resolution: "768x1376"
    seed: 573510462
    bg_L: 50.37
    bg_b: -9.15
    whole_L: 43.33
    whole_b: -7.76
    blowout_pct: 0.00
    sha256: "6cab19a6f6e2053950df0c02f316ae10003414736faebfbea04240e84f9ff3d"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: N_A
    notes: "bg_L=50.37, bg_b=-9.15, blowout=0.00%; 0 people, weathered wooden skiff with clear opposite empty wooden bench & misty Taihu hills."
```

---

### 卡片 03：`LOC-TAIPEI-STREET-2022` — 2022 台北陰天傍晚街頭騎樓與長椅

```yaml
loc_id: "LOC-TAIPEI-STREET-2022"
name: "2022 台北陰天傍晚街頭騎樓與長椅"
time_layer: "2022"
recurrence: "single_episode"
status: "LOCKED"
used_in_episodes: ["EP-01:S02", "EP-01:S03", "EP-01:S04a", "EP-01:S04b", "EP-01:S04c"]

light_lock_id: "LK-TAIPEI-DUSK22"
key_light_spec: "台北深秋冷青灰陰天傍晚漫射天光（6200–6800K），搭配微弱街燈與遠景散焦車燈冷暖點綴，濕潤舊柏油地面與騎樓陰影低飽和克制，絕無過曝"
target_lab_range:
  bg_L_range: [22.0, 38.0]
  bg_b_range: [-9.0, 0.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["台北濕冷灰青水泥與馬賽克騎樓柱", "深灰舊柏油路面", "微弱遠景冷白與暖黃散焦燈斑"]

spatial_anchors:
  - "前景／中景：典型台北舊式灰白馬賽克磁磚騎樓柱與街邊深灰長椅（供 S02/S03 靠柱與長椅坐姿調度）"
  - "中遠景：台灣街頭鐵窗格、舊式公寓立面、人行道與濕灰柏油馬路，遠方建築完全散焦且零可讀招牌"
  - "反打角 `_rev`：180° 轉回望向騎樓走廊縱深、長椅與街角路柱，預留右上空間供 S03/S04a SYS-01 全息投影站位"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "平視 35mm，沿人行道望向騎樓柱、街邊長椅與冷陰天台北街景縱深"
    purpose_shots: ["S02", "S04b", "S04c"]
  - angle_id: "rev"
    camera_axis: "平視 35mm 180° 反打角，自街側微仰望回騎樓柱、長椅與深暗騎樓上緣留白"
    purpose_shots: ["S03", "S04a"]

default_roomtone_id: "taipei_street_crowd_48k"
acoustics_profile: "urban_sidewalk_dusk_distant_traffic_scooter_hum"

no_people_rule: true
forbidden_elements:
  - "任何路人、機車騎士、人影、背影、手部"
  - "任何可讀中文／英文／日文招牌、店名、路牌、車牌號、廣告字樣（V9 硬紅線）"
  - "東京霓虹街景、紐約黃色計程車、上海歐式建築等非台北肌理"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "2022 深秋冷陰天傍晚台北街頭空景，灰白小磁磚騎樓柱、街邊長椅、老舊鐵窗公寓與微濕柏油路面，無人物、無任何可讀招牌文字"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/LOC-TAIPEI-STREET-2022/loc-taipei-street-2022-main.jpg"
    resolution: "768x1376"
    seed: 449559011
    bg_L: 29.84
    bg_b: -4.15
    whole_L: 30.75
    whole_b: -3.97
    blowout_pct: 0.00
    sha256: "c4265d9db2e72729cf02b1c1944aabecece0d1ea313fb563c33d93c3d3792784"
  - angle_id: "rev"
    path: "~/drama-line/casting/scenes/LOC-TAIPEI-STREET-2022/loc-taipei-street-2022-rev.jpg"
    resolution: "768x1376"
    seed: 1041536895
    bg_L: 28.97
    bg_b: -4.67
    whole_L: 32.91
    whole_b: -4.38
    blowout_pct: 0.00
    sha256: "e3b01ff803078f52ec8f4f589a96a8b946a0188331bfd972b6e075bf6b412997"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: PASS
    notes: "bg_L=29.84, bg_b=-4.15, blowout=0.00%; authentic Taipei mosaic arcade pillar, bench, iron window grilles, 0 people, 0 signage/text."
  - angle_id: "rev"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: PASS
    notes: "bg_L=28.97, bg_b=-4.67, blowout=0.00%; seamless 180-deg continuity vs _main (|dL_bg|=0.87 <= 15, |db_bg|=0.52 <= 12), 0 people, 0 text."
```

---

### 卡片 04：`LOC-FANLI-STUDIO-26` — 范蠡 2026 台北深夜小套房（系列常駐主場）

```yaml
loc_id: "LOC-FANLI-STUDIO-26"
name: "范蠡 2026 台北深夜小套房"
time_layer: "2026"
recurrence: "series_hq"
status: "LOCKED"
used_in_episodes: ["EP-01:S06-S12", "EP-01:S17a-S19"]

light_lock_id: "LK-STUDIO-NIGHT26"
key_light_spec: "左側書桌啞光黑低照度微冷檯燈（4800–5200K）局部照亮桌面、刻意壓暗周圍深炭灰牆面，右後方黑色金屬寬窗透入遠處台北 101 與都會高樓強烈散焦冷青藍夜光（6200K），絕無過曝白光"
target_lab_range:
  # 實測回寫：廣角/窗景（_desk/_window）之邊緣背景暗牆 bg_L=2.32–3.66、全幀 whole_L=11.11–13.84；
  # 桌面近景（_tabletop）因檯燈照亮胡桃桌面進入取樣邊緣，whole_L=25.53（三角度全幀 |ΔL*|=14.42 <= 15、|Δb*|=3.92 <= 12；上部暗牆 top_wall_L=2.55–3.91，跨度僅 1.36）。
  bg_L_range: [2.0, 24.0]
  whole_L_range: [10.0, 26.0]
  bg_b_range: [-4.0, 1.5]
  max_blowout_pct: 5.0
color_palette_3pt: ["暗炭黑室內牆面", "冷青藍台北深夜窗景散焦光", "極克制低飽和胡桃木與空白米白紙本"]

spatial_anchors:
  - "左前／中景：深胡桃暗木極簡書桌＋深灰簡約空辦公椅＋啞光黑檯燈，桌面置木桿毛筆（擱於素色筆擱）、四本 100% 空白無字紙本筆記、數張完全虛化無字淡藍折疊紙鈔與完全息屏純黑小螢幕"
  - "右後背景：黑色金屬框夜窗，窗外台北 101 與高樓群呈強烈散焦冷青藍夜景（完全不可讀）"
  - "右側中景暗區：大片乾淨深炭灰暗牆與負形空間，供 SYS-01 全息投影站立（conversation_eyeline）及 S08 後製無框資料側卡"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "desk"
    camera_axis: "平視 35mm，書桌居下三分之一左前、右側與窗下保留乾淨深炭灰暗區"
    purpose_shots: ["S06", "S07", "S08", "S09", "S10", "S11a", "S11c", "S18a", "S18b"]
  - angle_id: "window"
    camera_axis: "平視 35mm，夜窗與窗外台北 101 冷青散焦天際線佔上中景、左下帶出同一書桌角"
    purpose_shots: ["S12", "S17a"]
  - angle_id: "tabletop"
    camera_axis: "微俯 65mm 淺景深，聚焦胡桃桌面毛筆／空白筆記／虛化鈔票，背景虛化為息屏黑螢幕與深炭暗牆"
    purpose_shots: ["S06", "S19"]

default_roomtone_id: "studio_night_hum_48k"
acoustics_profile: "small_room_dry_distant_city_hum"

no_people_rule: true
forbidden_elements:
  - "任何人物、人影、背影、手部或窗面人像倒影"
  - "任何可讀中文／英文／數字、招牌、新聞字幕、螢幕 UI、紙鈔字號或筆跡（V9 硬紅線）"
  - "過曝白光面積 >5%、豪華網美風裝潢、RGB 電競燈帶"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "2026 深夜台北極簡狹小暗色單人套房空景，暗木書桌置毛筆、空白紙本、息屏黑螢幕與低照度黑檯燈，右後黑框夜窗外散焦冷青台北天際線，右側保留深炭灰暗牆空間"

ref_images:
  - angle_id: "desk"
    path: "~/drama-line/casting/scenes/LOC-FANLI-STUDIO-26/loc-fanli-studio-26-desk.jpg"
    resolution: "768x1376"
    seed: 1499757227
    bg_L: 2.32
    bg_b: -0.65
    whole_L: 11.11
    whole_b: -1.78
    blowout_pct: 0.01
    sha256: "e4bfe1a8cc5be69c2bedd5cba6118728256afad5cbed881139f137ad18222383"
  - angle_id: "window"
    path: "~/drama-line/casting/scenes/LOC-FANLI-STUDIO-26/loc-fanli-studio-26-window.jpg"
    resolution: "768x1376"
    seed: 807896257
    bg_L: 3.66
    bg_b: -1.13
    whole_L: 13.84
    whole_b: -2.98
    blowout_pct: 0.02
    sha256: "e1bf6909ab0797dab729ba2ac6bf2e880699794fbccf7cb9681e0753a53211d9"
  - angle_id: "tabletop"
    path: "~/drama-line/casting/scenes/LOC-FANLI-STUDIO-26/loc-fanli-studio-26-tabletop.jpg"
    resolution: "768x1376"
    seed: 1006386025
    bg_L: 23.60
    bg_b: -0.55
    whole_L: 25.53
    whole_b: 0.94
    blowout_pct: 0.00
    sha256: "4c4b576b725639a4520be912bee7a2fb0ae008076697ca48880934c60f63a013"

qc1_record:
  - angle_id: "desk"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: PASS
    notes: "2.5x zoom verified V9 clean (blank notebooks, blurry unreadable bills, powered-off monitor, defocused Taipei 101 bokeh); clean dark charcoal wall negative space on right; blowout=0.01%."
  - angle_id: "window"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: PASS
    notes: "i2i anchored to _desk; |dL_bg|=1.34, |db_bg|=0.48, blowout=0.02%; identical window frame, roller blind, Taipei 101 bokeh & desk corner; 0 people, 0 reflections, 0 text."
  - angle_id: "tabletop"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: PASS
    notes: "i2i anchored to _desk; 100% matching brush, ceramic rest, 4 blank notebooks, blurry bills, matte lamp & dark bokeh wall. 3-angle whole-frame |dL*|=14.42 <= 15, |db*|=3.92 <= 12, bg_b span=0.58, top_wall_L span=1.36 (note: border-ring bg_L=23.60 reflects lamp-lit tabletop filling bottom edge in CU framing)."
```

---

### 卡片 05：`LOC-YUE-COURT` — 春秋晚期越國朝堂大殿空座

```yaml
loc_id: "LOC-YUE-COURT"
name: "春秋晚期越國朝堂大殿空座"
time_layer: "春秋"
recurrence: "multi_episode"
status: "LOCKED"
used_in_episodes: ["EP-01:S13", "EP-01:S14a", "EP-01:S15b"]

light_lock_id: "LK-COURT-TORCH"
key_light_spec: "殿側低矮氧化青銅高燈與暗銅火盆搖曳暖琥珀燭火光（2500K），搭配微淡青煙與高反差深褐木柱暗影，絕無過曝白焰"
target_lab_range:
  bg_L_range: [4.0, 18.0]
  bg_b_range: [0.0, 8.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["深黑褐先秦素木方柱與木樑", "冷灰白素灰泥側牆與暗木地板", "克制暖琥珀銅燈火光與淡青煙"]

spatial_anchors:
  - "前景中央：素色編織蒲席（空席）與低矮深褐髹漆木案几，案上僅置一隻素面暗舊青銅爵杯（直供 S14a／S15b 朝堂空座視覺母題）"
  - "中景兩側：對稱素樸深暗實木方柱與石礎、兩列無人矮案蒲席、氧化青銅高燈與銅火盆"
  - "遠景：幽暗深遠大殿軸線空間，零匾額、零紅柱、零龍飾"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "平視 35mm 對稱軸線構圖，前景空席矮几、中景柱廊火光、上部外露木樑充足留白"
    purpose_shots: ["S13", "S14a", "S15b"]

default_roomtone_id: "ancient_hall_torch_48k"
acoustics_profile: "large_timber_hall_subtle_torch_crackle_quiet_reverb"

no_people_rule: true
forbidden_elements:
  - "任何君臣、侍衛、人物、剪影或手部"
  - "明清紅牆黃瓦、雕龍金柱、高腳桌椅、絲綢帷帳、懸掛書法字畫或匾額（嚴守春秋晚期先秦考據）"
  - "任何可辨漢字、篆文、標誌或過曝火光（V9）"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "春秋晚期約西元前 473 年素樸深暗木構越國朝堂大殿空景，粗獷黑褐方柱、外露木樑、灰泥素牆、鋪地蒲席與低矮暗漆木几空座、青銅高燈暖琥珀微光與淡煙，無人物無匾額無明清元素"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/LOC-YUE-COURT/loc-yue-court.jpg"
    resolution: "768x1376"
    seed: 871823775
    bg_L: 6.96
    bg_b: 2.57
    whole_L: 12.13
    whole_b: 3.64
    blowout_pct: 0.00
    sha256: "28d0b843318ef9c109365f6703381c0ab1a3ca0351ebd2e1772c46701c758505"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: N_A
    notes: "bg_L=6.96, bg_b=+2.57, whole_L=12.13, blowout=0.00%; 100% period-authentic pre-Qin dark timber hall with empty rush mats, low lacquer tables & bronze jue; 0 people, 0 plaques/text, 0 Ming/Qing anachronisms."
```

---

### 卡片 06：`LOC-WENZHONG-GATE` — 春秋晚期越國大夫文種府門與門內玄關

```yaml
loc_id: "LOC-WENZHONG-GATE"
name: "春秋晚期越國大夫文種府門與門內玄關"
time_layer: "春秋"
recurrence: "single_episode"
status: "LOCKED"
used_in_episodes: ["EP-01:S14b", "EP-01:S15a"]

light_lock_id: "LK-COURT-TORCH"
key_light_spec: "門廊兩側古樸鐵銅壁燈架暖琥珀火光（2500K）與門內微暖內室火光相呼應，對比門外深冷暗夜灰石階陰影，與 LOC-YUE-COURT 同鎖 LK-COURT-TORCH（跨景 |Δwhole_L|=0.33、|Δwhole_b|=0.45）"
target_lab_range:
  bg_L_range: [4.0, 18.0]
  bg_b_range: [-2.0, 6.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["未上漆深褐粗木門扇與椽樑", "冷灰粗鑿石階與素夯土灰牆", "暖琥珀門廊壁燈與內室微光"]

spatial_anchors:
  - "前景：粗鑿深灰石階與石門檻（供 S14b 竹簡信送抵府門調度）"
  - "中景：半掩厚重未上漆深褐雙扇實木大門，門內微露木柱、素色蒲席與空矮木几（供 S15a 文種背影讀信調度）"
  - "門楣與兩側：純素粗木門楣、外露木簷椽與素灰泥牆，零匾額、零紅漆、零石獅"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "平視 35mm，微側正視半開厚木府門與石階門檻，上方留足暗木屋簷與夜空空間"
    purpose_shots: ["S14b", "S15a"]

default_roomtone_id: "ancient_hall_torch_48k"
acoustics_profile: "night_courtyard_gate_subtle_torch_crackle_quiet_wind"

no_people_rule: true
forbidden_elements:
  - "任何人物、侍衛、僕役、人影或手部"
  - "明清朱紅漆大門、金色門釘、石獅子、紅紙燈籠、門額字牌（如「文府」）、雕龍畫鳳"
  - "任何可辨漢字、篆文、標誌或過曝火光（V9）"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "春秋晚期素樸未上漆深褐厚木越國大夫府門夜空景，半開雙扇舊木門露內室蒲席矮几暖微光，兩側古樸銅壁火把、粗鑿灰石階、素灰泥牆，無人物無匾額無朱漆紅燈籠"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/LOC-WENZHONG-GATE/loc-wenzhong-gate.jpg"
    resolution: "768x1376"
    seed: 937423317
    bg_L: 7.07
    bg_b: 0.00
    whole_L: 12.46
    whole_b: 3.19
    blowout_pct: 0.04
    sha256: "c0d81c28bf2db48f395f5b4a6919032254c6d40e61767f8d8fa1cb53d2f5bf29"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: N_A
    notes: "bg_L=7.07, bg_b=0.00, whole_L=12.46, whole_b=+3.19, blowout=0.04%; matches LOC-YUE-COURT LK-COURT-TORCH within |dWhole_L|=0.33 & |dWhole_b|=0.45; authentic pre-Qin rough timber gate, stone threshold & ajar inner vestibule; 0 people, 0 plaques/text."
```
