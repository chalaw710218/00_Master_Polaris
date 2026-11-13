#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hyperlocal Visual Design System & Kinetic Tokens (在地常民風土美學與微動態設計系統腳本)
落實創辦人親授「約瑟夫主要負責視覺化的部分」法旨。
自動匯出黑潮深藍、池上金、太麻里紅風土色彩學與 Modular Scale 1.25 字階。
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Windows UTF-8 stdout/stderr 安全重定向
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def generate_design_tokens(output_format: str = "tailwind"):
    """生成極星在地風土美學 Design Tokens"""
    
    tokens = {
        "colors": {
            "kuroshio-deep-blue": "#0a1128",
            "kuroshio-navy": "#1c2541",
            "chishang-gold": "#d4af37",
            "chishang-light-gold": "#f3e5ab",
            "taimali-sunrise-red": "#e63946",
            "taidong-slate": "#475569",
            "homely-cream-white": "#f8f9fa",
            "pure-black-barrier": "#030712"
        },
        "typography": {
            "scale_ratio": 1.25, # Major Third
            "font_family_sans": "system-ui, -apple-system, 'Noto Sans TC', sans-serif",
            "font_sizes": {
                "display": "48px",
                "h1": "38px",
                "h2": "30px",
                "h3": "24px",
                "body": "16px",
                "small": "14px"
            },
            "line_heights": {
                "tight": "1.2",
                "normal": "1.6",
                "relaxed": "1.8"
            }
        },
        "micro_kinetics": {
            "card_hover_lift": "translateY(-2px)",
            "photo_zoom_ratio": "scale(1.025)",
            "button_press": "translateY(1px)",
            "transition_timing": "cubic-bezier(0.33, 1, 0.68, 1)",
            "transition_duration": "240ms"
        },
        "layout_grid": {
            "columns": 12,
            "max_width": "1280px",
            "gutter": "24px",
            "senior_touch_target_min": "48px"
        }
    }

    if output_format == "css":
        css_lines = [":root {"]
        for c_name, c_hex in tokens["colors"].items():
            css_lines.append(f"  --color-{c_name}: {c_hex};")
        for f_name, f_size in tokens["typography"]["font_sizes"].items():
            css_lines.append(f"  --font-size-{f_name}: {f_size};")
        css_lines.append(f"  --transition-default: all {tokens['micro_kinetics']['transition_duration']} {tokens['micro_kinetics']['transition_timing']};")
        css_lines.append("}")
        return "\n".join(css_lines)

    # 預設回傳 Tailwind 配置字典 / JSON
    export_payload = {
        "status": "DESIGN_TOKENS_GENERATED",
        "artisan": "Josef (Chief Visual Officer)",
        "theme_name": "Polaris Taitung Hyperlocal Elegance",
        "generated_at": datetime.now().isoformat(),
        "design_tokens": tokens,
        "frontend_framework_compatibility": ["Tailwind CSS v3/v4", "Vanilla CSS", "React Styled-Components"],
        "taste_guarantee": "100% 杜絕 AI 模板塑料感，完美呈現台東純淨客廳與黑潮深邃秩序！"
    }
    return export_payload

def main():
    parser = argparse.ArgumentParser(description="Hyperlocal Visual Design System")
    parser.add_argument("--export-tokens", action="store_true", help="匯出風土 Design Tokens")
    parser.add_argument("--format", type=str, default="tailwind", choices=["tailwind", "css"], help="輸出格式")

    args = parser.parse_args()

    res = generate_design_tokens(args.format)
    if args.format == "css":
        print(res)
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
