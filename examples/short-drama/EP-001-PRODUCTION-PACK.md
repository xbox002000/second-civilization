# EP-001《開關》｜AI 真人電影感製作包 v0.1

- episode_id：EP-001
- 對應劇本：EP-001-THE-SWITCH.md v0.2
- 目標成片：70–80 秒
- 畫幅：9:16
- 影像風格：寫實真人電影感、現代科技商業劇
- Canon：EVENT_FICTION / NON_CANON
- 狀態：可進入角色參照與鏡頭測試；未完成影片生成、剪輯或發布。

## 1. 全片風格鎖定（所有鏡頭共用）

**Global prompt（建議貼在每個鏡頭 prompt 前）：**

Photorealistic live-action cinematic short drama, contemporary East Asian technology startup office, grounded naturalistic acting, realistic skin texture and subtle imperfections, restrained camera movement, 35mm cinema lens language, shallow depth of field only when motivated, practical lighting, charcoal black and cool slate-blue palette with small warm desk-lamp accents, believable modern office furniture and computer equipment, natural body proportions and hands, 24 fps film motion, vertical 9:16 composition, dramatic but understated, no fantasy, no historical costume, no celebrity likeness, no brand logos, no readable text, no subtitles, no watermark.

**Negative prompt：**

anime, illustration, 3D render, game cutscene, fantasy costume, ancient Chinese robe, crown, armor, exaggerated handsome model face, beauty filter, plastic skin, over-sharpened, melodramatic acting, exaggerated facial expression, excessive slow motion, handheld shake without motivation, floating camera, extra fingers, fused fingers, distorted hands, asymmetrical eyes, deformed teeth, duplicate people, changing face, changing hairstyle, changing clothing, logos, readable UI text, gibberish text, watermark, subtitles.

## 2. 角色連續性鎖定

### FANLI-01｜范蠡（暫定角色參照）
- 成年東亞男性，視覺年齡約 28 歲（只為影像一致性，不等於故事 Canon 年齡）。
- 自然黑色中短髮，略有層次與微亂；眉眼沉著，臉部自然，不像廣告模特。
- 炭黑色簡潔外套、黑色無標誌內搭、低調黑色腕錶。
- 動作幅度小，說話前會看一眼文件或對方；情緒透過停頓、眼神與呼吸表現。
- 禁止每個鏡頭重新設計臉型、髮型、膚色、服裝。

### ACHENG-01｜阿呈
- 成年東亞男性，約 33–36 歲。
- 短黑髮，略顯疲倦，眼下有輕微倦容；不留明顯鬍鬚。
- 深灰或暗橄欖色連帽外套，簡單 T-shirt。
- 動作較急，會反覆看手機和螢幕；焦慮但不是暴躁。

### XIA-01｜小夏
- 成年東亞女性，約 27–31 歲。
- 黑髮低馬尾，俐落自然；不濃妝。
- 深灰工作襯衫或簡單黑色上衣。
- 表情專注，動作有效率；講技術時會指向數據或白板，不誇張揮手。

**角色鎖定規則：** 先生成並核准三張單人角色參照圖，再開始影片鏡頭。每個鏡頭只使用對應角色參照；不可用分鏡拼貼圖當作臉部唯一參照。

## 3. 場景連續性

- 地點：同一間約 8–12 人規模的新創辦公室。
- 核心配置：長桌、兩台桌上螢幕、玻璃隔間、白板、落地窗、夜間城市背景。
- 夜戲照明：螢幕冷白光作主要面光；遠處保留一盞暖色桌燈。
- 清晨鏡頭：同一機位附近，窗外天色由深藍變灰藍，不要突然換成另一間辦公室。
- 螢幕圖表、郵件文字、白板方框、手機訊息一律後期合成；生成畫面只要模糊、不可讀的 UI。

## 4. 鏡頭生成表

每段先生成單一連續鏡頭，不要求 AI 一次完成多鏡頭剪輯。每段建議生成 5–8 秒，剪輯時依表格截取。

| Shot | 時碼目標 | 主要畫面 | 景別／運鏡 | 台詞／聲音 |
|---|---:|---|---|---|
| 01 | 0–8s | 阿呈讀到供應商通知 | 過肩近景，慢推 | 阿呈：「下週就要交付了。現在才跟我說這個？」 |
| 02 | 8–18s | 小夏指出替代模型測試結果 | 雙人中景，切手部細節 | 小夏：「可以切成本地模型。核心流程還能跑，但速度會慢，生成品質也會降。」 |
| 03 | 18–28s | 阿呈提議換供應商，小夏提醒重新核對依賴 | 手機近景接小夏反應鏡頭 | 阿呈：「那就換一家。只要能撐過這一週。」小夏：「換供應商也得重新確認來源、客戶和用途。」 |
| 04 | 28–42s | 范蠡聽完，觀察交付排程 | 范蠡中近景，穩定慢推 | 范蠡：「我們賣的是模型，還是替客戶解決問題？」停頓。「現在看來，我們把交付承諾，押在一個自己不能保證的開關上。」 |
| 05 | 42–59s | 小夏畫出降級交付方案，阿呈意識到尾款代價 | 白板過肩鏡頭，切阿呈表情 | 小夏：「核心功能照交。批次生成延後，進階效果先降級。」阿呈：「這樣會少收一筆尾款。」范蠡：「別把我們沒算好的風險，直接交給客戶承擔。」 |
| 06 | 59–70s | 阿呈向客戶說明交付調整 | 側面中景，電話不露可讀畫面 | 阿呈：「核心功能照期交付，批次生成延後一週，費用我會一起重算。」留出對方回應的沉默。 |
| 07 | 70–80s | 清晨，團隊繼續測試；范蠡看著城市 | 范蠡側面中景，緩慢拉遠 | 阿呈（畫外）：「下次怎麼避免？」范蠡：「先把不能控制的部分，寫進計畫裡。不要等它停了，才想起自己沒有退路。」 |

