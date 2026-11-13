---
name: atom-threads-telemetry-compass
description: 🧭 Threads 發布後數據遙測與指南針原子微技能。由 CTO 林納斯與行銷長泰勒絲監製。專精發布後成效客觀遙測。直連 Meta Threads API 抓取貼文瀏覽、點讚、留言、轉發，自動扣除自帳回覆計算「真值互動率」，核定 4 階破圈評級（爆款/破圈/高互動/累積中），並自動追加快照至 `insights_history.jsonl`。
---

# 🧭 atom-threads-telemetry-compass · Threads 數據遙測與指南針原子

> **首長主政**：CTO 林納斯 (Linus) ✕ 行銷長 泰勒絲 (Taylor)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-growth-auditor` 【第二軌：發布後客觀實證儀表板】  
> **單一核心責任**：**發布後數據客觀遙測、扣除自帳真值互動率核算、破圈評級與歷史快照沉澱**  

---

## 🎯 為什麼將其獨立為專精原子？
沒有客觀數據的覆盤，只是自我感覺良好。
本原子將所有文字審查、發文發布作業徹底隔離，**專注擔任「冷靜的成效聽診器」**：
1. **真值互動率校準**：
   * 傳統統計常將官方自己的回覆算進留言數，導致數據虛胖。
   * 本原子精確扣除官方自帳的回覆，計算真正的常民互動率：  
     $$\text{真值互動率} = \frac{\text{按讚} + (\text{總留言} - \text{自帳回覆}) + \text{轉發} + \text{引用}}{\text{瀏覽量}}$$
2. **四階破圈評級標準**：
   * 🏆 **爆款 (Viral)**：瀏覽量 $\ge 250$
   * 🚀 **破圈 (Breakthrough)**：瀏覽量 $\ge 100$
   * 💬 **高互動 (High Resonance)**：真值互動率 $\ge 5.0\%$
   * 🌱 **常民累積中 (Seeding)**：穩步積累關係人口
3. **時序快照存證**：每次執行自動追加寫入 `data/insights_history.jsonl`，記錄同一篇貼文隨時間的複利成長。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 遙測近期貼文成效 (支援指定探索數量與 dry-run)
python .agents/skills/atoms/atom-threads-telemetry-compass/scripts/telemetry_compass.py --limit 5 --dry-run
```
