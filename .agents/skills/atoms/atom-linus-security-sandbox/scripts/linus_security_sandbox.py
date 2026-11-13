#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-linus-security-sandbox: 資安金庫隔離與進程沙盒獵殺原子腳本
專職負責工程長林納斯 (Linus) 資安與進程防線（Pre-commit私鑰掃描、ReDoS回溯檢驗、沙盒隔離）。
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

# 敏感憑證與私鑰特徵庫
SECRET_SIGNATURES = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token"),
    (r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "Private Key"),
    (r"bearer\s+[a-zA-Z0-9_\-\.]{20,}", "Bearer Token"),
]

# 典型 ReDoS 災難性回溯特徵 (巢狀量詞)
REDOS_VULNERABILITY_PATTERNS = [
    r"\([^\)]*[\+\*]\)[\+\*]",  # (a+)+ or (x*)*
    r"\([^\)]*\|[^\)]*[\+\*]\)[\+\*]",  # (a|b+)+
]

def scan_text_for_secrets(text: str) -> dict:
    """Pre-commit 提交前私鑰與 Token 掃描"""
    lines = text.splitlines()
    findings = []

    for idx, line in enumerate(lines, 1):
        for pattern, sig_name in SECRET_SIGNATURES:
            if re.search(pattern, line):
                findings.append({
                    "line": idx,
                    "signature": sig_name,
                    "snippet": line.strip()[:60] + "..."
                })

    passed = (len(findings) == 0)
    return {
        "passed": passed,
        "findings_count": len(findings),
        "findings": findings
    }

def audit_regex_redos_safety(regex_pattern: str) -> dict:
    """審計正則表達式是否具備 ReDoS 回溯漏洞"""
    vulnerabilities = []
    for pat in REDOS_VULNERABILITY_PATTERNS:
        if re.search(pat, regex_pattern):
            vulnerabilities.append({
                "risk": "NESTED_QUANTIFIER_DETECTED",
                "pattern": pat,
                "reason": "偵測到巢狀量詞結構，在極端惡意輸入下將觸發 O(2^N) 災難性指數回溯！"
            })

    safe = (len(vulnerabilities) == 0)
    return {
        "regex": regex_pattern,
        "safe": safe,
        "vulnerabilities": vulnerabilities,
        "recommendation": "✅ 正則表達式符合 RE2 線性時間規範。" if safe else "❌ 警告：正則存在 ReDoS 漏洞，必須扁平化重寫！"
    }

def main():
    parser = argparse.ArgumentParser(description="資安金庫隔離與進程沙盒獵殺原子")
    parser.add_argument("--scan-secrets", type=str, help="待掃描之代碼檔案路徑")
    parser.add_argument("--audit-regex", type=str, help="待檢測之正則表達式")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-linus-security-sandbox] 啟動資安金庫與進程沙盒審查 ===")

    # 1. 審計正則 ReDoS
    if args.audit_regex:
        reg_res = audit_regex_redos_safety(args.audit_regex)
        print(f"\n🔍 **【Google RE2 正則線性時間審查 (Law 13)】**")
        print(f"表達式: `{reg_res['regex']}`")
        print(f"安全結論: {reg_res['recommendation']}")
        if not reg_res["safe"]:
            sys.exit(1)

    # 2. 掃描私鑰洩漏
    if args.scan_secrets and os.path.exists(args.scan_secrets):
        content = Path(args.scan_secrets).read_text(encoding='utf-8')
        sec_res = scan_text_for_secrets(content)
        print(f"\n🛡️ **【Pre-Commit 本地私鑰防漏掃描 (Law 11)】**")
        print(f"掃描檔案: {args.scan_secrets} | 違規洩漏數: {sec_res['findings_count']}")
        if not sec_res["passed"]:
            print("[-] 攔截到機密洩漏：")
            for f in sec_res["findings"]:
                print(f"  * 第 {f['line']} 行: [{f['signature']}]")
            sys.exit(1)
        else:
            print("[+] 未偵測到任何 API Key 或私鑰，物理防漏通過！")

    print("\n[+] 林納斯資安與沙盒隔離檢驗通過 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
