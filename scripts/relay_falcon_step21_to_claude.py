import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。第 1 輪學習（藥事法：代領、配送處方藥的限制）已執行完畢，結果回報如下：

### 1. before / after 待簽章區條目數
- **before**: 29
- **after**: 32
- **差額**: 32 - 29 = 3（精確等於 add 成功次數 3 次）

---

### 2. 每次 add 的執行結果

1. **第 1 次 add【成功】**
   - 標題：藥事法 第50條 處方藥品非經處方不得調劑供應
   - 出處：藥事法 第50條
   - 網址：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0030001&flno=50
   - 摘句：「須由醫師處方之藥品，非經醫師處方，不得調劑供應。」
   - 結果：`✅ [ADD_SUCCESS] 成功寫入待簽章區`

2. **第 2 次 add【成功】**
   - 標題：藥師法 第15條 藥品調劑與藥事照護專屬藥師
   - 出處：藥師法 第15條
   - 網址：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0030066&flno=15
   - 摘句：「藥師業務如下：  一、藥品販賣或管理。  二、藥品調劑。」
   - 結果：`✅ [ADD_SUCCESS] 成功寫入待簽章區`

3. **第 3 次 add【退回拒絕】**
   - 標題：健保醫療辦法 第7條 慢性病人特殊情況得委請他人代述病情領藥
   - 出處：健保醫療辦法 第7條
   - 網址：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0060009&flno=7
   - 摘句：「但須長期用藥之慢性病人，有下列特殊情況之一而無法親自就醫者，以繼續領取相同方劑為限，得委請他人向醫師陳述病情，醫師依其專業知識之判斷，確信可以掌握病情，始能開給相同方劑：  一、行動不便，經醫師認定或經受託人提供切結文件。」
   - 結果：`❌ [ADD_REJECTED] 出處法規名稱 '健保醫療辦法' 不完整或不符，法定完整名稱為 '全民健康保險醫療辦法'`
   - 存證：已將真實退件記錄存為 `scripts/tests/case_027_第1輪退件_法規簡稱不符完整法定名稱.md`【應退回】，`run_cases.py` 測試套件已擴充並通過（27 PASS / 0 FAIL）。

4. **第 4 次 add【修正法規全名後成功】**
   - 標題：全民健康保險醫療辦法 第7條 慢性病人特殊情況得委請他人代述病情領藥
   - 出處：全民健康保險醫療辦法 第7條
   - 網址：https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0060009&flno=7
   - 摘句：「但須長期用藥之慢性病人，有下列特殊情況之一而無法親自就醫者，以繼續領取相同方劑為限，得委請他人向醫師陳述病情，醫師依其專業知識之判斷，確信可以掌握病情，始能開給相同方劑：  一、行動不便，經醫師認定或經受託人提供切結文件。」
   - 結果：`✅ [ADD_SUCCESS] 成功寫入待簽章區`

---

### 3. learning_ledger.jsonl 追加行
檔案路徑：`Office_of_the_CIO_Falcon/01_Cognitive_Log/learning_ledger.jsonl`
```json
{"round": 1, "topic": "藥事法：代領、配送處方藥的限制", "started": "2026-11-25T00:48:35+08:00", "ended": "2026-11-25T00:51:25.073394+08:00", "add_ok": 3, "add_rejected": 1}
```

---

### 4. 對生活管家的影響推論
這是我方的推論：生活管家專員嚴禁在無合法處方箋或未經醫師診察之情況下為客戶代購、調劑處方藥品；但在慢性病長輩病情穩定、持有合法慢箋或符合全民健康保險醫療辦法第7條之特殊情況下，受長輩或家屬合法委託代為前往特約藥局領取已調劑之慢箋藥品並轉交，定性為純勞務跑腿委任，惟全程嚴禁涉及任何藥品調劑或藥事照護專業業務，以物理阻隔藥事法第50條與藥師法第15條之行政處罰紅線。
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
