# 分鏡元件落差分析（2026-11-27）

> 依據：開源工作流深研報告 `~/workspace/research_notes/opensource-storyboard-workflow-component-20261127-1446/report.md`（Toonflow、LocalMiniDrama、Huobao Drama、MovieAgent、Storyboarder、Pavo、Microdrama shotlist 等，欄位多為程式碼／文件實查）。
> 我方現況基準：乾跑節拍表（鏡號／時間／鏡長／引擎預估／畫面與對白要點／對白字數速率）＋ `script_pack.json` shots 契約（shot_id、beat_id、shot_type、priority、character_ids、location_id、camera 自由文字、action、dialogue、speaker、emotion、target_net_sec、face_lock_level、audio_hint、visual_text_overlay）＋散在工作流規則裡的首幀規則與資產銀行（未綁進鏡格）。

## 結論

生產級分鏡不是一格自由文字，而是 8–16 個結構欄位，外加兩層我們完全沒有的東西：**每鏡綁定的參照資產**，與**由欄位組裝衍生的圖／影雙 prompt**。我們現在的分鏡只覆蓋「身分＋時間」層；鏡頭語言埋在散文裡、參照靠人記、prompt 到 Stage 4 才臨時手寫——這就是薄弱感的來源。

## 須補齊的元件（依對生成一致性的影響排序）

### 第一級：結構性缺失（直接決定生成連不連戲）

1. **每鏡綁定資產 ID＋引用順序**：character／scene／**prop** 三類 ID 綁進鏡格，且引用順序固定（場景→人物→道具，`@ImageN` 清單）。Toonflow 用 join 表、Huobao 用 `character_ids/prop_ids`、LocalMiniDrama 明訂順序。我方：script_pack 有 character/location、**無 prop 綁定**；節拍表什麼都不綁，資產銀行與鏡格之間靠人腦對照。
2. **圖 prompt 與影 prompt 分離、且由欄位衍生**：`image_prompt`（靜幀）與 `video_prompt`（動態）是兩個獨立欄位，主流做法是由結構欄位以公式組裝（Microdrama 的 auto-formula、LocalMiniDrama 的組裝面板），不是手寫兩份。我方：兩者都不存在，Stage 4 臨時以散文提示詞應付。
3. **首幀＋尾幀雙參照＋尾幀鏈**：每鏡同時綁 first frame 與 last frame，且上一鏡尾幀＝下一鏡首幀（LocalMiniDrama 的 tail-frame link）。我方：只有「每鏡一張首幀」的口頭規則、沒有欄位；**尾幀概念完全缺席**——鏡與鏡之間的銜接現在沒有任何機制保證。
4. **生成模式欄位**：每鏡標明 first-frame-only／first+last／multi-reference（LocalMiniDrama 的 Classic vs Universal 是真欄位）。我方：只有引擎預估，沒有模式。

### 第二級：鏡頭語言與連戲狀態

5. **攝影拆欄**：景別／垂直角度／水平角度／運鏡，四個獨立欄位（Huobao、Pavo、MovieAgent、Storyboarder STS 皆然）。我方：script_pack 的 `camera` 是一串自由文字（"medium_close_up, slow push-in"），節拍表連這串都沒有。焦段僅存於專業清單與 prompt 文字，AI 工具無人設欄——列選配。
6. **鏡尾狀態（result／end-state）**：這一鏡結束時畫面停在什麼狀態——人物位置、道具在誰手裡、門開還是關；下一鏡的起點由此繼承。只有 Huobao 有此欄，卻是連戲的關鍵。我方：全靠散文（如按空腰間的遞進是寫在設計說明裡，不是欄位）。
7. **轉場類型欄位**：cut／match cut／dissolve／硬切＋觸發點。只有 Microdrama 把它做成欄位；我方寫在備註散文裡（S12 的 Match Cut）。
8. **氛圍與光線狀態**：場景級 time＋light、鏡級 atmosphere／lighting match（Huobao）。我方：look 只在集級 prompt 結構裡，鏡與鏡的光線銜接無欄位可查。
9. **視線／銀幕方向**：查遍主流工具——**沒有任何一家有專用欄位**，只存在於專業清單的備註。我方閃回不露臉、系統對話是屏幕介面，列備註級即可，不必設欄。

### 第三級：聲音與節奏

10. **音效／環境聲／BGM cue 每鏡（或每段）欄位**：Huobao 有 `sound_effect`＋`bgm_prompt`、Microdrama 有 SFX 欄。我方只有 `audio_hint` 一格，環境聲與音效沒有位置。
11. **節拍功能標籤**：HOOK／JOLT／CLIFF／PAYOFF（Microdrama 第 N 欄）。我方 beats 有 fact_tier（事實分層），但沒有「這一鏡在爽點結構裡幹什麼」的標籤——對爆款結構導向的短劇，這欄便宜又關鍵。
12. **微表情欄位**：Microdrama 的 `Microexpression` 欄；我方 `emotion` 只有粗粒度（「冷靜、銳利」）。我們的活人感北極星恰恰活在微表情上（S19「遲疑半秒」是整集的設計點，卻只能寫在散文裡）。

### 第四級：生產與 QC 狀態

13. **每鏡生成狀態＋失敗原因**：Toonflow 的 `state`（未生成／生成中／已完成／生成失敗）＋`reason`。我方產線在階段層級追蹤，鏡級無狀態欄。
14. **Take 選擇指標＋跳過旗標**：Toonflow 在 track 級有 `selectVideoId`（選定哪支候選）、`shouldGenerateImage`（本鏡跳過出圖）。我方挑片靠人工流程，無欄位承載。
15. **驗收規則形式化**：對白時長下限（Huobao：字數÷4.5/s＋2s 緩衝）這類規則應寫成欄位驗證而非人工核算——我方的字數／速率欄其實已是這件事的手工版，形式化即可。

## 明確不用補的（查證後的減法）

- **seed／負面 prompt 不設鏡級欄位**：所有受查工具都放在工作流／節點層，沒有一家放進分鏡表；我方現行放在 prompt 結構層是對的。
- **引擎／模型欄位不必再細化**：主流工具是專案級設定；我方的「每鏡引擎預估」反而比多數工具更細，保留作路由用途即可。
- **setup 編號、頁數、拍攝日等實拍欄位**：無實體片場，不需要；其對應物是生成批次／track 分組，已有概念。

## 我方已達標、不必動的

- 對白獨立欄位＋說話者（script_pack 已有；旁白分欄我方格式本就不用旁白，系統台詞屬對白）。
- priority 欄位（script_pack 已有，多數 AI 工具反而沒有）。
- 對白字數與速率（多數工具只有驗證規則、沒有欄位；我方是手工版，形式化後即達標）。

## 下一步建議

據此起草**分鏡規格 v2**（欄位表＋每欄的填寫規則與驗證規則），併入 script_pack 契約升版；依常規先與 agy 完成書面討論、經 Creator 過目，才套用到 EP-01 的正式分鏡包。
