"""
04_Weekly_Local_SEO_Post_Generator.py
======================================
極星「數位平權 · Google 商家 AI 數位店長」每週在地 SEO 動態生成器
主理：行銷長 泰勒絲 (Taylor Swift) 敘事架構 ✕ CTO 林納斯

功能亮點：
1. 為小店每週自動產出高吸引力 Google Updates 動態貼文
2. 結合節氣、在地台東生活感、當日現做幕後花絮與 CTA 引導
3. 植入 Google Maps 在地商家 SEO 關鍵字，提升店家在「附近餐廳/美食」的曝光權重
"""

import sys
import json
from dataclasses import dataclass
from typing import List

# 防呆：確保 Windows 主控台正確以 UTF-8 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

@dataclass
class LocalSEOTheme:
    title: str
    season_vibe: str
    dish_focus: str
    behind_the_scenes: str
    call_to_action: str
    hashtags: List[str]

def generate_weekly_google_post(store_name: str, owner_name: str, theme: LocalSEOTheme) -> str:
    post_content = (
        f"【{store_name} · 店長每週食記小語】🌿\n\n"
        f"大家最近過得好嗎？我是{owner_name}！\n\n"
        f"進入{theme.season_vibe}的時節，早晚風吹起來都有點涼意了。今天清晨在市場挑選當季食材時，"
        f"腦海裡第一個浮現的就是我們的這道「{theme.dish_focus}」。\n\n"
        f"很多常客常問我們為什麼湯頭喝起來特別甘甜？其實沒有什麼捷徑，就是{theme.behind_the_scenes}。"
        f"在這個講求快速的時代，我們依然相信：『用心熬出來的溫度，喝一口就知道。』\n\n"
        f"💡 {theme.call_to_action}\n\n"
        f"📍 店面位置：台東在地手作廚房\n"
        f"⏰ 今日現熬出爐，食材售完為止喔！歡迎大家路過進來坐坐吃碗熱騰騰的麵～\n\n"
        f"{' '.join(['#' + tag for tag in theme.hashtags])}"
    )
    return post_content

if __name__ == "__main__":
    sample_theme = LocalSEOTheme(
        title="秋冬暖胃現熬牛骨湯篇",
        season_vibe="秋末初冬微涼",
        dish_focus="道地現煮生牛河粉",
        behind_the_scenes="堅持每天清晨 5 點親自挑選新鮮大骨，慢火慢燉 6 小時，不加一粒人工味精",
        call_to_action="今天中午想吃點溫暖不油膩的嗎？淋上一瓣現擠檸檬汁與新鮮生辣椒，暖胃又過癮！",
        hashtags=["台東在地美食推薦", "錦鸞越南美食", "台東美食地圖", "台東必吃河粉", "秋冬暖胃首選"]
    )

    print("=" * 65)
    print("極星【Google 商家在地 SEO 每週動態生成展示】")
    print("=" * 65)
    print(generate_weekly_google_post("錦鸞越南美食", "鸞姐", sample_theme))
    print("=" * 65)
