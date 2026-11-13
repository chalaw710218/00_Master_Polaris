#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-yuki-brand-redline-gate: 品牌法定名稱零洩漏與出廠安全閘門原子腳本
專職執行《工作區憲則·規則 5》品牌法定名稱防火牆，一票否決「極星/Polaris」對外洩漏。
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 內部研發絕對機密代號（對外一票否決）
LEAKED_REDLINE_PATTERNS = [
    r"極星",
    r"polaris",
    r"北極星",
]

STATUTORY_BRAND_FULL = "生活的一部分，就醬點！"
STATUTORY_ROLE_NAME = "生活管家"

def scan_brand_firewall(text: str) -> dict:
    """執行品牌防火牆對外安全掃描"""
    lines = text.splitlines()
    violations = []

    combined_regex = re.compile("|".join(f"({p})" for p in LEAKED_REDLINE_PATTERNS), re.IGNORECASE)

    for idx, line in enumerate(lines, 1):
        matches = combined_regex.findall(line)
        if matches:
            matched_words = [m[0] for m in matches if m[0]]
            violations.append({
                "line": idx,
                "matched_words": matched_words,
                "content_snippet": line.strip()[:80]
            })

    has_brand = STATUTORY_BRAND_FULL in text or "就醬點" in text
    has_role = STATUTORY_ROLE_NAME in text

    passed = (len(violations) == 0)

    return {
        "passed": passed,
        "violations_count": len(violations),
        "violations": violations,
        "contains_statutory_brand": has_brand,
        "contains_statutory_role": has_role
    }

def auto_fix_brand_leak(text: str) -> str:
    """自動修復違規代號，平滑替換為法定名稱"""
    fixed = text
    # 將內部研發代號替換為合法業務自稱
    fixed = re.sub(r"極星團隊|極星內閣|極星夥伴", "生活管家團隊", fixed)
    fixed = re.sub(r"極星|polaris|北極星", "生活管家", fixed, flags=re.IGNORECASE)
    return fixed

def main():
    parser = argparse.ArgumentParser(description="品牌法定名稱零洩漏與出廠安全閘門原子")
    parser.add_argument("--text", type=str, help="待審查之對外文案純文字")
    parser.add_argument("--file-path", type=str, help="待審查檔案路徑")
    parser.add_argument("--auto-fix", action="store_true", default=False, help="自動修復違規代號")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    content = ""
    if args.file_path and os.path.exists(args.file_path):
        content = Path(args.file_path).read_text(encoding='utf-8')
    elif args.text:
        content = args.text
    else:
        # 內建模擬合規對外文案樣品
        content = (
            "【生活的一部分，就醬點！】在台東，柴米油鹽是真實的修行。"
            "我是您的生活管家，今天為大家準備了成功港直送的現流高脂午仔魚！"
        )

    print("=== [atom-yuki-brand-redline-gate] 啟動品牌法定名稱防火牆掃描 ===")
    res = scan_brand_firewall(content)

    print(f"\n官方品牌全稱確證 (生活的一部分，就醬點！): {'[已包含]' if res['contains_statutory_brand'] else '[未包含完整全稱]'}")
    print(f"日常業務自稱確證 (生活管家): {'[已包含]' if res['contains_statutory_role'] else '[未包含]'}")
    print(f"內部代號洩漏違規數: {res['violations_count']}")

    if not res["passed"]:
        print("\n❌ **【戴明安燈拉繩：攔截到品牌絕對紅線洩漏】**")
        for v in res["violations"]:
            print(f"  * 第 {v['line']} 行: 發現內部代號 {v['matched_words']} ➔ 『{v['content_snippet']}』")

        if args.auto_fix:
            fixed_text = auto_fix_brand_leak(content)
            print("\n[+] 已自動執行品牌名稱合規修復：")
            print(fixed_text[:200] + "...")
            if args.file_path and not args.dry_run:
                Path(args.file_path).write_text(fixed_text, encoding='utf-8')
                print("[+] 修復後文本已寫回檔案。")
            sys.exit(0)
        else:
            print("\n[-] 違反《全域憲則·規則5》，一票否決出廠 (Exit Code: 1)！")
            sys.exit(1)

    print("\n🛡️ **【品牌法定名稱零洩漏防火牆檢驗 100% 通過】**")
    print("[+] 無任何內部研發代號洩漏，准許正式發布出廠 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
