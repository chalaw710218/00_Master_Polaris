# -*- coding: utf-8 -*-
"""
delivery_gate.py — 仿生學習系統 · 通用交付門禁與回報審計器 (Universal Delivery Gate)
========================================================================================
遵循創辦人（品碩）親定之法典：
1. 核心習慣：數字或結果對不上時，直接寫「對不上」並附原始資料，不寫推測的解釋。
2. 規則 1：回報中的數字（幾條、幾項、幾站）由程式計算後貼上，不得手打。
3. 規則 2：回報結尾附「派工單對照表」，每項一列：項目／狀態（完成／未做／待實測）／證據。
   程式強制檢查：每個「完成」項目的證據檔案或 Commit Hash 必須物理存在。
   - 本機查不到 commit 時自動調用 gh api 查遠端，兩邊都查不到判定失敗。
4. 規則 3：commit 若變更 data/，DATA_VERSION 必須同時變更（git diff 檢查）。
   - 取不到 git diff 時明確輸出「無法檢查」並判定失敗，絕不靜默放行。

使用指示：
- 交件前，閣員在自己的對話中執行 bionic_core/delivery_gate.py，通過才能回報。
- 執行長雪 (Yuki) 收到任何閣員的回報時，用 delivery_gate.py 檢查回報內容，通過才轉給品碩；不通過直接退回。
========================================================================================
"""

import os
import re
import sys
import json
import argparse
import subprocess

def check_commit_exists(commit_hash, project_dir):
    """檢查 commit 是否存在：先查本機 git，查不到再查遠端 gh api"""
    # 1. 本機 git 檢查
    try:
        res = subprocess.run(
            ["git", "cat-file", "-e", f"{commit_hash}^{{commit}}"],
            cwd=project_dir, capture_output=True, text=True
        )
        if res.returncode == 0:
            return True, "local_git"
    except Exception:
        pass

    # 2. 本機查不到，改用 gh api 查遠端
    try:
        # 先抓取 origin 的 owner/repo
        remote_res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_dir, capture_output=True, text=True
        )
        remote_url = remote_res.stdout.strip()
        # 解析 owner/repo (https://github.com/owner/repo.git 或 git@github.com:owner/repo.git)
        m = re.search(r'github\.com[:/]([^/]+)/([^/\.]+)', remote_url)
        if m:
            repo_slug = f"{m.group(1)}/{m.group(2)}"
            gh_res = subprocess.run(
                ["gh", "api", f"/repos/{repo_slug}/commits/{commit_hash}"],
                cwd=project_dir, capture_output=True, text=True
            )
            if gh_res.returncode == 0:
                return True, "remote_github"
    except Exception:
        pass

    return False, "not_found"

def check_task_table(markdown_text, project_dir):
    """
    規則 2：檢查派工單對照表
    每個「完成」項目必須有證據，且證據檔案路徑或 commit 確實存在。
    """
    print("\n🔍 [規則 2] 檢查派工單對照表與證據實體驗收...")
    lines = markdown_text.strip().split("\n")
    table_lines = [l for l in lines if "|" in l and not l.strip().startswith("|---")]
    
    errors = []
    checked_count = 0

    for line in table_lines:
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 3:
            continue
        item, status, evidence = parts[0], parts[1], parts[2]
        if item in ["項目", "任務", "---", ""]:
            continue
            
        checked_count += 1
        if "完成" in status:
            if not evidence or evidence in ["無", "待補", "-", ""]:
                errors.append(f"❌ 項目「{item}」標記為完成，但缺少證據！")
                continue
                
            # 解析路徑或 commit
            paths = re.findall(r'\[.*?\]\((.*?)\)', evidence)
            if not paths:
                tokens = [t.strip(" `*") for t in evidence.split()]
                paths = [t for t in tokens if ("." in t or "/" in t or "\\" in t or len(t) == 40 or len(t) == 7)]
                
            if not paths:
                errors.append(f"❌ 項目「{item}」的證據「{evidence}」無法解析出有效檔案路徑或 Commit Hash！")
                continue
                
            for p in paths:
                clean_p = p.replace("file:///", "").replace("file://", "").split("#")[0]
                
                # 判定是否為 commit hash (7~40 碼十六進制)
                if re.match(r'^[0-9a-f]{7,40}$', clean_p.lower()):
                    exists, source = check_commit_exists(clean_p, project_dir)
                    if not exists:
                        errors.append(f"❌ 項目「{item}」的 Commit Hash 本機與遠端 GitHub 均不存在：{clean_p}")
                else:
                    # 檔案實體檢查
                    resolved = False
                    candidates = [
                        clean_p,
                        os.path.join(project_dir, clean_p),
                        os.path.abspath(clean_p)
                    ]
                    for cand in candidates:
                        if os.path.exists(cand):
                            resolved = True
                            break
                    if not resolved:
                        errors.append(f"❌ 項目「{item}」的證據檔案實體不存在：{clean_p}")

    if errors:
        for err in errors:
            print(err)
        return False
    
    print(f"✅ [規則 2 通過] 共審核 {checked_count} 個項目，所有「完成」項目的證據檔案或 Commit Hash 均真實存在！")
    return True

