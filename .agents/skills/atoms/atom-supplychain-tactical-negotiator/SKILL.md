---
name: atom-supplychain-tactical-negotiator
description: 預判盤商操盤手心理動機並產出高情商議價籌碼話術。在掌握底牌數據後進行供應商商務談判時使用；底層純數值拆解時不用。只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。
metadata:
  group: 管家選品
  parent: sharp-groupbuy-analyzer
  owner: 雪柔
  status: draft
  version: "1.0"
---

# 🧠 供應商商業心理戰預判與高情商議價話術原子技能 (Supply Chain Tactical Negotiator Atom)

> **核心職責**：專精於「對手操盤手心理動機解析、底牌數據戰術轉譯、高情商拆穿溢價話術、品牌法定名稱零洩漏防火牆」。  

---

## 核心功能與深度特性
1. **操盤手心理戰三大動機剖析 (Opponent Mindset Profiling)**：
   - **動機 A【恐慌溢價型】**：利用海運塞港或原料波動傳聞，故意加碼虛報溢價（對策：以真實波羅的海指數與產地期貨數據溫和戳破）。
   - **動機 B【庫存週轉型】**：面臨冷凍倉儲與臨期壓力，表面強硬但急需大量現款（對策：以「整批排程、現款週週結」換取極限底價）。
   - **動機 C【試探開高型】**：對新客戶採取「開高試探」策略，看對方是否懂行（對策：展現大盤規格專業術語，秒立行家威信）。
2. **老闆專用高情商談判話術 (High-EQ Negotiation Crafting)**：
   - 拒絕粗暴殺價（破壞商業合作），採用「感謝品質 ➔ 揭露行情常識 ➔ 提出雙贏方案 ➔ 定錨目標底價」之四步閉環話術。
3. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 談判對象為外部供應商，對外自稱強制為「生活管家」或採購主體「寶桑物流生活商行」，嚴禁出現內部代號「極星」。

---

## 執行腳本
```bash
python scripts/tactical_negotiator.py --item "智利冷凍鮭魚" --quote 450 --target 375 --strategy "turnover" --dry-run
```
