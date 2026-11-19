import csv
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
COG_LOG_DIR = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log"

ORIG_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence.md"
BACKUP_DIR = COG_LOG_DIR / "_未驗證封存"
BACKUP_FILE = BACKUP_DIR / "01_Experiences_and_Evidence_原檔_20261120.md"
V2_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence_v2.md"

INVENTORY_CSV = COG_LOG_DIR / "_fact_inventory.csv"
REVERIFY_CSV = COG_LOG_DIR / "_reverify_papers.csv"
EXP_CSV = COG_LOG_DIR / "_exp_evidence.csv"


def get_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not ORIG_FILE.is_file():
        print(f"錯誤：找不到原檔 {ORIG_FILE}", file=sys.stderr)
        sys.exit(1)
    if not INVENTORY_CSV.is_file():
        print(f"錯誤：找不到 inventory {INVENTORY_CSV}", file=sys.stderr)
        sys.exit(1)
    if not REVERIFY_CSV.is_file():
        print(f"錯誤：找不到 reverify {REVERIFY_CSV}", file=sys.stderr)
        sys.exit(1)
    if not EXP_CSV.is_file():
        print(f"錯誤：找不到 exp evidence {EXP_CSV}", file=sys.stderr)
        sys.exit(1)

    # 記錄原檔修改時間
    orig_mtime = datetime.fromtimestamp(ORIG_FILE.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    # (A) 備份：若備份檔已存在就不要重寫
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    if not BACKUP_FILE.exists():
        raw_bytes = ORIG_FILE.read_bytes()
        BACKUP_FILE.write_bytes(raw_bytes)

    # 比對 sha256
    orig_sha = get_sha256(ORIG_FILE)
    backup_sha = get_sha256(BACKUP_FILE)
    sha_identical = (orig_sha == backup_sha)
    sha_str = "是" if sha_identical else "否"

    # (B) 讀取 _fact_inventory.csv 建立序號 -> 標題對照表
    inventory_titles = {}
    with open(INVENTORY_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            seq = row[0].strip()
            title = row[1].strip() if len(row) > 1 else ""
            inventory_titles[seq] = title

    # (C) 讀取 _reverify_papers.csv 只收「已驗證」與「對不上」
    verified_count = 0
    mismatch_count = 0
    v2_entries = []

    with open(REVERIFY_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            seq = row[0].strip()
            status = row[1].strip() if len(row) > 1 else ""
            url = row[2].strip() if len(row) > 2 else ""
            quote = row[3].strip() if len(row) > 3 else ""
            note = row[4].strip() if len(row) > 4 else ""

            if status not in ("已驗證", "對不上"):
                continue

            inv_title = inventory_titles.get(seq, "")
            clean_title = inv_title.lstrip("#").strip()

            entry_lines = [
                f"### [序號 {seq}] {clean_title}",
                f"- 狀態：{status}",
                f"- 出處：{url}",
                f"- 逐字摘句：{quote}",
            ]
            if status == "對不上":
                entry_lines.append(f"- 對不上說明：{note}")
                mismatch_count += 1
            else:
                verified_count += 1

            v2_entries.append("\n".join(entry_lines))

    # (D) 讀取 _exp_evidence.csv 處理 4 條 EXP
    exp_groups = {}
    with open(EXP_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            seq = row[0].strip()
            evidence = row[1].strip() if len(row) > 1 else ""
            status = row[2].strip() if len(row) > 2 else ""
            path_str = row[3].strip() if len(row) > 3 else ""
            exp_groups.setdefault(seq, []).append((evidence, status, path_str))

    internal_verified_count = 0
    for seq in ("5", "6", "7", "8"):
        ev_list = exp_groups.get(seq, [])
        if not ev_list:
            continue
        # 檢查是否全部證據都「存在」
        if all(st == "存在" for _, st, _ in ev_list):
            inv_title = inventory_titles.get(seq, "")
            clean_title = inv_title.lstrip("#").strip()

            entry_lines = [
                f"### [序號 {seq}] {clean_title}",
                "- 狀態：已驗證（內部證據）",
            ]
            for ev, _, path_str in ev_list:
                entry_lines.append(f"- 證據：{ev} → {path_str}")
            entry_lines.append("- 備註：僅證明證據存在；原條目「客觀結果」未驗證，見 _未驗證封存/")

            v2_entries.append("\n".join(entry_lines))
            internal_verified_count += 1

    # (E) 產生 01_Experiences_and_Evidence_v2.md
    v2_content = "本檔只收有網址與逐字摘句的條目；其餘見 _未驗證封存/\n\n" + "\n\n".join(v2_entries) + "\n"
    V2_FILE.write_text(v2_content, encoding="utf-8")

    v2_total = len(v2_entries)

    print("=" * 40)
    print(f"v2 條目數: {v2_total}")
    print(f"已驗證: {verified_count} 條")
    print(f"對不上: {mismatch_count} 條")
    print(f"已驗證（內部證據）: {internal_verified_count} 條")
    print(f"備份檔 sha256 是否仍和原檔相同: {sha_str}")
    print(f"原檔修改時間: {orig_mtime}")
    print("=" * 40)
    print(f"備份檔路徑: {BACKUP_FILE}")
    print(f"v2 檔案路徑: {V2_FILE}")


if __name__ == "__main__":
    main()
