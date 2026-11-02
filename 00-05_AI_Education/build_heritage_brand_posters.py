import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR_FB = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts"
OUT_DIR_TH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts"
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"
STICKER_PATH = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\.user_uploaded\media_1793580557231_87c68fc1.jpg"

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"

def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size)

def get_circular_sticker(target_diameter):
    """讀取創始貼紙並裁切為帶有反鋸齒平滑邊緣的圓形徽章"""
    raw = Image.open(STICKER_PATH).convert("RGBA")
    w, h = raw.size
    
    # 建立精確圓形遮罩 (去除外部白色背景)
    # 觀察貼紙本體大致在中心直徑約 96% 區域
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    # 微調邊界確保乾淨的圓形外框
    cx, cy = w // 2, h // 2
    radius = int(min(w, h) * 0.485)
    mask_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=255)
    
    # 裁切出圓形圖
    circular = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    circular.paste(raw, (0, 0), mask=mask)
    
    # Crop to bounding box
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    cropped = circular.crop(bbox)
    
    # 縮放到目標尺寸
    resized = cropped.resize((target_diameter, target_diameter), Image.Resampling.LANCZOS)
    return resized

def add_drop_shadow(img_rgba, offset=(0, 10), blur=15, shadow_color=(30, 30, 30, 90)):
    """為圓形徽章添加柔和實體立體陰影"""
    w, h = img_rgba.size
    pad = blur * 2 + max(abs(offset[0]), abs(offset[1]))
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    
    # 萃取 alpha channel 作為陰影遮罩
    alpha = img_rgba.split()[3]
    shadow_mask = alpha.filter(ImageFilter.GaussianBlur(blur))
    
    # 建立與本體同尺寸的陰影色塊
    shadow_patch = Image.new("RGBA", (w, h), shadow_color)
    shadow_pos = (pad + offset[0], pad + offset[1])
    canvas.paste(shadow_patch, shadow_pos, mask=shadow_mask)
    
    # 貼上本體
    canvas.paste(img_rgba, (pad, pad), mask=img_rgba)
    return canvas, pad

