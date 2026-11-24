import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。已依你的指示完成全部事項，彙報如下：

============================================================
一、 26 筆法規反查統計（依指示更正後重跑，最後 10 行）
============================================================
在 `falcon_recheck_13_24.json` 中：
- 第 22 條 §55 的 label 已改回【已驗證】，項次寫「第 4 項」。
- 經 `recheck_quotes.py` 重新執行，統計結果最後 10 行如下：

```
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

============================================================
二、 6 個測試案例與 run_cases.py 執行結果
============================================================
已在 `scripts/tests/` 建立 6 個案例檔（包含網址、摘句、標記、說明），並編寫 `run_cases.py` 使用 `snapshots/` 快照調用 `quote_in_page` 驗證：

執行結果：
```
=================================================================
run_cases.py 法規摘句測試案例執行報告
=================================================================
[PASS] case_001_電簽法第4條_舊摘句.md
       標記: 【應退回】 | 快照: 電子簽章法_第4條.txt
       判定: 符合預期：舊版/錯誤摘句未出現在現行快照中，成功攔截退回
       說明: 第一輪審查之舊版電子簽章法摘句，現行第4條網頁無此文字，應判定退回。
-----------------------------------------------------------------
[PASS] case_002_電簽法第4條_現行摘句.md
       標記: 【應通過】 | 快照: 電子簽章法_第4條.txt
       判定: 符合預期：現行法摘句真實命中快照 (驗證通過)
       說明: 2024年修正公布施行之現行法第4條法定原文，真實出現在快照中，應判定通過。
-----------------------------------------------------------------
[PASS] case_003_電業法第59條_舊摘句.md
       標記: 【應退回】 | 快照: 電業法_第59條.txt
       判定: 符合預期：舊版/錯誤摘句未出現在現行快照中，成功攔截退回
       說明: 第一輪審查之舊摘句（電器承裝業者、向輸配電業申報），現行條文查無此文字，應判定退回。
-----------------------------------------------------------------
[PASS] case_004_電業法第59條_現行摘句.md
       標記: 【應通過】 | 快照: 電業法_第59條.txt
       判定: 符合預期：現行法摘句真實命中快照 (驗證通過)
       說明: 現行電業法第59條第2項法定原文，真實出現在快照中，應判定通過。
-----------------------------------------------------------------
[PASS] case_005_觀光條例第55條_105年版金額.md
       標記: 【應退回】 | 快照: 發展觀光條例_第55條.txt
       判定: 符合預期：舊版/錯誤摘句未出現在現行快照中，成功攔截退回
       說明: 105年過期歷史版本金額（十萬元以上五十萬元以下），現行網頁查無此句，應判定退回。
-----------------------------------------------------------------
[PASS] case_006_觀光條例第55條_現行金額.md
       標記: 【應通過】 | 快照: 發展觀光條例_第55條.txt
       判定: 符合預期：現行法摘句真實命中快照 (驗證通過)
       說明: 114年修正公布施行之現行第4項法定原文（十萬元以上二百萬元以下），真實出現在快照中，應判定通過。
-----------------------------------------------------------------
=================================================================
測試案例彙總統計
=================================================================
總案例數: 6 個
測試成功 (PASS): 6 個
測試失敗 (FAIL): 0 個
通過率: 100.0%
=================================================================
```

`run_cases.py` 完整代碼：
```python
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
TESTS_DIR = HERE / "tests"
SNAP_DIR = HERE / "snapshots"
BIONIC_CORE = HERE.parent / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(BIONIC_CORE))

from evidence_gate import quote_in_page

