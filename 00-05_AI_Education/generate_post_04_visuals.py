import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix"
OUT_DIR_FB = os.path.join(ROOT_DIR, "FB_Posts")
OUT_DIR_TH = os.path.join(ROOT_DIR, "Threads_Posts")
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"

def get_font(size, bold=False):
    font_path = r"C:\Windows\Fonts\msjhbd.ttc" if bold else r"C:\Windows\Fonts\msjh.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# ==========================================
# 1. FB-04: 約瑟夫德式黑金工匠海報 (1200x1200)
# ==========================================
def render_fb_04():
    W, H = 1200, 1200
    # 曜石磨砂碳黑底色 (#121316)，徹底跳脫前三篇米白底！
    bg_color = (18, 19, 22)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 德式雙層燙金幾何外框
    margin = 55
    gold_frame = (197, 168, 102) # 香檳燙金色
    gold_dark = (140, 115, 62)
    draw.rectangle([margin, margin, W - margin, H - margin], outline=gold_dark, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=gold_frame, width=1)
    
    # 四個角落的裝飾性金屬幾何角標
    corner_len = 24
    for cx, cy in [(margin + 12, margin + 12), (W - margin - 12, margin + 12), 
                   (margin + 12, H - margin - 12), (W - margin - 12, H - margin - 12)]:
        dx = 1 if cx == margin + 12 else -1
        dy = 1 if cy == margin + 12 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=(245, 183, 56), width=3)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=(245, 183, 56), width=3)

    # 頂部極簡標籤
    top_y = margin + 35
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教系列班", fill=(180, 160, 125), font=get_font(18, bold=True), anchor="mm")
    
    # 震撼標題區：鐵血承諾 (Level 1)
    title_y = top_y + 60
    draw.text((W // 2, title_y), "「醜話先說在前頭：", fill=(220, 220, 225), font=get_font(46, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 58), "沒做出店裡的專屬成果，", fill=(255, 255, 255), font=get_font(48, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 118), "當天不准下課！」", fill=(245, 183, 56), font=get_font(52, bold=True), anchor="mm") # 燙金大字

    # 緊急警示席次徽章 (Level 2)
    badge_y = title_y + 180
    badge_w, badge_h = 720, 52
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(35, 25, 20), outline=(220, 60, 50), width=2)
    # 左側紅色警告條
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=(220, 60, 50))
    draw.text((W // 2, badge_y + badge_h // 2), "【 緊急戰報 】 10 席實體座位已過半 · 僅剩最後 5 席！", fill=(255, 220, 210), font=get_font(21, bold=True), anchor="mm")

    # 中央視覺區：三週完整課表建築級網格 (400px 高)
    card_y = badge_y + 75
    card_w = 980
    card_h = 390
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(24, 26, 32), outline=gold_dark, width=2)
    
    # 頂部金屬橫條
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(36, 40, 50))
    draw.text((W // 2, card_y + 22), "【 2026 秋季 AI 家教實戰班 · 三週全流程課表 】", fill=gold_frame, font=get_font(18, bold=True), anchor="mm")

    # 三週課表內容
    curriculum = [
        ("第 1 講 ｜ 11/11 (週三) 14:00 - 16:00", "【 NotebookLM 數位大腦 · 漏斗深挖提問法 】", "進貨單/公文一鍵生雙人 Podcast，學會精準餵脈絡，逼 AI 吐出刀刀見血生意解法。（僅剩最後 5 席）", (245, 183, 56)),
        ("第 2 講 ｜ 11/18 (週三) 14:00 - 16:00", "【 Antigravity 操作 · Meta 官方自動發文串接 】", "手把手串接 FB 粉專與 Threads 官方 API！Python 自動排程圖文 ＋ 24 小時留言秒回。", (100, 180, 255)),
        ("第 3 講 ｜ 11/25 (週三) 14:00 - 16:00", "【 資料架構管理 · 擬人化店長分身工程 】", "解鎖「心智逆向工程」！把你的經商哲學與店鋪 SOP 封裝進 AI，親手打造專屬數位店長。", (230, 140, 30))
    ]

    sy = card_y + 65
    for idx, (time_tag, topic, desc, tag_color) in enumerate(curriculum):
        # 左側標記
        draw.rectangle([cx + 30, sy, cx + 38, sy + 78], fill=tag_color)
        draw.text((cx + 55, sy + 3), time_tag, fill=tag_color, font=get_font(17, bold=True))
        draw.text((cx + 55, sy + 28), topic, fill=(255, 255, 255), font=get_font(20, bold=True))
        draw.text((cx + 55, sy + 56), desc, fill=(175, 180, 195), font=get_font(15, bold=False))
        if idx < 2:
            draw.line([(cx + 30, sy + 92), (cx + card_w - 30, sy + 92)], fill=(45, 50, 62), width=1)
        sy += 105

    # 底部實戰承諾與座標
    foot_y = card_y + card_h + 35
    draw.line([(W // 2 - 160, foot_y), (W // 2 + 160, foot_y)], fill=gold_frame, width=2)
    
    font_venue = get_font(21, bold=True)
    draw.text((W // 2, foot_y + 32), "每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(230, 220, 205), font=font_venue, anchor="mm")
    
    font_sub2 = get_font(18, bold=False)
    draw.text((W // 2, foot_y + 68), "100% 純實體現場教學  ·  導師巡桌手把手排錯  ·  做完專屬成果才准下課", fill=(170, 160, 145), font=font_sub2, anchor="mm")
    
    font_cta = get_font(19, bold=True)
    draw.text((W // 2, foot_y + 104), "老學員 0 元免單 · 線上申請請見【第一則留言】", fill=(245, 183, 56), font=font_cta, anchor="mm")
    
    out_fb = os.path.join(OUT_DIR_FB, "FB_04_Iron_Discipline_Black_Gold.png")
    img.save(out_fb, quality=95)
    img.save(os.path.join(BRAIN_DIR, "FB_04_Iron_Discipline_Black_Gold.png"))
    print("FB-04 Black Gold generated:", out_fb)
    return out_fb

# ==========================================
# 2. TH-04: 脆專用 · 10 張椅子白板任務實況 (1080x1350 4:5)
# ==========================================
def render_th_04():
    W, H = 1080, 1350
    # 深沉工坊灰黑底色
    img = Image.new("RGB", (W, H), (20, 22, 28))
    draw = ImageDraw.Draw(img)
    
    margin = 45
    # 頂部狀態列
    draw.text((margin + 15, margin + 10), "家宅總部現場實況", fill=(160, 170, 185), font=get_font(18, bold=True))
    draw.text((W - margin - 150, margin + 10), "純實體 · 嚴禁線上", fill=(220, 60, 50), font=get_font(16, bold=True))
    draw.line([(margin, margin + 45), (W - margin, margin + 45)], fill=(45, 52, 65), width=1)
    
    # 教室實況任務白板卡片容器
    y = margin + 70
    card_h = 700
    draw.rectangle([margin, y, W - margin, y + card_h], fill=(28, 33, 44), outline=(60, 72, 95), width=2)
    
    # 白板頂部標籤
    draw.rectangle([margin + 30, y + 25, margin + 220, y + 62], fill=(220, 60, 50))
    draw.text((margin + 125, y + 43), "白板通告 · 巡桌軍規", fill=(255, 255, 255), font=get_font(17, bold=True), anchor="mm")
    
    draw.text((W - margin - 35, y + 43), "僅剩最後 5 席！", fill=(245, 183, 56), font=get_font(18, bold=True), anchor="rm")
    
    # 核心軍規手寫感標語
    draw.text((margin + 35, y + 95), "多一張椅子都沒有。", fill=(255, 255, 255), font=get_font(32, bold=True))
    draw.text((margin + 35, y + 145), "來真的，不准摸魚，沒做完專屬成果不放人。", fill=(245, 183, 56), font=get_font(21, bold=True))
    
    # 10 張椅子席次圖解矩陣
    seat_y = y + 200
    draw.text((margin + 35, seat_y), "【 正氣北路家宅 10 席實體座位即時狀態 】", fill=(180, 195, 215), font=get_font(17, bold=True))
    
    # 畫出 10 個席位方塊（前 5 個已鎖定，後 5 個倒數中）
    box_w = (W - margin * 2 - 70 - 40) // 5
    box_h = 60
    for i in range(10):
        row = i // 5
        col = i % 5
        bx = margin + 35 + col * (box_w + 10)
        by = seat_y + 35 + row * (box_h + 10)
        if i < 5:
            # 已鎖定 (深綠/暗金)
            draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(30, 55, 45), outline=(50, 140, 90), width=2)
            draw.text((bx + box_w // 2, by + 18), f"席位 {i+1:02d}", fill=(180, 220, 195), font=get_font(15, bold=True), anchor="mm")
            draw.text((bx + box_w // 2, by + 40), "已審查鎖定", fill=(70, 200, 130), font=get_font(13, bold=False), anchor="mm")
        else:
            # 最後 5 席 (紅色警示呼吸邊框)
            draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(50, 25, 25), outline=(220, 60, 50), width=2)
            draw.text((bx + box_w // 2, by + 18), f"席位 {i+1:02d}", fill=(255, 200, 200), font=get_font(15, bold=True), anchor="mm")
            draw.text((bx + box_w // 2, by + 40), "最後搶位！", fill=(255, 100, 90), font=get_font(13, bold=True), anchor="mm")

    # 三週課程速覽白板清單
    plan_y = seat_y + 195
    draw.rectangle([margin + 25, plan_y, W - margin - 25, plan_y + 265], fill=(20, 24, 32), outline=(50, 60, 78))
    
    draw.text((margin + 45, plan_y + 20), "秋季三週完整實戰課表（每週三 14:00 - 16:00 家宅）：", fill=(245, 183, 56), font=get_font(18, bold=True))
    
    lessons = [
        ("• 11/11 第 1 講", "NotebookLM 數位大腦 · 漏斗深挖提問法（僅剩最後 5 席）"),
        ("• 11/18 第 2 講", "Antigravity 操作 · Meta 官方自動發文串接 (FB/Threads API)"),
        ("• 11/25 第 3 講", "資料架構管理 · 擬人化店長分身 (心智逆向工程)")
    ]
    ly = plan_y + 60
    for l_head, l_desc in lessons:
        draw.text((margin + 45, ly), l_head, fill=(255, 255, 255), font=get_font(18, bold=True))
        draw.text((margin + 65, ly + 26), l_desc, fill=(180, 195, 215), font=get_font(16, bold=False))
        ly += 65

    # 底部實戰破局宣告卡
    by_foot = y + card_h + 35
    draw.rectangle([margin, by_foot, W - margin, by_foot + 400], fill=(28, 33, 44), outline=(60, 72, 95))
    draw.rectangle([margin, by_foot, margin + 8, by_foot + 400], fill=(220, 60, 50))
    
    draw.text((margin + 35, by_foot + 28), "前半段講心法，後半段全員打開筆電。", fill=(255, 255, 255), font=get_font(24, bold=True))
    draw.text((margin + 35, by_foot + 65), "我和助教一個一個螢幕盯著看，當場排查報錯。", fill=(245, 183, 56), font=get_font(20, bold=True))
    
    draw.text((margin + 35, by_foot + 115), "做不出專屬成果，當天真的不放人下課。", fill=(220, 230, 245), font=get_font(18, bold=False))
    draw.text((margin + 35, by_foot + 150), "想混學分的千萬別來；想解決店裡真難題的，快來卡位。", fill=(180, 190, 205), font=get_font(18, bold=False))
    
    draw.line([(margin + 35, by_foot + 200), (W - margin - 35, by_foot + 200)], fill=(55, 68, 88), width=1)
    
    draw.text((margin + 35, by_foot + 225), "【時間地點】 11/11 (週三) 14:00 · 台東市正氣北路166巷90號（家宅）", fill=(245, 183, 56), font=get_font(19, bold=True))
    draw.text((margin + 35, by_foot + 265), "【席次戰報】 10 席已過半 · 最後 5 席 ｜ 老學員 0 元免單 ｜ 留言區放表單", fill=(255, 255, 255), font=get_font(18, bold=True))
    
    out_th = os.path.join(OUT_DIR_TH, "TH_04_Classroom_Chairs_Countdown.jpg")
    img.save(out_th, quality=95)
    img.save(os.path.join(BRAIN_DIR, "TH_04_Classroom_Chairs_Countdown.jpg"))
    print("TH-04 generated:", out_th)
    return out_th

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    render_fb_04()
    render_th_04()
    print("All Post 04 visuals generated successfully!")
