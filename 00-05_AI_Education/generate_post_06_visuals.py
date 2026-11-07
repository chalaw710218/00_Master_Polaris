import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix"
OUT_DIR_FB = os.path.join(ROOT_DIR, "FB_Posts")
OUT_DIR_TH = os.path.join(ROOT_DIR, "Threads_Posts")
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"

os.makedirs(OUT_DIR_FB, exist_ok=True)
os.makedirs(OUT_DIR_TH, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_path = r"C:\Windows\Fonts\msjhbd.ttc" if bold else r"C:\Windows\Fonts\msjh.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# ==========================================
# 1. FB-06: 約瑟夫 Solari 機場機械翻牌倒數海報 (1200x1200)
# ==========================================
def render_fb_06():
    W, H = 1200, 1200
    # 工業啞光墨黑底色 (#0d1015)
    bg_color = (13, 16, 21)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_dark = (40, 50, 65)
    border_red = (220, 55, 45)
    amber_locked = (200, 145, 40)
    red_alert = (245, 65, 55)
    
    # 德式雙層外框
    draw.rectangle([margin, margin, W - margin, H - margin], outline=border_dark, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(25, 32, 42), width=1)
    
    # 四角機械標記
    corner_len = 24
    for cx, cy in [(margin + 12, margin + 12), (W - margin - 12, margin + 12), 
                   (margin + 12, H - margin - 12), (W - margin - 12, H - margin - 12)]:
        dx = 1 if cx == margin + 12 else -1
        dy = 1 if cy == margin + 12 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=red_alert, width=2)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=red_alert, width=2)

    # 頂部機械儀表板標籤
    top_y = margin + 35
    draw.text((W // 2, top_y), "FLIGHT GATE 1111 ｜ 正氣北路家宅 ｜ 席次最終召集令", fill=(170, 180, 195), font=get_font(18, bold=True), anchor="mm")
    
    # 震撼標題區：正選席次即刻關門
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 最後召集！正選席次即刻關閉，", fill=(235, 240, 248), font=get_font(40, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "堅持 10 人純實體 · 多一張椅子都不加！」", fill=red_alert, font=get_font(42, bold=True), anchor="mm")

    # 席次緊急通報長條
    badge_y = title_y + 115
    badge_w, badge_h = 800, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(32, 18, 18), outline=red_alert, width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=red_alert)
    draw.text((W // 2, badge_y + badge_h // 2), "【 登機門關閉倒數 】 10 席實體名額已過半 · 僅剩最後 5 席！", fill=(255, 215, 210), font=get_font(20, bold=True), anchor="mm")

    # 中央：Solari 10 席機械翻牌儀表板 (Mechanical Split-Flap Dashboard)
    board_y = badge_y + 68
    board_w = 1010
    board_h = 370
    bx = (W - board_w) // 2
    draw.rectangle([bx, board_y, bx + board_w, board_y + board_h], fill=(18, 22, 28), outline=(50, 60, 75), width=2)
    
    # 頂部狀態橫條
    draw.rectangle([bx, board_y, bx + board_w, board_y + 44], fill=(28, 34, 45))
    draw.text((bx + 30, board_y + 22), "SEAT ALLOCATION DASHBOARD ｜ 即時席次狀態雷達", fill=(160, 175, 195), font=get_font(16, bold=True), anchor="lm")
    draw.text((bx + board_w - 30, board_y + 22), "STATUS: FINAL CALLING", fill=red_alert, font=get_font(16, bold=True), anchor="rm")

    # 10 個席位插槽 (上下兩排，每排 5 個)
    slot_w = 175
    slot_h = 135
    gap_x = 18
    gap_y = 16
    start_x = bx + 22
    start_y = board_y + 60
    
    for i in range(10):
        row = i // 5
        col = i % 5
        sx = start_x + col * (slot_w + gap_x)
        sy = start_y + row * (slot_h + gap_y)
        seat_num = f"{i+1:02d}"
        
        if i < 5:
            # 01~05 號：已鎖定 (琥珀金 LOCKED)
            draw.rectangle([sx, sy, sx + slot_w, sy + slot_h], fill=(26, 28, 24), outline=amber_locked, width=2)
            # 中間翻牌折痕
            draw.line([(sx, sy + slot_h // 2), (sx + slot_w, sy + slot_h // 2)], fill=(40, 42, 35), width=1)
            draw.text((sx + 15, sy + 22), f"SEAT {seat_num}", fill=(160, 150, 130), font=get_font(15, bold=True))
            draw.text((sx + slot_w // 2, sy + 70), "LOCKED", fill=amber_locked, font=get_font(24, bold=True), anchor="mm")
            draw.text((sx + slot_w // 2, sy + 105), "正取已鎖定", fill=(210, 190, 150), font=get_font(14, bold=False), anchor="mm")
        else:
            # 06~10 號：最後召集 (警示紅 FINAL CALL)
            draw.rectangle([sx, sy, sx + slot_w, sy + slot_h], fill=(35, 18, 18), outline=red_alert, width=2)
            # 中間翻牌折痕
            draw.line([(sx, sy + slot_h // 2), (sx + slot_w, sy + slot_h // 2)], fill=(55, 25, 25), width=1)
            draw.text((sx + 15, sy + 22), f"SEAT {seat_num}", fill=(220, 140, 140), font=get_font(15, bold=True))
            draw.text((sx + slot_w // 2, sy + 70), "FINAL", fill=red_alert, font=get_font(24, bold=True), anchor="mm")
            draw.text((sx + slot_w // 2, sy + 105), "搶席倒數中", fill=(255, 200, 195), font=get_font(14, bold=True), anchor="mm")

    # 三週課表橫幅 (Curriculum Guide Bar) - 徹底避免 ✕，使用標準中圓點 · 與 ｜
    guide_y = board_y + board_h + 20
    guide_w = 1010
    guide_h = 70
    gx = (W - guide_w) // 2
    draw.rectangle([gx, guide_y, gx + guide_w, guide_y + guide_h], fill=(20, 25, 34), outline=(45, 55, 70), width=1)
    
    draw.text((gx + 25, guide_y + 15), "【秋季實戰三週全系列】", fill=(160, 175, 195), font=get_font(15, bold=True))
    draw.text((gx + 210, guide_y + 15), "11/11 第 1 講: NotebookLM 數位大腦 · 漏斗提問法 (最後 5 席即刻關門)", fill=red_alert, font=get_font(15, bold=True))
    draw.text((gx + 210, guide_y + 40), "11/18 第 2 講: Antigravity · 自動發文串接  ｜  11/25 第 3 講: 資料架構 · 數位店長分身", fill=(190, 205, 225), font=get_font(14, bold=False))

    # 底部關門原則與地點
    foot_y = guide_y + guide_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=red_alert, width=2)
    
    draw.text((W // 2, foot_y + 24), "每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(235, 240, 250), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "10 席正選額滿立即關閉表單 · 超額申請自動轉入候補梯次 ｜ 老學員回娘家 0 元免單", fill=(175, 185, 200), font=get_font(16, bold=False), anchor="mm")

    fb_path_1 = os.path.join(OUT_DIR_FB, "FB_06_Final_Call_Solari.png")
    fb_path_2 = os.path.join(BRAIN_DIR, "FB_06_Final_Call_Solari.png")
    img.save(fb_path_1, quality=95)
    img.save(fb_path_2, quality=95)
    print(f"✅ FB-06 海報生成完畢: {fb_path_1}")

# ==========================================
# 2. TH-06: 脆 (Threads) 後台倒數圖 (1080x1350 4:5)
# ==========================================
def render_th_06():
    W, H = 1080, 1350
    # 工業墨黑背景 (#101216)
    bg_color = (16, 18, 22)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 50
    red_alert = (245, 65, 55)
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(50, 55, 65), width=2)
    
    # 頂部小標
    draw.text((W // 2, margin + 40), "生活管家 · 家宅小教室 ｜ 招生最終通報", fill=(160, 170, 185), font=get_font(18, bold=False), anchor="mm")
    
    # 大字痛點反問
    draw.text((W // 2, margin + 110), "最後 5 席 · 即刻關門", fill=(255, 255, 255), font=get_font(52, bold=True), anchor="mm")
    draw.text((W // 2, margin + 175), "堅持 10 個人就 10 個人，多一張椅子都沒有。", fill=red_alert, font=get_font(30, bold=True), anchor="mm")
    
    # 中央黑色倒數卡片 (#1a1d24)
    card_y = margin + 240
    card_w = 880
    card_h = 600
    cx = (W - card_w) // 2
    draw.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=(22, 26, 33), outline=(65, 75, 95), width=2)
    
    # 卡片頂部紅條
    draw.rectangle([cx, card_y, cx + card_w, card_y + 12], fill=red_alert)
    
    draw.text((W // 2, card_y + 55), "【 審查與入席進度 】", fill=(240, 245, 255), font=get_font(26, bold=True), anchor="mm")
    
    points = [
        ("• 正選名額審查過半", "10 席實體座位目前僅剩最後 5 席，額滿即關門。"),
        ("• 系統自動排進行事曆", "審查通過的夥伴，正氣北路導航已直接同步入 Google 日曆。"),
        ("• 秋季三週完整課表", "11/11 數位智庫 ｜ 11/18 自動發文 ｜ 11/25 數位店長。"),
        ("• 手把手現場排錯到底", "前半段心法，後半段全員筆電打開巡桌盯著做。"),
        ("• 老朋友 0 元免單特權", "生活管家老學員回娘家全額免單，新朋友單堂 $500。")
    ]
    py = card_y + 110
    for title, desc in points:
        draw.text((cx + 50, py), title, fill=(255, 220, 215), font=get_font(22, bold=True))
        draw.text((cx + 50, py + 34), desc, fill=(175, 185, 200), font=get_font(18, bold=False))
        py += 95
        
    # 底部警示條 (無 Emoji，純標準 CJK)
    draw.rectangle([cx + 30, card_y + card_h - 75, cx + card_w - 30, card_y + card_h - 20], fill=(45, 18, 18), outline=red_alert, width=1)
    draw.text((W // 2, card_y + card_h - 48), "【 緊急關閉 】 額滿將即刻鎖定表單，超額填表自動轉入候補！", fill=(255, 205, 200), font=get_font(20, bold=True), anchor="mm")

    # 底部實體資訊
    foot_y = card_y + card_h + 50
    draw.text((W // 2, foot_y), "11/11 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(235, 240, 250), font=get_font(22, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 40), "最後席次申請表請見【第一則留言】，週三家宅見！", fill=(160, 170, 185), font=get_font(18, bold=False), anchor="mm")

    th_path_1 = os.path.join(OUT_DIR_TH, "TH_06_Final_Call_Form_Status.jpg")
    th_path_2 = os.path.join(BRAIN_DIR, "TH_06_Final_Call_Form_Status.jpg")
    img.save(th_path_1, quality=95)
    img.save(th_path_2, quality=95)
    print(f"✅ TH-06 配圖生成完畢: {th_path_1}")

if __name__ == "__main__":
    render_fb_06()
    render_th_06()
