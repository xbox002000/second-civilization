# 白膜／Clay／Greybox 預演開源工具參考（用戶 2026-11-28 補充提供，供與 agy 討論）

> 來源：用戶提供的彙整資料，未經我方獨立查證；討論時由 agy 只讀評估各專案（不安裝）。

## 1. CozyClay（用戶資料評：最推薦，功能最完整）
- GitHub：https://github.com/HaD0Yun/CozyClay
- 瀏覽器內開源 Previs 工具：簡單幾何體／Clay 角色排場景、走位、運鏡、切鏡，匯出 Greybox 參考影片＋首尾幀＋Prompt，可餵 MiniMax H3、Seedance、Kling 等。
- 純瀏覽器運行（`npx cozyclay`），不需 GPU 或複雜環境；支援時間軸、Dolly Rail、鏡頭限制提醒、MCP／Agent 控制。

## 2. Stage（專為 MiniMax H3 運鏡設計）
- GitHub：https://github.com/aledige63/Stage ；線上試用：https://aledige63.github.io/Stage/
- 簡單 3D 場景＋中性假人設計精確運鏡（orbit、dolly、crane、push-in、zoom 等），匯出 Greybox 參考影片＋對應英文 Prompt，專門給 H3。
- 運鏡控制細：支援 easing、弧線、翻滾；灰色假人提供清晰視差線索，不洩漏最終外觀。

## 3. CodeVideoModel（Microsoft Research）
- GitHub：https://github.com/code-video-model/CodeVideoModel
- 程式碼（Three.js）Previs：Prompt → AI 生成可編輯 Three.js 場景（含鏡頭、物體運動、物理）→ 渲染低模 Proxy 影片 → 交凍結的 MiniMax H3 生成最終影片。
- Apache-2.0；結構高度可控、可預覽修改；需要本地 NVIDIA GPU 跑 H3（我方 H3 走 Colab 閘道，此點需 agy 評估其 Previs 半段能否獨立使用）。

## 其他
| 專案 | 說明 |
|---|---|
| h3lite | Blender 白模＋H3 Ref2VA 工作流 |
| ComfyUI-Soundstage | ComfyUI 內直接做 3D Clay blocking |
| Mickmumpitz Clay-to-Cinematic | 經典「灰模影片→H3 成品」ComfyUI 流程 |

## 用戶資料的選型建議
- 最快上手、不裝重軟體 → CozyClay。
- 只想精準控制運鏡、針對 H3 → Stage。
- 程式碼／可重複性高 → CodeVideoModel。
- 已用 Blender → Blender 灰模＋現成 H3 Clay 工作流。
