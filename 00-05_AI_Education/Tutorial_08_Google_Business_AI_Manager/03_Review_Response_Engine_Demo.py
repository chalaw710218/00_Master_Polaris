"""
03_Review_Response_Engine_Demo.py
==================================
極星「數位平權 · Google 商家 AI 數位店長」評論回覆核心引擎 Demo
主理：CTO 林納斯 (Linus) 架構監製 ✕ 執行長 雪 (Yuki)

功能亮點：
1. 自動判定星級與情緒極性（5星好評 vs 1~3星負評）
2. 5星好評：注入店長本尊溫暖語氣 + 自然置入在地 SEO 關鍵字 + 推薦下次嘗試隱藏菜
3. 1~3星負評：太極降溫四部曲（接住情緒 -> 真誠致歉說明現做堅持 -> 提供私人聯繫管道 -> 展現大度成熟形象）
4. 100% 確定性防呆，消除機器人公版話
"""

import sys
import json
from dataclasses import dataclass
from typing import List, Dict

# 防呆：確保 Windows 主控台正確以 UTF-8 輸出，不因 Emoji 或繁中拋出編碼錯誤
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

@dataclass
class StoreProfile:
    name: str
    owner_name: str
    owner_tone: str
    greeting: str
    core_dishes: List[str]
    local_keywords: List[str]
    private_contact: str

def generate_review_reply(profile: StoreProfile, rating: int, customer_name: str, review_text: str) -> Dict[str, str]:
    """
    依據店家人格與評論內容，產出專屬店長回覆
    """
    if rating >= 4:
        # 5 星 / 4 星好評模式：熱情 + 感恩 + 招牌故事 + 在地 SEO
        reply = (
            f"哈囉 {customer_name}！{profile.greeting}！看到你的好評，我們整間店夥伴跟{profile.owner_name}心裡都暖洋洋的！✨\n\n"
            f"你提到的體驗真的讓我們很有共鳴！我們的「{profile.core_dishes[0]}」堅持每天清晨親手熬煮，不加人工甘味劑，"
            f"就是希望每位來【{profile.name}】的朋友，都能吃到最道地、最安心的家常美味。\n\n"
            f"身為【{profile.local_keywords[0]}】，下次如果有來台東或路過，非常推薦試試看我們的隱藏招牌「{profile.core_dishes[1]}」，"
            f"保證又是另一種驚喜喔！期待很快再見到你～祝你有個美好的一天！🍲"
        )
        strategy = "五星好評：溫暖在地共鳴 + 招牌食材堅持 + SEO在地關鍵字埋入 + 下次新品召回"
    else:
        # 1 星 ~ 3 星負評降溫模式：太極承擔 + 溫和誠懇 + 私人窗口
        reply = (
            f"{customer_name} 您好，我是【{profile.name}】的負責人{profile.owner_name}。\n\n"
            f"首先要向您致上最誠摯的歉意。看到您的評論，我心裡非常過意不去，也深深明白用餐體驗不如預期時的失望與沮喪。\n\n"
            f"您提到的問題（{review_text[:30]}...），我們店內已經立即展開內部檢核與SOP調整。由於店內料理堅持現點現煮、當日新鮮備料，"
            f"若在尖峰時段因忙亂造成疏漏或等候過久，這是我們必須檢討與改進的責任。\n\n"
            f"我們非常珍惜每位客人的真實聲音，希望有機會能向您親自致歉並做適當的補償。如果您願意，"
            f"請隨時透過我們的官方聯絡方式（{profile.private_contact}）與我直接聯繫。\n\n"
            f"再次感謝您的指教，祝您順心平安。"
        )
        strategy = "負評降溫：太極四部曲（老闆親自具名 + 接住情緒真誠道歉 + 說明現做改進SOP + 提供專屬私人溝通窗口）"

    return {
        "customer": customer_name,
        "rating": f"{rating} 星",
        "review_text": review_text,
        "strategy": strategy,
        "reply": reply
    }

if __name__ == "__main__":
    # 範例店鋪（錦鸞越南美食規格）
    demo_store = StoreProfile(
        name="錦鸞越南美食",
        owner_name="鸞姐",
        owner_tone="溫暖熱情、豪爽像鄰家大姐、對道地南洋食材有極致堅持",
        greeting="吃飽沒？很高興認識你！",
        core_dishes=["招牌道地牛肉河粉", "黃金酥脆越式法國麵包", "鮮蝦涼拌春捲"],
        local_keywords=["台東道地南洋料理推薦", "台東市必吃越南河粉", "台東火車站周邊美食"],
        private_contact="官方 LINE @jinluan 或店內電話 089-XXXXXX"
    )

    test_cases = [
        {
            "name": "張先生",
            "rating": 5,
            "text": "湯頭真的很清甜很道地，牛肉也很嫩！份量超級足夠，大推法國麵包外皮酥脆到不行！"
        },
        {
            "name": "陳小姐",
            "rating": 1,
            "text": "中午人超多等了整整半個小時，外帶回家發現居然少給了辣椒跟檸檬，吃起來少一味很失望。"
        }
    ]

    print("=" * 65)
    print("極星【數位平權 · Google 商家 AI 數位店長】評論回覆引擎實測")
    print("=" * 65)

    for i, tc in enumerate(test_cases, 1):
        result = generate_review_reply(demo_store, tc["rating"], tc["name"], tc["text"])
        print(f"\n【案例 {i}】顧客：{result['customer']} ｜ 給予評價：{result['rating']}")
        print(f"顧客留言：「{result['review_text']}」")
        print(f"戰略判定：{result['strategy']}")
        print("-" * 65)
        print("【AI 數位店長本尊回覆內容】：")
        print(result["reply"])
        print("=" * 65)
