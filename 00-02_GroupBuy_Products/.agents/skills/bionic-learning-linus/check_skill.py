#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_skill.py — 驗收 bionic-learning-linus 技能檔修正成果
"""

import sys
import re
from pathlib import Path

def main():
    cur = Path(__file__).resolve()
    # 尋找 00_Master_Polaris 根目錄
    polaris_root = None
    for p in [cur] + list(cur.parents):
        if (p / ".agents" / "skills" / "bionic-learning-linus" / "SKILL.md").exists():
            polaris_root = p
            break

    if not polaris_root:
        # fallback: 假設上一層
        polaris_root = cur.parents[1]

    p1 = polaris_root / "00-00_Gamification_Engine" / "Office_of_the_CTO_Linus" / "bionic-learning-linus.md"
    p2 = polaris_root / ".agents" / "skills" / "bionic-learning-linus" / "SKILL.md"

    if not p1.exists() or not p2.exists():
        print(f"錯誤：檔案不存在 p1={p1.exists()} p2={p2.exists()}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)

    t1 = p1.read_text(encoding="utf-8")
    t2 = p2.read_text(encoding="utf-8")

    # 1. 兩份檔案內容完全相同
    cond1 = (t1 == t2)

    # 2. base_master 這一行包含 v6.5
    base_master_lines = [l for l in t1.splitlines() if l.strip().startswith("base_master:")]
    cond2 = bool(base_master_lines and "v6.5" in base_master_lines[0])

    # 3. 全文找不到「v5.2」，也找不到「210」
    cond3 = ("v5.2" not in t1) and ("210" not in t1)

    # 4. 第六章和第八章用正則抓「數字＋單位」或「數字＋%」，抓到 0 筆
    ch6_match = re.search(r"##\s*⚡?\s*第六章.*?(?=##\s*🔬?\s*第七章)", t1, re.DOTALL)
    ch8_match = re.search(r"##\s*⚖️?\s*第八章.*?(?=##\s*📚?\s*第九章)", t1, re.DOTALL)

    ch6_text = ch6_match.group(0) if ch6_match else ""
    ch8_text = ch8_match.group(0) if ch8_match else ""
    target_text = ch6_text + "\n" + ch8_text

    pattern = r"\d+(?:\.\d+)?\s*(?:%|ms|μs|us|s|sec|min|h|MB|GB|KB|TB|B|Bytes|TPS|QPS|cpb|倍|次|筆|個|行|秒|分|小時|天|輪|代|階)"
    matches = re.findall(pattern, target_text, re.IGNORECASE)
    cond4 = (len(matches) == 0)

    # 5. 「第 2–5 章依母版 v6.5 執行」這句有出現
    cond5 = ("第 2–5 章依母版 v6.5 執行" in t1)

    all_pass = cond1 and cond2 and cond3 and cond4 and cond5

    if not all_pass:
        print("FAIL")
        sys.exit(1)

    # 印出最後 6 行
    print("1. 兩份檔案內容完全相同：PASS")
    print("2. base_master 包含 v6.5：PASS")
    print("3. 全文無 v5.2 且無 210：PASS")
    print(f"4. 第六章與第八章數字單位及%抓到 {len(matches)} 筆：PASS")
    print("5. 「第 2–5 章依母版 v6.5 執行」存在：PASS")
    print("驗收結果：ALL PASS")

if __name__ == "__main__":
    main()
