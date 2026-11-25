"""
publish_tonight_midnight_post.py — 今晚深夜檔次生活管家圖文發布腳本
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from threads_publisher import publish_thread
from image_hash_gate import check_image_poka_yoke, register_published_image_hash
from text_hash_gate import check_text_poka_yoke, register_published_text_hash
from topic_safety_gate import check_topic_safety
from service_truth_gate import check_service_truth_poka_yoke

POST_TEXT = (
    "深夜十一點半的台東，夜風把老木窗吹得微微發響。\n"
    "剛剛在書桌前把一整天的筆記收尾，手邊這杯熱茶還留著淡淡的炒米香。\n\n"
    "忙碌了一整天，不管今天有多匆忙、或是心裡有什麼還沒解開的結，\n"
    "回到家、洗過熱水澡之後，這個夜晚就該只屬於你自己。\n\n"
    "不用急著向世界證明什麼，也不用焦慮明天的行事曆。\n"
    "把手機調成靜音，替自己倒杯溫水或熱茶，\n"
    "讓肩頸在安靜的黃光裡慢慢放鬆下來。\n\n"
    "今晚，生活管家替你留一盞燈。\n"
    "大家晚安，好好睡一覺。"
)

def main(image_path: str):
    img = Path(image_path)
    if not img.exists():
        print(f"❌ 找不到指定圖片檔案: {img}")
        sys.exit(1)

    print("=== 開始執行全套發布前安燈質檢門禁 ===")

    # 1. 圖片雜湊防呆
    print("1. 正在檢查圖片 SHA-256 物理雜湊...")
    is_img_ok, img_err = check_image_poka_yoke(str(img))
    if not is_img_ok:
        print(f"🛑 圖片安燈硬攔截: {img_err}")
        sys.exit(1)
    print("   ✅ 圖片 SHA-256 檢驗合格（全新未發布照片）！")

    # 2. 文本雜湊與相似度防呆
    print("2. 正在檢查文本雜湊與前台相似度...")
    is_txt_ok, txt_err = check_text_poka_yoke(POST_TEXT)
    if not is_txt_ok:
        print(f"🛑 文本安燈硬攔截: {txt_err}")
        sys.exit(1)
    print("   ✅ 文本雜湊與相似度檢驗合格（100% 原創新文案）！")

    # 3. 主題安全防呆
    print("3. 正在檢查敏感詞與話題安全...")
    is_safe, safe_err = check_topic_safety(POST_TEXT)
    if not is_safe:
        print(f"🛑 話題安燈硬攔截: {safe_err}")
        sys.exit(1)
    print("   ✅ 話題安全檢驗合格！")

    # 4. 服務真實性防呆
    print("4. 正在檢查服務真實性...")
    is_truth, truth_err = check_service_truth_poka_yoke(POST_TEXT)
    if not is_truth:
        print(f"🛑 服務真實性硬攔截: {truth_err}")
        sys.exit(1)
    print("   ✅ 服務真實性檢驗合格！")

    # 5. 正式發布
    print("\n🚀 所有門禁全數通過，正式發送至 Threads API...")
    post_id = publish_thread(
        text=POST_TEXT,
        image=str(img),
        topic_tag="台東生活"
    )

    if not post_id:
        print("❌ 發布失敗！")
        sys.exit(1)

    print(f"\n🎉 貼文發布大成功！Threads Post ID: {post_id}")

    # 6. 註冊圖片與文本雜湊
    print("正在將圖片與文本雜湊永久封裝入庫...")
    register_published_image_hash(str(img), post_id)
    register_published_text_hash(POST_TEXT, post_id)
    print("✅ 雜湊庫更新完成，終生防重複！")

    return post_id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python publish_tonight_midnight_post.py <圖片路徑>")
        sys.exit(1)
    main(sys.argv[1])
