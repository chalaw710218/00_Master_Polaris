#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_feedback_control.py — 清掉補登的假對照組（一次性修正）
放在 scripts/ 資料夾，與 feedback_loop.py 同一層。執行：
    python fix_feedback_control.py          # 先看會刪哪些（不動檔案）
    python fix_feedback_control.py --apply  # 真的修正（會先備份）
做的事：把內容開頭是「【歷史發布紀錄】」的補登舊貼文從 feedback_posts.json 移除。
它們不是同日同條件發的對照組，留著會讓比較失真。
"""
import json
import shutil
import sys
import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HUB_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = HUB_DIR / "data" / "feedback_posts.json"
MARK = "【歷史發布紀錄】"


def main():
    apply = "--apply" in sys.argv
    if not LOG_FILE.exists():
        print(f"找不到 {LOG_FILE}")
        sys.exit(1)
    posts = json.loads(LOG_FILE.read_text(encoding="utf-8"))
    fake = [p for p in posts if str(p.get("content", "")).startswith(MARK)]
    keep = [p for p in posts if p not in fake]

    print(f"總共 {len(posts)} 篇｜要移除的補登舊貼文 {len(fake)} 篇｜保留 {len(keep)} 篇")
    for p in fake:
        print(f"  - {p['post_id']}  {p['content'][:30]}")

    if not apply:
        print("\n（預覽模式，檔案沒動。確認無誤後加 --apply 執行）")
        return
    if not fake:
        print("沒有需要移除的項目。")
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = LOG_FILE.with_name(f"feedback_posts.backup_{stamp}.json")
    shutil.copy2(LOG_FILE, backup)
    LOG_FILE.write_text(json.dumps(keep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n已完成。備份在 {backup.name}")
    print("提醒：今天起每天第一篇請用 --k-id control 發，文案不要套用任何 K 知識。")


if __name__ == "__main__":
    main()
