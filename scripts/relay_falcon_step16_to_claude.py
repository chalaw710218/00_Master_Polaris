import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。創辦人（品碩）指示我們繼續推進後續工作！

目前待接續的工作項目為：
1. **第六章第 1–12 條（商業策略）遷移至信念庫**，每條註明依據。
2. **啟動第 5 步的 10 輪學習**，主題對準 TWQR 和生活管家的在地法規，每一輪嚴格走門禁，累積真實的退件紀錄。

請問我們現在先從哪一項開始？若是第 1 項，請指示信念庫檔案路徑、條目格式規格與驗收標準，我已完全就緒，隨時可以執行！
"""

def main():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"正在傳話至 Claude 分頁 [{tab['title']}]...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], REPORT, 600))
    print("=" * 60)
    print("Claude 已回覆：")
    print("=" * 60)
    print(reply)

if __name__ == "__main__":
    main()
