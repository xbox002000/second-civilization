# 架構決策紀錄（ADR）

## ADR-001：獨立專案倉庫
- 狀態：ACCEPTED
- 決策：第二次文明使用獨立 GitHub repository，不放入 `My-AI-Novels`。
- 原因：`My-AI-Novels` 原本保存《臥龍豆包》小說稿，避免不同 IP 的 Canon、素材與工作流程混雜。

## ADR-002：先建立工作流，再開發自動化
- 狀態：ACCEPTED
- 決策：先用 Markdown 規格、模板和人工／半自動流程跑通一集，再開發整合程式。
- 原因：先驗證真正需要自動化的環節，避免先做出複雜但無法交付內容的系統。

## ADR-003：GitHub / AFFiNE / Paperclip 分工
- 狀態：PROPOSED
- 決策：GitHub 保存正式規格與版本；AFFiNE 用於視覺化知識庫；Paperclip 負責 Agent 任務編排。
- 待驗證：AFFiNE 與 Paperclip 的實際資料同步方式、可用 MCP 工具與權限。

## ADR-004：人工發布閘門
- 狀態：ACCEPTED
- 決策：MVP 階段所有對外發布皆需人工核准。
