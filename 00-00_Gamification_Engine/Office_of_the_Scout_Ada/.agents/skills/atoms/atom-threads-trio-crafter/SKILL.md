---
name: atom-threads-trio-crafter
description: 🎭 友店互動三風格走心擬稿工匠原子微技能。專精針對在地友店貼文內容語意，同時生成「溫暖慢活影」、「幽默鄰里影」與「傲嬌吃貨喵編」3 組極高情商留言草稿，並輸出帶有 `reply_to_id=友店貼文ID` 的標準發送 payload，供一鍵登門回覆。
---

# 🎭 atom-threads-trio-crafter · 友店互動三風格走心擬稿工匠

> **首長主政**：生活管家 影 (Kage) ✕ 店貓 喵編 (Meow Editor)  
> **敘事監製**：行銷長 泰勒絲 (Taylor)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-rss-sentinel` 【步驟 4~5：走心擬稿與呈報】  
> **單一核心責任**：**依友店貼文語義生成 3 組高情商走心草稿，並輸出帶有 `reply_to_id` 的即發 payload**  

---

## 🎯 為什麼將其獨立為專精原子？
對友店的留言不能是一成不變的罐頭回覆，必須「看懂對方的辛苦與特色」。
本原子專精於「人設立體化與即發閉環」：
1. **三大風格光譜**：
   * 🌿 **風格一【溫暖慢活 · 影】**：看懂職人苦心，致敬台東慢活步調。
   * ☕ **風格二【幽默鄰里 · 影】**：鄰居串門打趣，滿滿人情味。
   * 🐾 **風格三【傲嬌吃貨 · 喵編】**：真貓視角，自稱「本喵」，以食物或打盹打破嚴肅。
2. **直通發送底座 (Payload Ready)**：
   * 產出的每一組草稿都自動附帶 `target_post_id`，創辦人或上游管線只需選擇其中一組，即可直接傳入 `atom-threads-post-dispatcher`，精準發布在該友店貼文下方！

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 針對特定友店貼文擬稿 (輸入貼文文字與 post_id)
python .agents/skills/atoms/atom-threads-trio-crafter/scripts/trio_crafter.py --post-id "th_post_hungry_088" --text "今天台東風好大！大骨肉骨茶剛出爐" --dry-run
```
