import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """Claude 你好，我是雪柔。

我已完成以下各項任務：
1. 建立 `falcon_recheck_13_24.json`，收錄 12 條完整資料（含 `rule_no`, `url`, `quote`, `label`）。
2. 特別重查第 20 條現行《電子簽章法》第 4 條，從網頁逐字摘取現行條文：「電子文件及電子簽章，符合本法規定者，在功能上等同於實體文件及簽章，不得僅因其電子形式而否認其法律效力。」（標記維持【已驗證】，因確實規範功能等同原則）。
3. 修正第 17 條（動保法第 25-2 條原文為「停止營業」非「停業」）、第 18 條（電業法 pcode 為 J0030011，原文為「電器承裝業」非「電器承裝業者」）、第 21 條（室裝辦法第 3 條原文含除外文字）。
4. 編寫 `recheck_quotes.py`，調用母版 `bionic_core/evidence_gate.py` 的 `fetch_page_text` 與 `quote_in_page(quote, page_text)`，統計數字全由程式即時動態計算。

以下為 `recheck_quotes.py` 完整程式碼：

```python
\"\"\"
recheck_quotes.py — 驗證第六章第 13–24 條逐字摘句是否真實出現在官方網頁
呼叫母版 bionic_core/evidence_gate.py 之 fetch_page_text 與 quote_in_page
\"\"\"

import json
import sys
from pathlib import Path

# 強制 UTF-8 輸出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
BIONIC_CORE = HERE.parent / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(BIONIC_CORE))

from evidence_gate import fetch_page_text, quote_in_page

JSON_PATH = HERE / "falcon_recheck_13_24.json"


def main():
    if not JSON_PATH.exists():
        print(f"錯誤：找不到 {JSON_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    results = []
    counts_verify = {"PASS": 0, "FAIL": 0, "FETCH_ERROR": 0}
    counts_label = {"【已驗證】": 0, "【對不上】": 0, "【未驗證】": 0}

    for item in records:
        r_no = item.get("rule_no", "")
        url = item.get("url", "")
        quote = item.get("quote", "")
        label = item.get("label", "【未驗證】")

        counts_label[label] = counts_label.get(label, 0) + 1

        try:
            page_text = fetch_page_text(url, timeout=20)
        except Exception as e:
            status = "FETCH_ERROR"
            counts_verify["FETCH_ERROR"] += 1
            print(f"{r_no} | {url} | FETCH_ERROR")
            results.append((r_no, url, status, label, str(e)))
            continue

        ok, msg = quote_in_page(quote, page_text)
        if ok:
            status = "PASS"
            counts_verify["PASS"] += 1
            print(f"{r_no} | {url} | PASS")
        else:
            status = "FAIL"
            counts_verify["FAIL"] += 1
            print(f"{r_no} | {url} | FAIL")

        results.append((r_no, url, status, label, msg))

    total = len(records)
    print("\\n" + "=" * 50)
    print("recheck_quotes.py 程式執行統計結果")
    print("=" * 50)
    print(f"總查核筆數: {total} 筆")
    print(f"摘句驗證 PASS (出現在網頁): {counts_verify['PASS']} 筆")
    print(f"摘句驗證 FAIL (找不到摘句): {counts_verify['FAIL']} 筆")
    print(f"網頁抓取 FETCH_ERROR: {counts_verify['FETCH_ERROR']} 筆")
    print("-" * 50)
    print(f"法條比對標記 【已驗證】: {counts_label['【已驗證】']} 條")
    print(f"法條比對標記 【對不上】: {counts_label['【對不上】']} 條")
    print(f"法條比對標記 【未驗證】: {counts_label['【未驗證】']} 條")
    print("=" * 50)


if __name__ == "__main__":
    main()
```

---
### 執行結果最後 15 行

```
第22條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0110001&flno=27 | PASS
第23條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0080001&flno=356-1 | PASS
第24條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0020001&flno=1 | PASS

==================================================
recheck_quotes.py 程式執行統計結果
==================================================
總查核筆數: 12 筆
摘句驗證 PASS (出現在網頁): 12 筆
摘句驗證 FAIL (找不到摘句): 0 筆
網頁抓取 FETCH_ERROR: 0 筆
--------------------------------------------------
法條比對標記 【已驗證】: 6 條
法條比對標記 【對不上】: 6 條
法條比對標記 【未驗證】: 0 條
==================================================
```
"""

def main():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"正在傳話至 Claude 分頁 [{tab['title']}]...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], f"【雪柔】{REPORT}", 600))
    print("Claude 已回覆：\n" + reply)

if __name__ == "__main__":
    main()
