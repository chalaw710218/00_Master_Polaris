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
# 1. FB-05: 約瑟夫德式天平價值對照海報 (1200x1200)
# ==========================================
def render_fb_05():
    W, H = 1200, 1200
    # 深海軍藍石墨底色 (#121926)，徹底跳脫米黃與碳黑，建立第三種視覺層次
    bg_color = (18, 25, 38)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 55
    border_blue = (45, 75, 115)
    accent_blue = (70, 130, 200)
    gold_highlight = (245, 183, 56)
    
    # 德式外框
    draw.rectangle([margin, margin, W - margin, H - margin], outline=border_blue, width=2)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=(30, 48, 75), width=1)
    
    # 四角幾何標記
    corner_len = 20
    for cx, cy in [(margin + 12, margin + 12), (W - margin - 12, margin + 12), 
                   (margin + 12, H - margin - 12), (W - margin - 12, H - margin - 12)]:
        dx = 1 if cx == margin + 12 else -1
        dy = 1 if cy == margin + 12 else -1
        draw.line([(cx, cy), (cx + dx * corner_len, cy)], fill=accent_blue, width=2)
        draw.line([(cx, cy), (cx, cy + dy * corner_len)], fill=accent_blue, width=2)

    # 頂部標籤
    top_y = margin + 35
    draw.text((W // 2, top_y), "生活管家 · 家宅 ｜ 2026 秋季單元經濟價值精算", fill=(130, 165, 210), font=get_font(18, bold=True), anchor="mm")
    
    # 核心金句大標題
    title_y = top_y + 55
    draw.text((W // 2, title_y), "「 500 元連兩杯燕麥奶拿鐵都不夠，", fill=(215, 228, 245), font=get_font(40, bold=True), anchor="mm")
    draw.text((W // 2, title_y + 54), "但在這裡，能為你買回一整年的時間！」", fill=gold_highlight, font=get_font(42, bold=True), anchor="mm")

    # 緊急席次警示條 (已過半，僅剩 5 席)
    badge_y = title_y + 115
    badge_w, badge_h = 760, 48
    bx = (W - badge_w) // 2
    draw.rectangle([bx, badge_y, bx + badge_w, badge_y + badge_h], fill=(28, 38, 56), outline=(220, 80, 60), width=2)
    draw.rectangle([bx, badge_y, bx + 10, badge_y + badge_h], fill=(220, 80, 60))
    draw.text((W // 2, badge_y + badge_h // 2), "【 席次緊急通報 】 10 席實體名額已過半 · 僅剩最後 5 席！", fill=(255, 225, 215), font=get_font(20, bold=True), anchor="mm")

    # 中央左右天平對抗資訊盒 (The Balance Grid)
    grid_y = badge_y + 68
    grid_w = 1010
    col_w = 485
    gap = 40
    card_h = 370
    left_x = (W - grid_w) // 2
    right_x = left_x + col_w + gap
    
    # --- 左側卡片：連鎖拿鐵兩杯 (消耗品) ---
    draw.rectangle([left_x, grid_y, left_x + col_w, grid_y + card_h], fill=(24, 30, 42), outline=(60, 70, 88), width=2)
    draw.rectangle([left_x, grid_y, left_x + col_w, grid_y + 52], fill=(35, 42, 56))
    draw.text((left_x + col_w // 2, grid_y + 26), "連鎖燕麥奶拿鐵 2 杯 ｜ NT$ 520", fill=(185, 195, 210), font=get_font(18, bold=True), anchor="mm")
    
    left_items = [
        ("喝完就沒了", "15 分鐘飲用完畢，只留下一次性紙杯與熱量"),
        ("每日重複扣款", "屬於短暫生理提神，無法降低日常營運負擔"),
        ("雜事依舊堆成山", "進貨單照樣看花眼、客人私訊依然半夜回不完"),
        ("本質是摩擦成本", "純粹的個人日常消費，無法沉澱為生意資產")
    ]
    ly = grid_y + 75
    for tag, desc in left_items:
        draw.rectangle([left_x + 20, ly, left_x + 26, ly + 46], fill=(160, 75, 75)) # 暗紅標記
        draw.text((left_x + 40, ly + 2), tag, fill=(240, 160, 160), font=get_font(18, bold=True))
        draw.text((left_x + 40, ly + 26), desc, fill=(165, 175, 190), font=get_font(14, bold=False))
        ly += 68

    # --- 右側卡片：台東 AI 實戰大師班 (高價值資產) ---
    draw.rectangle([right_x, grid_y, right_x + col_w, grid_y + card_h], fill=(20, 36, 58), outline=gold_highlight, width=2)
    draw.rectangle([right_x, grid_y, right_x + col_w, grid_y + 52], fill=(28, 52, 85))
    draw.text((right_x + col_w // 2, grid_y + 26), "台東 AI 實戰大師班 ｜ NT$ 500 (老學員 $0)", fill=gold_highlight, font=get_font(18, bold=True), anchor="mm")
    
    right_items = [
        ("打造專屬數位大腦", "公文、進貨單 1 分鐘生雙人 Podcast，過目不忘"),
        ("24 小時不睡覺特助", "零幻覺私密智囊，每一句生意解法皆有憑有據"),
        ("Meta 自動發文與秒回", "FB 粉專 / Threads API 官方排程，夜間零焦慮"),
        ("做完專屬成果才准走", "100% 純實體 10 席，導師現場巡桌排錯到底")
    ]
    ry = grid_y + 75
    for tag, desc in right_items:
        draw.rectangle([right_x + 20, ry, right_x + 26, ry + 46], fill=gold_highlight) # 金色標記
        draw.text((right_x + 40, ry + 2), tag, fill=gold_highlight, font=get_font(18, bold=True))
        draw.text((right_x + 40, ry + 26), desc, fill=(225, 235, 250), font=get_font(14, bold=False))
        ry += 68

    # 三週課程總覽橫幅 (Curriculum Bar)
    bar_y = grid_y + card_h + 20
    bar_w = 1010
    bar_h = 70
    bx = (W - bar_w) // 2
    draw.rectangle([bx, bar_y, bx + bar_w, bar_y + bar_h], fill=(22, 32, 48), outline=border_blue, width=1)
    
    # 三週課表內容橫向排版 (完全移除 ✕ 與特殊符號，改用標準 CJK · 與 ｜)
    c1 = "11/11 第 1 講: NotebookLM 數位大腦 (僅剩 5 席)"
    c2 = "11/18 第 2 講: Antigravity · 自動發文串接"
    c3 = "11/25 第 3 講: 資料架構 · 數位店長分身"
    draw.text((bx + 30, bar_y + 15), "【秋季實戰完整三週】", fill=(130, 165, 210), font=get_font(15, bold=True))
    draw.text((bx + 200, bar_y + 15), c1, fill=gold_highlight, font=get_font(15, bold=True))
    draw.text((bx + 200, bar_y + 40), f"{c2}  ｜  {c3}", fill=(185, 205, 230), font=get_font(14, bold=False))

    # 底部實體資訊與老學員免單特權
    foot_y = bar_y + bar_h + 25
    draw.line([(W // 2 - 180, foot_y), (W // 2 + 180, foot_y)], fill=accent_blue, width=2)
    
    draw.text((W // 2, foot_y + 24), "每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(215, 230, 250), font=get_font(20, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 54), "老學員 0 元免單回娘家 ｜ 新朋友單堂 $500 · 審查通過寄發 Email 正取繳費信", fill=(160, 190, 225), font=get_font(16, bold=False), anchor="mm")

    fb_path_1 = os.path.join(OUT_DIR_FB, "FB_05_Latte_vs_AI_Balance.png")
    fb_path_2 = os.path.join(BRAIN_DIR, "FB_05_Latte_vs_AI_Balance.png")
    img.save(fb_path_1, quality=95)
    img.save(fb_path_2, quality=95)
    print(f"✅ FB-05 海報生成完畢: {fb_path_1}")

# ==========================================
# 2. TH-05: 脆 (Threads) 手寫便簽與咖啡對照圖 (1080x1350 4:5)
# ==========================================
def render_th_05():
    W, H = 1080, 1350
    # 溫暖牛皮紙與深咖啡調複合背景 (#1a1816)
    bg_color = (24, 22, 20)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 50
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(65, 58, 50), width=2)
    
    # 頂部小字
    draw.text((W // 2, margin + 40), "台東生活日常隨筆 ｜ 咖啡發票與數位特助", fill=(160, 145, 130), font=get_font(18, bold=False), anchor="mm")
    
    # 大字痛點反問
    draw.text((W // 2, margin + 110), "500 塊在台東能幹嘛？", fill=(245, 235, 220), font=get_font(48, bold=True), anchor="mm")
    draw.text((W // 2, margin + 175), "兩杯燕麥奶拿鐵，喝完就沒了。", fill=(200, 150, 90), font=get_font(34, bold=True), anchor="mm")
    
    # 中央便簽大卡片 (牛皮紙感 #2c2722)
    note_y = margin + 240
    note_w = 880
    note_h = 600
    nx = (W - note_w) // 2
    draw.rectangle([nx, note_y, nx + note_w, note_y + note_h], fill=(38, 34, 30), outline=(120, 100, 75), width=2)
    
    # 便簽頂部膠帶視覺
    tape_w, tape_h = 160, 36
    draw.rectangle([(W - tape_w) // 2, note_y - 18, (W + tape_w) // 2, note_y + 18], fill=(85, 75, 60))
    
    draw.text((W // 2, note_y + 55), "【 算一算這筆帳 】", fill=(235, 185, 110), font=get_font(26, bold=True), anchor="mm")
    
    points = [
        ("• 兩杯連鎖咖啡 $520", "買到的是：15 分鐘的微苦，跟依然堆成山的雜事。"),
        ("• 台東實戰大師班 $500", "帶走的是：一台 24 小時不睡覺、零幻覺的專屬數位大腦。"),
        ("• 完整連貫三週課", "11/11 數位智庫 ｜ 11/18 自動發文 ｜ 11/25 數位店長。"),
        ("• 老朋友專屬特權", "只要曾是生活管家的學員或老夥伴，學費 0 元全免單！"),
        ("• 嚴格限額 10 席", "多一張椅子都不加，現場巡桌排錯，做完才准下課。")
    ]
    py = note_y + 110
    for title, desc in points:
        draw.text((nx + 50, py), title, fill=(255, 245, 230), font=get_font(22, bold=True))
        draw.text((nx + 50, py + 34), desc, fill=(185, 170, 155), font=get_font(18, bold=False))
        py += 95
        
    # 緊急席次倒數條 (無 Emoji，純標準 CJK)
    draw.rectangle([nx + 30, note_y + note_h - 75, nx + note_w - 30, note_y + note_h - 20], fill=(60, 25, 20), outline=(220, 70, 50), width=1)
    draw.text((W // 2, note_y + note_h - 48), "【 倒數 】 第 1 講目前僅剩最後 5 席！額滿立即關門！", fill=(255, 200, 190), font=get_font(20, bold=True), anchor="mm")

    # 底部實體資訊
    foot_y = note_y + note_h + 50
    draw.text((W // 2, foot_y), "每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(225, 215, 200), font=get_font(22, bold=True), anchor="mm")
    draw.text((W // 2, foot_y + 40), "實體入席申請表已放【第一則留言】，週三見。", fill=(160, 145, 130), font=get_font(18, bold=False), anchor="mm")

    th_path_1 = os.path.join(OUT_DIR_TH, "TH_05_Latte_Receipt_Sticky_Note.jpg")
    th_path_2 = os.path.join(BRAIN_DIR, "TH_05_Latte_Receipt_Sticky_Note.jpg")
    img.save(th_path_1, quality=95)
    img.save(th_path_2, quality=95)
    print(f"✅ TH-05 配圖生成完畢: {th_path_1}")

if __name__ == "__main__":
    render_fb_05()
    render_th_05()
