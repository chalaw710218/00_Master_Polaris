---
name: atom-photo-classifier
description: 👁️ 照片視覺語意精準分類原子微技能。由首席科技偵察官艾達 (Ada) 與首席視覺長約瑟夫監製。專精在創辦人輸入單張照片時，快速進行視覺特徵分析與 OCR 語意提煉，確定性判定三條戰術路線（EVENT_POSTER, SOURCING_PRODUCT, FOUNDER_LIFE），並輸出標準分類結構。
---

# 👁️ atom-photo-classifier · 照片視覺語意精準分類原子

> **首長主政**：首席科技偵察官 艾達 (Ada) ✕ 首席視覺長 約瑟夫 (Josef)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`one-shot-photo-marketer` 【Step 1：視覺與語意自適應分類】  
> **單一核心責任**：**輸入單張照片，進行毫秒級特徵識別與 OCR 萃取，精準判定三條業務路線**  

---

## 🎯 為什麼將其獨立為專精原子？
分類是一切後續動作的導航中樞。
本原子將所有文案撰寫、情報挖掘與發布邏輯徹底隔離，**專注做好「一眼看穿照片本質的慧眼」**：
1. **三大確定性戰術路線**：
   * 🎫 **`EVENT_POSTER`（活動海報）**：含有日期、地點、講座、工作坊、繪本、文化展演。
   * 🥩 **`SOURCING_PRODUCT`（生鮮選品）**：肉品、海鮮、農產、原物料樣品、價格包裝。
   * 🛵 **`FOUNDER_LIFE`（創辦人日常）**：外送後照鏡、家宅修繕、代碼螢幕、深夜理貨、街景。
2. **結構化要素提取**：
   * 提取關鍵時間、地點、品名與視覺氛圍，作為下游文案原子開工的純淨原料。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 輸入照片路徑或描述進行分類判定
python .agents/skills/atoms/atom-photo-classifier/scripts/photo_classifier.py --input "20261113_taitung_bread_workshop.jpg" --notes "草民舉辦的週末野莓酸種烘焙分享會" --dry-run
```
