import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container

img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts\TH_02_ChatGPT_Fluff_Red_Cross.jpg"
if not os.path.exists(img_path):
    img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_02_ChatGPT_Fluff_Red_Cross.jpg"

th_message = """「問 AI 怎麼改善小店生意，它永遠回我三千字教科書廢話。」

很多台東在地老闆跟我吐過苦水：
問 AI 怎麼做行銷，它叫你「加強社群宣傳、推出促銷優惠、精準鎖定受眾」。
幹！誰不知道？！預算就兩萬、店裡就兩個人，到底要怎麼做？！

其實不能怪 AI 笨。
是你一開局就急著向它求答案，脈絡根本沒熱身！

AI 就像個頂尖高材生，你不給它真實背景，它只能背教科書給你看。
想讓它吐出刀刀見血的解法，只需要換個問法：
1. 先鋪全景：把菜單、真實客群與平日營業額一次塞給它，嚴禁它給建議。
2. 再逼細節：鎖死預算、人力與時間，把教科書空話全部堵死。
3. 飽和求解：脈絡餵飽了才要清單，吐出來的答案立刻就能用。

下週三下午在台東家宅，我現場帶大家實戰演練一次。
純實體巡桌排錯，限額 10 席。

留言區放申請表，老學員 0 元免單。"""

th_first_comment = """🐾 11/11 (週三) 14:00《AI 家教實戰系列班 · 第 1 講》
• 實體限額 10 席，現場巡桌排錯，沒做完專屬成果不准下課
• 學費：新朋友 $500 / 老學員 0 元免單回娘家
• 流程：填表後由導師審查，審查通過會寄 Email 通知繳費與報到，確認完成才鎖定席次
• 申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
• 地點：台東市正氣北路166巷90號（家宅）"""

print("=" * 50)
print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序 (Post 02)...")
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

print("\n" + "=" * 50)
print("🏁 Threads Post 02 發射完成！")
print(f"📱 Threads: {th_url}")
print("=" * 50)
