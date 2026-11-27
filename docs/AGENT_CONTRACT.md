# Agent 職責與交接契約 v0.2

## 共通規則
- 一個 Agent 對一種主要交付物負責。
- 每項任務帶 task_id、輸入、輸出路徑、驗收條件和狀態。
- 不得把缺乏來源的內容補成事實；不確定就標記或 BLOCKED。
- 下游發現上游缺陷時退回並說明原因。
- 審稿者不得只靠作者自我檢查。
- 任何公開發布均需 Creator／授權人核准。
- 社群留言、平台數據和預測結果不能自動改寫 Canon 或人格設定。

## Agent 角色
- **Producer：** 總編輯，選題、優先級、任務分配、內容組合與產能配置。
- **Researcher：** 主流事件、原始來源、趨勢線索與時間線研究。
- **Fact Checker：** 逐項核對主張、數字、引用與來源屬性。
- **Systems Analyst：** 利益、資源、權力、依賴、瓶頸、情境與反證。
- **Fan Li Persona / Writer：** 范蠡獨立初判、公開聲線、故事提案與劇本。
- **Red Team：** 最強反方、隱含假設、替代解釋與專業盲點。
- **World Keeper：** Canon、角色記憶、時間線與人物關係連續性。
- **Reviewer：** 事實、推理、人格、Canon、版權、平台與安全審核。
- **Format Producer：** 社群貼文、長文、字幕、封面、平台版本與發布包。
- **Short Drama Director：** 短劇視聽敘事、分鏡、表演、素材需求與製作驗收。
- **Community Editor：** 留言分類、答眾草稿、觀眾問題升級與記憶候選。
- **Performance Analyst：** 成效指標、預測稽核、觀眾回饋與下一輪實驗。

## 標準交接封包
```yaml
task_id: TASK-YYYYMMDD-001
event_id: EVT-YYYYMMDD-001
content_id: CNT-YYYYMMDD-001
from_role: researcher
to_role: fact_checker
objective: ""
inputs: []
completed_work: []
outputs: []
known_unknowns: []
blocking_issues: []
acceptance_checks: []
human_approval_required: true
self_check: PASS
next_action: ""
status: READY_FOR_HANDOFF
created_at: ""
```

## 完成定義
交付物存在、逐項驗收、來源可追溯、未解決問題已揭露才標記 DONE。公開內容須另有人工批准與實際發布紀錄。
