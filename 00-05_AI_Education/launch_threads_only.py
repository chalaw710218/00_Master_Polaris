import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container

img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts\TH_Desk_Scene_AI_Delivery.jpg"
if not os.path.exists(img_path):
    img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_Desk_Scene_AI_Delivery.jpg"

th_message = """做物流、管店鋪這些年，最深的體會只有一個：
我們的時間真的永遠不夠用。

每天忙完店裡的雜事坐下來，夜深了，小孩也睡了。
那麼努力打拼是為了家人，結果連陪他們好好吃頓飯的時間都被吃光。

這幾個月我用 AI 打造了一套辦公室，幫我把資料整理好。
不是為了追什麼科技潮流，只是想把屬於自己的時間和主導權買回來，活得從容一點。

下週三下午在台東家宅，我開一間小教室，手把手帶大家做一次。
限 10 個人，多一張椅子都沒有。

留言區放表單，想把時間找回來的來喝杯茶吧。"""

th_first_comment = """🐾 11/11 (週三) 14:00《AI 家教實戰系列班 · 第 1 講》
• 實體限額 10 席，沒做完專屬成果不准下課
• 學費：新朋友 $500 / 老學員 0 元免單回娘家
• 流程：填表後由導師審查，審查通過會寄 Email 通知繳費與報到，確認完成才鎖定席次
• 申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
• 地點：台東市正氣北路166巷90號（家宅）"""

print("=" * 50)
print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序...")
print("=" * 50)

# 上傳圖片至 Meta CDN
print(f"📤 正在託管 Threads 配圖至 Meta CDN: {img_path}")
cdn_url = upload_local_image_to_meta_cdn(img_path)
if not cdn_url:
    print("⚠️ 無法取得 CDN 網址，將以純文字發布！")

# 建立主貼文容器
creation_id = create_media_container(
    text=th_message,
    image_url=cdn_url,
    topic_tag="生活服務"
)

if not creation_id:
    print("❌ Threads 建立貼文容器失敗！")
    sys.exit(1)

time.sleep(3)
post_id = publish_container(creation_id)
if not post_id:
    print("❌ Threads 主貼文發布失敗！")
    sys.exit(1)

th_url = f"https://www.threads.net/@hellotaitung/post/{post_id}"
print(f"🎉 Threads 主貼文發布成功！Post ID: {post_id}")
print(f"🔗 Threads 貼文網址: {th_url}")

# 發表 Threads 首留言橋接
print("💬 正在發布 Threads 首則留言（表單連結）...")
time.sleep(3)
reply_creation_id = create_media_container(
    text=th_first_comment,
    reply_to_id=post_id
)

if reply_creation_id:
    time.sleep(2)
    reply_id = publish_container(reply_creation_id)
    if reply_id:
        print(f"✅ Threads 首則留言發布成功！Reply ID: {reply_id}")
    else:
        print("⚠️ Threads 首留言發布失敗")
else:
    print("⚠️ Threads 建立留言容器失敗")

print("\n🏁 Threads 發射全流程閉環完畢！")
