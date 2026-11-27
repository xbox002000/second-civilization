# EP-001《開關》｜AI 真人電影感製作包 v0.2

- episode_id：EP-001
- 對應劇本：EP-001-THE-SWITCH.md v0.3（本文件取代舊 v0.1 鏡頭表）
- 目標成片：95–100 秒
- 畫幅：9:16
- 視覺形式：AI 真人電影感
- Canon：EVENT_FICTION / NON_CANON
- 狀態：可進入角色參照與鏡頭測試；尚未生成影片、剪輯或發布。

## 1. 本版最重要的改動

舊版把范蠡寫成只負責指出風險的策略顧問，角色籌碼不足。v0.2 依新劇本調整：
- 范蠡是早期策略投資人，持有有限股權但不管理日常營運。
- 他曾提出備援方案，且留下風險備忘錄；他不知道危機何時發生。
- 他憑合同附件和過往決策紀錄追溯風險來源。
- 他有追加資源的選擇權，但追加資金附有治理條件。
- 他不代替工程師判斷技術，也不無條件救公司。

此身份只適用於本集非 Canon 情境，不能直接寫入長篇主線。

## 2. 全片風格鎖定

**Global prompt：**

Photorealistic live-action cinematic short drama, contemporary East Asian technology startup office, grounded naturalistic acting, realistic skin texture and subtle imperfections, restrained camera movement, 35mm cinema lens language, practical lighting, charcoal black and cool slate-blue palette with small warm desk-lamp accents, believable modern office furniture and computer equipment, natural body proportions and hands, vertical 9:16 composition, understated intellectual tension, no fantasy, no historical costume, no celebrity likeness, no brand logos, no readable text, no subtitles, no watermark.

**Negative prompt：**

anime, illustration, 3D render, game cutscene, fantasy costume, ancient Chinese robe, crown, armor, exaggerated handsome model face, beauty filter, plastic skin, melodramatic acting, exaggerated facial expression, excessive slow motion, floating camera, extra fingers, fused fingers, distorted hands, changing face, changing hairstyle, changing clothing, logos, readable UI text, gibberish text, watermark, subtitles.

## 3. 角色參照

### FANLI-01｜范蠡（暫定）
- 成年東亞男性，視覺年齡約 28 歲；僅供影像一致性，不是故事 Canon。
- 自然黑色中短髮，略有層次與微亂。
- 炭黑色簡潔外套、黑色無標誌內搭、低調腕錶。
- 不做冷酷凝視或英雄姿態；他先看文件，再看人。
- 高位感來自不急於搶話、掌握合同與決策紀錄，以及提出有條件的資源交換。

### ACHENG-01｜阿呈
- 成年東亞男性，約 33–36 歲；短黑髮、略顯疲憊。
- 深灰或暗橄欖色連帽外套、簡單 T-shirt。
- 面對壓力時語速快，談到自己刪除備援方案時出現防衛和羞愧。

### XIA-01｜小夏
- 成年東亞女性，約 27–31 歲；黑髮低馬尾、深灰工作服。
- 技術表述清楚，曾經反對停掉備援；不是只提供正確答案的工具人。

三張單人參照圖需先分別生成並核准，未核准前只作內部測試。

## 4. 場景連續性

- 同一間小型新創辦公室：長桌、兩台螢幕、玻璃隔間、白板、落地窗。
- 夜戲：冷白螢幕光為主，遠處留一盞暖燈。
- 清晨：相同辦公室與機位，窗外天色變成灰藍。
- 合約、被刪除的備援附件、郵件、圖表、白板文字一律後期合成；生成畫面不要出現可讀文字。

## 5. 新版鏡頭生成表

| Shot | 時碼 | 畫面／運鏡 | 主要台詞或行動 |
|---|---:|---|---|
| 01 | 0–8s | 阿呈收到供應商通知，過肩近景，輕微推近 | 「下週就要交付。現在供應商說容量要重新確認，客戶那邊怎麼交代？」 |
| 02 | 8–20s | 阿呈走向范蠡；范蠡翻開合約附件，鏡頭切手部與紙張 | 「先告訴我，這條是誰刪的？」 |
| 03 | 20–34s | 小夏指出備援曾被停用；切阿呈防衛表情與范蠡抬眼 | 「你是為了讓簡報上的毛利更好看，把退路賣掉了。」 |
| 04 | 34–49s | 范蠡把合約推回桌面；穩定中近景，不用低角度 | 「把客戶合約、交付承諾和剩餘現金流拿來。先算清楚我們還能承擔哪一種失敗。」 |
| 05 | 49–68s | 小夏展示三種交付方案；白板圖後製合成 | 范蠡：「三條路都要付代價。差別是，你要自己選代價，還是等別人替你選。」 |
| 06 | 68–82s | 阿呈問是否追加投資；范蠡沉默片刻再提出治理條件 | 「我可以考慮。但技術負責人要有否決權，備援成本要進正式預算，對客戶的承諾也要重新談。」 |
| 07 | 82–95s | 清晨，同一間辦公室；團隊繼續工作，范蠡收起備援附件 | 「我不知道它什麼時候發生。我只知道，不能把不受自己控制的事，當成自己的能力。」 |

