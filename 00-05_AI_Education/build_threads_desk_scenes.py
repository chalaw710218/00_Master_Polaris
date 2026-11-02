import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

p_badge = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_Badge_1111_Class.jpg"
p_badge_ai = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_Badge_AI_Delivery.jpg"
out_dir = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"
out_dir_th = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts"

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"

def get_font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)

def render_desk_scene(badge_path, note_lines, out_filename):
    W, H = 1080, 1350 # 4:5 Threads 比例
    
    # 建立溫暖木質工作桌底色 (#E8DFD1 到 #DFCFC0 微微漸層與木質暗角)
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    y_idx, x_idx = np.indices((H, W))
    
    # 微漸層與噪點感，模擬真實實木桌
    base_r = 236 - (y_idx / H * 18) - (x_idx / W * 10)
    base_g = 226 - (y_idx / H * 20) - (x_idx / W * 12)
    base_b = 212 - (y_idx / H * 22) - (x_idx / W * 14)
    
    arr[:, :, 0] = np.clip(base_r, 200, 245)
    arr[:, :, 1] = np.clip(base_g, 190, 235)
    arr[:, :, 2] = np.clip(base_b, 175, 220)
    
    desk_img = Image.fromarray(arr).convert("RGBA")
    
    # 讀取修改後的胸章
    badge = Image.open(badge_path).convert("RGBA")
    bw, bh = badge.size
    
    # 裁切圓形並加上真實陰影
    cx, cy = bw // 2, bh // 2
    r = int(min(bw, bh) * 0.485)
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    
    badge_circle = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    badge_circle.paste(badge, (0, 0), mask=mask)
    badge_cropped = badge_circle.crop([cx - r, cy - r, cx + r, cy + r])
    
    # 縮放到約 680px 直徑
    target_d = 660
    badge_resized = badge_cropped.resize((target_d, target_d), Image.Resampling.LANCZOS)
    
    # 微旋轉 -3 度（模擬隨手擺放）
    badge_rot = badge_resized.rotate(-3, resample=Image.Resampling.BICUBIC, expand=True)
    
    # 陰影
    pad = 40
    sh_layer = Image.new("RGBA", (badge_rot.width + pad * 2, badge_rot.height + pad * 2), (0, 0, 0, 0))
    alpha = badge_rot.split()[3].filter(ImageFilter.GaussianBlur(16))
    sh_patch = Image.new("RGBA", badge_rot.size, (20, 15, 10, 85))
    sh_layer.paste(sh_patch, (pad + 4, pad + 14), mask=alpha)
    sh_layer.paste(badge_rot, (pad, pad), mask=badge_rot)
    
    # 貼在木桌上半偏中位置
    pos_x = (W - badge_rot.width) // 2
    pos_y = 110
    desk_img.paste(sh_layer, (pos_x - pad, pos_y - pad), mask=sh_layer)
    
    # 在右下偏中位置貼一張黃色便簽 (Post-it note)
    note_w, note_h = 620, 340
    note = Image.new("RGBA", (note_w, note_h), (255, 245, 157, 255)) # 溫暖便籤黃
    note_draw = ImageDraw.Draw(note)
    
    # 便簽頂部微深黃色黏膠條
    note_draw.rectangle([0, 0, note_w, 28], fill=(245, 230, 130, 255))
    
    # 便簽手寫筆記感
    ny = 50
    for idx, line in enumerate(note_lines):
        is_red = ("10" in line or "買回來" in line or "走" in line)
        col = (193, 18, 31, 255) if is_red else (40, 36, 30, 255)
        f = get_font(30 if idx == 0 else (36 if is_red else 26), bold=True)
        note_draw.text((35, ny), line, fill=col, font=f)
        ny += 48
        
    # 便簽旋轉 2 度
    note_rot = note.rotate(2, resample=Image.Resampling.BICUBIC, expand=True)
    
    # 便簽柔和陰影
    n_pad = 30
    n_sh = Image.new("RGBA", (note_rot.width + n_pad * 2, note_rot.height + n_pad * 2), (0, 0, 0, 0))
    n_alpha = note_rot.split()[3].filter(ImageFilter.GaussianBlur(10))
    n_patch = Image.new("RGBA", note_rot.size, (20, 15, 10, 50))
    n_sh.paste(n_patch, (n_pad + 2, n_pad + 8), mask=n_alpha)
    n_sh.paste(note_rot, (n_pad, n_pad), mask=note_rot)
    
    # 貼上便簽
    note_pos_x = (W - note_rot.width) // 2
    note_pos_y = pos_y + target_d + 55
    desk_img.paste(n_sh, (note_pos_x - n_pad, note_pos_y - n_pad), mask=n_sh)
    
    # 存檔
    out_brain = os.path.join(out_dir, out_filename)
    desk_img.convert("RGB").save(out_brain, quality=95)
    desk_img.convert("RGB").save(os.path.join(out_dir_th, out_filename), quality=95)
    print("Desk scene rendered:", out_brain)
    return out_brain

if __name__ == "__main__":
    lines1 = [
        "📌 11/11 (三) 14:00 首講",
        "📍 正氣北路166巷90號（家宅）",
        "⚠️ 純實體限額 10 席，多一張都不加",
        "把時間買回來，做完才准下課！☕"
    ]
    render_desk_scene(p_badge, lines1, "TH_Desk_Scene_Class.jpg")
    
    lines2 = [
        "🛵 雜事交給 AI 跑腿，時間還給家人",
        "📍 11/11 (週三) 下午 14:00 @ 家宅",
        "⚠️ 只有 10 張椅子！",
        "—— 留言區放表單，來喝杯熱茶吧"
    ]
    render_desk_scene(p_badge_ai, lines2, "TH_Desk_Scene_AI_Delivery.jpg")
