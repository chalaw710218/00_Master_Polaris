# -*- coding: utf-8 -*-
"""
Create Post 01 Minimalist, Vivid, High-Impact Poster
Background: AI-generated warm artisanal tea & golden light scene
Typography: Microsoft JhengHei Bold, strictly no unsupported glyphs
Target Size: 1080 x 1350 (4:5)
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

bg_source = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\poster_01_bg_v2_1795416566367.jpg"
out_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering\images"
out_file = os.path.join(out_dir, "POST_01_Countdown_48H_Poster.png")
desktop_file = r"C:\Users\lenovo\Desktop\POST_01_倒數48小時海報.png"

# Target Canvas Size
W, H = 1080, 1350

# 1. Load and Crop/Fit Background to 1080x1350
img_bg = Image.open(bg_source).convert("RGBA")
bg_w, bg_h = img_bg.size

# Scale to cover W, H
scale = max(W / bg_w, H / bg_h)
new_w, new_h = int(bg_w * scale), int(bg_h * scale)
img_bg = img_bg.resize((new_w, new_h), Image.Resampling.LANCZOS)

# Center crop
left = (new_w - W) // 2
top = (new_h - H) // 2
img_bg = img_bg.crop((left, top, left + W, top + H))

# 2. Add Top & Bottom Dark Gradient Overlay for perfect typography contrast
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_ov = ImageDraw.Draw(overlay)

# Top gradient: 0 to 450px
for y in range(450):
    alpha = int(220 * (1 - (y / 450) ** 1.3))
    draw_ov.line([(0, y), (W, y)], fill=(13, 17, 23, alpha))

# Bottom gradient: 800 to 1350px
for y in range(800, H):
    alpha = int(235 * (((y - 800) / (H - 800)) ** 1.2))
    draw_ov.line([(0, y), (W, y)], fill=(13, 17, 23, alpha))

# Center slight darkening (25% opacity) to keep background warm but not distracting
draw_ov.rectangle([0, 0, W, H], fill=(13, 17, 23, 40))

# Composite background and gradient
canvas = Image.alpha_composite(img_bg, overlay)
draw = ImageDraw.Draw(canvas)

# Fonts
font_path = "C:/Windows/Fonts/msjhbd.ttc"
font_tag = ImageFont.truetype(font_path, 28)
font_title = ImageFont.truetype(font_path, 88)
font_sub = ImageFont.truetype(font_path, 42)
font_highlight = ImageFont.truetype(font_path, 32)
font_footer = ImageFont.truetype(font_path, 28)

# Colors
C_AMBER = (251, 191, 36, 255)       # #FBBF24
C_AMBER_DEEP = (245, 158, 11, 255)  # #F59E0B
C_CORAL = (251, 113, 133, 255)     # #FB7185
C_WHITE = (248, 250, 252, 255)     # #F8FAFC
C_MUTED = (203, 213, 225, 255)     # #CBD5E1

# ================= 頂部：品牌與講次標籤 =================
tag_text = "生活管家 · 2026 秋季實戰家教班"
tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
tag_w = tag_bbox[2] - tag_bbox[0]
tag_h = tag_bbox[3] - tag_bbox[1]
tag_x = (W - tag_w) // 2
tag_y = 75

# Draw tag background capsule
pad_x, pad_y = 22, 10
draw.rounded_rectangle(
    [tag_x - pad_x, tag_y - pad_y, tag_x + tag_w + pad_x, tag_y + tag_h + pad_y + 2],
    radius=20,
    fill=(22, 27, 34, 210),
    outline=(245, 158, 11, 230),
    width=2
)
draw.text((tag_x, tag_y), tag_text, font=font_tag, fill=C_AMBER)

# ================= 主標題：倒數 48 小時 =================
title_text = "倒數 48 小時"
t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
t_w = t_bbox[2] - t_bbox[0]
t_x = (W - t_w) // 2
t_y = 150

# Subtle drop shadow for 3D punch
draw.text((t_x + 3, t_y + 4), title_text, font=font_title, fill=(0, 0, 0, 180))
draw.text((t_x, t_y), title_text, font=font_title, fill=C_WHITE)

# ================= 副標題：把老闆的靈魂，捏進 AI 裡 =================
sub_text = "把老闆的靈魂，捏進 AI 裡"
s_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
s_w = s_bbox[2] - s_bbox[0]
s_x = (W - s_w) // 2
s_y = 275

draw.text((s_x + 2, s_y + 2), sub_text, font=font_sub, fill=(0, 0, 0, 180))
draw.text((s_x, s_y), sub_text, font=font_sub, fill=C_AMBER)

# ================= 底部卡片：核心亮點 =================
hl_text = "【 告別冷血公文腔 · 打造專屬數位店長 】"
hl_bbox = draw.textbbox((0, 0), hl_text, font=font_highlight)
hl_w = hl_bbox[2] - hl_bbox[0]
hl_h = hl_bbox[3] - hl_bbox[1]
hl_x = (W - hl_w) // 2
hl_y = 1130

# Translucent dark card behind highlight
hl_pad_x, hl_pad_y = 26, 14
draw.rounded_rectangle(
    [hl_x - hl_pad_x, hl_y - hl_pad_y, hl_x + hl_w + hl_pad_x, hl_y + hl_h + hl_pad_y + 2],
    radius=12,
    fill=(10, 14, 23, 220),
    outline=(244, 63, 94, 200),
    width=2
)
draw.text((hl_x, hl_y), hl_text, font=font_highlight, fill=C_CORAL)

# ================= 底部資訊列：時間、地點、席位 =================
footer_text = "11/25 (三) 14:00 台東家宅總部 ｜ 純實體教學 · 嚴格限額 6 席"
f_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
f_w = f_bbox[2] - f_bbox[0]
f_x = (W - f_w) // 2
f_y = 1240

# Background line/bar
draw.rectangle([60, f_y - 20, W - 60, f_y - 18], fill=(245, 158, 11, 120))
draw.text((f_x, f_y), footer_text, font=font_footer, fill=C_MUTED)

# Save output
canvas_rgb = canvas.convert("RGB")
canvas_rgb.save(out_file, "PNG", quality=95)
shutil.copyfile(out_file, desktop_file)

print(f"Post 01 Poster successfully created:")
print(f"1. Workspace: {out_file}")
print(f"2. Desktop: {desktop_file}")
