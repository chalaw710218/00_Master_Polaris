# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def render_postcard(base_path, out_path, stamp_bg, dear_text, quote_text, body1, body2, date_str):
    if not os.path.exists(base_path):
        print(f"❌ 找不到底圖: {base_path}")
        return False
        
    raw_img = Image.open(base_path)
    canvas_w, canvas_h = 1080, 1440
    canvas = Image.new('RGB', (canvas_w, canvas_h), (250, 248, 242))
    draw = ImageDraw.Draw(canvas)

    margin_lr = 50
    margin_top = 50
    photo_w = canvas_w - (margin_lr * 2)
    photo_h = 920

    base_w, base_h = raw_img.size
    scale = max(photo_w / base_w, photo_h / base_h)
    new_w, new_h = int(base_w * scale), int(base_h * scale)
    resized = raw_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left, top = (new_w - photo_w) // 2, (new_h - photo_h) // 2
    cropped = resized.crop((left, top, left + photo_w, top + photo_h))

    canvas.paste(cropped, (margin_lr, margin_top))
    draw.rectangle([margin_lr, margin_top, margin_lr + photo_w, margin_top + photo_h], outline=(210, 200, 185), width=2)

    # Stamp
    stamp_w, stamp_h = 130, 160
    stamp_x = margin_lr + photo_w - stamp_w - 30
    stamp_y = margin_top + 30
    draw.rectangle([stamp_x - 4, stamp_y - 4, stamp_x + stamp_w + 4, stamp_y + stamp_h + 4], fill=(255, 255, 255), outline=(220, 215, 205), width=1)
    draw.rectangle([stamp_x, stamp_y, stamp_x + stamp_w, stamp_y + stamp_h], fill=stamp_bg)

    font_arial = r'C:\Windows\Fonts\arial.ttf'
    font_bold = r'C:\Windows\Fonts\msjhbd.ttc'
    font_norm = r'C:\Windows\Fonts\msjh.ttc'

    f_stamp_title = ImageFont.truetype(font_bold, 15, index=0)
    f_stamp_eng = ImageFont.truetype(font_arial, 11)
    f_stamp_price = ImageFont.truetype(font_arial, 16)

    draw.text((stamp_x + 16, stamp_y + 15), '都蘭共學', font=f_stamp_title, fill=(255, 255, 255))
    draw.text((stamp_x + 28, stamp_y + 40), 'TAITUNG', font=f_stamp_eng, fill=(240, 240, 240))
    draw.line([(stamp_x + 15, stamp_y + 65), (stamp_x + stamp_w - 15, stamp_y + 65)], fill=(150, 170, 180), width=1)
    draw.text((stamp_x + 36, stamp_y + 85), '慢活', font=f_stamp_title, fill=(255, 255, 255))
    draw.text((stamp_x + 25, stamp_y + 120), 'NT$ 3000', font=f_stamp_price, fill=(255, 235, 150))

    # Postmark
    pm_cx = stamp_x - 10
    pm_cy = stamp_y + 80
    postmark_img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    pm_draw = ImageDraw.Draw(postmark_img)
    pm_draw.ellipse([pm_cx - 55, pm_cy - 55, pm_cx + 55, pm_cy + 55], outline=(50, 50, 50, 210), width=2)
    pm_draw.ellipse([pm_cx - 47, pm_cy - 47, pm_cx + 47, pm_cy + 47], outline=(50, 50, 50, 160), width=1)
    f_pm_text = ImageFont.truetype(font_arial, 11)
    f_pm_date = ImageFont.truetype(font_arial, 12)
    f_pm_cn = ImageFont.truetype(font_bold, 12, index=0)
    pm_draw.text((pm_cx - 38, pm_cy - 30), 'TAITUNG DULAN', font=f_pm_text, fill=(50, 50, 50, 220))
    pm_draw.text((pm_cx - 30, pm_cy - 8), date_str, font=f_pm_date, fill=(50, 50, 50, 220))
    pm_draw.text((pm_cx - 26, pm_cy + 15), '共學堂', font=f_pm_cn, fill=(50, 50, 50, 200))
    for dy in [-15, 0, 15]:
        pm_draw.line([(pm_cx - 150, pm_cy + dy), (pm_cx - 65, pm_cy + dy)], fill=(50, 50, 50, 180), width=2)

    canvas = Image.alpha_composite(canvas.convert('RGBA'), postmark_img).convert('RGB')
    draw = ImageDraw.Draw(canvas)

    f_greeting = ImageFont.truetype(font_bold, 24, index=0)
    f_quote = ImageFont.truetype(font_bold, 28, index=0)
    f_body = ImageFont.truetype(font_norm, 20, index=0)
    f_footer = ImageFont.truetype(font_norm, 17, index=0)
    f_info = ImageFont.truetype(font_bold, 18, index=0)
    f_cta = ImageFont.truetype(font_bold, 18, index=0)

    text_x = margin_lr + 20
    draw.text((text_x, 1005), dear_text, font=f_greeting, fill=(60, 50, 40))
    draw.text((text_x, 1055), quote_text, font=f_quote, fill=(180, 55, 40))
    draw.text((text_x, 1115), body1, font=f_body, fill=(70, 70, 70))
    draw.text((text_x, 1150), body2, font=f_body, fill=(70, 70, 70))
    draw.line([(text_x, 1205), (canvas_w - margin_lr - 20, 1205)], fill=(225, 215, 200), width=1)
    draw.text((text_x, 1225), '― 寄自：都蘭共學堂  x  生活管家（台東市正氣路教室  x  都蘭四季八里莊園）', font=f_footer, fill=(110, 100, 90))
    draw.text((text_x, 1265), '全期 6 堂共 3,000 元（實體樣書送印自費） ｜ 12/4 正式開課 ‧ 11/28 截止開班統計', font=f_info, fill=(45, 85, 75))
    draw.text((text_x, 1310), '▼  詳細介紹與線上報名表單，請見留言區第一樓  ▼', font=f_cta, fill=(195, 120, 20))

    canvas.save(out_path, quality=95)
    print(f'✅ Rendered successfully: {out_path}')
    return True

