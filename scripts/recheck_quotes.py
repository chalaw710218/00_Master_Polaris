"""
recheck_quotes.py — 逐條驗證第六章第 13–24 條所有被引用條號之逐字摘句
呼叫母版 bionic_core/evidence_gate.py 之 fetch_page_text 與 quote_in_page
每抓取一頁即原封不動存成 snapshots/<law>_<article>.txt，供外部查核驗收
"""

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
SNAP_DIR = HERE / "snapshots"
SNAP_DIR.mkdir(parents=True, exist_ok=True)


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
        law = item.get("law", "")
        article = item.get("article", "")
        url = item.get("url", "")
        quote = item.get("quote", "")
        label = item.get("label", "【未驗證】")

        counts_label[label] = counts_label.get(label, 0) + 1

        # 抓取網頁
        try:
            page_text = fetch_page_text(url, timeout=20)
        except Exception as e:
            status = "FETCH_ERROR"
            counts_verify["FETCH_ERROR"] += 1
            print(f"{r_no} | {law} {article} | {url} | FETCH_ERROR")
            results.append((r_no, law, article, url, status, label, str(e)))
            continue

        # 儲存原始快照供外部檢驗 (原封不動存檔)
        snap_file = SNAP_DIR / f"{law}_{article}.txt"
        try:
            with open(snap_file, "w", encoding="utf-8") as sf:
                sf.write(page_text)
        except Exception as se:
            print(f"警告：快照寫入失敗 {snap_file}: {se}", file=sys.stderr)

        # 呼叫母版 evidence_gate 比對摘句
        ok, msg = quote_in_page(quote, page_text)
        if ok:
            status = "PASS"
            counts_verify["PASS"] += 1
            print(f"{r_no} | {law} {article} | {url} | PASS")
        else:
            status = "FAIL"
            counts_verify["FAIL"] += 1
            print(f"{r_no} | {law} {article} | {url} | FAIL")

        results.append((r_no, law, article, url, status, label, msg))

    total = len(records)
    print("\n" + "=" * 60)
    print("recheck_quotes.py 程式執行統計結果")
    print("=" * 60)
    print(f"總查核筆數 (被引用條號): {total} 筆")
    print(f"摘句驗證 PASS (真實出現在網頁): {counts_verify['PASS']} 筆")
    print(f"摘句驗證 FAIL (網頁找不到摘句): {counts_verify['FAIL']} 筆")
    print(f"網頁抓取 FETCH_ERROR: {counts_verify['FETCH_ERROR']} 筆")
    print("-" * 60)
    print(f"法條比對標記 【已驗證】: {counts_label['【已驗證】']} 筆")
    print(f"法條比對標記 【對不上】: {counts_label['【對不上】']} 筆")
    print(f"法條比對標記 【未驗證】: {counts_label['【未驗證】']} 筆")
    print(f"快照存檔目錄: {SNAP_DIR.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
