# MiniMax H3 運鏡控制參考（用戶 2026-11-28 提供，供與 agy 討論）

> 來源：用戶提供的彙整資料（稱據 MiniMax 官方提示詞指南，Hugging Face MiniMax-H3 repo 之 `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` 與 ref 版本；未經我方獨立查證，討論時由 agy 對照官方文件核實）。

## 總論
H3 運鏡以「提示詞＋官方詞表」為基礎；複雜／精準運鏡轉向「白膜／Clay 預演（Previs）＋參考影片（Ref2VA）」。兩種都是主流，後者在需要可控鏡頭路徑時更可靠。

## 1. 提示詞運鏡（官方基礎）
- H3 沒有獨立運鏡控件，鏡頭運動靠文字進入模型；官方提供固定詞表（約 12–20 種基礎動作），須用規定說法，否則容易失效。
- 詞表核心：Zoom In/Out、Tilt Up/Down、Pan Left/Right（機身不動類）；Push In/Pull Out、Truck Left/Right、Pedestal Up/Down、Arc Shot、Tracking Shot（整機移動類）；Static Shot、Shake Slightly/Strongly、POV、Roll Clockwise/Counterclockwise。
- 寫法公式：`運動類型 +（可選）幅度 +（可選）速度`，自然嵌進句子；中幅常速可省略。每鏡只寫一次主要運鏡，並搭配景別。
  - 例：`The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.`
- 官方三段式結構最穩：`integrated_multimodal_description`（含 `[Shot 1]`、時間戳切鏡如 `At 00:03.500, the camera cuts to ...`）／`overall_soundscape`／`non_diegetic_music`。
- 社群另有提示詞生成器、Camera Motion LoRA、named shots 技能包（dolly zoom、whip pan、360 orbit 等以基礎詞組合成句）。
- 缺點：複雜路徑（多段複合、精確速度／弧線）容易不穩或被模型自行解讀。

## 2. 白膜預演＋Ref2VA（精準運鏡主流進階）
- 原理：先以 Blender 等工具做灰色／白模預演動畫，精準控制鏡頭路徑、速度、主體走位與時序，輸出短片作 reference video 餵 H3 Ref2VA；提示詞明示「Follow the composition, subject positions, camera path and timing of <Video 1> exactly, frame by frame. Replace materials with ...」，模型保留幾何／路徑／時序，換上寫實材質、光影與原生音效。
- 白模優勢：給模型清晰的視差與尺度線索，又不洩漏最終外觀。
- 成熟工作流：Mickmumpitz 的 clay-to-cinematic、各種 ComfyUI 圖、Stage 工具。
- 缺點：需要 3D／預演工具能力，受參考影片總時長限制。

## 3. 輔助方式
- 首尾幀（FL2VA）：鎖開場／結束構圖，運鏡靠中間提示詞補。
- 參考圖＋提示詞：鎖外觀，運鏡靠文字。
- LoRA／節點：Camera Motion LoRA（觸發詞 `camera motion`）；ComfyUI 社群有 Camera H3 類視覺化相機編輯節點。加速 LoRA 步數太低可能抑制運鏡。

## 4. 實務建議（用戶資料結論）
- 簡單快速日常：官方詞表寫提示詞已夠。
- 精準路徑／複雜運鏡／導演級控制：優先白膜 Previs＋Ref2VA（社群驗證最穩）。
- 兩者可結合：白模鎖路徑，提示詞細化風格與細節。

## 5. 社群 Skill 資源（僅供討論評估，未經授權不得安裝）
- `minimaxh3-shots-skills`（loopforge0）：12 種官方基礎運鏡組合成 named shots（dolly zoom、crash zoom、whip pan、snorricam、360 orbit、crane rise 等），每 shot 附實測提示詞、失敗原因、可靠性標註，附 `build_prompt.py`。https://github.com/loopforge0/minimaxh3-shots-skills
- `h3-camera-motion-lib`（swan7-py／MiniMax-H3-Skills-Local）：中文運鏡提示詞庫，可直接貼 `detailed_description` 的中文鏡頭句，標註實測狀態（成立／部分成立／失敗）、推薦 LoRA 與寫法紀律。https://github.com/swan7-py/MiniMax-H3-Skills-Local/tree/main/h3-camera-motion-lib
- 官方 `h3-prompt-writing`（MiniMax-AI/MiniMax-H3 repo 內 skills）：提示詞結構（三段式／Ref2VA 六段式）、欄位順序、時間戳、參考標籤。https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- 建議優先序（用戶資料）：先官方結構 skill → 再 named shots skill → 中文工作流再加中文運鏡庫。
