import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 加入 threads_publisher 所在路徑
SCRIPTS_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts"
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container

def launch_threads_01():
    print("=" * 60)
    print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序 —— 第 2 講連載【篇號 01】...")
    print("=" * 60)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_01_No_Photo_Automation.png"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\FB_L02_01_No_Photo_Automation.png"
        
    th_message = """週三下午第 1 講在家宅開練，現場剛好 4 個人。

坦白說，這是我覺得最踏實的事。
因為不用站在台上按投影片應付幾十個人，我可以拉張椅子直接坐在每個人旁邊，認真聽著每間店遇到的困難，看著螢幕一步一步排錯到底。
忙到最後，連一張照片都忘了拍。

但比起擺拍大合照，每個人筆電螢幕亮著做出來的成果最真實。

下週三第 2 講，我們要帶大家消滅最煩的雜事：
串接 Meta 官方 API，Python 3 秒自動排程發 FB 與 Threads，24 小時留言自動秒回。

依然是 6 席極致小班，自備筆電，做完專屬發射台才准走。
表單放第一則留言，下週三見。"""

    th_first_comment = """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講極致小班須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
全班極限 6 席深度陪伴，API 沒跑通不准走。

📅 時間：11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）
🎯 主題：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)
💰 費用：老學員（含第 1 講夥伴）0 元免單 ｜ 新朋友單堂 $500

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""

    print(f"📤 正在託管 Threads 配圖至 Meta CDN: {os.path.basename(img_path)}")
    cdn_url = upload_local_image_to_meta_cdn(img_path)
    if not cdn_url:
        print("⚠️ 無法取得 CDN 網址，將以純文字發布！")
        
    creation_id = create_media_container(
        text=th_message,
        image_url=cdn_url,
        topic_tag="生活服務"
    )
    if not creation_id:
        print("❌ 建立 Threads 貼文容器失敗！")
        return False, None
        
    time.sleep(3)
    post_id = publish_container(creation_id)
    if not post_id:
        print("❌ Threads 主貼文發布失敗！")
        return False, None
        
    th_url = f"https://www.threads.net/@hellotaitung/post/{post_id}"
    print(f"🎉 Threads 主貼文發布成功！Post ID: {post_id}")
    print(f"🔗 Threads 貼文網址: {th_url}")
    
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
        
    return True, th_url

if __name__ == "__main__":
    launch_threads_01()