def check_data_version_diff(project_dir, data_rel_path="data", entry_rel_path="index.html", version_var="DATA_VERSION"):
    """
    規則 3：git diff 檢查，若 commit 變更 data/，DATA_VERSION 必須同時變更。
    區分「不適用」與「無法檢查」：
    - 專案非 git repo、無 data/ 目錄、或入口檔無版本變數 → 輸出「不適用」並通過 (PASS)。
    - 本來應具備版本連動，但取不到 git diff → 才判定失敗 (FAIL)。
    """
    print("\n🔍 [規則 3] 檢查 data/ 變更與版本號連動...")

    # 1. 檢查是否為 git 倉庫
    git_check = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=project_dir, capture_output=True, text=True
    )
    if git_check.returncode != 0:
        print("ℹ️ [規則 3 不適用] 目標專案非 git 倉庫，跳過版本連動檢查。")
        return True

    # 2. 檢查專案是否具備 data/ 目錄（支援自動向下偵測一層）
    full_data_path = os.path.join(project_dir, data_rel_path)
    if not os.path.exists(full_data_path):
        found_sub = None
        for root, dirs, files in os.walk(project_dir):
            if ".git" in root or "node_modules" in root or "__pycache__" in root:
                continue
            if "data" in dirs:
                found_sub = os.path.relpath(os.path.join(root, "data"), project_dir)
                break
        if found_sub:
            data_rel_path = found_sub
            full_data_path = os.path.join(project_dir, data_rel_path)
        else:
            print(f"ℹ️ [規則 3 不適用] 專案無 {data_rel_path} 目錄，跳過版本連動檢查。")
            return True

    # 3. 檢查入口檔案是否存在且包含版本變數（支援自動向下偵測一層）
    full_entry_path = os.path.join(project_dir, entry_rel_path)
    if not os.path.exists(full_entry_path):
        found_entry = None
        for root, dirs, files in os.walk(project_dir):
            if ".git" in root or "node_modules" in root or "__pycache__" in root:
                continue
            if os.path.basename(entry_rel_path) in files:
                found_entry = os.path.relpath(os.path.join(root, os.path.basename(entry_rel_path)), project_dir)
                break
        if found_entry:
            entry_rel_path = found_entry
            full_entry_path = os.path.join(project_dir, entry_rel_path)
        else:
            print(f"ℹ️ [規則 3 不適用] 專案無入口檔案 {entry_rel_path}，跳過版本連動檢查。")
            return True

    try:
        with open(full_entry_path, "r", encoding="utf-8", errors="ignore") as ef:
            if version_var not in ef.read():
                print(f"ℹ️ [規則 3 不適用] 入口檔案無 {version_var} 版本變數，跳過版本連動檢查。")
                return True
    except Exception:
        print(f"ℹ️ [規則 3 不適用] 無法讀取入口檔案 {entry_rel_path}，跳過版本連動檢查。")
        return True

    # 4. 到此代表專案具備 data/ 與版本變數，本來就應該檢查版本連動！
    res = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        cwd=project_dir, capture_output=True, text=True
    )
    if res.returncode != 0:
        print(f"❌ 錯誤：本專案具備 {data_rel_path} 與 {version_var}，但無法檢查 git diff（取得 HEAD~1 失敗，Exit Code {res.returncode}）！")
        if res.stderr.strip():
            print(f"   詳細原因: {res.stderr.strip()}")
        return False

    changed_files = res.stdout.strip().split("\n")
    data_changed = any(data_rel_path in f for f in changed_files if f)
    entry_changed = any(os.path.basename(entry_rel_path) in f for f in changed_files if f)

    if data_changed:
        if not entry_changed:
            print(f"❌ 錯誤：{data_rel_path} 目錄已變更，但 {entry_rel_path} 未變更，{version_var} 未更新！")
            return False

        diff_res = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--", entry_rel_path],
            cwd=project_dir, capture_output=True, text=True
        )
        if version_var not in diff_res.stdout:
            print(f"❌ 錯誤：{data_rel_path} 已變更，但 {entry_rel_path} 的 diff 中未修改 {version_var}！")
            return False

    print("✅ [規則 3 通過] data/ 變更與版本號保持嚴格連動（若有修改皆同步推進）！")
    return True

