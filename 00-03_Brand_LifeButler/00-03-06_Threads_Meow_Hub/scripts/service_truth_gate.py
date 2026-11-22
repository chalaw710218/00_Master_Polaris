#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
service_truth_gate.py — 服務真實性發文出廠硬門禁 (v3.0 創辦人親定精準版)

落實創辦人（品碩）親定鐵律：
1. 現有服務：外送、代跑腿、追垃圾車（代倒垃圾）。可以直接寫（不攔截）。
2. 未來服務：獨居長輩送湯、居家小修（換電池、換燈泡、通水管）、代買藥品、免動腦備菜。
   只能用「規劃中、想做、問大家需不需要」的口吻。
3. 不管哪種服務，具體的人物、事件、對話只能寫真的發生過的。沒發生過的寫成一般性描述，不准編情節。
4. 關鍵字清單只擋未來服務字眼（送湯給長輩/獨居長輩送湯、換電池、換燈泡、通水管、代買藥、備菜），
   不擋外送、跑腿、垃圾車相關字眼。
"""

import re

# 只擋未來尚未提供之服務字眼（不擋現有之外送、代跑腿、追垃圾車/代倒垃圾）
FUTURE_SERVICE_PATTERNS = [
    r"送湯給.*長輩",
    r"送湯給.*阿公",
    r"送湯給.*阿嬤",
    r"送湯給.*奶奶",
    r"獨居.*送湯",
    r"長輩.*送湯",
    r"換電池",
    r"換燈泡",
    r"通水管",
    r"居家小修",
    r"代買藥",
    r"買藥",
    r"免動腦備菜",
    r"備菜"
]

# 未來服務必須同時出現的「規劃/徵詢」意圖字眼
REQUIRED_FUTURE_INTENT_KEYWORDS = [
    "規劃", "想做", "需要嗎", "打算", "問大家", "籌備",
    "有沒有需要", "問問看", "構想", "正在準備", "需不需要"
]

def check_service_truth_poka_yoke(content: str) -> tuple[bool, str]:
    """
    檢查貼文是否觸犯「把未來服務寫成已發生事實」之紅線。
    回傳：(is_valid, reason)
    """
    if not content:
        return True, "內容為空"

    hit_services = []
    for pat in FUTURE_SERVICE_PATTERNS:
        matches = re.findall(pat, content)
        if matches:
            hit_services.extend(matches)

    # 若未涉及任何未來服務（例如只寫現有外送、跑腿、追垃圾車、日常白描），直接放行
    if not hit_services:
        return True, "✅ 服務真實性合格：未涉及未開通之未來服務"

    # 若涉及未來服務，檢查是否具備「規劃中/問大家需不需要」之意圖詞
    hit_intents = [w for w in REQUIRED_FUTURE_INTENT_KEYWORDS if w in content]
    
    if hit_intents:
        return True, (
            f"✅ 服務真實性合格：涉及未來服務 ({', '.join(sorted(set(hit_services)))})，"
            f"且已包含規劃/徵詢字眼 ({', '.join(hit_intents)})"
        )

    # 觸犯紅線：把未來服務寫成已發生事實
    reason = (
        f"❌ [服務真實性硬攔截] 草稿出現未來服務字眼 ({', '.join(sorted(set(hit_services)))})，"
        f"卻未同時出現「{'、'.join(REQUIRED_FUTURE_INTENT_KEYWORDS[:4])}」等規劃徵詢字眼！"
        f"依創辦人鐵律：未來服務只能用「規劃中、想做、問大家需不需要」之口吻！"
    )
    return False, reason


if __name__ == "__main__":
    print("=== 執行 service_truth_gate.py (v3.0) 單元測試 ===")
    test_cases = [
        # 1. 現有服務（外送、跑腿、追垃圾車）-> 應放行 (True)
        ("傍晚幫忙跑腿送達生活物資與熱騰騰的晚餐外送", True, "現有服務：外送與跑腿"),
        ("下班不用狼狽追垃圾車，生活管家代倒垃圾服務隨時支援", True, "現有服務：追垃圾車/代倒垃圾"),
        ("騎車幫長輩跑腿提菜與日常外送", True, "現有服務：跑腿提菜外送"),
        # 2. 未來服務寫成已發生（無規劃/徵詢字眼）-> 應擋下 (False)
        ("今天去幫阿公換電池跟換燈泡，順便通水管", False, "未來服務違規：居家小修寫成已發生"),
        ("下午幫獨居長輩送湯過去，還順路幫奶奶代買藥品", False, "未來服務違規：長輩送湯與代買藥寫成已發生"),
        ("今晚推出免動腦備菜盒幫大家省時間", False, "未來服務違規：免動腦備菜寫成已發生"),
        # 3. 未來服務搭配規劃/徵詢口吻 -> 應放行 (True)
        ("我們正在規劃獨居長輩送湯服務，你家附近有需要的長輩嗎？", True, "未來服務合規：長輩送湯+正在規劃/需要"),
        ("未來想做幫長輩換電池、換燈泡、通水管的居家小修，問大家需不需要？", True, "未來服務合規：居家小修+想做/需不需要"),
        ("如果生活管家規劃代買藥品與免動腦備菜，大家覺得有需要嗎？", True, "未來服務合規：代買藥/備菜+規劃/需要嗎"),
    ]
    
    all_passed = True
    for idx, (text, expected, label) in enumerate(test_cases, 1):
        ok, msg = check_service_truth_poka_yoke(text)
        status = "PASS" if ok == expected else "FAIL"
        if ok != expected:
            all_passed = False
        print(f"[Test {idx:02d}] [{status}] ({label})")
        print(f"  輸入: {text}")
        print(f"  預期: {expected} | 實測: {ok} -> {msg}\n")
        assert ok == expected, f"測試失敗: {text}"
        
    print(f"🎉 單元測試結果：{len(test_cases)}/{len(test_cases)} 全數通過 (Exit Code 0)！")
