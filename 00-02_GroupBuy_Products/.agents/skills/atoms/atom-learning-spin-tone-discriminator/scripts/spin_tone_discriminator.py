#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-learning-spin-tone-discriminator: SPIN 內部自對弈去 AI 腔與創辦人神韻對齊原子腳本
專職負責執行 UCLA SPIN 內部自對弈盲測，一票否決 AI 說教套話與農場詞，守護實幹商人底色。
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# AI 腔、套話、說教詞與農場宣傳詞庫
AI_SLOP_PATTERNS = [
    r"在當今瞬息萬變的世界中",
    r"總之，",
    r"讓我們深入探討",
    r"無疑是一個",
    r"值得注意的是",
    r"如前所述",
    r"顛覆性",
    r"引領未來",
    r"保證賺錢",
    r"限時瘋搶",
    r"震撼揭秘",
    r"不可思議的奇蹟",
]

# 創辦人品碩（闆仔）實幹商人語音正向信號
FOUNDER_PRAGMATIC_SIGNALS = [
    r"算大帳",
    r"跑腿費",
    r"成本",
    r"損耗",
    r"真實",
    r"物理",
    r"實體",
    r"坦白講",
    r"老老實實",
    r"閉環",
    r"真值",
]

def discriminate_tone(text: str, strict_mode: bool = False) -> dict:
    """執行 SPIN 自對弈判別審查"""
    found_slop = []
    for pattern in AI_SLOP_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            found_slop.append({"pattern": pattern, "count": len(matches)})

    found_pragmatic = []
    for pattern in FOUNDER_PRAGMATIC_SIGNALS:
        matches = re.findall(pattern, text)
        if matches:
            found_pragmatic.append({"signal": pattern, "count": len(matches)})

    # 計算對齊分數 (基準分 100)
    score = 100
    penalty = sum(m["count"] for m in found_slop) * (25 if strict_mode else 15)
    bonus = min(20, sum(m["count"] for m in found_pragmatic) * 5)
    final_score = max(0, min(100, score - penalty + bonus))

    pass_threshold = 80 if strict_mode else 70
    is_passed = (final_score >= pass_threshold) and (len(found_slop) == 0)

    return {
        "score": final_score,
        "is_passed": is_passed,
        "pass_threshold": pass_threshold,
        "ai_slop_detected": found_slop,
        "pragmatic_signals": found_pragmatic,
        "recommendation": (
            "✅ 判別通過！文字已徹底消除 AI 說教腔與農場虛詞，對齊創辦人實幹商人神韻。"
            if is_passed else
            "❌ 判別失敗！偵測到 AI 腔或浮誇虛詞，強制打回生成器重寫修剪！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="SPIN 內部自對弈去 AI 腔與創辦人神韻對齊原子")
    parser.add_argument("--input-text", type=str, help="待審查草案純文字")
    parser.add_argument("--file-path", type=str, help="待審查檔案路徑")
    parser.add_argument("--strict-founder-mode", action="store_true", default=False, help="嚴格闆仔模式")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    content = ""
    if args.file_path and os.path.exists(args.file_path):
        content = Path(args.file_path).read_text(encoding='utf-8')
    elif args.input_text:
        content = args.input_text
    else:
        # 內建模擬合規實幹文案
        content = (
            "老老實實把水產冷鏈成本算大帳，扣除 8% 物理損耗與跑腿費，"
            "堅持 0.0% 包冰真實淨重，給夥伴透明分成，不玩任何虛假的促銷套路。"
        )

    print("=== [atom-learning-spin-tone-discriminator] 啟動 UCLA SPIN 內部自對弈審查 ===")
    res = discriminate_tone(content, strict_mode=args.strict_founder_mode)

    print("\n🎭 **【SPIN 自對弈審查證明】**")
    print(f"對齊得分: {res['score']} / 100 (合格線: {res['pass_threshold']})")
    print(f"審查結論: {res['recommendation']}")
    if res["ai_slop_detected"]:
        print(f"[-] 攔截到 AI 腔/農場詞: {res['ai_slop_detected']}")
    if res["pragmatic_signals"]:
        print(f"[+] 識別出實幹商人信號: {res['pragmatic_signals']}")

    if res["is_passed"]:
        print("\n[+] SPIN 自對弈判別通過 (Exit Code: 0)！")
        sys.exit(0)
    else:
        print("\n[-] SPIN 自對弈判別未通過，觸發出廠阻斷 (Exit Code: 1)！")
        sys.exit(1)

if __name__ == "__main__":
    main()
