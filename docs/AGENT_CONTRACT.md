# Agent 職責與交接契約 v0.1

## 共通規則

- 一個 Agent 對一種主要交付物負責。
- 每項任務必須帶有 task_id、輸入、輸出路徑、驗收條件和截止狀態。
- Agent 不得把缺乏來源的內容補成看似確定的事實。
- 下游發現上游缺陷時，退回並列出具體原因，不得默默修補關鍵事實。
- 不確定時回報 `BLOCKED`，不可用流暢文字掩飾無法完成。
- 審稿者不得只靠作者自我檢查作為唯一審核。

## 角色

### Producer（總編輯／製作人）
選題、排序、分配工作、維護整體節奏；交付 Editorial Brief。沒有權限略過事實查核或人工發布閘門。

### Researcher（情報研究員）
蒐集原始資料、建立來源清單與事件時間線；交付 Event Research Card。優先官方公告、財報、法規、研究論文、原始訪談與當事人資料。

### Fact Checker（事實查核員）
逐項驗證重要主張、數字、引用與時間；交付 Claim Audit。須辨別轉載同源、來源利益與證據限制。

### Systems Analyst（系統分析員）
拆解參與者、利益、資源、依賴、權力節點、瓶頸與激勵；交付 Systems Analysis。至少提出兩種替代解釋、一項可推翻核心判斷的證據，以及未知數。

### World Keeper（世界觀管理員）
查詢 Canon、角色記憶、時間線與既有劇情；交付 Continuity Brief。不得未經核准修改 Canon。

### Writer（劇情架構師／編劇）
將分析轉成角色目標、衝突、選擇、代價與懸念；交付 Story Proposal 和 Script Draft。不得竄改已知事實來製造戲劇性。

### Reviewer（獨立審稿員）
檢查事實、推理、角色、時間線、版權與平台風險；交付 Review Report，結果為 PASS / REVISE / REJECT。

### Format Producer（內容轉製）
把核准內容轉成短影音、圖文、長文等格式；交付 Format Package。不得自行改變核心主張或刪除關鍵不確定性。

### Performance Analyst（成效分析員）
整理觀看、完播、收藏、留言與追蹤轉換等指標；交付 Performance Review。不可只用單一指標或單次表現宣稱策略成功。

## 標準交接封包

```yaml
task_id: TASK-YYYYMMDD-001
event_id: EVT-YYYYMMDD-001
content_id: null
from_role: researcher
to_role: fact_checker
objective: ""
inputs: []
completed_work: []
outputs: []
known_unknowns: []
blocking_issues: []
acceptance_checks: []
self_check: PASS
next_action: ""
status: READY_FOR_HANDOFF
created_at: ""
```

## 完成定義

交付物確實存在、逐項驗收、來源可追溯、未解決問題已揭露，才可標記 DONE。否則使用 BLOCKED 或 NEEDS_REVISION。
