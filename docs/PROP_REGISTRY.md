# 《第二次文明》道具資產登記表（Prop Registry）

> **文件狀態**：現行有效（道具層唯一權威規格文件，v1.0，2026-11-28）  
> **對齊規格**：`EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §2.1、`STORYBOARD-SPEC-V2.md`（v2.4）§3.C.1、`COSTUME_REGISTRY.md`  
> **管理原則**：一物一 ID（`PROP-{TYPE}-{NN}`），僅通過 PROP-QC-1 六項全數驗收後方得轉 `LOCKED`；二進位參考圖存於生產 VM `~/drama-line/casting/props/{prop_id}/`，不進 git repo。

---

## 總覽索引

| Prop ID | 名稱 | 階層 | 狀態 | 允許時代 | 禁用時代 | 參考圖數 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`PROP-SWORD-01`** | 范蠡春秋青銅越劍 | `hero` | **LOCKED** | `春秋` | `2022`, `2026` | 3 張（三態） |
| **`PROP-SWORD-02`** | 越王禮制青銅賜劍 | `insert` | **LOCKED** | `春秋` | `2022`, `2026` | 1 張（捧賜態） |
| **`PROP-BAMBOO-01`** | 春秋無字素面竹簡 | `recurring` | **LOCKED** | `春秋` | `2022`, `2026` | 2 張（展開／半捲） |
| **`PROP-COIN-01`** | 古銅方孔圓錢（現代信物） | `recurring` | `PENDING` *(P2)* | `2022`, `2026` | `春秋` | 0（EP-01 不擋；嚴禁裁 R2C2） |

---

## 逐卡凍結規格與 QC-1 紀錄

### 卡片 01：`PROP-SWORD-01` — 范蠡春秋青銅越劍

```yaml
prop_id: "PROP-SWORD-01"
name: "范蠡春秋青銅越劍"
tier: "hero"
status: "LOCKED"
used_in_episodes: ["EP-01:S00", "EP-01:S13(OUTFIT-03)"]
linked_outfits: ["FANLI-OUTFIT-02", "FANLI-OUTFIT-03"]

allowed_eras: ["春秋"]
forbidden_eras: ["2022", "2026"]
forbidden_outfits: ["FANLI-OUTFIT-01"]

dimensions_cm: "全長約 58–62 cm；劍身 46–50 cm；劍柄 10–12 cm；鞘寬 4.5–5 cm"
scale_reference: "劍柄長度約成年男子單掌寬 1.15 倍；收鞘斜佩左腰時，鞘尾止於左大腿中段，絕不拖及膝下"
materials_and_finish: "暗舊氧化青銅（零亮金／零鏡面不鏽鋼）、啞光深褐黑髹漆木鞘配舊銅劍珌與雙細銅箍"
silhouette_key_parts:
  - "圓盤首素面氧化暗舊青銅柱柄（錨定 fanli-outfit03-45.jpg）"
  - "緊湊舊銅窄劍格（無大型浮雕龍虎護手）"
  - "暗啞深褐黑髹漆直鞘＋細銅箍＋舊銅劍珌"
  - "無銘文雙刃氧化青銅劍身（清晰菱形中脊、霧面氧化光澤）"

wear_side: "anatomical_left_hip"
hold_hand:
  press_or_steady: "anatomical_left_hand"
  draw_1inch: "left_thumb_push_guard OR two_hand_cross_draw(L-scabbard + R-hilt)"
required_states:
  - state: "sheathed_hip"
  - state: "hand_on_hilt_ecu"
  - state: "unsheathed_1inch"

forbidden_elements:
  - "任何劍身銘文、篆字、漢字、數字、浮水印（V9 硬紅線）"
  - "漢代長鐵環首刀、唐橫刀、明清龍紋護手、劍穗流蘇、亮銀不鏽鋼、亮金塗裝"
  - "現代服裝／2022–2026 場景出現實劍（僅限按空腰間）"

asset_contract:
  role: "prop"
  default_owns: ["prop_appearance"]
  default_never_inherit: ["studio_backdrop", "source_lighting", "overlay_text"]
zh_prompt_anchor: "春秋晚期短制暗舊青銅越劍，圓首素柄、窄銅格、啞光深褐黑髹漆劍鞘配舊銅珌，無銘文無劍穗"

