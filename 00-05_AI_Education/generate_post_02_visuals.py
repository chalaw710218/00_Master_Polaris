import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR_FB = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts"
OUT_DIR_TH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts"
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"
STICKER_CLEAN = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\.user_uploaded\media_1793580557231_87c68fc1.jpg"

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"

def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size)

def get_circular_badge(diameter):
    raw = Image.open(STICKER_CLEAN).convert("RGBA")
    w, h = raw.size
    cx, cy = w // 2, h // 2
    radius = int(min(w, h) * 0.485)
    
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=255)
    
    circular = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    circular.paste(raw, (0, 0), mask=mask)
    cropped = circular.crop([cx - radius, cy - radius, cx + radius, cy + radius])
    return cropped.resize((diameter, diameter), Image.Resampling.LANCZOS)

# ==========================================
# 1. FB-02: 漏斗深挖對比大字版 (1200x1200 1:1)
# ==========================================
def render_fb_02():
    W, H = 1200, 1200
    bg_color = (250, 246, 237) # 溫潤奶油紙質
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 70
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(220, 212, 196), width=2)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(40, 36, 32), width=1)
    
    # 頂部小標 (垂直居中微調，杜絕任何 Unicode 字符缺字方塊)
    top_y = 110
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教班", fill=(120, 110, 100), font=get_font(18, bold=True), anchor="mm")
    
    # 震撼問題標題 (Level 1)
    title_y = top_y + 70
    draw.text((W // 2, title_y), "「問 AI 怎麼改善生意，", fill=(30, 28, 25), font=get_font(52, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 68), "它永遠回三千字官腔廢話。」", fill=(193, 18, 31), font=get_font(52, bold=True), anchor="mm")
    
    sub_y = title_y + 140
    draw.text((W // 2, sub_y), "真相不是 AI 不聰明，而是你一開局就急著求答案！", fill=(80, 75, 70), font=get_font(23, bold=False), anchor="mm")
    
    # 中央視覺區：三層漏斗結構卡片 (400px 高)
    card_y = sub_y + 45
    card_w = 920
    card_h = 380
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(255, 255, 255), outline=(40, 36, 32), width=2)
    
    # 頂部深色小標籤
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(40, 36, 32))
    draw.text((W // 2, card_y + 22), "【 漏斗式三層深挖提問法 · Funnel Prompting 】", fill=(245, 183, 56), font=get_font(18, bold=True), anchor="mm")
    
    # 三層梯級漏斗圖解
    steps = [
        ("第 1 層：先鋪全景 (Context)", "把店裡的菜單、進貨單、真實客群一次餵飽，未預熱絕不求解！", (245, 183, 56)),
        ("第 2 層：再逼細節 (Constraints)", "鎖死預算、人力、時間與台東在地限制，逼退教科書空話！", (230, 140, 30)),
        ("第 3 層：飽和求解 (Decision)", "當脈絡 100% 飽和，逼問精準行動清單，吐出來的解法刀刀見血！", (193, 18, 31))
    ]
    
    sy = card_y + 70
    for idx, (head, desc, color) in enumerate(steps):
        # 左側色塊標記
        draw.rectangle([cx + 35, sy, cx + 43, sy + 68], fill=color)
        draw.text((cx + 60, sy + 5), head, fill=(30, 30, 30), font=get_font(21, bold=True))
        draw.text((cx + 60, sy + 38), desc, fill=(100, 95, 90), font=get_font(16, bold=False))
        if idx < 2:
            draw.line([(cx + 35, sy + 85), (cx + card_w - 35, sy + 85)], fill=(235, 230, 220), width=1)
        sy += 100

    # 底部實戰與家宅座標 (Level 2 & 3)
    foot_y = card_y + card_h + 45
    draw.line([(W // 2 - 140, foot_y), (W // 2 + 140, foot_y)], fill=(245, 183, 56), width=3)
    
    font_venue = get_font(21, bold=True)
    draw.text((W // 2, foot_y + 38), "11/11 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(50, 45, 40), font=font_venue, anchor="mm")
    
    font_sub2 = get_font(18, bold=False)
    draw.text((W // 2, foot_y + 75), "自備筆電現場巡桌排錯  ·  限額 10 席  ·  做完專屬成果才准下課", fill=(100, 90, 80), font=font_sub2, anchor="mm")
    
    font_cta = get_font(19, bold=True)
    draw.text((W // 2, foot_y + 112), "老學員 0 元免單 · 線上申請請見【第一則留言】", fill=(193, 18, 31), font=font_cta, anchor="mm")
    
    out_fb = os.path.join(OUT_DIR_FB, "FB_02_Funnel_Prompting_Minimal.png")
    img.save(out_fb, quality=95)
    img.save(os.path.join(BRAIN_DIR, "FB_02_Funnel_Prompting_Minimal.png"))
    print("FB-02 Minimal generated:", out_fb)
    return out_fb

# ==========================================
# 2. TH-02: 脆專用 · ChatGPT 翻車截圖 ✕ 紅筆打叉 (1080x1350 4:5)
# ==========================================
def render_th_02():
    W, H = 1080, 1350
    # 模擬深色模式或乾淨的聊天介面底色 (#F7F7F8 淺灰白)
    img = Image.new("RGB", (W, H), (245, 245, 247))
    draw = ImageDraw.Draw(img)
    
    margin = 45
    # 頂部假手機狀態列
    draw.text((margin + 15, margin + 10), "09:41", fill=(60, 60, 60), font=get_font(18, bold=True))
    draw.text((W - margin - 120, margin + 10), "5G  100%", fill=(60, 60, 60), font=get_font(16, bold=True))
    draw.line([(margin, margin + 45), (W - margin, margin + 45)], fill=(225, 225, 230), width=1)
    
    # 模擬 ChatGPT 對話對話框
    y = margin + 70
    
    # 使用者發問氣泡 (右側靠齊，淺灰藍)
    q_text = "老闆問：我的小店預算只有兩萬，想改善營收該怎麼做？"
    font_chat = get_font(21, bold=False)
    draw.rectangle([W - margin - 640, y, W - margin, y + 80], fill=(230, 235, 245), outline=(200, 210, 230))
    draw.text((W - margin - 615, y + 25), q_text, fill=(30, 40, 60), font=get_font(21, bold=True))
    
    # AI 回覆區塊 (左側，經典白底卡片)
    y += 115
    card_h = 620
    draw.rectangle([margin, y, W - margin, y + card_h], fill=(255, 255, 255), outline=(215, 215, 225), width=2)
    
    # ChatGPT 小頭像與名字
    draw.ellipse([margin + 25, y + 20, margin + 65, y + 60], fill=(16, 163, 127)) # OpenAI 綠
    draw.text((margin + 36, y + 26), "AI", fill=(255, 255, 255), font=get_font(18, bold=True))
    draw.text((margin + 80, y + 28), "ChatGPT (專業官腔模式)", fill=(100, 100, 100), font=get_font(18, bold=True))
    
    # 官腔回答內容
    fluff_lines = [
        "這是一個非常好的問題！針對您的情況，建議如下：",
        "",
        "1. 加強社群宣傳：定期在社群發布優質內容與短影音。",
        "2. 提升品牌知名度：打造動人的在地品牌故事與形象。",
        "3. 精準鎖定受眾：分析消費者畫像，實施針對性行銷。",
        "4. 推出促銷方案：舉辦滿額折扣、買一送一或會員優惠。",
        "5. 改善顧客體驗：以賓至如歸的服務提升客戶回購率...",
        "",
        "總結來說，只要持之以恆，營業額一定能穩步成長！"
    ]
    cy = y + 80
    for fl in fluff_lines:
        c = (60, 60, 60) if fl.startswith("1.") or fl.startswith("2.") or fl.startswith("3.") else (120, 120, 120)
        draw.text((margin + 35, cy), fl, fill=c, font=get_font(20, bold=False))
        cy += 45
        
    # 重磅刺眼粗紅筆：大叉叉重重劃過 AI 的回答區！
    # 畫出帶有厚度的手繪質感紅叉
    red_color = (220, 38, 38)
    draw.line([(margin + 50, y + 100), (W - margin - 50, y + card_h - 60)], fill=red_color, width=12)
    draw.line([(margin + 50, y + card_h - 60), (W - margin - 50, y + 100)], fill=red_color, width=12)
    
    # 刺眼手寫憤怒圈註框
    box_w, box_h = 360, 110
    bx = (W - box_w) // 2
    by = y + (card_h - box_h) // 2
    draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(255, 255, 255), outline=red_color, width=6)
    draw.text((W // 2, by + box_h // 2), "幹！誰不知道？！", fill=red_color, font=get_font(42, bold=True), anchor="mm")
    
    # 下方自嘲與實戰破局區
    by_foot = y + card_h + 45
    draw.rectangle([margin, by_foot, W - margin, by_foot + 380], fill=(24, 28, 36), outline=(50, 60, 75))
    draw.rectangle([margin, by_foot, margin + 8, by_foot + 380], fill=(245, 183, 56))
    
    draw.text((margin + 35, by_foot + 30), "為什麼 AI 永遠回三千字教科書廢話？", fill=(255, 255, 255), font=get_font(26, bold=True))
    draw.text((margin + 35, by_foot + 75), "因為你一開局就急著求答案，脈絡（Context）根本沒熱身！", fill=(245, 183, 56), font=get_font(20, bold=True))
    
    draw.text((margin + 35, by_foot + 125), "下週三下午在台東家宅，現場拆解「三層深挖提問法」：", fill=(190, 200, 210), font=get_font(18, bold=False))
    draw.text((margin + 35, by_foot + 160), "先鋪全景  →  再逼細節  →  脈絡飽和了才求解！", fill=(255, 255, 255), font=get_font(21, bold=True))
    draw.text((margin + 35, by_foot + 200), "吐出來的答案立刻刀刀見血，現場做完專屬成果才准走。", fill=(190, 200, 210), font=get_font(18, bold=False))
    
    draw.line([(margin + 35, by_foot + 245), (W - margin - 35, by_foot + 245)], fill=(60, 70, 85), width=1)
    
    draw.text((margin + 35, by_foot + 270), "【時間地點】 11/11 (週三) 14:00 · 台東市正氣北路166巷90號（家宅）", fill=(245, 183, 56), font=get_font(19, bold=True))
    draw.text((margin + 35, by_foot + 310), "【報名須知】 純實體限額 10 席 ｜ 老學員 0 元免單 ｜ 留言區放表單", fill=(255, 255, 255), font=get_font(18, bold=True))
    
    out_th = os.path.join(OUT_DIR_TH, "TH_02_ChatGPT_Fluff_Red_Cross.jpg")
    img.save(out_th, quality=95)
    img.save(os.path.join(BRAIN_DIR, "TH_02_ChatGPT_Fluff_Red_Cross.jpg"))
    print("TH-02 generated:", out_th)
    return out_th

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    render_fb_02()
    render_th_02()
    print("All Post 02 visuals generated successfully!")
