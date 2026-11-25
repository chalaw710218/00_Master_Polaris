#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deming_real_learning.py - 戴明之真實品質稽核與統計製程管制引擎
對 .agents/skills/atom-*/scripts/*.py 逐一做兩項真實檢查：
  1. py_compile 語法編譯
  2. `python <script> --help` 實際執行（不觸發業務副作用），記錄 Exit Code 與耗時
每次稽核寫入歷史 (vaults/deming_quality_history.jsonl)；累積 >= 5 次後才計算 p 管制圖，
未達樣本數時明確標示「樣本不足」，不下統計結論。
注意：--help 僅證明「可載入、可解析參數」，不等於功能正確。
"""

import sys
import os
import glob
import json
import math
import time
import argparse
import subprocess
import py_compile
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))  # .agents/skills 的上一層即 .agents
SKILLS_DIR = os.path.join(SKILLS_DIR, "skills")
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "deming_quality_history.jsonl"))
MIN_RUNS_FOR_PCHART = 5
TIMEOUT_S = 90


def discover():
    # 原子分散兩處：頂層 skills/atom-*（後期梯隊）與 skills/atoms/atom-*（早期梯隊）
    patterns = [
        os.path.join(SKILLS_DIR, "atom-*", "scripts", "*.py"),
        os.path.join(SKILLS_DIR, "atoms", "atom-*", "scripts", "*.py"),
    ]
    found = set()
    for pat in patterns:
        found.update(glob.glob(pat))
    return sorted(found)


def check_one(path):
    rel = os.path.relpath(path, SKILLS_DIR).replace("\\", "/")
    result = {"script": rel, "compile_ok": False, "help_exit": None, "seconds": None, "error": ""}
    try:
        py_compile.compile(path, doraise=True)
        result["compile_ok"] = True
    except py_compile.PyCompileError as e:
        result["error"] = "compile: " + str(e).strip()[:200]
        return result
    t0 = time.time()
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        p = subprocess.run([sys.executable, path, "--help"], capture_output=True,
                           timeout=TIMEOUT_S, env=env)
        result["help_exit"] = p.returncode
        if p.returncode != 0:
            result["error"] = (p.stderr.decode("utf-8", "replace").strip().splitlines() or [""])[-1][:200]
    except subprocess.TimeoutExpired:
        result["error"] = "timeout>%ds" % TIMEOUT_S
    result["seconds"] = round(time.time() - t0, 2)
    return result


def p_chart(history):
    """以歷次不合格比例畫 p 管制圖（常態近似 3 sigma）。"""
    if len(history) < MIN_RUNS_FOR_PCHART:
        return {"status": "樣本不足", "runs": len(history), "need": MIN_RUNS_FOR_PCHART}
    ps = [h["defects"] / h["total"] for h in history if h["total"]]
    n_bar = sum(h["total"] for h in history) / len(history)
    p_bar = sum(h["defects"] for h in history) / sum(h["total"] for h in history)
    sigma = math.sqrt(p_bar * (1 - p_bar) / n_bar)
    ucl, lcl = p_bar + 3 * sigma, max(0.0, p_bar - 3 * sigma)
    latest = ps[-1]
    return {
        "status": "OUT_OF_CONTROL(特殊變異，需追查根因)" if (latest > ucl or latest < lcl) else "IN_CONTROL(常態變異，勿瞎折騰)",
        "p_bar": round(p_bar, 4), "UCL": round(ucl, 4), "LCL": round(lcl, 4), "latest_p": round(latest, 4),
    }


def audit(workers):
    scripts = discover()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(check_one, scripts))
    failures = [r for r in results if not r["compile_ok"] or r["help_exit"] != 0]
    run = {
        "audited_at": datetime.now().isoformat(),
        "total": len(results),
        "defects": len(failures),
        "passed": len(results) - len(failures),
        "failures": failures,
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(run, ensure_ascii=False) + "\n")
    history = []
    with open(HISTORY, "r", encoding="utf-8") as f:
        history = [json.loads(l) for l in f if l.strip()]
    slow = sorted([r for r in results if r["seconds"]], key=lambda r: r["seconds"], reverse=True)[:3]
    return {
        "status": "AUDITED",
        "scripts_checked": run["total"],
        "passed": run["passed"],
        "defects": run["defects"],
        "failures": failures,
        "slowest_3": [{"script": r["script"], "seconds": r["seconds"]} for r in slow],
        "p_chart": p_chart(history),
        "limitation": "--help 只證明可載入與參數解析，不證明功能正確；SPC 需累積多次稽核才有意義。",
        "history_file": HISTORY,
    }


def main():
    ap = argparse.ArgumentParser(description="戴明之真實品質稽核與 SPC 引擎")
    ap.add_argument("--audit", action="store_true", help="稽核所有 atom 腳本並寫入歷史")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    if not args.audit:
        ap.print_help()
        return
    print(json.dumps(audit(args.workers), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
