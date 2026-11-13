#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-gentle-optical-tokens: 光學符記與高齡 APCA 對比度審計原子
由首席前端架構師尼奧 (Neo) ✕ 首席視覺長約瑟夫 (Josef) 聯合打造
"""

import sys
import os
import argparse
import math

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    hex_str = hex_str.strip().lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    if len(hex_str) != 6:
        raise ValueError(f"無效的 HEX 顏色格式: #{hex_str}")
    return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def sRGB_to_luminance(r: int, g: int, b: int) -> float:
    # 物理感知亮度轉換 (sRGB Y)
    def channel_linear(c: int) -> float:
        v = c / 255.0
        return math.pow((v + 0.055) / 1.055, 2.4) if v > 0.04045 else v / 12.92
    
    r_lin = channel_linear(r)
    g_lin = channel_linear(g)
    b_lin = channel_linear(b)
    return 0.2126729 * r_lin + 0.7151522 * g_lin + 0.0721750 * b_lin

def calculate_simple_apca_lc(txt_hex: str, bg_hex: str) -> float:
    """
    計算簡化版 APCA (Lc) 輕感知對比度數值
    回傳絕對值對比分數 (0~110)
    """
    txt_rgb = hex_to_rgb(txt_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    
    y_txt = sRGB_to_luminance(*txt_rgb)
    y_bg = sRGB_to_luminance(*bg_rgb)
    
    # 鉗位防除零
    y_txt = max(y_txt, 0.001)
    y_bg = max(y_bg, 0.001)
    
    if y_bg > y_txt:
        # 暗字在亮底 (常規淺色模式)
        ratio = (math.pow(y_bg, 0.56) - math.pow(y_txt, 0.62)) * 1.14
        lc = ratio * 100.0
    else:
        # 亮字在暗底 (深色模式)
        ratio = (math.pow(y_txt, 0.56) - math.pow(y_bg, 0.62)) * 1.14
        lc = ratio * 100.0
    return abs(lc)

def generate_gentle_css(txt_hex: str, bg_hex: str, optical_ratio: float, mode: str) -> str:
    accent_warm = "#D97706" if mode == "light" else "#F59E0B"
    border_soft = "#E5E0D8" if mode == "light" else "#2D3135"
    
    css = f"""/**
 * Polaris Gentle UI Design Tokens (v1.0)
 * 專為常民與高齡視力平權打造之光學級 CSS 變數
 * 模式: {mode.upper()} | 菲克補償比: {optical_ratio:.2f}
 */
:root {{
  /* [基礎色彩系統 · 風土大地色彩] */
  --gentle-color-bg: {bg_hex};
  --gentle-color-text-main: {txt_hex};
  --gentle-color-accent-warm: {accent_warm};
  --gentle-color-border-subtle: {border_soft};

  /* [光學排版與字體微感知] */
  --gentle-font-family: system-ui, -apple-system, BlinkMacSystemFont, "PingFang TC", "Microsoft JhengHei", sans-serif;
  --gentle-stroke-optical-ratio: {optical_ratio:.2f}; /* 約瑟夫光學橫細豎粗 1:{optical_ratio:.2f} */
  
  /* [高齡視力平權尺寸規範 - 最小正文字體 18px，標題 24px+] */
  --gentle-font-size-body: 1.125rem; /* 18px */
  --gentle-font-size-title: 1.5rem;   /* 24px */
  --gentle-font-size-hero: 2rem;      /* 32px */
  --gentle-line-height-comfortable: 1.75;
  --gentle-letter-spacing-open: 0.025em;

  /* [無挫折觸控基數 - 最小熱區 56px] */
  --gentle-touch-min-target: 56px;
  --gentle-radius-organic: 12px;
  --gentle-shadow-ambient: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}}

/* [約瑟夫中西混排光學校正樣式] */
.gentle-body-text {{
  font-family: var(--gentle-font-family);
  font-size: var(--gentle-font-size-body);
  line-height: var(--gentle-line-height-comfortable);
  letter-spacing: var(--gentle-letter-spacing-open);
  color: var(--gentle-color-text-main);
  background-color: var(--gentle-color-bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
"""
    return css

def main():
    parser = argparse.ArgumentParser(description="光學符記與高齡對比度審計原子 (atom-gentle-optical-tokens)")
    parser.add_argument("--primary-color", type=str, default="#2C261E", help="主要文字/前景色彩 HEX (預設縱谷深炭褐 #2C261E)")
    parser.add_argument("--bg-color", type=str, default="#FBF9F5", help="背景色彩 HEX (預設暖米紙白 #FBF9F5)")
    parser.add_argument("--surface-mode", type=str, choices=["light", "dark"], default="light", help="介面色彩模式")
    parser.add_argument("--optical-ratio", type=float, default=1.18, help="菲克垂直水平筆畫補償比率 (預設 1.18)")
    parser.add_argument("--output-css", type=str, default="gentle-ui-tokens.css", help="產出 CSS 路徑")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")
    
    args = parser.parse_args()
    
    txt_color = args.primary_color
    bg_color = args.bg_color
    
    # 1. APCA 對比度硬核物理審計
    lc_score = calculate_simple_apca_lc(txt_color, bg_color)
    min_required_lc = 75.0  # 高齡無挫折與烈日環境下 APCA 最低要求 Lc >= 75
    
    passed_audit = lc_score >= min_required_lc
    
    print(f"=== [atom-gentle-optical-tokens 光學符記與高齡對比度審計] ===")
    print(f"前景文字色: {txt_color} | 背景色: {bg_color} | 模式: {args.surface_mode.upper()}")
    print(f"菲克橫細豎粗光學補償: 1:{args.optical_ratio:.2f}")
    print(f"APCA 輕感知對比度 (Lc): {lc_score:.2f} (門檻要求: >= {min_required_lc:.1f})")
    
    if not passed_audit:
        print(f"[戴明安燈警報] APCA Lc 未達標 ({lc_score:.2f} < {min_required_lc})！在高齡或強光下可讀性嚴重不足！")
        sys.exit(1)
    
    print(f"[APCA 視力平權門禁] 審計合格！滿足常民與縱谷烈日高對比要求。")
    
    css_content = generate_gentle_css(txt_color, bg_color, args.optical_ratio, args.surface_mode)
    
    if args.dry_run:
        print(f"\n[物理演練模式 --dry-run] 產生之 gentle-ui-tokens.css 預覽 (前 250 字元):")
        print(css_content[:250] + "...\n")
        print("[物理演練驗證成功] Exit Code: 0")
        return
        
    with open(args.output_css, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"[實體文件落地] 已生成光學 CSS 符記庫: {args.output_css}")
    print("[執行成功] Exit Code: 0")

if __name__ == "__main__":
    main()
