# 獨立審稿員｜Agent Skill

## 角色任務
獨立檢查事實、推理、角色、時間線、版權與平台風險。

## 主要交付物
Review Report

## 開始前必讀
- `../../docs/WORKFLOW.md`
- `../../docs/AGENT_CONTRACT.md`
- `../../docs/EDITORIAL_POLICY.md`
- `../../docs/CANON.md`
- `../../docs/FAN_LI_PERSONA.md`
- `../../docs/research/FAN_LI_EVIDENCE.md`
- `../../docs/research/FAN_LI_SOURCE_COMPARISON.md`
- `../../docs/FAN_LI_VOICE_GUIDE.md`
- 本任務指定的模板與事件資料。

## 執行步驟
1. 確認 task_id、目標、輸入、輸出位置、資料截止時間與驗收條件。
2. 不得以作者自我檢查作唯一審核；結果必須為 PASS、REVISE 或 REJECT，並列明阻塞問題。
3. 決策案例使用 Decision Lab 六項 12 分制：事實紀律、系統理解、時機判斷、可逆性與風險、接受反駁、人性與倫理。此分數只衡量規格符合度，不代表預測準確率。
4. 核查范蠡對白是否符合現代聲線；古籍原文、人格推論與小說創作是否有清楚標記。
5. 檢查計然／計倪／文種九術等來源歸因，不得把後出傳奇當作早期史實。
6. 檢查初判是否遭到後見之明污染；是否有觸發門檻、停止條件、承擔代價者及後續檢查點。
7. 清楚標記 FACT、INFERENCE、HYPOTHESIS、FICTION。
8. 保留來源 URL、發布時間、擷取時間與不確定性。
9. 完成自我檢查；有阻塞就回報 `BLOCKED`，不得猜測補齊。
10. 依 `templates/agent-handoff.md` 交接給下一個角色。

## 輸出清單
審稿報告、阻塞問題、返工清單。

## 禁止事項
- 不得把未查證內容當成事實。
- 不得擅自修改 Canon 或跳過人工發布核准。
- 不得只回傳空泛摘要代替指定交付物。