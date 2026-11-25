#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step4_cleaner.py
================
第 4 步：清理與歸檔執行器（只搬不刪，__pycache__ 例外，全動作可復原）
"""

import os
import shutil
import sys
from pathlib import Path

# 設定標準輸出編碼為 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

def main():
    moved_records = []

    # -------------------------------------------------------------
    # 【二、編碼轉換 (UTF-16 -> UTF-8)】
    # 原檔先複製一份到同層 _archive/，檔名加上 _utf16原檔，再把原位置轉成 UTF-8
    # -------------------------------------------------------------
    targets_utf16 = [
        ROOT / "00-00_Gamification_Engine/Office_of_the_Scout_Ada/01_Cognitive_Log/學習帳本.txt",
        ROOT / "00-03_Brand_LifeButler/00-03-08_Productized_Services/02_外圈代倒垃圾包月_999與1999/05_Trash_Radar_Engine/evidence/scenarios_verification_output.txt"
    ]

    for p in targets_utf16:
        if p.exists():
            archive_dir = p.parent / "_archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            backup_name = f"{p.stem}_utf16原檔{p.suffix}"
            backup_path = archive_dir / backup_name

            # 檢查是否已為 UTF-8
            try:
                p.read_text(encoding="utf-8")
                # 已是 UTF-8，無需重複轉換
                continue
            except UnicodeDecodeError:
                pass

            # 複製原始 byte 備份
            if not backup_path.exists():
                shutil.copy2(p, backup_path)
            
            # 讀取 UTF-16 並寫回 UTF-8 (不帶 BOM)
            content = p.read_text(encoding="utf-16")
            p.write_text(content, encoding="utf-8")

            rel_orig = p.relative_to(ROOT)
            rel_bak = backup_path.relative_to(ROOT)
            moved_records.append((f"[編碼轉換] {rel_orig} (原檔備份)", str(rel_bak)))

    # -------------------------------------------------------------
    # 【三、舊版檔歸檔】
    # -------------------------------------------------------------
    legacy_skills = [
        (
            ROOT / ".agents/skills/bionic-learning-linus/SKILL_備份_20261122.md",
            ROOT / ".agents/skills/bionic-learning-linus/_archive/SKILL_備份_20261122.md"
        ),
        (
            ROOT / "00-00_Gamification_Engine/Office_of_the_Scout_Ada/01_Cognitive_Log/_未驗證封存/SKILL_ada_舊版.md",
            ROOT / "00-00_Gamification_Engine/Office_of_the_Scout_Ada/01_Cognitive_Log/_未驗證封存/_archive/SKILL_ada_舊版.md"
        )
    ]

    for src, dst in legacy_skills:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            moved_records.append((f"[舊版歸檔] {src.relative_to(ROOT)}", str(dst.relative_to(ROOT))))

    # -------------------------------------------------------------
    # 【四、備份檔 .bak 移到同層 _archive/】
    # -------------------------------------------------------------
    bak_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirnames:
            dirnames.remove(".git")
        if "office_of_the_scout_ada/.agents/skills" in Path(dirpath).as_posix().lower():
            continue
        # 排除已在 _archive 中的
        if "_archive" in Path(dirpath).as_posix().lower() or "_master_history" in Path(dirpath).as_posix().lower():
            continue
        for f in filenames:
            if ".bak" in f:
                bak_files.append(Path(dirpath) / f)

    for b in bak_files:
        archive_dir = b.parent / "_archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        dst = archive_dir / b.name
        shutil.move(b, dst)
        moved_records.append((f"[.bak 歸檔] {b.relative_to(ROOT)}", str(dst.relative_to(ROOT))))

    # -------------------------------------------------------------
    # 【四-2、刪除 __pycache__ 和 .pyc】
    # -------------------------------------------------------------
    import stat

    def remove_readonly(func, path, excinfo):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass

    deleted_pyc = 0
    deleted_pycache = 0

    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
        if ".git" in dirpath:
            continue
        if "office_of_the_scout_ada/.agents/skills" in Path(dirpath).as_posix().lower():
            continue

        for f in filenames:
            if f.endswith(".pyc"):
                p = Path(dirpath) / f
                try:
                    os.chmod(p, stat.S_IWRITE)
                    p.unlink()
                    deleted_pyc += 1
                except Exception:
                    pass

        for d in dirnames:
            if d == "__pycache__":
                p = Path(dirpath) / d
                try:
                    shutil.rmtree(p, onerror=remove_readonly)
                    deleted_pycache += 1
                except Exception:
                    pass

    print("=" * 70)
    print("🧹 第 4 步清理與歸檔完成清單")
    print("=" * 70)
    for orig, new_loc in moved_records:
        print(f"• {orig} ➔ {new_loc}")
    print("-" * 70)
    print(f"🗑️  刪除 __pycache__ 快取資料夾共：{deleted_pycache} 處")
    print(f"🗑️  刪除殘留 .pyc 檔案共：{deleted_pyc} 份")
    print("=" * 70)


if __name__ == "__main__":
    main()
