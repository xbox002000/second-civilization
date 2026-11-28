# 分鏡規格 v2.4.1（整合定版）

> **版本**：**v2.4.1 FINAL**（2026-11-28 整合定版；含 Creator 2026-11-28 21:18 `SYS-01` 顯現導演定調修訂）。  
> **版本沿革**：
> - **v2.0**：Muse 起草 → agy 工程討論（`STORYBOARD_SPEC_V2_AGY_MEMO.md`）→ Creator 拍板雙檔原子鏡契約（schema 2.0）。
> - **v2.0 + 附錄 A**：運鏡控制四級分層與 H3／Flow／Wan 方言（`CAMERA_WORKFLOW_AGY_MEMO.md`）。
> - **v2.1 + 附錄 B**：導演層、V12 護欄與 QC-D 閘（`DIRECTOR_LAYER_AGY_MEMO.md`、DEMO-02 QC-D 常規五條）。
> - **v2.2 + 附錄 C + §九**：工作流修訂 AMD-01～07 與 Demo 邊界條款（`WORKFLOW_V2_AMENDMENT_AGY_MEMO.md`）。
> - **v2.3**：整合 SM-7A（4 槽 H3 Ref2VA 實測三條件）、Clay Test（L3 白膜實測四條件）與 Seedance 生態方法／電影提示詞工藝收斂案（Items 1–7）。
> - **v2.4**：整合 **附錄 D（導演鏡頭覆蓋與豎屏短劇節奏 V14 閘門，含 Creator `INSERT_ECU_DURATION` 插鏡時長紀律）**、**§C.4 AMD-05 v3（`SYS-01` 生成主導＋後製精修，經 `SM-8` 6/6 GO 實證放行）**、以及 **H3 官方規格對賬修訂**（`H3_MODE_EXCLUSION`、`H3_MIN_DURATION ≥4.0s` 墊幀、`5+17k` 實長進位檢核、產線品質帽措辭校準）。
> - **v2.4.1（本版）**：整合 **Creator 2026-11-28 21:18 `SYS-01` 顯現導演定調**（`SYS01-MANIFESTATION-DIRECTION.md`）：① **§C.4 尺度表收斂為平視單一預設**（`eye_level_in_front`，`0.90–1.00×`、站位主角面前同一地平面、下身消散點落地面附近；退役仰視英雄尺度 `manifestation_hero` `1.25–1.45×`，含 2022 初現）；② **顯現語法改「剪輯硬切入為主（`editorial_cut_in`）／鏡內光凝成形降為偶爾點綴（`in_shot_materialize`）」**，明訂**前鏡三要素預告組（冷青光 cue＋范蠡視線轉向＋`sound_drop`）**為標準入場鋪墊；③ **§A.9 `SM-8`** 改註載體技術 PASS、構圖已被本定調取代（superseded composition）；④ `preflight_gate.py` 新增非阻斷 Advisory **`SYS01_MANIFESTATION_DIRECTION`**。
>
> **定位**：定義「一集分鏡包」的資訊結構與驗證契約（`script_pack.json` schema **2.4**，向下相容 2.0–2.3；對齊 `edit_manifest.json` v1.1 與 DESIGN v1.4／待同步 v1.5）。  
> **不可動搖紅線**：一切可讀文字後製合成（V9）；事實分層由 beat 繼承（V10）；seed 不入鏡級欄位；H3 端正向編譯／零裸否定靜止詞；全面 ElevenLabs TTS 對白路線。

## 零、受控聖經檔案索引（Bible Index｜v2.4.1 更新）

| 檔案路徑 | 狀態 | 職責 |
|---|---|---|
| `bible/anchors/FANLI.yaml` | **LOCKED (v2.3)** | 范蠡跨鏡身分與時代條件錨點唯一準據（眉疤、時代髮型、現代方孔錢、左腕舊銅錶）與 QC 鍵位映射 |
| `bible/anchors/SYS01.yaml` | **LOCKED (v2.4.1)** | `SYS-01` 跨鏡身分、黑大衣＋紅圍巾、全息光學五要素、V9 禁面板紅線、平視面前單一預設尺度（`eye_level_in_front`）與剪輯切入顯現語法（AMD-05 v3 ＋ 2026-11-28 定調） |
| `bible/performance/micro_expressions.yaml` | **LOCKED (v2.3)** | 4 分區 × 21 核心微表情有界詞表、L1–L4 強度標尺與反 AI 假臉衛生清單 |
| `bible/camera/named_shots.yaml` | **LOCKED (v2.4)** | 18 個高頻 9:16 受控鏡型庫與 `verified_9x16_status` |
| `voices/FANLI.yaml`（repo 對齊 `voices/FANLI.yaml`） | **LOCKED** | 范蠡 ElevenLabs 聲線單點鎖定（`FANLI-CAND-F`，`eleven_v4`），嚴禁鏡級覆寫 |
| `bible/director/playbook.md` | 累積制 | 導演手記（一條裁示一條目，每集闡述前必讀） |
| `COSTUME_REGISTRY.md` / `MASTER_FACE_DECISION.md` | **LOCKED** | 服裝資產卡（`FANLI-OUTFIT-01..04`）與身分層唯一基準（`fanli-master-B-userface.png`） |
| `docs/PROP_REGISTRY.md` / `docs/LOCATION_REGISTRY.md` | **ACTIVE (v2.4)** | 一物一 ID 道具卡（`PROP-*`）與場景母圖／光線鎖卡（`LOC-*`）及 QC-1 紀錄 |

---

## 一、架構：兩層制 × 三檔分離

```text
episodes/EP{NNN}/
├── input/script_pack.json        # 上游核准後不可變，鎖 SHA256（schema 2.3）
│   ├── episode metadata + event_anchor + beats[]
│   ├── segments[]                # 場段層：同場共用屬性（含光線、環境音底床）只填一次
│   └── shots[]                   # 扁平原子鏡：1 筆 = 1 張首幀 = 1 支生成片
├── plan/production_state.json    # 執行期可變檔，不汙染上游核准
│   └── shots_state[shot_id]      # TTS 實測、最終路由與降級、實檔指標、H 層狀態、previs_artifacts
└── plan/edit_manifest.json       # 組裝契約（v1.1）：裁切、音軌（A1–A4）、SYS-01 合成與母帶規格
```

設計原則：
1. **原子鏡（嚴禁單鏡多切鏡）**：廢除 `sub_shots`；明文駁回外部提示詞資料之「單鏡 `[Shot 1]/[Shot 2]` 多切鏡時間碼寫法」。複合拍一律拆成原子鏡（`S16a`／`S16b`），每鏡恰有一張首幀與一支輸出片——對齊 LTX 預演、QC-1/QC-2 Diff 表與 `edit_manifest`。
2. **共用上移**：場景、時間層、光線基底、氛圍、環境音底床、音樂 cue、世界反應預設放場段層；鏡級只填差異與覆寫，禁止同場重複抄寫。
3. **prompt 是衍生物**：由欄位按引擎方言與電影優先序編譯（§五、§A.4）；人工覆寫僅限敘事／構圖／資產語意層，且必填 `prompt_override_reason`（記錄於 `production_state`）；主稽核站為 Stage 3 QC-1 首幀門與 Stage 5 QC-2 成片門。
4. **連戲靠綁定與繼承**：資產 ID 有序綁定＋作用域契約＋場段光線繼承＋鏡尾狀態交接。尾幀鏈為例外手段（見 V4），不是預設。

---

## 二、場段層 `segments[]`

| 欄位 | 必填 | 規則 |
|---|---|---|
| `segment_id` | ● | `SEG-##` |
| `scene_id` | ● | 場景資產 ID（須於 assets_manifest 登錄且 LOCKED） |
| `time_layer` | ● | 本系列：`春秋`／`2022`／`2026` |
| `lighting_base` | ● | 本段光線基底：明確光源方向＋光質＋色溫感；段內各鏡預設繼承 |
| `light_lock_id` | ● | 段級光線鎖定 ID（如 `LK-ALLEY-NIGHT`，全段共用；原附錄 B.2 併入正文） |
| `atmosphere` | ○ | 純視覺：空氣感、有限克制色盤傾向 |
| `ambience` | ●（v2.3 升級） | 段級環境音底床規格，見 §2.1（向下相容 v2.0 純字串，字串視為 `note` 並預設 `library_roomtone`） |
| `bgm_cue` | ○ | 音樂 cue ID；預設 `none` |
| `world_reaction_default` | ○ | 段級世界反應基調（原附錄 B.2 併入） |
| `public_exposure` | ○ | `private`／`semi`／`public`（配 V12c） |
| `anomaly_level` | ○ | `low`／`mid`／`high`（配 V12c） |
| `audio_groups[]` | ○ | 跨鏡共用 TTS 群組：`{group_id, speaker, delivery_mode, lines[]}`；供畫外音跨鏡與 J/L-cut 對齊字幕（嚴禁內含 `voice_id`/`model_id` 覆寫） |
| `segment_pacing_profile` | ●（v2.4） | `hook`／`escalation`／`confrontation`／`revelation`／`climax`／`release_bridge`／`chase_tension`（對接附錄 D.2 節奏帶） |
| `axis_plan` | ◐（v2.4） | `≥2` 人物鏡段必填：`{char_id: {screen_side, default_facing}}`（180° 軸線鎖，配 R9） |
| `target_shot_density_per_10s` | ○（v2.4） | `[min, max]` 覆寫段級預設節奏帶 |

### 2.1 段級環境音底床規格 `segments[].ambience`（v2.3 新增）

每場段須指定一條連續環境底床，跨場段以 **0.25s crossfade** 銜接；**禁止以單支短片原音硬循環撐全集**（取代 DEMO-02 手寫 `volume=0.07` 循環 S1 原音之舊做法）：

```json
"ambience": {
  "source": "library_roomtone | retained_native_bed | generated_sfx_bed | silent",
  "asset_id": "alley_night_wet_48k",
  "target_db": -24.0,
  "note": "Humid Taipei narrow alley night room tone with faint distant city hum"
}
```

- **`library_roomtone`（預設首選）**：使用 `audio_lib/roomtone/` 之 CC0 連續底噪——零循環接縫、零人聲漏音、跨引擎一致。
- **`retained_native_bed`（嚴格受限）**：僅允許用於 `voice_mode == "none"` 且（H3 時）`non_diegetic_music: N/A` 之純動作／空景／白膜鏡，須先確認 `native_voice_verified_clean: true`（F7 檢核），鏡間強制 `0.20–0.30s` crossfade；凡 `voice_mode == "tts"` 之對白鏡 **100% 禁止**抽取該鏡原生音軌作底噪。
- **`generated_sfx_bed`（選配）**：由音效生成或純環境生成片抽出之定製底噪，須先歸檔至 `audio_lib/roomtone/` 跨鏡複用。
- **`silent`**：僅供刻意的完全靜音段（若同段有 `sound_drop` 特效拍點則 preflight 發 `WARN`）。

---

## 三、原子鏡層 `shots[]`（schema 2.3）

必填性：● 必填　○ 選填　◐ 條件必填

