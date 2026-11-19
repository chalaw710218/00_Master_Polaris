import csv
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Setup import path for evidence_gate
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
GATE_DIR = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

try:
    from evidence_gate import fetch_page_text, quote_in_page
except ImportError as e:
    print(f"無法載入 evidence_gate: {e}", file=sys.stderr)
    sys.exit(1)


def find_target_csv():
    candidates = [
        PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log" / "_reverify_papers.csv",
        Path("00-00_Gamification_Engine/Office_of_the_CEO_Yuki/01_Cognitive_Log/_reverify_papers.csv"),
        Path("Office_of_the_CEO_Yuki/01_Cognitive_Log/_reverify_papers.csv"),
    ]
    for c in candidates:
        if c.is_file():
            return c.resolve()
    matches = list(PROJECT_ROOT.glob("**/_reverify_papers.csv"))
    if matches:
        return matches[0].resolve()
    raise FileNotFoundError("找不到 _reverify_papers.csv")


def main():
    csv_path = find_target_csv()

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)

    total_rows = len(rows)
    verified_count = 0
    mismatch_count = 0
    unverified_count = 0
    failed_count = 0

    print(f"檢查檔案: {csv_path}")
    print(f"總共讀取 {total_rows} 列待驗證項目...\n")

    for row in rows:
        if not row:
            continue
        seq = row[0].strip()
        status = row[1].strip()
        url = row[2].strip() if len(row) > 2 else ""
        quote = row[3].strip() if len(row) > 3 else ""
        note = row[4].strip() if len(row) > 4 else ""

        if status in ("已驗證", "對不上"):
            if not url or not quote:
                print(f"❌ [序號 {seq}] 格式錯誤：標記為「{status}」但缺少網址或逐字摘句")
                failed_count += 1
                continue

            if status == "已驗證":
                frags = [f.strip(" \"'.") for f in re.split(r"\.\.\.|…", quote)]
                frags = [f for f in frags if f]
                short_frags = [f for f in frags if len(f) < 20]
                if short_frags:
                    print(f"❌ [序號 {seq}] 已驗證摘句片段不足 20 字：「{short_frags[0]}」（長度 {len(short_frags[0])} < 20）")
                    failed_count += 1
                    continue

            try:
                page_text = fetch_page_text(url, timeout=20)
                ok, err_msg = quote_in_page(quote, page_text)
                if ok:
                    print(f"✅ [序號 {seq}] {status}：抓取成功，摘句驗證通過 ({url})")
                    if status == "已驗證":
                        verified_count += 1
                    else:
                        mismatch_count += 1
                else:
                    print(f"❌ [序號 {seq}] {status}：摘句不在網頁上 - {err_msg} ({url})")
                    failed_count += 1
            except Exception as e:
                print(f"❌ [序號 {seq}] {status}：抓取網頁失敗 - {e} ({url})")
                failed_count += 1

        elif status == "未驗證":
            print(f"⚪ [序號 {seq}] 未驗證：{note or '找不到出處'}")
            unverified_count += 1

        else:
            print(f"❌ [序號 {seq}] 未知狀態：{status}")
            failed_count += 1

    print("\n" + "=" * 40)
    print(f"總列數: {total_rows}")
    print(f"已驗證: {verified_count} 列")
    print(f"對不上: {mismatch_count} 列")
    print(f"未驗證: {unverified_count} 列")
    print(f"檢查失敗: {failed_count} 列")
    print("=" * 40)

    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
