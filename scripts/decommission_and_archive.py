import os
import shutil
import hashlib
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    # 1. 搜尋提到 initialize_daughter_skills 的檔案
    cmd = ["git", "grep", "-l", "initialize_daughter_skills"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    
    raw_files = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    filtered_files = []
    for f in raw_files:
        if "_archive" in f or "_master_history" in f or "_未驗證封存" in f:
            continue
        filtered_files.append(f)
        
    print("=== 提到 initialize_daughter_skills 的檔案搜尋 ===")
    print(f"搜尋到的數量: {len(filtered_files)}")
    for f in filtered_files:
        print(f"  - {f}")
    print()

    # 改名 00-00_Gamification_Engine/initialize_daughter_skills.py
    old_script = PROJECT_ROOT / "00-00_Gamification_Engine" / "initialize_daughter_skills.py"
    new_script = PROJECT_ROOT / "00-00_Gamification_Engine" / "initialize_daughter_skills_停用_20261120.py"
    note_file = PROJECT_ROOT / "00-00_Gamification_Engine" / "initialize_daughter_skills_停用說明.txt"
    
    if old_script.exists():
        shutil.move(str(old_script), str(new_script))
        
    note_content = "2026-11-20 品碩決定停用：此程式會重寫所有閣員子版，覆蓋已整理的內容。\n"
    note_file.write_text(note_content, encoding="utf-8")
    
    old_script_not_exists = not old_script.exists()
    new_script_exists = new_script.exists()
    
    # 2. 移走重複的子版
    office_yuki = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "bionic-learning-yuki.md"
    archive_dir = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_yuki = archive_dir / "bionic-learning-yuki_辦公室副本_20261120.md"
    
    copy_sha_match = False
    office_yuki_not_exists = False
    
    if office_yuki.exists():
        with open(office_yuki, "rb") as f:
            orig_bytes = f.read()
        orig_sha = hashlib.sha256(orig_bytes).hexdigest()
        
        shutil.copy2(str(office_yuki), str(archive_yuki))
        
        with open(archive_yuki, "rb") as f:
            bak_bytes = f.read()
        bak_sha = hashlib.sha256(bak_bytes).hexdigest()
        
        if orig_sha == bak_sha:
            copy_sha_match = True
            os.remove(str(office_yuki))
            office_yuki_not_exists = not office_yuki.exists()
    else:
        # 已移走的情況
        if archive_yuki.exists():
            copy_sha_match = True
            office_yuki_not_exists = True

    # 3. .agents 的 SKILL.md sha256 前 16 碼
    active_skill = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-yuki" / "SKILL.md"
    with open(active_skill, "rb") as f:
        skill_bytes = f.read()
    active_sha = hashlib.sha256(skill_bytes).hexdigest()
    active_sha_16 = active_sha[:16]
    
    # 印出檢查結果
    print("=== 執行結果驗證 ===")
    print(f"舊程式原檔名是否已不存在: {'是' if old_script_not_exists else '否'}")
    print(f"舊程式新檔名是否存在: {'是' if new_script_exists else '否'}")
    print(f"辦公室副本備份 sha256 是否相同: {'是' if copy_sha_match else '否'}")
    print(f"辦公室副本原位置是否已不存在: {'是' if office_yuki_not_exists else '否'}")
    print(f".agents 的 SKILL.md sha256 前 16 碼: {active_sha_16} (完整: {active_sha})")
    
    if old_script_not_exists and new_script_exists and copy_sha_match and office_yuki_not_exists:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
