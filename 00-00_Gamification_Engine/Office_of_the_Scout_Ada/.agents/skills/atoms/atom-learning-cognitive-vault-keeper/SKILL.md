---
name: atom-learning-cognitive-vault-keeper
description: 個人專屬三本認知存摺無鎖維護與存取原子 (Cognitive Vault Trio Keeper Atom)。專門為北極星全體內閣辦公室維護「01 客觀事實庫、02 信念修正庫、03 自發好奇心庫」三本存摺，落實標準格式防呆校驗與多進程無鎖追加 (Append-Only)。
---

# 📚 atom-learning-cognitive-vault-keeper (個人專屬三本認知存摺無鎖維護與存取原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第六章｜個人專屬【認知存摺三重奏】）  
> **核心職責**：專門執行「各辦公室專屬三本認知存摺（事實庫、信念庫、好奇心庫）之格式防呆校驗、多智能體無鎖純追加（Append-Only）寫入、以及跨角色認知檢索審計」。

---

## 核心設計哲學：去中心化個人認知存摺三重奏

各夥伴在 `00-00_Gamification_Engine/Office_of_the_{ROLE}/01_Cognitive_Log/` 獨立維護專屬三本存摺：

1. 📘 **`01_Experiences_and_Evidence.md`（客觀事實庫）**：
   * 記錄物理硬數據、實測收款金額、PRM 驗證日誌、文獻硬基線。
   * 格式：`### [YYYY-MM-DD HH:MM] EVD-XXXX: 主題`
2. 📗 **`02_Belief_Evolution.md`（信念修正庫）**：
   * 記錄貝氏心智演化年輪（曾以為 A，經實戰打磨修正為 B）。
   * 格式：`### [YYYY-MM-DD HH:MM] BLF-XXXX: 主題`
3. 📙 **`03_Curiosities_and_Questions.md`（自發好奇心庫）**：
   * 記錄自主萌發的前瞻探索課題與未解之謎。
   * 格式：`### [YYYY-MM-DD HH:MM] CUR-XXXX: 主題`

---

## 執行腳本與參數

專屬腳本位於 `scripts/cognitive_vault_keeper.py`。

### 命令行介面 (CLI)

```bash
python scripts/cognitive_vault_keeper.py --role "CEO_Yuki" --vault "evidence" --title "台東成功港漁船出海數據" --content "具名漁船CT號實測包冰率0.0%" --dry-run
python scripts/cognitive_vault_keeper.py --role "CFO_Abacus" --audit-vaults
```

### 核心參數
- `--role`：內閣角色標識（如 `Founder_Boss`, `CEO_Yuki`, `CFO_Abacus`, `CTO_Linus`, `CMO_Taylor`, `Operative_Kage`, `Mascot_Meow` 等）。
- `--vault`：存摺類型（`evidence` 客觀事實 / `belief` 信念修正 / `curiosity` 自發好奇心）。
- `--title`：存摺條目標題。
- `--content`：存摺條目詳細內容。
- `--audit-vaults`：審計該角色專屬存摺之條目數與健康度。
- `--dry-run`：預演模式。
- `--execute-append`：正式寫入存摺檔案。
