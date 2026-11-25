# -*- coding: utf-8 -*-
"""
scripts/execute_step6_cleanup.py
執行副本清理與單一真理源 (SSOT) 治理：
1. 備份 C:\\Users\\lenovo\\.gemini\\config\\skills\\ 至 00_Master_Polaris/_archive/gemini_global_skills_20261126/ 並脫敏金鑰
2. 清理 C:\\Users\\lenovo\\.gemini\\config\\skills\\ 內 7 個技能目錄
3. 將 00-02_GroupBuy_Products/.agents/skills/sharp-groupbuy-analyzer 搬進根目錄 .agents/skills/
4. 備份 00-02_GroupBuy_Products/.agents 至 00-02_GroupBuy_Products/_archive/agents_backup_20261126/ 並脫敏
5. 刪除 00-02_GroupBuy_Products/.agents 實體目錄，建立指向根目錄 .agents 的 Junction
6. 驗證 00-02 跨聯結路徑讀取
"""

import os
import re
import stat
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(".").resolve()
ROOT_AGENTS = BASE_DIR / ".agents"
ROOT_SKILLS = ROOT_AGENTS / "skills"

GLOBAL_SKILLS_DIR = Path("C:/Users/lenovo/.gemini/config/skills")
GLOBAL_BACKUP_DIR = BASE_DIR / "_archive" / "gemini_global_skills_20261126"

GB_DIR = BASE_DIR / "00-02_GroupBuy_Products"
GB_AGENTS = GB_DIR / ".agents"
GB_BACKUP_DIR = GB_DIR / "_archive" / "agents_backup_20261126"

TOKEN_PATTERN = re.compile(r"EAA[0-9a-zA-Z]{30,}")

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

print("=" * 70)
print("📦【第一階段：備份與清理全域配置 C:\\Users\\lenovo\\.gemini\\config\\skills\\】")
print("=" * 70)

# 1. 備份全域 skills 目錄
if GLOBAL_SKILLS_DIR.exists():
    if GLOBAL_BACKUP_DIR.exists():
        shutil.rmtree(GLOBAL_BACKUP_DIR, onerror=remove_readonly)
    shutil.copytree(GLOBAL_SKILLS_DIR, GLOBAL_BACKUP_DIR)
    print(f"✅ 已完整備份全域技能至: {GLOBAL_BACKUP_DIR}")

    # 脫敏備份檔
    sanitized_count = 0
    for root, dirs, files in os.walk(GLOBAL_BACKUP_DIR):
        for f in files:
            p = Path(root) / f
            try:
                text = p.read_text(encoding="utf-8")
                if TOKEN_PATTERN.search(text):
                    clean_text = TOKEN_PATTERN.sub("[REDACTED_FB_PAGE_TOKEN]", text)
                    p.write_text(clean_text, encoding="utf-8")
                    sanitized_count += 1
            except Exception:
                pass
    print(f"🔒 備份檔金鑰脫敏完成，處理了 {sanitized_count} 份含有金鑰之檔案。")

    # 2. 清理全域 7 個目錄
    targets_to_remove = [
        "ai-pricing-auditor",
        "daily-closing-sop",
        "facebook-publisher",
        "one-shot-photo-marketer",
        "persona-reverse-engineer",
        "rea-reverse-engineer",
        "sharp-groupbuy-analyzer"
    ]
    for name in targets_to_remove:
        sub_dir = GLOBAL_SKILLS_DIR / name
        if sub_dir.exists():
            shutil.rmtree(sub_dir, onerror=remove_readonly)
            print(f"  🗑️ 已自全域移除: {name}")

    remaining = list(GLOBAL_SKILLS_DIR.iterdir())
    print(f"📊 全域 skills 資料夾清理後殘留項目數: {len(remaining)}")
    for r in remaining:
        print(f"   殘留: {r.name}")
else:
    print("⚠️ 全域 skills 目錄不存在，略過清理。")

print("\n" + "=" * 70)
print("📦【第二階段：00-02 sharp-groupbuy-analyzer 遷移與 Junction 建立】")
print("=" * 70)

# 3. 將 sharp-groupbuy-analyzer 搬進根目錄 .agents/skills/
gb_sharp_src = GB_AGENTS / "skills" / "sharp-groupbuy-analyzer"
root_sharp_dst = ROOT_SKILLS / "sharp-groupbuy-analyzer"

if gb_sharp_src.exists():
    if root_sharp_dst.exists():
        shutil.rmtree(root_sharp_dst, onerror=remove_readonly)
    shutil.copytree(gb_sharp_src, root_sharp_dst)
    print(f"✅ 已將 sharp-groupbuy-analyzer 複製至根目錄: {root_sharp_dst}")
else:
    print(f"⚠️ 找不到 00-02 中的 sharp-groupbuy-analyzer: {gb_sharp_src}")

# 4. 備份 00-02/.agents
GB_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
backup_target = GB_BACKUP_DIR / "agents_original"
if backup_target.exists():
    shutil.rmtree(backup_target, onerror=remove_readonly)
shutil.copytree(GB_AGENTS, backup_target)
print(f"✅ 已將 00-02/.agents 備份至: {backup_target}")

# 脫敏 00-02 備份檔
gb_sanitized = 0
for root, dirs, files in os.walk(backup_target):
    for f in files:
        p = Path(root) / f
        try:
            text = p.read_text(encoding="utf-8")
            if TOKEN_PATTERN.search(text):
                clean_text = TOKEN_PATTERN.sub("[REDACTED_FB_PAGE_TOKEN]", text)
                p.write_text(clean_text, encoding="utf-8")
                gb_sanitized += 1
        except Exception:
            pass
print(f"🔒 00-02 備份檔金鑰脫敏完成，處理了 {gb_sanitized} 份含有金鑰之檔案。")

# 5. 刪除 00-02/.agents 實體目錄，建立 Junction
shutil.rmtree(GB_AGENTS, onerror=remove_readonly)
print("🗑️ 已移除 00-02/.agents 實體目錄。")

# 呼叫 cmd 建立 Junction
junction_cmd = f'cmd /c mklink /J "{GB_AGENTS}" "{ROOT_AGENTS}"'
print(f"執行 Junction 指令: {junction_cmd}")
res = subprocess.run(junction_cmd, capture_output=True, text=True, shell=True)
print("命令輸出:", res.stdout.strip())
if res.returncode != 0:
    print("❌ Junction 建立失敗:", res.stderr.strip())
else:
    print("🎉 Junction 建立成功！")

# 6. 驗證 00-02 跨聯結路徑讀取
print("\n" + "=" * 70)
print("🔍【第三階段：驗證 00-02 跨聯結讀取能力】")
print("=" * 70)

check_paths = [
    GB_AGENTS / "skills" / "facebook-publisher" / "SKILL.md",
    GB_AGENTS / "skills" / "sharp-groupbuy-analyzer" / "SKILL.md"
]

all_readable = True
for cp in check_paths:
    if cp.exists():
        lines = len(cp.read_text(encoding="utf-8").splitlines())
        print(f"✅ 成功跨聯結讀取: {cp.relative_to(BASE_DIR)} ({lines} 行)")
    else:
        print(f"❌ 無法讀取: {cp}")
        all_readable = False

if all_readable:
    print("🎯 00-02 透過 Junction 正常讀取全域單一正本技能，驗證通過！")
else:
    print("❌ 跨聯結驗證未通過！")
