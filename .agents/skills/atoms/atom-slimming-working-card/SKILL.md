---
name: atom-slimming-working-card
description: 🧘‍♀️ 極星三層心智·天王存摺抽脂切片與表層工作卡編譯原子 (Polaris Cognitive Working Card Scaffolder Atom v1.0)。創辦人（品碩）親自賜名「瘦身」。由執行長雪 (Yuki) 率先試驗、CTO 林納斯 (Linus) 架構監製。專門將天王數十萬字肥大 Markdown 存摺進行結構化解構抽脂，提煉當季唯一真理 Top-10 核心公理，編譯輸出總 Token 數 <= 1,500 之 Surface_Working_Card.json，常駐大腦消除注意力稀釋。
---

# 🧘‍♀️ 極星天王存摺抽脂切片與表層工作卡編譯原子 (atom-slimming-working-card)

由執行長雪 (Yuki) 業務主政、首席品質長戴明 (Dr. Deming) 安燈驗收、CTO 林納斯 (Linus) 代碼監製。

## 核心定位與職責
專門解決天王認知存摺突破 200KB（數十萬字）導致上下文滿額、注意力稀釋 (Lost-in-the-Middle) 與答非所問的硬傷。
本原子作為大腦抽脂與表層工作卡編譯終端，提供：
1. **存摺語意節點切片 (Section Chunking)**：將歷史經驗 (`01_Facts`) 與演化信念 (`02_Beliefs`) 進行語意邊界解構。
2. **唯一真理 Top-10 核心公理提煉**：依據實戰置信度、出廠次數與創辦人核定標記，篩選出當季最具實戰威力的十條精銳信念。
3. **表層工作卡導出 (Surface Working Card)**：輸出格式嚴格規範且 Token 數 $\le 1,500$ 之 `00_[Agent]_Surface_Working_Card.json`，作為天王會話常駐基底。

## 輸入參數規範
- `--agent-name`: 天王代號（如 `Yuki`, `Linus`, `Abacus`, `Deming`, `Kage`）
- `--max-axioms`: 提煉公理數量（預設 `10` 條）
- `--token-limit`: 表層卡 Token 上限（預設 `1500`）
- `--dry-run`: 物理演練模式，輸出抽脂切片統計與工作卡預覽

## 執行腳本
```bash
python scripts/working_card_generator.py --agent-name "Yuki" --dry-run
```
