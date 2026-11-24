import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。兩件事已全部按你的規格精確修正完畢，彙報如下：

============================================================
一、 修 run_cases.py 與新增 case_007 執行結果
============================================================
1. **修復兩處漏洞**：
   a. 已刪除寫死的 `target_names`，改為動態掃描 `sorted(TESTS_DIR.glob("case_*.md"))`。
   b. `find_snapshot` 刪除 fallback，找不到「同一部法、同一條號」快照時直接回傳 `None`；在主流程中，若找不到快照則業務判定 FAIL。
      - 若案例標記為【應退回】（如 case_007），則成功攔截退回，判定 PASS。
      - 若案例標記為【應通過】，則判定 FAIL。
2. **新增 `case_007_快照條號不符.md`**：
   - 網址填公平法 §42，但在 `snapshots/` 裡故意不放 §42 的快照，標【應退回】。
3. **執行結果（最後 10 行）**：
```
[PASS] case_007_快照條號不符.md
       標記: 【應退回】 | 快照: 無 (條號不符或檔案不存在)
       判定: 符合預期：找不到對應條號快照，業務判定 FAIL，成功攔截退回
       說明: 網址引用公平交易法第42條罰則，但 snapshots/ 資料夾中故意不提供第42條快照（僅有第21條）。find_snapshot 必須嚴格比對條號，不得拿第21條快照充數，找不到精確條號快照時必須判定 FAIL，成功攔截退回。
-----------------------------------------------------------------
=================================================================
測試案例彙總統計
=================================================================
總案例數: 7 個
測試成功 (PASS): 7 個
測試失敗 (FAIL): 0 個
通過率: 100.0%
=================================================================
```

============================================================
二、 類別 B 改名與「營運幕僚長」grep 搜尋輸出
============================================================
1. **修改完成清單**：
   - `00-00_Corporate_AI_HR_Directory.md` 第 26 行、第 63 行：已改為「首席法務顧問兼市場情報長 (CIO)」
   - `00-03-04-00_Characters_Overview.md` 第 30 行：已改為「首席法務顧問兼市場情報長 CIO」
   - `06_獵鷹_Falcon/persona.md` 第 4 行：已改為「首席法務顧問兼市場情報長 (CIO / Chief Legal & Market Intelligence)」
   - `06_獵鷹_Falcon/images/README.md` 第 3 行：已改為「首席法務顧問兼市場情報長」
   - `02_外圈代倒垃圾包月_999與1999/01_SOP_標準作業流程.md` 第 6 行：已改為「首席法務顧問兼市場情報長 雪柔 (Sheryl) 審定」
   - `scripts/append_log.py`、`scripts/append_log_case01.py` 第 9 行：已改為「首席法務顧問兼市場情報長 雪柔」
2. **保留與更正說明**：
   - `00-00_Corporate_AI_HR_Directory.md` 第 64 行：保留「美國財政部幕僚長」（原型人物歷史經歷，不改動）。
   - `00-00_System_Operations_Log.md`：歷史紀錄不篡改，已於檔尾追加：
     `職稱更正：雪柔自 2026-11-24 起為首席法務顧問兼市場情報長`
3. **全系統 grep 搜尋「營運幕僚長」完整輸出**：
```
00-00_System_Operations_Log.md:1791:> **主政長官**：首席法務顧問兼營運幕僚長 雪柔 (Sheryl Sandberg) ＆ 首席品質長 戴明 (Dr. Deming)
00-00_System_Operations_Log.md:1809:> **主政長官**：首席法務顧問兼營運幕僚長 雪柔 (Sheryl Sandberg) ＆ 市場行銷長 泰勒絲 (Taylor)
00-00_System_Operations_Log.md:1818:> **主政長官**：首席法務顧問兼營運幕僚長 雪柔 (Sheryl Sandberg) ＆ 市場行銷長 泰勒絲 (Taylor)
TOTAL_MATCHES: 3
```
（全系統除 `System_Operations_Log.md` 的 3 處歷史操作日誌外，其餘所有工作區現行檔案均已零殘留！）

兩項任務皆已達到驗收標準，請 Claude 指示下一步「修正技能檔第六章：把第 13–24 條補上出處網址，對不上的照快照改正」！
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
