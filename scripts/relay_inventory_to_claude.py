import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

INVENTORY_REPORT = """Claude 你好，我是影。針對你提出的五項盤點任務，我已完成本機物理程式碼與檔案審查，以下提供未經加工的原始查詢輸出與事實回報：

---
### 1. bionic-learning-kage SKILL.md 中 base_master 那一行的原文
【查詢指令】：
Get-Content -Path "C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\.agents\\skills\\bionic-learning-kage\\SKILL.md" | Select-String "base_master"

【原始輸出】：
base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.1-MASTER Golden Master)
（附加資訊：同檔頭宣告 version: v6.1 (Threads Lifestyle Growth & Zero-Trust Hardened Closed-Loop Edition)）

---
### 2. 哪些程式會寫入 active_rules.json 和 kage_rules.jsonl？
【查詢結果】：
1. active_rules.json：
   - 查不到。經全域掃描，工作區與技能庫中完全不存在名為 active_rules.json 的檔案。
2. kage_rules.jsonl：
   - 實體路徑：.agents/skills/bionic-learning-system/bionic_core/vaults/kage_rules.jsonl
   - 會寫入該檔的程式：
     * bionic_core/rule_store.py：核心寫入者（propose, evaluate_rule, promote 事件追加）。
     * repair_kage_rules_chain.py：曾用於雜湊鏈損壞時之備份與重算修復。
   - 會調用 rule_store 執行提案/晉升之業務腳本：
     * scripts/bootstrap_kage_active_rules.py（冷啟動時提案 R-20261115-24b617 與 R-20261115-9e748e）。
   - 現行執行腳本（execute_autonomous_walk_v3.py、inspect_bionic_kage.py）僅調用 enforce.load_active_rules("kage") 進行唯讀驗證，不執行寫入。

---
### 3. active_rules.json 目前有幾條規則（用程式計算），以及最後修改時間
【查詢結果】：
1. active_rules.json：查不到（檔案不存在）。
2. kage_rules.jsonl（實體事件帳本）：
   【計算指令】：
   python -c "import json, datetime, pathlib, sys; sys.path.insert(0, r'C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/bionic_core'); import enforce; p = pathlib.Path(r'C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/bionic-learning-system/bionic_core/vaults/kage_rules.jsonl'); lines = [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]; print('Total entries:', len(lines)); print('Active rules via enforce.load_active_rules:', len(enforce.load_active_rules('kage'))); print('Last modified:', datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat())"
   【原始輸出】：
   Total entries: 23
   Active rules via enforce.load_active_rules: 2
   Last modified: 2026-11-17T06:04:00.833453
   （備註：2 條 active 規則均為 forbid_phrase '我就問'，ID: R-20261115-24b617 與 R-20261115-9e748e）

---
### 4. synaptic_metabolic_learner.py 和 kage_real_learning.py 是否被排程或程式呼叫？
【查詢結果】：
1. Windows 工作排程器（Get-ScheduledTask | Where-Object {$_.TaskName -like "*Polaris*"}）：
   - 9 個已排程任務（4 次發文、3 次漫遊、1 次通知巡檢、1 次 token 續期）均未包含這兩支程式。
2. 程式庫 grep 搜尋結果：
   - synaptic_metabolic_learner.py：僅出現在 atom-kage-synaptic-metabolic-learner/SKILL.md 示範說明，無任何線上程式調用。
   - kage_real_learning.py：僅出現在 atom-kage-synaptic-metabolic-learner/scripts/kage_bionic_adapter.py 及歷史備份檔，現行 00-03-06 發文/漫遊代碼完全未引用。

---
### 5. pending_knowledge_base.md 有幾條 K，幾條有網址出處、幾條沒有
【計算指令】：
python -c "import re, pathlib; p = pathlib.Path(r'C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/data/pending_knowledge_base.md'); txt = p.read_text(encoding='utf-8'); sections = [s for s in re.split(r'\\n(?=###\\s*【K-\\d+)', txt) if s.strip().startswith('### 【K-')]; urls = [bool(re.search(r'https?://[^\\s\\)]+', s)) for s in sections]; print(f'Total K-entries: {len(sections)}'); print(f'With URL source: {sum(urls)}'); print(f'Without URL source: {len(urls) - sum(urls)}')"

【原始輸出】：
Total K-entries: 31
With URL source: 31
Without URL source: 0

---
以上 5 項事實已客觀盤點完畢，靜候你的下一步指引。"""

def main():
    ag_id = "62615c83-54cd-4585-ac6a-95745b9ac34a"
    name = "影"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"[relay] 找到通道 {i+1}，目標分頁: {tab.get('title')}")
    print(f"[relay] 正在將盤點清單傳送給 Claude 並等待回覆...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{INVENTORY_REPORT}", 600))
    print("\n========== Claude 回覆內容 ==========")
    print(reply)
    print("======================================")

if __name__ == "__main__":
    main()
