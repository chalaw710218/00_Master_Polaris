#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neo_real_learning.py - 尼奧之真實前端資產重量稽核引擎
對您指定的前端目錄做真實量測（--measure <目錄>）：
  - 依副檔名統計檔案數與位元組；文字資產另計 gzip 壓縮後大小
  - 「首屏程式碼」= .js/.mjs/.css 的 gzip 總和，對照您指定的預算（--budget-kb，預設 50）
  - 若目錄內有 package.json，列出 dependencies 中命中『肥大套件清單』者（清單為靜態知識，非量測）
結果寫入歷史 (vaults/neo_weight_history.jsonl)。不連網、不執行目錄內任何程式碼。
注意：這是靜態檔案重量，不是瀏覽器實測的 FCP/LCP/INP；後者需要真實瀏覽器量測。
"""

import sys
import os
import gzip
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
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "neo_weight_history.jsonl"))
TEXT_EXT = {".html", ".css", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".json", ".svg"}
SHIP_EXT = {".js", ".mjs", ".css"}
HEAVY_DEPS = {  # 靜態知識：常見肥大或有輕量替代的套件
    "moment": "改用 Intl.DateTimeFormat / date-fns 單函式匯入",
    "lodash": "改用原生方法或 lodash-es 單函式匯入",
    "jquery": "改用原生 DOM API",
    "axios": "改用原生 fetch",
}
SKIP_DIRS = {"node_modules", ".git", "__pycache__"}
MAX_FILES = 5000


def measure(root):
    by_ext, ship_gz, total_files = {}, 0, 0
    biggest = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            total_files += 1
            if total_files > MAX_FILES:
                return None
            p = os.path.join(dp, fn)
            ext = os.path.splitext(fn)[1].lower()
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            e = by_ext.setdefault(ext or "(none)", {"files": 0, "bytes": 0, "gzip_bytes": 0})
            e["files"] += 1
            e["bytes"] += size
            if ext in TEXT_EXT:
                try:
                    gz = len(gzip.compress(open(p, "rb").read(), 6))
                except OSError:
                    gz = size
                e["gzip_bytes"] += gz
                if ext in SHIP_EXT:
                    ship_gz += gz
            biggest.append((size, os.path.relpath(p, root).replace("\\", "/")))
    biggest.sort(reverse=True)
    return by_ext, ship_gz, total_files, biggest[:5]


def heavy_deps(root):
    pj = os.path.join(root, "package.json")
    if not os.path.exists(pj):
        return None
    try:
        data = json.load(open(pj, encoding="utf-8"))
    except Exception:
        return {"error": "package.json 無法解析"}
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    return [{"package": k, "suggestion": v} for k, v in HEAVY_DEPS.items() if k in deps]


def main():
    ap = argparse.ArgumentParser(description="尼奧之真實前端資產重量稽核引擎")
    ap.add_argument("--measure", help="要量測的前端目錄")
    ap.add_argument("--budget-kb", type=float, default=50.0, help="首屏程式碼 gzip 預算 KB（您指定的參數）")
    args = ap.parse_args()
    if not args.measure:
        ap.print_help()
        return
    root = os.path.abspath(args.measure)
    if not os.path.isdir(root):
        print(json.dumps({"error": "目錄不存在", "path": root}, ensure_ascii=False))
        sys.exit(1)
    res = measure(root)
    if res is None:
        print(json.dumps({"error": "檔案數超過 %d，請指定更小的目錄" % MAX_FILES}, ensure_ascii=False))
        sys.exit(1)
    by_ext, ship_gz, total_files, biggest = res
    ship_kb = round(ship_gz / 1024, 2)
    report = {
        "status": "ASSETS_MEASURED",
        "measured_at": datetime.now().isoformat(timespec="seconds"),
        "root": root,
        "files": total_files,
        "by_extension": by_ext,
        "shipped_code_gzip_kb": ship_kb,
        "budget_kb": args.budget_kb,
        "within_budget": ship_kb <= args.budget_kb,
        "biggest_files": [{"bytes": s, "path": p} for s, p in biggest],
        "heavy_dependencies": heavy_deps(root),
        "limitation": "靜態檔案重量；非瀏覽器實測的 FCP/LCP/INP/CLS。",
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"measured_at": report["measured_at"], "root": root, "files": total_files,
                            "shipped_code_gzip_kb": ship_kb, "within_budget": report["within_budget"]},
                           ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
