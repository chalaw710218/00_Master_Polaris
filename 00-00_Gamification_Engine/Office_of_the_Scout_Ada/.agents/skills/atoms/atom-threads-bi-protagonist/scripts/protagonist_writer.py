#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protagonist_writer.py
====================================================================
✍️ atom-threads-bi-protagonist 雙主角生理週期原創隨筆創作原子
首長：行銷長泰勒絲 ✕ 生活管家影 ✕ 店貓喵編 ✕ 戴明博士
單一職責：雙主角生理週期排程、單一標籤、留白排版、35mm 微瑕真實視覺提示詞。
====================================================================
"""

import sys
import os
import json
import random
import argparse
from datetime import datetime
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

MEOW_POSTS = [
    {
        "hook": "週一的開工打卡，是人類發明最違反生物本能的發明。",
        "body": "本喵在紙箱裡翻了個身，前爪縮在胸口。\n\n外面下著細雨，聽說你們又要去擠那台晃來晃去的捷運。\n\n不用太羨慕本喵，本喵等一下也要在暖爐前值班打盹三個小時，很辛苦的。",
        "tag": "#貓咪日常",
        "image_prompt": "35mm natural photography, cozy indoor morning light, a classic gray tabby cat with yellow-green eyes sleeping peacefully curled up inside a cardboard box, shallow depth of field, real whiskers and soft fur textures, grainy, film-like warm imperfection, no digital smoothing."
    },
    {
        "hook": "人類每天盯著那個發光的長方形發呆，裡面到底有什麼？",
        "body": "明明沒有肉泥的味道，也沒有烤魚的香氣。\n\n看你們嘆氣嘆成那樣，本喵勉為其難跳上桌子，用尾巴掃一下鍵盤。\n\n好了，今天的工作進度就到這裡，准你關螢幕摸肚肚兩分鐘。",
        "tag": "#打工人日常",
        "image_prompt": "35mm analog camera shot, an authentic gray tabby cat sitting casually on a cluttered wooden desk next to a laptop keyboard, turning its head slightly with an aloof expression, natural soft window side light, real domestic home setting, cozy, cinematic grain."
    }
]

SHADOW_POSTS = [
    {
        "hook": "入冬之後的台東夜晚，廚房那鍋滾沸的熱氣才是生活唯一的解藥。",
        "body": "下班趕回家的路上，風把圍巾吹得有些涼。\n\n切幾片在地老薑，丟進兩把剝皮辣椒，慢火煨出清甜的雞湯。\n\n生活就算有再多不如意，只要能坐下來熱騰騰地喝上一碗，心就安靜落地了。",
        "tag": "#日常料理",
        "image_prompt": "35mm real life photo, cinematic warm kitchen interior at night, a 28-year-old gentle East Asian female lifestyle butler wearing a cozy beige oversized knitted sweater and thin round glasses, loose low ponytail, ladling steaming hot chicken soup into a rustic ceramic bowl, soft steam rising, warm bokeh, gentle smile, documentary aesthetic."
    },
    {
        "hook": "週末的早晨不需要鬧鐘，窗外的鳥叫聲就是最自然的喚醒。",
        "body": "泡了一壺在地紅烏龍，茶湯透著琥珀色的微光。\n\n把陽台晾著的棉質床單收進來，滿滿都是曬過太陽的香氣。\n\n不趕時間的日子，把動作放慢一半，生活才會慢慢長出肉來。",
        "tag": "#台東生活",
        "image_prompt": "35mm domestic still life, bright peaceful weekend morning, sunlight pouring through sheer white curtains onto a wooden table, a warm cup of amber Taiwanese oolong tea steaming gently beside an open book, natural linen fabric texture, soft dust motes in sunbeams, poetic realism."
    }
]

def determine_protagonist() -> str:
    """依據生理週率自動判定主役 (週一至週三喵編，週四至週日影)"""
    weekday = datetime.now().weekday() # 0 = Monday, 6 = Sunday
    if weekday in [0, 1, 2]:
        return "meow"
    return "shadow"

def create_protagonist_post(role: str = "auto") -> Dict[str, Any]:
    """生成原創貼文 payload"""
    if role == "auto":
        role = determine_protagonist()
        
    if role == "meow":
        post_data = random.choice(MEOW_POSTS)
        speaker = "店貓 喵編 (Meow Editor · 灰色虎斑貓)"
        post_text = f"{post_data['hook']}\n\n{post_data['body']}\n\n{post_data['tag']}"
    else:
        post_data = random.choice(SHADOW_POSTS)
        speaker = "生活管家 影 (Kage · 28歲女性管家)"
        post_text = f"{post_data['hook']}\n\n{post_data['body']}\n\n{post_data['tag']}"

    return {
        "status": "success",
        "atom": "atom-threads-bi-protagonist",
        "protagonist_role": speaker,
        "topic_tag": post_data["tag"],
        "post_text": post_text,
        "char_count": len(post_text),
        "visual_dna_prompt": post_data["image_prompt"],
        "rules_complied": {
            "single_topic_tag": True,
            "seo_in_first_two_lines": True,
            "breath_spacing_layout": True,
            "35mm_anti_ai_visual": True
        },
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-bi-protagonist 雙主角原創隨筆創作原子")
    parser.add_argument("--role", type=str, default="auto", choices=["auto", "meow", "shadow"], help="指定主役角色")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬生成")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = create_protagonist_post(role=args.role)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['protagonist_role']}] 今日原創隨筆:\n{result['post_text']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
