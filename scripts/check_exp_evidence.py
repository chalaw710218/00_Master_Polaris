import csv
import os
import re
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
ORIG_FILE = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log" / "01_Experiences_and_Evidence.md"


def is_git_repo(root: Path) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=root,
            capture_output=True,
            text=True
        )
        return r.returncode == 0 and r.stdout.strip() == "true"
    except Exception:
        return False


def check_commit(commit_hash: str, root: Path, git_ok: bool) -> tuple:
    if not git_ok:
        return "無法檢查", "非 git 倉庫或無 git 指令"

    # 本機 git cat-file -e
    try:
        r = subprocess.run(
            ["git", "cat-file", "-e", commit_hash],
            cwd=root,
            capture_output=True,
            text=True
        )
        if r.returncode == 0:
            return "存在", "本機 git commit 存在"
    except Exception as e:
        return "無法檢查", f"執行 git 失敗: {e}"

    # 本機查不到時改用 gh api
    try:
        r = subprocess.run(
            ["gh", "api", f"repos/:owner/:repo/commits/{commit_hash}"],
            cwd=root,
            capture_output=True,
            text=True
        )
        if r.returncode == 0:
            return "存在", "GitHub 遠端 commit 存在"
    except Exception:
        pass

    return "不存在", "本機與遠端皆查無此 commit"


def find_file(target_str: str, root: Path) -> tuple:
    # 優先直接路徑判斷
    p = root / target_str
    if p.is_file():
        return "存在", str(p.resolve())

    # 全域搜尋（包含 .agents 等隱藏目錄，但略過 .git）
    target_norm = target_str.replace("\\", "/").rstrip("/")
    target_name = Path(target_norm).name

    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for fn in filenames:
            full = Path(dirpath) / fn
            rel = full.relative_to(root).as_posix()
            if rel == target_norm or rel.endswith("/" + target_norm) or fn == target_norm:
                matches.append(full.resolve())

    if matches:
        return "存在", str(matches[0])

    return "不存在", ""


def parse_exp_entries(text: str):
    pattern = re.compile(r"^(?:## |### |\d+\.\s*\*\*第)", re.MULTILINE)
    matches = list(pattern.finditer(text))

    entries = {}
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entry_text = text[start:end]
        seq = i + 1
        if seq in (5, 6, 7, 8):
            entries[seq] = entry_text

    return entries


def main():
    if not ORIG_FILE.is_file():
        print(f"錯誤：找不到原檔 {ORIG_FILE}", file=sys.stderr)
        sys.exit(1)

    text = ORIG_FILE.read_text(encoding="utf-8")
    entries = parse_exp_entries(text)

    git_ok = is_git_repo(PROJECT_ROOT)

    results = []  # list of (seq, evidence_desc, status, path_or_info)
    entry_status = {}  # seq -> bool (True if all evidences exist)

    for seq in (5, 6, 7, 8):
        entry_text = entries.get(seq, "")
        entry_status[seq] = True

        # 抓取 commit hash
        commits = re.findall(r"(?i)commit\s*[`'\"]?([0-9a-fA-F]{7,40})", entry_text)
        commits = list(dict.fromkeys(commits))

        # 抓取反引號檔案
        raw_backticks = re.findall(r"`([^`]+)`", entry_text)
        files = []
        for b in raw_backticks:
            b = b.strip()
            if b in commits:
                continue
            if b.endswith("/"):
                continue
            if b.endswith((".md", ".json", ".py", ".txt", "/SKILL.md")) or "/" in b or b.startswith("."):
                # 過濾非檔案字串（如 git rm -r --cached）
                if not b.startswith("git "):
                    files.append(b)
        files = list(dict.fromkeys(files))

        # 逐項檢查 commit
        for c in commits:
            status, info = check_commit(c, PROJECT_ROOT, git_ok)
            results.append((seq, f"commit {c}", status, info))
            if status != "存在":
                entry_status[seq] = False

        # 逐項檢查檔案
        for f in files:
            status, path_str = find_file(f, PROJECT_ROOT)
            results.append((seq, f, status, path_str))
            if status != "存在":
                entry_status[seq] = False

    # 印出表格
    print("序號 | 證據 | 狀態 | 完整路徑 / 說明")
    print("-" * 80)
    for seq, ev, st, info in results:
        print(f"{seq} | {ev} | {st} | {info}")

    # 輸出 _exp_evidence.csv
    exp_csv_path = ORIG_FILE.parent / "_exp_evidence.csv"
    with open(exp_csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["序號", "證據", "狀態", "完整路徑"])
        for seq, ev, st, info in results:
            writer.writerow([seq, ev, st, info])

    # 統計結果
    all_exist_count = sum(1 for seq in (5, 6, 7, 8) if entry_status[seq])
    missing_count = 4 - all_exist_count

    print("=" * 80)
    print(f"4 條中「證據全部存在」: {all_exist_count} 條")
    print(f"「有缺」: {missing_count} 條")
    print("=" * 80)

    if missing_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
