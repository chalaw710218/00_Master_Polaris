#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstration: Threads Interaction Safety Gate Enforcement
驗證每日安全上限攔截機制：
1. 將上限暫時設為 1
2. 執行第 1 則留言 -> 通行並記錄 (1/1)
3. 執行第 2 則留言 -> 被安全門禁硬性擋下並停止
4. 驗收完成後將上限恢復為法定 15 則留言 / 60 個愛心
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from interaction_safety_gate import (
    can_comment,
    record_comment,
    reset_daily_stats_for_test,
    load_safety_state,
    save_safety_state,
    DEFAULT_MAX_COMMENTS,
    DEFAULT_MAX_LIKES
)

def run_demonstration():
    print("==================================================")
    print("🧪 [安全門禁實測] 每日走心留言上限防風控攔截演練")
    print("==================================================")

    # 1. 暫時將上限設為 1
    print("\n👉 步驟 1: 暫時將每日走心留言安全上限設為 1")
    reset_daily_stats_for_test(max_comments=1, max_likes=1)
    state = load_safety_state()
    print(f"   當前設定: 走心留言上限 = {state['max_comments']}, 今日已發 = {state['comments_count']}")

    # 2. 嘗試第 1 則走心留言
    print("\n👉 步驟 2: 嘗試發送第 1 則走心留言 (目標: @hattcoffee)")
    allowed_1, reason_1 = can_comment()
    print(f"   門禁審查結果: allowed={allowed_1} | {reason_1}")
    if allowed_1:
        record_comment(
            target_user="hattcoffee",
            post_url="https://www.threads.net/@hattcoffee/post/test1",
            comment_text="今天看到店裡手沖的香氣隔著螢幕都能感受到溫暖，老闆辛苦了！"
        )
        print("   ✅ 第 1 則走心留言成功放行並寫入紀錄！")

    # 3. 嘗試第 2 則走心留言
    print("\n👉 步驟 3: 嘗試發送第 2 則走心留言 (目標: @956leissmoker)")
    allowed_2, reason_2 = can_comment()
    print(f"   門禁審查結果: allowed={allowed_2} | {reason_2}")
    if not allowed_2:
        print(f"   🛑 [成功攔截] {reason_2}！第 2 則留言被硬性擋下，保護帳號安全！")
    else:
        print("   ❌ 異常：第 2 則未被擋下！")

    # 4. 恢復法定上限
    print("\n👉 步驟 4: 測試完畢，立即將安全上限恢復為法定 15 則留言 / 60 個愛心")
    state = reset_daily_stats_for_test(max_comments=DEFAULT_MAX_COMMENTS, max_likes=DEFAULT_MAX_LIKES)
    print(f"   恢復後狀態: 走心留言上限 = {state['max_comments']}, 愛心上限 = {state['max_likes']}, 當前計數 = {state['comments_count']}")
    print("==================================================")

if __name__ == "__main__":
    run_demonstration()
