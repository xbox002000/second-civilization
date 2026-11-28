# 電影質感提示詞工藝（用戶 2026-11-28 提供，供 Muse 參考與 agy 討論）

> 核心論點：電影質感來自精確的攝影與導演指令（導演語言），不是堆砌 cinematic／masterpiece／8K／epic 等詞，也不是把提示詞寫長。

## 核心公式（優先順序）

1. **光源與光質**（最高優先）：明確光源方向、質感、色溫。例：soft warm window light from the left, gentle falloff, dust visible in the beam。忌只寫 cinematic lighting。
2. **鏡頭與景別**：具體焦段＋景別＋一項主運鏡。例：35mm medium shot, slow dolly in with small amplitude。忌堆砌 dynamic camera, epic angles。
3. **可觀察動作**：以具體物理動作描述情緒。例：shoulders drop, gaze lowers, fingers tighten on the cup。忌只寫 she feels sad。
4. **色彩與調色**：有限調色盤＋對比控制。例：restrained cool-blue and amber palette, low saturation, soft highlight roll-off。忌只寫 cinematic color grade。
5. **聲音設計**：環境音＋物理音效（配樂可選）。

## 單鏡頭結構

```text
Live-action cinematic, [焦段] [景別] of [主體].
[具體物理動作，按時間順序].
[單一主運鏡 + 幅度/速度].
[明確光源與光質].
[有限調色盤 / 材質質感].
Sound: [環境音 + 物理音效]. No music / or restrained score.
```

## 多鏡頭寫法

- 用 [Shot 1]、[Shot 2] At 00:03.500 明確時間點。
- 每個切鏡必須帶來新資訊（新角度／新空間／新情緒），否則改用運鏡。
- 每個 Shot 內只給一個主運鏡。
- Ref2VA 模式下明確指定每個參考素材的職責（身份／場景／運鏡參考）。

## 實戰加分項

1. 微表情與呼吸：眨眼、視線移動、呼吸胸部起伏、嘴角微動，比大動作更有電影感。
2. 物理真實性：布料慣性、頭髮隨風、腳步與地面接觸、光影變化。
3. 控制複雜度：5–8 秒單鏡通常比硬塞多事件的 15 秒更穩定、更有質感。
4. 參考素材分工：人物圖鎖身份與服裝／場景圖鎖環境與光向／運鏡影片鎖路徑與節奏；提示詞專注「這次要發生什麼」。
5. 聲音是電影感的一半：明確環境底噪（雨聲、腳步、呼吸、金屬碰撞）。

## 生成前快速檢查清單

- 有明確光源方向嗎？／只有一個主運鏡嗎？／動作是可觀察的物理描述嗎？／調色有限且克制嗎？／聲音有被設計嗎？／時間線與片長匹配嗎？
