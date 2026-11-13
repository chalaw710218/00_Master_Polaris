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

# ==========================================
# 1. POSTER 01: 科技流水線藍圖版 (1200x1200)
# ==========================================
def render_poster_01():
    W, H = 1200, 1200
    bg_color = (10, 15, 29) # 賽博藍黑底
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_cyan = (40, 95, 160)
    accent_cyan = (60, 180, 240)
    gold_highlight = (245, 183, 56)
    
    draw.rectangle([margin, margin, W - margin, H - margin], outline=border_cyan, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(20, 45, 80), width=1)
    
    corner_len = 22
    for cx, cy in [(margin + 12, margin + 12), (W - margin - 12, margin + 12), 
                   (margin + 12, H - margin - 12), (W - margin - 12, H - margin - 12)]:
        dx = 1 if cx == margin + 12 else -1
        dy = 1 if cy == margin + 12 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=accent_cyan, width=2)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=accent_cyan, width=2)

    top_y = margin + 35
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教系列班 · 第 2 講", fill=(140, 185, 235), font=get_font(18, bold=True), anchor="mm")
    
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 告別手動複製貼上！把社群發射台交給 AI 」", fill=(225, 238, 255), font=get_font(38, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "Antigravity 操作 · Meta 官方自動發文串接", fill=gold_highlight, font=get_font(42, bold=True), anchor="mm")

    badge_y = title_y + 115
    badge_w, badge_h = 780, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(18, 30, 52), outline=accent_cyan, width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=accent_cyan)
    draw.text((W // 2, badge_y + badge_h // 2), "【 鐵血驗收 】 現場自備筆電巡桌排錯到底 · API 沒跑通不准走！", fill=(220, 245, 255), font=get_font(20, bold=True), anchor="mm")

    card_y = badge_y + 68
    card_w = 1010
    card_h = 370
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(14, 22, 40), outline=(35, 60, 100), width=2)
    
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(22, 36, 65))
    draw.text((cx + 30, card_y + 22), "AUTOMATION ARCHITECTURE ｜ 全自動發文流水線解密", fill=(160, 210, 255), font=get_font(16, bold=True), anchor="lm")
    draw.text((cx + card_w - 30, card_y + 22), "STATUS: 100% PRODUCTION READY", fill=gold_highlight, font=get_font(15, bold=True), anchor="rm")

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
        draw.rectangle([mx, col_y, mx + col_w, col_y + 36], fill=(26, 42, 75))
        draw.text((mx + col_w // 2, col_y + 18), m_title, fill=tag_color, font=get_font(15, bold=True), anchor="mm")
        draw.text((mx + col_w // 2, col_y + 52), m_sub, fill=(225, 235, 250), font=get_font(14, bold=True), anchor="mm")
        
        iy = col_y + 80
        for item in items:
            draw.text((mx + 15, iy), item, fill=(180, 195, 220), font=get_font(13, bold=False))
            iy += 35

    bonus_y = card_y + card_h + 20
    bonus_w = 1010
    bonus_h = 70
    bx = (W - bonus_w) // 2
    draw.rectangle([bx, bonus_y, bx + bonus_w, bonus_y + bonus_h], fill=(16, 26, 46), outline=border_cyan, width=1)
    
    draw.text((bx + 30, bonus_y + 15), "【 專屬回娘家特權 】", fill=gold_highlight, font=get_font(15, bold=True))
    draw.text((bx + 200, bonus_y + 15), "老學員（含第 1 講夥伴）0 元免單！ ｜ 新朋友實戰價單堂 NT$ 500", fill=(240, 245, 255), font=get_font(15, bold=True))
    draw.text((bx + 200, bonus_y + 40), "全班極限 6 席純實體手把手教學 · 額滿立即關門 · 做完才准下課", fill=(170, 190, 220), font=get_font(14, bold=False))

    foot_y = bonus_y + bonus_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=accent_cyan, width=2)
    draw.text((W // 2, foot_y + 24), "11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(230, 240, 255), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "自備筆電實機排錯 ｜ 審查通過發送 Email 正取繳費信 ｜ 線上申請請見第一則留言", fill=(160, 185, 215), font=get_font(16, bold=False), anchor="mm")

    p1 = os.path.join(ROOT_DIR, "FB_L02_01_No_Photo_Automation.png")
    p2 = os.path.join(BRAIN_DIR, "FB_L02_01_No_Photo_Automation.png")
    img.save(p1, quality=95)
    img.save(p2, quality=95)
    print(f"✅ 海報 01 生成完畢: {p1}")

# ==========================================
# 2. POSTER 02: 官方合法直連與資安防禦版 (1200x1200)
# ==========================================
def render_poster_02():
    W, H = 1200, 1200
    bg_color = (17, 20, 26) # 曜石墨黑底
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_gold = (180, 145, 75)
    accent_gold = (245, 183, 56)
    alert_red = (235, 75, 65)
    safe_green = (65, 195, 120)
    
    draw.rectangle([margin, margin, W - margin, H - margin], outline=border_gold, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(35, 42, 55), width=1)
    
    top_y = margin + 35
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教系列班 · 資安與官方直連防線", fill=(195, 175, 135), font=get_font(18, bold=True), anchor="mm")
    
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 黑心外掛會被封號！我們教你走 Meta 官方直連 」", fill=(245, 245, 250), font=get_font(38, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "100% 合法乾淨通道 · Facebook ＆ Threads 官方 API", fill=accent_gold, font=get_font(40, bold=True), anchor="mm")

    badge_y = title_y + 115
    badge_w, badge_h = 780, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(30, 26, 20), outline=accent_gold, width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=accent_gold)
    draw.text((W // 2, badge_y + badge_h // 2), "【 官方通道保障 】 拒絕非法爬蟲與黑產外掛 · 安全合規永不封號", fill=(255, 240, 210), font=get_font(20, bold=True), anchor="mm")

    # 中央對抗資訊盒：非法外掛 vs 官方 API 直連
    grid_y = badge_y + 68
    grid_w = 1010
    col_w = 485
    gap = 40
    card_h = 370
    left_x = (W - grid_w) // 2
    right_x = left_x + col_w + gap
    
    # 左側：市面黑心外掛與模擬器 (危險警示)
    draw.rectangle([left_x, grid_y, left_x + col_w, grid_y + card_h], fill=(26, 20, 22), outline=alert_red, width=2)
    draw.rectangle([left_x, grid_y, left_x + col_w, grid_y + 52], fill=(42, 24, 28))
    draw.text((left_x + col_w // 2, grid_y + 26), "市售黑心外掛 / 網頁爬蟲 (高風險)", fill=(255, 170, 165), font=get_font(18, bold=True), anchor="mm")
    
    left_points = [
        ("帳號隨時被封禁", "違反 Meta 使用者條款，觸發官方風控直接鎖粉專"),
        ("密碼與帳密洩漏", "第三方外掛程式偷讀 Cookie，資安隱患極大"),
        ("介面改版就崩潰", "臉書按鈕一改版腳本就失效，維護成本極高"),
        ("觸及率被判定垃圾", "被演算法判定為機器人濫發，觸及率直接歸零")
    ]
    ly = grid_y + 75
    for tag, desc in left_points:
        draw.rectangle([left_x + 20, ly, left_x + 26, ly + 46], fill=alert_red)
        draw.text((left_x + 40, ly + 2), tag, fill=alert_red, font=get_font(18, bold=True))
        draw.text((left_x + 40, ly + 26), desc, fill=(200, 175, 180), font=get_font(14, bold=False))
        ly += 68

    # 右側：極星官方 API 直連架構 (合法安心)
    draw.rectangle([right_x, grid_y, right_x + col_w, grid_y + card_h], fill=(20, 28, 25), outline=safe_green, width=2)
    draw.rectangle([right_x, grid_y, right_x + col_w, grid_y + 52], fill=(25, 48, 38))
    draw.text((right_x + col_w // 2, grid_y + 26), "Meta 官方合法 API 直連 (100% 安全)", fill=safe_green, font=get_font(18, bold=True), anchor="mm")
    
    right_points = [
        ("官方通道穩定發布", "使用 Meta 認證 Graph API 與 Threads API 合法發文"),
        ("金鑰環境隔離防護", "Token 存放於本機環境變數，永遠不向外洩漏"),
        ("官方伺服器直接響應", "3 秒內上傳圖文並取得官方貼文 ID，零延遲"),
        ("演算法天然高權重", "官方 API 合規發文，享有最高規格發布權限")
    ]
    ry = grid_y + 75
    for tag, desc in right_points:
        draw.rectangle([right_x + 20, ry, right_x + 26, ry + 46], fill=safe_green)
        draw.text((right_x + 40, ry + 2), tag, fill=safe_green, font=get_font(18, bold=True))
        draw.text((right_x + 40, ry + 26), desc, fill=(190, 215, 205), font=get_font(14, bold=False))
        ry += 68

    bonus_y = grid_y + card_h + 20
    bonus_w = 1010
    bonus_h = 70
    bx = (W - bonus_w) // 2
    draw.rectangle([bx, bonus_y, bx + bonus_w, bonus_y + bonus_h], fill=(24, 28, 35), outline=border_gold, width=1)
    
    draw.text((bx + 30, bonus_y + 15), "【 現場實機排錯保證 】", fill=accent_gold, font=get_font(15, bold=True))
    draw.text((bx + 220, bonus_y + 15), "老學員 0 元免單回娘家！ ｜ 新朋友實戰價單堂 NT$ 500", fill=(245, 245, 250), font=get_font(15, bold=True))
    draw.text((bx + 220, bonus_y + 40), "全員自備筆電 · 導師現場巡桌手把手排錯 · 沒發出第一篇不准下課", fill=(180, 190, 205), font=get_font(14, bold=False))

    foot_y = bonus_y + bonus_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=accent_gold, width=2)
    draw.text((W // 2, foot_y + 24), "11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(240, 235, 220), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "6 席純實體精緻小班 ｜ 審查通過發送 Email 正取繳費信 ｜ 申請表請見第一則留言", fill=(175, 170, 160), font=get_font(16, bold=False), anchor="mm")

    p1 = os.path.join(ROOT_DIR, "FB_L02_02_Official_API_Security.png")
    p2 = os.path.join(BRAIN_DIR, "FB_L02_02_Official_API_Security.png")
    img.save(p1, quality=95)
    img.save(p2, quality=95)
    print(f"✅ 海報 02 生成完畢: {p1}")

# ==========================================
# 3. POSTER 03: 明天開課登機門倒數版 (1200x1200)
# ==========================================
def render_poster_03():
    W, H = 1200, 1200
    bg_color = (14, 16, 22) # 啞光炭黑底
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_red = (220, 60, 50)
    accent_gold = (245, 183, 56)
    
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(45, 50, 65), width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(25, 30, 42), width=1)
    
    top_y = margin + 35
    draw.text((W // 2, top_y), "FLIGHT GATE 1118 ｜ 正氣北路家宅 ｜ 席次最終倒數通報", fill=(175, 185, 200), font=get_font(18, bold=True), anchor="mm")
    
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 最後召集！明天下午 14:00 準時開練 」", fill=(240, 245, 255), font=get_font(40, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "堅持 6 人精緻小班 · 多一張椅子都不加！", fill=border_red, font=get_font(42, bold=True), anchor="mm")

    badge_y = title_y + 115
    badge_w, badge_h = 800, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(35, 18, 18), outline=border_red, width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=border_red)
    draw.text((W // 2, badge_y + badge_h // 2), "【 登機門即刻關閉 】 第 2 講席次即將滿額 · 額滿表單立即鎖定！", fill=(255, 220, 215), font=get_font(20, bold=True), anchor="mm")

    # 中央大卡片：明天現場 3 大交付成果
    card_y = badge_y + 68
    card_w = 1010
    card_h = 370
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(20, 24, 32), outline=(50, 60, 75), width=2)
    
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(28, 34, 45))
    draw.text((cx + 30, card_y + 22), "TOMORROW'S DELIVERABLES ｜ 明天下午帶走的專屬資產", fill=(160, 180, 210), font=get_font(16, bold=True), anchor="lm")
    draw.text((cx + card_w - 30, card_y + 22), "COUNTDOWN: FINAL 24 HOURS", fill=border_red, font=get_font(16, bold=True), anchor="rm")

    col_w = 300
    col_gap = 25
    col_start_x = cx + 30
    col_y = card_y + 65
    col_h = 280

    deliverables = [
        ("資產 01 ｜ 官方通道", "Meta API 永久金鑰", [
            "• Facebook 粉專官方認證串接",
            "• Threads 官方 API 正式通行",
            "• 本機安全隔離，永不外洩",
            "• 擺脫黑產外掛封號惡夢"
        ], border_red),
        ("資產 02 ｜ 發射腳本", "Python 3秒自動排程", [
            "• 本地資料夾自動圖文檢驗",
            "• 一鍵推播雙平台＋首留言導流",
            "• 指定未來時間全自動發布",
            "• 真正省下每天手動剪貼時間"
        ], accent_gold),
        ("資產 03 ｜ 守護特助", "24小時留言自動秒回", [
            "• 客人半夜留言即時情商回覆",
            "• 打造專屬店鋪客服互動邏輯",
            "• 從此徹底告別半夜回訊焦慮",
            "• 系統在後台安靜替你招攬顧客"
        ], (80, 200, 140))
    ]

    for idx, (d_title, d_sub, items, tag_color) in enumerate(deliverables):
        dx = col_start_x + idx * (col_w + col_gap)
        draw.rectangle([dx, col_y, dx + col_w, col_y + col_h], fill=(24, 28, 38), outline=(45, 55, 70), width=1)
        draw.rectangle([dx, col_y, dx + col_w, col_y + 36], fill=(32, 40, 55))
        draw.text((dx + col_w // 2, col_y + 18), d_title, fill=tag_color, font=get_font(15, bold=True), anchor="mm")
        draw.text((dx + col_w // 2, col_y + 52), d_sub, fill=(240, 245, 255), font=get_font(14, bold=True), anchor="mm")
        
        iy = col_y + 80
        for item in items:
            draw.text((dx + 15, iy), item, fill=(185, 195, 215), font=get_font(13, bold=False))
            iy += 35

    bonus_y = card_y + card_h + 20
    bonus_w = 1010
    bonus_h = 70
    bx = (W - bonus_w) // 2
    draw.rectangle([bx, bonus_y, bx + bonus_w, bonus_y + bonus_h], fill=(22, 26, 35), outline=(50, 60, 75), width=1)
    
    draw.text((bx + 30, bonus_y + 15), "【 最後召集令 】", fill=border_red, font=get_font(15, bold=True))
    draw.text((bx + 180, bonus_y + 15), "老學員 0 元免單回娘家！ ｜ 新朋友實戰價單堂 NT$ 500", fill=(245, 245, 255), font=get_font(15, bold=True))
    draw.text((bx + 180, bonus_y + 40), "額滿即刻關閉表單 · 超額申請自動轉入候補 · 明天現場見", fill=(175, 185, 205), font=get_font(14, bold=False))

    foot_y = bonus_y + bonus_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=border_red, width=2)
    draw.text((W // 2, foot_y + 24), "明天 11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(240, 245, 255), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "自備筆電實機排錯到底 ｜ 做完專屬成果才准下課 ｜ 線上申請表請見第一則留言", fill=(170, 180, 195), font=get_font(16, bold=False), anchor="mm")

    p1 = os.path.join(ROOT_DIR, "FB_L02_03_Final_Call_Tomorrow.png")
    p2 = os.path.join(BRAIN_DIR, "FB_L02_03_Final_Call_Tomorrow.png")
    img.save(p1, quality=95)
    img.save(p2, quality=95)
    print(f"✅ 海報 03 生成完畢: {p1}")

if __name__ == "__main__":
    render_poster_01()
    render_poster_02()
    render_poster_03()
