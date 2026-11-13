---
name: atom-learning-prm-step-verifier
description: PRM 過程級逐步驗證與物理終點法官原子 (Process-Supervised Reward Verifier & Ground-Truth Gate Atom)。專門在推論過程中對每一步邏輯中繼步驟進行獨立打分 (Positive/Negative)，徹底消滅中間邏輯跳躍與獎勵投機 (Reward Hacking)，並執行 Exit Code 0 終點物理驗證。
---

# 🔒 atom-learning-prm-step-verifier (PRM 過程級逐步驗證與物理終點法官原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第二章｜外部物理驗證器與 PRM 過程級逐步驗證）  
> **核心職責**：專門執行「推論過程步步打分（PRM）、邏輯跳躍與未接地假設攔截、以及三相物理終點法官檢驗（Exit Code 0、商業數據真實對齊、憲法紅隊零違規）」。

---

## 核心設計哲學：DeepMind ICLR 2024 & OpenAI PRM

1. **嚴禁獎勵投機 (Reward Hacking)**：
   * 拒絕僅依賴最終結果的粗糙獎勵（Outcome Reward Model）。
   * 在 `<thought>` 內部，對「步驟 1: 數據讀取與成本拆解 ➔ 步驟 2: 扣除耗損與運費計算 ➔ 步驟 3: 毛利定價與話術推演」的每一個中繼步驟獨立打分。
   * 任一步驟出錯立即原地回滾修正，杜絕「中間胡說八道、碰巧猜對答案」。
2. **終點三相物理法官**：
   * **法官 1 (代碼物理驗證器)**：Python 運行環境實測，退出碼必須等於 0 (`Exit Code == 0`)。
   * **法官 2 (商業流水天平)**：比對真實歷史帳本或物理稱重數據，嚴禁憑空捏造數字。
   * **法官 3 (憲法紅隊閘門)**：商道道德、品牌法定名稱零洩漏防火牆 100% 通過。

---

## 執行腳本與參數

專屬腳本位於 `scripts/prm_step_verifier.py`。

### 命令行介面 (CLI)

```bash
python scripts/prm_step_verifier.py --steps-file "sample_steps.json" --verify-code "scripts/sample.py"
python scripts/prm_step_verifier.py --reasoning-text "步驟1: 讀取成本... 步驟2: 計算耗損..." --dry-run
```

### 核心參數
- `--steps-file`：包含推論步驟清單之 JSON 檔案。
- `--reasoning-text`：推論過程純文字。
- `--verify-code`：待執行的伴隨 Python 腳本，實測是否能跑出 Exit Code 0。
- `--dry-run`：預演模式，輸出 PRM 步步打分診斷報告。
