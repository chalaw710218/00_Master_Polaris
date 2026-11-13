---
name: atom-taste-hyperlocal-design-system
description: 首席視覺長約瑟夫·極星在地常民風土美學與微動態設計系統原子 (Hyperlocal Visual Design System & Kinetic Tokens Protocol v1.0)。落實創辦人親授「約瑟夫主要負責視覺化的部分」法旨！將全球頂級設計系統（Design Tokens、和聲比例、光學校準）與台東在地風土色彩學（黑潮深藍、池上黃金稻穗、太麻里日出紅）深度融合，自動輸出可直接執行的 CSS 變數、Tailwind 設定檔與呼吸微動態 Tokens。
---

# 🎨 首席視覺長約瑟夫·極星在地常民風土美學與微動態設計系統原子 (Hyperlocal Visual Design System Protocol v1.0)

> **最高憲則法旨**：創辦人（品碩）親傳 —— **「約瑟夫主要負責視覺化的部分」**。  
> **核心職責**：將抽象的品牌靈魂轉譯為具備物理確定性的 Design Tokens，讓極星所有前端頁面與產品界面散發出兼具「大廠高級秩序」與「常民客廳煙火氣」的獨特風土美學。

---

## 一、 風土色彩學與視覺 Tokens 矩陣

```
[黑潮深藍 #0a1128] ─── 主色調：沉穩、深邃、專業安全感
[池上金   #d4af37] ─── 亮點色：陽光、豐收、尊貴溫暖
[太麻里紅 #e63946] ─── 警示/主動色：第一道曙光、熱情、活力
[常民米白 #f8f9fa] ─── 背景底色：紙本溫度、不刺眼、高齡友善
```

1. **字體光學和聲 (Typography Scale)**：
   * 採用 Modular Scale 1.25（Major Third 和聲），嚴守標題 48px / 38px / 30px / 24px / 內文 16px / 輔助 14px 階梯。
2. **克制呼吸微動態 (Kinetic Tokens)**：
   * `ease-out-cubic`: `cubic-bezier(0.33, 1, 0.68, 1)`（自然回彈，0 拖泥帶水）。
   * 按鍵懸停微抬升 2px，點擊微下沉 1px，給予前線外送員與高齡長輩最明確的觸覺視覺回饋。

---

## 二、 執行工具規範

* 執行腳本：`scripts/hyperlocal_design_system.py`
* 支援指令：
  ```bash
  python scripts/hyperlocal_design_system.py --export-tokens --format "tailwind"
  python scripts/hyperlocal_design_system.py --export-tokens --format "css"
  ```
