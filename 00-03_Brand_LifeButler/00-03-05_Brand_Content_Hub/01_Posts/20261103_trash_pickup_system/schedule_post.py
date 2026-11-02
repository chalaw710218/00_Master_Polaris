import sys
import datetime
import zoneinfo
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
FB_TOKEN = env.get('FB_PAGE_ACCESS_TOKEN')
FB_PAGE_ID = '110505444816362'
img_path = Path(r'00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/01_Posts/20261103_trash_pickup_system/vespa_suit_trash_truck.jpg')

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

tz = zoneinfo.ZoneInfo('Asia/Taipei')
target_dt = datetime.datetime(2026, 11, 3, 8, 30, 0, tzinfo=tz)
scheduled_ts = int(target_dt.timestamp())

print("1. 正在上傳圖片至 Facebook Page 暫存區 (published=false)...")
url_photo = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
with open(img_path, 'rb') as f:
    r_photo = requests.post(url_photo, files={'source': f}, data={
        'access_token': FB_TOKEN,
        'published': 'false'
    })
photo_data = r_photo.json()
print("Photo response:", photo_data)

photo_id = photo_data.get('id')
if not photo_id:
    print("❌ 圖片上傳失敗")
    sys.exit(1)

# 取得 CDN URL
url_query = f"https://graph.facebook.com/v20.0/{photo_id}?fields=images&access_token={FB_TOKEN}"
r_query = requests.get(url_query).json()
cdn_url = r_query.get('images', [{}])[0].get('source')
print("CDN URL 獲取成功:", cdn_url)

print(f"2. 正在向 Facebook Page 提交 8:30 預約排程: {target_dt} (TS: {scheduled_ts})...")
url_feed = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
payload = {
    'access_token': FB_TOKEN,
    'message': message,
    'attached_media[0]': f'{{"media_fbid":"{photo_id}"}}',
    'published': 'false',
    'scheduled_publish_time': scheduled_ts
}
r_feed = requests.post(url_feed, data=payload).json()
print("Feed schedule response:", r_feed)

if 'id' in r_feed:
    post_id = r_feed['id']
    print(f"✅ Facebook 粉絲專頁排程成功！Post ID: {post_id}，預計於 2026-11-03 08:30:00 自動公開發布！")
    
    # 儲存排程資訊供 Threads 排程腳本調用
    info = {
        "fb_post_id": post_id,
        "photo_id": photo_id,
        "cdn_url": cdn_url,
        "target_time": "2026-11-03 08:30:00",
        "timestamp": scheduled_ts
    }
    import json
    with open("00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/01_Posts/20261103_trash_pickup_system/schedule_info.json", "w", encoding="utf-8") as f_out:
        json.dump(info, f_out, ensure_ascii=False, indent=2)
else:
    print("❌ Facebook 排程發布失敗:", r_feed)
