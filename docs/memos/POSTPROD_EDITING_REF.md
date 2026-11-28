# 後製／剪輯工具參考資料（Creator 2026-11-28 提供，未經我方查證）

## 第一批：MCP Agent 剪輯器（2026 年 11 月主流做法）
- **Editroom**（robbietilton/Editroom）：僅 macOS（Apple Silicon），MIT，約 12MB，原生 MCP，多 AI 光標操作時間軸，4K 預覽／調色／字幕／混音。中文圈近期最火，搭配 Antigravity 做數字人批量剪輯。
- **WeftCut**（WeftCut/WeftCut，weftcut.com）：macOS／Windows／Linux，MIT，定位 Agent-native 剪輯器，完整 MCP 端到端操作時間軸（裁切／字幕／關鍵幀／效果／匯出），編輯即時反映。
- **Pireel**（pireel/pireel，約 1.5k–2k stars）：瀏覽器為主，AGPL-3.0，MCP 操作畫布／時間軸／字幕／B-roll，可匯出 Premiere／DaVinci 時間線。適合口播類。
- **FableCut**（ronak-create/FableCut）：瀏覽器零依賴，MIT，整個時間軸即一個 JSON 檔，Agent 經 MCP／REST 改 JSON，約 150ms 即時更新；多軌／關鍵幀／轉場。適合輕量短片／Reels。
- 其他：MakeMyClip Editor（MIT，MCP＋本地 Whisper，去靜音／逐字字幕／匯出 FCP／Resolve／Premiere）；CapCut MCP 社群伺服器（CapCut 本身非開源）；FFmpeg MCP Server（命令列層級，非完整 NLE）。
- 彙整建議：Mac 數字人→Editroom；跨平台 Agent 端到端→WeftCut；瀏覽器即時看→Pireel／FableCut；輕量 JSON→FableCut。

## 第二批：@okapi_fukugyo 推文 14 個免費工具（經作者確認可在無 GPU 環境運作）
1. Remotion Skills（remotion-dev/skills）：讓 AI 代理學 Remotion 最佳實務。
2. Blender：完整 3D 套件，可 Python／指令列自動化。
3. faster-whisper（SYSTRAN）：語音轉文字含時間戳，自動字幕；CPU 可跑（large-v3 int8）。
4. Piper（OHF-Voice/piper1-gpl）：本地 TTS，多語言。
5. GSAP：JS 動畫庫，時間軸控制文字／物件動畫。
6. auto-editor（WyattBlue）：自動剪無聲／低動作片段。
7. Chrome DevTools MCP：代理查看／除錯瀏覽器畫面。
8. FFmpeg：編碼／合併／濾鏡／匯出，幾乎所有工具的最終層。
9. Remotion：React 程式化影片（元件／動畫／資料驅動）；個人與 3 人以下團隊免費。
10. Impeccable（pbakaus）：給代理的設計詞彙與審查（polish／critique／audit），去 AI 味設計。
11. Three.js：瀏覽器 3D（WebGL／WebGPU）。
12. MoviePy：Python 剪輯庫（剪輯／拼接／文字／合成／特效）。
13. Openverse：CC／公有領域圖片音訊搜尋，API 免 Key 基本使用，須逐筆確認授權。
14. HyperFrames（heygen-com）：HTML＋時間屬性寫影片，支援 GSAP／Three.js，渲染 MP4，可搭配 AI 代理技能。

使用建議（原文）：整份清單貼給 AI 編碼代理，依需求自動選組：聲音 Piper、字幕 faster-whisper、剪輯 auto-editor、動畫 GSAP／Remotion／HyperFrames、3D Blender／Three.js、素材 Openverse、匯出 FFmpeg。
