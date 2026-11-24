import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """Claude 你好，我是雪柔。

我已按照你的指示完成「按被引用條號逐條拆解」與「全量快照落地」：

1. **改寫 `falcon_recheck_13_24.json`**：
   - 擴充至第六章第 13–24 條所提及的所有法定條號（含罰則與關聯條文：觀光條例 §55、公平法 §42、建築法 §95-1、動保法 §22、公寓條例 §53、長照法 §3、民法 §224、仲裁法 §15、電簽法 §5、廢清法 §41、§46 等）。
   - 每筆包含 `rule_no, law, article, url, quote, label`，總筆數由程式計算為 26 筆。
2. **網頁快照原封不動落地**：
   - 抓取每一頁時，皆同步以 `snapshots/<law>_<article>.txt` 格式原封不動儲存於磁碟，供你隨時查核抽驗。
   - 磁碟快照路徑：`C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\scripts\\snapshots`
3. **逐字原文校準**：
   - 針對抽查發現的差異重新取樣：廢清法 §46 原文「一年以上七年以下」、動保法 §22 原文「依法領得營業證照」、觀光條例 §55 原文「處新臺幣十萬元以上二百萬元以下罰鍰」（現行法為 10 萬~200 萬，含旅館業務）。
   - 經 `recheck_quotes.py` 呼叫 `bionic_core/evidence_gate.py` 之 `quote_in_page`，26 筆摘句全部為 **PASS**。

---
### 統計結果回報

- **總查核筆數**：26 筆（由程式即時動態計算）
- **snapshots 資料夾路徑**：`C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\scripts\\snapshots`

執行結果最後 15 行：
```
第22條 | 發展觀光條例 第55條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0110001&flno=55 | PASS
第23條 | 公司法 第356-1條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0080001&flno=356-1 | PASS
第23條 | 公司法 第356-7條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0080001&flno=356-7 | PASS
第24條 | 民法 第224條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=B0000001&flno=224 | PASS
第24條 | 仲裁法 第1條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0020001&flno=1 | PASS
第24條 | 仲裁法 第15條 | https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0020001&flno=15 | PASS

============================================================
recheck_quotes.py 程式執行統計結果
============================================================
總查核筆數 (被引用條號): 26 筆
摘句驗證 PASS (真實出現在網頁): 26 筆
摘句驗證 FAIL (網頁找不到摘句): 0 筆
網頁抓取 FETCH_ERROR: 0 筆
------------------------------------------------------------
法條比對標記 【已驗證】: 20 筆
法條比對標記 【對不上】: 6 筆
法條比對標記 【未驗證】: 0 筆
快照存檔目錄: C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\scripts\\snapshots
============================================================
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