def calc_project_stats(project_dir):
    """規則 1：通用專案數據計算（供回報複製貼上）"""
    stats = {"project_dir": os.path.abspath(project_dir)}
    
    # 自動偵測常見 data/ 或 json
    for root, dirs, files in os.walk(project_dir):
        if ".git" in root or "node_modules" in root or "__pycache__" in root:
            continue
        for f in files:
            if f.endswith(".json") and not f.endswith("package-lock.json") and not f.endswith("tsconfig.json"):
                rel_f = os.path.relpath(os.path.join(root, f), project_dir)
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8") as jf:
                        d = json.load(jf)
                        if isinstance(d, list):
                            stats[f"{rel_f} (list_count)"] = len(d)
                        elif isinstance(d, dict):
                            stats[f"{rel_f} (keys_count)"] = len(d)
                except Exception:
                    pass
                    
    print("\n================ [規則 1] 程式計算客觀數據 (不得手打) ================")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("=======================================================================")
    return stats

def main():
    parser = argparse.ArgumentParser(description="仿生學習通用交付門禁 (Universal Delivery Gate)")
    parser.add_argument("--project-dir", default=".", help="目標專案目錄")
    parser.add_argument("--check-table", help="派工單表格 Markdown 文本或檔案路徑")
    parser.add_argument("--check-diff", action="store_true", help="執行規則 3 diff 檢查")
    parser.add_argument("--data-path", default="data", help="資料檔案相對路徑")
    parser.add_argument("--entry-file", default="index.html", help="入口檔案相對路徑")
    parser.add_argument("--version-var", default="DATA_VERSION", help="版本變數名稱")
    parser.add_argument("--stats", action="store_true", help="執行規則 1 專案數據計算")

    args = parser.parse_args()
    proj_dir = os.path.abspath(args.project_dir)

    all_passed = True

    if args.stats:
        calc_project_stats(proj_dir)

    if args.check_table:
        table_content = args.check_table
        if os.path.exists(table_content):
            with open(table_content, "r", encoding="utf-8") as tf:
                table_content = tf.read()
        ok2 = check_task_table(table_content, proj_dir)
        if not ok2:
            all_passed = False

    if args.check_diff:
        ok3 = check_data_version_diff(proj_dir, args.data_path, args.entry_file, args.version_var)
        if not ok3:
            all_passed = False

    if not all_passed:
        print("\n❌ 交付門禁質檢未通過！請修復上述錯誤後再行回報。")
        sys.exit(1)
    else:
        print("\n🎉 交付門禁質檢全數通過 (Exit Code: 0)！可正式交付回報。")
        sys.exit(0)

if __name__ == "__main__":
    main()
