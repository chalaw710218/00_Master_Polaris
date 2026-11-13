#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
boss_direct_copy.py
====================================================================
🛠️ atom-boss-direct-copy 闆仔直男真實日常敘事原子
首長：創辦人闆仔 ✕ 店貓喵編 ✕ 戴明博士
單一職責：零 Emoji 鋼印、刪節號呼吸感、達倫布朗痛點切入、外送收尾、留言相聲。
====================================================================
"""

import sys
import os
import re
import json
import random
import argparse
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOSS_SCENES = {
    "DELIVERY": {
        "hook": "說個正事... 你應該也有過那種經驗，安全帽鏡片起霧，前面紅燈亮了，後照鏡全是水珠，手把冰得發麻。",
        "body": "剛送完最後一單長輩的熱湯。\n\n很多人問我為什麼白天寫代碼，晚上還要自己騎車出來跑外送。\n\n老實說沒那麼多偉大情懷... 只是坐在冷氣房看報表久了，會忘記真實世界的柏油路有多顛簸，也容易忘記一個老人推開紗門接過便當那一刻的眼神。\n\n踩在泥巴裡，人比較清醒，做出來的系統才不會不食人間煙火。",
        "ending": "雨又變大了... 我要去送外送跟寫程式了，先這樣…",
        "meow_roast": "（在暖氣前翻了個白眼）闆仔又在深夜自言自語了。有空打那麼多字，不如趕快回來把本喵的肉泥罐打開喵～"
    },
    "CODE": {
        "hook": "說個正事... 凌晨一點十七分，終端機黑底綠字的光照在螢幕上，手指敲鍵盤敲到指尖有點發麻。",
        "body": "剛剛把最後一個離線防呆的邏輯測通。\n\n其實做點餐系統最難的不是花俏的動畫，而是當台東街角突然跳電、或者長輩的手指在螢幕上按得太重時，系統能不能安安靜靜頂住。\n\n我們不求當什麼科技巨頭... 只要這座城鎮需要我們的時候，系統不會當掉，這樣就及格了。",
        "ending": "咖啡涼了... 我要去送外送跟寫程式了，先這樣…",
        "meow_roast": "（踩在 Enter 鍵上）本喵已經坐在旁邊盯了三個小時，再不睡覺，本喵明天早上就去抓破外送箱！"
    },
    "REPAIR": {
        "hook": "說個正事... 螺絲起子轉到手心磨出紅印，老舊水龍頭的水滴聲終於停了下來。",
        "body": "下午去幫寶桑的一位阿嬤換水龍頭。\n\n阿嬤一直說要塞五百塊給我，推了老半天最後收了兩顆自家種的芭樂。\n\n生活管家做的事情真的很瑣碎... 換燈泡、通水管、送菜、除草。但看著老人家鬆了一口氣的表情，就覺得這比在簡報上畫大餅踏實多了。",
        "ending": "芭樂挺甜的... 我要去送外送跟寫程式了，先這樣…",
        "meow_roast": "（搶過芭樂聞了兩下）這不是肉，差評！不過看在阿嬤的面子上，本喵准你明天再去巡邏一次。"
    }
}

def generate_boss_post(context: str = "") -> Dict[str, Any]:
    """生成闆仔直男文案"""
    t = context.lower()
    if any(k in t for k in ["碼", "程式", "螢幕", "電腦", "終端", "夜"]):
        key = "CODE"
    elif any(k in t for k in ["修", "水", "燈", "草", "管", "阿嬤", "長輩"]):
        key = "REPAIR"
    else:
        key = "DELIVERY"

    cfg = BOSS_SCENES[key]
    full_copy = f"{cfg['hook']}\n\n{cfg['body']}\n\n{cfg['ending']}"
    
    # 嚴格戴明安燈：檢查是否誤用 Emoji
    has_emoji = bool(re.search(r"[\U00010000-\U0010ffff]", full_copy))
    if has_emoji:
        # 強制剔除
        full_copy = re.sub(r"[\U00010000-\U0010ffff]", "", full_copy)

    return {
        "status": "success",
        "atom": "atom-boss-direct-copy",
        "scene_matched": key,
        "input_context": context,
        "boss_copy": full_copy,
        "first_comment_meow_roast": cfg["meow_roast"],
        "andon_checks": {
            "zero_emoji_enforced": True,
            "darren_brown_hook": True,
            "ellipsis_breathing": True,
            "boss_signature_ending": True
        },
        "char_count": len(full_copy),
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-boss-direct-copy 闆仔直男真實日常敘事原子")
    parser.add_argument("--context", type=str, default="下雨天送外送，機車後照鏡全是水珠", help="日常照片情境")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = generate_boss_post(context=args.context)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 闆仔直男隨筆 ===\n{result['boss_copy']}\n")
        print(f"=== 留言相聲彩蛋 ===\n{result['first_comment_meow_roast']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
