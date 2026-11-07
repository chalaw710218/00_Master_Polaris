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
sys.path.append(str(SCRIPT_DIR))

from threads_publisher import publish_thread, API_BASE, THREADS_ACCESS_TOKEN
from evaluate_threads_draft import evaluate_threads_draft

POST_TEXT = """花蓮有最速之男「楊俊瀚」🏃💨
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
留言或私訊小盒子，闆仔明天就去你家門口幫你追車！👇"""

FIRST_COMMENT_TEXT = """各位台東鄉親，需求登記請私訊小盒子或在底下留言「+1」！
闆仔會傳預約表單給您，並親自敲時間到府確認門前放置點！
（真的只收家庭垃圾喔，拜託不要偷塞彈簧床給我～🛵💨）"""

IMAGE_PATH = ROOT_DIR / "00-03_Brand_LifeButler" / "00-03-08_Productized_Services" / "02_外圈代倒垃圾包月_999與1999" / "images" / "boss_suit_chasing_trash_truck.jpg"

print(f"🖼️ 檢查圖片路徑: {IMAGE_PATH}")
if not IMAGE_PATH.exists():
    print(f"❌ 找不到圖片檔案: {IMAGE_PATH}")
    sys.exit(1)

print("🔍 [步驟 1] 執行發布前品質審計...")
score, report = evaluate_threads_draft(POST_TEXT)
print(f"🏆 審計得分: {score} / 100")
for r in report:
    print("  ", r)

if score < 90:
    print("❌ 評分未達 90，終止發布！")
    sys.exit(1)

print("\n🚀 [步驟 2] 調用 Meta Threads API 發布主貼文（附西裝追車實拍照）...")
post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="生活服務")

if not post_id:
    print("❌ 主貼文發布失敗！")
    sys.exit(1)

print(f"\n🎉 [步驟 3] 主貼文發布成功！Post ID: {post_id}")

permalink = None
try:
    info_res = requests.get(f"{API_BASE}/{post_id}?fields=id,text,permalink,timestamp&access_token={THREADS_ACCESS_TOKEN}").json()
    permalink = info_res.get("permalink")
    print(f"🔗 貼文公開永久連結: {permalink}")
except Exception as e:
    print(f"⚠️ 查詢 permalink 提示: {e}")

# 稍等 2 秒，啟動首回覆橋接 (First Comment Bridge)
print("\n💬 [步驟 4] 啟動作者首回覆橋接（置入留言導流資訊）...")
time.sleep(2)
comment_id = publish_thread(text=FIRST_COMMENT_TEXT, reply_to_id=post_id)

if comment_id:
    print(f"✨ 首回覆發布成功！Comment ID: {comment_id}")
else:
    print("⚠️ 首回覆發布未成功，請稍後手動補上。")

result = {
    "post_id": post_id,
    "permalink": permalink,
    "comment_id": comment_id,
    "score": score,
    "image_path": str(IMAGE_PATH),
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
}

with open(SCRIPT_DIR / "latest_trash_service_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n🏁 全部發布與首回覆閉環完成！")
