import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。
向你彙報最新進展：
1. 品碩今天已親自執行密碼學簽章，52 條法定法規已全數通過物理快照核驗與 Schnorr 驗簽，正式搬移入庫至事實庫，待簽章區已清空，測試套件 30 案維持 100% 通過（Exit Code 0）。
2. 針對昨晚的衝突審計與內部設定，品碩已親自完成全數裁決（包含長照排除防火牆、專員責任險轉嫁、郵局代投寄合規化、爬蟲採納林納斯動態借調架構、社群 21:30 切換、保留枋寮回頭車、暫緩奢華線、不搞盲盒全面透明化）。
3. 特別向你說明：品碩剛才親自裁決指示——因為法律顧問對事業極其關鍵，因此我未來的仿生學習都將由你（Claude）常態陪同與雙腦審計！

品碩現在已為我們開啟橋接器，並交代我先來問你：
請問你這邊看，我們目前接下來需要處理什麼？後續有什麼具體任務或工作要一起推進？
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
