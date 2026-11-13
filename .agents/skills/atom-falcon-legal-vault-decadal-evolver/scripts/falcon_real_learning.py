#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
falcon_real_learning.py - 雪柔之法律引用待查證清單引擎
法規網站目前無法連線（見 yuki 引擎 BLOCKERS），因此本引擎只做「能真實完成」的部分：
掃描雪柔四個法律原子的程式碼，以正規表達式抽出所有『法條引用』與『裁判案號』，
逐一列為 UNVERIFIED，產出給雪柔對照官方來源的查核清單。
- 不判斷任何條文內容是否正確；不補全、不改寫任何引用。
- 已被標為【待查證】的案號會單獨計數。
清單寫入 vaults/falcon_citation_worklist.json。
"""

import sys
import os
import re
import glob
import json
import argparse
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(os.path.normpath(os.path.join(HERE, "..", "..", "..")), "skills")
WORKLIST = os.path.normpath(os.path.join(HERE, "..", "vaults", "falcon_citation_worklist.json"))
FALCON_ATOMS = [
    "atom-falcon-statute-legislative-learner",
    "atom-falcon-precedent-caselaw-analyst",
    "atom-falcon-regulatory-moat-architect",
    "atom-falcon-legal-vault-decadal-evolver",
]
ARTICLE_RE = re.compile(r"《([^》]{2,20})》第\s*(\d+)\s*條(?:之\s*(\d+))?(?:第\s*(\d+)\s*[項款])?(?:第\s*(\d+)\s*[項款])?")
CASE_RE = re.compile(r"\d{2,3}\s*年度[^\s，。；、]{1,12}字第\s*\d+\s*號")
PENDING = "【待查證】"


def scan():
    articles, cases, pending = {}, {}, 0
    files = []
    for atom in FALCON_ATOMS:
        files += glob.glob(os.path.join(SKILLS_DIR, atom, "scripts", "*.py"))
        files += glob.glob(os.path.join(SKILLS_DIR, atom, "SKILL.md"))
    for p in sorted(files):
        rel = os.path.relpath(p, SKILLS_DIR).replace("\\", "/")
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for ln, line in enumerate(f, 1):
                pending += line.count(PENDING)
                for m in ARTICLE_RE.finditer(line):
                    key = m.group(0).replace(" ", "")
                    articles.setdefault(key, {"citation": key, "law": m.group(1), "locations": []})["locations"].append(f"{rel}:{ln}")
                for m in CASE_RE.finditer(line):
                    key = m.group(0).replace(" ", "")
                    cases.setdefault(key, {"citation": key, "locations": []})["locations"].append(f"{rel}:{ln}")
    for v in list(articles.values()) + list(cases.values()):
        v["status"] = "UNVERIFIED"
        v["locations"] = v["locations"][:5]
    by_law = {}
    for a in articles.values():
        by_law[a["law"]] = by_law.get(a["law"], 0) + 1
    return {
        "status": "WORKLIST_BUILT",
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "files_scanned": len(files),
        "unique_article_citations": len(articles),
        "unique_case_numbers_in_code": len(cases),
        "pending_markers": pending,
        "articles_by_law": dict(sorted(by_law.items(), key=lambda x: -x[1])),
        "article_citations": sorted(articles.values(), key=lambda x: x["citation"]),
        "case_numbers": sorted(cases.values(), key=lambda x: x["citation"]),
        "next_step": "待全國法規資料庫可連線（或創辦人提供官方 ZIP）後，逐條對照官方條文；裁判案號須至司法院裁判書系統查證。",
        "limitation": "僅抽取引用字串，不驗證其正確性。",
    }


def main():
    ap = argparse.ArgumentParser(description="雪柔之法律引用待查證清單引擎")
    ap.add_argument("--build-worklist", action="store_true")
    args = ap.parse_args()
    if not args.build_worklist:
        ap.print_help()
        return
    rep = scan()
    os.makedirs(os.path.dirname(WORKLIST), exist_ok=True)
    with open(WORKLIST, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print(json.dumps(rep, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
