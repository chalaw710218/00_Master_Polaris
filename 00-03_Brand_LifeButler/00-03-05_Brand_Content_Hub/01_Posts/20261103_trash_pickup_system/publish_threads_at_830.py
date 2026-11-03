# -*- coding: utf-8 -*-
import sys
import time
import requests
import json
from pathlib import Path

# Fix Windows console UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_env():
    cur = Path.cwd()
    for parent in [cur] + list(cur.parents):
        env_file = parent / '.secrets.env'
        if env_file.exists():
            env_vars = {}
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        env_vars[k.strip()] = v.strip()
            return env_vars
    return {}

env = load_env()
USER_ID = env.get("THREADS_USER_ID")
TOKEN = env.get("THREADS_ACCESS_TOKEN")
API_BASE = "https://graph.threads.net/v1.0"

# 載入排程資訊取得 CDN URL
info_path = Path("00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/01_Posts/20261103_trash_pickup_system/schedule_info.json")
cdn_url = None
if info_path.exists():
    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)
        cdn_url = info.get("cdn_url")

main_text = """【我獨自倒垃圾的人生升級系統】

相信很多男人被老婆指使去倒垃圾，心裡都是心不甘情不願的，總覺得倒垃圾既瑣碎又浪費時間。
老實說，以前的我也一樣。
但自從那次開始，我徹底愛上了倒垃圾這件事！

那天，一位熟悉的老客戶問我：
「品碩，我下午傍晚都要去接送小孩，根本趕不上垃圾車的時間，能不能請你順便幫我倒垃圾？」
我爽快回她：「好啊！」

於是我們約定好時間，定時定點到她家門口收走垃圾，準時送上垃圾車。
那一刻，我拎著手中的兩袋垃圾，心裡突然有種奇妙的衝擊：
原來，別人眼中的日常麻煩，是可以被轉化為真金白銀的服務價值。

這項服務默默試行了一年多的時間，如今也終於被我抓出了一套標準 SOP——包括什麼時候分類回收、袋子的大小該如何規範、甚至怎麼安排路線追垃圾車最省時省力。

生活管家在做的，從來不是這一趟跑腿要算多少錢。
我們真正做的是幫你卸下生活中的瑣碎麻煩，讓你拿回人生的主導權，把省下來的時間，留給家人或更重要的事情上！（續下文👇）

Ps.圖是P的，請勿模仿！感謝原Po"""

reply_text = """至於……這套服務的費用怎麼計算？
下回分曉！

你可以先加入我們的 LINE 官方帳號詢問，但我可能暫時不會回覆你，因為……「我就說了，下回分曉！」🤣
想掌握第一手資訊？歡迎隨時加入！

生活管家，為你搞定生活瑣事，把時間留給最重要的人。"""

def publish_threads():
    if not USER_ID or not TOKEN:
        print("❌ 錯誤：尚未設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN")
        return None

    print(f"🚀 主貼文字數: {len(main_text)} 字，正在建立主貼文容器...")
    payload1 = {
        "access_token": TOKEN,
        "text": main_text,
        "media_type": "IMAGE" if cdn_url else "TEXT"
    }
    if cdn_url:
        payload1["image_url"] = cdn_url

    r1 = requests.post(f"{API_BASE}/{USER_ID}/threads", data=payload1).json()
    creation_id = r1.get("id")
    if not creation_id:
        print(f"❌ 建立主貼容器失敗: {r1}")
        return None

    print(f"⏳ 主貼容器建立成功 ({creation_id})，等待 3 秒發布...")
    time.sleep(3)

    r2 = requests.post(f"{API_BASE}/{USER_ID}/threads_publish", data={
        "access_token": TOKEN,
        "creation_id": creation_id
    }).json()

    post_id = r2.get("id")
    if not post_id:
        print(f"❌ 主貼發布失敗: {r2}")
        return None

    print(f"🎉 主貼發布成功！Post ID: {post_id}")
    print(f"🔗 主貼網址: https://www.threads.net/@/post/{post_id}")

    # 建立串接留言 (Reply)
    print(f"🚀 正在串接第一則作者回覆（續篇與 LINE 引流）...")
    payload2 = {
        "access_token": TOKEN,
        "text": reply_text,
        "reply_to_id": post_id,
        "media_type": "TEXT"
    }
    r3 = requests.post(f"{API_BASE}/{USER_ID}/threads", data=payload2).json()
    reply_creation_id = r3.get("id")
    if reply_creation_id:
        time.sleep(2)
        r4 = requests.post(f"{API_BASE}/{USER_ID}/threads_publish", data={
            "access_token": TOKEN,
            "creation_id": reply_creation_id
        }).json()
        reply_post_id = r4.get("id")
        if reply_post_id:
            print(f"🎉 串接回覆發布成功！Reply ID: {reply_post_id}")
        else:
            print(f"⚠️ 串接回覆發布未回顯 ID: {r4}")
    else:
        print(f"⚠️ 建立串接回覆容器失敗: {r3}")

    # 更新 schedule_info.json
    if info_path.exists():
        with open(info_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["threads_post_id"] = post_id
        data["threads_published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return post_id

if __name__ == "__main__":
    publish_threads()
