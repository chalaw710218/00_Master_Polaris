import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

p_photo = r"C:/Users/lenovo/.gemini/antigravity/brain/fab99572-f34f-40f2-ab07-c039187414cc/.user_uploaded/media_1793580563107_e5369969.jpg"
p_clean = r"C:/Users/lenovo/.gemini/antigravity/brain/fab99572-f34f-40f2-ab07-c039187414cc/.user_uploaded/media_1793580557231_87c68fc1.jpg"

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
def get_font(size):
    return ImageFont.truetype(FONT_BOLD, size)

def create_modified_badge(source_path, top_text, btm_text, out_path, is_photo=True):
    img = Image.open(source_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Text area bounding box in source (approx y: 568 to 925)
    # Let's paint over the text with the exact cream color/gradient
    # In the photo, y=568 is the black dividing line.
    # We want to fill the region between the outer black border and the top dividing line.
    
    # Create mask for the cream text area
    # The inner border is a circle centered at approx (512, 510) with radius ~450
    cx, cy = 512, 510
    radius = 442 if is_photo else 446
    
    # We only want to repaint where y > 567 and distance from center < radius
    arr = np.array(img)
    y_indices, x_indices = np.indices((h, w))
    dist_sq = (x_indices - cx)**2 + (y_indices - cy)**2
    
    # Region to repaint: below the horizontal dividing line (y >= 570) and inside the circular black border
    mask_region = (y_indices >= 568) & (dist_sq < (radius - 5)**2)
    
    # Calculate lighting gradient for cream
    if is_photo:
        # Subtle lighting: top-left slightly brighter, bottom slightly darker
        # y from 568 to 930
        grad_y = (y_indices - 568) / (930 - 568)
        grad_x = (x_indices - 200) / 600.0
        
        # Base cream approx (240, 233, 212) at top to (232, 222, 200) at bottom
        r_chan = np.clip(242 - grad_y * 10 - grad_x * 4, 220, 245).astype(np.uint8)
        g_chan = np.clip(235 - grad_y * 12 - grad_x * 4, 215, 240).astype(np.uint8)
        b_chan = np.clip(215 - grad_y * 14 - grad_x * 4, 195, 220).astype(np.uint8)
        
        arr[mask_region, 0] = r_chan[mask_region]
        arr[mask_region, 1] = g_chan[mask_region]
        arr[mask_region, 2] = b_chan[mask_region]
        arr[mask_region, 3] = 255
    else:
        # Flat clean sticker: solid cream (255, 253, 242)
        arr[mask_region, 0] = 255
        arr[mask_region, 1] = 253
        arr[mask_region, 2] = 242
        arr[mask_region, 3] = 255
        
    cleaned_img = Image.fromarray(arr)
    draw_clean = ImageDraw.Draw(cleaned_img)
    
    # Ink color matching the original black ink
    ink_color = (26, 27, 22, 255) if is_photo else (30, 30, 30, 255)
    
    # Draw new texts
    # Line 1: top_text (large bold, e.g. "創始夥伴" or "把時間買回來")
    # Line 2: btm_text (medium bold, e.g. "11/11 家宅開課中")
    
    font_top = get_font(132 if len(top_text) <= 4 else 105)
    font_btm = get_font(68 if len(btm_text) <= 8 else 60)
    
    # Y-positions: Line 1 center at approx y=685, Line 2 center at approx y=825
    y1 = 680
    y2 = 825
    
    draw_clean.text((cx, y1), top_text, fill=ink_color, font=font_top, anchor="mm")
    draw_clean.text((cx, y2), btm_text, fill=ink_color, font=font_btm, anchor="mm")
    
    cleaned_img.convert("RGB").save(out_path, quality=95)
    print("Saved:", out_path)
    return out_path

if __name__ == "__main__":
    out_dir = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc"
    
    # Option 1: 創始夥伴 ✕ 11/11 家宅開課中
    create_modified_badge(p_photo, "創始夥伴", "11/11 家宅開課中", os.path.join(out_dir, "TH_Badge_1111_Class.jpg"), is_photo=True)
    
    # Option 2: 創始夥伴 ✕ 雜事ＡＩ代送中
    create_modified_badge(p_photo, "創始夥伴", "雜事ＡＩ代送中", os.path.join(out_dir, "TH_Badge_AI_Delivery.jpg"), is_photo=True)
    
    # Option 3: 把時間買回來 ✕ 11/11 家宅開課中
    create_modified_badge(p_photo, "把時間買回來", "11/11 家宅開課中", os.path.join(out_dir, "TH_Badge_Time_Home.jpg"), is_photo=True)
