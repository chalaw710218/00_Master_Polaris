import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

STEP3_REPORT = """Claude 你好，我是影。第三個任務已依指示修改完畢，以下為各修改項目的原文與查核結果回報：

---
### 1. 檔頭前 15 行原文（版本全面對齊 v6.5）
```markdown
---
name: bionic-learning-kage
description: 👤 首席特務兼生活管家影特化版 (Shadow Operative & Threads Lifestyle Growth Variant v6.5 零信任硬化閉環旗艦版)。繼承北極星仿生學習系統母版 (v6.5-MASTER Golden Master)，融合創辦人（品碩）親傳之「神經離合器雜訊過濾力學」、「四階社群轉化漏斗」、「雙主角人設增粉矩陣」，並全面接入 Master RFC #002 零信任硬化執行層（Threads 官方真實數據真值驗算、SHA-256 防刷輪次、Phase 0 先讀後寫強制閘門、第四本機器可讀規則庫與滿十輪停機審計三段落硬檢）。
lock_status: ALIGNED_WITH_MASTER_V6.5
base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.5-MASTER)
version: v6.5-kage
role_key: kage
is_daughter_variant: true
can_evolve_independently: true
authorized_by: 陳品碩 (Pinshuo)
---

# 👤 首席特務兼生活管家影特化版 (Shadow Lifestyle Growth Variant v6.5 · 零信任硬化閉環旗艦版)

> ⚡ **【v6.5 憲法級總綱 · 文字不等於進化】**（2026-11-14 創辦人批准 Master RFC #002）  
```
（註：開頭原先宣稱第 2–5 章永久 IMMUTABLE 鎖定之文字已刪除，替換為單行：`> **第 2–5 章依母版 v6.5-MASTER 執行。**`）

---
### 2. 第一章第 4 條與第十二章第 9 條（學習輪次只算學習）
【第一章第 4 條】：
```markdown
4. **創辦人親定鐵律｜每 10 輪強制執行衝突大審計 (Decadal Conflict Checkpoint)**：每滿 10 輪「學習」強制審計。發文和逛逛不計入學習輪次，不寫入 kage_cycles.jsonl。
```

【第十二章第 9 條】：
```markdown
9. **十輪大審計律**：每滿 10 輪「學習」強制審計。發文和逛逛不計入學習輪次，不寫入 kage_cycles.jsonl。
```

【發文與逛逛程式 grep cycle_ledger 結果】：
經精確搜尋排程調用之發文/逛逛程式庫：
- `execute_autonomous_walk_v3.py`（排程核心發文與漫遊主腳本）：**0 matches（完全未呼叫 cycle_ledger）**
- `interaction_safety_gate.py`：**0 matches**
- `calculate_weekly_relationship_metrics.py`：**0 matches**
- `feedback_loop.py`：**0 matches**
- `post_walk_reflector.py`（漫遊後自省）：
  * Line 10: 註釋說明
  * Line 40: `CYCLE_LEDGER_PATH = ...`（常數定義）
  * Line 226: 程式碼中顯式標記註解：`# - 仿生學習輪次維持暫停（不調用 cycle_ledger.tick 推進輪次，不新增 K）。`
  （結論：實際運行之發文與逛逛流程均未調用 `cycle_ledger.py tick`）

---
### 3. 第十章原文（對齊 threads-autonomous-walker）
```markdown
## 🤝 第十章｜主動社交 80/20 廣域漏斗與友店雙向 ROI 審計 (Outbound Social CRM)

依 `threads-autonomous-walker` 技能執行：拜訪的友店全部按愛心，至少一半留走心留言；每日上限留言 15、愛心 60。
```

---
### 4. 第十三章 SOP 第 2 條與流程圖原文
【流程圖第 ⑦ 步】：
```mermaid
flowchart LR
    T["① 漫遊定時器 / 排程觸發"] --> P["② 受控上網感知 (arXiv CS.CL)"]
    P --> V["③ 後台真值驗算 (insights_history.jsonl)"]
    V --> D["④ 規則蒸餾入庫 (kage_rules.jsonl)"]
    D --> E["⑤ 發文前強制閘門 (enforce.py gate)"]
    E --> M["⑥ 貼文發布後 24h 遙測 (A/B 效果)"]
    M --> R["⑦ 提案給品碩核准"]
    R -.附唯一 SHA-256 憑證.-> C["⑧ cycle_ledger.py tick 入帳"]
```

【SOP 第 2 條】：
```markdown
2. **零信任真值驗算與轉正**：
   * `rule_store.py evaluate` 只產出建議，不自動轉正。規則轉正需 `feedback_loop.py` 至少 6 篇樣本支持，並由品碩回『收』。
```

---
以上四處衝突已徹底消除對齊，請審閱並指示反查 31 條儲備知識庫之具體步驟！"""

def main():
    ag_id = "62615c83-54cd-4585-ac6a-95745b9ac34a"
    name = "影"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"[relay] 找到通道 {i+1}，目標分頁: {tab.get('title')}")
    print(f"[relay] 正在將第三任務執行結果傳送給 Claude 並等待回覆...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{STEP3_REPORT}", 600))
    print("\n========== Claude 回覆內容 ==========")
    print(reply)
    print("======================================")

if __name__ == "__main__":
    main()
