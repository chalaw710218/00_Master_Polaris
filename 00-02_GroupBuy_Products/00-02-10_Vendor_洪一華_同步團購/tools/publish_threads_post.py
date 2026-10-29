# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# Ensure utf-8 output in Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

THREADS_HUB_SCRIPTS = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
sys.path.insert(0, str(THREADS_HUB_SCRIPTS))

from threads_publisher import publish_thread

# 創辦人親定鐵律：Threads 上絕不使用「闆仔」，純粹由「小編（影）」與「喵編」搭檔演繹！
POST_TEXT = """(測試文)下單不列入計算！
我就問到底有多少人跟本喵一樣，以前總覺得雞胸肉又乾又柴像在啃木頭？🐱

今天趁小編去廚房忙著備料，本喵偷偷霸佔餐桌！
（小編影在旁白扶額：好啦，喵編剛剛蹲在桌邊眼巴巴盯著那盤肉，是在催我快點公開多汁的秘密...）

這盤煎到金黃爆汁的土雞清肉，真的不是五星級大廚魔法，全靠我們挑選時死守的那套標準：
認明「工廠直出一次急凍」的安心土雞，沒有反覆退冰灌水，肉質本身的鮮甜與天然白胺酸全被鎖死在纖維裡✨
下鍋前 5% 鹽水泡半小時，逆著紋路垂直切，大火煎香後關火蓋鍋燜熟，咬下去真的爆汁！

每天在外打拚生活已經夠辛苦了，回家吃飯真的別再委屈嘴巴喵～

想看這批土雞清肉完整規格的，第一則留言本喵偷放任意門給你們（跑走🐾）"""

IMAGE_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\04_Shadow_Kage_Operative\images\meow_chicken_breast_lunch.jpg")

print(f"📝 貼文字數: {len(POST_TEXT)} 字")
print(f"🖼️ 配圖路徑: {IMAGE_PATH} (存在: {IMAGE_PATH.exists()})")

# 檢查是否有違禁詞「闆仔」
if "闆仔" in POST_TEXT:
    print("❌ 攔截：貼文中包含違禁詞【闆仔】！Threads 嚴禁使用！")
    sys.exit(1)

post_id = publish_thread(
    text=POST_TEXT,
    image=str(IMAGE_PATH),
    topic_tag="美食外送"
)

if post_id:
    print(f"\n🎉 影 ✕ 喵編 Threads 純雙軌發布大成功！")
    print(f"🔗 Threads 串文連結: https://www.threads.net/@hellotaitung/post/{post_id}")
    
    first_comment = """🐾 喵編任意門在此（小聲說）：
這批「大成安心雞・土雞去皮清肉 500g」是小編今天挖到的寶，工廠直送一次急凍，煮湯炒菜煎排都嫩爆！
因為這篇是系統同步連線測試，下單不列入計算喔～
想看詳細規格與試辦外送的，往這邊走喵👉 https://www.facebook.com/110505444816362_1146589971383238"""
    
    print("\n💬 正在發布喵編的第一則留言引導...")
    comment_id = publish_thread(
        text=first_comment,
        reply_to_id=post_id
    )
    if comment_id:
        print(f"✅ 第一則留言發布成功！Comment ID: {comment_id}")
else:
    print("\n❌ Threads 發布失敗！")
