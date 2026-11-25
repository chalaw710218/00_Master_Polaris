---
name: atom-evolution-knowledge-pruner
description: 仿生探索與死知識殘酷自噬修剪原子 (Bionic Knowledge Exploration & Autophagic Pruning Atom)。專職負責外部資訊探索、第一原則拆解、與過期假設/虛胖死知識的殘酷溶酶體自噬修剪，確保系統只保留經物理驗證之有效認知。
---

# 🧬 atom-evolution-knowledge-pruner (仿生探索與死知識殘酷自噬修剪原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-self-evolution`  
> **核心職責**：專門執行「外部環境探索、事實採礦、以及對過期假設、未經驗證死知識、虛胖文本的殘酷溶酶體自噬修剪（Autophagic Pruning）」。

---

## 核心設計哲學：大隅良典細胞自噬與第一原則

1. **自進化不是累積死知識**：死知識堆疊只會造成上下文膨脹、注意力稀釋與推論遲鈍。真正的自進化是動態代謝負熵。
2. **溶酶體殘酷修剪機制**：
   * 凡未經 Exit Code 0 驗證的猜想 ➔ 標記為待檢。
   * 凡過期或已被新公理覆蓋的舊條目 ➔ 殘酷自噬清除或移至墓碑區（Tombstone）。
   * 凡含有 AI 腔、套話、或未接地氣之虛詞 ➔ 立即物理剃除。

---

## 執行腳本與參數

專屬腳本位於 `scripts/knowledge_pruner.py`。

### 命令行介面 (CLI)

```bash
python scripts/knowledge_pruner.py --target-dir "00-00_Gamification_Engine" --dry-run
python scripts/knowledge_pruner.py --file-path "00-00_System_Operations_Log.md" --dead-axiom-pattern "已淘汰" --execute-prune
```

### 核心參數
- `--target-dir`：欲掃描與修剪之目標資料夾。
- `--file-path`：特定待修剪目標檔案路徑。
- `--dead-axiom-pattern`：死知識特徵正則或關鍵字。
- `--dry-run`：預演模式，輸出修剪診斷報告與建議，不覆寫實體檔案。
- `--execute-prune`：實體修剪模式，自動執行溶酶體自噬與負熵精簡。
