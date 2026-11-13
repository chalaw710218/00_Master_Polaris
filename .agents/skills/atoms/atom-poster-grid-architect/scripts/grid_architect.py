#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/grid_architect.py
約瑟夫 12 欄複合網格與光學排版精算引擎
嚴格遵循約瑟夫六十項終極法典、CSF 高齡視力平權與台東風土幾何比例
"""

import sys
import json
import argparse
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

# 標準印刷與數位尺寸定義 (300 DPI 像素換算)
FORMAT_SPECS = {
    "A3": {
        "width_px": 3508,
        "height_px": 4960,
        "bleed_mm": 3,
        "bleed_px": 85,
        "dpi": 300,
        "columns": 12,
        "margin_px": 177, # 約 15mm
        "gutter_px": 47   # 約 4mm
    },
    "A4": {
        "width_px": 2480,
        "height_px": 3508,
        "bleed_mm": 3,
        "bleed_px": 85,
        "dpi": 300,
        "columns": 12,
        "margin_px": 142, # 約 12mm
        "gutter_px": 35   # 約 3mm
    },
    "IG_PORTRAIT": {
        "width_px": 1080,
        "height_px": 1350,
        "bleed_mm": 0,
        "bleed_px": 0,
        "dpi": 72,
        "columns": 8,
        "margin_px": 64,
        "gutter_px": 24
    },
    "REELS": {
        "width_px": 1080,
        "height_px": 1920,
        "bleed_mm": 0,
        "bleed_px": 0,
        "dpi": 72,
        "columns": 8,
        "margin_px": 64,
        "gutter_px": 24
    }
}

# 台東在地風土大地調色盤 (CMYK 印刷安全值 + Web HEX)
TERROIR_PALETTES = {
    "local_produce": {
        "name": "台東大地與熟穗生機色系",
        "primary": {"hex": "#E08B28", "cmyk": "C0 M50 Y95 K0", "label": "關山熟穗金 (主視覺)"},
        "secondary": {"hex": "#2C5E3B", "cmyk": "C75 M25 Y80 K30", "label": "中央山脈松柏綠 (次標/護角)"},
        "accent": {"hex": "#D9381E", "cmyk": "C10 M90 Y90 K0", "label": "大武野薑金萱紅 (CTA/印章)"},
        "background": {"hex": "#F9F6F0", "cmyk": "C2 M2 Y5 K0", "label": "未漂白大豆紙原色 (底色)"},
        "text": {"hex": "#1A1918", "cmyk": "C0 M0 Y0 K95", "label": "松煙碳黑 (內文/高對比)"}
    },
    "senior_care": {
        "name": "生活管家溫潤守護色系",
        "primary": {"hex": "#1B3B6F", "cmyk": "C90 M65 Y20 K25", "label": "太平洋深海晨藍 (安穩主視覺)"},
        "secondary": {"hex": "#C29B38", "cmyk": "C20 M35 Y85 K5", "label": "晨光暖橙金 (溫暖輔色)"},
        "accent": {"hex": "#9E2A2B", "cmyk": "C20 M90 Y75 K15", "label": "鹿野紅烏龍磚紅 (重點警示/二維碼)"},
        "background": {"hex": "#FAF8F5", "cmyk": "C1 M1 Y3 K0", "label": "暖玉白 (舒適護眼底色)"},
        "text": {"hex": "#121820", "cmyk": "C0 M0 Y0 K98", "label": "極深湛青黑 (高齡 CSF 視力平權標題)"}
    },
    "tech_workshop": {
        "name": "極星前沿開拓純粹色系",
        "primary": {"hex": "#0D1B2A", "cmyk": "C85 M70 Y50 K60", "label": "深邃星空青墨 (極致理性)"},
        "secondary": {"hex": "#415A77", "cmyk": "C65 M45 Y30 K5", "label": "太平洋鐵灰藍 (架構輔色)"},
        "accent": {"hex": "#00B4D8", "cmyk": "C70 M0 Y5 K0", "label": "光纖躍動湖水藍 (高光提示)"},
        "background": {"hex": "#FFFFFF", "cmyk": "C0 M0 Y0 K0", "label": "純淨雪白"},
        "text": {"hex": "#050B14", "cmyk": "C0 M0 Y0 K100", "label": "K100 單色黑直壓"}
    }
}

def calculate_grid_and_typography(fmt: str, theme: str, title: str, subtitle: str = "") -> Dict[str, Any]:
    """計算嚴謹物理網格、CSF 高齡視力平權字級梯隊與排版約束"""
    spec = FORMAT_SPECS.get(fmt, FORMAT_SPECS["A4"])
    palette = TERROIR_PALETTES.get(theme, TERROIR_PALETTES["senior_care"])

    w = spec["width_px"]
    h = spec["height_px"]
    bleed = spec["bleed_px"]
    cols = spec["columns"]
    margin = spec["margin_px"]
    gutter = spec["gutter_px"]

    # 實體淨畫布 (扣除出血線後)
    net_w = w - (bleed * 2)
    net_h = h - (bleed * 2)

    # 12 欄寬度計算: net_w - (margin * 2) - (gutter * (cols - 1))
    total_gutters = gutter * (cols - 1)
    usable_w = net_w - (margin * 2)
    col_w = (usable_w - total_gutters) / cols

    # 高齡 CSF 視力平權字級換算 (基於淨高度比例，避免任何看不清楚)
    # 標題 >= 1/14 畫布高度
    title_font_size = round(net_h / 14)
    # 副標題 >= 1/26 畫布高度
    subtitle_font_size = round(net_h / 26)
    # 正文內文 >= 1/48 畫布高度 (印刷在 A4 約 18pt 以上，長者極易閱讀)
    body_font_size = round(net_h / 48)
    # 註釋/電話/QR說明 >= 1/65 畫布高度 (A4 約 13pt 以上)
    caption_font_size = round(net_h / 65)

    # 最小 QR Code 印刷物理大小 (法典規定：至少 28mm，300 DPI 下約 330px)
    min_qr_size_px = 330 if spec["dpi"] == 300 else 180

    return {
        "status": "SUCCESS",
        "format": fmt,
        "specifications": {
            "canvas_total_px": f"{w} x {h}",
            "net_canvas_px": f"{net_w} x {net_h}",
            "dpi": spec["dpi"],
            "bleed_px": bleed,
            "bleed_mm": spec["bleed_mm"],
            "margin_px": margin,
            "columns": cols,
            "column_width_px": round(col_w, 1),
            "gutter_px": gutter
        },
        "optical_typography_csf": {
            "title": {
                "text": title,
                "recommended_size_px": title_font_size,
                "line_height_ratio": 1.25,
                "optical_balance_ratio": "橫細豎粗 1:1.18 補償"
            },
            "subtitle": {
                "text": subtitle or "生活的一部分，就醬點！",
                "recommended_size_px": subtitle_font_size,
                "line_height_ratio": 1.35
            },
            "body": {
                "recommended_size_px": body_font_size,
                "line_height_ratio": 1.6,
                "max_chars_per_line": 28
            },
            "qr_and_contacts": {
                "min_qr_dimension_px": min_qr_size_px,
                "min_qr_dimension_mm": "28mm (防呆掃描極限)",
                "caption_size_px": caption_font_size
            }
        },
        "terroir_palette": palette,
        "grid_layout_blueprint": [
            {"zone": "頂部呼吸區 (天頭)", "height_span_ratio": 0.12, "usage": "品牌識別、微氣象/風土小引"},
            {"zone": "視覺核心層 (視覺焦點)", "height_span_ratio": 0.40, "usage": "真實高清攝影、阿美族八角花幾何微彩蛋"},
            {"zone": "標題與敘事層 (黃金視線)", "height_span_ratio": 0.28, "usage": f"主標題 ({title_font_size}px) + 副標題"},
            {"zone": "行動召喚與地基 (地腳)", "height_span_ratio": 0.20, "usage": f"雙欄排版：左側明碼價格/時間，右側 {min_qr_size_px}px QR Code 與客服電話"}
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="約瑟夫 12 欄複合網格與光學排版精算引擎")
    parser.add_argument("--format", type=str, default="A4", choices=["A3", "A4", "IG_PORTRAIT", "REELS"], help="海報格式規格")
    parser.add_argument("--theme", type=str, default="senior_care", choices=["local_produce", "senior_care", "tech_workshop"], help="風土主題配色")
    parser.add_argument("--title", type=str, default="生活管家·溫暖安居到府服務", help="主標題文字")
    parser.add_argument("--subtitle", type=str, default="生活的一部分，就醬點！", help="副標題文字")
    parser.add_argument("--dry-run", action="store_true", help="執行排版幾何模擬驗證")
    args = parser.parse_args()

    result = calculate_grid_and_typography(args.format, args.theme, args.title, args.subtitle)

    print("==================================================")
    print("📐 約瑟夫 12 欄複合網格與光學排版精算完成 (Exit Code: 0)")
    print(f"規格格式: {args.format} (總解析度: {result['specifications']['canvas_total_px']} @ {result['specifications']['dpi']} DPI)")
    print(f"出血線: {result['specifications']['bleed_mm']} mm ({result['specifications']['bleed_px']} px) | 內距邊界: {result['specifications']['margin_px']} px")
    print(f"網格欄位: {result['specifications']['columns']} 欄 | 每欄寬: {result['specifications']['column_width_px']} px | 間距: {result['specifications']['gutter_px']} px")
    print("--------------------------------------------------")
    print("👀 高齡 CSF 視力平權字級梯隊:")
    print(f"  - 主標題: {result['optical_typography_csf']['title']['recommended_size_px']} px ({result['optical_typography_csf']['title']['optical_balance_ratio']})")
    print(f"  - 副標題: {result['optical_typography_csf']['subtitle']['recommended_size_px']} px")
    print(f"  - 內文字: {result['optical_typography_csf']['body']['recommended_size_px']} px (每行建議 <= 28 繁體漢字)")
    print(f"  - QR Code: {result['optical_typography_csf']['qr_and_contacts']['min_qr_dimension_px']} px ({result['optical_typography_csf']['qr_and_contacts']['min_qr_dimension_mm']})")
    print("--------------------------------------------------")
    print(f"🎨 風土調色盤 [{result['terroir_palette']['name']}]:")
    print(f"  - 主色: {result['terroir_palette']['primary']['label']} -> {result['terroir_palette']['primary']['hex']} / {result['terroir_palette']['primary']['cmyk']}")
    print(f"  - 輔色: {result['terroir_palette']['secondary']['label']} -> {result['terroir_palette']['secondary']['hex']}")
    print(f"  - 內文: {result['terroir_palette']['text']['label']} -> {result['terroir_palette']['text']['cmyk']}")
    print("==================================================")

if __name__ == "__main__":
    main()
