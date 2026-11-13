import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation"
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"

os.makedirs(ROOT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_path = r"C:\Windows\Fonts\msjhbd.ttc" if bold else r"C:\Windows\Fonts\msjh.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def render_lesson_02_poster():
    W, H = 1200, 1200
    # 深邃賽博科技藍黑底色 (#0a0f1d)
    bg_color = (10, 15, 29)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_cyan = (40, 95, 160)
    accent_cyan = (60, 180, 240)
    gold_highlight = (245, 183, 56)
    
    # 德式工匠雙層外框
    draw.rectangle([margin, margin, W - margin, H - margin], outline=border_cyan, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(20, 45, 80), width=1)
    
    # 四角幾何定位標記
    corner_len = 22
    for cx, cy in [(margin + 12, margin + 12), (W - margin - 12, margin + 12), 
                   (margin + 12, H - margin - 12), (W - margin - 12, H - margin - 12)]:
        dx = 1 if cx == margin + 12 else -1
        dy = 1 if cy == margin + 12 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=accent_cyan, width=2)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=accent_cyan, width=2)

    # 頂部小標
    top_y = margin + 35
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教系列班 · 第 2 講", fill=(140, 185, 235), font=get_font(18, bold=True), anchor="mm")
    
    # 震撼標題
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 告別手動複製貼上！把社群發射台交給 AI 」", fill=(225, 238, 255), font=get_font(38, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "Antigravity 操作 · Meta 官方自動發文串接", fill=gold_highlight, font=get_font(42, bold=True), anchor="mm")

    # 鐵血驗收警示徽章
    badge_y = title_y + 115
    badge_w, badge_h = 780, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(18, 30, 52), outline=accent_cyan, width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=accent_cyan)
    draw.text((W // 2, badge_y + badge_h // 2), "【 鐵血驗收 】 現場自備筆電巡桌排錯到底 · API 沒跑通不准走！", fill=(220, 245, 255), font=get_font(20, bold=True), anchor="mm")

    # 中央流水線架構圖卡 (The Pipeline Blueprint)
    card_y = badge_y + 68
    card_w = 1010
    card_h = 370
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(14, 22, 40), outline=(35, 60, 100), width=2)
    
    # 頂部橫條
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(22, 36, 65))
    draw.text((cx + 30, card_y + 22), "AUTOMATION ARCHITECTURE ｜ 全自動發文流水線解密", fill=(160, 210, 255), font=get_font(16, bold=True), anchor="lm")
    draw.text((cx + card_w - 30, card_y + 22), "STATUS: 100% PRODUCTION READY", fill=gold_highlight, font=get_font(15, bold=True), anchor="rm")

    # 三大核心模組區塊 (橫向 3 欄)
    col_w = 300
    col_gap = 25
    col_start_x = cx + 30
    col_y = card_y + 65
    col_h = 280

    modules = [
        ("模組 01 ｜ 本地素材包", "資料夾自動格式檢查", [
            "• 本地放入商品照與文案草稿",
            "• Python 自動檢測圖片解析度",
            "• 告別手動開瀏覽器剪貼文案",
            "• 建立專屬排程內容發射庫"
        ], (40, 70, 120), accent_cyan),
        ("模組 02 ｜ 終端機與 API", "Antigravity · Meta 直連", [
            "• 串接 Facebook 官方粉專 API",
            "• 串接 Threads 官方 API 授權",
            "• 金鑰環境隔離保護永不洩漏",
            "• 3 秒內完成代碼調用發布"
        ], (50, 80, 130), gold_highlight),
        ("模組 03 ｜ 24H 自動化閉環", "夜間自動排程與秒回", [
            "• 指定未來時間全自動精準發射",
            "• 留言區首則自動掛載導流表單",
            "• 24 小時留言自動巡邏秒回",
            "• 徹底消滅小老闆半夜回訊焦慮"
        ], (40, 70, 120), (120, 220, 140))
    ]

    for idx, (m_title, m_sub, items, bg_box, tag_color) in enumerate(modules):
        mx = col_start_x + idx * (col_w + col_gap)
        draw.rectangle([mx, col_y, mx + col_w, col_y + col_h], fill=(18, 28, 50), outline=bg_box, width=1)
        # 頂部色條
        draw.rectangle([mx, col_y, mx + col_w, col_y + 36], fill=(26, 42, 75))
        draw.text((mx + col_w // 2, col_y + 18), m_title, fill=tag_color, font=get_font(15, bold=True), anchor="mm")
        draw.text((mx + col_w // 2, col_y + 52), m_sub, fill=(225, 235, 250), font=get_font(14, bold=True), anchor="mm")
        
        iy = col_y + 80
        for item in items:
            draw.text((mx + 15, iy), item, fill=(180, 195, 220), font=get_font(13, bold=False))
            iy += 35

    # 席次與老學員特權橫幅 (Bonus Bar)
    bonus_y = card_y + card_h + 20
    bonus_w = 1010
    bonus_h = 70
    bx = (W - bonus_w) // 2
    draw.rectangle([bx, bonus_y, bx + bonus_w, bonus_y + bonus_h], fill=(16, 26, 46), outline=border_cyan, width=1)
    
    draw.text((bx + 30, bonus_y + 15), "【 專屬回娘家特權 】", fill=gold_highlight, font=get_font(15, bold=True))
    draw.text((bx + 200, bonus_y + 15), "老學員（含第 1 講夥伴）0 元免單！ ｜ 新朋友實戰價單堂 NT$ 500", fill=(240, 245, 255), font=get_font(15, bold=True))
    draw.text((bx + 200, bonus_y + 40), "全班極限 6 席純實體手把手教學 · 額滿立即關門 · 做完才准下課", fill=(170, 190, 220), font=get_font(14, bold=False))

    # 底部實體資訊與地點
    foot_y = bonus_y + bonus_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=accent_cyan, width=2)
    
    draw.text((W // 2, foot_y + 24), "11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(230, 240, 255), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "自備筆電實機排錯 ｜ 審查通過發送 Email 正取繳費信 ｜ 線上申請請見第一則留言", fill=(160, 185, 215), font=get_font(16, bold=False), anchor="mm")

    p1 = os.path.join(ROOT_DIR, "FB_Lesson_02_Automation_Blueprint.png")
    p2 = os.path.join(BRAIN_DIR, "FB_Lesson_02_Automation_Blueprint.png")
    img.save(p1, quality=95)
    img.save(p2, quality=95)
    print(f"✅ 第 2 講專屬海報生成完畢: {p1}")

if __name__ == "__main__":
    render_lesson_02_poster()
