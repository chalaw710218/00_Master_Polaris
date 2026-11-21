# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

base_img_path = r'02_Visual_Assets\\poster_02_farmer_artisan.jpg'
out_img_path = r'02_Visual_Assets\\poster_02_cinematic_final.jpg'

img = Image.open(base_img_path).convert('RGBA')
w, h = img.size

overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw_ol = ImageDraw.Draw(overlay)

# Top gradient
for y in range(400):
    alpha = int(140 * (1.0 - y / 400.0)**1.3)
    draw_ol.line([(0, y), (w, y)], fill=(15, 20, 25, alpha))

# Bottom gradient
for y in range(h - 300, h):
    ratio = (y - (h - 300)) / 300.0
    alpha = int(180 * (ratio**1.2))
    draw_ol.line([(0, y), (w, y)], fill=(12, 16, 20, alpha))

img = Image.alpha_composite(img, overlay)
draw = ImageDraw.Draw(img)

font_bold = r'C:\\Windows\\Fonts\\msjhbd.ttc'
font_norm = r'C:\\Windows\\Fonts\\msjh.ttc'
font_arial = r'C:\\Windows\\Fonts\\arial.ttf'

f_present = ImageFont.truetype(font_norm, 18, index=0)
f_tagline = ImageFont.truetype(font_norm, 22, index=0)
f_title = ImageFont.truetype(font_bold, 44, index=0)
f_eng = ImageFont.truetype(font_arial, 16)
f_subhook = ImageFont.truetype(font_bold, 20, index=0)

f_credit_bold = ImageFont.truetype(font_bold, 17, index=0)
f_credit_norm = ImageFont.truetype(font_norm, 16, index=0)
f_credit_small = ImageFont.truetype(font_norm, 15, index=0)

def draw_centered_text(y, text, font, fill=(255, 255, 255, 240), shadow=True):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    x = (w - tw) // 2
    if shadow:
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=fill)

# Top Presenter & Tagline
draw_centered_text(60, '都 蘭 共 學 堂   x   生 活 管 家   聯 合 呈 獻', f_present, fill=(230, 235, 240, 220))
draw_centered_text(105, '「 幾 十 年 的 土 地 汗 水 ， 是 這 座 島 嶼 最 動 人 的 故 事 」', f_tagline, fill=(255, 245, 225, 240))

# Main Title & Subtitle
draw_centered_text(160, '《 說 出 你 的 土 地 與 生 活 》', f_title, fill=(255, 255, 255, 255))
draw_centered_text(225, 'S P E A K   Y O U R   S T O R Y   I N T O   A   B O O K', f_eng, fill=(220, 205, 175, 230))
draw_centered_text(265, '不 用 請 寫 手   .   AI 當 助 理   .   6 週 完 成 專 屬 書 稿', f_subhook, fill=(255, 220, 130, 250))

# Bottom Billing Block
draw_centered_text(h - 260, '―  哈爸  x  江冠明 ： 都蘭慢活寫作共創營（第二期）  ―', f_credit_bold, fill=(255, 235, 180, 255))
draw_centered_text(h - 225, '【領銜主演】你的土地與創業心血   |   【口述代筆】AI 隨身秘書', f_credit_norm, fill=(235, 240, 245, 230))
draw_centered_text(h - 195, '【作家心法】江冠明   |   【口述架構】哈爸   |   【實體陪寫】品碩助教  x  阿鐘教練', f_credit_norm, fill=(235, 240, 245, 230))
draw_centered_text(h - 160, '雙實體教室同步：台東市正氣路教室   x   都蘭四季八里自然莊園', f_credit_bold, fill=(255, 255, 255, 240))
draw_centered_text(h - 128, '全期 6 堂共 3,000 元（平均 500/堂） ｜ 12/4 開課 ‧ 11/28 截止開班統計', f_credit_small, fill=(210, 220, 230, 220))
draw_centered_text(h - 90, '▼  報 名 表 單 請 見 留 言 區 第 一 樓  ▼', f_credit_bold, fill=(255, 215, 100, 255))

img.convert('RGB').save(out_img_path, quality=95)
print('Poster 2 generated successfully!')