### A 敘事
| 欄位 | 必填 | 規則 |
|---|---|---|
| `shot_id` | ● | `S##` 或 `S##a/b`（拆鏡）；順序即放映順序 |
| `segment_id` | ● | 所屬場段；場景／時間層／光線／音場由此繼承 |
| `beat_id` | ● | 主 beat（畫面敘事的事實層）；圖卡類另由 overlay 各自綁 beat（見 G） |
| `beat_function` | ● | HOOK／SETUP／ESCALATION／JOLT／TURN／PAYOFF／CLIFF／BRIDGE，一鏡一主功能 |
| `priority` | ● | hero／standard／insert（決定引擎路由與抽卡預算） |
| `shot_intent` | ● | 一句話，這鏡要觀眾感覺什麼（原 B.2 併入） |
| `action` | ● | 一個主動作：誰＋身體部位＋可觀察物理幅度；動詞轉折 ≤1 次，超過即拆鏡 |
| `start_pose` | ◐ | AI 鏡必填：第一幀定格的起手姿勢（靜態可讀），供 `image_prompt` 使用，並須能銜接前鏡 `end_state` |
| `subject_facing` | ◐ | 角色鏡必填：`front`／`left`／`right`／`back`——臉部特徵左右基準（如左眉疤）以此為準，防鏡像翻車 |
| `face_visible` | ● | bool；背影／遠景／手部特寫如實填 false |
| `microexpression` | ◐ | `face_visible=true` 時必填，粒度到可觀察物理描述；禁美顏塑膠肌／過演詞（見 `bible/performance/micro_expressions.yaml`） |
| `performance_beat` | ● | `{from, trigger, to, deliberate_hold, intensity?: "L1"|"L2"|"L3"|"L4", lexicon_ids?: string[], intensity_override_reason?: string}`（v2.3 擴充，見附錄 B.2） |
| `dialogue[]` | ◐ | 每句一筆：`{line_id, speaker, line, tts_emotion_tags[], delivery_mode: on_camera/off_camera/voiceover, pause_after_sec, delivery?: {pre_pause_sec?, pace?, volume?}}`。`voiceover` 不驅動口型。**音色單點鎖定（v2.3）**：`speaker` 唯一映射至 `voices/{SPEAKER}.yaml`（`LOCKED`），嚴禁在 `dialogue[]` 覆寫 `voice_id`/`model_id`，且不在影片 `video_prompt` 寫逐句音色綁定（全 TTS 路線下屬 no-op）。`FANLI` 預設 `delivery: {pre_pause_sec: 0.5, pace: "measured", volume: "low"}`。 |
| `end_state` | ◐ | AI 鏡必填：鏡尾可觀察狀態（人物位置姿勢、道具在誰手裡、門／燈／屏幕狀態）；`cpu_card` 填固定值 `card_hold` |

### B 攝影（v2.4 覆蓋欄位升級）
| 欄位 | 必填 | 規則 |
|---|---|---|
| `shot_size` | ●（v2.4） | 純距離枚舉：`WS`／`MLS`／`MS`／`MCU`／`CU`／`ECU`／`CARD`（向下相容 2.0–2.3：`ELS`/`LS`→`WS`、`2S`→`MS`+`is_two_shot`、`OTS`→`MCU`+`is_ots`、`INSERT`→`ECU`+`is_insert`） |
| `framing_flags` | ○（v2.4） | `{is_ots, is_reverse, is_two_shot, is_insert}`（未填預設全 `false`） |
| `angle_v` | ● | eye／low／high／bird／worm |
| `angle_h` | ● | front／three-quarter／profile／back／OTS／POV／reverse |
| `movement` | ●（v2.4） | 詳見附錄 A.2 擴充結構（`{type, direction?, speed, amplitude?, end_shot_size?, easing?, named_shot?, motivation}`；一鏡一運鏡；v2.4 非 CARD 必填 **`motivation`** 6 枚舉，見附錄 D.1.1） |
| `control_method` | ● | `L1_prompt`（預設）／`L2_flf`／`L3_clay_ref2v`／`L3_clay_controlnet`／`L4_post_25d`（見附錄 A.3） |
| `camera_psychology` | ● | `stable_control`／`handheld_anxiety`／`subjective_pov`／`predator_stalk`／`cold_observe`／`intimate_drift`（見附錄 B.2／B.4） |
| `coverage_role` | ●（v2.4） | `establish`／`action`／`speaker`／`reaction`／`insert_detail`／`turn_jolt`／`peak_hold`／`card_evidence` |
| `emotional_peak` | ●（v2.4） | bool；標記該段情緒峰值鏡（配 R1b） |
| `dialogue_mode` | ●（v2.4） | `none`／`on_camera`／`off_camera`／`voiceover`／`l_cut_carry` |
| `screen_side` / `axis_turn_trigger` | ◐ / ○（v2.4） | `left`／`center`／`right`（人物鏡必填）；同角翻向觸發詞（選填，配 R9） |
| `internal_event_sec` / `hold_justification` | ○ / ◐（v2.4） | `float[]`（鏡內可觀察事件時碼，配 No-Dead-Air）；`hold_justification`（`dread`/`peak_emotion`/`held_reaction`/`performance_hold`/`voiceover_density`/`final_image`，長鏡與 `>2.0s` 插鏡說明） |
| `sys01_in_frame` / `sys01_scale_mode` | ◐（v2.4.1） | 凡 `SYS-01` 入鏡必填：`sys01_in_frame: true`＋`sys01_scale_mode`（預設合法值僅 **`eye_level_in_front`**〔向下相容別名 `conversation_eyeline`，皆為 `0.90–1.00×` 平視面前同地平面〕與 **`solo_cu`**；舊 `manifestation_hero` 仰視懸空已退役，填寫觸發 Advisory `SYS01_MANIFESTATION_DIRECTION`），詳見 §C.4 |
| `sys01_apparition_mode` | ○（v2.4.1） | `SYS-01` 入鏡選填（別名 `apparition_mode`）：**`editorial_cut_in`**（入場唯一預設，前鏡三要素預告後硬切入已成場）｜`already_present`（同場延續鏡已在場）｜`in_shot_materialize`（降為偶爾點綴，未附理由觸發 Advisory `SYS01_MANIFESTATION_DIRECTION`） |
| `camera_notes` | ○ | 焦段感等僅入 prompt 文字的備註 |
| `previs_brief` | ◐ | 僅 L3 必填，1–2 句走位與起迄機位要點 |

### C 參照綁定（v2.3 作用域契約與未見側重建規則）
| 欄位 | 必填 | 規則 |
|---|---|---|
| `asset_refs` | ● | 有序 `[{asset_id, role, media_kind?, owns?, never_inherit?, scope_target?, scope_window?}]`（向下相容 v2.0 `{asset_id, role}`）。`role` ∈ `first_frame`／`scene`／`character`／`prop`／`previs_video`；**順序固定 `first_frame/scene → characters → props`**（即 V3 餵圖序；`previs_video` 獨立送 `<Video 1>`）。`cpu_card` 可空。 |
| `outfit_id` | ◐ | 每位出鏡角色必填，引服裝登記表 ID（如 `FANLI-OUTFIT-02`） |
| `first_frame` | ● | `{source: generated / derived_shot / generated_dual_lock / l3_clay_frame0 / ref_shot / prev_tail / none_cpu_card, ref_shot_id?, scene_angle_id?}`；同段非首鏡／反打強制依 AMD-04（§C.3） |
| `last_frame` | ◐ | 僅 `gen_mode = i2v_first_last` 時必填 |
| `chain_trim_override` | ◐ | 啟用 `prev_tail` 或 `i2v_first_last` 時必填 |

#### §3.C.1 `asset_refs[]` 角色預設契約表（免手填基準，v2.3）
`owns[]` 與 `never_inherit[]` 未填時由編譯器與 `preflight_gate.py` 按角色預設自動補齊；具跨時代參考圖、含烘焙道具母圖（如帶竹簡之 `fanli-master-ancient-front.jpg`）或 L3 白膜片者**必須顯式覆寫**：

| `role` | 預設 `owns[]` | 預設 `never_inherit[]` |
|---|---|---|
| `first_frame`（QC-1 已核准首幀） | `["framing_pose", "environment_lighting"]` | `["identity_override", "motion_lock", "overlay_text"]` |
| `scene`（空景母圖 `LOC-*`） | `["environment_lighting", "style_palette"]` | `["native_audio", "overlay_text"]` |
| `character`（同時代定裝母圖） | `["identity", "costume"]` | `["studio_backdrop", "source_lighting", "card_layout", "overlay_text", "native_audio"]` |
| `prop`（獨立道具卡） | `["prop_appearance"]` | `["studio_backdrop", "source_lighting", "overlay_text"]` |
| `previs_video`（L3 白膜 `<Video 1>`） | `["camera_motion", "blocking_timing"]` | `["clay_material", "environment_lighting", "identity_override", "native_audio"]` |

- **特例強制覆寫**：① 帶非本鏡道具之母圖（如空手鏡餵 `ancient-front`）必於 `never_inherit[]` 加 `"baked_prop"`；② 多格角色設定卡（`charactercard`）嚴禁未裁切單格直接餵圖；③ 跨時代參考圖必顯式縮限 `owns: ["identity"]`、`never_inherit: ["costume", ...]`。

#### §3.C.2 多參考主體與 L4 餵圖上限（v2.3 實測鎖定）
- **Colab L4 24GB（`minimax-h3-video`）**：
  - 4 槽 `ref_image_size="max"` 對白／反應鏡：圖像參考建議與實測安全上限 **≤ 4 張**（SM-7A 實測餘裕 1.85 GiB；`>4` 發 `WARN`，`>9` 為 `FAIL`）。
  - `L3_clay_ref2v`（`ref_image_size="match"`）：硬上限 **≤ 3 張圖 ＋ 1 支 `ref_video_0 ≤ 0.35 MP`**（Clay Test 實測餘裕 1.31 GiB；超標即 `FAIL`）。
- **單鏡獨立出鏡角色主體**：建議 **≤ 2 人**（3 人以上或雙人多動作易串染，優先拆正反打原子鏡）。

#### §3.C.3 人物參考預設範圍、未見側重建與退役水平翻轉法（v2.3）
1. **預設範圍**：`role="character"` 預設涵蓋完整可見角色（骨相＋傷痕＋髮型＋體型＋服裝配飾）。僅在借用他套服裝／他時代母圖之臉部時（如古裝鏡餵現代 `fanli-master-B-userface.png`），必顯式縮限 `owns: ["identity"]`、`never_inherit: ["costume", "studio_backdrop", "source_lighting"]`。
2. **未見側結構重建**：視角為母圖未直接拍攝之角度時，嚴格依同套母圖剪裁、布料、滾邊與穿戴結構推演重建，**嚴禁發明新配件**，且手性結構絕不鏡像：
   - 春秋深衣（`OUTFIT-02/03/04`）永遠**交領右衽**（角色左襟壓右襟，正面視覺小寫 `y` 形）；
   - 傷痕永遠僅存於**解剖學左眉尾**（露右臉鏡之解剖學右眉必 100% 無疤）；
   - 現代腕錶永鎖左腕、方孔錢主歸右手、朝服短劍永鎖左腰。
3. **~~Step 0 水平翻轉法~~（v2.3 正式退役 RETIRED）**：SM-7A 實證 `tmp_flip45.jpg` 水平翻轉直接製造 `左衽` 反領與錯邊疤（`fanli-master-ancient-45R.v1-flip-defect.jpg` 已封存禁用）。嚴禁將任何水平鏡像圖作為首幀或影片參考輸入（`preflight_gate.py` 以 `FLIP_ASSET_BAN` 硬封殺）。日後補拍右側 45°／背影母圖一律以未翻轉 `userface`＋同套母圖結構重建並經 QC-1 2.5× 臉領放大核驗後鎖庫。