ref_images:
  - state: "sheathed_hip"
    path: "~/drama-line/casting/props/PROP-SWORD-01/prop-sword-01-sheathed-hip.jpg"
    resolution: "768x1376"
    seed: 753199284
    sha256: "6c442edbcc820f171bffba561cdd8ad3ffbcf6bcabe26820f6b44556ed3d292b"
  - state: "hand_on_hilt_ecu"
    path: "~/drama-line/casting/props/PROP-SWORD-01/prop-sword-01-hand-on-hilt-ecu.jpg"
    resolution: "768x1376"
    seed: 849614483
    sha256: "027f91a8f45388de2f7b681b0adcad9ae9a72125dcfe24aaf2727a2f265535c8"
  - state: "unsheathed_1inch"
    path: "~/drama-line/casting/props/PROP-SWORD-01/prop-sword-01-unsheathed-1inch.jpg"
    resolution: "768x1376"
    seed: 826619030
    sha256: "f45f66bc8bbdd2b54a8a23f8b5f000697cecc0556dfa00b9fa0719b426ea0e5d"

qc1_record:
  - state: "sheathed_hip"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "Anchored directly to fanli-outfit03-45.jpg + OUTFIT-02 linen robe; left hip diagonal hang, mid-thigh stop, 5 natural fingers each hand, 0 text."
  - state: "hand_on_hilt_ecu"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "Anatomical left hand (5 clean fingers, no watch/ring) gripping identical pommel/hilt/guard; cuff trim and jade bi match state 1."
  - state: "unsheathed_1inch"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "1-inch matte oxidized bronze blade with crisp diamond ridge exposed; right-hand cross-draw grip (5 clean fingers); 0 blade inscription."
```

---

### 卡片 02：`PROP-SWORD-02` — 越王禮制青銅賜劍（Creator 2026-11-28 拍板獨立建卡）

```yaml
prop_id: "PROP-SWORD-02"
name: "越王禮制青銅賜劍"
tier: "insert"
status: "LOCKED"
used_in_episodes: ["EP-01:S16a"]
linked_outfits: []

allowed_eras: ["春秋"]
forbidden_eras: ["2022", "2026"]
forbidden_outfits: ["FANLI-OUTFIT-01"]

dimensions_cm: "全長約 58–62 cm，橫置於折疊玄黑素面絲帛布上"
scale_reference: "雙手橫托於胸前平舉，劍身全長略寬於雙掌間距，明確呈現君王賜死禮儀尺度"
materials_and_finish: "暗舊氧化青銅配細密先秦雲雷幾何暗紋劍格、深玄黑帶極暗沉朱褐漆光澤髹漆禮鞘、雙細暗紋銅箍與暗銅珌；完全無亮金、無銘文"
silhouette_key_parts:
  - "較精緻細密先秦雲雷暗紋氧化銅格（與 PROP-SWORD-01 素窄格一眼區隔）"
  - "圓盤首素雅青銅柱柄"
  - "深玄黑暗沉朱褐髹漆禮鞘配雙細銅箍與紋飾銅珌"
  - "底襯折疊整齊之啞光玄黑素面絲帛布，內侍雙手平托"

wear_side: "handheld_only"
hold_hand:
  present: "two_hands_horizontal_on_black_silk"
required_states:
  - state: "ceremonial_granted"

forbidden_elements:
  - "任何劍身或劍鞘銘文、篆字、漢字、數字（V9 硬紅線；《史記》賜劍不名屬鏤）"
  - "亮金塗裝、鏡面不鏽鋼、明清龍鳳浮雕、仙俠光效、劍穗流蘇"
  - "現代服裝／2022–2026 場景出現；人臉入鏡（S16a 嚴守只拍手與劍）"

asset_contract:
  role: "prop"
  default_owns: ["prop_appearance"]
  default_never_inherit: ["studio_backdrop", "source_lighting", "overlay_text"]
zh_prompt_anchor: "春秋晚期越王禮制青銅賜劍，細密暗紋氧化青銅格、深漆禮鞘配暗銅珌，無銘文無亮金，內侍雙手橫托於折疊玄黑素帛布上"

ref_images:
  - state: "ceremonial_granted"
    path: "~/drama-line/casting/props/PROP-SWORD-02/prop-sword-02-ceremonial-granted.jpg"
    resolution: "768x1376"
    seed: 1755511532
    sha256: "1c6eb0524df08b7186ecfcd5554dd00208eb3339bc044c798c686b31deef067a"

qc1_record:
  - state: "ceremonial_granted"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "Unmistakable royal ceremonial Yue sword distinct from PROP-SWORD-01; cloud-thunder bronze guard, deep dark lacquer scabbard, folded matte black silk, clean two-handed presentation, 0 inscriptions, 0 faces."
