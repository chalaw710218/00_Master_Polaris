import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR_FB = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts"
OUT_DIR_TH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts"
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"
PHOTO_BOSS = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-04_Brand_Characters\02_闆仔_Boss\images\boss_origin_photo_glasses.jpg"

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"

def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size)

def draw_amis_falo(draw, cx, cy, radius, color):
    """台東阿美族八角花神聖幾何標誌"""
    points = []
    inner_r = radius * 0.42
    for i in range(16):
        angle = i * (math.pi / 8) - (math.pi / 2)
        r = radius if (i % 2 == 0) else inner_r
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=None, outline=color, width=2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)

# ==========================================
# 1. FB-01A: 純粹瑞士風格排版 (Swiss Typographic Master) - 1:1 (1200x1200)
# ==========================================
def render_fb_01a():
    W, H = 1200, 1200
    img = Image.new("RGB", (W, H), (20, 24, 28)) # 深石板玄武岩
    draw = ImageDraw.Draw(img)
    
    # 網格參考線與邊框 (留白率 35%)
    margin = 80
    inner_w = W - 2 * margin
    inner_h = H - 2 * margin
    
    # 雅緻外框雙細線
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(45, 52, 60), width=1)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(35, 40, 48), width=1)
    
    # 左上角：八角花與品牌身分標誌
    falo_x, falo_y = margin + 45, margin + 45
    draw_amis_falo(draw, falo_x, falo_y, 22, (212, 163, 71)) # 琥珀金
    
    font_brand = get_font(20, bold=True)
    draw.text((falo_x + 38, falo_y - 14), "生活管家 · 家宅總部", fill=(212, 163, 71), font=font_brand)
    font_sub_brand = get_font(15, bold=False)
    draw.text((falo_x + 38, falo_y + 12), "TAITUNG · 2026 AUTUMN WORKSHOP", fill=(140, 150, 160), font=font_sub_brand)
    
    # 右上角：極具約束力的班別編號
    font_code = get_font(18, bold=True)
    draw.text((W - margin - 220, margin + 35), "LESSON 01 實體手把手", fill=(240, 240, 245), font=font_code)
    draw.rectangle([W - margin - 225, margin + 65, W - margin - 30, margin + 66], fill=(212, 163, 71))
    
    # 水平分隔線
    draw.line([(margin + 30, margin + 95), (W - margin - 30, margin + 95)], fill=(50, 58, 68), width=1)
    
    # 中上部：第一凝視點（頂部 28%~35%）- 主標題
    title_y = 230
    font_lead = get_font(24, bold=False)
    draw.text((margin + 50, title_y), "給在台東打拼、每天被雜事追著跑的自營店家：", fill=(180, 190, 200), font=font_lead)
    
    font_h1 = get_font(64, bold=True)
    draw.text((margin + 50, title_y + 55), "把時間買回來，", fill=(255, 255, 255), font=font_h1)
    draw.text((margin + 50, title_y + 140), "多陪陪家人。", fill=(212, 163, 71), font=font_h1)
    
    # 核心引言對白區塊 (卡片底襯)
    card_y = title_y + 260
    card_h = 290
    draw.rectangle([margin + 40, card_y, W - margin - 40, card_y + card_h], fill=(28, 33, 40), outline=(60, 70, 82), width=1)
    # 左側引言豎條裝飾
    draw.rectangle([margin + 40, card_y, margin + 48, card_y + card_h], fill=(212, 163, 71))
    
    font_quote = get_font(22, bold=False)
    font_quote_bold = get_font(23, bold=True)
    lines = [
        ("每天備料、進貨、算帳、回客人訊息，常常一個人當三個人用。", False),
        ("等忙完坐下來，夜深了，孩子也睡了。", False),
        ("我們那麼努力，本是為了給家人更好的生活，", True),
        ("最後卻連好好陪他們吃頓飯的時間，都被雜事吃得乾乾淨淨。", True),
        ("這幾個月，我用 AI 在電腦裡打造了專屬辦公室。不是為了追科技潮流，", False),
        ("只是想幫自己買回一點時間，多留心力過生活。", False),
    ]
    cur_y = card_y + 30
    for text, is_hl in lines:
        c = (255, 255, 255) if is_hl else (190, 200, 210)
        f = font_quote_bold if is_hl else font_quote
        draw.text((margin + 75, cur_y), text, fill=c, font=f)
        cur_y += 38
        
    # 底部實戰班承諾與規格閘門 (Level 3 行動區)
    foot_y = 880
    draw.line([(margin + 40, foot_y), (W - margin - 40, foot_y)], fill=(50, 58, 68), width=1)
    
    # 3 個關鍵數據方塊
    specs = [
        ("11/11 週三 14:00", "開課日期", "台東市正氣北路家宅總部"),
        ("嚴格限額 10 席", "教學紀律", "導師手把手巡桌排錯"),
        ("做完專屬成果", "課堂承諾", "沒做出成果不准下課")
    ]
    block_w = (inner_w - 80) // 3
    for idx, (head, tag, desc) in enumerate(specs):
        bx = margin + 40 + idx * block_w
        # 小標籤
        font_tag = get_font(14, bold=True)
        draw.rectangle([bx, foot_y + 25, bx + 70, foot_y + 45], fill=(45, 55, 68))
        draw.text((bx + 8, foot_y + 27), tag, fill=(212, 163, 71), font=font_tag)
        # 標題
        font_head = get_font(21, bold=True)
        draw.text((bx, foot_y + 55), head, fill=(255, 255, 255), font=font_head)
        # 說明
        font_desc = get_font(15, bold=False)
        draw.text((bx, foot_y + 90), desc, fill=(150, 160, 170), font=font_desc)
        
    # 最底層行動呼籲
    cta_y = 1045
    draw.rectangle([margin + 40, cta_y, W - margin - 40, cta_y + 55], fill=(35, 42, 52), outline=(212, 163, 71), width=1)
    font_cta = get_font(20, bold=True)
    draw.text((margin + 65, cta_y + 14), "💬 課表與實體入席申請表，請見【第一則留言】", fill=(245, 245, 250), font=font_cta)
    draw.text((W - margin - 220, cta_y + 16), "老學員 0 元免單回娘家 →", fill=(212, 163, 71), font=get_font(16, bold=True))
    
    out_path = os.path.join(OUT_DIR_FB, "FB_01_Time_And_Family_Swiss.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    # copy to brain
    img.save(os.path.join(BRAIN_DIR, "FB_01_Time_And_Family_Swiss.png"))
    return out_path

# ==========================================
# 2. FB-01B: 真實人文誌編排版 (Founder Photo Editorial) - 1:1 (1200x1200)
# ==========================================
def render_fb_01b():
    W, H = 1200, 1200
    img = Image.new("RGB", (W, H), (18, 20, 24))
    draw = ImageDraw.Draw(img)
    
    margin = 60
    # 左側 48% 為真實照片 (帶深邃膠卷色調與暗角)，右側 52% 為瑞士字體編排
    photo_w = 540
    photo_h = H - 2 * margin
    
    if os.path.exists(PHOTO_BOSS):
        boss_raw = Image.open(PHOTO_BOSS).convert("RGB")
        # 進行精準裁切填滿
        bw, bh = boss_raw.size
        target_ratio = photo_w / photo_h
        current_ratio = bw / bh
        if current_ratio > target_ratio:
            # 寬過多，切兩旁
            new_bw = int(bh * target_ratio)
            left = (bw - new_bw) // 2
            boss_cropped = boss_raw.crop((left, 0, left + new_bw, bh))
        else:
            new_bh = int(bw / target_ratio)
            top = int((bh - new_bh) * 0.2) # 偏上對焦臉部與眼鏡
            boss_cropped = boss_raw.crop((0, top, bw, top + new_bh))
            
        boss_resized = boss_cropped.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        
        # 加上底片調性：微降飽和度、提升對比，加深左下微暗角
        enhancer = ImageEnhance.Color(boss_resized)
        boss_graded = enhancer.enhance(0.75) # 沉著冷靜人文調
        
        # 貼上照片
        img.paste(boss_graded, (margin, margin))
        
        # 照片內微光感與邊緣羽化遮罩，自然融入背景
        photo_draw = ImageDraw.Draw(img)
        # 照片四周微細線
        photo_draw.rectangle([margin, margin, margin + photo_w, margin + photo_h], outline=(55, 62, 70), width=1)
        # 照片左上角浮水印
        photo_draw.text((margin + 25, margin + 25), "FOUNDER / PINSHUO", fill=(220, 225, 230), font=get_font(13, bold=True))
        photo_draw.text((margin + 25, margin + 45), "生活管家創辦人 · 實體家教導師", fill=(180, 185, 190), font=get_font(12, bold=False))
        # 照片底部小標記
        photo_draw.rectangle([margin + 25, margin + photo_h - 75, margin + photo_w - 25, margin + photo_h - 25], fill=(15, 18, 22))
        photo_draw.text((margin + 40, margin + photo_h - 63), "「雜事交給 AI，時間還給家人。」", fill=(212, 163, 71), font=get_font(16, bold=True))
    
    # 右側資訊區
    rx = margin + photo_w + 50
    rw = W - margin - rx
    
    # 右上品牌
    draw_amis_falo(draw, rx + 15, margin + 30, 16, (212, 163, 71))
    draw.text((rx + 42, margin + 18), "生活管家 · 家宅總部", fill=(212, 163, 71), font=get_font(17, bold=True))
    draw.text((rx + 42, margin + 40), "2026 秋季 AI 家教實戰班", fill=(140, 150, 160), font=get_font(13, bold=False))
    
    draw.line([(rx, margin + 75), (W - margin, margin + 75)], fill=(45, 52, 60), width=1)
    
    # 大主標
    draw.text((rx, margin + 110), "在台東做生意這幾年，", fill=(180, 190, 200), font=get_font(20, bold=False))
    draw.text((rx, margin + 145), "時間永遠不夠用。", fill=(255, 255, 255), font=get_font(36, bold=True))
    
    draw.text((rx, margin + 220), "把時間買回來，", fill=(212, 163, 71), font=get_font(44, bold=True))
    draw.text((rx, margin + 280), "多陪陪家人。", fill=(255, 255, 255), font=get_font(44, bold=True))
    
    # 引文內容
    p_y = margin + 370
    p_texts = [
        "每天備料、進貨、算帳、回客人，常常一個人當三個人用。",
        "忙完坐下夜深了，孩子也睡了。",
        "",
        "我們那麼努力是為了給家人更好的生活，",
        "最後卻連陪他們吃頓飯的時間都被吃光。",
        "",
        "學 AI 不是為了追潮流，",
        "只是想買回屬於自己的時間與生活心力。"
    ]
    f_p = get_font(17, bold=False)
    for t in p_texts:
        if t == "":
            p_y += 12
            continue
        c = (245, 245, 245) if ("家人" in t or "時間" in t) else (175, 185, 195)
        draw.text((rx, p_y), t, fill=c, font=f_p)
        p_y += 28
        
    # 下方重點卡片
    p_y += 25
    draw.rectangle([rx, p_y, W - margin, p_y + 180], fill=(26, 30, 36), outline=(50, 60, 72), width=1)
    draw.rectangle([rx, p_y, rx + 6, p_y + 180], fill=(212, 163, 71))
    
    draw.text((rx + 25, p_y + 20), "📌 11/11 (週三) 14:00 - 16:00 首講", fill=(255, 255, 255), font=get_font(18, bold=True))
    draw.text((rx + 25, p_y + 55), "📍 地點：生活管家總部（台東市正氣北路166巷90號）", fill=(180, 190, 200), font=get_font(15, bold=False))
    draw.text((rx + 25, p_y + 85), "⚠️ 100% 純實體教學 ｜ 限額 10 席 ｜ 手把手巡桌排錯", fill=(212, 163, 71), font=get_font(15, bold=True))
    draw.text((rx + 25, p_y + 115), "🌟 沒做出專屬成果不准下課！老學員免單回娘家", fill=(200, 210, 220), font=get_font(15, bold=False))
    draw.text((rx + 25, p_y + 145), "💬 線上申請表請見【第一則留言】", fill=(100, 200, 255), font=get_font(15, bold=True))
    
    # 底部簽名
    draw.text((rx, H - margin - 30), "—— 生活管家 闆仔（陳品碩）寫於台東", fill=(130, 140, 150), font=get_font(15, bold=False))
    
    out_path = os.path.join(OUT_DIR_FB, "FB_01_Time_And_Family_Editorial.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    img.save(os.path.join(BRAIN_DIR, "FB_01_Time_And_Family_Editorial.png"))
    return out_path

# ==========================================
# 3. TH-01: 脆專用直式深夜手寫行程卡 (Threads Midnight Note) - 4:5 (1080x1350)
# ==========================================
def render_th_01():
    W, H = 1080, 1350
    # 深邃午夜藍黑 (#0B0F14)，高對比反塑料感
    img = Image.new("RGB", (W, H), (12, 15, 20))
    draw = ImageDraw.Draw(img)
    
    margin = 65
    
    # 頂部時戳與微型座標（像老闆深夜隨手發文前的真實備忘錄）
    font_mono = get_font(18, bold=True)
    draw.text((margin, margin), "23:45 PM · 台東正氣北路", fill=(120, 135, 150), font=font_mono)
    draw.text((W - margin - 150, margin), "[MEMO #01]", fill=(120, 135, 150), font=font_mono)
    draw.line([(margin, margin + 35), (W - margin, margin + 35)], fill=(35, 42, 52), width=1)
    
    # 震撼問題標題
    y = margin + 70
    draw.text((margin, y), "做物流、管店鋪這幾年，", fill=(180, 190, 205), font=get_font(26, bold=False))
    y += 45
    draw.text((margin, y), "最深的體會只有一個：", fill=(180, 190, 205), font=get_font(26, bold=False))
    y += 55
    draw.text((margin, y), "我們的時間，", fill=(255, 255, 255), font=get_font(52, bold=True))
    y += 75
    draw.text((margin, y), "真的永遠不夠用。", fill=(230, 57, 70), font=get_font(52, bold=True))
    
    # 畫一張真實小老闆的一天行程卡 (Schedule Card)
    y += 110
    card_top = y
    card_h = 360
    draw.rectangle([margin, card_top, W - margin, card_top + card_h], fill=(18, 22, 30), outline=(45, 55, 68), width=1)
    
    # 卡片標題
    draw.rectangle([margin, card_top, margin + 6, card_top + card_h], fill=(230, 57, 70))
    draw.text((margin + 30, card_top + 20), "自營店家日常時間流水帳（一個人的三頭六臂）", fill=(150, 165, 180), font=get_font(16, bold=True))
    
    schedule = [
        ("07:30", "開車載貨、進冰庫備料、搬箱堆疊"),
        ("10:30", "回客人改單催單訊息、緊急補叫耗材"),
        ("14:00", "跑物流送件、庫存盤點、處理退換貨"),
        ("18:30", "晚班巡店、對 POS 機收銀帳、結算跑腿費"),
        ("22:00", "夜深了，小孩睡了，晚飯還沒吃...")
    ]
    sy = card_top + 60
    for t_str, s_desc in schedule:
        is_night = ("22:00" in t_str)
        t_col = (230, 57, 70) if is_night else (212, 163, 71)
        d_col = (255, 255, 255) if is_night else (190, 200, 210)
        draw.text((margin + 30, sy), t_str, fill=t_col, font=get_font(18, bold=True))
        draw.text((margin + 115, sy), s_desc, fill=d_col, font=get_font(18, bold=is_night))
        sy += 55
        
    # 紅筆手寫圈註感區塊 (The Brutal Punchline)
    y = card_top + card_h + 50
    draw.rectangle([margin, y, W - margin, y + 170], fill=(24, 28, 38), outline=(230, 57, 70), width=2)
    # 警示紅條
    draw.rectangle([margin + 10, y + 10, margin + 14, y + 160], fill=(230, 57, 70))
    
    font_p1 = get_font(23, bold=True)
    draw.text((margin + 35, y + 30), "「我們那麼努力，本是為了給家人更好的生活，", fill=(255, 255, 255), font=font_p1)
    draw.text((margin + 35, y + 75), "最後卻連好好陪他們吃頓飯的時間，", fill=(255, 255, 255), font=font_p1)
    draw.text((margin + 35, y + 120), "都被雜事吃得乾乾淨淨。」", fill=(230, 57, 70), font=get_font(24, bold=True))
    
    # 破局與實體教室
    y += 215
    draw.text((margin, y), "這幾個月我用 AI 打造了一套虛擬辦公室，把雜事理順。", fill=(185, 195, 205), font=get_font(20, bold=False))
    y += 35
    draw.text((margin, y), "不是追潮流，只是想把屬於自己的時間買回來。", fill=(212, 163, 71), font=get_font(21, bold=True))
    
    # 底部實戰邀請 (Threads 專屬真實手寫卡片)
    y += 65
    draw.rectangle([margin, y, W - margin, y + 125], fill=(16, 20, 26), outline=(60, 70, 85), width=1)
    draw.text((margin + 25, y + 20), "11/11 (週三) 下午 14:00 · 台東生活管家總部", fill=(255, 255, 255), font=get_font(19, bold=True))
    draw.text((margin + 25, y + 55), "嚴格限額 10 個人，多一張椅子都沒有。坐在身邊手把手教。", fill=(180, 190, 200), font=get_font(16, bold=False))
    draw.text((margin + 25, y + 88), "想把時間找回來的，留言區填表單，來喝杯熱茶吧 ☕", fill=(212, 163, 71), font=get_font(16, bold=True))
    
    out_path = os.path.join(OUT_DIR_TH, "TH_01_Midnight_Schedule.png")
    img.save(out_path, quality=95)
    print("Generated:", out_path)
    img.save(os.path.join(BRAIN_DIR, "TH_01_Midnight_Schedule.png"))
    return out_path

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    p1 = render_fb_01a()
    p2 = render_fb_01b()
    p3 = render_th_01()
    print("All 3 designs rendered successfully!")
