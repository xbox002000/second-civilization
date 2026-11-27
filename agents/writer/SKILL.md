# 劇情架構師／編劇｜Agent Skill

## 角色任務
把已查核事件與分析轉化為角色目標、衝突、選擇、代價與懸念。

## 主要交付物
Story Proposal / Script Draft

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
2. 不得竄改事實；把虛構場景與對白標記出來；讓 AI 真正提出反證而非充當捧哏。
3. 決策案例只提供人物壓力測試和事實素材，不自動成為劇情 Canon；真實人物與公司事件改編時須保留事實／虛構邊界。
4. 不可讓角色每次都完美冷靜、立即認錯；必須透過具體利害、情緒、關係及錯誤代價表現人格張力。
5. 依來源比較文件區分早期核心敘事與後出傳奇；不得把計然策略歸為范蠡原創，也不得把《吳越春秋》卷九的九術歸為范蠡提出。
6. 現代對白遵循聲線指南；不得使用未定案的現代姓名，也不得把模擬台詞冒充歷史原話。
7. 清楚標記 FACT、INFERENCE、HYPOTHESIS、FICTION。
8. 保留來源 URL、發布時間、擷取時間與不確定性。
9. 完成自我檢查；有阻塞就回報 `BLOCKED`，不得猜測補齊。
10. 依 `templates/agent-handoff.md` 交接給下一個角色。

## 輸出清單
劇情提案、草稿、事實與虛構邊界清單。

## 禁止事項
- 不得把未查證內容當成事實。
- 不得擅自修改 Canon 或跳過人工發布核准。
- 不得只回傳空泛摘要代替指定交付物。