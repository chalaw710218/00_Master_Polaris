#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
linus_real_learning.py - 林納斯之真實代碼自噬掃描引擎
以 AST 靜態分析 .agents/skills 下全部原子腳本，找出：
  1. 未使用的 import
  2. 定義後從未被引用的函式（排除 main 與 dunder）
只產出「自噬候選清單」，不自動刪除任何程式碼（刪除須經審閱）。
所有數字皆由實際掃描得出。靜態分析有誤報可能（例如動態呼叫），故標示為候選。
"""

import sys
import os
import ast
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
SKILLS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SKILLS_DIR = os.path.join(SKILLS_DIR, "skills")
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "linus_autophagy_history.jsonl"))


def discover():
    found = set()
    for pat in (os.path.join(SKILLS_DIR, "atom-*", "scripts", "*.py"),
                os.path.join(SKILLS_DIR, "atoms", "atom-*", "scripts", "*.py")):
        found.update(glob.glob(pat))
    return sorted(found)


def analyze(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return {"parse_error": str(e)[:120]}
    imported = {}  # name -> lineno
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported[(a.asname or a.name).split(".")[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom) and node.module != "__future__":
            for a in node.names:
                imported[a.asname or a.name] = node.lineno
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    used |= {n.value.id for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    unused_imports = sorted(f"{k}@L{v}" for k, v in imported.items() if k not in used)
    funcs = {n.name: n.lineno for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    unused_funcs = sorted(f"{k}@L{v}" for k, v in funcs.items()
                          if k != "main" and not (k.startswith("__") and k.endswith("__")) and k not in used)
    return {"unused_imports": unused_imports, "unused_functions": unused_funcs,
            "lines": src.count("\n") + 1}


def scan():
    scripts = discover()
    rows = []
    for p in scripts:
        rel = os.path.relpath(p, SKILLS_DIR).replace("\\", "/")
        r = analyze(p)
        r["script"] = rel
        rows.append(r)
    parse_errors = [r for r in rows if "parse_error" in r]
    ok = [r for r in rows if "parse_error" not in r]
    with_imports = [r for r in ok if r["unused_imports"]]
    with_funcs = [r for r in ok if r["unused_functions"]]
    total_unused_imports = sum(len(r["unused_imports"]) for r in ok)
    total_unused_funcs = sum(len(r["unused_functions"]) for r in ok)
    total_lines = sum(r["lines"] for r in ok)
    report = {
        "status": "AUTOPHAGY_SCANNED",
        "scanned_at": datetime.now().isoformat(),
        "scripts_scanned": len(rows),
        "parse_errors": [{"script": r["script"], "error": r["parse_error"]} for r in parse_errors],
        "total_lines": total_lines,
        "unused_imports_total": total_unused_imports,
        "scripts_with_unused_imports": len(with_imports),
        "unused_functions_total": total_unused_funcs,
        "scripts_with_unused_functions": len(with_funcs),
        "top_import_offenders": sorted(
            [{"script": r["script"], "items": r["unused_imports"]} for r in with_imports],
            key=lambda x: len(x["items"]), reverse=True)[:5],
        "unused_function_candidates": [
            {"script": r["script"], "items": r["unused_functions"]} for r in with_funcs][:10],
        "note": "候選清單僅供審閱，未自動刪除任何程式碼；靜態分析可能漏判動態呼叫。",
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({k: report[k] for k in (
            "scanned_at", "scripts_scanned", "total_lines", "unused_imports_total",
            "unused_functions_total")}, ensure_ascii=False) + "\n")
    return report


def main():
    ap = argparse.ArgumentParser(description="林納斯之真實代碼自噬掃描引擎")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--out", help="將完整 JSON 報告直接以 UTF-8 寫入此檔（避開 shell 轉碼）")
    args = ap.parse_args()
    if not args.scan:
        ap.print_help()
        return
    report = scan()
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(json.dumps({"status": report["status"], "written_to": args.out}))
    else:
        print(text)


if __name__ == "__main__":
    main()
