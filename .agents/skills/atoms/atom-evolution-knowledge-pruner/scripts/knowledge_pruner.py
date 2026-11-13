#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-evolution-knowledge-pruner: 仿生探索與死知識殘酷自噬修剪原子腳本
專職負責掃描、識別與自噬修剪過期死知識、重複冗餘與未驗證廢棄假設。
"""

import sys
import os
import argparse
import re
import json
from pathlib import Path
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 典型死知識與未落地 AI 腔特徵詞庫
DEAD_KNOWLEDGE_PATTERNS = [
    r"\[待確認\]",
    r"\[未經證實\]",
    r"未來可能考慮",
    r"或許可以嘗試",
    r"待創辦人指示是否要",
    r"TODO: 待辦未清",
    r"deprecated",
    r"已過期廢棄",
]

def scan_file_for_dead_knowledge(file_path: Path, custom_pattern: str = None) -> dict:
    """掃描單一檔案中的死知識與冗餘片段"""
    try:
        text = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"file": str(file_path), "error": str(e), "matches": [], "line_count": 0}

    lines = text.splitlines()
    patterns = list(DEAD_KNOWLEDGE_PATTERNS)
    if custom_pattern:
        patterns.append(custom_pattern)

    combined_regex = re.compile("|".join(f"({p})" for p in patterns), re.IGNORECASE)
    
    matches = []
    for idx, line in enumerate(lines, 1):
        if combined_regex.search(line):
            matches.append({
                "line": idx,
                "content": line.strip()[:100]
            })

    return {
        "file": str(file_path),
        "total_lines": len(lines),
        "dead_knowledge_count": len(matches),
        "matches": matches
    }

def prune_dead_knowledge(file_path: Path, custom_pattern: str = None, dry_run: bool = True) -> dict:
    """執行溶酶體殘酷自噬修剪"""
    scan_result = scan_file_for_dead_knowledge(file_path, custom_pattern)
    if scan_result.get("error"):
        return scan_result

    if scan_result["dead_knowledge_count"] == 0:
        return {"file": str(file_path), "status": "CLEAN", "pruned_count": 0}

    lines = file_path.read_text(encoding='utf-8').splitlines()
    patterns = list(DEAD_KNOWLEDGE_PATTERNS)
    if custom_pattern:
        patterns.append(custom_pattern)
    combined_regex = re.compile("|".join(f"({p})" for p in patterns), re.IGNORECASE)

    retained_lines = []
    pruned_lines = []

    for idx, line in enumerate(lines, 1):
        if combined_regex.search(line):
            pruned_lines.append((idx, line))
        else:
            retained_lines.append(line)

    if not dry_run:
        # 寫回修剪後的純淨檔案
        file_path.write_text("\n".join(retained_lines) + "\n", encoding='utf-8')
        status = "PRUNED_SUCCESS"
    else:
        status = "DRY_RUN_DETECTED"

    return {
        "file": str(file_path),
        "status": status,
        "original_lines": len(lines),
        "retained_lines": len(retained_lines),
        "pruned_count": len(pruned_lines),
        "pruned_sample": [p[1].strip()[:80] for p in pruned_lines[:5]]
    }

def main():
    parser = argparse.ArgumentParser(description="仿生探索與死知識殘酷自噬修剪原子")
    parser.add_argument("--target-dir", type=str, help="掃描並修剪之資料夾")
    parser.add_argument("--file-path", type=str, help="指定掃描並修剪之單一檔案")
    parser.add_argument("--dead-axiom-pattern", type=str, default=None, help="自定義死知識特徵正則")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式，不實體修改")
    parser.add_argument("--execute-prune", action="store_true", default=False, help="正式執行物理修剪")

    args = parser.parse_args()

    # 預設為 dry_run
    dry_run = not args.execute_prune

    targets = []
    if args.file_path:
        p = Path(args.file_path)
        if p.exists() and p.is_file():
            targets.append(p)
        else:
            print(f"[-] 錯誤：找不到指定檔案 {args.file_path}")
            sys.exit(1)
    elif args.target_dir:
        d = Path(args.target_dir)
        if d.exists() and d.is_dir():
            targets.extend(list(d.glob("*.md")))
        else:
            print(f"[-] 錯誤：找不到指定資料夾 {args.target_dir}")
            sys.exit(1)
    else:
        # 若未指定，預設對當前工作區系統根檔案做無害掃描測試
        sample_path = Path("00-00_Gamification_Engine/00-00_Skills_Specialization_Master_Plan.md")
        if sample_path.exists():
            targets.append(sample_path)
        else:
            print("[*] 請指定 --file-path 或 --target-dir。")
            sys.exit(0)

    print(f"=== [atom-evolution-knowledge-pruner] 啟動溶酶體自噬掃描 ===")
    print(f"模式: {'[DRY-RUN 預演]' if dry_run else '[EXECUTE 實體修剪]'}")
    print(f"目標檔案數: {len(targets)}")

    results = []
    total_pruned = 0
    for t in targets:
        res = prune_dead_knowledge(t, args.dead_axiom_pattern, dry_run=dry_run)
        results.append(res)
        total_pruned += res.get("pruned_count", 0)
        print(f"-> 檔案: {t.name} | 狀態: {res.get('status')} | 偵測死知識: {res.get('pruned_count', 0)} 行")

    print(f"\n[+] 掃描完畢！共審查 {len(targets)} 個檔案，識別並處理 {total_pruned} 處冗餘/死知識。")
    sys.exit(0)

if __name__ == "__main__":
    main()
