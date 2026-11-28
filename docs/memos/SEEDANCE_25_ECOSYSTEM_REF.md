# Seedance 2.5 開源生態調研（2026-11-28，Muse 實查）

> 用戶提供初步彙整，本檔為逐項核實＋深讀後的借鑑評估。只讀評估，未安裝任何 skill（依減法紀律與社群套件紅線）。研究副本在 ~/workspace/research_seedance/（四個 repo 的 shallow clone）。

## 一、專案核實（2026-11-28 GitHub 實查）

| 專案 | 星數 | 授權 | 狀態 | 備註 |
|---|---|---|---|---|
| liyue-aigc/seedance-2-5-video-director | 826 | MIT | 2026-11-27 仍更新 | 與用戶彙整相符；中文導演 Skill，不呼叫付費 API |
| nutllwhy/seedance-tvc-director | 362 | MIT | 2026-11-27 更新 | TVC 廣告專向，本專案暫無關 |
| T8mars/ComfyUI_Seedance | 54 | 未標 | 2026-11-25 更新 | ComfyUI 節點，走第三方低價 API |
| paperfoot/seedance-cli | 27 | MIT | 2026-11-01 更新 | Rust CLI，需自備 API 存取 |
| xianyu110/awesome-seedance-2.5 | **僅 5** | NOASSERTION | 2026-10-23 | 用戶彙整未標星數；屬案例庫而非熱門專案，引用時勿高估 |
| allenGKC/Seedance-2.5、sjinn-ai/seedance2.5-skills、woodfantasy/Seedance-ShotDesign-Skills | API 限流未查得 | — | clone 成功、結構與描述相符 | woodfantasy 內容最厚（cinematography／micro-expressions／multimodal-references 等 15 份 references） |

## 二、可借鑑方法（提示詞側，零成本，建議經 agy 討論後併入我方規格）

1. **資產鎖定表＋「不繼承」欄**（liyue `multimodal-patterns.md`）：每項參考資產寫成 scoped contract——來源＋借用特徵＋作用對象/時段＋受保護不變量＋**明確不繼承項**（背景、文字、版式、原音軌）。我方 V3 槽位規格只寫「負責什麼」，缺「不繼承什麼」——這正是參考圖背景/光線污染生成的已知失敗模式，建議補入 script_pack 的 asset_refs 欄位設計。
2. **一維度一權威**（allenGKC `references.md`）：identity／首尾幀／動作／運鏡／環境／音色／音樂／時序／風格，每維度只能有一個 owner，兩個 owner 即衝突；不擁有任何維度的資產直接移除。比我方現行分工表更乾淨的表述，可作 QC-0 檢查原則。
3. **跨鏡身分錨點清單**（woodfantasy `multimodal-references.md`）：每角色指定 2–3 個永久可見的區別標記，列入 continuity bible 不變量（其範例即「左眉淺疤＋銀戒指＋口袋鋼筆」）。范蠡已有天然錨點（左眉尾疤、方孔錢、低束髮/低馬尾），但未形式化為錨點清單——建議在角色聖經明列，QC-1/QC-2 對照表逐項核對（與 costume_4pt 欄位銜接）。
4. **人物參考的預設範圍與未見側重建規則**（liyue）：人物參考圖預設＝完整可見角色（身分＋臉＋髮型＋體型＋服裝＋配飾），除非明示「只參考臉」；未拍到的側面/背面須依可見的剪裁、顏色、材質、穿法一致重建，不得另發明一套。此規則正對 Step 0 右側臉盲區的處置邏輯。
5. **微表情圖庫＋強度四級＋情緒弧線時間軸**（woodfantasy `micro-expressions.md`，488 行）：面部七分區詞庫、L1 克制→L4 爆發強度標尺、2 秒精度的微表情時間軸編排、反 AI 假臉禁忌詞。我方導演層有 performance_beat {from, trigger, to} 結構但無表情詞彙與強度標尺——這是 DEMO-02「表演僵硬」失敗的直接補強材料，建議收斂為我方 bible/performance 詞表（比照 named_shots.yaml 的自建方式，不整包移植）。
6. **音色綁定句式**（liyue／woodfantasy）：每句對白綁定角色＋音色來源＋時段＋保留特徵（音高、停頓、呼吸、強度），禁止一句「用 @Audio 1」帶過。與我方 TTS 全合成路線相容（綁定對象換成 voice_id＋表演參數）。
7. **穩定主體數經驗值**（woodfantasy）：影片/音訊主體 1–5 最穩、圖像主體 1–8 最穩，超出漸不穩——可作 Ref2VA 餵圖數與雙人鏡拆分決策的參考線。

## 三、Seedance 2.5 引擎本身（付費，另案決策）

- 原生能力（據上述 skill 文件與官方手冊轉述）：最多 30 圖／10 影片／10 音訊參考、4–30 秒單 clip、30–180 秒 Long Video、白模（clay）影片輸入、原生對白與音色綁定、多人物獨立綁定。功能面幾乎覆蓋我方 H3 Ref2VA＋CozyClay＋TTS 鏈的合體。
- 存取與價格（2026-11 中旬多來源一致，檢索 2026-11-28）：官方 BytePlus ModelArk API——5 秒 720p 約 $1.16、10 秒約 $2.31（token 計價 $10.70/百萬）；2.5 Flash 5 秒 720p 約 $0.76；啟用門檻為帳戶持有 $30 credits/資源包。Replicate 同價（$0.2312/秒）；fal 約 2 倍。Dreamina 消費版約 $15/月、每支 5 秒 720p 攤約 $1.76。
- **成本警告**：廢片全額計費——以我方抽卡倍率（N=2–3）計，每支留用 5 秒 720p 實付約 $2.3–3.5，是全新支出線（現行 Flow 走訂閱點數、H3 走 Colab 沉沒成本）。導入與否屬生產決策，須經用戶拍板＋agy 工作流討論，不在本調研授權內。
- 生態註記：用戶的現代裝角色卡即豆包（ByteDance）生成，Dreamina 為同生態；若日後試 Seedance，資產鏈同生態可能略減轉換摩擦（未驗證，僅記錄）。

## 四、結論

- 不安裝任何上述 skill（減法紀律）；方法層借鑑第二節 1–7 項，併入路徑比照 named_shots.yaml 先例：由 agy 討論收斂成我方自有 bible/規格條文。
- 引擎層維持現行路由（Flow Omni＋H3 Ref2VA＋Wan＋LTX）；Seedance 列為「SM-7A 若不過關時」的備選試驗候選，屆時另提小額試驗案（含預算上限）請用戶拍板。
