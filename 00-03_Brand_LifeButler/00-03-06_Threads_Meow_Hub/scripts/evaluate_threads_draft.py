import re
import sys
from pathlib import Path

# 確保 Windows 支援 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def evaluate_threads_draft(text):
    """
    依據 2026 Threads 演算法與社群心理學，對草稿進行五維度品質審計 (滿分 100 分)
    1. 開頭懸念鉤子 (Hook Strength) - 20分
    2. 排版呼吸感與行距 (Breathing Room) - 20分
    3. 零硬廣與無外連安全度 (Zero Hard-Ads & Link Safety) - 20分
    4. 雙簧人設與真實自嘲 (Vulnerability & Authenticity) - 20分
    5. 結尾對話鉤子 (Open-Loop Ending) - 20分
    """
    score = 0
    feedback = []

    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    if not lines:
        return 0, ["❌ 內容為空"]

    # 1. 鉤子審計 (前兩行)
    first_two = " ".join(lines[:2])
    forbidden_greetings = ["大家好", "哈囉大家", "今天小編要", "推薦大家", "限時特惠"]
    if any(g in first_two for g in forbidden_greetings):
        feedback.append("⚠️ 開頭有陳舊問候或推銷廢話，降低用戶滑動暫停率 (-10)")
        score += 10
    elif any(k in first_two for k in ["全台灣", "到底", "剛剛", "大吵", "我就問", "報告", "宣佈", "最難"]):
        feedback.append("✅ 開頭鉤子張力極強，精準創造認知失調 (+20)")
        score += 20
    else:
        feedback.append("🟡 開頭鉤子平鋪直敘，建議加入反問或驚訝語氣 (+14)")
        score += 14

    # 2. 排版呼吸感審計
    avg_line_len = sum(len(l) for l in lines) / len(lines)
    if avg_line_len <= 25 and len(lines) >= 5:
        feedback.append("✅ 句子短促，換行頻率高，完美符合脆友呼吸感閱讀習慣 (+20)")
        score += 20
    elif avg_line_len > 35:
        feedback.append("⚠️ 單行字數偏長（大於35字），在手機小螢幕容易形成閱讀壓迫感 (-8)")
        score += 12
    else:
        score += 16
        feedback.append("🟡 排版尚可，可多嘗試一兩句話即換行 (+16)")

    # 3. 零硬廣與外連審計
    if re.search(r"https?://", text):
        feedback.append("❌ 致命扣分：內文檢測到外部超連結！演算法將嚴重抑制推播 (-20)")
    else:
        score += 20
        feedback.append("✅ 安全合規：內文無外部超連結，零觸發降權風險 (+20)")

    hard_sell_words = ["特價", "滿千免運", "點擊購買", "下單連結", "搶購"]
    if any(w in text for w in hard_sell_words):
        feedback.append("⚠️ 內文帶有硬廣字眼，容易激發脆友心理防禦 (-10)")
        score -= 10

    # 4. 雙簧人設與真實自嘲審計
    has_boss = any(k in text for k in ["闆仔", "老闆", "品碩", "外送", "安全帽", "算帳"])
    has_meow = any(k in text for k in ["喵", "貓", "本喵", "罐罐", "爪子"])
    if has_boss and has_meow:
        feedback.append("✅ 完美調用『貓咪前台 ＋ 闆仔男主角』雙簧人設，故事性與親民感極高 (+20)")
        score += 20
    elif has_boss or has_meow:
        feedback.append("🟡 僅帶入單一人設，建議加入貓咪吐槽或老闆實幹細節 (+15)")
        score += 15
    else:
        feedback.append("⚠️ 缺乏生活管家專屬人設識別，易流於大眾文案 (+8)")
        score += 8

    # 5. 結尾對話鉤子審計
    last_two = " ".join(lines[-2:])
    if any(k in last_two for k in ["？", "?", "舉手", "留言", "告訴我", "抄作業", "哪一種", "還是"]):
        feedback.append("✅ 結尾成功拋出開放式提問，強力誘發網友在留言區互動 (+20)")
        score += 20
    else:
        feedback.append("⚠️ 結尾缺乏對話鉤子，容易被已讀不回 (-10)")
        score += 10

    return max(0, min(100, score)), feedback

if __name__ == "__main__":
    test_draft = """
我就問全台灣，
到底有多少人跟我一樣，
每次滿懷信心想煎一條金黃酥脆的午仔魚，
起鍋時整條魚皮全部黏在鍋底，
端上桌直接變成「乾煎骨肉分離魚」的？？？

闆仔剛剛在廚房看不下去，
敲我腦袋傳授了四字口訣：

「乾、熱、定、晃」

今天照這招煎，
真的金黃酥脆到像居酒屋大廚做的！
有被魚皮背叛過的人，在留言區舉個手取暖一下喵...👇
"""
    score, report = evaluate_threads_draft(test_draft)
    print(f"🏆 草稿評分: {score} / 100")
    for r in report:
        print("  ", r)
