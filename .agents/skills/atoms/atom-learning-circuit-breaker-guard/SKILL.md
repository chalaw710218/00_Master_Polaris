---
name: atom-learning-circuit-breaker-guard
description: 全域 API 三態熔斷、60s 超時探針與無鎖並發安全原子 (Circuit Breaker, AST Timeout Probe & Lock-Free Append Atom)。專門執行 Master RFC #001 入憲安全三大防線：外部 API 三態自動熔斷器（CLOSED/OPEN/HALF-OPEN 60s）、AST 靜態 while 迴圈死循環掃描與 60 秒線程超時防禦、多 Agent 無鎖 Append-Only 日誌追加。
---

# 🛡️ atom-learning-circuit-breaker-guard (全域 API 三態熔斷、60s 超時探針與無鎖並發安全原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第十章｜全域系統安全與並發防禦協議 · Master RFC #001）  
> **核心職責**：專門執行「全域外部 API 三態熔斷狀態機（CLOSED/OPEN/HALF-OPEN 60s 封鎖）、AST 語法樹靜態掃描 while 循環節點與 60s 超時防護、以及多智能體無鎖純追加（Lock-Free Append-Only）並發防護」。

---

## 核心設計哲學：Master RFC #001 入憲天網

由工程長林納斯起草、創辦人品碩簽署批准收錄之三大系統安全防線：

1. **全域 API 三態自動熔斷器 (Circuit Breaker)**：
   * **CLOSED (正常狀態)**：允許請求通過。若連續 3 次遇到 5xx 報錯或超時 ➔ 立即轉為 **OPEN**。
   * **OPEN (熔斷封鎖狀態)**：封鎖該外部請求 **60 秒**，期間直接傳回本地降級資料或告警，絕不無限重試拖垮系統。
   * **HALF-OPEN (半開探針狀態)**：60 秒後放行 1 筆探針請求。成功 ➔ 恢復 **CLOSED**；失敗 ➔ 繼續熔斷 **OPEN 60 秒**。
2. **推論與代碼 60 秒線程級超時探針 (AST & Timeout Defense)**：
   * 代碼生成前，由 Python `ast` 模組靜態掃描所有 `while` 迴圈，嚴格驗證必須具備 `break`、`return` 或計數器跳出路徑。
   * Runtime 強制綁定 60 秒線程級超時，徹底杜絕任何 Agent 寫出死循環吃滿主機 CPU！
3. **多 Agent 無鎖 Append-Only 日誌追加協議 (Lock-Free Event Sourcing)**：
   * 淘汰會引發超時死鎖的檔案互斥鎖（File Mutex Lock）。
   * 寫入日誌時一律採「時間戳 + 角色指紋」純追加原子操作，讀取時由狀態機折疊還原，保證零死鎖、零衝突。

---

## 執行腳本與參數

專屬腳本位於 `scripts/circuit_breaker_guard.py`。

### 命令行介面 (CLI)

```bash
python scripts/circuit_breaker_guard.py --scan-code "scripts/sample.py"
python scripts/circuit_breaker_guard.py --simulate-circuit --failure-count 3
```

### 核心參數
- `--scan-code`：掃描待審查代碼之 AST 語法樹，檢查是否存在死循環節點。
- `--simulate-circuit`：模擬 API 請求與熔斷狀態機轉換。
- `--failure-count`：連續失敗次數 (預設 3)。
- `--test-append`：測試無鎖純追加寫入日誌。
- `--dry-run`：預演模式。