### D 連戲
| 欄位 | 必填 | 規則 |
|---|---|---|
| `lighting_state` | ○ | 鏡級光線覆寫；未填即繼承段 `lighting_base` |
| `continuity_override` | ○ | 僅跳場／刻意改變時填；未填即自動繼承上一鏡 `end_state` |
| `continuity_notes` | ○ | 視線方向、正反打左右位等備註 |
| `world_reaction` | ◐ | 預設繼承段級 `world_reaction_default`，偏離時必填並附理由（配 V12c） |

### E 時間
| 欄位 | 必填 | 規則 |
|---|---|---|
| `target_net_sec` | ● | 成片淨秒數（不含裁切緩衝）；生成長＝淨長＋緩衝，由 `trim_policy` 決定 |
| `trim_policy` | ● | `standard_0.5s`（頭尾各裁 0.5s，生成長＝淨長＋1.0s）／`none`／`tail_only`（尾裁 0.5s） |
| `duration_from_audio` | ● | bool；聲音先行定版後，淨長以 TTS 實測為準（回寫 `production_state`） |
| `reaction_hold_sec` | ○ | 反應拍秒數，預設 0；V2 核算自動扣除 |
| `transition_out` | ● | `{type: cut / match-cut / dissolve / hard-cut / continuous, trigger: action/eyeline/sound/object/none}`；`continuous` 為啟用尾幀鏈的唯一入口 |

### F 聲音（v2.3 升級分層 Foley 與 -14 LUFS 混音基準）
| 欄位 | 必填 | 規則 |
|---|---|---|
| `voice_mode` | ● | `tts`／`none`（本系列對白全面 TTS） |
| `ambient_source` | ● | `post_roomtone`（預設，對接段級 `library_roomtone`）／`native_keep`（**嚴限 `voice_mode=none` 且 F7 驗淨**，若 `voice_mode=tts` 觸發 `AUDIO_BED_HYGIENE` 硬駁回）／`silent` |
| `sfx` | ○ | 結構化陣列（向下相容字串清單）：`[{cue, timing_sec?, level_class: "subtle_foley"|"accent_sfx", source?: "library"|"native_extract"|"generated", asset_id?}]`；每場段精選 2–4 個關鍵物理觸點 |
| `audio_group_id` | ◐ | 本鏡對白屬跨鏡群組時必填（連回段層 `audio_groups[]`） |

#### §3.F.1 四軌混音電平基準表（校準至 `edit_manifest.json` v1.1 母帶 `-14.0 LUFS` / `True Peak ≤ -1.5 dBTP`）
| 音軌 | 來源 | 無對白基準電平 | 對白期間閃避（Duck） | `sound_drop` 拍點（0.30–0.35s） |
|---|---|---|---|---|
| **A1 對白（TTS）** | `voices/*.yaml` 鎖定 TTS | 基準 `0 dB`（幹聲歸一 `-16 ± 1 LUFS`） | — | 靜默待觸發後起聲 |
| **A2 環境底床（Ambience）** | 段級 `library_roomtone`（或合規 `retained_native_bed`） | **`-24 dBFS`**（`-22 ~ -26`；先 `volumedetect` 計補償增益，禁裸寫 `volume=0.07`） | 再降 **`-6 dB`**（落 `-28 ~ -32 dBFS`） | 壓至 **`-38 dBFS`**（20ms 斜坡，禁數位死靜爆音） |
| **A3 物理 Foley / SFX** | `audio_lib/sfx/`（按 `timing_sec` 對位） | `subtle_foley`：**`-16 dBFS`**<br>`accent_sfx`：**`-8 dBFS`**（限幅 `≤ -3 dBTP`） | `subtle_foley` 降 `-4 dB`；`accent_sfx` 錯開起聲 | `glitch_in` 於抽空結束瞬間觸發 `accent_sfx` |
| **A4 配樂（BGM，選配）** | `audio_lib/bgm/`（預設 `none`） | **`-20 dBFS`**（`-18 ~ -22`） | 再降 **`-10 ~ -12 dB`** | 同 A2 壓至 `-38 dBFS` |

### G 生成
| 欄位 | 必填 | 規則 |
|---|---|---|
| `engine_route` | ● | `flow`（Omni 1.2 Flash 預設）／`h3`／`wan`／`ltx`／`ffmpeg_card`（最終路由與降級記於 `production_state`） |
| `gen_mode` | ● | `i2v_first`／`i2v_first_last`／`ref2v`／`cpu_card` |
| `image_prompt` | ● | §五電影優先序衍生（`cpu_card` 為卡面規格描述） |
| `video_prompt` | ◐ | 非 `cpu_card` 必填，§五與 §A.4 引擎方言衍生 |
| `face_lock_level` | ● | `strict`／`standard`／`none` |
| `lip_sensitive` | ● | bool；初值可由 `face_visible && on_camera && shot_size ∈ {MCU,CU,ECU}` 自動預標，QC-1.5 定案 |
| `vfx_beats[]` | ○ | `[{type: glitch_in|light_shift|sound_drop|env_reaction|composite_ui, exec_layer: gen_prompt|post_ffmpeg|assembly}]`（原 B.2 併入） |
| `visual_text_overlay[]` | ○ | `{type: fullscreen_card/lower_third/diegetic_screen/corner_badge, text, placement, start_sec, end_sec, beat_id}`；生成畫面永不含文字（V9） |

### H 生產狀態（位於 `plan/production_state.json`，不入 `script_pack.json`）
`state`（planned／frames_ready／generated／selected／done／failed）、`fail_reason`、`takes[]`、`selected_take`、TTS 實測秒數與 `audio_ref`、`audio_offset_ms`、最終路由與降級紀錄、英文雙 prompt 與 `prompt_override_reason`、首尾幀實檔指標、`previs_artifacts`、`qc_checks` 結果。`script_pack.json` 內僅保留 `production_mode`（`normal`／`demo`／`skip_image`／`reuse`）一欄供上游表態。

---

## 四、引擎 × 模式相容表（v2.4 實測回填＋H3 互斥紅線）

| `gen_mode` | `flow`（`omni-1.2-flash` 預設；`veo-fast/quality` 2026-12-05 退役） | `h3`（`minimax-h3-video` on Colab L4 24GB；官方原生 9 圖／3 影／3 音／4–15s） | `wan`（閘道） | `ltx` | `ffmpeg_card` |
|---|---|---|---|---|---|
| `i2v_first` | ✓（`omni-1.2-flash` 原生最長 15s，V1 穩態上限 7.5s 生成；`veo-lite` 最長 8s） | ✓（Base `MiniMaxH3ImageToVideo`，**禁與 `ref2v` 混用**） | ✓ | ✓（預演，淨 ≤2.5s） | — |
| `i2v_first_last` | △ 待驗（SM-5） | △ **end_frame 未驗證（SM-4）；架構級 100% 禁與 `ref2v` 混用（`H3_MODE_EXCLUSION`）** | △ 未驗證 | — | — |
| `ref2v` | ✓（Omni 1.2 最多 7 ref；R2V 禁與 i2v 混用） | **✓ 已實測鎖定（`MiniMaxH3ReferenceToVideo`，100% 禁接 `last_frame`/`L2_flf`）**：L4 4 槽 `max` 對白／反應基線（SM-7A：`544×960` 8-step `4.67m` 0 OOM）；L3 白膜 `ref_video_0 ≤ 0.35 MP`＋3 圖 `match` `≤5s`（Clay Test：`7.18m` 0 OOM）；**最短生成 `≥4.0s (107f)`、幀數按 `5+17k` 網格實算** | △ 待驗 | — | — |
| `cpu_card` | — | — | — | — | ✓（圖卡／無框資料側卡） |

`i2v_first_last` 在 SM-4／SM-5 通過前列**例外模式**，僅偽長鏡與 match-cut 得用且須填 `chain_trim_override`。**H3 互斥硬規則（`H3_MODE_EXCLUSION`）**：官方與 ComfyUI 節點層（`MiniMaxH3ImageToVideo` vs `MiniMaxH3ReferenceToVideo`）架構級禁止混用 `last_frame`/`L2_flf` 與 `ref2v`；`<Picture 1>` 首幀屬 Ref2VA 軟參考，不屬 FL2V 混用。

---

## 五、prompt 衍生公式（v2.3 電影優先序編譯規則）

> **取代說明**：~~v2.0 沿用舊 Seedance 10 段順序（將光線置於第 6 位 look）~~ 已由本版 **電影優先序（Light → Lens/Camera → Observable Action → Restrained Palette → Sound）** 取代；各引擎方言再依 §A.4 落地。

1. **Flow（`omni-1.2-flash` / `nano2`）——全面套用電影優先序**：
   - **`image_prompt`（定格於 `start_pose`）**：`9:16 vertical live-action frame.` → `[1. 光源方向＋光質＋色溫 (light_lock/lighting_base)]` → `[2. 焦段感＋景別＋角度＋主體 start_pose/subject_facing]` → `[3. 場景環境與服裝／錨點細節]` → `[4. 有限克制調色盤與材質肌理 (atmosphere)]` → `[Avoid: 精簡視覺禁詞，必含 no readable text，禁裸否定靜止詞]`。
   - **`video_prompt`**：`Live-action cinematic, [生成秒數]s 9:16 single shot.` → `[1. 明確光源方向與光質]` → `[2. 焦段感＋景別＋單一主運鏡＋幅度/速度]` → `[3. 主體可觀察物理動作＋微表情＋物理真實細節（布料/呼吸）＋鏡尾 end_state]` → `[4. 有限克制調色盤與材質]` → `[5. Sound: 環境音＋物理音效；無對白/無配樂明示]` → `[Avoid: 精簡視覺禁詞＋anti_ai_face_hygiene，禁裸否定靜止詞]`。
2. **H3（Ref2VA 六段式／Base 三段式）**：**保留官方外殼段序不變**，於 `detailed_description`（或 `integrated_multimodal_description`）段落內部強制「光線＋景別運鏡 → 可觀察動作與微表情／`<d>` 對白 → 調色與 `end_state`」前移，並將 `never_inherit[]` 轉為正向替換句（詳見 §A.4）。
3. **Wan（2.2）**：極簡動作無聲方言：`[1. 光線短語], [2. 景別＋單一主運鏡] of [3. 主體＋可觀察物理動作], [4. 克制色調]`；不輸出 `Sound:` 段，所有 `never_inherit[]` 於 Stage 3 首幀淨化。

---

## 六、驗證規則總表（QC-0 / `preflight_gate.py`）

### 6.1 硬閘規則（任一 `FAIL` 退碼非零、阻斷送出）

