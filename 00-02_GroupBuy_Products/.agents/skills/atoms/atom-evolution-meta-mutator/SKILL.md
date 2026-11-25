---
name: atom-evolution-meta-mutator
description: 遞歸架構自我重寫與基因突變發布原子 (Recursive Meta-Evolution & Architecture Mutation Atom)。專門依據客觀驗證真值，執行技能規範與心智大綱的遞歸自我重寫、基因突變升版、白皮書發布與自對弈驗證 (SPIN)。
---

# 🧬 atom-evolution-meta-mutator (遞歸架構自我重寫與基因突變發布原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-self-evolution`  
> **核心職責**：專門執行「遞歸自我重寫（Meta-Evolution）、架構基因突變、世代升版（Generation N ➔ N+1）與白皮書頒布驗收」。

---

## 核心設計哲學：複雜適應系統 (CAS) 與遞歸重寫

1. **不可變真理公理**：在自重寫過程中，底層核心公理（如創辦人主權、台灣繁體中文、物理真值）具備永久鋼印，任何突變不得篡改。
2. **安全沙盒突變**：
   * 突變前後必須通過語意與代碼語法檢查（Exit Code 0）。
   * 自動比對新舊版本突變差量（Mutation Diff），生成世代進程說明。
   * 自動維護白皮書與世代白皮書歷史記錄。

---

## 執行腳本與參數

專屬腳本位於 `scripts/meta_mutator.py`。

### 命令行介面 (CLI)

```bash
python scripts/meta_mutator.py --target-skill "bionic-self-evolution" --dry-run
python scripts/meta_mutator.py --target-skill "bionic-self-evolution" --new-generation "171" --new-feature "高階感官食療微影音" --execute-mutate
```

### 核心參數
- `--target-skill`：欲突變自我重寫之目標技能名稱。
- `--new-generation`：突變後的新世代編號（如 171）。
- `--new-feature`：本輪突變之核心演化特性或主題描述。
- `--dry-run`：預演模式，計算突變前後版本差量與白皮書草案。
- `--execute-mutate`：正式寫入突變版本並更新技能文件。
