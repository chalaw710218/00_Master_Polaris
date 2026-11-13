#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
event_intel_copy.py
====================================================================
📰 atom-event-intel-copy 活動海報全網情報深掘與五階文案原子
首長：行銷長泰勒絲 ✕ 戴明博士
單一職責：活動海報深度情感推進、D1~D5 文案矩陣、在地地推話術、私域導流。
====================================================================
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def generate_event_copy_matrix(event_name: str, host: str, date_loc: str = "本週末 @ 台東市區") -> Dict[str, Any]:
    """生成五階段文案矩陣"""
    matrix = {
        "D1_HOOK": {
            "stage_name": "D1【下鉤懸念篇 · 顛覆認知】",
            "copy": f"你有沒有想過，為什麼市面上那麼多麵包，吃完肚子總是脹氣不舒服？\n\n這不是你的腸胃有問題，而是我們已經太久沒有吃過『真正由時間發酵』的食物了。\n\n【{host}】這次決定把清晨四點的廚房秘密攤開在陽光下……\n\n#台東生活 #慢食風土",
            "comment_link": "想了解真正酸種麵包的發酵秘密？詳細活動場次已整理在第一則留言。"
        },
        "D2_EMOTION": {
            "stage_name": "D2【走心情感篇 · 常民痛點】",
            "copy": f"在講求快速翻桌的時代，願意花三天等一個麵團自然呼吸的人，在很多人眼裡叫做傻子。\n\n但如果沒有這群傻子的堅持，我們大概只能一輩子吃工廠流水線的化學香精。\n\n敬所有在街角安靜守護真材實料的職人們。\n\n#在地職人 #日常堅持",
            "comment_link": "活動名額有限，想給自己一個踏實早晨的朋友，報名傳送門請看留言區。"
        },
        "D3_CLIMAX": {
            "stage_name": "D3【核心爆點篇 · 拒絕妥協】",
            "copy": f"『如果為了賺錢要我加改良劑，那我寧可把烤箱關掉去挑地瓜葉。』\n\n這是主辦人幾年前創業碰壁時說過的一句話。\n\n這次的【{event_name}】，不只是教學，是一場關於生活主權的溫柔奪回。\n\n#飲食主權 #台東慢食",
            "comment_link": "完整講者訪談與活動資訊，管家已置頂於第一則留言。"
        },
        "D4_AUTHORITY": {
            "stage_name": "D4【權威背書篇 · 專題直擊】",
            "copy": f"大報專題與主流媒體爭相報導的背後，其實只有四個字：【實事求是】。\n\n看見台東的土地如何孕育出純淨野生酵母，這份震撼值得你親自走進現場摸摸麵團。\n\n時間：{date_loc}\n\n#文化深耕 #風土飲食",
            "comment_link": "倒數名額最後保留，點擊留言區連結立即預約席次。"
        },
        "D5_CONVERT": {
            "stage_name": "D5【極限轉換篇 · 最後席次】",
            "copy": f"最後 24 小時倒數。\n\n我們不賣焦慮，但烤箱的容量確實有限，多一張椅子都擠不下了。\n\n如果你週末正好在台東，留兩個小時給自己，來聞聞剛出爐的香氣吧。\n\n#最後席次 #美好相遇",
            "comment_link": "席次即將關閉，請直接私訊生活管家或由留言區表單完成確認。"
        }
    }

    local_promote_guide = [
        "1. 在地友好店家（如咖啡、早午餐、獨立書店）櫃台拜訪指引：",
        f"   『老闆打擾了！我們這週末跟【{host}】合辦【{event_name}】，推廣在地真材實料。這張海報能不能借櫃台一角張貼？我們也會在線上文案裡感謝貴店的友善支持！』"
    ]

    return {
        "status": "success",
        "atom": "atom-event-intel-copy",
        "event_name": event_name,
        "host": host,
        "date_location": date_loc,
        "five_stages_copy": matrix,
        "local_store_promotion_guide": local_promote_guide,
        "comment_cta_strategy": "內文嚴格零外部連結（防止演算法降權），所有報名連結均由第一則公開款待留言引導。",
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-event-intel-copy 活動海報五階文案原子")
    parser.add_argument("--event-name", type=str, default="野莓酸種烘焙分享會", help="活動主題")
    parser.add_argument("--host", type=str, default="草民料理", help="主辦或講者")
    parser.add_argument("--date-loc", type=str, default="本週末 @ 台東市區", help="時間地點")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = generate_event_copy_matrix(event_name=args.event_name, host=args.host, date_loc=args.date_loc)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== {result['event_name']} 五階文案矩陣生成完畢 ===")
        print(result["five_stages_copy"]["D1_HOOK"]["copy"])

    sys.exit(0)

if __name__ == "__main__":
    main()
