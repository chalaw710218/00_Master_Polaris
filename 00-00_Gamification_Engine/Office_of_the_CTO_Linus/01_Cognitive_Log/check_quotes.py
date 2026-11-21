# -*- coding: utf-8 -*-
"""
check_quotes.py — 動態檢查反查表中的網址與逐字原文是否真實存在於網頁中
"""

import sys
import re
from pathlib import Path

# 動態尋找 00_Master_Polaris 根目錄並載入 evidence_gate
cur = Path(__file__).resolve()
polaris_root = None
for p in cur.parents:
    if (p / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "evidence_gate.py").exists():
        polaris_root = p
        break

if not polaris_root:
    print("錯誤：找不到 evidence_gate.py", file=sys.stderr)
    sys.exit(1)

bionic_core_path = polaris_root / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
if str(bionic_core_path) not in sys.path:
    sys.path.insert(0, str(bionic_core_path))

from evidence_gate import fetch_page_text, quote_in_page


def parse_and_check(md_path: Path):
    if not md_path.exists():
        print(f"錯誤：找不到檔案 {md_path}", file=sys.stderr)
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_found = False
    col_idx = {}

    for line_num, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells:
            continue

        # 偵測表頭
        if "編號" in cells and ("網址" in cells or "標記" in cells):
            header_found = True
            for i, c in enumerate(cells):
                col_idx[c] = i
            continue

        # 略過分隔線
        if all(re.match(r"^:?-+:?$", c) for c in cells):
            continue

        if not header_found:
            continue

        # 提取各欄位
        try:
            row_id = cells[col_idx.get("編號", 0)]
            tag = cells[col_idx.get("標記", 2)]
            url = cells[col_idx.get("網址", 3)]
            quote = cells[col_idx.get("逐字原句", 4)]
        except IndexError:
            continue

        if not row_id or not row_id.isdigit():
            # 可能是非數據列
            continue

        # 判斷邏輯
        if "未驗證" in tag:
            print(f"{row_id} 跳過（未驗證）")
            continue

        if url == "無" or not url or quote == "無" or not quote:
            print(f"{row_id} 跳過（無網址/原句）")
            continue

        if "已驗證" in tag or "概念有出處" in tag or "對不上" in tag:
            try:
                page_text = fetch_page_text(url)
            except Exception as e:
                print(f"{row_id} False 抓不到（{e}）")
                continue

            ok, why = quote_in_page(quote, page_text)
            if ok:
                print(f"{row_id} True")
            else:
                print(f"{row_id} False {why}")
        else:
            print(f"{row_id} 跳過（未驗證）")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python check_quotes.py <反查表.md>")
        sys.exit(1)

    target_file = Path(sys.argv[1]).resolve()
    parse_and_check(target_file)
