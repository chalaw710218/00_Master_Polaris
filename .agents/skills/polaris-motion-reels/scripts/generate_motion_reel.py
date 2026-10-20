#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris Motion Reels Synthesizer (極星微動態短影音自動合成引擎)
技能: polaris-motion-reels
作者: 影 (Shadow)
"""

import sys
import os
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio

# Windows console UTF-8 setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def crop_and_resize_to_canvas(img, target_w, target_h, scale=1.0, pan_x=0.0, pan_y=0.0):
    """Crop and resize image to fit target canvas with dynamic zoom and pan."""
    orig_w, orig_h = img.size
    
    # Calculate aspect ratios
    target_aspect = target_w / target_h
    orig_aspect = orig_w / orig_h
    
    if orig_aspect > target_aspect:
        # Original is wider than canvas
        base_h = orig_h
        base_w = int(orig_h * target_aspect)
    else:
        # Original is taller than canvas
        base_w = orig_w
        base_h = int(orig_w / target_aspect)
        
    # Apply zoom scale
    crop_w = int(base_w / scale)
    crop_h = int(base_h / scale)
    
    # Center with pan offset
    center_x = orig_w / 2.0 + pan_x * (orig_w - crop_w) / 2.0
    center_y = orig_h / 2.0 + pan_y * (orig_h - crop_h) / 2.0
    
    left = max(0, min(orig_w - crop_w, int(center_x - crop_w / 2.0)))
    top = max(0, min(orig_h - crop_h, int(center_y - crop_h / 2.0)))
    right = left + crop_w
    bottom = top + crop_h
    
    cropped = img.crop((left, top, right, bottom))
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

def overlay_subtitles_and_branding(frame_img, text=None, brand_tag="生活管家，就醬點！ @hellotaitung"):
    """Draw stylish minimalist typography overlay on frame."""
    draw = ImageDraw.Draw(frame_img)
    w, h = frame_img.size
    
    # Bottom gradient overlay for readability
    gradient_h = int(h * 0.28)
    gradient = Image.new("RGBA", (w, gradient_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for y in range(gradient_h):
        alpha = int((y / gradient_h) ** 1.5 * 180)
        g_draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))
        
    frame_img.paste(gradient, (0, h - gradient_h), gradient)
    
    # Draw text
    draw = ImageDraw.Draw(frame_img)
    try:
        # Try finding standard system font on Windows
        font_path = "C:/Windows/Fonts/msjhbd.ttc" # Microsoft JhengHei Bold
        if not os.path.exists(font_path):
            font_path = "C:/Windows/Fonts/simhei.ttf"
        font_title = ImageFont.truetype(font_path, int(w * 0.048)) if os.path.exists(font_path) else ImageFont.load_default()
        font_tag = ImageFont.truetype(font_path, int(w * 0.032)) if os.path.exists(font_path) else ImageFont.load_default()
    except Exception:
        font_title = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        
    if text:
        # Wrap or center text
        text_bbox = draw.textbbox((0, 0), text, font=font_title)
        text_w = text_bbox[2] - text_bbox[0]
        text_x = (w - text_w) // 2
        text_y = int(h * 0.82)
        # Shadow
        draw.text((text_x + 2, text_y + 2), text, font=font_title, fill=(0, 0, 0, 220))
        draw.text((text_x, text_y), text, font=font_title, fill=(255, 255, 255, 255))
        
    if brand_tag:
        tag_bbox = draw.textbbox((0, 0), brand_tag, font=font_tag)
        tag_w = tag_bbox[2] - tag_bbox[0]
        tag_x = (w - tag_w) // 2
        tag_y = int(h * 0.89)
        draw.text((tag_x + 1, tag_y + 1), brand_tag, font=font_tag, fill=(0, 0, 0, 180))
        draw.text((tag_x, tag_y), brand_tag, font=font_tag, fill=(240, 240, 240, 220))
        
    return frame_img

def render_motion_video(image_path, output_path, duration=6.0, fps=24, motion="zoom_in", aspect="9:16", text=None):
    """Render full MP4 video with motion kinetics and typography."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"找不到輸入圖片: {image_path}")
        
    # Canvas dimension
    if aspect == "9:16":
        canvas_w, canvas_h = 1080, 1920
    elif aspect == "1:1":
        canvas_w, canvas_h = 1080, 1080
    else:
        canvas_w, canvas_h = 1920, 1080
        
    img = Image.open(image_path).convert("RGBA")
    total_frames = int(duration * fps)
    
    print(f"🎬 [Polaris Motion] 開始渲染短影音...")
    print(f"📐 規格: {aspect} ({canvas_w}x{canvas_h}) | 長度: {duration}s | 總幀數: {total_frames} | 運鏡模式: {motion}")
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=8, pixelformat='yuv420p')
    
    for f in range(total_frames):
        progress = f / float(total_frames) # 0.0 to 1.0
        
        # Calculate dynamic motion parameters
        if motion == "zoom_in":
            scale = 1.0 + 0.15 * progress
            pan_x, pan_y = 0.0, -0.05 * progress
        elif motion == "zoom_out":
            scale = 1.15 - 0.15 * progress
            pan_x, pan_y = 0.0, 0.05 * progress
        elif motion == "pan_up":
            scale = 1.10
            pan_x = 0.0
            pan_y = 0.1 - 0.2 * progress
        elif motion == "breathing":
            scale = 1.0 + 0.06 * np.sin(progress * np.pi)
            pan_x, pan_y = 0.0, 0.0
        else:
            scale = 1.0
            pan_x, pan_y = 0.0, 0.0
            
        frame_canvas = crop_and_resize_to_canvas(img, canvas_w, canvas_h, scale=scale, pan_x=pan_x, pan_y=pan_y)
        
        # Apply subtitles on the canvas
        final_frame = overlay_subtitles_and_branding(frame_canvas, text=text)
        
        # Convert PIL to RGB numpy array for imageio
        rgb_frame = np.array(final_frame.convert("RGB"))
        writer.append_data(rgb_frame)
        
        if (f + 1) % int(fps * 2) == 0 or f == total_frames - 1:
            print(f"   ↳ 渲染進度: {int((f + 1) / total_frames * 100)}% ({f + 1}/{total_frames} 幀)")
            
    writer.close()
    print(f"✨ [Polaris Motion] 短影音合成完畢！\n📁 產出路徑: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="極星微動態短影音自動合成引擎")
    parser.add_argument("--image", type=str, required=True, help="輸入靜態高清圖片路徑")
    parser.add_argument("--output", type=str, default="", help="輸出 .mp4 影片檔案路徑")
    parser.add_argument("--duration", type=float, default=6.0, help="影片秒數長度 (預設 6.0)")
    parser.add_argument("--fps", type=int, default=24, help="每秒影格數 (預設 24)")
    parser.add_argument("--motion", choices=["zoom_in", "zoom_out", "pan_up", "breathing"], default="zoom_in", help="運鏡模式")
    parser.add_argument("--aspect", choices=["9:16", "1:1", "16:9"], default="9:16", help="影音畫面比例")
    parser.add_argument("--text", type=str, default="", help="畫面動態字幕文案")
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    
    if args.output:
        out_path = args.output
    else:
        stem = Path(args.image).stem
        out_path = str(skill_dir / "output" / f"{stem}_{args.motion}_{args.aspect.replace(':', '_')}.mp4")
        
    render_motion_video(
        image_path=args.image,
        output_path=out_path,
        duration=args.duration,
        fps=args.fps,
        motion=args.motion,
        aspect=args.aspect,
        text=args.text
    )

if __name__ == "__main__":
    main()