| 規則 | 內容 | 自動化 |
|---|---|---|
| **V1 時長（v2.4 產線品質帽＋H3 17-frame 實長檢核）** | 以「生成總長＝淨長＋裁切緩衝」對齊產線品質抗漂移帽與 Colab L4 穩態包絡（**註：以下為產線品質帽與 L4 穩態上限，非 H3 模型 15s 物理上限**）：<br>• **`ltx`**：淨長 `≤ 2.5s`<br>• **`h3`（`L3_clay_ref2v` on L4）**：**生成長硬上限 `≤ 5.0s`**（`standard_0.5s` 淨 `≤ 4.0s`／`tail_only` 淨 `≤ 4.5s`；超時須轉 A100/G4，對齊 Clay Test Condition 3）<br>• **`h3`（4 槽 `max` 對白 CU on L4）**：建議淨長 `≤ 4.5s`（生成 `≤ 5.5s`，超標發 `WARN`）、**產線品質與 L4 穩態硬上限生成實長 `≤ 6.5s`（依 17-frame 時間網格 `5+17k` 實算幀長檢核：`a ≤ 5.8s` 穩落已測 `141f = 5.875s`；`a = 6.2s` 實進位 `158f = 6.583s` 將觸發硬頂或需 A100/SM-9 驗證）**<br>• **`H3_MIN_DURATION` 墊幀保護（v2.4）**：凡路由至 H3 且 `net+trim < 4.0s` 之短鏡，`preflight_gate.py` 發 `WARN [H3_MIN_DURATION]` 提示執行端 `run_stage4_h3.py` 自動墊高生成參數至 **`≥ 4.0s`（`107f = 4.46s`）**，於 Stage 6A 裁回所需淨秒數<br>• **`wan`**：硬上限生成 `≤ 6.0s`（淨 `≤ 5.0s`）<br>• **`flow`（Omni 1.2 Flash）**：硬上限生成 `≤ 7.5s`（淨 `≤ 6.5s`）<br>• **短鏡提醒（`WARN`）**：非 `is_insert`/`is_reverse`/`ECU`/`reaction`/`turn_jolt` 之 AI 鏡生成 `< 3.0s` 發 `WARN`（或任何 AI 鏡 `< 2.0s`）；聲音先行定版後全線以 `D_tts + 0.4s` 重跑。 | 全自動（`V1_DURATION_ENVELOPE` / `H3_MIN_DURATION`） |
| **V2 對白速率** | 可用時長＝`target_net_sec − reaction_hold_sec − 0.35s×換人輪數`；含標點 ≤5.5 字/秒、純字 ≤5.0；英文詞 1 詞≈2 漢字、數字按位數計。 | 全自動 |
| **V3 綁定與聲線單點鎖** | `asset_refs` ≥1（`cpu_card` 除外）且順序 `first_frame/scene → characters → props`；資產須 `LOCKED`；`speaker` 聲線檔須 `LOCKED` 且嚴禁 `dialogue[]`/`audio_groups[]` 覆寫 `voice_id`/`model_id`（`VOICE_AUTHORITY_LOCK`）。 | 全自動 |
| **V4 幀鏈** | 僅 `transition_out.type=continuous` 或明示 match-cut 得用 `prev_tail`/`i2v_first_last`，且 `chain_trim_override` 必填。 | 格式自動／理由人工 |
| **V6 一鏡一運鏡／一主動作** | `movement.type` 受控枚舉硬閘；主動作動詞轉折 >1 次告警拆鏡；禁單鏡多切鏡時間碼。 | 半自動 |
| **V7 鏡尾狀態** | AI 鏡 `end_state` 非空且含可觀察狀態；`cpu_card` 填 `card_hold`。 | 半自動 |
| **V8 微表情** | `face_visible=true` 而 `microexpression` 空＝不過；voiceover 鏡有臉仍須填。 | 全自動 |
| **V9 文字紅線（v2.4 AMD-05 v3）** | 生成畫面零可讀文字、零浮動面板、零圓形 HUD 光環；舊 `SYS01_BAN` 退役，改由 **`SYS01_TEXT_PANEL_BAN`** 硬攔面板／HUD／文字詞與 **`SYS01_PROJECTION_ANCHOR_REQ`** 強制全息光學詞＋黑大衣紅圍巾＋尺度模式；`avoid`/`避免：` 必含禁字禁面板詞。 | 全自動＋雙門人工 |
| **V10 事實綁定** | `shot.beat_id` 與每個 `visual_text_overlay[].beat_id` 指涉 FACT 者必具非空 `source_ids`。 | 全自動 |
| **V11 運鏡分級護欄** | 單集 L3 >2 鏡須 Creator 特批、>3 鏡告警；快線（T2）出現 L3 硬駁回；`L2_flf` 必配 `gen_mode=i2v_first_last`；H3 嚴禁 `gen_mode=ref2v` 混帶 `last_frame` 或 `control_method=L2_flf`（**`H3_MODE_EXCLUSION`**）。 | 全自動 |
| **V12a–c 導演硬閘** | V12a 雙門對稱光線（QC-1＋QC-2 留存＋爆光 `<5%`）；V12b `performance_beat` 狀態變化＋詞庫強度／景別耦合與反 AI 假臉（`PERF_INTENSITY_CONFLICT`、`AI_FACE_TABOO`）；V12c 公開高異常場須有 `world_reaction`。 | 全自動＋雙門人工 |
| **V13 一維度一權威（v2.3 新增）** | 單鏡所有參考資產對每個 `(dimension, scope_target)` 僅允許**唯一邏輯權威組（`owner_group_key`）**；互斥權威硬駁回（`V13_AUTHORITY_CONFLICT`）；擁有 0 維度之孤兒資產硬駁回（`V13_ORPHAN_ASSET`）。同角色、同鎖定年齡帶、同 `outfit_id` 之多視角母圖（如 `ancient-cu`＋`ancient-45`＋`ancient-45R`）屬**同一權威組**，不計衝突。 | 全自動（`preflight_gate.py`） |
| **V14 鏡頭覆蓋與短劇節奏閘（v2.4 新增，附錄 D）** | `COVERAGE_SCALE_VARIETY`（R1a）、`COVERAGE_PEAK_CLOSEUP`（R1b）、`COVERAGE_SCALE_STAGNATION`（R1c，升級 V12d）、`COVERAGE_DETAIL_CADENCE`（R2）、`COVERAGE_NON_DIALOGUE_CAP`（R3，與 `SCALE_JUMP_BAN` 聯檢限 Δrank=1）、`COVERAGE_TWO_PERSON_DIALOGUE`（R4）、`COVERAGE_SEGMENT_KINETIC`／`COVERAGE_MOVE_MOTIVATION`（R5a/b，擴充 V12e）、`COVERAGE_DEAD_AIR`（無死氣硬上限）、`COVERAGE_ECU_RATIONING`（R8）、`COVERAGE_AXIS_DISCIPLINE`（R9）；另有 Advisory `COVERAGE_PACE_ENVELOPE`（R7）與 **`INSERT_ECU_DURATION`**（插鏡／ECU 淨長 >2.0s 無理由說明發 `WARN`）。 | 全自動（`preflight_gate.py`） |
| **AMD-01/04/05/07＋v2.3/v2.4 契約閘** | `ROUTING_LOCK`、`PROMPT_HYGIENE_NEGATION`、`PROMPT_HYGIENE_DIALECT`、`TWO_SHOT_MICRO_MOTION`、`LIP_SENSITIVE_DIALOGUE`、`SYS01_TEXT_PANEL_BAN`、`SYS01_PROJECTION_ANCHOR_REQ`、`SAME_LOCATION_DERIVATION`、`SCALE_JUMP_BAN`、`H3_MODE_EXCLUSION`、`ASSET_CONTRACT`、`REF_COUNT_BUDGET`、`ERA_ANCHOR_CONFLICT`、`CROSS_ERA_CHAR_SCOPE`、`FLIP_ASSET_BAN`、`UNSEEN_SIDE_GUARD`、`AUDIO_BED_HYGIENE`。 | 全自動（`preflight_gate.py`） |

#### §6.1.1 V13 九大受控維度與權威組判定表（v2.3）
| `dimension` | `scope_target` | 唯一權威組鍵（`owner_group_key`） | 典型衝突案例（必駁回） |
|---|---|---|---|
| `identity` | 角色 ID（如 `FANLI`） | `char_id:age_band`（同人同齡多視角共享 1 組） | 混餵 `fanli-master-A`（28 歲）與 `fanli-master-B`（38 歲）；或 `first_frame` 與 `character` 同宣稱 `identity` |
| `costume` | 角色 ID | `char_id:outfit_id`（同套多視角共享 1 組） | 混餵 `OUTFIT-01` 與 `OUTFIT-02` 且未將前者縮限為 `owns=["identity"]` |
| `framing_pose` | `"SHOT"` | 單一 `asset_id` | 兩張不同構圖圖同宣稱 `framing_pose` |
| `environment_lighting` | `"SHOT"` | 單一 `asset_id`（`first_frame` 或 `LOC-*`） | `asset_refs[]` 同時帶 `role="first_frame"` 與 `role="scene"` 且未擇一（多圖 H3 鏡由 `<Pic 1>` 首幀擁有、移去冗餘 `LOC-*` 省 L4 VRAM） |
| `camera_motion` | `"SHOT"` | 單一來源（L3:`previs_video`／L1:`movement`／L2:`flf`） | L3 白膜鏡同時給出衝突運鏡片 |
| `blocking_timing` | `"SHOT"` | 單一來源 | 兩支參考片同控走位節奏 |
| `prop_appearance` | 道具 ID | 單一 `asset_id` | 兩張不同樣式道具卡同控同一道具 |
| `audio_timbre` | 說話者 ID | 單一 `voices/{speaker}.yaml` | 單集／單鏡指派兩組聲線 |
| `style_palette` | `"SHOT"` | 段級 `light_lock_id`＋單一 `scene` 來源 | 混入不同色盤／畫風參考圖 |

### 6.2 Advisory 警告規則（`WARN`，不阻斷放行）
- **V5 狀態連續**（LLM／人工初檢）、**V12d 鏡頭多元**（連 3 鏡景別角度重心全同）、**V12e 運鏡心理一致性**。
- **v2.3 電影工藝四項自檢**（去重已由 V1/V2/V6 硬鎖項目，零退出碼影響）：
  1. `CRAFT_LIGHT_SPECIFICITY`：缺乏光源方向／光質詞，或含空泛詞 `cinematic lighting`。
  2. `CRAFT_OBSERVABLE_ACTION`：`action`/`microexpression` 含純抽象情緒詞而缺身體動作，或含空泛詞 `epic`/`masterpiece`/`8K`/`stunning`。
  3. `CRAFT_PALETTE_NO_FLUFF`：缺克制色盤／材質線索，或含空泛詞 `cinematic color grade`。
  4. `CRAFT_SOUND_DESIGNED`：非 `cpu_card` 鏡既無段級 `ambience`、亦無 `sfx`，且 H3 `overall_soundscape` 空或 `N/A`。
- **范蠡 `L4` 強度警戒**（`PERF_INTENSITY_CEILING`）、**L4 H3 `max` >4 圖或 >5.5s 生成提示**、**`H3_MIN_DURATION` 短鏡自動墊至 ≥4.0s (107f) 提示**、**`COVERAGE_PACE_ENVELOPE` 場段 ASL／反節拍器 CV 提示**、**`INSERT_ECU_DURATION`（v2.4 Creator 裁示：任何 `INSERT`/`ECU` 尺幅淨長 `> 2.0s` 且無 `hold_justification`〔如 `performance_hold`/`voiceover_density`/`final_image`〕者發 `WARN`）**、**`SYS01_MANIFESTATION_DIRECTION`（v2.4.1 Creator 顯現定調：凡 `SYS-01` 入鏡仍用已退役 `manifestation_hero`、`angle_v ∈ {low, worm}`、或未附點綴理由使用 `in_shot_materialize` 者發 `WARN`）**、**帶道具母圖未標 `baked_prop` 提示**。