## 5. 逐鏡 Video Prompt

### SHOT 01 — Supplier Notice
A tired East Asian male startup founder in his mid-30s sits alone at a desk late at night, reading an urgent email on a computer monitor. The monitor casts cool white light across his face. He leans forward, eyes moving across the screen, then exhales and rubs the bridge of his nose. Over-the-shoulder medium close-up, slow controlled push-in, modern small technology startup office, realistic screen reflections, restrained anxious performance. The screen contains only blurred unreadable interface shapes, no legible text.

### SHOT 02 — The Alternative
An East Asian female software engineer in her late 20s with black hair tied in a low ponytail stands beside a desk, showing a laptop to the same tired male founder. She points to two blurred performance charts and calmly explains a smaller local model fallback. The founder listens with a tense jaw, then looks away. Medium two-shot followed by a close insert of her finger pointing at the screen, realistic office lighting, stable camera, no readable text.

### SHOT 03 — Switching Providers
The same male founder lifts his phone and looks for another cloud provider option, frustrated but trying to stay composed. Cut to the same female engineer shaking her head slightly and explaining that changing providers does not remove the need to verify source, customer and use conditions. Tight close-up on phone with abstract unreadable UI, then over-the-shoulder reaction shot. No brand logo, no legible messages, natural restrained acting.

### SHOT 04 — Fan Li's Question
The same young East Asian male character from the approved Fan Li portrait sits at the far end of the meeting table, wearing a charcoal-black jacket over a plain black shirt and a simple dark wristwatch. He has slightly tousled medium-short black hair and a calm, observant expression. He has listened without interrupting. He glances at the delivery schedule on paper, then raises his eyes toward the founder and speaks evenly. Medium close-up, very slow push-in, hold a brief silence after the first question, practical cool screen light and a warm desk lamp in the background. No heroic low angle, no supernatural effect.

### SHOT 05 — The Cost
The same female engineer stands at a whiteboard and outlines three simple modules using unlabeled boxes. She gestures to the core workflow, advanced generation and batch processing sections. The same male founder watches, realizing that delaying batch processing will reduce the final contract payment. Fan Li sits quietly in the background, attentive but not triumphant. Over-shoulder framing, insert of marker drawing three blank boxes, then close reaction shot of the founder. All labels and diagrams will be composited in post-production, not generated.

### SHOT 06 — Taking Responsibility
The same founder stands near the window and makes a difficult phone call to a client. He explains the revised delivery scope and listens without interrupting. His shoulders are tense; after hearing the response, he nods once and writes a note. Side medium shot, city reflections in the glass, slow restrained camera move, no visible phone screen, no audible synthetic dialogue generated by the video model.

### SHOT 07 — Dawn, No Victory Pose
Early dawn in the same startup office. The female engineer tests the fallback system at her workstation; the founder rewrites the delivery plan at the long table. Fan Li stands by the window in side profile, wearing the same charcoal-black jacket, looking out at the waking city. He does not smile or pose heroically. Slow gentle pull-back, natural dawn blue light gradually mixing with the warm desk lamp, quiet realistic atmosphere, consistent faces and wardrobe.

## 6. 聲音與剪輯

- 先製作乾淨對白音軌，再以角色參照做嘴型匹配；長句可拆成正面短鏡與反應鏡。
- 范蠡聲音：自然台灣國語，中低音域，語速正常略慢，不做古裝腔或刻意低沉。
- 阿呈聲音：較快，前半段有壓力；在向客戶說明時放慢。
- 小夏聲音：清楚、專業，不要像客服播報。
- 音效：伺服器風扇低頻、鍵盤、手機震動、椅子移動、窗外城市環境音。
- 配樂：前半段極低存在感；范蠡提問後略收音；最後清晨只留下淡薄持續音，不做勝利式高潮。
- 螢幕文字、白板字、郵件、字幕、標題卡全部後期製作。

## 7. 封面與片尾
- 封面：范蠡側臉在畫面右側，左側為一台顯示中斷進度的模糊工作站；文字後期加兩行：「算力不是你的」「你還剩下什麼？」
- 片尾：黑底暖白字「能租到，不代表掌握。」下方小字「虛構短劇｜受近期 AI 算力監管事件啟發」。

## 8. 生成及驗收順序
1. 先生成三位演員單人參照圖，Creator 核准范蠡臉部。
2. 生成場景空鏡，固定辦公室位置與光線。
3. 先測 Shot 04 范蠡近景和 Shot 01 阿呈近景，確認臉部一致及表演品質。
4. 通過後再生成剩餘五段。
5. 統一錄音、對嘴、字幕、UI 和聲音設計。
6. 剪出粗剪，Reviewer 檢查劇情、角色與視聽品質。
7. Creator 核准後才輸出正式版本。

## 9. 最低成片驗收
- [ ] 三位角色跨鏡頭保持同一臉部與服裝。
- [ ] 辦公室夜景／清晨場景連續。
- [ ] 手部、眼睛、嘴型和物件沒有明顯生成錯誤。
- [ ] 對白可聽清楚，范蠡不使用古裝腔。
- [ ] 故事有選擇、代價和承擔，不以一句格言解決問題。
- [ ] 清楚標示 Event Fiction / Non-Canon。
- [ ] 音樂、素材、聲音和影像授權狀態可追溯。
- [ ] Creator 最終核准。
