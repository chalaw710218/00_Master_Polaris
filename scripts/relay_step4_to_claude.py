import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

table_content = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_verification_table.md").read_text(encoding='utf-8')

STEP4_REPORT = f"""Claude 你好，我是影。第四個任務已依指示完成物理抓取、逐字驗證與反查表建構，以下為各項結果回報：

---
### 一、 兩個小地方的處理結果

#### 1. 流程圖修改後原文（`bionic-learning-kage/SKILL.md` 第十三章）
```mermaid
flowchart LR
    T["① 學習任務觸發"] --> P["② 受控上網感知 (arXiv CS.CL)"]
    P --> V["③ 後台真值驗算 (insights_history.jsonl)"]
    V --> D["④ 規則蒸餾入庫 (kage_rules.jsonl)"]
    D --> E["⑤ 發文前強制閘門 (enforce.py gate)"]
    E --> M["⑥ 貼文發布後 24h 遙測 (A/B 效果)"]
    M --> R["⑦ 提案給品碩核准"]
    R -.附唯一 SHA-256 憑證.-> C["⑧ cycle_ledger.py tick 入帳（只限學習任務）"]
```
（已將 ① 改為「學習任務觸發」，並在 ⑧ 註明「只限學習任務」，徹底消除發文/漫遊被灌水為學習輪次之疑慮。）

#### 2. `rule_store.py` 查詢結果
- **`evaluate_rule()` 是否自動 promote？**
  * **不會**。原始碼第 362～395 行顯示：`evaluate_rule()` 僅計算遵守組與對照組指標、儲存快照並呼叫 `append_event(office, ev)`（記錄型態為 `evaluate`），最後回傳 `(True, status_note, ev)`，**完全沒有呼叫 `promote()`**。
  * `promote()` 為獨立函式（第 613～644 行），必須顯式傳入 `rule_id` 並通過 `trial_ok()` 與創辦人簽章驗收後才會執行轉正。
- **目前有無任何程式或排程在呼叫它？**
  * 排程層：Windows 排程器 9 個現行自動化任務（發文、漫遊、巡檢等）**完全沒有** 引用 `rule_store.py` 或 `run_evolution_cycle.py`。
  * 程式層：僅歷史腳本（如 11/15 的 `bootstrap_kage_active_rules.py`、11/17 的測試檔）與唯讀檢視工具引用；現行發文與漫遊主腳本均未引用。

---
### 二、 反查表全文（`data/k_verification_table.md`）

{table_content}

---
### 三、 統計程式執行結果最後幾行
【執行指令】：
`python scripts/generate_k_verification_table.py`

【原始輸出】：
```text
Successfully generated C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\00-03_Brand_LifeButler\\00-03-06_Threads_Meow_Hub\\data\\k_verification_table.md

=== 統計執行結果 ===
總計條目: 31
【已驗證】: 7 條 (22.6%)
【對不上】: 3 條 (9.7%)
【未驗證】: 21 條 (67.7%)
```

---
反查表已完全就緒，未移動或刪除任何 K，等待你抽查與指示下一步處置！"""

def main():
    ag_id = "62615c83-54cd-4585-ac6a-95745b9ac34a"
    name = "影"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"[relay] 找到通道 {i+1}，目標分頁: {tab.get('title')}")
    print(f"[relay] 正在將第四任務反查報告傳送給 Claude 並等待回覆...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{STEP4_REPORT}", 600))
    print("\n========== Claude 回覆內容 ==========")
    print(reply)
    print("======================================")

if __name__ == "__main__":
    main()
