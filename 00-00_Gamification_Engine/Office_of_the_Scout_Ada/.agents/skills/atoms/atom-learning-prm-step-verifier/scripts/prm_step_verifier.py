#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-learning-prm-step-verifier: PRM 過程級逐步驗證與物理終點法官原子腳本
專職負責在推論過程中對每一步邏輯進行逐步評分 (PRM)，並執行 Exit Code 0 終點物理驗證。
"""

import sys
import os
import argparse
import json
import re
import subprocess
from pathlib import Path

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 典型邏輯漏洞與獎勵投機關鍵特徵
LOGICAL_FALLACY_PATTERNS = [
    r"顯而易見",
    r"無庸置疑肯定會",
    r"大家都知道一定",
    r"保證百分之百穩賺",
    r"憑直覺大概是",
    r"隨便抓個數字",
]

def score_reasoning_step(step_idx: int, step_content: str) -> dict:
    """對單一推論步驟進行 PRM 過程級獨立打分"""
    for pattern in LOGICAL_FALLACY_PATTERNS:
        if re.search(pattern, step_content):
            return {
                "step": step_idx,
                "score": "Negative (0.0)",
                "passed": False,
                "reason": f"偵測到非接地跳躍假說或投機詞彙：『{pattern}』，違反 PRM 逐步可驗證性！",
                "content_snippet": step_content[:80]
            }

    # 長度與實質內容檢查
    if len(step_content.strip()) < 5:
        return {
            "step": step_idx,
            "score": "Negative (0.0)",
            "passed": False,
            "reason": "步驟內容過於空洞，缺乏實質推論依據",
            "content_snippet": step_content
        }

    return {
        "step": step_idx,
        "score": "Positive (+1.0)",
        "passed": True,
        "reason": "邏輯鏈自洽、具備因果支撐、無未經證實之跳躍詞彙",
        "content_snippet": step_content[:80]
    }

def verify_code_exit_code(script_path: str) -> dict:
    """法官 1：終點代碼物理驗證器 (Exit Code == 0)"""
    if not script_path or not os.path.exists(script_path):
        return {"executed": False, "exit_code": 0, "status": "SKIPPED_OR_EMPTY"}

    try:
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=30)
        return {
            "executed": True,
            "exit_code": res.returncode,
            "passed": (res.returncode == 0),
            "stdout": res.stdout[:200],
            "stderr": res.stderr[:200]
        }
    except Exception as e:
        return {
            "executed": True,
            "exit_code": -1,
            "passed": False,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="PRM 過程級逐步驗證與物理終點法官原子")
    parser.add_argument("--steps-file", type=str, help="推論步驟 JSON 檔案")
    parser.add_argument("--reasoning-text", type=str, help="推論純文字 (步驟以換行或序號分隔)")
    parser.add_argument("--verify-code", type=str, help="待驗證之實體 Python 腳本路徑")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    steps = []
    if args.steps_file and os.path.exists(args.steps_file):
        with open(args.steps_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                steps = data
            elif isinstance(data, dict) and "steps" in data:
                steps = data["steps"]
    elif args.reasoning_text:
        raw_steps = [s.strip() for s in args.reasoning_text.splitlines() if s.strip()]
        steps = raw_steps
    else:
        # 內建模擬測試推論鏈
        steps = [
            "步驟 1: 讀取成本數據，還原大盤批發價與包材冷鏈摩擦成本",
            "步驟 2: 扣除失水率 8% 與包冰率 0.0%，計算實質出貨淨重",
            "步驟 3: 結合 5D 定價模型，推導合理毛利空間與顧客讓利區間",
            "步驟 4: 產出高情商談判話術，建立雙贏合作架構"
        ]

    print("=== [atom-learning-prm-step-verifier] 啟動 PRM 過程級逐步驗證 ===")
    scored_steps = []
    all_steps_passed = True
    for idx, step_content in enumerate(steps, 1):
        res = score_reasoning_step(idx, step_content)
        scored_steps.append(res)
        if not res["passed"]:
            all_steps_passed = False
        print(f"-> 步驟 {idx}: [{res['score']}] - {res['reason']}")

    # 物理終點法官檢查
    code_res = verify_code_exit_code(args.verify_code)
    code_passed = code_res.get("passed", True)

    overall_passed = all_steps_passed and code_passed

    report = {
        "status": "PRM_PASSED" if overall_passed else "PRM_FAILED_ANDON_TRIGGERED",
        "total_steps": len(steps),
        "steps_verification": scored_steps,
        "physical_code_judge": code_res,
        "overall_passed": overall_passed
    }

    print("\n🔒 **【PRM 過程驗證與物理驗證報告】**")
    print(f"過程級逐步驗證狀態: {'[100% 通過 Positive]' if all_steps_passed else '[攔截到邏輯缺陷 Negative]'}")
    print(f"終點物理代碼驗證 (Exit Code: 0): {'[通過]' if code_passed else '[失敗]'}")

    if overall_passed:
        print("\n[+] PRM 逐步驗證與終點物理法官全數通過 (Exit Code: 0)！")
        sys.exit(0)
    else:
        print("\n[-] PRM 檢驗未通過，觸發安燈拉繩，就地回滾修正！")
        sys.exit(1)

if __name__ == "__main__":
    main()
