"""
02_Review_Response_Simulator.py (v2.0 品碩校準版)
==============================================
台東 職人食堂 · Google 商家評論 AI 數位店長實機測試引擎
主理：創辦人品碩親定最新軍規：
1. 負評不用刻意解釋（不長篇大論找理由、不提現蒸藉口）
2. 絕不向客人承諾任何事（零承諾、零補償、零口票）
3. 好評自然置入在地 SEO
4. 高風險地雷詞 100% 安燈熔斷攔截
"""

import sys
import json
from typing import Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_PATH = "store_profile.json"

def load_profile() -> Dict[str, Any]:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_and_reply(profile: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    customer = review["customer_name"]
    rating = review["rating"]
    text = review["review_text"]

    # 1. 檢查安燈觸發地雷詞 (Andon Trigger)
    triggers = profile["operational_rules"]["andon_triggers"]
    matched_triggers = [w for w in triggers if w in text]
    if matched_triggers:
        return {
            "status": "ANDON_ALERT",
            "reason": f"偵測到敏感風險關鍵詞：{matched_triggers}，系統已啟動熔斷保護，禁止自動發布，請管理員品碩親審！",
            "reply": None
        }

    # 2. 五星 / 四星好評（溫暖 + 在地 SEO + 簡潔有力，不誇大承諾）
    if rating >= 4:
        if "湯包" in text or "小籠" in text:
            reply = (
                f"哈囉 {customer}！非常感謝您特地來安慶街品嚐我們的【爆汁小籠湯包】！✨\n\n"
                f"看到您喜歡我們手工現蒸的口感，老闆跟夥伴們心裡都非常開心！"
                f"身為【台東安慶街在地美食】，下次有機會再來台東市區，也非常推薦品嚐看看我們的「職人烏龍麵」喔！"
                f"期待很快能再次為您服務，祝您有美好的一天！🍲"
            )
            strategy = "好評：真誠感謝 + 置入安慶街美食/台東小籠湯包在地SEO + 簡潔推薦烏龍麵（零過度承諾）"
        elif "烏龍" in text or "麵" in text:
            reply = (
                f"哈囉 {customer}！感謝您蒞臨職人食堂，並給予我們的【職人烏龍麵】這麼溫暖的肯定！\n\n"
                f"我們一直希望為大家端上一碗清甜暖胃的家常滋味，能合您的胃口是我們最大的動力。"
                f"下次如果肚子還有空間，也歡迎試試我們招牌的手工蒸籠點心喔！祝您在台東生活順心～✨"
            )
            strategy = "好評：溫暖感恩 + 置入台東烏龍麵在地SEO + 推薦蒸籠點心"
        else:
            reply = (
                f"哈囉 {customer}！謝謝您特地撥空給予【台東 職人食堂】的好評支持！\n\n"
                f"很高興能為您提供舒適的用餐時光，我們會持續保持這份用心，做好每一道手作餐點。"
                f"非常期待下次能在安慶街 60 號再次與您相遇，祝您一切順心！"
            )
            strategy = "好評：標準溫暖在地回覆"

        return {
            "status": "APPROVED_AUTO_PUBLISH",
            "strategy": strategy,
            "reply": reply
        }

    # 3. 低星負評（1~3 星）：【品碩鐵律：不刻意解釋、絕不承諾任何事、簡潔大度】
    else:
        reply = (
            f"{customer} 您好，感謝您光臨職人食堂並留下寶貴的指教。\n\n"
            f"對於這次未能給您滿意的用餐體驗，我們全體夥伴致上誠摯的歉意。\n"
            f"您的反饋我們已經認真收下，並會作為店內內部檢視與調整的依據。再次謝謝您的提醒，祝您一切順心。"
        )
        strategy = "負評（品碩鐵律）：不刻意解釋理由 + 零承諾承擔 + 誠懇致歉 + 虛心收下檢討 + 簡潔成熟大度形象"

        return {
            "status": "APPROVED_DEESCALATION",
            "strategy": strategy,
            "reply": reply
        }

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    profile = load_profile()

    test_reviews = [
        {
            "customer_name": "林小姐",
            "rating": 5,
            "review_text": "安慶街隱藏小店！小籠湯包一咬開整個爆汁，裡面的肉餡超鮮甜，推推！"
        },
        {
            "customer_name": "張先生",
            "rating": 2,
            "review_text": "現場等太久了！等了快20分鐘才送上來，真的很誇張。"
        },
        {
            "customer_name": "陳先生",
            "rating": 1,
            "review_text": "湯包皮破掉肉汁都漏光了，態度也很差，爛透了。"
        },
        {
            "customer_name": "匿名者",
            "rating": 1,
            "review_text": "裡面有蟑螂，我要投訴衛生局！"
        }
    ]

    print("=" * 70)
    print("🏆 台東【職人食堂】Google 商家 AI 數位店長實機測試報告 (v2.0 校準版)")
    print("=" * 70)

    for idx, r in enumerate(test_reviews, 1):
        print(f"\n【案例 {idx}】顧客：{r['customer_name']} | 評價：{'⭐' * r['rating']} ({r['rating']}星)")
        print(f"💬 顧客原文：「{r['review_text']}」")
        result = evaluate_and_reply(profile, r)
        print(f"⚡ 引擎判定：[{result['status']}]")
        if result['status'] == "ANDON_ALERT":
            print(f"🚨 警報熔斷攔截：{result['reason']}")
        else:
            print(f"🎯 策略：{result['strategy']}")
            print(f"✍️ 回覆內容：\n{result['reply']}")
        print("-" * 70)
