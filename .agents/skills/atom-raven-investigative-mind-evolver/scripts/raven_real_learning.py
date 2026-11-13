#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raven_real_learning.py - 渡鴉之證據來源分級稽核引擎（方法論，不針對任何人）
渡鴉「越來越厲害」的真實依據 = 每一則調查論斷是否有可回溯、可獨立查證的來源。
輸入：您提供的論斷檔 JSONL（--findings），每行：
  {"claim": "...", "sources": [{"url": "https://...", "type": "official|media|social|other"}]}
分級（只看來源結構，不判斷論斷真偽）：
  A = 至少 2 個不同網域，且至少 1 個 official（官方/司法/登記機關）
  B = 至少 2 個不同網域，但無 official
  C = 僅 1 個獨立網域（同網域多筆視為同一來源）
  D = 無來源
只有 A 級可作為「已查證事實」呈報；B 為待佐證；C/D 一律標註「未經證實」，不得當事實陳述。
本引擎不蒐集、不查詢任何個人資料。
"""

import sys
import os
import json
import argparse
from datetime import datetime
from urllib.parse import urlparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "raven_provenance_history.jsonl"))


def domain_of(url):
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return ""
    return host[4:] if host.startswith("www.") else host


def grade(finding):
    srcs = [s for s in (finding.get("sources") or []) if domain_of(s.get("url", ""))]
    domains = {domain_of(s["url"]) for s in srcs}
    official = any(s.get("type") == "official" for s in srcs)
    if not domains:
        return "D", "無可回溯來源"
    if len(domains) >= 2 and official:
        return "A", "多個獨立網域且含官方來源"
    if len(domains) >= 2:
        return "B", "多個獨立網域但缺官方來源，待佐證"
    return "C", "僅單一獨立網域，未經交叉查證"


def main():
    ap = argparse.ArgumentParser(description="渡鴉之證據來源分級稽核引擎")
    ap.add_argument("--findings", help="論斷 JSONL 路徑")
    args = ap.parse_args()
    if not args.findings:
        ap.print_help()
        return
    if not os.path.exists(args.findings):
        print(json.dumps({"error": "找不到論斷檔", "path": args.findings}, ensure_ascii=False))
        sys.exit(1)
    rows, bad = [], []
    with open(args.findings, "r", encoding="utf-8-sig") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                fd = json.loads(line)
                g, why = grade(fd)
                rows.append({"line": n, "claim": str(fd.get("claim", ""))[:80], "grade": g, "reason": why})
            except Exception as e:
                bad.append({"line": n, "error": str(e)[:80]})
    tally = {k: sum(1 for r in rows if r["grade"] == k) for k in "ABCD"}
    report = {
        "status": "PROVENANCE_GRADED",
        "graded_at": datetime.now().isoformat(timespec="seconds"),
        "findings_file": args.findings,
        "total": len(rows),
        "tally": tally,
        "reportable_as_verified_fact": [r["line"] for r in rows if r["grade"] == "A"],
        "must_label_unverified": [r["line"] for r in rows if r["grade"] in ("C", "D")],
        "details": rows,
        "parse_errors": bad,
        "limitation": "只評來源結構，不判斷論斷真偽；A 級仍須人工核對來源內容。",
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"graded_at": report["graded_at"], "total": len(rows), "tally": tally},
                           ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
