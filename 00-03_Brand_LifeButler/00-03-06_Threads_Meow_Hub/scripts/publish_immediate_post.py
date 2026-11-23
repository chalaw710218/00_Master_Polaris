#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_immediate_post.py — 即時發布指定貼文（通過全部三道門禁並登記對照組）
"""

import sys
from pathlib import Path
import json
import time
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HUB_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(HUB_DIR / "scripts"))

from service_truth_gate import check_service_truth_poka_yoke
from text_hash_gate import check_text_poka_yoke, register_published_text_hash
from image_hash_gate import check_image_poka_yoke, register_published_image_hash
from threads_publisher import publish_thread, API_BASE, THREADS_ACCESS_TOKEN
from feedback_loop import log_post

POST_TEXT = """（把前腳折好在胸口，窩在木窗台前）
看著外面的微風吹過街道，
這大概就是世界上最安心的時刻喵。

人類總是在忙著跟時間賽跑，
但對本喵來說，最重要的只有兩件事：
罐罐打開的聲音，還有陽光曬暖的毛毯。

今天大家的生活還順利嗎？
累了就學本喵一樣，原地折手手深呼吸一下喵！🐾 #台東生活"""

FIRST_REPLY = "（翻肚肚打呼嚕）下午如果精神有點渙散，站起來喝口溫水，剩下的半天笑著過喵🐾"

IMAGE_PATH = r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\meow_taitung_afternoon_loaf_1795416514806.jpg"

def main():
    print("=" * 60)
    print("🚀 [即時發布] 開始執行生活管家 店貓喵編 對照組發文流水線...")
    print("=" * 60)

    # 1. 服務真實性門禁
    print("1️⃣ [門禁檢驗] 執行 service_truth_gate...")
    ok_truth, msg_truth = check_service_truth_poka_yoke(POST_TEXT)
    if not ok_truth:
        raise ValueError(f"❌ 服務真實性門禁攔截: {msg_truth}")
    print(f"   ✅ {msg_truth}")

    # 2. 文案雜湊與相似度門禁
    print("2️⃣ [門禁檢驗] 執行 text_hash_gate...")
    ok_text, msg_text = check_text_poka_yoke(POST_TEXT, threshold=0.70, check_remote=True)
    if not ok_text:
        raise ValueError(f"❌ 文案雜湊門禁攔截: {msg_text}")
    print(f"   ✅ {msg_text}")

    # 3. 圖片實體雜湊門禁
    print("3️⃣ [門禁檢驗] 執行 image_hash_gate...")
    ok_img, msg_img = check_image_poka_yoke(IMAGE_PATH)
    if not ok_img:
        raise ValueError(f"❌ 圖片雜湊門禁攔截: {msg_img}")
    print(f"   ✅ {msg_img}")

    # 4. 發布主貼文
    print("4️⃣ [API 發布] 正在向 Threads API 發布主貼文...")
    post_id = publish_thread(text=POST_TEXT, image=IMAGE_PATH, topic_tag="耍廢日常")
    if not post_id:
        raise RuntimeError("❌ Threads API 發布主貼文失敗，未取得 Post ID！")
    print(f"   🎉 主貼文發布成功！Post ID: {post_id}")

    # 取得官方 permalink
    permalink = f"https://www.threads.net/@hellotaitung/post/{post_id}"
    try:
        r = requests.get(
            f"{API_BASE}/{post_id}",
            params={"fields": "id,text,permalink", "access_token": THREADS_ACCESS_TOKEN},
            timeout=10,
        )
        if r.status_code == 200 and r.json().get("permalink"):
            permalink = r.json()["permalink"]
    except Exception as e:
        print(f"   ⚠️ 查詢官方 permalink 提示: {e}")
    print(f"   🔗 官方永久連結: {permalink}")

    # 5. 發布首回覆
    print("5️⃣ [API 首回覆] 正在發布首回覆...")
    time.sleep(2)
    reply_id = publish_thread(text=FIRST_REPLY, reply_to_id=post_id)
    if reply_id:
        print(f"   ✅ 首回覆發布成功！Reply ID: {reply_id}")
    else:
        print("   ⚠️ 首回覆發布未成功")

    # 6. 登記文案與圖片物理雜湊
    print("6️⃣ [雜湊入庫] 正在將文案與圖片雜湊寫入永久去重庫...")
    register_published_text_hash(POST_TEXT, post_id)
    register_published_image_hash(IMAGE_PATH, post_id, topic="耍廢日常")
    print("   ✅ 物理雜湊永久封裝入庫完成！")

    # 7. 登記常態反饋測試 (對照組 [])
    print("7️⃣ [反饋登記] 正在將貼文登記至 feedback_posts.json (對照組 [])...")
    entry = log_post(post_id, [], POST_TEXT, hot_trend=False)
    print(f"   ✅ 成功登記對照組: is_control={entry.get('is_control')}, k_ids={entry.get('k_ids')}")

    print("=" * 60)
    print("✨ 發布任務 100% 圓滿達成！")
    print(f"貼文 ID: {post_id}")
    print(f"永久連結: {permalink}")
    print(f"貼文原文:\n{POST_TEXT}")
    print("=" * 60)

if __name__ == "__main__":
    main()