---

## 七、範例（EP-01 拆鏡寫法）

- **S04 拆二**：`S04a`（對白鏡：她說完「范蠡先生」，`face_visible: true`，對白三句、`pause_after_sec` 逐句標）＋`S04b`（反應鏡：無對白、`action` 只寫僵住與轉身、`reaction_hold_sec` 全鏡）。
- **S11 拆三**：`S11a`（h3 對白）＋`S11b`（`cpu_card` 全屏新聞卡，overlay 綁 F5 FACT beat）＋`S11c`（h3 對白）。
- **S16 拆二＋音組**：段層定義 `audio_groups: [{group_id: AG-S16, speaker: FANLI, delivery_mode: voiceover}]`；`S16a` 捧劍特寫（`face_visible: false`）＋`S16b` 湖上閉眼（`first_frame.source=ref_shot, ref_shot_id: S01`、微表情 `z3_closed_still_lips`、voiceover 閉唇句）。

---

## 八、銜接與待辦

- **欄位分責**：上游（編劇端）填敘事契約；下游（生產端）於 `production_state.json` 與 `edit_manifest.json` 補工程實態，互不覆寫。
- **待辦（不屬本規格）**：① DESIGN 升 v1.5 同步 schema 2.3 與 `edit_manifest` v1.1；② SM-1／SM-4／SM-5 冒煙測試清零前，`i2v_first_last` 維持例外模式；③ VM 補裝 Node `>= 22.19`＋`npm`/`npx` 以啟用本機 CozyClay CLI/MCP（見 §A.5）；④ EP-01 正式分鏡包依 v2.3 重鑄（經 Gate A3）。

---

## 九、Demo／試拍模式邊界條款（Demo-Mode Boundary Clause｜零豁免紅線）

> **立法目的**：杜絕「試水心態」演變為隱形規格降級（DEMO-01 跳段光線、DEMO-02 跳路由與比對 QC）。Demo 模式不是脫離管線的手工捷徑，而是**同一條產線加上 `"production_mode": "demo"` 旗標的精簡執行檔**；凡未遵守下方「永不可跳清單」之產出，**不得作為工作流能力驗證或設計評核依據**。

### 9.1 Demo 模式「可以跳過」的項目（僅限產量與精修）
1. **集數與鏡頭規模**：可縮減為 1 個 segment、3–6 顆原子鏡（不須湊滿 12–20 鏡全集）。
2. **階段 0.5 完整闡述散文**：可改走 §B.1 快線「3 分鐘極簡導演卡」，但結構化欄位（`light_lock_id`、`camera_psychology`、`vfx_beats`）仍須如實填入 `script_pack.json`。
3. **階段 3.5 LTX 動態預演（QC-1.5）**：總長 ≤30 秒之單段 demo 可跳過 GPU 預演，改以「首幀＋TTS」1 分鐘 CPU 快檢替代。
4. **多倍抽卡預算（N）**：非英雄鏡／非特寫鏡可降至 N=1；英雄特寫鏡仍建議 N=2（不回寫正式 `yield_log.jsonl`）。
5. **階段 6B 精修與階段 7 社群封裝**：可跳過精校字幕樣式、片尾 Truth Ledger 聲明卡、多平台比例轉製與 Google Drive 歸檔（母帶電平與環境底床仍依 §3.F.1 執行）。

### 9.2 Demo 模式「永遠不可跳過」的項目（零豁免紅線）
1. **結構化契約與前置驗證閘**：必須建立精簡 `script_pack.json` 並通過 `preflight_gate.py`（V1–V14、引擎方言編譯、禁裸否定詞、雙人微動作條款）；Stage 0.5 雖可省去長散文，但**逐鏡覆蓋表（附錄 D.1）與結構化覆蓋欄位永不可跳過**，並須通過 V14 覆蓋硬閘；**嚴禁手寫臨時 bash 散文 prompt 直接調用生成工具**。
2. **身份載體分工與 V3 餵圖順序**：依 §C.1 分工表強制綁定身份載體與 V3（`first_frame/scene → characters → props`）槽位；嚴禁單首幀 i2v 承接 `lip_sensitive=true` 特寫或跨尺幅大幅推臉。
3. **同場景衍生規則**：同段第 2 鏡起嚴禁以「空景母圖＋文字」獨立重生已出場人物或背景，必走 Path A／B／C（§C.3）。
4. **資產歸屬紅線**：V9 畫面禁字禁面板紅線與 `SYS-01` 全息投影生成主導＋後製精修規格（§C.4 AMD-05 v3）全程生效，無試拍例外。
5. **QC-1 跨鏡首幀比對門**：必須由 `diff_sheet_gen.py --mode qc1` 產出高解析 `qc1_diff_sheet.jpg`（含 2.5× 臉領放大），完成靜態不變量核對並寫入 `qc1_gate.json (PASS)`，始得啟動影片生成。
6. **QC-2 跨鏡成片幀驗收門**：必須由 `diff_sheet_gen.py --mode qc2` 產出 `qc2_diff_sheet.jpg`，逐鏡完成六維成片抽幀驗收並寫入 `qc2_gate.json (PASS)`，始得進入粗剪與 QC-D。
7. **引擎路由鎖定**：`lip_sensitive=true` 與 `face_lock_level=strict` 正臉特寫鏡鎖定 H3 多圖 Ref2VA（SM-7A 已驗證啟用），Demo 模式不自動豁免。若因算力暫缺由 Creator 事前明文簽核臨時降級（`creator_waiver_signed: true`＋`demo_waiver_reason`），輸出粗剪左上角須自動燒入 **`[ROUTING_WAIVED]`** 浮水印，且僅供非口型／非保臉維度參考。

---

# 附錄 A：運鏡控制與引擎方言（v2.0＋v2.3 實測整合）

## A.1 四級分層（每鏡必填一級，記於 `control_method`）

| 級 | 方法 | 每集佔比（20 鏡） | 適用鏡型 | 成本與失敗模式 |
|---|---|---|---|---|
| **L1** | 詞表提示詞（預設主力） | 65–75% | 常規對白、過肩、反應、簡單平搖／微手持、Wan 動作 B-roll | 零額外工時；轉頭角度守 ±30° 內防臉部特徵翻轉 |
| **L2** | 首尾幀差分（`i2v_first_last`） | 5–10% | 起迄構圖須精準收斂的單調移動、Match Cut | ＋1 張尾幀；須配 `trim_policy: tail_only/none` 與 `chain_trim_override`；**SM-4/5 通過前列例外模式** |
| **L3** | 白膜預演＋H3 Ref2VA | **嚴限 0–2 鏡／集（MS/LS 非對白）** | 複雜弧線環繞、前景遮擋揭示、走位與運鏡嚴格同步、跨鏡精準同機位呼應 | **Clay Test 實測有條件採納**：L4 硬鎖 `ref_video_0 ≤ 0.35 MP`＋`match`＋`≤5s`＋`<Pic 1>` 場景錨（見 §A.5） |
| **L4** | 後製運鏡（ffmpeg） | 15–20% | 全部 `cpu_card`、≤12% 微幅數碼慢推、crash zoom 後製補救 | 0 GPU、100% 過稿；無真實視差，禁用於立體環繞 |

**快線紀律**：快線（T2）全面禁用 L3，僅走 L1＋L4。

## A.2 `movement` 欄位擴充（向後相容 v2.0）

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

- `type` ●：static／push-in／pull-out／zoom-in／zoom-out／pan／tilt／truck／pedestal／arc／track／handheld／roll／pov。
- `direction` ◐：pan／tilt／truck／pedestal／arc／roll 時填 left／right／up／down／cw／ccw。
- `speed` ●：slow／standard／fast。
- `amplitude` ○（預設 medium）：small／medium／large。
- `end_shot_size` ○：鏡尾收束景別。
- `easing` ○（預設 ease-in-out）：linear／ease-in／ease-out／ease-in-out——**僅 L3 與 L4 消費，禁寫進 L1 文字 prompt**。
- `named_shot` ○：指向 `bible/camera/named_shots.yaml` 受控 ID。

## A.3 `control_method`、V11 與 `previs_artifacts`

- `script_pack.json`：`control_method` ●（預設 `L1_prompt`）、`previs_brief` ◐（僅 L3 必填）。
- `production_state.json`：`previs_artifacts`：`{tool, project_file, ref_video_path, depth_video_path?, extracted_frame0_path?, approved_at}`。
- **V11**：見 §6.1。

## A.4 引擎 prompt 方言（v2.3 整合電影優先序＋作用域正向編譯）

1. **H3（Ref2VA 六段式／Base 三段式）——外殼嚴格保留、內部電影優先序＋正向替換**：
   - **外層段序不變**：Base 模式首行 `<Picture N>` 對齊指令＋空行，接 `integrated_multimodal_description`／`overall_soundscape`／`non_diegetic_music`；Ref2VA 嚴格六段式：`subject_definitions` → `summary`（方括號任務前綴）→ `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`。
   - **Q6 槽位分責＋`owns[]` 正向排他**：於 `subject_definitions` 與 `retention_analysis` 以正向排他句宣告各槽職權（例：`<Picture 1> defining ONLY the wet alley lighting and opening framing; <Picture 2..4> defining EXCLUSIVELY <Subject 1>'s facial identity, scar anatomy, and OUTFIT-02`）。
   - **`never_inherit[]` 嚴禁直譯否定詞（v2.3 正向替換表）**：絕不輸出 `do not inherit / no grey clay / no bamboo scroll`，一律查表轉譯寫入 `retention_analysis`／`detailed_description`：
     - `clay_material` → `rendering all surfaces in photorealistic live-action textures from <Picture 1> and <Subject 1>`
     - `studio_backdrop` / `source_lighting` → `placing <Subject 1> naturally into the environment and lighting exclusively defined by <Picture 1>`
     - `baked_prop` → `with empty hands`（或明寫本鏡實際持物）
     - `overlay_text` / `card_layout` → `clean natural live-action frame with unobstructed surfaces`
     - `native_audio` → 依 `voice_mode` 與 `non_diegetic_music: N/A` 處理
   - **`detailed_description` 內部電影優先序（v2.3）**：首句寫「光線方向與光質（`light_lock`）＋景別焦段＋單一官方原語運鏡」→ 中句寫「可觀察物理動作＋微表情＋反 AI 假臉正向膚質護欄＋`<d>[Chinese] 台詞</d>`（或畫外音閉唇固定句：`says in an off-screen voiceover: <d>[Chinese] …</d> while his lips remain completely closed.`）」→ 尾句寫「有限克制調色盤與鏡尾 `end_state`」。
   - **音樂欄**：無配樂一律 `non_diegetic_music: N/A`。
   - 參考上限（官方）：圖 ≤9、片 ≤3（總長 ≤15s）、音 ≤3；輸出 4–15s 整數秒、24 FPS、9:16（L4 實測上限見 §3.C.2 與 §6.1 V1）。