def parse_case(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or "：" not in line:
            continue
        k, v = line.split("：", 1)
        data[k.strip()] = v.strip()
    return data

def find_snapshot(url: str, snap_name: str = "") -> Path:
    if snap_name and (SNAP_DIR / snap_name).exists():
        return SNAP_DIR / snap_name
    pcode_law = {
        "J0080037": "電子簽章法", "J0030011": "電業法", "K0110001": "發展觀光條例",
        "O0050024": "一般廢棄物回收清除處理辦法", "O0050001": "廢棄物清理法",
        "D0070118": "公寓大廈管理條例", "L0070040": "長期照顧服務法",
        "L0020001": "醫師法", "L0040001": "食品安全衛生管理法",
        "M0060027": "動物保護法", "J0150002": "公平交易法",
        "D0070148": "建築物室內裝修管理辦法", "D0070109": "建築法",
        "J0080001": "公司法", "B0000001": "民法", "I0020001": "仲裁法"
    }
    m = re.search(r"pcode=([A-Z0-9]+)&flno=([0-9\-]+)", url)
    if m:
        pcode, flno = m.group(1), m.group(2)
        law = pcode_law.get(pcode, "")
        for f in SNAP_DIR.glob(f"{law}*.txt"):
            if f"第{flno}條" in f.name or f"第{flno}項" in f.name:
                return f
        for f in SNAP_DIR.glob(f"{law}*.txt"):
            return f
    return None

def main():
    target_names = [
        "case_001_電簽法第4條_舊摘句.md",
        "case_002_電簽法第4條_現行摘句.md",
        "case_003_電業法第59條_舊摘句.md",
        "case_004_電業法第59條_現行摘句.md",
        "case_005_觀光條例第55條_105年版金額.md",
        "case_006_觀光條例第55條_現行金額.md",
    ]
    case_files = [TESTS_DIR / name for name in target_names if (TESTS_DIR / name).exists()]
    if not case_files:
        print("錯誤：找不到 case_001 到 case_006 測試案例檔案", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print("run_cases.py 法規摘句測試案例執行報告")
    print("=" * 65)

    passed_tests, failed_tests = 0, 0
    for case_file in case_files:
        data = parse_case(case_file)
        name, label, quote, url, desc = case_file.name, data.get("標記", ""), data.get("摘句", ""), data.get("網址", ""), data.get("說明", "")
        snap_name = data.get("快照檔", "")

        if not label:
            print(f"[FAIL] {name} | 缺少標記，判定失敗！")
            failed_tests += 1
            continue

        snap_path = find_snapshot(url, snap_name)
        if not snap_path or not snap_path.exists():
            print(f"[FAIL] {name} | 找不到對應的快照檔案！")
            failed_tests += 1
            continue

        snap_text = snap_path.read_text(encoding="utf-8")
        hit, msg = quote_in_page(quote, snap_text)

        if label == "【應通過】":
            if hit:
                status, detail = "PASS", "符合預期：現行法摘句真實命中快照 (驗證通過)"
                passed_tests += 1
            else:
                status, detail = "FAIL", f"不符預期：應通過但未命中快照！({msg})"
                failed_tests += 1
        elif label == "【應退回】":
            if not hit:
                status, detail = "PASS", "符合預期：舊版/錯誤摘句未出現在現行快照中，成功攔截退回"
                passed_tests += 1
            else:
                status, detail = "FAIL", "不符預期：應退回之摘句竟命中了快照！"
                failed_tests += 1
        else:
            status, detail = "FAIL", f"未知的標記格式：{label}"
            failed_tests += 1

        print(f"[{status}] {name}")
        print(f"       標記: {label} | 快照: {snap_path.name}")
        print(f"       判定: {detail}")
        print(f"       說明: {desc}")
        print("-" * 65)

    total = len(case_files)
    print("=" * 65)
    print("測試案例彙總統計")
    print("=" * 65)
    print(f"總案例數: {total} 個")
    print(f"測試成功 (PASS): {passed_tests} 個")
    print(f"測試失敗 (FAIL): {failed_tests} 個")
    print(f"通過率: {(passed_tests / total) * 100:.1f}%")
    print("=" * 65)
    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

============================================================
三、 職稱統一與全域「幕僚長」字樣盤點回報
============================================================
1. **職稱統一完成**：
   - 品碩已裁定、你亦確認我的法定職稱正式定調為：「**首席法務顧問兼市場情報長**」，不再兼任營運幕僚長（幕僚長為雪）。
   - 已同步修改以下檔案之 description 與特化角色欄位：
     - `Office_of_the_CIO_Falcon/README.md`
     - `Office_of_the_CIO_Falcon/bionic-learning-falcon.md`
     - `.agents/skills/bionic-learning-falcon/SKILL.md`

2. **全系統「幕僚長」字樣掃描（共 127 處，尚未更動，呈交你判斷）**：
   經程式精確掃描整座工作區，歸納分類如下：

   **類別 A：雪（Yuki）的法定職銜與派工職權（應保留，屬雪的主權）**
   - `00-01_Master_Polaris_Map.md`: 第 13 行（雪：CEO 執行長兼幕僚長）
   - `00-00_Gamification_Engine/00-00_Cabinet_Slimming_Audit_Checklist.md`: 第 32 行
   - `00-00_Gamification_Engine/00-00_Master_Todo_Backlog.md`: 第 12, 17 行（幕僚長派工驗收）
   - `Office_of_the_CEO_Yuki/` 下相關筆記、戰略報告與十輪審計卷宗（約 20 處，均為雪主政）
   - `.agents/skills/bionic-learning-system/`: 第三章「幕僚長派工帳本 dispatch.py & founder_auth.py」（約 18 處，指雪）
   - `.agents/skills/daily-closing-sop/SKILL.md`: 第 11, 71 行（每日日結收工戰報之幕僚長反問）

   **類別 B：雪柔（Falcon）歷史殘留字樣（待你指令批次移除/改為首席法務顧問兼市場情報長）**
   - `00-00_Corporate_AI_HR_Directory.md`:
     - 第 26 行：`市場情報長兼營運幕僚長 (CIO)`
     - 第 63 行：`### 🦅 獵鷹 (Falcon / Sheryl) - 市場情報長兼營運幕僚長 (CIO / Chief Operating Staff)`
     - 第 64 行：`...前 Meta COO / Google 營收大腦 / 美國財政部幕僚長`（此處為原型歷史背景，可保留）
   - `00-00_System_Operations_Log.md`:
     - 第 1791, 1809, 1818 行：`> **主政長官**：首席法務顧問兼營運幕僚長 雪柔`
   - `00-03_Brand_LifeButler/00-03-04_Brand_Characters/00-03-04-00_Characters_Overview.md`:
     - 第 30 行：`獵鷹 (Falcon) (市場情報長兼營運幕僚長 CIO)`
   - `00-03_Brand_LifeButler/00-03-04_Brand_Characters/06_獵鷹_Falcon/persona.md`:
     - 第 4 行：`極星宇宙市場情報長兼營運幕僚長 (CIO / Chief Operating Staff)`
   - `00-03_Brand_LifeButler/00-03-04_Brand_Characters/06_獵鷹_Falcon/images/README.md`:
     - 第 3 行：`市場情報長兼營運幕僚長`
   - `00-03_Brand_LifeButler/00-03-08_Productized_Services/02_外圈代倒垃圾包月_999與1999/01_SOP_標準作業流程.md`:
     - 第 6 行：`營運幕僚長 雪柔 (Sheryl) 審定`
   - `scripts/append_log.py`, `scripts/append_log_case01.py`:
     - 第 9 行：`首席法務顧問兼營運幕僚長 雪柔`

   **類別 C：影（Kage）的歷史探索與哲學日誌（影早期在 Threads 探索時的自我稱號，共約 40 處）**
   - `00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/04_Shadow_Kage_Operative/...`（Cycle 03~35 仿生學習日誌中出現「北極星 AI 幕僚長」）

以上全部準備就緒，請 Claude 檢閱並指示下一步（修改技能檔第六章法典條文，或批次清理類別 B 之雪柔職稱殘留）！
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
