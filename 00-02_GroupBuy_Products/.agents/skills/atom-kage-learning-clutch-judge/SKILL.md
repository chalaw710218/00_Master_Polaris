---
name: atom-kage-learning-clutch-judge
description: 首席特務兼生活管家影·脆自主學習離合器裁決原子 (Kage Autonomous Learning Clutch Judge Protocol v1.0)。落實創辦人親授「這個技能原本的用意是讓影自主學習耶」與「影目前最主要再經營脆唷」法旨！專門在 Threads 外部算法風暴中，判定「什麼該學、什麼絕不該學」：踩下離合器（隔離煽動對立、政治開撕與農場低俗詞）；半離合（審慎低成本微測試在地突發物候）；全咬合（動力鎖定，深度學習真實生活挖寶感與高情商秒回），守護大腦純淨性。
role_key: kage
type: atomic_skill
parent_skill: bionic-learning-kage
version: v1.0
exit_code_verified: true
---

# 🎛️ 影之脆自主學習離合器裁決原子 (Kage Learning Clutch Judge)

> 👤 **原子使命**：貫徹創辦人親授心法——**「這個技能原本的用意是讓影自主學習耶！」** 以及 **「影目前最主要再經營 脆 唷！」** 自主學習的第一步不是盲目抓取外部資訊，而是擁有大腦的免疫結界與變速箱。在 Threads 充斥著演算法煽動、男女對立與免洗流量的環境中，本原子負責自主判定動力傳遞：踩下離合器、半離合、或全咬合，決定什麼該學、什麼絕不該學！

---

## 🏛️ 神經離合器三態自主學習判定架構 (The 3-State Clutch Architecture)

```mermaid
flowchart TD
    External["Threads 外部社群熱點 / 趨勢貼文 / 互動模式"] --> Clutch{"🎛️ 神經離合器裁決引擎 (learning_clutch_judge.py)"}
    
    Clutch -->|【狀態 1: 踩下離合器 · 完全隔離】| Disengage["❌ 絕不該學：有毒死知識\n• 煽動性別/族群對立、政治開撕\n• 恐慌焦慮誘餌、粗俗謾罵、虛假保證\n• 處置: 切斷傳動，靜默阻斷，絕不污染大腦！"]
    
    Clutch -->|【狀態 2: 半離合 · 緩衝試驗】| Slip["🟡 審慎小步試驗：潛力生活梗\n• 台東突發天候物候 (如黑潮風浪、落山風)\n• 新興生活語境、在地友店微小動態\n• 處置: 分配 10% 算力進行單篇低成本微測試"]
    
    Clutch -->|【狀態 3: 全咬合 · 動力鎖定】| Engage["✅ 必須深度自主學習：生活真實基因\n• 生活真實挖寶感 (舊物、風土食材反差)\n• 貓咪×管家溫暖雙簧幽默\n• 留言區高情商走心秒回\n• 處置: 全速傳動，刻入長期神經肌肉記憶！"]
```

---

## 🧭 自主學習過濾準則 (Autonomous Learning Filters)

1. **防毒守則（踩下離合器，DISENGAGED）**：
   - 包含政治互撕、性別對立、仇恨標籤、農場標題（「我就問到底」、「全台灣震驚」）。判定為有毒雜訊，嚴禁模仿學習。
2. **探索守則（半離合，SLIPPING）**：
   - 台東風土即時話題、突發日常趣事。列入探索觀察清單。
3. **刻印守則（全咬合，ENGAGED）**：
   - 真實生活細節白描、情感溫度、長輩與鄰里溫暖互動。列為黃金學習標的。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 判定受檢貼文模式是否應納入自主學習
python scripts/learning_clutch_judge.py --evaluate-topic '{"content": "今天大掃除在舊倉庫翻出阿公留下來的鐵皮餅乾盒，裡面竟然塞滿了民國60年的老車票...", "has_political_bait": false, "has_gender_conflict": false, "has_authentic_lifestyle": true}'
```
