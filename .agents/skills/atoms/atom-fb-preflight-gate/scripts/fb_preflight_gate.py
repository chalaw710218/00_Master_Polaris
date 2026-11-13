#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fb_preflight_gate.py
Facebook 貼文防降權與品牌紅線安燈引擎
嚴格審查內文零外連、自動抽離封裝第一留言、品牌零洩漏防火牆與 10m~75d 排程合法性
"""

import sys
import re
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]
URL_REGEX = re.compile(r'https?://[^\s]+')

DEFAULT_STORE_INFO = """📍【門市取貨與服務資訊】
• 取貨地址：台東市正氣北路166巷90號
• 服務區域：台東市區、知本、南王、都蘭、東河專人配送
• 生活管家，就醬點！ 溫暖到府"""

def inspect_and_sanitize_fb_post(text: str, schedule_str: str = None) -> Dict[str, Any]:
    """審查並淨化 FB 貼文，將外部網址自動抽離並封裝為第一則留言"""
    andon_triggered = False
    violations: List[str] = []
    passes: List[str] = []

    # 1. 品牌法定名稱零洩漏審查
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in text:
            andon_triggered = True
            violations.append(f"【品牌紅線致命違規】內文出現內部代號「{forbidden}」！對外法定品牌僅能為「生活的一部分，就醬點！」或自稱「生活管家」")

    # 2. 檢測外部 URL
    found_urls = URL_REGEX.findall(text)
    sanitized_text = text
    first_comment_lines = []

    if found_urls:
        passes.append(f"偵測到 {len(found_urls)} 個外部連結，啟動自動防降權抽離程序")
        # 移除非法連結並替換為合規引導詞
        for url in found_urls:
            sanitized_text = sanitized_text.replace(url, "")
            first_comment_lines.append(f"👉 點擊連結直達：{url}")

        sanitized_text = sanitized_text.strip()
        # 追加合規引導詞
        guide_sentence = "\n\n👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！"
        if "【第一則留言】" not in sanitized_text:
            sanitized_text += guide_sentence
    else:
        passes.append("內文純淨檢驗合格: 零外部超連結 (100% 規避 Meta 降權演算法)")

    # 封裝第一則留言
    first_comment_payload = ""
    if first_comment_lines or found_urls:
        first_comment_payload = "【生活管家 貼心指引與預約連結】\n" + "\n".join(first_comment_lines) + "\n\n" + DEFAULT_STORE_INFO
    else:
        first_comment_payload = "👉 點擊加入管家專屬 LINE 官方帳號（內有完整系統可直接點選訂購）：\nhttps://lin.ee/z83YSq6\n\n" + DEFAULT_STORE_INFO

    # 3. 排程時間合法性檢驗 (10 分鐘 ~ 75 天)
    schedule_timestamp = None
    if schedule_str:
        try:
            # 支援 YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DDTHH:MM
            sched_dt = datetime.fromisoformat(schedule_str.replace(" ", "T"))
            now = datetime.now()
            min_allowed = now + timedelta(minutes=10)
            max_allowed = now + timedelta(days=75)

            if sched_dt < min_allowed:
                andon_triggered = True
                violations.append(f"【排程時間過近】排程時間 {sched_dt} 距現在不足 10 分鐘 (Meta API 強制要求 >= 10 分鐘)")
            elif sched_dt > max_allowed:
                andon_triggered = True
                violations.append(f"【排程時間過遠】排程時間 {sched_dt} 超過 75 天上限")
            else:
                schedule_timestamp = int(sched_dt.timestamp())
                passes.append(f"排程時間檢驗合格: {sched_dt} (符合 10m~75d 規範)")
        except ValueError:
            andon_triggered = True
            violations.append(f"【排程格式錯誤】無法解析排程時間格式「{schedule_str}」，請使用 YYYY-MM-DD HH:MM:SS")

    return {
        "status": "ABORT_ANDON" if andon_triggered else "PASS_FOR_DISPATCH",
        "verdict": "❌ 觸發戴明安燈拉繩！貼文存在合規缺陷！" if andon_triggered else "✅ 戴明安燈審查通過！貼文已就緒！",
        "clean_post_message": sanitized_text,
        "first_comment_payload": first_comment_payload,
        "scheduled_publish_time": schedule_timestamp,
        "violations": violations,
        "passes": passes
    }

def main():
    parser = argparse.ArgumentParser(description="Facebook 貼文防降權與品牌紅線安燈引擎")
    parser.add_argument("--text", type=str, default="生活管家台東生鮮直送！訂購點這裡：https://lin.ee/z83YSq6 生活的一部分，就醬點！", help="原始貼文草稿")
    parser.add_argument("--schedule", type=str, default=None, help="預約排程時間 (格式: YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--dry-run", action="store_true", help="執行防降權審查與抽離模擬")
    args = parser.parse_args()

    result = inspect_and_sanitize_fb_post(args.text, args.schedule)

    print("==================================================")
    print(f"🛑 Facebook 貼文前置安燈審查: {result['status']}")
    print(result["verdict"])
    print("--------------------------------------------------")
    print("檢查通過項目:")
    for p in result["passes"]:
        print(f"  [✓] {p}")

    if result["violations"]:
        print("--------------------------------------------------")
        print("⚠️ 攔截違規與安燈拉繩項目:")
        for v in result["violations"]:
            print(f"  [✗] {v}")
        print("==================================================")
        sys.exit(1)

    print("--------------------------------------------------")
    print("📝 淨化後安全發布內文 (防降權且零外連):")
    print(result["clean_post_message"])
    print("--------------------------------------------------")
    print("💬 自動封裝第一則留言 (First Comment Payload):")
    print(result["first_comment_payload"])
    if result["scheduled_publish_time"]:
        print(f"⏰ 排程發布時間戳: {result['scheduled_publish_time']}")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