2. **Flow（`omni-1.2-flash` / `veo-lite`）**：採 §五電影優先序；`never_inherit[]` 動作類轉正向替換，純視覺偽影類（`studio_backdrop`、`card_layout`、`overlay_text`、`anti_ai_face_hygiene`）併入句尾精簡 `Avoid:`（禁動作靜止否定詞）。
3. **Wan（2.2）**：採 §五極簡無聲方言；所有 `never_inherit[]` 於 Stage 3 首幀淨化。

## A.5 L3 工具定版與 Clay Test 實測四條件（v2.3 實測採納）

> **Clay Test 結論（2026-11-28，`claytest/CLAY_TEST_RESULT.md`）**：**ADOPT WITH CONDITIONS**（0–2 顆 MS/LS 非對白英雄鏡／集）。實測原生 `MiniMaxH3ReferenceToVideo`（`ref_videos.ref_video_0`＋3 圖）在 Colab L4 達成 3–8% 軌跡緊跟與 **0.19% 灰像素（零灰模滲漏）**，毋須改新 profile 亦毋須無條件觸發 ControlNet。

**四項強制採納條件（v2.3 入規）**：
1. **條件 1 — SM-6 預演產製路徑（VM 工具缺口）**：本 VM 目前僅裝 `node v18.20.4`（低於 CozyClay 需求 `>= 22.19`）且無 `npm`/`npx`/`cclay`，故 CozyClay 本機代理自動化暫為 **BLOCKED**（非帳號牆；日後補齊 Node `>= 22.19`＋`npm`/`npx` 並驗證 SwiftShader 無頭出片時仍強制 `cclay telemetry off` 與 `cclay update --off`）。過渡期採二擇一：① Muse／Creator 於 `cozyclay.org/#try` 匯出 9:16 24fps 灰模 MP4；② 簡單走道／走位測試使用已驗證之零依賴 Python 3D 灰模算圖器（`claytest/render_clay_previs.py`）。
2. **條件 2 — 強制 `<Picture 1>` 場景錨＋正向替換（防灰模滲漏）與尾幀互斥禁令**：必以鎖定空景（`LOC-*` 或 QC-1 首幀）放 `<Picture 1>`（V3 順序）配角色母圖 `<Picture 2..3>` 及正向替換句；**禁止僅餵灰模片＋灰棚角色卡而缺場景錨**。**L3 `h3_r2v_clay` 尾幀禁令（`H3_MODE_EXCLUSION`）**：CozyClay 匯出之首幀 PNG 僅供 Stage 3 輔助產出寫實圖再作為 Ref2VA `<Picture 1>`（軟參考），**尾幀 PNG 絕不可作為 H3 `last_frame` 混進 Ref2VA 工作流**（尾幀僅供離線 QC-2 疊圖或改走純 L2 `MiniMaxH3ImageToVideo`）。已驗證預裝之 `h3-controlnet`（Depth）留作滲漏備援（`L3_clay_controlnet`）；軌跡被蒸餾壓扁時切 20-step 非蒸餾權重。
3. **條件 3 — Colab L4 嚴格記憶體包絡（SM-3）**：L4 24GB（必開 `high_mem: true`）實測峰值 `20.727 GiB` VRAM（餘 `1.307 GiB`）、System RAM 餘 `2.64 GiB`，故 L4 跑 L3 **硬鎖**：`ref_video_0 ≤ 0.35 MP`（`ImageScaleToTotalPixels`）、`ref_image_size="match"`、圖像參考 `≤ 3` 張、輸出 `0.5 MP`（`544×960`）、**生成長 `≤ 5.0s`**（可複用工作流：`claytest/workflows/h3_r2v_clay.json`）。凡超過 5s、`0.8 MP` 或需 `ref_image_size="max"` 之 L3 鏡一律轉 A100／G4。
4. **條件 4 — 景別紀律與 QC-2 服裝四項門檻**：嚴限 **0–2 顆 MS/LS 非對白走位／運鏡英雄鏡／集**（對白正臉 CU 禁用；快線 T2 禁用）。因 `match` 尺幅於 t=3.5s 曾見短暫 `左衽` 翻領，必須嚴格執行 QC-2 抽幀服裝四項核驗（必要時以 QC-1 核准首幀作 `<Picture 1>` 鎖領）。

## A.6 運鏡 QC 驗收（QC-2 硬門檻；有效區間 `[+0.5s, end−0.5s]` 抽幀）

| 級 | 比對 | 合格標準 | 不達標處置 |
|---|---|---|---|
| L1 | 三幀＋動態播放 | 方向與型別正確；景別推進與 `end_shot_size` 一致（主體高度誤差 ≤±20%）；臉部左右基準不翻轉 | 調 `amplitude`/`speed` 重抽；連 2 輪偏離則升級 L2／L3 |
| L2 | `f_0` 對首幀、`f_end` 對尾幀、`f_mid` 驗過渡 | 首尾構圖與角色一致；中段無瞬移殘影肢體扭斷 | 降級 L1 或拆兩顆原子鏡 |
| L3 | 成片與灰模同時間碼 50% 疊合 | 主體位置偏差 ≤15% 畫寬／高、視差弧線一致；**零灰模滲漏**；臉與服裝過 QC-2 | 滲漏→切 `L3_clay_controlnet` Depth；軌跡壓扁→切 20-step |
| L4 | 全段抽幀＋平台安全區遮罩 | 繁中文字 100% 清晰零裁切、避開 UI 區；zoompan 平滑無黑邊 | 改 ffmpeg 參數重算 |

## A.7 `named_shots.yaml` 庫與 A.8 EP-01 試套定案
- 維持 v2.0+A 精選 8–10 鏡型（`steady-dialogue-lock`、`slow-push-verdict`、`subtle-pull-reveal`、`handheld-jolt`、`ots-push-tension`、`arc-reveal-90`、`low-angle-authority`、`match-cut-bridge`、`crash-zoom-post`、`ken-burns-card`），標註 `verified_9x16_status`。
- EP-01 三難鏡定案不變：S01（L3，冒煙未過降 L1 Flow）、S02（L1 Flow＋L4 字卡）、S17（L1 H3 六段式 4 槽 Ref2VA）。

## A.9 開拍前冒煙測試清單（v2.3 回填實測狀態）

| 項目 | 狀態 | 實測結論 / 備註 |
|---|---|---|
| SM-1 TriPRISM 8-step 對 L1 詞表運鏡服從度 | 待辦 | 隨 DEMO-02 v2 與 EP-01 補驗 |
| **SM-2 自組 clay 工作流（`ref_video_0`）＋防滲漏** | **DONE — ADOPT WITH CONDITIONS** | `claytest/CLAY_TEST_RESULT.md`：原生 Ref2VA 3–8% 偏差、0.19% 灰像素（零滲漏）；`h3-controlnet` 留備援 |
| **SM-3 Colab L4 跑 L3 記憶體上限** | **DONE — ADOPT WITH CONDITIONS** | 0 OOM（峰值 `20.727 GiB`／餘 `1.307 GiB`），硬鎖 `ref_video_0 ≤ 0.35 MP`＋`match`＋`≤5s`＋`high_mem: true` |
| SM-4 `h3-i2v` `last_frame` 收斂度 | 待辦 | 通過前 L2 維持例外模式 |
| SM-5 Flow `omni-1.2-flash`/`veo-lite` 尾幀與 L1 服從度 | 待辦 | 隨實跑回填 |
| **SM-6 VM 上 CozyClay 無頭出片可行性** | **DONE — BLOCKED (VM Runtime)** | 非登入牆；卡 `node v18.20.4 < 22.19` 且無 `npm`/`npx`。過渡期走瀏覽器版或 Python 3D 算圖器 |
| **SM-7A H3 原生 4 槽 Ref2VA（DEMO-02 S4）** | **DONE — ADOPT WITH CONDITIONS** | `sm7a/SM7A_RESULT.md`：4 槽 `max` `0.5 MP` L4 `4.67m` 0 OOM；採納為對白 CU 基線（三條件見 §C.1） |
| **SM-7B RefMod（`ComfyUI-MiniMaxH3Mod`）** | **WATCH（不升階）** | 僅在乾淨首幀 `>30°` 大角度轉頭 CU 仍漂移時觸發 |
| **SM-8 AMD-05 v3 `SYS-01` 全息投影 Carrier A** | **DONE — CARRIER PASS（6/6 技術達標；構圖已於 2026-11-28 取代）** | `sm8/SM8_t1.mp4`（`LOC-ALLEY-NIGHT`＋`OUTFIT-02`＋`sys01-ref-34L-smile/front`）：首幀 `nano2` 1 抽過 QC-1（0 pts）、4s Omni `i2v` 1 抽過 5 幀 QC-2（**12 pts / 0 CU**、`dL*` 跨度 `2.70`、爆光 `0.19%`、V9 零字零面板 `0/5`）。**載體與質感裁決維持 PASS**（正式解鎖 §C.4 v3 技術路線）；**惟 SM-8 首幀之半空懸浮仰視構圖已被 2026-11-28 Creator 顯現定調取代（composition superseded）**，後續新拍改採平視面前同地平面站位（`nano2` 0 點重組首幀），詳見 `sm8/SM8_RESULT.md` 與 §C.4 |

---

# 附錄 B：導演層（v2.1＋v2.3 微表情收斂）

## B.1 導演闡述（階段 0.5）
每集於劇本鎖定（Gate A3）後、分鏡包裝前產出導演闡述，逐 segment 填：情緒曲線／運鏡心理基調／場景邏輯／世界反應基調／特效拍點／光線鎖定（快線 T2／Demo 改走 3 分鐘極簡導演卡）。

## B.2 欄位落點與微表情標尺（v2.3 擴充）
核心欄位已併入正文 §二與 §三（`light_lock_id`、`shot_intent`、`camera_psychology`、`vfx_beats[]`、`world_reaction`、`performance_beat`）。

**v2.3 `performance_beat` 擴充與強度紀律**：
- 結構：`{from, trigger, to, deliberate_hold, intensity?: "L1"|"L2"|"L3"|"L4", lexicon_ids?: string[], intensity_override_reason?: string}`。
- 預設強度：`deliberate_hold=true` 預設 `L1`（配 `L3/L4` 觸發 `PERF_INTENSITY_CONFLICT` 硬駁回），其餘預設 `L2`。
- **范蠡強度上限**：常態鎖定 `L1`（~70%）與 `L2`（~25%），危機上限 `L3`（≤5%）；`L4` 僅供配角／目擊者（標於范蠡未填 `intensity_override_reason` 發 `WARN [PERF_INTENSITY_CEILING]`）。
- **有界詞庫（`bible/performance/micro_expressions.yaml`）**：4 分區（`Z1 眼瞼視線`、`Z2 眉心眉弓`、`Z3 唇線下顎`、`Z4 呼吸肩頸`）× 21 核心詞條；單鏡選填 1–3 項對應 `from`/`to`（拒絕 488 行整包移植與單鏡 2 秒多段情緒翻轉）。
- **景別耦合**：`min_shot_size: CU/MCU` 詞條不得配發於 `MS/LS/ELS` 鏡（併入 `SCALE_JUMP_BAN` 硬駁回）；`2S` 雙人鏡必配至少一項 `Z4` 或微動作詞（自動滿足 §B.8-5）。
- **反 AI 假臉衛生**：`microexpression` 與 prompt 嚴禁美顏塑膠肌、商業假笑與誇張過演詞（`AI_FACE_TABOO` 硬駁回）；Flow 編譯入 `Avoid:`，H3 編譯為正向膚質護欄句。

