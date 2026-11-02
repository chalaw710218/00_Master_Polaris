import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR_FB = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts"
OUT_DIR_TH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts"
BRAIN_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"

STICKER_CLEAN = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\.user_uploaded\media_1793580557231_87c68fc1.jpg"
BADGE_PHOTO = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\.user_uploaded\media_1793580563107_e5369969.jpg"

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

def add_drop_shadow(img_rgba, offset=(0, 12), blur=18, shadow_color=(20, 20, 20, 80)):
    w, h = img_rgba.size
    pad = blur * 2 + max(abs(offset[0]), abs(offset[1]))
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    
    alpha = img_rgba.split()[3]
    shadow_mask = alpha.filter(ImageFilter.GaussianBlur(blur))
    shadow_patch = Image.new("RGBA", (w, h), shadow_color)
    shadow_pos = (pad + offset[0], pad + offset[1])
    canvas.paste(shadow_patch, shadow_pos, mask=shadow_mask)
    canvas.paste(img_rgba, (pad, pad), mask=img_rgba)
    return canvas, pad

def render_facebook_minimal():
    """Facebook 極致減法版 (1200x1200, 1:1)"""
    W, H = 1200, 1200
    # 溫潤暖奶油紙質 (#FAF6ED)
    bg_color = (250, 246, 237)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 70
    
    # 優雅極細外框 (雙細線，保留 40% 空間感)
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(220, 212, 196), width=2)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(40, 36, 32), width=1)
    
    # 頂部簡約小字 (呼吸感)
    top_y = margin + 35
    font_top = get_font(18, bold=True)
    draw.text((W // 2, top_y), "生活管家 · 家宅 ✕ 寶桑原點", fill=(120, 110, 100), font=font_top, anchor="mm")
    
    # 中央英雄圖騰：狂飆抱魚貓咪徽章 (直徑 480px)
    badge_size = 480
    badge = get_circular_badge(badge_size)
    badge_shadow, pad = add_drop_shadow(badge, offset=(0, 14), blur=16, shadow_color=(30, 25, 20, 75))
    
    badge_x = (W - badge_size) // 2
    badge_y = top_y + 40
    img.paste(badge_shadow, (badge_x - pad, badge_y - pad), mask=badge_shadow)
    
    # 徽章下方：心靈刺刀大標題 (Level 1)
    title_y = badge_y + badge_size + 50
    font_h1 = get_font(56, bold=True)
    draw.text((W // 2, title_y), "把時間買回來，", fill=(30, 28, 25), font=font_h1, anchor="mm")
    draw.text((W // 2, title_y + 70), "多陪陪家人。", fill=(193, 18, 31), font=font_h1, anchor="mm") # 暖紅點題
    
    # 裝飾細線
    div_y = title_y + 125
    draw.line([(W // 2 - 120, div_y), (W // 2 + 120, div_y)], fill=(245, 183, 56), width=3)
    
    # 底部唯一座標與行動指引 (Level 2 & 3)
    foot_y = div_y + 35
    font_venue = get_font(21, bold=True)
    draw.text((W // 2, foot_y), "11/11 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）", fill=(50, 45, 40), font=font_venue, anchor="mm")
    
    font_sub = get_font(18, bold=False)
    draw.text((W // 2, foot_y + 38), "100% 純實體現場實戰 ✕ 限額 10 席 ✕ 沒做完專屬成果不准下課", fill=(100, 90, 80), font=font_sub, anchor="mm")
    
    font_cta = get_font(18, bold=True)
    draw.text((W // 2, foot_y + 75), "💬 老學員 0 元免單 ＆ 正取申請，請見【第一則留言】", fill=(193, 18, 31), font=font_cta, anchor="mm")
    
    out_fb = os.path.join(OUT_DIR_FB, "FB_01_Time_And_Family_Minimal.png")
    img.save(out_fb, quality=95)
    print("FB Minimal rendered:", out_fb)
    img.save(os.path.join(BRAIN_DIR, "FB_01_Time_And_Family_Minimal.png"))
    return out_fb

def copy_threads_authentic_badge():
    """Threads 直接使用闆仔真實翻拍的胸章照片 (零代碼修飾，純粹真實)"""
    raw_badge = Image.open(BADGE_PHOTO)
    out_th = os.path.join(OUT_DIR_TH, "TH_01_Origin_Badge_Real.jpg")
    raw_badge.save(out_th, quality=95)
    print("Threads Authentic Badge saved:", out_th)
    raw_badge.save(os.path.join(BRAIN_DIR, "TH_01_Origin_Badge_Real.jpg"))
    return out_th

if __name__ == "__main__":
    os.makedirs(OUT_DIR_FB, exist_ok=True)
    os.makedirs(OUT_DIR_TH, exist_ok=True)
    os.makedirs(BRAIN_DIR, exist_ok=True)
    
    render_facebook_minimal()
    copy_threads_authentic_badge()
    print("Done!")