if __name__ == '__main__':
    # 執行所有可用的卡片渲染
    postcards = [
        (
            r'02_Visual_Assets\postcard_07_classroom.jpg',
            r'02_Visual_Assets\postcard_07_final.jpg',
            (45, 95, 80), # Taitung tea green
            'Dear 住在台東市區的你：',
            '「住在台東市區的朋友，不用大老遠跑都蘭！」',
            '市區朋友直接在正氣路教室上課，市區免奔波。',
            '助教全程在旁陪伴，從手機語音到完成專屬電子書稿。',
            '2026.11.26'
        ),
        (
            r'02_Visual_Assets\postcard_08_book_prototype.jpg',
            r'02_Visual_Assets\postcard_08_final.jpg',
            (120, 65, 45), # Craftsman terracotta
            'Dear 想把人生留成一本書的你：',
            '「一堂 500 元的寫作課：雙師資 x 實體助教 x 出書模板」',
            '不是昂貴的商業課，而是在地溫暖共學，全期 6 堂 3,000 元。',
            '江冠明作家心法 ＋ 哈爸實戰工具，把歲月真正捧在手心。',
            '2026.11.26'
        ),
        (
            r'02_Visual_Assets\postcard_09_countdown.jpg',
            r'02_Visual_Assets\postcard_09_final.jpg',
            (140, 85, 35), # Golden amber
            'Dear 心裡一直有故事想寫的你：',
            '「最後倒數 36 小時！只差最後幾位就確定開班」',
            '明天 11/28 截止人數統計，滿 12 人即開班，不足額則順延。',
            '市區正氣路與都蘭現場助教都已準備好，放膽給自己一次嘗試！',
            '2026.11.27'
        ),
        (
            r'02_Visual_Assets\postcard_10_twilight.jpg',
            r'02_Visual_Assets\postcard_10_final.jpg',
            (35, 55, 90), # Pacific twilight blue
            'Dear 給自己這份冬天禮物的你：',
            '「今晚最後倒數壓線：給自己這個冬天，留下一本書」',
            '今晚截止開班人數盤點，給自己每週五晚上一段沉澱的時光。',
            '6 週後捧著專屬書稿，期待下週五在文字與山海中與你相遇！',
            '2026.11.27'
        )
    ]

    for p in postcards:
        render_postcard(*p)
