# -*- coding: utf-8 -*-
"""
生成生活管家 2026 秋季實戰家教班 · 第 3 講宣傳圖片 (3 張 4:5 1080x1350)
修正版：徹底移除所有未支援之 Emoji 與特殊 Unicode 符號，100% 杜絕方框豆腐塊 (□) 亂碼！
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering\images"
DESKTOP_DIR = r"C:\Users\lenovo\Desktop\第3講宣傳圖卡"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

FONT_PATH_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_PATH_REG = "C:/Windows/Fonts/msjh.ttc"

def get_font(size, bold=False):
    path = FONT_PATH_BOLD if bold else FONT_PATH_REG
    return ImageFont.truetype(path, size)

# 顏色定義
C_BG = (10, 15, 29)             # 深藍黑
C_CARD = (18, 26, 47)           # 卡片深藍
C_BORDER = (56, 189, 248)       # 青藍
C_WHITE = (248, 250, 252)       # 純白
C_MUTED = (148, 163, 184)       # 淺灰藍
C_LIGHT_GRAY = (203, 213, 225)  # 高對比淺灰
C_AMBER = (245, 158, 11)        # 琥珀金
C_EMERALD = (16, 185, 129)      # 翡翠綠
C_ROSE = (244, 63, 94)          # 玫瑰紅
C_PURPLE = (168, 85, 247)       # 紫色

def draw_header_badge(draw, text, y=60, color=C_AMBER, bg_color=(20, 30, 55)):
    font = get_font(26, bold=True)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad_x, pad_y = 28, 14
    box_w = w + pad_x * 2
    box_h = h + pad_y * 2
    x0 = (1080 - box_w) // 2
    y0 = y
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=24, fill=bg_color, outline=color, width=2)
    draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=font, fill=color)
    return y0 + box_h

def draw_footer_bar(draw, text_left, text_right):
    y0 = 1250
    draw.line([(60, y0), (1020, y0)], fill=(40, 55, 85), width=2)
    font = get_font(24, bold=True)
    draw.text((60, y0 + 25), text_left, font=font, fill=C_MUTED)
    
    font_r = get_font(24, bold=True)
    bbox = font_r.getbbox(text_right)
    rw = bbox[2] - bbox[0]
    draw.text((1020 - rw, y0 + 25), text_right, font=font_r, fill=C_AMBER)

# ==========================================
# 圖 1: 三部曲演進全景圖
# ==========================================
def create_image_1():
    img = Image.new("RGB", (1080, 1350), C_BG)
    draw = ImageDraw.Draw(img)
    
    y = draw_header_badge(draw, "生活管家 · 2026 秋季實戰家教班", y=55, color=C_AMBER)
    
    y += 30
    title = "從大腦、手腳到靈魂"
    font_t = get_font(52, bold=True)
    bbox = font_t.getbbox(title)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, y), title, font=font_t, fill=C_WHITE)
    
    y += 75
    sub = "三週打造一台「像你親自顧店」的 AI 專屬數位發射台"
    font_s = get_font(25, bold=False)
    bbox = font_s.getbbox(sub)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, y), sub, font=font_s, fill=C_BORDER)
    
    cards = [
        ("第 1 講 · 大腦成形 (10/28)", "NotebookLM 深度消化真實資料 → 海報文案", "【突破】解決：「不知道要寫什麼、內容雜亂」\n【成果】大腦智囊就位，產出專屬故事海報", C_CARD, C_BORDER),
        ("第 2 講 · 手腳串通 (11/18)", "Meta 官方 API 直連 → 照片一傳，AI 幫你發文！", "【突破】解決：「開店忙碌沒空天天手動複製貼上」\n【成果】打通官方通道，3 秒自動發布與留言導流", C_CARD, C_AMBER),
        ("第 3 講 · 注入靈魂 (11/25 壓軸)", "SSOT 商業架構 與 擬人化捏臉 → 接地氣有溫度！", "【突破】解決：「AI 講話冷冰冰、滿滿塑膠公文罐頭味」\n【成果】現場捏出專屬分身，開口就像老闆親自說話", (25, 38, 70), C_EMERALD)
    ]
    
    card_y = y + 70
    for tag, headline, detail, bg_c, border_c in cards:
        draw.rounded_rectangle([60, card_y, 1020, card_y + 225], radius=18, fill=bg_c, outline=border_c, width=3 if border_c == C_EMERALD else 2)
        
        f_tag = get_font(22, bold=True)
        draw.text((95, card_y + 22), tag, font=f_tag, fill=border_c)
        
        f_head = get_font(28, bold=True)
        draw.text((95, card_y + 60), headline, font=f_head, fill=C_WHITE)
        
        f_det = get_font(21, bold=False)
        lines = detail.split("\n")
        draw.text((95, card_y + 115), lines[0], font=f_det, fill=C_LIGHT_GRAY)
        draw.text((95, card_y + 155), lines[1], font=f_det, fill=border_c if border_c == C_EMERALD else C_AMBER)
        
        card_y += 255
        
    draw_footer_bar(draw, "地點：台東市正氣北路166巷90號（家宅總部）", "★ 純實體教學 · 嚴格限額 6 席")
    
    path = os.path.join(OUTPUT_DIR, "FB_L03_01_Evolution_Trilogy.png")
    img.save(path)
    shutil.copy2(path, os.path.join(DESKTOP_DIR, "FB_L03_01_Evolution_Trilogy.png"))
    print("Saved Image 1 cleanly:", path)

# ==========================================
# 圖 2: 反差對照圖
# ==========================================
def create_image_2():
    img = Image.new("RGB", (1080, 1350), C_BG)
    draw = ImageDraw.Draw(img)
    
    y = draw_header_badge(draw, "拒絕冷冰冰公文腔 · 告別塑膠罐頭感", y=55, color=C_ROSE)
    
    y += 30
    title = "你的 AI 是冷血機器人？"
    font_t = get_font(48, bold=True)
    bbox = font_t.getbbox(title)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, y), title, font=font_t, fill=C_WHITE)
    
    y += 68
    title2 = "還是像你「親自顧店」的專屬分身？"
    font_t2 = get_font(42, bold=True)
    bbox2 = font_t2.getbbox(title2)
    draw.text(((1080 - (bbox2[2] - bbox2[0])) // 2, y), title2, font=font_t2, fill=C_EMERALD)
    
    card_w = 460
    card_h = 670
    card_top = 285
    
    # 左卡: 傳統冷冰冰 AI
    draw.rounded_rectangle([60, card_top, 60 + card_w, card_top + card_h], radius=18, fill=C_CARD, outline=C_ROSE, width=2)
    draw.text((95, card_top + 30), "【傳統冷冰冰 AI】", font=get_font(28, bold=True), fill=C_ROSE)
    
    left_items = [
        "• 開口第一句：\n  「尊敬的顧客您好，感謝諮詢」",
        "• 滿嘴官腔公文味，死板毫無人情味",
        "• 每次問都要重新提醒規則與細節",
        "• 電腦檔案越存越亂，AI 經常瞎掰",
        "• 客人一秒看穿是機器人，失去信任"
    ]
    cur_y = card_top + 95
    for item in left_items:
        draw.text((95, cur_y), item, font=get_font(21), fill=C_LIGHT_GRAY)
        cur_y += 105
        
    # 右卡: 注入靈魂的 AI 分身
    draw.rounded_rectangle([560, card_top, 560 + card_w, card_top + card_h], radius=18, fill=(20, 35, 60), outline=C_EMERALD, width=3)
    draw.text((595, card_top + 30), "【注入靈魂的 AI 分身】", font=get_font(28, bold=True), fill=C_EMERALD)
    
    right_items = [
        "• 開口第一句：\n  「阿姐早！今天剛進好料，幫你留？」",
        "• 像闆娘親自倒茶寒暄，接地氣有溫度",
        "• SSOT 乾淨資料庫，永遠報對價錢",
        "• 刻印你的說話習慣與情緒底線",
        "• 客人聊得舒服，自然產生商業黏著！"
    ]
    cur_y = card_top + 95
    for item in right_items:
        draw.text((595, cur_y), item, font=get_font(21), fill=C_LIGHT_GRAY)
        cur_y += 105

    # 下方重點召集框
    box_y = card_top + card_h + 30
    draw.rounded_rectangle([60, box_y, 1020, box_y + 170], radius=16, fill=(15, 23, 42), outline=C_AMBER, width=2)
    f_call = get_font(26, bold=True)
    draw.text((95, box_y + 25), "★ 11/25 (週三) 14:00 現場實機一對一調教", font=f_call, fill=C_AMBER)
    f_sub = get_font(22, bold=False)
    draw.text((95, box_y + 70), "• 掌握五層同心圓捏臉法，徹底告別塑膠罐頭感！", font=f_sub, fill=C_WHITE)
    draw.text((95, box_y + 110), "• 沒現場捏出合格分身不准下課！", font=f_sub, fill=C_BORDER)

    draw_footer_bar(draw, "生活管家 · 家宅總部實體課", "★ 嚴格限額 6 席 · 額滿即關")
    
    path = os.path.join(OUTPUT_DIR, "FB_L03_02_Anti_Robot_Persona.png")
    img.save(path)
    shutil.copy2(path, os.path.join(DESKTOP_DIR, "FB_L03_02_Anti_Robot_Persona.png"))
    print("Saved Image 2 cleanly:", path)

# ==========================================
# 圖 3: 現場大招募海報
# ==========================================
def create_image_3():
    img = Image.new("RGB", (1080, 1350), C_BG)
    draw = ImageDraw.Draw(img)
    
    y = draw_header_badge(draw, "2026 秋季實戰家教班 · 終極壓軸篇", y=50, color=C_EMERALD)
    
    y += 25
    title = "為你的 AI 注入靈魂！"
    font_t = get_font(56, bold=True)
    bbox = font_t.getbbox(title)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, y), title, font=font_t, fill=C_WHITE)
    
    y += 85
    sub = "資料架構管理 與 AI 擬人化工程"
    font_s = get_font(36, bold=True)
    bbox = font_s.getbbox(sub)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, y), sub, font=font_s, fill=C_AMBER)
    
    y += 75
    banner_y = y
    draw.rounded_rectangle([60, banner_y, 1020, banner_y + 160], radius=16, fill=(20, 30, 55), outline=C_BORDER, width=2)
    draw.text((95, banner_y + 20), "【創辦人昨日實戰驗收心得】：", font=get_font(23, bold=True), fill=C_BORDER)
    draw.text((95, banner_y + 60), "「昨天帶著學員實際一步步操作將 AI 的臉書自動發文串接起來，", font=get_font(22, bold=False), fill=C_WHITE)
    draw.text((95, banner_y + 100), "之後只要傳照片給 AI，後續文案跟 Po 文步驟就讓 AI 幫你處理嘍！」", font=get_font(22, bold=True), fill=C_EMERALD)
    
    info_y = banner_y + 185
    draw.rounded_rectangle([60, info_y, 1020, info_y + 440], radius=18, fill=C_CARD, outline=C_EMERALD, width=3)
    
    draw.text((100, info_y + 30), "【第 3 講 課程資訊與保證】", font=get_font(30, bold=True), fill=C_WHITE)
    
    details = [
        ("上課時間", "2026-11-25 (週三) 14:00 - 16:00 (13:50 報到)"),
        ("上課地點", "生活管家·家宅總部（台東市正氣北路166巷90號）"),
        ("核心任務", "告別檔案垃圾場 ✕ 捏出像老闆親自說話的 AI 分身"),
        ("現場紀律", "100% 純實體教學 · 講師全場巡桌 · 沒捏出成果不准下課！"),
        ("限額席位", "★【嚴格限額 6 席】（老學員享 0 元回娘家免單特權）")
    ]
    
    cur_y = info_y + 90
    for label, val in details:
        draw.text((100, cur_y), label + "：", font=get_font(24, bold=True), fill=C_AMBER if "限額" in label or "時間" in label else C_BORDER)
        draw.text((250, cur_y), val, font=get_font(23, bold=True if "限額" in val else False), fill=C_EMERALD if "限額" in val else C_LIGHT_GRAY)
        cur_y += 65
        
    draw_footer_bar(draw, "【立即點擊】第一則留言填表搶席", "★ 僅限 6 席 · 額滿立刻關閉")
    
    path = os.path.join(OUTPUT_DIR, "FB_L03_03_Master_Recruit_Poster.png")
    img.save(path)
    shutil.copy2(path, os.path.join(DESKTOP_DIR, "FB_L03_03_Master_Recruit_Poster.png"))
    print("Saved Image 3 cleanly:", path)

if __name__ == "__main__":
    create_image_1()
    create_image_2()
    create_image_3()
    print("All 3 clean images generated successfully without any tofu boxes!")
