import sys
import time
import requests
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
import json
info_path = Path("00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/01_Posts/20261103_trash_pickup_system/schedule_info.json")
cdn_url = None
if info_path.exists():
    with open(info_path, "r", encoding="utf-8") as f:
        info = json.load(f)
        cdn_url = info.get("cdn_url")

message = """【我獨自倒垃圾的人生升級系統】

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
我們真正做的是幫你卸下生活中的瑣碎麻煩，讓你拿回人生的主導權，把省下來的時間，留給家人或更重要的事情上！

至於……這套服務的費用怎麼計算？
下回分曉！

你可以先加入我們的 LINE 官方帳號詢問，但我可能暫時不會回覆你，因為……「我就說了，下回分曉！」🤣
想掌握第一手資訊？歡迎隨時加入！

Ps.圖是P的，請勿模仿！感謝原Po"""

def publish_threads():
    if not USER_ID or not TOKEN:
        print("❌ 錯誤：尚未設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN")
        return None

    print("🚀 正在發布 Threads 貼文...")
    payload = {
        "access_token": TOKEN,
        "text": message,
        "media_type": "IMAGE" if cdn_url else "TEXT"
    }
    if cdn_url:
        payload["image_url"] = cdn_url

    r1 = requests.post(f"{API_BASE}/{USER_ID}/threads", data=payload).json()
    creation_id = r1.get("id")
    if not creation_id:
        print(f"❌ 建立 Threads 容器失敗: {r1}")
        return None

    time.sleep(3)

    r2 = requests.post(f"{API_BASE}/{USER_ID}/threads_publish", data={
        "access_token": TOKEN,
        "creation_id": creation_id
    }).json()

    post_id = r2.get("id")
    if post_id:
        print(f"🎉 Threads 發布成功！Post ID: {post_id}")
        url = f"https://www.threads.net/@/post/{post_id}"
        print(f"🔗 貼文網址: {url}")
        
        # 存檔至 Published Archive
        archive_path = Path("00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/03_Published_Archive.md")
        if archive_path.exists():
            with open(archive_path, "a", encoding="utf-8") as f:
                f.write(f"\n- **[2026-11-03 08:30] 【我獨自倒垃圾的人生升級系統】** (Post ID: `{post_id}`) | [查看貼文]({url})\n")
        return post_id
    else:
        print(f"❌ Threads 發布失敗: {r2}")
        return None

if __name__ == "__main__":
    publish_threads()
