import asyncio
import sys
from pathlib import Path

# Set UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT_TEXT = """========================================
總信念數: 135
找得到對應: 7 條
  - 對應到已驗證: 3 條
  - 對應到對不上: 4 條
  - 對應到內部證據: 0 條
找不到對應: 128 條
========================================
csv 路徑: C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\00-00_Gamification_Engine\\Office_of_the_CEO_Yuki\\01_Cognitive_Log\\_belief_match_proposal.csv"""

def main():
    ag_id = "44896662-b7c0-4aaa-9282-f12cda292979"
    name = "雪"
    i, p = claude_relay.find_pair(ag_id)
    if not p.get("enabled"):
        claude_relay.fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = claude_relay.find_tab(p["claude_href"])
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【{name}】{REPORT_TEXT}", 600))
    print("Claude 已回覆：" + str(reply))

if __name__ == "__main__":
    main()
