# -*- coding: utf-8 -*-
"""
Generate Posters for Post 02, Post 03, and Post 04
All 4:5 (1080x1350), unique background photos, clean typography, zero tofu boxes
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

font_path = "C:/Windows/Fonts/msjhbd.ttc"
font_tag = ImageFont.truetype(font_path, 28)
font_title = ImageFont.truetype(font_path, 84)
font_title_small = ImageFont.truetype(font_path, 72)
font_sub = ImageFont.truetype(font_path, 40)
font_highlight = ImageFont.truetype(font_path, 32)
font_footer = ImageFont.truetype(font_path, 28)

C_AMBER = (251, 191, 36, 255)
C_CORAL = (251, 113, 133, 255)
C_WHITE = (248, 250, 252, 255)
C_MUTED = (203, 213, 225, 255)

W, H = 1080, 1350
out_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering\images"

def create_poster(bg_path, out_name, desktop_name, title_text, sub_text, hl_text, footer_text, hl_color=C_CORAL, use_small_title=False):
    img_bg = Image.open(bg_path).convert("RGBA")
    bg_w, bg_h = img_bg.size
    scale = max(W / bg_w, H / bg_h)
    new_w, new_h = int(bg_w * scale), int(bg_h * scale)
    img_bg = img_bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    img_bg = img_bg.crop((left, top, left + W, top + H))
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Top gradient
    for y in range(450):
        alpha = int(225 * (1 - (y / 450) ** 1.3))
        draw_ov.line([(0, y), (W, y)], fill=(13, 17, 23, alpha))
        
    # Bottom gradient
    for y in range(800, H):
        alpha = int(240 * (((y - 800) / (H - 800)) ** 1.2))
        draw_ov.line([(0, y), (W, y)], fill=(13, 17, 23, alpha))
        
    draw_ov.rectangle([0, 0, W, H], fill=(13, 17, 23, 45))
    
    canvas = Image.alpha_composite(img_bg, overlay)
    draw = ImageDraw.Draw(canvas)
    
    # Tag
    tag_text = "生活管家 · 2026 秋季實戰家教班"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_h = tag_bbox[3] - tag_bbox[1]
    tag_x = (W - tag_w) // 2
    tag_y = 75
    draw.rounded_rectangle(
        [tag_x - 22, tag_y - 10, tag_x + tag_w + 22, tag_y + tag_h + 12],
        radius=20, fill=(22, 27, 34, 215), outline=(245, 158, 11, 230), width=2
    )
    draw.text((tag_x, tag_y), tag_text, font=font_tag, fill=C_AMBER)
    
    # Title
    t_font = font_title_small if use_small_title else font_title
    t_bbox = draw.textbbox((0, 0), title_text, font=t_font)
    t_w = t_bbox[2] - t_bbox[0]
    t_x = (W - t_w) // 2
    t_y = 155
    draw.text((t_x + 3, t_y + 4), title_text, font=t_font, fill=(0, 0, 0, 200))
    draw.text((t_x, t_y), title_text, font=t_font, fill=C_WHITE)
    
    # Subtitle
    s_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    s_w = s_bbox[2] - s_bbox[0]
    s_x = (W - s_w) // 2
    s_y = 265
    draw.text((s_x + 2, s_y + 2), sub_text, font=font_sub, fill=(0, 0, 0, 180))
    draw.text((s_x, s_y), sub_text, font=font_sub, fill=C_AMBER)
    
    # Highlight Box
    hl_bbox = draw.textbbox((0, 0), hl_text, font=font_highlight)
    hl_w = hl_bbox[2] - hl_bbox[0]
    hl_h = hl_bbox[3] - hl_bbox[1]
    hl_x = (W - hl_w) // 2
    hl_y = 1130
    draw.rounded_rectangle(
        [hl_x - 26, hl_y - 14, hl_x + hl_w + 26, hl_y + hl_h + 16],
        radius=12, fill=(10, 14, 23, 225), outline=hl_color, width=2
    )
    draw.text((hl_x, hl_y), hl_text, font=font_highlight, fill=hl_color)
    
    # Footer
    f_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
    f_w = f_bbox[2] - f_bbox[0]
    f_x = (W - f_w) // 2
    f_y = 1240
    draw.rectangle([60, f_y - 20, W - 60, f_y - 18], fill=(245, 158, 11, 130))
    draw.text((f_x, f_y), footer_text, font=font_footer, fill=C_MUTED)
    
    # Save
    out_p = os.path.join(out_dir, out_name)
    desk_p = os.path.join(r"C:\Users\lenovo\Desktop", desktop_name)
    canvas.convert("RGB").save(out_p, "PNG", quality=95)
    shutil.copyfile(out_p, desk_p)
    print(f"Generated: {desk_p}")

# Post 02
create_poster(
    bg_path=r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\artisanal_wood_carving_poster_bg_v3_1795418512377.jpg",
    out_name="POST_02_Anti_Slop_Chisel_Poster.png",
    desktop_name="POST_02_去塑料三刀法海報.png",
    title_text="去 AI 塑料味三刀法",
    sub_text="開口就像你親自顧店一樣有溫度",
    hl_text="【 砍客套 · 換五感 · 加日常 】",
    footer_text="11/25 (三) 14:00 台東家宅總部 ｜ 純實體教學 · 嚴格限額 6 席",
    hl_color=C_CORAL,
    use_small_title=True
)

# Post 03
create_poster(
    bg_path=r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\taitung_night_townhouse_1795418487404.jpg",
    out_name="POST_03_Final_18H_Night_Poster.png",
    desktop_name="POST_03_倒數18小時海報.png",
    title_text="倒數 18 小時",
    sub_text="最後席位，今晚截止報名",
    hl_text="【 現場巡桌個別調教 · 沒捏出分身不准下課 】",
    footer_text="11/25 (三) 14:00 台東家宅總部 ｜ 嚴格限額 6 席 · 額滿即關",
    hl_color=C_AMBER
)

# Post 04
create_poster(
    bg_path=r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\ai_workshop_morning_poster_bg_v2_1795418510731.jpg",
    out_name="POST_04_See_You_Today_Poster.png",
    desktop_name="POST_04_今天下午見海報.png",
    title_text="今天下午 14:00 見！",
    sub_text="為你的店，注入專屬 AI 靈魂",
    hl_text="【 正氣北路家宅總部 · 熱茶已備妥，筆電請充飽 】",
    footer_text="純實體教學 ｜ 現場實機對話驗收合格 ｜ 不見不散",
    hl_color=C_CORAL,
    use_small_title=True
)
