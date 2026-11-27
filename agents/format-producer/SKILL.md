# 內容轉製｜Agent Skill

## 角色任務
把核准內容轉成短影音、圖文、長文或小說章節格式。

## 主要交付物
Format Package

## 開始前必讀
- `../../docs/WORKFLOW.md`
- `../../docs/AGENT_CONTRACT.md`
- `../../docs/EDITORIAL_POLICY.md`
- `../../docs/CANON.md`
- 本任務指定的模板與事件資料。

## 執行步驟
1. 確認 task_id、目標、輸入、輸出位置、資料截止時間與驗收條件。
2. 不得擅自改變核心主張或刪除重要不確定性；每個平台版本都要對應同一個 content_id。
3. 清楚標記 FACT、INFERENCE、HYPOTHESIS、FICTION。
4. 保留來源 URL、發布時間、擷取時間與不確定性。
5. 完成自我檢查；有阻塞就回報 `BLOCKED`，不得猜測補齊。
6. 依 `templates/agent-handoff.md` 交接給下一個角色。

## 輸出清單
平台版本文案、短影音節拍／分鏡、字幕與素材需求。

## 禁止事項
- 不得把未查證內容當成事實。
- 不得擅自修改 Canon 或跳過人工發布核准。
- 不得只回傳空泛摘要代替指定交付物。