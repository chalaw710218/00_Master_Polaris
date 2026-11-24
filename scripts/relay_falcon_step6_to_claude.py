import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

# 讀取 chapter6_13_24_revised.md 全文
revised_content = (HERE / "chapter6_13_24_revised.md").read_text(encoding="utf-8")

REPORT = f"""【雪柔】
Claude 你好，我是雪柔。已依照改寫原則與格式規範完成任務，彙報如下：

============================================================
一、 第 1 項清單程式輸出（falcon_recheck_13_24.json 中 label=【對不上】之筆數）
============================================================
執行 `python scripts/list_mismatches.py` 程式輸出如下：
```
TOTAL_MISMATCHES: 6
rule_no: 第13條 | law: 一般廢棄物回收清除處理辦法 | article: 第2條
rule_no: 第14條 | law: 公寓大廈管理條例 | article: 第3條
rule_no: 第14條 | law: 公寓大廈管理條例 | article: 第53條
rule_no: 第19條 | law: 公平交易法 | article: 第21條
rule_no: 第21條 | law: 建築法 | article: 第77-2條
rule_no: 第24條 | law: 仲裁法 | article: 第1條
```

============================================================
二、 chapter6_13_24_revised.md 全文
============================================================
（依改寫原則：條文無之詞標示為我方推論、補齊真正罰則條號、刪除地院秘密仲裁與無依據之六個月、數字完整保留）

```markdown
{revised_content}
```

============================================================
三、 check_ch6.py 執行結果最後 5 行與 Exit Code
============================================================
`check_ch6.py` 對 `chapter6_13_24_revised.md` 內全部 26 組「出處網址 + 原文」逐條調用 `quote_in_page` 比對 `snapshots/` 快照：

執行結果最後 5 行：
```
總檢驗條目數: 26 組
檢驗通過 (PASS): 26 組
檢驗失敗 (FAIL): 0 組
通過率: 100.0%
======================================================================

[結論] 全部 100% 通過快照逐字檢驗，Exit Code 0
```
- **Exit Code**: 0

全量 26 組法規出處與逐字原文全部嚴格對齊實體快照，請 Claude 檢閱！
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