## 6. 逐鏡 Video Prompt

### SHOT 01 — The Notice
A tired East Asian male startup founder in his mid-30s sits at a desk late at night, reading a supplier email on a computer monitor. He refreshes the inbox, leans forward, then looks toward a colleague standing behind him. Cool monitor light, restrained anxiety, over-the-shoulder medium close-up, slow controlled push-in. Screen interface blurred and unreadable.

### SHOT 02 — The Deleted Clause
The same founder approaches a young East Asian male investor sitting quietly at the meeting table. The investor has slightly tousled medium-short black hair, charcoal-black jacket, plain black shirt and a simple dark wristwatch, matching the approved Fan Li reference. He does not immediately look up. He opens a printed contract appendix, points to a visibly highlighted but unreadable removed clause, and asks a short question. Start on the paper and hand, then rack focus to the founder's face. Calm, precise, no dramatic low angle.

### SHOT 03 — The Decision Behind the Crisis
An East Asian female technical lead in her late 20s stands beside the table and points to the old backup architecture diagram. She explains that she had opposed suspending it. The founder responds defensively, then falls silent as the investor looks up. Use a restrained three-person composition, natural dialogue rhythm, small facial movements, no theatrical anger. All diagrams are added in post.

### SHOT 04 — The Choice
The same Fan Li character gently slides the contract back across the table. He asks for the customer contract, delivery commitments and remaining cash flow. Medium close-up, stable camera, direct but not aggressive eye contact. His authority comes from having the document and knowing the previous decision, not from an intimidating pose.

### SHOT 05 — Three Costs
The technical lead points to three separate fallback plans represented by simple blank boxes on a whiteboard: wait for current capacity, use a smaller local model, or deliver core functionality first and delay batch generation. The founder listens, visibly calculating the lost final payment. Over-shoulder shot and close inserts; whiteboard labels added later.

### SHOT 06 — Terms, Not Rescue
The founder asks the investor whether he will provide additional capital. Fan Li pauses, then calmly states conditions. Keep Fan Li's expression restrained, eyes steady, no smile. Cut to the founder realizing the funding comes with governance changes; cut to the engineer listening. The negotiation must feel real, not like a heroic ultimatum.

### SHOT 07 — No Victory
Early dawn in the same office. The engineer tests the fallback system; the founder rewrites the delivery scope; Fan Li puts the deleted appendix into a folder. A close insert reveals the appendix date from two months earlier and an old risk memo with Fan Li's handwriting, both added as post-production props. The female engineer challenges him about why he did not stop the founder. He admits that he knew the risk but allowed the founder to choose, then realizes he cannot outsource his own responsibility. Slow pull-back, natural dawn light, subdued ending. No heroic pose or triumphant score.

## 7. 聲音與剪輯

- 范蠡：自然台灣國語，中低音域，語速正常略慢；不刻意低沉、不用古裝腔。
- 阿呈：前段急，防衛時語速加快；看到文件後停頓。
- 小夏：清楚、專業，語氣平穩，對阿呈保留不滿。
- 重要台詞先錄乾淨對白，再做嘴型匹配；必要時使用反應鏡頭避免長時間嘴型生成。
- 音效：伺服器風扇低頻、紙張翻動、文件滑過桌面、鍵盤、手機震動、清晨城市環境音。
- 音樂不做英雄式高潮；「你把退路賣掉了」後留白；片尾對話再留一次空白，讓范蠡的自我追問成立。

## 8. 生成順序
1. 核准范蠡、阿呈、小夏三張單人角色參照圖。
2. 先生成合約文件特寫、辦公室空鏡，確定場景一致。
3. 優先測試 Shot 02（翻合約）與 Shot 06（談追加資金），因為它們最能檢驗范蠡的高位感。
4. 再生成其他鏡頭，逐段 5–8 秒。
5. 後期合成合同附件、圖表、白板與字幕。
6. 完成粗剪後由 Reviewer 檢查演技、角色權力關係、事實／虛構邊界。
7. Creator 核准後才輸出與發布。

## 9. 驗收
- [ ] 范蠡跨鏡頭保持同一臉部、髮型、服裝。
- [ ] 范蠡的高位感來自資訊、文件與談判條件，而非表演腔。
- [ ] 對手和配角有能力，不被寫笨。
- [ ] 范蠡不懂技術細節時沒有假裝懂。
- [ ] 劇情有明確選擇和代價，沒有免費解救。
- [ ] Event Fiction／Non-Canon 標記清楚。
- [ ] 素材授權和 AI 生成版本可追溯。
- [ ] Creator 最終核准。
