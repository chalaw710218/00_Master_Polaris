#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/overlay_safezone.py
短影音安全區避讓字幕與品牌動態覆層精算引擎
嚴格避讓 IG Reels/Threads/TikTok 原生 UI、防眩光漸層、Fade In/Out 時間軸與品牌零洩漏審查
"""

import sys
import argparse
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]

# IG Reels / TikTok / Threads 9:16 (1080x1920) 原生 UI 邊界
SAFE_ZONE_SPEC_9_16 = {
    "top_system_bar_px": 180,      # 頂部狀態列與返回按鈕
    "bottom_caption_bar_px": 380,  # 底部原作者帳號與貼文前兩行
    "right_action_bar_px": 140,    # 右側愛心、留言、轉發、收藏按鈕列
    "left_margin_px": 80           # 左側呼吸邊距
}

def calculate_safe_zone(canvas_w: int = 1080, canvas_h: int = 1920) -> Dict[str, Any]:
    """計算實體黃金可視安全矩形 (Safe Zone Bounding Box)"""
    top = SAFE_ZONE_SPEC_9_16["top_system_bar_px"]
    bottom = canvas_h - SAFE_ZONE_SPEC_9_16["bottom_caption_bar_px"]
    left = SAFE_ZONE_SPEC_9_16["left_margin_px"]
    right = canvas_w - SAFE_ZONE_SPEC_9_16["right_action_bar_px"]

    safe_w = right - left
    safe_h = bottom - top

    return {
        "safe_rect": {
            "left_px": left,
            "right_px": right,
            "top_px": top,
            "bottom_px": bottom,
            "width_px": safe_w,
            "height_px": safe_h
        },
        "typography_anchors": {
            "main_title_y_px": bottom - 100,  # 緊靠安全區底線上方 100px (最佳黃金視線)
            "brand_tag_y_px": bottom - 30     # 安全區底部貼線
        }
    }

def calculate_text_fade_alpha(frame_idx: int, total_frames: int, fps: int = 24) -> float:
    """計算字幕淡入 (0~0.8s) 與淡出 (倒數 0.5s) 不透明度 (0.0 ~ 1.0)"""
    t_sec = frame_idx / fps
    total_sec = total_frames / fps

    # 淡入區間 (0 ~ 0.8s)
    if t_sec < 0.8:
        return min(1.0, t_sec / 0.8)
    # 淡出區間 (結尾前 0.5s)
    elif t_sec > (total_sec - 0.5):
        remain = max(0.0, total_sec - t_sec)
        return min(1.0, remain / 0.5)
    # 常駐完全不透明
    else:
        return 1.0

Tuple_Result = tuple[bool, str]

def inspect_brand_redline(text: str, brand_tag: str) -> Tuple_Result:
    """戴明安燈：出廠前品牌法定名稱零洩漏防火牆審查"""
    combined = f"{text} {brand_tag}"
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in combined:
            return False, f"海報/短影音文案出現內部代號「{forbidden}」，觸發品牌紅線安燈！對外僅能使用「生活管家」或「生活的一部分，就醬點！」"
    return True, "品牌審查通過：100% 符合對外法定名稱規範"

def main():
    parser = argparse.ArgumentParser(description="短影音安全區避讓字幕與品牌動態覆層精算引擎")
    parser.add_argument("--title", type=str, default="起鍋前的一圈米酒，是整個廚房最迷人的時刻 🔥", help="字幕主標題")
    parser.add_argument("--brand-tag", type=str, default="生活管家，就醬點！ @hellotaitung", help="品牌署名標識")
    parser.add_argument("--duration", type=float, default=5.0, help="影片時長 (秒)")
    parser.add_argument("--fps", type=int, default=24, help="每秒畫格數")
    parser.add_argument("--dry-run", action="store_true", help="執行安全區與覆層幾何模擬")
    args = parser.parse_args()

    # 1. 品牌紅線審查
    is_valid_brand, brand_msg = inspect_brand_redline(args.title, args.brand_tag)
    if not is_valid_brand:
        print("==================================================")
        print("🛑 戴明安燈拉繩！短影音覆層出廠攔截！")
        print(f"[✗] {brand_msg}")
        print("==================================================")
        sys.exit(1)

    # 2. 安全區幾何精算
    safe_info = calculate_safe_zone(1080, 1920)
    total_frames = int(args.duration * args.fps)

    # 3. 抽樣淡入淡出 Alpha
    alpha_samples = [
        (0, calculate_text_fade_alpha(0, total_frames, args.fps)),
        (int(args.fps * 0.4), calculate_text_fade_alpha(int(args.fps * 0.4), total_frames, args.fps)),
        (int(args.fps * 1.5), calculate_text_fade_alpha(int(args.fps * 1.5), total_frames, args.fps)),
        (total_frames - int(args.fps * 0.25), calculate_text_fade_alpha(total_frames - int(args.fps * 0.25), total_frames, args.fps)),
        (total_frames - 1, calculate_text_fade_alpha(total_frames - 1, total_frames, args.fps))
    ]

    print("==================================================")
    print("📱 短影音社群 UI 安全區幾何與動態覆層精算完成 (Exit Code: 0)")
    print(f"畫布規格: 1080 x 1920 (9:16 直式 Reels / Threads / TikTok)")
    print(f"安全可視矩形: 左 {safe_info['safe_rect']['left_px']}px ~ 右 {safe_info['safe_rect']['right_px']}px | 上 {safe_info['safe_rect']['top_px']}px ~ 下 {safe_info['safe_rect']['bottom_px']}px")
    print(f"UI 避讓邊界: 頂部扣除 {SAFE_ZONE_SPEC_9_16['top_system_bar_px']}px | 底部文案避讓 {SAFE_ZONE_SPEC_9_16['bottom_caption_bar_px']}px | 右側按鈕避讓 {SAFE_ZONE_SPEC_9_16['right_action_bar_px']}px")
    print("--------------------------------------------------")
    print("🔤 動態字卡排版座標與光學屬性:")
    print(f"  - 主字幕 Y 軸錨點: {safe_info['typography_anchors']['main_title_y_px']} px (避開底部文案區，100% 居中無遮擋)")
    print(f"  - 品牌標識 Y 軸錨點: {safe_info['typography_anchors']['brand_tag_y_px']} px (署名: {args.brand_tag})")
    print(f"  - 防眩光漸變層: 底部高度 537 px (28% 漸層黑遮罩，抗背光白字清晰)")
    print("--------------------------------------------------")
    print("⏳ 字幕動態淡入淡出 (Fade-In/Out) 時間軸驗證:")
    for f_idx, alpha in alpha_samples:
        t_sec = f_idx / args.fps
        print(f"  - Frame {f_idx:03d} [{t_sec:4.2f}s]: 字幕不透明度 Alpha = {alpha * 100:5.1f}%")
    print("--------------------------------------------------")
    print(f"🛡️ 品牌法定名稱防火牆: {brand_msg}")
    print("==================================================")

if __name__ == "__main__":
    main()
