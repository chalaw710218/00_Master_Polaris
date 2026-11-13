#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_diagram_artisan.py - 約瑟夫商業數據與服務流程圖卡視覺化引擎
版權所有 (c) 2026 極星內閣 - 首席視覺長約瑟夫 (Josef / CVO)
"""

import sys
import json
import argparse
import os

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 極星地理色彩代碼
COLOR_DEEP_BLUE = "#0F2537"
COLOR_GOLD = "#D4AF37"
COLOR_SUNRISE_RED = "#E24A3B"
COLOR_RICE_WHITE = "#F9F8F5"
COLOR_CARBON_BLACK = "#1E1E1E"

def generate_flow_svg(title: str, steps: list) -> str:
    """生成服務流程向量 SVG 圖卡 (800x450)"""
    width = 800
    height = 450
    step_count = len(steps)
    step_width = (width - 100) / max(1, step_count)
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'  <rect width="{width}" height="{height}" fill="{COLOR_RICE_WHITE}" rx="16"/>',
        f'  <text x="50" y="60" font-family="system-ui, sans-serif" font-size="28" font-weight="bold" fill="{COLOR_DEEP_BLUE}">{title}</text>',
        f'  <line x1="50" y1="80" x2="750" y2="80" stroke="{COLOR_GOLD}" stroke-width="3"/>'
    ]
    
    for i, step in enumerate(steps):
        center_x = 50 + (i * step_width) + (step_width / 2)
        center_y = 220
        
        # 連接線
        if i < step_count - 1:
            next_x = 50 + ((i + 1) * step_width) + (step_width / 2)
            svg_lines.append(f'  <line x1="{center_x}" y1="{center_y}" x2="{next_x}" y2="{center_y}" stroke="{COLOR_DEEP_BLUE}" stroke-width="4" stroke-dasharray="6,6"/>')
            
        # 節點圓形
        svg_lines.append(f'  <circle cx="{center_x}" cy="{center_y}" r="32" fill="{COLOR_DEEP_BLUE}" stroke="{COLOR_GOLD}" stroke-width="4"/>')
        svg_lines.append(f'  <text x="{center_x}" y="{center_y + 8}" font-family="system-ui, sans-serif" font-size="20" font-weight="bold" fill="{COLOR_RICE_WHITE}" text-anchor="middle">{i+1}</text>')
        
        # 步驟文字
        svg_lines.append(f'  <text x="{center_x}" y="{center_y + 70}" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="{COLOR_CARBON_BLACK}" text-anchor="middle">{step}</text>')
        
    svg_lines.append(f'  <text x="50" y="410" font-family="system-ui, sans-serif" font-size="13" fill="#888888">生活的一部分，就醬點！· 生活管家服務體系</text>')
    svg_lines.append('</svg>')
    
    return "\n".join(svg_lines)

def build_diagram(data: dict) -> dict:
    """構建商業數據或流程圖卡"""
    title = data.get("title", "服務流程圖卡")
    steps = data.get("steps", [])
    output_path = data.get("output_svg")
    
    svg_code = generate_flow_svg(title, steps)
    
    if output_path:
        try:
            # 確保目錄存在
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_code)
            saved = True
        except Exception as e:
            saved = False
    else:
        saved = False
        
    return {
        "title": title,
        "step_count": len(steps),
        "steps": steps,
        "color_palette_applied": {
            "primary": COLOR_DEEP_BLUE,
            "accent_gold": COLOR_GOLD,
            "background": COLOR_RICE_WHITE
        },
        "svg_file_saved": output_path if saved else "MEMORY_BUFFER",
        "svg_bytes_length": len(svg_code),
        "josef_commentary": "流程視覺化生成完畢！採用黑潮深藍與池上金配色，節點清晰，一目了然！"
    }

def main():
    parser = argparse.ArgumentParser(description="約瑟夫商業流程與圖卡視覺化引擎")
    parser.add_argument("--flow-diagram", type=str, required=True, help="流程資料 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.flow_diagram)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = build_diagram(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