```

---

### 卡片 03：`PROP-BAMBOO-01` — 春秋無字素面竹簡

```yaml
prop_id: "PROP-BAMBOO-01"
name: "春秋無字素面竹簡"
tier: "recurring"
status: "LOCKED"
used_in_episodes: ["EP-01:S14b", "EP-01:S15a"]
linked_outfits: ["FANLI-OUTFIT-02"]

allowed_eras: ["春秋"]
forbidden_eras: ["2022", "2026"]
forbidden_outfits: ["FANLI-OUTFIT-01"]

dimensions_cm: "單簡寬約 1.0 cm、長約 22 cm，約 11–14 簡編聯成卷"
scale_reference: "單手可握半捲卷筒，展開寬約 14–16 cm"
materials_and_finish: "天然做舊暖黃褐啞光竹片、自然竹絲纖維與包漿、上下兩道深米褐天然細麻繩編聯；表面 100% 空白無字"
silhouette_key_parts:
  - "天然做舊暖黃褐窄竹片（非紙張、非線裝書）"
  - "上下兩道細麻繩規整編聯＋繫卷細麻繩"
  - "100% 空白無墨素面（一切文字由後製處理或鏡頭留白）"

wear_side: "tabletop"
hold_hand:
  read_or_deliver: "two_hands_open_or_single_hand_rolled"
required_states:
  - state: "open"
  - state: "half_rolled"

forbidden_elements:
  - "任何墨字、漢字、篆書、偽字符、印章、筆畫痕跡（V9 硬紅線）"
  - "線裝書、宣紙、塑膠光澤"

asset_contract:
  role: "prop"
  default_owns: ["prop_appearance"]
  default_never_inherit: ["studio_backdrop", "source_lighting", "overlay_text"]
zh_prompt_anchor: "春秋晚期天然做舊暖黃褐素面竹簡，上下雙道細麻繩編聯，竹面完全空白無墨無字"

ref_images:
  - state: "open"
    path: "~/drama-line/casting/props/PROP-BAMBOO-01/prop-bamboo-01-open.jpg"
    resolution: "768x1376"
    seed: 1514202061
    sha256: "878efdb238dc9d9049174d96e0237b317f6d06f2d8b920e4cb1e2af9f0680f31"
  - state: "half_rolled"
    path: "~/drama-line/casting/props/PROP-BAMBOO-01/prop-bamboo-01-half-rolled.jpg"
    resolution: "768x1376"
    seed: 567894861
    sha256: "c856f943f9fcce8d4daeec3faaed4db0c03b0231d12a7ccd32ed77997852a455"

qc1_record:
  - state: "open"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "11 aged bamboo slips with authentic twin braided hemp cords; 100% blank uninscribed surface, neutral studio light."
  - state: "half_rolled"
    verdict: "PASS (6/6)"
    checks: { era_accuracy: PASS, scale_and_proportion: PASS, handedness_and_wear_side: PASS, state_completeness: PASS, v9_zero_text: PASS, material_lighting_neutrality: PASS }
    notes: "100% material & cord match to open state, left side naturally half-rolled with hemp tie cord, 0 ink/characters."
```

---

### 卡片 04：`PROP-COIN-01` — 古銅方孔圓錢（現代限定信物｜P2 延後）

```yaml
prop_id: "PROP-COIN-01"
name: "古銅方孔圓錢（現代限定信物）"
tier: "recurring"
status: "PENDING"  # P2：EP-01 0 鏡剛需，不擋開拍；日後獨立生成無字磨損面
used_in_episodes: ["EP-02+"]
linked_outfits: ["FANLI-OUTFIT-01"]

allowed_eras: ["2022", "2026"]
forbidden_eras: ["春秋"]
forbidden_outfits: ["FANLI-OUTFIT-02", "FANLI-OUTFIT-03", "FANLI-OUTFIT-04"]

dimensions_cm: "直徑 3.8–4.5 cm、厚邊方孔"
materials_and_finish: "暗褐氧化古銅包漿，錢面字跡磨損至 100% 不可辨讀（V9 硬紅線）"
forbidden_elements:
  - "嚴禁裁切 fanli-modern-charactercard-expressions.png R2C2（該格錢面含可辨偽字「通寶」，違反 V9）"
  - "春秋古裝戲 100% 禁用（春秋晚期尚未出現方孔圓錢）"
ref_images: []
qc1_record: []
```
