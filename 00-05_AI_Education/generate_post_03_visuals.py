import os
import sys
import math
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
# 1. FB-03: 瑞士國際主義 · 音訊摘要與通勤革命 (1200x1200)
# ==========================================
def render_fb_03():
    W, H = 1200, 1200
    bg_color = (250, 246, 237) # 溫潤暖奶油紙質 (#FAF6ED)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 70
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(220, 212, 196), width=2)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(40, 36, 32), width=1)
    
    # 頂部小標
    top_y = 110
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季實體家教班", fill=(120, 110, 100), font=get_font(18, bold=True), anchor="mm")
    
    # 震撼問題標題 (Level 1)
    title_y = top_y + 70
    draw.text((W // 2, title_y), "「從 30 頁死板公文，", fill=(30, 28, 25), font=get_font(52, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 68), "到 10 分鐘通勤雙人廣播。」", fill=(193, 18, 31), font=get_font(52, bold=True), anchor="mm")
    
    sub_y = title_y + 140
    draw.text((W // 2, sub_y), "科技不是用來供奉的，開車戴上耳機用聽的，雜事瞬間消化完！", fill=(80, 75, 70), font=get_font(23, bold=False), anchor="mm")
    
    # 中央視覺區：音訊轉換工作流卡片 (400px 高)
    card_y = sub_y + 45
    card_w = 920
    card_h = 380
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(255, 255, 255), outline=(40, 36, 32), width=2)
    
    # 頂部深色小標籤
    draw.rectangle([cx, card_y, cx + card_w, card_y + 44], fill=(40, 36, 32))
    draw.text((W // 2, card_y + 22), "【 Google NotebookLM · Audio Overview 雙人對談黑科技 】", fill=(245, 183, 56), font=get_font(18, bold=True), anchor="mm")
    
    # 卡片內部三步驟轉換
    steps = [
        ("【輸入】店內雜亂資料一鍵餵入", "進貨單據、補助公文、手寫筆記與長篇企劃，無需排版直接匯入！", (60, 90, 140)),
        ("【魔法】AI 自動重構為美式雙人 Podcast", "1 分鐘生成流利對話，兩位數位主持人幽默一搭一唱、深挖核心洞察！", (245, 183, 56)),
        ("【輸出】通勤開車、備料做家事戴耳機搞定", "把螢幕前的痛苦閱讀，徹底釋放為日常碎片時間的有聲高效吸收！", (193, 18, 31))
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
    draw.text((W // 2, foot_y + 75), "帶店裡資料現場做一段廣播帶回家  ·  限額 10 席  ·  做完專屬成果才准下課", fill=(100, 90, 80), font=font_sub2, anchor="mm")
    
    font_cta = get_font(19, bold=True)
    draw.text((W // 2, foot_y + 112), "老學員 0 元免單 · 線上申請請見【第一則留言】", fill=(193, 18, 31), font=font_cta, anchor="mm")
    
    out_fb = os.path.join(OUT_DIR_FB, "FB_03_Audio_Overview_Minimal.png")
    img.save(out_fb, quality=95)
    img.save(os.path.join(BRAIN_DIR, "FB_03_Audio_Overview_Minimal.png"))
    print("FB-03 Minimal generated:", out_fb)
    return out_fb

# ==========================================
# 2. TH-03: 脆專用 · 車載 Podcast 播放介面隨手拍 (1080x1350 4:5)
# ==========================================
def render_th_03():
    W, H = 1080, 1350
    # 車載夜間/灰黑沉浸氛圍 (#181C24)
    img = Image.new("RGB", (W, H), (24, 28, 36))
    draw = ImageDraw.Draw(img)
    
    margin = 45
    # 頂部狀態列
    draw.text((margin + 15, margin + 10), "17:42", fill=(160, 170, 185), font=get_font(18, bold=True))
    draw.text((W - margin - 140, margin + 10), "車載藍牙連線", fill=(70, 180, 120), font=get_font(16, bold=True))
    draw.line([(margin, margin + 45), (W - margin, margin + 45)], fill=(40, 48, 60), width=1)
    
    # 播放中卡片容器
    y = margin + 70
    card_h = 720
    draw.rectangle([margin, y, W - margin, y + card_h], fill=(32, 38, 50), outline=(55, 68, 88), width=2)
    
    # 頂部頻道標示
    draw.rectangle([margin + 30, y + 25, margin + 190, y + 60], fill=(245, 183, 56))
    draw.text((margin + 110, y + 42), "AI 語音隨選廣播", fill=(20, 24, 32), font=get_font(16, bold=True), anchor="mm")
    
    draw.text((W - margin - 35, y + 42), "NotebookLM Audio Overview", fill=(140, 155, 175), font=get_font(16, bold=False), anchor="rm")
    
    # 音訊標題
    draw.text((margin + 35, y + 95), "台東小店 11 月進貨成本與補助公文速報.mp3", fill=(255, 255, 255), font=get_font(26, bold=True))
    draw.text((margin + 35, y + 135), "兩位 AI 虛擬主持人 ｜ 深度研討對話模式", fill=(170, 185, 205), font=get_font(18, bold=False))
    
    # 模擬動態雙人對談波形 (Sound Waveform)
    wave_y = y + 185
    wave_w = W - margin * 2 - 70
    num_bars = 48
    bar_spacing = wave_w / num_bars
    for i in range(num_bars):
        # 模擬波峰波谷
        val = math.sin(i * 0.45) * math.cos(i * 0.25) * 50 + 60
        bx = margin + 35 + i * bar_spacing
        color = (245, 183, 56) if i < 28 else (70, 85, 110)
        draw.rounded_rectangle([bx, wave_y + 70 - val / 2, bx + 8, wave_y + 70 + val / 2], radius=4, fill=color)
        
    # 時間進度條
    prog_y = wave_y + 155
    draw.line([(margin + 35, prog_y), (W - margin - 35, prog_y)], fill=(55, 68, 88), width=6)
    draw.line([(margin + 35, prog_y), (margin + 35 + int(wave_w * 0.58), prog_y)], fill=(245, 183, 56), width=6)
    draw.ellipse([margin + 35 + int(wave_w * 0.58) - 8, prog_y - 8, margin + 35 + int(wave_w * 0.58) + 8, prog_y + 8], fill=(255, 255, 255))
    
    draw.text((margin + 35, prog_y + 22), "05:42", fill=(180, 190, 205), font=get_font(15, bold=False))
    draw.text((W - margin - 35, prog_y + 22), "09:48", fill=(120, 135, 155), font=get_font(15, bold=False), anchor="ra")
    
    # 雙人對談生動對白區
    chat_y = prog_y + 60
    draw.rectangle([margin + 25, chat_y, W - margin - 25, chat_y + 180], fill=(22, 26, 35), outline=(45, 55, 72))
    
    draw.text((margin + 45, chat_y + 25), "Host A（男聲）:「等等！這份進貨單跟上週比，海鮮成本直接跳了 15% 耶！」", fill=(245, 183, 56), font=get_font(19, bold=True))
    draw.text((margin + 45, chat_y + 70), "Host B（女聲）:「對啊！所以這份公文裡的節能補助剛好能補上缺口，", fill=(220, 230, 245), font=get_font(19, bold=False))
    draw.text((margin + 45, chat_y + 105), "　　　　　　　 建議老闆先把高利潤的限定私房菜推上首頁...」", fill=(220, 230, 245), font=get_font(19, bold=False))
    draw.text((margin + 45, chat_y + 145), "（開車聽完一邊笑一邊點頭，原本頭痛的 30 頁死公文全消化完了）", fill=(130, 145, 165), font=get_font(16, bold=False))

    # 底部實戰破局宣告卡
    by_foot = y + card_h + 35
    draw.rectangle([margin, by_foot, W - margin, by_foot + 380], fill=(32, 38, 50), outline=(55, 68, 88))
    draw.rectangle([margin, by_foot, margin + 8, by_foot + 380], fill=(245, 183, 56))
    
    draw.text((margin + 35, by_foot + 30), "開車從市區回知本的路上，", fill=(255, 255, 255), font=get_font(26, bold=True))
    draw.text((margin + 35, by_foot + 70), "聽兩個美國人把我店裡的進貨單聊完了...笑死，超實用！", fill=(245, 183, 56), font=get_font(21, bold=True))
    
    draw.text((margin + 35, by_foot + 120), "下週三下午在台東家宅，帶上你店裡最生硬的死資料：", fill=(190, 200, 215), font=get_font(18, bold=False))
    draw.text((margin + 35, by_foot + 155), "進貨單 ＋ 補助公文 ＋ 菜單品項  →  現場做一檔專屬廣播帶回家！", fill=(255, 255, 255), font=get_font(20, bold=True))
    draw.text((margin + 35, by_foot + 195), "從此開車不用盯螢幕，戴上耳機用聽的就全搞定。", fill=(190, 200, 215), font=get_font(18, bold=False))
    
    draw.line([(margin + 35, by_foot + 240), (W - margin - 35, by_foot + 240)], fill=(55, 68, 88), width=1)
    
    draw.text((margin + 35, by_foot + 265), "【時間地點】 11/11 (週三) 14:00 · 台東市正氣北路166巷90號（家宅）", fill=(245, 183, 56), font=get_font(19, bold=True))
    draw.text((margin + 35, by_foot + 305), "【報名須知】 純實體限額 10 席 ｜ 老學員 0 元免單 ｜ 留言區放表單", fill=(255, 255, 255), font=get_font(18, bold=True))
    
    out_th = os.path.join(OUT_DIR_TH, "TH_03_Car_Podcast_Player.jpg")
    img.save(out_th, quality=95)
    img.save(os.path.join(BRAIN_DIR, "TH_03_Car_Podcast_Player.jpg"))
    print("TH-03 generated:", out_th)
    return out_th

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    render_fb_03()
    render_th_03()
    print("All Post 03 visuals generated successfully!")
