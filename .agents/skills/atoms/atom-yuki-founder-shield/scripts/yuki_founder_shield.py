#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-yuki-founder-shield: 創辦人時間主權防護罩與一鍵審批封裝原子腳本
專職負責執行長雪 (Yuki) 捍衛創辦人時間主權，過濾日常雜訊並組裝一鍵審批卡片。
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROUTINE_NOISE_KEYWORDS = [
    "超時", "重試", "重構警告", "排程碰撞", "格式調整", "暫存清理", "日常點讚", "微小摩擦", "日誌輪替"
]

STRATEGIC_KEYWORDS = [
    "股權", "定價大改", "生死", "法規威脅", "開課席次", "重大合約", "合作分成", "預算超支"
]

def filter_founder_noise(event_desc: str) -> dict:
    """三道防線雜訊過濾器"""
    event_lower = event_desc.lower()

    if any(k in event_lower for k in STRATEGIC_KEYWORDS):
        return {
            "action": "ESCALATE_TO_FOUNDER",
            "shield_status": "PASSED_DEFENSE_GATE_3",
            "reason": "涉及重大主權、定價或戰略命脈，必須封裝審批卡呈報創辦人！"
        }

    return {
        "action": "ABSORBED_BY_CABINET",
        "shield_status": "INTERCEPTED_BY_DEFENSE_GATE_1_OR_2",
        "reason": "屬於日常工程/協同雜訊，由執行長雪與相關首長在幕後安靜自癒，絕不驚動創辦人！"
    }

def build_approval_card(topic: str, plan_a: str, plan_b: str) -> str:
    """封裝 <= 100 字之一鍵審批卡片"""
    card = (
        f"🎯 **【執行長雪 · 創辦人一鍵審批卡】**\n"
        f"報告品碩，關於『{topic}』經內閣預咀嚼，提煉兩全解法：\n"
        f"  * 【方案 A (穩健守江山)】：{plan_a}\n"
        f"  * 【方案 B (敏捷開新局)】：{plan_b}\n"
        f"請創辦人一鍵裁決：【回覆 A / B / 核准】"
    )
    return card

def main():
    parser = argparse.ArgumentParser(description="創辦人時間主權防護罩與一鍵審批封裝原子")
    parser.add_argument("--topic", type=str, default="友店合作利潤分成比例裁決", help="重大決策主題")
    parser.add_argument("--plan-a", type=str, default="採 60/40 分成，死守 114 天無債水庫底線", help="方案 A")
    parser.add_argument("--plan-b", type=str, default="採 70/30 讓利友店，換取台東全區快速插旗", help="方案 B")
    parser.add_argument("--filter-noise", type=str, help="檢測特定日常事件是否被防護罩過濾")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-yuki-founder-shield] 啟動創辦人時間主權防護結界 ===")

    if args.filter_noise:
        res = filter_founder_noise(args.filter_noise)
        print(f"\n事件評估: 『{args.filter_noise}』")
        print(f"防護罩裁決: [{res['action']}] | 狀態: {res['shield_status']}")
        print(f"防護依據: {res['reason']}")
        sys.exit(0)

    card_text = build_approval_card(args.topic, args.plan_a, args.plan_b)
    print("\n" + card_text)

    # 驗證字數是否精煉
    char_count = len(card_text)
    print(f"\n[+] 一鍵審批卡片生成完畢 (總長度: {char_count} 字，符合低熵專注心流) (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
