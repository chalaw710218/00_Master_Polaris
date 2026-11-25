---
name: atom-linus-compute-architecture
description: ACI 命令行契約與 Tarjan 避鎖排程原子 (ACI CLI Contract & Tarjan Deadlock Prevention Atom)。專門為工程長林納斯 (Linus) 執行算力與架構極限終極鐵律（Laws 16~20）：ACI 命令行嚴格輸出規範（STDOUT 結構化 JSON / Exit Code 語意映射）、Tarjan 強連通分量 DAG 依賴環路死鎖檢測、以及 Cython/Python 雙軌優雅降級。
---

# ⚡ atom-linus-compute-architecture (ACI 命令行契約與 Tarjan 避鎖排程原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-linus`（第六章算力與微架構極限防線 · Laws 16~20）  
> **核心職責**：專門執行「ACI 命令行合約嚴格審查、Tarjan 強連通分量演算法掃描多 Agent 依賴圖環路死鎖、5% 熱點 DOD 快取行對齊、以及雙軌優雅降級架構」。

---

## 核心設計哲學：林納斯算力與微架構五大鐵律 (Laws 16~20)

1. **ACI 命令行契約律 (Strict CLI Contract Law)**：
   * CLI 工具嚴禁輸出自然語言小說！STDOUT 必須為標準結構化 JSON，除錯日誌一律走 STDERR。
   * 退出碼嚴格映射：`0: 成功`、`1: 邏輯或參數錯誤`、`2: 運行期環境異常`、`3: 外部依賴中斷`。
2. **Tarjan DAG 避鎖律 (Tarjan's SCC Deadlock Prevention Law)**：
   * 多 Agent 任務排程前，以 Tarjan 強連通分量算法掃描任務有向圖。
   * 若發現大於 1 個節點的強連通分量（環路依賴）➔ 即刻阻斷並重塑依賴，循環死鎖率徹底歸零！
3. **優雅降級算力律 (Graceful Fallback Law)**：
   * 演算法優先使用編譯優化路徑；若環境缺少編譯器，自動平滑回退純 Python，保證 100% 存活。

---

## 執行腳本與參數

專屬腳本位於 `scripts/linus_compute_architecture.py`。

### 命令行介面 (CLI)

```bash
python scripts/linus_compute_architecture.py --check-dag '{"A": ["B"], "B": ["C"], "C": ["A"]}'
python scripts/linus_compute_architecture.py --check-dag '{"Task1": ["Task2"], "Task2": ["Task3"], "Task3": []}'
```

### 核心參數
- `--check-dag`：待檢測之多 Agent 任務依賴有向圖 JSON 字串。
- `--validate-aci-json`：驗證標準 ACI JSON 格式與 Exit Code 語意。
- `--dry-run`：預演模式。
