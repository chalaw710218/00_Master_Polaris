"""第一軌：發布前質量閘門 (Pre-Flight Quality Gate)

用法：
  python preflight_audit.py --file draft.txt [--persona meow|shadow] [--threshold 90]
  python preflight_audit.py --text "草稿內容..."
  echo 草稿 | python preflight_audit.py

退出碼：0 = 通過 (>= threshold 且無致命項)；1 = 打回重寫。
"""
import argparse
import re
import sys

from _common import *  # noqa: F401,F403  (含 UTF-8 設定)

BAIT_WORDS = ["留言+1", "留言 +1", "+1", "快來買", "限時搶購", "限時", "搶購", "手慢無", "最後機會", "錯過可惜"]
HARD_SELL = ["特價", "滿千免運", "點擊購買", "下單連結", "優惠碼"]
STALE_GREETINGS = ["大家好", "哈囉大家", "今天小編要", "推薦大家"]
HOOK_WORDS = ["全台灣", "到底", "剛剛", "我就問", "報告", "宣佈", "這合理嗎", "居然", "竟然", "？？"]
CTA_WORDS = ["？", "?", "舉手", "留言區", "告訴我", "回報", "報個", "哪一種", "還是"]
BOSS_WORDS = ["闆仔", "老闆", "品碩"]
CAT_WORDS = ["喵", "貓", "本喵", "罐罐", "爪"]


def audit(text, persona="meow"):
    """回傳 (score, fatal, items)；items 為 (等級, 訊息)。"""
    score, fatal, items = 0, [], []
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return 0, ["內容為空"], [("❌", "內容為空")]

    # 1. 鉤子 (20)
    first_two = " ".join(lines[:2])
    if any(g in first_two for g in STALE_GREETINGS):
        score += 8
        items.append(("⚠️", "開頭為陳舊問候/推銷語，降低停留率 (+8)"))
    elif any(k in first_two for k in HOOK_WORDS):
        score += 20
        items.append(("✅", "開頭鉤子具認知失調張力 (+20)"))
    else:
        score += 13
        items.append(("🟡", "開頭平鋪直敘，建議加入反差或反問 (+13)"))

    # 2. 呼吸感 (20)
    avg = sum(len(l) for l in lines) / len(lines)
    if avg <= 25 and len(lines) >= 5:
        score += 20
        items.append(("✅", f"短句多換行，平均每行 {avg:.0f} 字 (+20)"))
    elif avg > 35:
        score += 10
        items.append(("⚠️", f"平均每行 {avg:.0f} 字，手機閱讀壓迫 (+10)"))
    else:
        score += 15
        items.append(("🟡", f"排版尚可，平均每行 {avg:.0f} 字 (+15)"))

    # 3. 零外鏈與無硬廣 (20)
    if re.search(r"https?://|www\.", text):
        fatal.append("內文含外部連結（演算法降權）")
        items.append(("❌", "致命：內文含外部連結 (+0)"))
    elif any(w in text for w in HARD_SELL):
        score += 10
        items.append(("⚠️", "含硬廣字眼，易觸發心理防禦 (+10)"))
    else:
        score += 20
        items.append(("✅", "零外鏈、無硬廣 (+20)"))

    # 4. 人設 (20)
    has_boss = any(k in text for k in BOSS_WORDS)
    has_cat = any(k in text for k in CAT_WORDS)
    if persona == "meow":
        if "本貓" in text:
            fatal.append("喵編誤用「本貓」（唯一許可：本喵）")
            items.append(("❌", "致命：喵編誤用「本貓」"))
        elif has_boss and has_cat:
            score += 20
            items.append(("✅", "貓咪×闆仔雙簧人設完整 (+20)"))
        else:
            score += 14
            items.append(("🟡", "僅單一人設，建議補上闆仔或貓咪視角 (+14)"))
        if "本喵" not in text:
            items.append(("🟡", "喵編貼文未出現「本喵」，確認人稱是否正確"))
    else:
        score += 20 if has_boss or "小編" in text else 12
        items.append(("✅" if has_boss or "小編" in text else "🟡", "小編視角人設檢查"))

    # 5. 結尾對話鉤子 (20)
    last_two = " ".join(lines[-2:])
    if any(k in last_two for k in CTA_WORDS):
        score += 20
        items.append(("✅", "結尾為開放式提問，誘發留言 (+20)"))
    else:
        score += 8
        items.append(("⚠️", "結尾缺乏對話鉤子 (+8)"))

    # 致命守則（不計分，直接打回）
    hits = [w for w in BAIT_WORDS if w in text]
    if hits:
        fatal.append(f"含急迫/誘餌字眼：{', '.join(hits)}")
        items.append(("❌", f"致命：誘餌/急迫字眼 {hits}"))
    if len(text) > 500:
        fatal.append(f"字數 {len(text)} 超過 Threads 500 字上限")
        items.append(("❌", f"致命：字數 {len(text)} > 500"))

    return max(0, min(100, score)), fatal, items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--text")
    ap.add_argument("--persona", default="meow", choices=["meow", "shadow"])
    ap.add_argument("--threshold", type=int, default=90)
    a = ap.parse_args()

    if a.file:
        text = open(a.file, "r", encoding="utf-8").read()
    elif a.text:
        text = a.text
    else:
        text = sys.stdin.read()

    score, fatal, items = audit(text, a.persona)
    print(f"🏆 發布前審計分數：{score} / 100（門檻 {a.threshold}）")
    for lvl, msg in items:
        print(f"  {lvl} {msg}")
    if fatal or score < a.threshold:
        print("\n🛑 打回重寫：" + ("；".join(fatal) if fatal else f"分數低於門檻 {a.threshold}"))
        sys.exit(1)
    print("\n🟢 通過質量閘門，可以發布。")


if __name__ == "__main__":
    main()
