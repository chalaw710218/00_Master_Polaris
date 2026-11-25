#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-learning-cognitive-vault-keeper: 個人專屬三本認知存摺無鎖維護與存取原子腳本
專職負責維護內閣專屬「客觀事實庫、信念修正庫、自發好奇心庫」，落實防呆校驗與無鎖追加。
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROLE_DIRECTORY_MAP = {
    "Founder_Boss": "Office_of_the_Founder_Boss/01_Cognitive_Log",
    "CEO_Yuki": "Office_of_the_CEO_Yuki/01_Cognitive_Log",
    "CFO_Abacus": "Office_of_the_CFO_Abacus/01_Cognitive_Log",
    "CTO_Linus": "Office_of_the_CTO_Linus/01_Cognitive_Log",
    "CMO_Taylor": "Office_of_the_CMO_Taylor/01_Cognitive_Log",
    "CIO_Falcon": "Office_of_the_CIO_Falcon/01_Cognitive_Log",
    "Operative_Kage": "Office_of_the_Operative_Kage/01_Cognitive_Log",
    "Mascot_Meow": "Lounge_of_the_Mascot_Meow/01_Cognitive_Log",
}

VAULT_FILENAME_MAP = {
    "evidence": ("01_Experiences_and_Evidence.md", "EVD"),
    "belief": ("02_Belief_Evolution.md", "BLF"),
    "curiosity": ("03_Curiosities_and_Questions.md", "CUR")
}

def resolve_role_path(role_key: str) -> Path:
    """尋找角色的 01_Cognitive_Log 資料夾"""
    # 模糊比對角色 key
    matched_rel = None
    for k, v in ROLE_DIRECTORY_MAP.items():
        if k.lower() in role_key.lower() or role_key.lower() in k.lower():
            matched_rel = v
            break

    if not matched_rel:
        matched_rel = f"Office_of_{role_key}/01_Cognitive_Log"

    base_dir = Path("00-00_Gamification_Engine")
    return base_dir / matched_rel

def format_vault_entry(vault_type: str, title: str, content: str) -> str:
    """格式化存摺條目"""
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    tag_prefix = VAULT_FILENAME_MAP.get(vault_type, ("unknown.md", "LOG"))[1]
    serial = now.strftime("%Y%m%d-%H%M%S")

    entry = (
        f"\n### [{time_str}] {tag_prefix}-{serial}: {title}\n"
        f"- **登錄時間**：`{now.isoformat()}`\n"
        f"- **核心內容**：{content}\n"
    )
    return entry

def audit_role_vaults(role_dir: Path) -> dict:
    """審計角色專屬存摺"""
    stats = {}
    if not role_dir.exists():
        return {"exists": False, "role_dir": str(role_dir), "stats": {}}

    for v_key, (fname, tag) in VAULT_FILENAME_MAP.items():
        fpath = role_dir / fname
        if fpath.exists():
            text = fpath.read_text(encoding='utf-8')
            entries = len(re.findall(r"^###\s+\[", text, re.MULTILINE))
            stats[v_key] = {"file": fname, "exists": True, "entries_count": entries, "size_bytes": len(text)}
        else:
            stats[v_key] = {"file": fname, "exists": False, "entries_count": 0, "size_bytes": 0}

    return {"exists": True, "role_dir": str(role_dir), "stats": stats}

def main():
    parser = argparse.ArgumentParser(description="個人專屬三本認知存摺無鎖維護與存取原子")
    parser.add_argument("--role", type=str, default="CEO_Yuki", help="內閣角色標識")
    parser.add_argument("--vault", type=str, choices=["evidence", "belief", "curiosity"], default="evidence", help="存摺類型")
    parser.add_argument("--title", type=str, default="客觀事實條目", help="存摺條目標題")
    parser.add_argument("--content", type=str, default="實測數據 Exit Code 0 通過", help="存摺核心內容")
    parser.add_argument("--audit-vaults", action="store_true", default=False, help="審計角色存摺狀態")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")
    parser.add_argument("--execute-append", action="store_true", default=False, help="正式寫入存摺")

    args = parser.parse_args()
    dry_run = not args.execute_append

    role_dir = resolve_role_path(args.role)

    print(f"=== [atom-learning-cognitive-vault-keeper] 認知存摺三重奏維護 ===")
    print(f"目標角色: {args.role} | 目錄: {role_dir}")

    if args.audit_vaults:
        audit_res = audit_role_vaults(role_dir)
        print("\n📚 **【認知存摺審計結果】**")
        print(json.dumps(audit_res, ensure_ascii=False, indent=2))
        sys.exit(0)

    filename, tag = VAULT_FILENAME_MAP[args.vault]
    target_file = role_dir / filename
    formatted_entry = format_vault_entry(args.vault, args.title, args.content)

    print(f"模式: {'[DRY-RUN 預演]' if dry_run else '[EXECUTE 實體追加]'}")
    print(f"目標檔案: {filename}")
    print(f"格式化條目預覽:{formatted_entry}")

    if not dry_run:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, "a", encoding="utf-8") as f:
            f.write(formatted_entry)
        print(f"[+] 成功以無鎖追加（Append-Only）寫入存摺：{target_file}")
    else:
        print("[i] 預演完畢，格式合規。使用 --execute-append 可正式寫入。")

    sys.exit(0)

if __name__ == "__main__":
    main()