## B.3 V12 導演護欄
V12a（雙門對稱光線）、V12b（`performance_beat`＋v2.3 詞庫強度與景別耦合）、V12c（公開高異常場世界反應）、V12d（Advisory 鏡頭多元）、V12e（Advisory 運鏡心理一致性）。詳見 §6.1–6.2。

## B.4 `camera_psychology` 衍生與引擎盲區補救
映射表依 `DIRECTOR_LAYER_AGY_MEMO.md` Q3 定稿表執行；失焦合焦（`gblur`）、過穩微抖、燈閃兩幀等盲區走 ffmpeg 後製補救；運鏡強度由 `movement.amplitude` 控制，禁自由文字後綴。

## B.5 QC-D 導演 QC 閘與 B.6 導演手記
- **位置**：Stage 6A 粗剪之後、Stage 6B 精修／QC-3 之前。
- **六檢**：① 合理性／② 情緒可讀／**③ 鏡頭覆蓋與短劇節奏（詳見附錄 D.5 QC-D 四項子檢）**／④ 光線連續／⑤ 運鏡心理／⑥ 特效拍點。
- **導演手記（`bible/director/playbook.md`）**：累積制，每集闡述前必讀。

## B.7 Creator 定案三點與 B.8 QC-D 首例裁決（DEMO-02）
1. **長台詞鏡拆分常規**：反應鏡 → 剪輯接點特效 → 主鏡＋L-cut。
2. **眼中倒映降載**：720p CU 以瞳孔反光點＋半臉輝光表達（看清倒影另拆 ECU）。
3. **目擊者反打**：異常事件補目擊者反應反打鏡。
4. **DEMO-02 QC-D 六類不過與常規五條**：① QC-1 服裝四項逐項對照；② 臉／年齡／傷痕邊一律以成片抽幀驗收；③ 相鄰鏡 `end_state → start_pose` 姿勢接點檢查；④ `SYS-01` 彈窗後製合成化（§C.4）；⑤ 雙人鏡強制微動作條款。

---

# 附錄 C：工作流修訂 AMD-01～07（v2.2＋v2.3 SM-7A 與錨點整合）

> 工程落點：`tools/preflight_gate.py`、`tools/diff_sheet_gen.py`、`tools/sys01_composite.py`、`sm7a/workflows/h3_r2v_4ref_groupB.json`、`claytest/workflows/h3_r2v_clay.json`。

## C.1 AMD-01 身份載體分工（納入 SM-7A 三條件）

| 鏡頭類型 | 強制載體 | 禁止 |
|---|---|---|
| 對白特寫／近景（`lip_sensitive`） | **原生 4 槽 H3 Ref2VA**（V3 順序，`ref_image_size="max"`，`544×960` 8-step TriPRISM；`h3_r2v_4ref_groupB.json`） | 單首幀 i2v；省略對白本文；餵入含錯邊疤／反領之髒 `<Pic 1>` |
| 雙人同框／過肩 | 有對白或主角正臉：H3 Ref2VA；無對白中景對峙：Flow 同源衍生＋同尺幅 i2v | 靜止否定詞；同場後續鏡獨立 i2i |
| 動作／中遠景 | 首幀 i2v（主角露臉走 Flow 同尺幅；高動量無正臉走 Wan；複雜走位弧線走 L3 Clay＋H3） | 跨尺幅推臉（臉框放大 >1.8× 或轉頭 >±30°） |
| 反應／無對白近景、目擊反打 | 主角 CU/MCU 反應：H3 Ref2VA（閉唇鎖定）；配角短反打 ≤2.5s：Flow 同源衍生＋同尺幅 i2v | 空景母圖＋文字重生同場人物 |
| 證據卡／聲明卡／無框資料側卡 | CPU 後製合成（Pillow＋ffmpeg） | 100% 禁止進生成端 |
| `SYS-01` 全息投影鏡（v2.4 AMD-05 v3） | **Carrier A：Flow `nano2` 雙卡首幀（單視角裁切 ref）→ Flow Omni `i2v_first`**＋後製微光精修（`S04b` 范蠡 CU 則 `SYS-01` 退為畫外聲；獨鏡對嘴選配 3–4 槽 H3 Solo） | 餵原始多格角色卡；生成浮動面板／HUD 光環／文字；與范蠡混塞進 L4 4 槽 H3 |

**SM-7A 三項強制採納條件（v2.3 入規，自 `sm7a/SM7A_RESULT.md`）**：
1. **條件 1 — Stage 4 前強制 QC-1 乾淨首幀**：4 槽 Ref2VA 是「時序保持穩定器」，**不是「首幀缺陷橡皮擦」**（SM-7A 實證 `<Pic 1>` 錯邊疤無法被 `<Pic 2..4>` 覆寫）。嚴禁將錯邊疤、反領（`左衽`）或缺簪首幀送入 H3 Ref2VA；每顆對白 CU 首幀必經 Path A 衍生並通過 `qc1_gate.json == PASS`。
2. **條件 2 — 鎖定已修補之 `fanli-master-ancient-45R.jpg`（`右衽`＋右眉無疤）並退役水平翻轉法**：所有 `OUTFIT-02` 4 槽母圖（`ancient-cu`、`ancient-45`、修補後 `ancient-45R`）100% 統一為小寫 `y` 形 `右衽`；封存禁用 `fanli-master-ancient-45R.v1-flip-defect.jpg`，並於首顆乾淨首幀對白 CU（DEMO-02 v2 S4）實測驗證 QC-2 錯邊疤 `0/5`。
3. **條件 3 — L4 標準解析度＋升頻與音訊對位**：L4 對白 CU 標準化於 `h3_r2v_4ref_groupB.json`（`544×960` `0.5 MP`、`ref_image_size="max"`、8 steps TriPRISM、`~4.67m`/`~0.13 CU`），組裝端升頻至 `720×1280`／`1080×1920` 並以鎖定 ElevenLabs TTS 取代原聲對位（精對起音與停頓）。**SM-7B RefMod（`ComfyUI-MiniMaxH3Mod`）維持 `WATCH`**，僅於乾淨首幀 `>30°` 大轉頭 CU 仍漂移時升階。

Flow 引擎預設為 **Omni 1.2 Flash**（取代舊 Veo Fast/Quality，後者 2026-12-05 退役）。禁止獨立 i2i 四紅線：同場反打／切近／續接鏡、已出場配角續演、主角非主參考側 CU/MCU（必附右側無疤母圖）、`SYS-01` 與一切文字卡。

## C.2 AMD-02＋03 雙門對稱 QC 與身分錨點鍵位映射（v2.3）

- **QC-1（首幀門）**：硬鎖靜態不變量——`qc1_diff_sheet.jpg`（定裝錨＋首幀＋2.5× 臉領放大）＋ `qc1_gate.json`（5 鍵：`age_id`、`scar_side`、`costume_4pt`、`light_lock`、`pose_spatial`＋各首幀 SHA256），Stage 4 前以 `diff_sheet_gen.py --verify` 強制驗簽。
- **QC-2（挑片門）**：硬鎖動態保持率——`qc2_diff_sheet.jpg`（定裝＋首幀＋§5.1 抽幀＋2.5× 放大）＋ `qc2_gate.json`（6 鍵：另加 `expression_lip`＋首幀與成片 SHA256），Stage 6A 組裝前強制驗簽。V12a 光線雙門對稱（QC-1 靜態鎖＋QC-2 留存比對＋爆光 `<5%`）。
- **v2.3 身分錨點映射（不新增第 7 頂層鍵）**：`bible/anchors/FANLI.yaml` 四項錨點精確歸入既有鍵位，零破壞且防雙重扣分：
  - `ANC-FANLI-01`（左眉尾淡疤）→ **`scar_side`**；
  - `ANC-FANLI-02`（時代髮型剪影）→ **`costume_4pt` 第 ② 項**（銀髮比併入 `age_id`）；
  - `ANC-FANLI-03`（現代方孔錢）與 `ANC-FANLI-04`（左腕舊銅錶）→ **`costume_4pt` 第 ③ 項配件與第 ④ 項時代禁則**（春秋 `OUTFIT-02/03` 嚴禁方孔錢與腕錶；現代 `OUTFIT-01` 驗左腕錶／無字方孔錢）。
  - `diff_sheet_gen.py` 支援 `--anchors-dir bible/anchors/` 依 `time_layer`＋`outfit_id` 於 Col 0／Col 2 自動列印該鏡時代必現錨點與禁則，並於單鏡紀錄增選填 `failed_anchor_ids: []`。

## C.3 AMD-04 同場景衍生規則
同段非首鏡、反打／過肩、共用配角鏡頭，首幀來源僅三合法路徑：**Path A** 錨鏡衍生（`derived_shot`＋`ref_shot_id`）／**Path B** 反打空景＋錨鏡雙鎖（`generated_dual_lock`＋`LOC_rev`＋`ref_shot_id`）／**Path C** CozyClay 共用場地（`l3_clay_frame0`）。僅餵單一 `LOC-*` 空景重生人物者 preflight 硬駁回。

## C.4 AMD-05 `SYS-01` 全息投影生成主導＋後製精修化（v3 載體定案｜v2.4.1 顯現導演定調修訂）

`SYS-01` 虛擬真人投影採**「生成端主導（Generation-Primary）＋後製精修（Post-Polish）」**（載體與質感經 `SM-8` 6/6 技術 PASS 驗證），確保自然膚色、冰藍輪廓光、半透明軀幹、粒子消散與現場光影回打達成原生整合；**構圖尺度與顯現語法依 Creator 2026-11-28 21:18 導演定調（`SYS01-MANIFESTATION-DIRECTION.md`）全面收斂為「平視面前同地平面單一預設＋剪輯硬切入為主」**。

1. **核心生成路由（預設 Carrier A — SM-8 載體 PASS 維持有效）**：
   - **雙人顯現與中景對話鏡（`MS`/`2S`/`OTS`，`lip_sensitive=false`）**：於 Stage 3 以 `nano2 i2i`（0 點）結合場景／前鏡錨點（AMD-04）、主角母圖與**裁切後單視角 `SYS-01` 參考圖**（`casting/master/sys01-ref-*.png`，嚴守 §3.C.1 禁餵原始多格卡與 `expressions` R2C5 異常格）生成**平視、站位主角面前、同一地平面、半透明**之全息投影首幀，通過 **QC-1 雙臉＋投影外觀＋平視地平面構圖＋零文字門** 後，送 Flow Omni 1.2 Flash（`i2v_first`）生成動態。
   - **范蠡特寫開口鏡（如 `S04b`）**：嚴禁將 `SYS-01` 塞入范蠡 4 槽 H3 Ref2VA；維持純范蠡平視 4 槽 H3 CU（臉側承接前方眼平冷青回打光，非仰視半空），`SYS-01` 採畫外 TTS 接聲。
   - **`SYS-01` 獨鏡微表情特寫（如 `S19`）**：以鎖定表情單格（如 R1C1 微笑 → R1C5 收斂，並配高解析 `sys01-ref-front.png`）於 Stage 3 產出像素對齊之平視全息首幀（與可選尾幀），經 Flow Omni `i2v_first` / `i2v_first_last` 生成；若逾 2 抽仍過演，改以該兩張已過 QC-1 之全息靜幀於組裝端執行 0.5s 微過渡保底。
   - **`SYS-01` 獨鏡對嘴特寫（`lip_sensitive=true` 選配）**：僅限 `SYS-01` 獨佔 3–4 槽 H3 Ref2VA（`<Pic 1>` 全息首幀＋`<Pic 2..3>` 單視角臉／圍巾錨點），嚴禁與范蠡混槽。

