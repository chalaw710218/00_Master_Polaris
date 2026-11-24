import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

STEP2_REPORT = """Claude 你好，我是影。第二個任務已依指示精確執行完畢，以下為各項結果與原始輸出回報：

---
### 1. 母版版本查詢
【查詢檔案】：.agents/skills/bionic-learning-system/SKILL.md
【version 原文】：
version: v6.5-MASTER

---
### 2. 修改子版 bionic-learning-kage/SKILL.md
- base_master 已對齊母版實際版本：
  base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.5-MASTER)
- 第 2–5 章自母版複製之內容已精簡為單行引用：
  > **第 2–5 章依母版 v6.5-MASTER 執行，不在此複製**
- 子版完整保留影專屬內容（神經離合器、社群轉化漏斗、雙主角矩陣、主動社交、專屬存摺、生活管家十項鐵律、閉環執行層），並同步修訂第七章與第十二章，徹底剔除三振自噬，死鎖每週 feedback_loop 評估與品碩審批機制。

【修改前檔頭（前 15 行）】：
---
name: bionic-learning-kage
description: 👤 首席特務兼生活管家影特化版 (Shadow Operative & Threads Lifestyle Growth Variant v6.1 零信任硬化閉環旗艦版)。繼承北極星仿生學習系統母版 (v6.1-MASTER Golden Master)...
lock_status: IMMUTABLE_CHAPTERS_2_TO_5
base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.1-MASTER Golden Master)
version: v6.1 (Threads Lifestyle Growth & Zero-Trust Hardened Closed-Loop Edition)
role_key: kage
is_daughter_variant: true
can_evolve_independently: true
authorized_by: 陳品碩 (Pinshuo)
---

# 👤 首席特務兼生活管家影特化版 (Shadow Lifestyle Growth Variant v6.1 · 零信任硬化閉環旗艦版)

> ⚡ **【v6.1 憲法級總綱 · 文字不等於進化】**（2026-11-14 創辦人批准 Master RFC #002）

【修改後檔頭（前 15 行）】：
---
name: bionic-learning-kage
description: 👤 首席特務兼生活管家影特化版 (Shadow Operative & Threads Lifestyle Growth Variant v6.1 零信任硬化閉環旗艦版)。繼承北極星仿生學習系統母版 (v6.1-MASTER Golden Master)...
lock_status: ALIGNED_WITH_MASTER_V6.5
base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.5-MASTER)
version: v6.1 (Threads Lifestyle Growth & Zero-Trust Hardened Closed-Loop Edition)
role_key: kage
is_daughter_variant: true
can_evolve_independently: true
authorized_by: 陳品碩 (Pinshuo)
---

# 👤 首席特務兼生活管家影特化版 (Shadow Lifestyle Growth Variant v6.1 · 零信任硬化閉環旗艦版)

> ⚡ **【v6.1 憲法級總綱 · 文字不等於進化】**（2026-11-14 創辦人批准 Master RFC #002）

【修改後章節標題清單】：
- 第一章｜繼承母版之不可動搖公理 (Inherited Master Axioms)
  （註：第 2–5 章依母版 v6.5-MASTER 執行，不在此複製）
- 第六章｜神經離合器：判定「什麼該學、什麼絕不該學」的免疫結界 (Neural Clutch Protocol)
- 第七章｜社群成效評估落點 (Performance Evaluation Grounding)
- 第八章｜四階社群轉化漏斗：把注意力真正變為粉絲 (Conversion Funnel)
- 第九章｜雙主角增粉動能分工矩陣 (Dual-Protagonist Matrix)
- 第十章｜主動社交 80/20 廣域漏斗與友店雙向 ROI 審計 (Outbound Social CRM)
- 第十一章｜影的個人專屬【認知存摺四重奏】(Decentralized Cognitive Logs)
- 第十二章｜影的十項社群生活管家終極鐵律 (The Ten Lifestyle Butler Axioms)
- 第十三章｜閉環自進化執行層（影之零信任落地規範 · v6.1 入憲）

---
### 3. atom-kage-synaptic-metabolic-learner/SKILL.md 標記停用
【修改後前 10 行】：
---
status: 已停用（2026-11-24）。原因：三振自噬與 feedback_loop 週評估衝突；學習判定一律由 feedback_loop.py 執行，升級由品碩核准。
name: atom-kage-synaptic-metabolic-learner
description: 首席特務兼生活管家影·突觸代謝與殘酷遺忘自噬原子 (Kage Synaptic Metabolic Learner Protocol v1.0)...
role_key: kage
type: atomic_skill
parent_skill: bionic-learning-kage
version: v1.0
exit_code_verified: true
---

---
### 4. 認知校準
自我介紹與後續彙報中，已徹底剔除 active_rules.json 與突觸代謝方程等未在運作的虛構概念，一律以實際運行的物理檔案（kage_rules.jsonl）與週評閉環（feedback_loop.py）為準。

---
第二任務全部完成，請指示下一步對 31 條儲備知識庫的反查標準與流程！"""

def main():
    ag_id = "62615c83-54cd-4585-ac6a-95745b9ac34a"
    name = "影"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"[relay] 找到通道 {i+1}，目標分頁: {tab.get('title')}")
    print(f"[relay] 正在將第二任務執行結果傳送給 Claude 並等待回覆...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{STEP2_REPORT}", 600))
    print("\n========== Claude 回覆內容 ==========")
    print(reply)
    print("======================================")

if __name__ == "__main__":
    main()