# =========================================================================
# 提案 A：【寶桑暖陽經典版】(Sunlit Baosang Heritage) - 1:1 (1200x1200)
# 溫暖米白畫布 ✕ 經典暖陽黃 ✕ 創始貼紙徽章 ✕ 昭和物流單風格
# =========================================================================
def render_heritage_a():
    W, H = 1200, 1200
    # 溫暖奶油紙質色
    bg_color = (252, 249, 242)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    inner_w = W - 2 * margin
    
    # 外圍懷舊雙重邊框 (昭和手作感)
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(225, 215, 198), width=3)
    draw.rectangle([margin + 8, margin + 8, W - margin - 8, H - margin - 8], outline=(40, 40, 40), width=3)
    
    # 頂部抬頭 Bar (向日葵黃底塊)
    bar_y = margin + 18
    bar_h = 56
    draw.rectangle([margin + 18, bar_y, W - margin - 18, bar_y + bar_h], fill=(245, 183, 56))
    draw.rectangle([margin + 18, bar_y, W - margin - 18, bar_y + bar_h], outline=(40, 40, 40), width=2)
    
    font_bar = get_font(21, bold=True)
    draw.text((margin + 40, bar_y + 14), "★ 生活管家 · 寶桑原點 ✕ 2026 秋季實體家教班 ★", fill=(30, 30, 30), font=font_bar)
    draw.text((W - margin - 220, bar_y + 16), "限額 10 席 · 純實體", fill=(193, 18, 31), font=get_font(18, bold=True))
    
    # 主體上半部：左側放置創始徽章，右側放置重磅主標題
    badge_size = 380
    badge = get_circular_sticker(badge_size)
    badge_with_shadow, pad = add_drop_shadow(badge, offset=(4, 8), blur=12, shadow_color=(0, 0, 0, 70))
    
    bx = margin + 35
    by = bar_y + bar_h + 30
    img.paste(badge_with_shadow, (bx - pad, by - pad), mask=badge_with_shadow)
    
    # 右側標題區
    tx = bx + badge_size + 40
    ty = by + 25
    
    draw.text((tx, ty), "致所有在台東每天拼命的自營店家：", fill=(110, 100, 90), font=get_font(18, bold=False))
    
    font_h1 = get_font(48, bold=True)
    draw.text((tx, ty + 42), "把時間買回來，", fill=(30, 30, 30), font=font_h1)
    draw.text((tx, ty + 105), "多陪陪家人。", fill=(193, 18, 31), font=font_h1)
    
    # 標題下方小裝飾線
    draw.rectangle([tx, ty + 175, tx + 280, ty + 179], fill=(245, 183, 56))
    
    # 右側感性短文
    quote_lines = [
        "就像當年這隻抱著魚狂飆的貓一樣，",
        "備料、送貨、回訊息，常常一人當三人用。",
        "忙完坐下夜深了，孩子也睡了。",
        "",
        "學 AI 不是為了追潮流，",
        "只是想買回屬於自己的時間與生活。"
    ]
    qy = ty + 195
    for ql in quote_lines:
        if ql == "":
            qy += 10
            continue
        c = (193, 18, 31) if "買回屬於自己的時間" in ql else (60, 60, 60)
        draw.text((tx, qy), ql, fill=c, font=get_font(18, bold=("買回" in ql)))
        qy += 28

    # 下半部：昭和風「物流委託單 / 上課憑證」資訊卡
    ticket_y = by + badge_size + 40
    ticket_h = 320
    draw.rectangle([margin + 25, ticket_y, W - margin - 25, ticket_y + ticket_h], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    # 頂部裝飾條
    draw.rectangle([margin + 25, ticket_y, W - margin - 25, ticket_y + 42], fill=(40, 40, 40))
    draw.text((margin + 45, ticket_y + 10), "◆ 實體現場教學 · 專屬課堂履約條款 ◆", fill=(250, 250, 250), font=get_font(18, bold=True))
    draw.text((W - margin - 220, ticket_y + 12), "No. 20261111-TAITUNG", fill=(245, 183, 56), font=get_font(15, bold=True))
    
    # 資訊欄位 (4 個格子)
    grid_data = [
        ("📅 首講日期", "2026/11/11 (週三) 14:00 - 16:00", (30, 30, 30)),
        ("📍 上課地點", "生活管家總部（台東市正氣北路166巷90號）", (30, 30, 30)),
        ("⚠️ 教學紀律", "100% 純實體！限額 10 席！導師手把手巡桌排錯！", (193, 18, 31)),
        ("💡 鐵血保證", "做完店裡專屬成果才准下課！老學員 0 元免單回娘家！", (40, 100, 40))
    ]
    gy = ticket_y + 60
    for title, val, col in grid_data:
        draw.text((margin + 50, gy), title, fill=(100, 100, 100), font=get_font(18, bold=True))
        draw.text((margin + 180, gy), val, fill=col, font=get_font(20, bold=True))
        draw.line([(margin + 45, gy + 38), (W - margin - 45, gy + 38)], fill=(235, 230, 220), width=1)
        gy += 55
        
    # 底部紅色蓋章印記效果
    draw.text((margin + 50, ticket_y + ticket_h - 45), "💬 線上申請表與老學員免單名額，請見【第一則留言】", fill=(193, 18, 31), font=get_font(18, bold=True))
    
    # 仿紅色橢圓印章
    stamp_x = W - margin - 180
    stamp_y = ticket_y + ticket_h - 55
    draw.ellipse([stamp_x, stamp_y, stamp_x + 130, stamp_y + 40], outline=(193, 18, 31), width=2)
    draw.text((stamp_x + 22, stamp_y + 8), "極度嚴格", fill=(193, 18, 31), font=get_font(18, bold=True))
    
    # 最底欄
    draw.text((margin + 30, H - margin - 35), "生活管家 ✕ 寶桑物流 · 陪伴台東在地店家把日子過好", fill=(130, 125, 115), font=get_font(15, bold=False))
    
    out_path = os.path.join(OUT_DIR_FB, "FB_01_Heritage_Sunlit.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    img.save(os.path.join(BRAIN_DIR, "FB_01_Heritage_Sunlit.png"))
    return out_path

# =========================================================================
# 提案 B：【雙色對比昭和海報版】(Showa Duo-tone 60/40 Edition) - 1:1 (1200x1200)
# 完全復刻原貼紙 60/40 比例：上半暖陽黃 ✕ 下半奶油白，力量感極強！
# =========================================================================
def render_heritage_b():
    W, H = 1200, 1200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    split_y = int(H * 0.52) # 60/40 分割
    
    # 上半部：鮮明溫暖向日葵黃 (#F5B738)
    draw.rectangle([0, 0, W, split_y], fill=(245, 183, 56))
    # 下半部：奶油暖白 (#FFFDF5)
    draw.rectangle([0, split_y, W, H], fill=(255, 253, 245))
    
    # 水平粗黑邊界線（呼應貼紙標誌）
    draw.line([(0, split_y), (W, split_y)], fill=(30, 30, 30), width=6)
    
    margin = 55
    # 粗黑外邊框
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(30, 30, 30), width=4)
    
    # 上半部配置：中央霸氣放置徽章，兩側標語
    badge_size = 420
    badge = get_circular_sticker(badge_size)
    badge_with_shadow, pad = add_drop_shadow(badge, offset=(0, 8), blur=14, shadow_color=(0, 0, 0, 80))
    
    # 放置於上半部左中偏左
    bx = margin + 45
    by = margin + 50
    img.paste(badge_with_shadow, (bx - pad, by - pad), mask=badge_with_shadow)
    
    # 上半部右側：醒目的大標題
    tx = bx + badge_size + 40
    ty = margin + 70
    
    # 小徽章標籤
    draw.rectangle([tx, ty, tx + 180, ty + 36], fill=(30, 30, 30))
    draw.text((tx + 15, ty + 6), "生活管家 · 實體家教", fill=(245, 183, 56), font=get_font(17, bold=True))
    
    font_b_h1 = get_font(52, bold=True)
    draw.text((tx, ty + 60), "把時間", fill=(30, 30, 30), font=font_b_h1)
    draw.text((tx, ty + 125), "買回來，", fill=(30, 30, 30), font=font_b_h1)
    draw.text((tx, ty + 195), "多陪陪家人。", fill=(193, 18, 31), font=font_b_h1)
    
    draw.text((tx, ty + 285), "「跑物流、管店鋪這些年，", fill=(50, 45, 40), font=get_font(21, bold=True))
    draw.text((tx, ty + 320), "時間真的永遠不夠用。」", fill=(50, 45, 40), font=get_font(21, bold=True))
    
    # 下半部配置：奶油白底，扎實粗黑大字與課表卡片
    by2 = split_y + 40
    
    # 引言小段
    quote_text = "每天像這隻貓一樣抱著魚拼命狂飆，忙完夜深了，孩子也睡了。\n學 AI 不是為了追潮流，只是想把雜事理順，多留一點心力過生活。"
    draw.text((margin + 50, by2), quote_text, fill=(70, 70, 70), font=get_font(20, bold=False), spacing=10)
    
    # 底部實戰卡片
    card_y = by2 + 80
    card_h = 240
    draw.rectangle([margin + 40, card_y, W - margin - 40, card_y + card_h], fill=(248, 246, 240), outline=(30, 30, 30), width=2)
    # 左側黃色標籤邊
    draw.rectangle([margin + 40, card_y, margin + 55, card_y + card_h], fill=(245, 183, 56))
    
    draw.text((margin + 80, card_y + 25), "📌 11/11 (週三) 14:00 - 16:00 首講實體開跑！", fill=(30, 30, 30), font=get_font(23, bold=True))
    draw.text((margin + 80, card_y + 70), "📍 地點：生活管家總部（台東市正氣北路166巷90號）", fill=(60, 60, 60), font=get_font(18, bold=False))
    draw.text((margin + 80, card_y + 110), "⚠️ 100% 純實體現場 ✕ 限額 10 席 ✕ 沒做出成果不准下課！", fill=(193, 18, 31), font=get_font(19, bold=True))
    draw.text((margin + 80, card_y + 150), "☕ 老學員回娘家 0 元免單 ｜ 完整報名表請見【第一則留言】", fill=(40, 110, 40), font=get_font(19, bold=True))
    
    # 底部簽名
    draw.text((margin + 80, card_y + 195), "—— 寶桑物流・生活管家 闆仔 與 夥伴們敬上", fill=(130, 130, 130), font=get_font(15, bold=False))
    
    out_path = os.path.join(OUT_DIR_FB, "FB_01_Heritage_Showa.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    img.save(os.path.join(BRAIN_DIR, "FB_01_Heritage_Showa.png"))
    return out_path

# =========================================================================
# 提案 C：【脆專用 · 貓咪跑腿日常直式版】(Threads 4:5, 1080x1350)
# 像一張被貼在出貨板夾上的真實備忘錄，幽默、自嘲、痛點一針見血！
# =========================================================================
def render_heritage_threads():
    W, H = 1080, 1350
    # 溫暖牛皮紙底色 (#F7F2E7)
    img = Image.new("RGB", (W, H), (247, 242, 231))
    draw = ImageDraw.Draw(img)
    
    margin = 55
    # 板夾邊框
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(60, 50, 40), width=2)
    
    # 頂部貼紙：傾斜一點點（增加隨手貼的真實感）
    badge_size = 280
    badge = get_circular_sticker(badge_size)
    badge_rot = badge.rotate(-4, resample=Image.Resampling.BICUBIC, expand=True)
    badge_with_shadow, pad = add_drop_shadow(badge_rot, offset=(3, 6), blur=10, shadow_color=(0, 0, 0, 60))
    
    # 貼在右上角
    bx = W - margin - badge_rot.width - 25
    by = margin + 30
    img.paste(badge_with_shadow, (bx - pad, by - pad), mask=badge_with_shadow)
    
    # 左上角標題
    tx = margin + 40
    ty = margin + 50
    draw.text((tx, ty), "台東小老闆日常流水帳", fill=(120, 110, 100), font=get_font(20, bold=True))
    draw.line([(tx, ty + 35), (tx + 220, ty + 35)], fill=(120, 110, 100), width=1)
    
    draw.text((tx, ty + 55), "我們每天到底", fill=(40, 35, 30), font=get_font(38, bold=True))
    draw.text((tx, ty + 108), "在瞎忙什麼？", fill=(193, 18, 31), font=get_font(42, bold=True))
    
    # 貓咪指涉說明
    draw.text((tx, ty + 185), "↗ 就像右上角這隻貓一樣：", fill=(90, 80, 70), font=get_font(18, bold=True))
    draw.text((tx, ty + 215), "抱著魚狂飆，滿頭大汗怕送遲了，", fill=(90, 80, 70), font=get_font(18, bold=False))
    draw.text((tx, ty + 242), "永遠不知道今天幾點能吃晚飯。", fill=(90, 80, 70), font=get_font(18, bold=False))
    
    # 時間軸清單卡片
    card_y = ty + 300
    card_h = 420
    draw.rectangle([tx, card_y, W - margin - 40, card_y + card_h], fill=(255, 255, 255), outline=(60, 50, 40), width=2)
    # 卡片標籤
    draw.rectangle([tx, card_y, tx + 6, card_y + card_h], fill=(245, 183, 56))
    
    timeline = [
        ("07:30", "開車載貨、冰庫搬箱備料（狂飆如貓）"),
        ("10:30", "客人催單、改規格、補叫原物料"),
        ("14:00", "跑物流送件、庫存盤點、對帳單"),
        ("18:30", "晚班巡店、回不完的 LINE 訊息"),
        ("22:00", "夜深了，小孩睡了，飯又涼了...")
    ]
    sy = card_y + 25
    for tm, desc in timeline:
        is_late = ("22:00" in tm)
        c_t = (193, 18, 31) if is_late else (245, 140, 20)
        c_d = (193, 18, 31) if is_late else (50, 45, 40)
        draw.text((tx + 25, sy), tm, fill=c_t, font=get_font(20, bold=True))
        draw.text((tx + 105, sy), desc, fill=c_d, font=get_font(19, bold=is_late))
        draw.line([(tx + 20, sy + 45), (W - margin - 55, sy + 45)], fill=(240, 235, 225), width=1)
        sy += 65
        
    # 手寫刺眼紅框金句
    qy = card_y + card_h + 35
    q_h = 175
    draw.rectangle([tx, qy, W - margin - 40, qy + q_h], fill=(254, 242, 242), outline=(193, 18, 31), width=2)
    draw.rectangle([tx + 10, qy + 10, tx + 15, qy + q_h - 10], fill=(193, 18, 31))
    
    draw.text((tx + 30, qy + 25), "「我們那麼努力，本是為了給家人更好的生活，", fill=(30, 30, 30), font=get_font(21, bold=True))
    draw.text((tx + 30, qy + 65), "最後卻連好好陪他們吃頓飯的時間，", fill=(30, 30, 30), font=get_font(21, bold=True))
    draw.text((tx + 30, qy + 110), "都被雜事吃得乾乾淨淨。」", fill=(193, 18, 31), font=get_font(24, bold=True))
    
    # 底部行動區
    by_foot = qy + q_h + 35
    draw.text((tx, by_foot), "雜事交給數位助理跑腿，時間買回來還給家人。", fill=(40, 35, 30), font=get_font(20, bold=True))
    draw.text((tx, by_foot + 35), "11/11 週三下午 14:00 · 台東總部小班實戰（限 10 個人）", fill=(110, 100, 90), font=get_font(17, bold=False))
    draw.text((tx, by_foot + 68), "👉 留言區放線上申請表，想把時間找回來的來喝杯茶吧 ☕", fill=(193, 18, 31), font=get_font(18, bold=True))
    
    out_path = os.path.join(OUT_DIR_TH, "TH_01_Heritage_Cat.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    img.save(os.path.join(BRAIN_DIR, "TH_01_Heritage_Cat.png"))
    return out_path

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    render_heritage_a()
    render_heritage_b()
    render_heritage_threads()
    print("All heritage brand posters rendered successfully!")