2. **顯現尺度表 — 平視單一預設（v2.4.1 取代 AMD-05 v3 舊尺度草案與 SM-8 首幀構圖）**：

| 尺度模式（`sys01_scale_mode`） | 構圖、站位與地平面規格 | 適用鏡型 | 狀態 |
| :--- | :--- | :--- | :---: |
| **`eye_level_in_front`**<br>*(向下相容別名：`conversation_eyeline`)* | **平視構圖**（`angle_v: eye`，眼平 ±5°）、尺度 **`0.90–1.00×`**（與范蠡同高）；站位於范蠡**面前**、與他**同一地平面**；半透明軀幹，下身可粒子消散但**消散點必落於地面附近**（絕非半空懸浮漂浮、絕非仰視壓頂） | **全線雙人顯現與對話鏡唯一預設**（含 **2022 初現 `S03`/`S04a`**、DEMO-03 `S3b`、EP-01 `S08`/`S10`；`S08` 預留暗區給後製無框側卡） | **唯一預設（v2.4.1）** |
| **`solo_cu`** | 85mm 平視正面胸上特寫，保障 360px 手機縮圖微表情可讀性（如 `S19` R1C1→R1C5 微笑收斂 0.5 秒遲疑） | `SYS-01` 獨鏡特寫（`S19`） | **獨鏡特寫專用** |
| ~~`manifestation_hero`~~ | ~~右上半空懸浮半身投影、尺度 1.25–1.45×、范蠡左下仰視 20–35°~~ | ~~原 AMD-05 v3 2022 初現草案與 SM-8 首幀~~ | **RETIRED（2026-11-28 退役，含 2022 初現）** |

3. **顯現語法 — 剪輯切入為主／鏡內凝聚為偶爾點綴（v2.4.1）**：
   - **主語法 — 剪輯硬切入已成場（`sys01_apparition_mode: "editorial_cut_in"`，唯一入場預設）**：「忽然彈現在主角面前」的驚嚇／突現體感**靠分鏡硬切實現，不靠鏡內特效凝聚**。
   - **標準前鏡鋪墊 — 前鏡三要素預告組（Pre-Shot Cue Triple）**：凡 `SYS-01` 進入場景之鏡頭（如 EP-01 `S03`、`S08`、DEMO-03 `S3b`），其**前一鏡尾段**（如 `S02`、`S07`、`S3a`）必設置以下三要素作為標準起手式：
     1. **冷青光 cue（Light Cue）**：范蠡臉側／衣領閃過一道冷青微光（物理空間異常觸發）；
     2. **環境聲抽空（`sound_drop`）**：環境底噪驟降至 `-38 dBFS`（約 `0.35s`），瞬間抽空現場音場；
     3. **范蠡視線轉向（Eyeline Shift）**：范蠡警覺轉眼望向他**正前方眼平預定位**（非仰頭看半空）；
     → **隨即硬切入下一鏡**：硬切進場瞬間，`SYS-01` **已經完整在場**（半透明、平視 `0.90–1.00×`、站位於他面前同一地平面、下身消散點落於地面附近）。
   - **輔語法 — 鏡內光凝成形（`sys01_apparition_mode: "in_shot_materialize"`，降級為偶爾點綴）**：不再作主要顯現表達，僅於劇本或導演闡述明確指定之極少數特殊節點作為偶爾點綴（須填理由，否則 `preflight_gate.py` 發 Advisory `WARN [SYS01_MANIFESTATION_DIRECTION]`）。
   - **同場延續鏡（`sys01_apparition_mode: "already_present"`）**：用於同場段她已出現後的續接對話／反打／獨鏡（如 `S04a`、`S10`、`S19`）。

4. **強制視覺錨點與 V9 禁字紅線**：
   - 凡 `SYS-01` 入鏡，生成提示詞（中文房規）**必須**包含：① 至少 2 項全息光學錨詞（`全息投影`／`掃描線`／`粒子消散`／`半透明`／`藍色輪廓光`／`下身光塵化`）；② 臉部自然膚色保護與鎖定服裝錨點（`黑色羊毛大衣`＋`深紅色粗針織圍巾`）；③ 明確預設尺度模式（`sys01_scale_mode`: `eye_level_in_front`〔或相容別名 `conversation_eyeline`〕｜`solo_cu`；若仍標 `manifestation_hero` 或 `angle_v ∈ {low, worm}`，preflight 發 Advisory `WARN [SYS01_MANIFESTATION_DIRECTION]`），並寫明平視、站位主角面前同一地平面、下身粒子消散點落地面附近（禁半空懸浮）。
   - **V9 零文字／零面板鐵律維持不變**：生成端**100% 嚴禁**任何可讀文字、偽文字、浮動小面板、數據視窗、圓形 HUD 光環、品牌標誌與音訊波形條（`preflight_gate.py` 以 `SYS01_TEXT_PANEL_BAN` 硬封殺，QC-1/QC-2 出現單幀即一票否決）。

5. **後製精修層（`tools/sys01_composite.py` 保留職責）**：
   - 不再承擔常態人像去背貼片，轉為提供輕量確定性後製：① 前鏡三要素預告之冷青光 cue 與 `sound_drop`（`-38 dBFS` `0.35s`）＋啟動音效；② 必要時以緊縮羽化遮罩（`ry=0.21`）微補范蠡臉側眼平冷青回光平衡；③ 依 `SYS01.yaml` TTS 音訊 RMS 驅動投影區 `+4–6%` 輝光微脈；④ 獨立無框資料／新聞側卡疊加（如 `S08` `--mode datacard`）與 2 幀篆字「蠡」閃現（`S03`/`S19`）；⑤ 鏡內光凝特效降為偶爾點綴工具；保留舊 `--mode panel` 僅供歷史回放與極端故障降級。

6. **歷史祖父條款與 SM-8 分拆裁決（Grandfathering）**：
   - `DEMO02_v2`（`demo02_v2/DEMO02_v2.mp4`，採 AMD-05 v1 幾何四層合成，QC-0/1/2 全簽核）視為已驗收之管線里程碑，**豁免追溯重製**。
   - `SM-8`（`sm8/SM8_t1.mp4`，2026-11-28）之 **載體與質感裁決維持 PASS**（6/6 達標、12 pts / 0 CU），但其半空懸浮仰視構圖已於同日被 Creator 定調取代（**composition superseded**）；自 **2026-11-28 定調起**，所有新拍（含 DEMO-03 與 EP-01）全面適用 **AMD-05 v3 載體 ＋ v2.4.1 平視面前同地平面＋剪輯硬切顯現規格**（首幀以 `nano2` 0 點重組）。

## C.5 AMD-06＋07 入口契約與 `preflight_gate.py` 強制力（v2.4.1）
- 一切生成（含 demo）只能由 `script_pack.json` 經引擎方言編譯產出 prompt；手寫 bash 散文 prompt 全面禁止。
- `tools/preflight_gate.py` 執行全部硬閘（AMD-01/04/05 v3/07 ＋ v2.3 增量 ＋ **v2.4 增量**：V14 鏡頭覆蓋 12 條、`H3_MODE_EXCLUSION`、`H3_MIN_DURATION`、17-frame `5+17k` 實長檢核、`SYS01_TEXT_PANEL_BAN`、`SYS01_PROJECTION_ANCHOR_REQ`）與非阻斷 Advisory 提示（4 項電影工藝＋`COVERAGE_PACE_ENVELOPE`＋`INSERT_ECU_DURATION`＋**v2.4.1 `SYS01_MANIFESTATION_DIRECTION`**）。
- Demo 邊界條款全文見 §九，零豁免生效。

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

- **景別建議淨長**：`ECU` `1.0–2.0s`（絕對 `0.8–2.5s`；依 Creator 裁示 **`INSERT`/`ECU` 淨長 `> 2.0s` 無理由說明觸發 Advisory `INSERT_ECU_DURATION` `WARN`**）；`CU` 無對白反應 `1.2–2.5s`、對白／峰值 `2.5–4.8s`（守 V1 產線品質帽／V2）；`MCU` `2.0–4.0s`；`MS` `2.0–3.5s`；`MLS` `1.8–3.0s`；`WS` 定場 **`≤ 2.5s`**（跨 1 級推進 ≤4.0s）；`CARD` `1.5–3.0s`。
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
12. **插鏡／ECU 時長紀律（ADVISORY：`INSERT_ECU_DURATION`｜2026-11-28 Creator 裁示）**：任何 `shot_size == "ECU"` 或 `framing_flags.is_insert == true`（含舊版 `shot_size == "INSERT"`）之鏡頭，若淨時長 `target_net_sec > 2.0s` 且未填理由說明（`hold_justification` 或合理備註如 `performance_hold`/`voiceover_density`/`final_image`），`preflight_gate.py` 發出 `WARN [INSERT_ECU_DURATION]`。

## D.4 與 V1／V2／`SCALE_JUMP_BAN` 及成本紀律的組合

1. **短插鏡 V1 豁免與 H3 4.0s 墊幀分流**：`is_insert`/`is_reverse`/`ECU`/`reaction`/`turn_jolt` 鏡頭生成長落於 `2.0–3.0s`（或 `trim_policy: "tail_only"`）不觸發 `V1_DURATION_ENVELOPE` 短鏡 `WARN`（僅豁免剪輯淨長；若路由至 H3，仍依 `H3_MIN_DURATION` 自動墊高生成參數至 `≥4.0s / 107f` 再於 Stage 6A 裁切）。
2. **長台詞用 L-cut 降 ASL，禁硬壓 V2**：超過 `3.5s` 之對白優先以 `audio_groups[]` 走 L-cut 切入 `1.2–1.8s` 聽者反應或無臉細節插鏡，兼顧 V2 語速與豎屏快節奏。
3. **成本感知買密度**：新增節奏鏡優先配發 **無正臉 `ECU` 插鏡（Flow `3s tail_only` 或 Wan 2.2）**、**`cpu_card`（0 成本）**、**L4 剪輯接點特效（甩鏡／急推／微推／補抖）**與**同片雙切反應回收**，嚴控 `H3-4Ref` 對白 CU 總鏡數不膨脹。

## D.5 QC-D 第 ③ 檢細化（鏡頭覆蓋與短劇節奏）

Stage 6A 粗剪後於 QC-D 第 ③ 檢逐一確認（過／不過＋一句證據）：
- **③a 景別弧線**：景別變化服務情緒遞進，峰值穩落最緊 `CU`/`ECU`；
- **③b 豎屏張力**：前 1.5–3s 靜音即有視覺變故，無空轉死氣與機械等長感，長停頓皆具明確張力動機；
- **③c 反應與細節**：切在聽者反應與手／眼細節，非純盯說話者念稿；`ECU` 節制打在轉折拍點；
- **③d 軸線視線**：跨切視線與左右空間自然連貫，無無故跳軸。
