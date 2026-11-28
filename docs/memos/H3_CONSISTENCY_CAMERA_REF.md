# H3 人物一致性＋電影運鏡方法彙整（用戶 2026-11-28 提供，待查證）

> 用戶提供之社群方法彙整。內容未經查證，僅作評估線索；查證與取捨見 agy 備忘錄（另檔）。

## 一、人物一致性
- **RefMod**：用 4–10 張角色圖（正臉、側臉、全身）做成 ~1–2MB 小檔，像 LoRA 一樣載入，不用訓練。資源：`ComfyUI-MiniMaxH3Mod`、Stable Yogi／LoRAtech 工作流。
- **多角度 Character Sheet**：Turnaround Sheet（正、3/4、側、背＋臉部特寫）餵 Ref2VA；Qwen Image 生成 sheet。
- **Character Swap LoRA**：參考圖＋Guide Video 把影片人物替換成目標角色，保留動作與運鏡。資源：Alissonerdx／Akatz Labs。
- **首幀鎖定＋多參考**：圖像模型先生成高品質首幀鎖臉，再進 H3 I2V／Ref2VA。
- **傳統 LoRA**：自訓，最穩最麻煩。
- 提示詞分工：`<Picture 1>` 只負責身份（臉、髮型、服裝），不負責運鏡或場景。

## 二、電影級運鏡
- **Camera H3（bruxosdovfx）**：ComfyUI 視覺化運鏡編輯器，拖曳設關鍵幀，自動生成 H3 運鏡提示詞。GitHub: `NyckM/3d-Camera-control-H3-Minimax`。
- **Stable Yogi 11 Camera Shots**：11 種實測運鏡 Prompt＋工作流。
- **H3 Camera Control（Azimuth/Elevation）**：角度參數控制環繞／推拉，RunComfy 有現成工作流。
- **Depth／Camera Reference**：運鏡影片或白膜預演當參考，H3 跟隨（Floyo、Mickmumpitz Clay-to-Cinematic）。
- 搭配：Stage／CozyClay 白膜 → Greybox 當 `<Video 1>`（運鏡），角色圖當 `<Picture 1>`（身份），Prompt 明確分工。

## 三、推薦組合（原文）
1. 日常最穩：Character Sheet → RefMod → Ref2VA（多參考）＋運鏡提示詞。
2. 電影感運鏡：Camera H3 或 Stage 白膜 → 運鏡參考 → RefMod 進 Ref2VA。
3. 已有表演影片換人：Character Swap LoRA。
