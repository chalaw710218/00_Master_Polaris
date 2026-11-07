import os
import sys
import json
import time
import requests
from pathlib import Path

# 確保 Windows 終端機支援 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]

# 讀取 .secrets.env
ENV_PATH = ROOT_DIR / ".secrets.env"
def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

ENV = load_env(ENV_PATH)
PAGE_ID = "110505444816362"
TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")

if not TOKEN:
    print("❌ 錯誤：未找到 FB_PAGE_ACCESS_TOKEN！")
    sys.exit(1)

IMAGE_PATH = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-08_Productized_Services" / "02_外圈代倒垃圾包月_999與1999" / "images" / "boss_suit_chasing_trash_truck.jpg"

if not IMAGE_PATH.exists():
    print(f"❌ 找不到圖片檔案: {IMAGE_PATH}")
    sys.exit(1)

MESSAGE = """花蓮有最速之男「楊俊瀚」🏃💨
但台東呢？

台東有最垃圾之男——「我們家闆仔」🤣！

每天傍晚在台東街頭，
你看到穿著西裝筆挺、皮鞋鋥亮、頭戴安全帽，
手裡卻提著一大袋廚餘垃圾在馬路上玩命狂奔的……
沒錯，那就是他。

他不是在趕著簽千萬合約，
他是在幫台東人追垃圾車。🗑️

「這輩子，別再為了追垃圾車狼狽衝刺了，把狼狽留給闆仔就好。」

⚠️ 先說好我們的規矩：
1. 我們只收【家庭生活垃圾＋資源回收】（裝潢廢土大卡車請放過我們機車後座）
2. 每次限 20L 兩包（含回收，超過會拍照留證併入下月帳單）
3. 絕不背外送便當的保溫箱出勤，100% 衛生無交叉污染！

🌿【方案只有兩種】：
• 999 輕量包（每週 2 次，小家庭救星）
• 1,999 旗艦包（每週 5 次全收運日天天清，垃圾絕不過夜）

想把傍晚時間留給晚餐跟家人的，
預約登記資訊管家已整理在【第一則留言】中，或直接私訊粉專小盒子，闆仔明天就去你家門口幫你追車！👇"""

FIRST_COMMENT_TEXT = """🛎️【闆仔在線回覆・需求登記專區】：

各位台東鄉親，需要代倒垃圾服務的朋友：
👉 歡迎直接「私訊粉專小盒子」或在底下留言「+1」！
👉 也可直接點擊加入生活管家專屬 LINE 官方帳號：
https://lin.ee/z83YSq6

闆仔會傳需求登記表單給您，並親自跟您敲時間到府確認門前放置點！
（真的只收家庭垃圾喔，拜託不要偷塞彈簧床給我～🛵💨）

📍【生活管家服務樞紐】
• 家宅地址：台東市正氣北路166巷90號
• 服務區域：台東市區各主要生活圈專人定時機車清運"""

print("📤 [步驟 1] 上傳西裝追車實拍照至 Facebook 暫存區...")
url_photo = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
try:
    with open(IMAGE_PATH, "rb") as f:
        files = {"source": f}
        data = {"access_token": TOKEN, "published": "false"}
        r = requests.post(url_photo, files=files, data=data, timeout=30)
        photo_data = r.json()
        photo_id = photo_data.get("id")
        if not photo_id:
            print(f"❌ 圖片上傳失敗: {photo_data}")
            sys.exit(1)
        print(f"✅ 成功上傳圖片 ID: {photo_id}")
except Exception as e:
    print(f"❌ 上傳圖片異常: {e}")
    sys.exit(1)

print("\n🚀 [步驟 2] 發布 Facebook 圖文貼文...")
url_feed = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
payload = {
    "access_token": TOKEN,
    "message": MESSAGE,
    "attached_media[0]": f'{{"media_fbid":"{photo_id}"}}',
    "published": True
}

r2 = requests.post(url_feed, data=payload, timeout=30)
result = r2.json()

if "id" not in result:
    print(f"❌ 貼文發布失敗: {result}")
    sys.exit(1)

post_id = result["id"]
print(f"🎉 Facebook 貼文即時發布成功！Post ID: {post_id}")

print("\n💬 [步驟 3] 發表第一則留言（置入 LINE 與登記導流）...")
time.sleep(2)
url_comment = f"https://graph.facebook.com/v20.0/{post_id}/comments"
comment_payload = {
    "access_token": TOKEN,
    "message": FIRST_COMMENT_TEXT
}
r_comment = requests.post(url_comment, data=comment_payload, timeout=20)
c_res = r_comment.json()

comment_id = c_res.get("id")
if comment_id:
    print(f"✅ 第一則留言發布成功！Comment ID: {comment_id}")
else:
    print(f"⚠️ 第一則留言未成功: {c_res}")

# 記錄於粉專貼文紀錄
archive_path = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-05_Brand_Content_Hub" / "00_Social_Posts_Master_Archive.md"
try:
    archive_entry = f"""
### 【FB 發布】台東最垃圾之男・代倒垃圾服務上線 🗑️🏃💨
- **發布時間**：{time.strftime("%Y-%m-%d %H:%M:%S")}
- **FB Post ID**：`{post_id}`
- **Comment ID**：`{comment_id}`
- **圖片**：`boss_suit_chasing_trash_truck.jpg`
- **粉專專頁**：生活的一部分，就醬點！
"""
    if archive_path.exists():
        with open(archive_path, "a", encoding="utf-8") as af:
            af.write(archive_entry)
        print("📁 已自動歸檔至 00_Social_Posts_Master_Archive.md！")
except Exception as e:
    print(f"⚠️ 歸檔提示: {e}")

print("\n🏁 Facebook 發文與首則留言閉環全部完成！")
