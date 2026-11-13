---
name: atom-growth-quality-gate
description: 📐 萬用戴明五維品質出廠安燈閘門 (Universal Deming Andon Quality Gate)。由首席品質長戴明博士 (Dr. Deming) 親自掌舵。適用於任何社群貼文 (Threads/FB)、實體海報文案、LINE 對話、客服話術與商業交付物。五維嚴格打分，低於 90 分或觸犯品牌紅線即一票否決。
---

# 📐 atom-growth-quality-gate · 萬用戴明五維品質出廠安燈閘門

> **首長主政**：首席品質長 戴明博士 (Dr. Deming · CQO)  
> **法規監製**：法務長 雪柔 (Falcon · CIO)  
> **核心定位**：**全域萬用出廠質檢微技能 (Universal Quality Gate Atom)**  

---

## 🎯 為什麼是「萬用出廠安燈」？
在傳統流程中，品質檢驗常依附在特定渠道（例如只在發 Threads 前看一眼）。
戴明博士親定：**「品質是全系統的靈魂，安燈閘門必須是萬用的！」**
任何對外或交付創辦人的文字成果（無論是 Facebook 貼文、Threads 短文、海報標題、LINE 官方帳號問候，還是家訪破冰話術），出廠前一律呼叫本原子進行客觀、形式化審查。

---

## 📊 萬用戴明五維評分矩陣 (Five-Dimensional Andon Matrix)

| 維度 | 權重 | 審查要點與扣分標準 |
| :--- | :---: | :--- |
| **1. 品牌紅線 (Brand Line)** | **一票否決** | 嚴禁出現「極星」、「Polaris」等內部代號（發現即 0 分否決）。對外自稱法定「生活管家」。 |
| **2. 去 AI 塑料感 (Anti-AI Tone)** | **25%** | 排除「親愛的、探索、引領、助力、賦能、讓我們一起」等虛浮 AI 詞彙。 |
| **3. 常民共鳴度 (Folk Resonance)** | **25%** | 是否具備市井煙火氣、柴米油鹽、打工人真實體會或店貓真實行為。 |
| **4. 留白與節奏感 (Pacing & Breath)**| **25%** | 避免大段擁擠文字壁，是否有適當換行、呼吸感與短促有力的金句。 |
| **5. 合規與真實度 (Fact & Safety)** | **25%** | 無誇大療效、無違法保證、無聳動假消息，實事求是。 |

---

## 💻 物理調用介面 (Universal CLI Interface)

```bash
# 萬用檢驗任何文案或發布內容
python scripts/quality_gate_deep.py --text "今天台東下著細雨，生活管家準備了熱茶，歡迎進來避雨歇歇腳。"
```

### 輸出範例 (Universal JSON)
```json
{
  "status": "PASS",
  "total_score": 96.0,
  "andon_light": "GREEN",
  "dimensions": {
    "brand_compliance": 100.0,
    "anti_ai_tone": 95.0,
    "folk_resonance": 95.0,
    "pacing_breath": 94.0,
    "legal_safety": 100.0
  },
  "feedback": "文字溫暖、具備真實場景感，無 AI 塑料套話，准予出廠發布。"
}
```
