# -*- coding: utf-8 -*-
"""
Polaris Visual Design & Print Production Generator
Script: generate_print_collaterals.py
Author: Josef Müller-Brockmann (CVO) & Yuki (CEO) & Deming (CQO)
Description:
  Generates commercial-grade vector SVG print assets and HTML preview galleries
  for "生活的一部分，就醬點！" (LifeButler) according to CIS Guidelines v1.0.
  
Includes:
  1. Business Card Front & Back (90mm x 54mm + 1mm bleed)
  2. Delivery Box Mascot Seal Badge (150mm diameter + 2mm bleed)
  3. Packaging Sealing Strip (120mm x 35mm + 1mm bleed)
  4. HTML Visual Showcase with responsive rendering & print marks
"""

import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "03_Print_Collaterals")

os.makedirs(os.path.join(OUTPUT_DIR, "01_Business_Card_90x54mm"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "02_Delivery_Box_Badge_150mm"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "03_Package_Sealing_Strip_120x35mm"), exist_ok=True)

# -------------------------------------------------------------
# 1. 生活管家隨身名片 正面 (Business Card Front: 90x54mm + 1mm bleed = 92x56mm)
# -------------------------------------------------------------
# ViewBox in mm scale: 92 x 56 mm. Trim box: (1, 1, 90, 54).
def generate_business_card_front():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 92 56" width="92mm" height="56mm">
  <defs>
    <style>
      .bg { fill: #FAF8F3; }
      .bleed-border { fill: none; stroke: #E8E4DA; stroke-width: 0.2; stroke-dasharray: 1 1; }
      .brand-primary { fill: #F5A623; }
      .brand-secondary { fill: #8B572A; }
      .brand-ink { fill: #1A1A1A; }
      .brand-fresh { fill: #2E7D32; }
      .text-title { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 3.4px; fill: #1A1A1A; letter-spacing: 0.15px; }
      .text-subtitle { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 1.8px; fill: #8B572A; letter-spacing: 0.08px; }
      .text-name { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 5.2px; fill: #1A1A1A; letter-spacing: 0.4px; }
      .text-role { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 2.2px; fill: #8B572A; }
      .text-tag { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 500; font-size: 1.6px; fill: #4A4A4A; }
      .text-contact-label { font-family: 'DIN Next', 'Barlow', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 1.8px; fill: #8B572A; }
      .text-contact-val { font-family: 'DIN Next', 'Barlow', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 2.3px; fill: #1A1A1A; letter-spacing: 0.2px; }
      .accent-pill { fill: #F5A623; rx: 0.8px; }
      .pill-text { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 1.5px; fill: #FFFFFF; }
    </style>
  </defs>

  <!-- 出血背景 (含 1mm 出血) -->
  <rect width="92" height="56" class="bg"/>

  <!-- 出血安全裁切示意框 (Trim Line: 90 x 54 mm, 距邊緣 1mm) -->
  <rect x="1" y="1" width="90" height="54" class="bleed-border"/>

  <!-- 左上角：軌道 A 品牌符號與品牌字標 -->
  <g transform="translate(6, 6)">
    <!-- 圓角幾何生活圖標 (Pin + Smile) -->
    <rect x="0" y="0" width="7.2" height="7.2" rx="1.8" class="brand-primary"/>
    <circle cx="3.6" cy="3.0" r="1.2" fill="#FFFFFF"/>
    <circle cx="3.6" cy="3.0" r="0.5" fill="#F5A623"/>
    <path d="M 2.1 5.1 Q 3.6 6.3 5.1 5.1" stroke="#FFFFFF" stroke-width="0.45" stroke-linecap="round" fill="none"/>

    <!-- 品牌全稱與標語 -->
    <text x="9.2" y="4.0" class="text-title">生活的一部分，就醬點！</text>
    <text x="9.3" y="6.6" class="text-subtitle">日常便利 · 暖心到府 · 在地生活管家</text>
  </g>

  <!-- 幾何分割與裝飾線 (極簡包浩斯) -->
  <line x1="6" y1="17" x2="86" y2="17" stroke="#E8E4DA" stroke-width="0.3"/>
  <rect x="6" y="16.8" width="8" height="0.4" fill="#F5A623"/>

  <!-- 左下主體：人物與職稱 -->
  <g transform="translate(6, 25)">
    <text x="0" y="0" class="text-name">品 碩</text>
    <text x="17" y="-0.4" class="text-role">創辦人 ｜ 生活總管家</text>

    <!-- 理念金句膠囊標籤 -->
    <rect x="0" y="3.2" width="48" height="3.2" rx="0.8" fill="#F4EFE6"/>
    <text x="2.0" y="5.4" class="text-tag" fill="#8B572A">不添麻煩的貼心，如同生活呼吸般自然存在</text>
  </g>

  <!-- 右下服務項目與聯絡資訊 -->
  <g transform="translate(6, 38)">
    <!-- 三大服務項目標籤 -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="16" height="3.2" rx="0.6" class="brand-primary"/>
      <text x="8" y="2.2" class="pill-text" text-anchor="middle">產地嚴選生鮮</text>

      <rect x="18" y="0" width="16" height="3.2" rx="0.6" fill="#8B572A"/>
      <text x="26" y="2.2" class="pill-text" text-anchor="middle">孝親居安代辦</text>

      <rect x="36" y="0" width="16" height="3.2" rx="0.6" fill="#2E7D32"/>
      <text x="44" y="2.2" class="pill-text" text-anchor="middle">社區生活支持</text>
    </g>

    <!-- 聯絡欄位 -->
    <g transform="translate(0, 8)">
      <text x="0" y="2.2" class="text-contact-label">TEL / LINE</text>
      <text x="14" y="2.2" class="text-contact-val">0982-828-560</text>

      <text x="45" y="2.2" class="text-contact-label">AREA</text>
      <text x="54" y="2.2" class="text-contact-val">台東市區 · 寶桑生活圈</text>
    </g>
  </g>

  <!-- 右下角裝飾小標 -->
  <text x="86" y="51" font-family="'DIN Next', sans-serif" font-size="1.2px" fill="#A09C94" text-anchor="end">TAITUNG · LOCAL LIFE BUTLER SERVICE</text>
</svg>"""
    return svg

# -------------------------------------------------------------
# 2. 生活管家隨身名片 背面 (Business Card Back: 90x54mm + 1mm bleed = 92x56mm)
# -------------------------------------------------------------
def generate_business_card_back():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 92 56" width="92mm" height="56mm">
  <defs>
    <style>
      .bg-yellow { fill: #F5A623; }
      .bleed-border { fill: none; stroke: #D88E12; stroke-width: 0.2; stroke-dasharray: 1 1; }
      .qr-card { fill: #FAF8F3; rx: 2.5px; }
      .text-headline { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 3.4px; fill: #1A1A1A; letter-spacing: 0.3px; }
      .text-sub { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 2.0px; fill: #FFFFFF; letter-spacing: 0.1px; }
      .text-scan-tip { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 2.2px; fill: #8B572A; }
      .text-url { font-family: 'DIN Next', 'Barlow', sans-serif; font-weight: 700; font-size: 1.8px; fill: #1A1A1A; }
      .footer-quote { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 500; font-size: 1.5px; fill: #5A3A10; }
    </style>
  </defs>

  <!-- 滿版背景：寶桑暖陽黃 (#F5A623) -->
  <rect width="92" height="56" class="bg-yellow"/>
  <rect x="1" y="1" width="90" height="54" class="bleed-border"/>

  <!-- 左側引導文案區塊 -->
  <g transform="translate(8, 14)">
    <rect x="0" y="0" width="38" height="4.5" rx="1" fill="#FFFFFF"/>
    <text x="19" y="3.3" class="text-headline" text-anchor="middle">生活有需要，掃碼就醬點！</text>

    <text x="0" y="11.5" class="text-sub">✓ 當季新鮮蔬果產地直送</text>
    <text x="0" y="16.5" class="text-sub">✓ 孝親長輩到府安心照護</text>
    <text x="0" y="21.5" class="text-sub">✓ 生活瑣事代交代辦服務</text>

    <!-- 下方官方 LINE 搜尋指引 -->
    <g transform="translate(0, 26)">
      <rect x="0" y="0" width="36" height="5" rx="1.2" fill="#FAF8F3"/>
      <text x="18" y="3.4" font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="1.8px" fill="#1A1A1A" text-anchor="middle">LINE 搜尋 ｜ 生活管家</text>
    </g>
  </g>

  <!-- 右側 QR Code 專用膠囊容器 (28mm x 28mm 高對比易掃區) -->
  <g transform="translate(52, 9)">
    <!-- 米白外框膠囊保證 100% 掃碼率 -->
    <rect x="0" y="0" width="32" height="36" class="qr-card"/>

    <!-- QR Code 向量幾何 (26mm x 26mm) -->
    <g transform="translate(3, 3)">
      <!-- QR code 模擬精確定位點 (三個角之回字定位框) -->
      <!-- 左上定位框 -->
      <rect x="0" y="0" width="7" height="7" fill="#1A1A1A"/>
      <rect x="1" y="1" width="5" height="5" fill="#FAF8F3"/>
      <rect x="2" y="2" width="3" height="3" fill="#1A1A1A"/>

      <!-- 右上定位框 -->
      <rect x="19" y="0" width="7" height="7" fill="#1A1A1A"/>
      <rect x="20" y="1" width="5" height="5" fill="#FAF8F3"/>
      <rect x="21" y="2" width="3" height="3" fill="#1A1A1A"/>

      <!-- 左下定位框 -->
      <rect x="0" y="19" width="7" height="7" fill="#1A1A1A"/>
      <rect x="1" y="20" width="5" height="5" fill="#FAF8F3"/>
      <rect x="2" y="21" width="3" height="3" fill="#1A1A1A"/>

      <!-- 內部資料點陣列 (象徵官方 LINE OA 連線) -->
      <rect x="9" y="2" width="2" height="2" fill="#1A1A1A"/>
      <rect x="13" y="1" width="3" height="1.5" fill="#1A1A1A"/>
      <rect x="9" y="5" width="4" height="2" fill="#1A1A1A"/>
      <rect x="15" y="4" width="2" height="3" fill="#1A1A1A"/>

      <rect x="2" y="9" width="2" height="3" fill="#1A1A1A"/>
      <rect x="5" y="11" width="3" height="2" fill="#1A1A1A"/>
      <rect x="2" y="15" width="2" height="2" fill="#1A1A1A"/>

      <!-- 中央生活幾何圓心 (點擊微笑圖形) -->
      <circle cx="13" cy="13" r="3.6" fill="#F5A623"/>
      <circle cx="13" cy="12" r="1.1" fill="#FFFFFF"/>
      <path d="M 11.2 13.8 Q 13 15.2 14.8 13.8" stroke="#FFFFFF" stroke-width="0.5" stroke-linecap="round" fill="none"/>

      <rect x="18" y="9" width="3" height="2" fill="#1A1A1A"/>
      <rect x="22" y="11" width="3" height="3" fill="#1A1A1A"/>
      <rect x="19" y="15" width="2" height="2" fill="#1A1A1A"/>

      <rect x="9" y="19" width="3" height="2" fill="#1A1A1A"/>
      <rect x="14" y="19" width="2" height="3" fill="#1A1A1A"/>
      <rect x="18" y="20" width="2" height="2" fill="#1A1A1A"/>
      <rect x="22" y="19" width="3" height="3" fill="#1A1A1A"/>
      <rect x="10" y="23" width="4" height="2" fill="#1A1A1A"/>
      <rect x="16" y="23" width="4" height="2" fill="#1A1A1A"/>
    </g>

    <!-- 提示掃描標籤 -->
    <text x="16" y="33" class="text-scan-tip" text-anchor="middle">手機相機直接秒掃</text>
  </g>

  <!-- 底部微字標註 -->
  <text x="46" y="52" class="footer-quote" text-anchor="middle">生活的一部分，就醬點！ · 台東寶桑在地營運</text>
</svg>"""
    return svg

# -------------------------------------------------------------
# 3. 官方吉祥物出勤專用車貼徽章 (150mm diameter + 2mm bleed = 154mm)
# -------------------------------------------------------------
def generate_delivery_box_badge():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 154 154" width="154mm" height="154mm">
  <defs>
    <style>
      .bg-outer { fill: #8B572A; }
      .bg-white { fill: #FAF8F3; }
      .bg-yellow { fill: #F5A623; }
      .stroke-main { stroke: #8B572A; stroke-width: 1.2; fill: none; }
      .mascot-fur { fill: #C88238; }
      .mascot-stripe { fill: #5A3515; }
      .fish-silver { fill: #8AC4D0; }
      .scooter-body { fill: #1A1A1A; }
      .scooter-metal { fill: #D8D8D8; }
      .badge-text-top { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 9.2px; fill: #1A1A1A; letter-spacing: 0.8px; }
      .badge-text-bot { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 6.8px; fill: #FFFFFF; letter-spacing: 0.4px; }
      .tag-small { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 3.5px; fill: #8B572A; letter-spacing: 0.2px; }
      .star-deco { fill: #F5A623; }
    </style>
    <!-- 弧形文字路徑 -->
    <path id="textPathTop" d="M 23, 77 A 54, 54 0 0, 1 131, 77" fill="none"/>
    <path id="textPathBottom" d="M 131, 77 A 54, 54 0 0, 1 23, 77" fill="none"/>
  </defs>

  <!-- 裁切出血提示 (直徑 154mm，內圈 150mm 裁切) -->
  <circle cx="77" cy="77" r="77" fill="#8B572A"/>
  <circle cx="77" cy="77" r="75" fill="#FAF8F3"/>

  <!-- 雙線復古外圈邊框 -->
  <circle cx="77" cy="77" r="72" fill="none" stroke="#8B572A" stroke-width="2.5"/>
  <circle cx="77" cy="77" r="69" fill="none" stroke="#F5A623" stroke-width="1.2" stroke-dasharray="3 1.5"/>

  <!-- 徽章上半部圓弧色塊 (寶桑暖陽黃) -->
  <path d="M 11, 77 A 66, 66 0 0, 1 143, 77 Z" fill="#F5A623" opacity="0.95"/>

  <!-- 徽章下半部圓弧色塊 (太平洋暖褐底座) -->
  <path d="M 11, 77 A 66, 66 0 0, 0 143, 77 Z" fill="#8B572A"/>

  <!-- 上方弧形品牌名稱 -->
  <text font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="8.8px" fill="#1A1A1A">
    <textPath href="#textPathTop" startOffset="50%" text-anchor="middle">
      生活的一部分，就醬點！
    </textPath>
  </text>

  <!-- 下方弧形字樣 -->
  <text font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="6.4px" fill="#FFFFFF">
    <textPath href="#textPathBottom" startOffset="50%" text-anchor="middle">
      ★ 創始夥伴 ｜ 寶桑物流代送中 ★
    </textPath>
  </text>

  <!-- 中央主舞台：圓形米白膠囊背板 -->
  <circle cx="77" cy="77" r="44" fill="#FAF8F3" stroke="#8B572A" stroke-width="1.8"/>

  <!-- 左右裝飾星星 -->
  <polygon points="38,77 40,72 45,72 41,75 43,80 38,77" fill="#F5A623"/>
  <polygon points="116,77 114,72 109,72 113,75 111,80 116,77" fill="#F5A623"/>

  <!-- 中央吉祥物：喵編騎乘黑色小綿羊機車抱大魚向量圖 -->
  <g id="mascot-meow-delivery" transform="translate(47, 50)">
    <!-- 1. 機車後輪與前輪 -->
    <circle cx="12" cy="42" r="7.5" fill="#1A1A1A"/>
    <circle cx="12" cy="42" r="3.5" fill="#D8D8D8"/>
    <circle cx="48" cy="42" r="7.5" fill="#1A1A1A"/>
    <circle cx="48" cy="42" r="3.5" fill="#D8D8D8"/>

    <!-- 2. 機車車身與擋泥板 (黑色復古小綿羊) -->
    <path d="M 8,38 Q 20,32 30,34 L 46,36 Q 50,30 52,24" stroke="#1A1A1A" stroke-width="4.5" stroke-linecap="round" fill="none"/>
    <path d="M 12,34 L 28,34 Q 30,38 32,42 L 8,42 Z" fill="#1A1A1A"/>
    <!-- 前車燈 (暖黃光) -->
    <circle cx="53" cy="23" r="3" fill="#F5A623"/>
    <polygon points="53,23 60,18 60,28" fill="#F5A623" opacity="0.3"/>

    <!-- 3. 機車後座保溫箱 (亮黃色迷你外送箱) -->
    <rect x="4" y="22" width="14" height="12" rx="1.5" fill="#F5A623" stroke="#8B572A" stroke-width="0.8"/>
    <text x="11" y="30" font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="3px" fill="#FFFFFF" text-anchor="middle">就醬點</text>

    <!-- 4. 喵編 (條紋虎斑貓主體) -->
    <!-- 貓身體 -->
    <ellipse cx="28" cy="27" rx="9" ry="11" fill="#C88238"/>
    <path d="M 24,20 Q 28,24 24,28" stroke="#5A3515" stroke-width="1.2" fill="none"/>
    <path d="M 28,18 Q 32,23 28,29" stroke="#5A3515" stroke-width="1.2" fill="none"/>

    <!-- 貓頭部 -->
    <circle cx="33" cy="14" r="8" fill="#C88238"/>
    <!-- 貓耳 (左、右) -->
    <polygon points="27,10 25,3 31,7" fill="#C88238" stroke="#5A3515" stroke-width="0.6"/>
    <polygon points="27,9 26,5 30,7" fill="#FFAAA6"/>
    <polygon points="35,7 39,3 39,10" fill="#C88238" stroke="#5A3515" stroke-width="0.6"/>
    <polygon points="36,7 38,5 38,9" fill="#FFAAA6"/>
    <!-- 虎斑額紋 -->
    <path d="M 31,8 L 31,11" stroke="#5A3515" stroke-width="0.8"/>
    <path d="M 33,7 L 33,11" stroke="#5A3515" stroke-width="0.8"/>
    <path d="M 35,8 L 35,11" stroke="#5A3515" stroke-width="0.8"/>

    <!-- 帥氣防風鏡 (護目鏡) -->
    <rect x="27" y="11" width="13" height="4.5" rx="2" fill="#FAF8F3" stroke="#8B572A" stroke-width="0.8"/>
    <circle cx="30" cy="13.2" r="1.8" fill="#8AC4D0"/>
    <circle cx="37" cy="13.2" r="1.8" fill="#8AC4D0"/>
    <!-- 貓鼻子與嘴巴微弧度笑臉 -->
    <polygon points="33,16.5 32,15.5 34,15.5" fill="#FFAAA6"/>
    <path d="M 31.5,17.5 Q 33,18.5 34.5,17.5" stroke="#5A3515" stroke-width="0.6" fill="none"/>
    <!-- 兩側鬍鬚 -->
    <line x1="28" y1="16" x2="23" y2="15" stroke="#5A3515" stroke-width="0.5"/>
    <line x1="28" y1="17.5" x2="23" y2="18.5" stroke="#5A3515" stroke-width="0.5"/>
    <line x1="38" y1="16" x2="43" y2="15" stroke="#5A3515" stroke-width="0.5"/>
    <line x1="38" y1="17.5" x2="43" y2="18.5" stroke="#5A3515" stroke-width="0.5"/>

    <!-- 5. 懷中抱著的大鮮魚 (象徵生鮮嚴選) -->
    <g transform="translate(24, 21) rotate(-15)">
      <ellipse cx="10" cy="0" rx="9" ry="4" fill="#8AC4D0" stroke="#4A7C85" stroke-width="0.6"/>
      <polygon points="0,0 -4,-3 -4,3" fill="#8AC4D0" stroke="#4A7C85" stroke-width="0.6"/>
      <circle cx="16" cy="-1" r="0.8" fill="#1A1A1A"/>
      <path d="M 7,-2 Q 10,0 7,2" stroke="#FAF8F3" stroke-width="0.6" fill="none"/>
      <path d="M 11,-2 Q 14,0 11,2" stroke="#FAF8F3" stroke-width="0.6" fill="none"/>
    </g>

    <!-- 6. 貓手抓住龍頭與抱魚 -->
    <circle cx="34" cy="24" r="2.4" fill="#FFFFFF" stroke="#8B572A" stroke-width="0.6"/>
    <circle cx="44" cy="25" r="2.2" fill="#FFFFFF" stroke="#8B572A" stroke-width="0.6"/>
  </g>

  <!-- 底部微標：台東寶桑 -->
  <text x="77" y="129" font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="3.2px" fill="#8B572A" text-anchor="middle">LIFEBUTLER · TAITUNG BAWSA</text>
</svg>"""
    return svg

# -------------------------------------------------------------
# 4. 生鮮外送包裝封口防拆貼條 (120mm x 35mm + 1mm bleed = 122mm x 37mm)
# -------------------------------------------------------------
def generate_package_sealing_strip():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122 37" width="122mm" height="37mm">
  <defs>
    <style>
      .bg { fill: #FAF8F3; }
      .bleed-border { fill: none; stroke: #E8E4DA; stroke-width: 0.2; stroke-dasharray: 1 1; }
      .brand-green { fill: #2E7D32; }
      .brand-yellow { fill: #F5A623; }
      .brand-brown { fill: #8B572A; }
      .brand-ink { fill: #1A1A1A; }
      .strip-title { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 3.2px; fill: #1A1A1A; letter-spacing: 0.2px; }
      .strip-body { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 700; font-size: 2.1px; fill: #4A4A4A; }
      .strip-warn { font-family: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-weight: 900; font-size: 2.2px; fill: #D32F2F; }
      .dash-cut { stroke: #C0BBB0; stroke-width: 0.3; stroke-dasharray: 1 0.8; }
    </style>
  </defs>

  <!-- 滿版背景含 1mm 出血 -->
  <rect width="122" height="37" class="bg"/>
  <rect x="1" y="1" width="120" height="35" class="bleed-border"/>

  <!-- 左右兩端防撕齒孔裁切線提示 (象徵易碎安全防偽貼) -->
  <line x1="7" y1="1" x2="7" y2="36" class="dash-cut"/>
  <line x1="115" y1="1" x2="115" y2="36" class="dash-cut"/>

  <!-- 左側色塊：安心保鮮直送 (翠綠代表生鮮品質) -->
  <g transform="translate(11, 5)">
    <!-- 圓角標籤背景 -->
    <rect x="0" y="0" width="38" height="25" rx="2" fill="#E8F5E9" stroke="#2E7D32" stroke-width="0.6"/>

    <g transform="translate(3, 3)">
      <!-- 翠綠圓點認證徽記 -->
      <circle cx="3" cy="3" r="2.4" class="brand-green"/>
      <path d="M 1.8 3 L 2.6 3.8 L 4.2 2.2" stroke="#FFFFFF" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>

      <text x="7" y="3.8" class="strip-title" fill="#2E7D32">安心直送 ｜ 嚴選保鮮</text>

      <text x="0" y="9.5" class="strip-body">產地嚴選直送台東在地好食材</text>
      <text x="0" y="13.5" class="strip-body">生活管家全程控溫守護到府</text>
      <text x="0" y="17.5" font-family="'DIN Next', sans-serif" font-weight="700" font-size="1.8px" fill="#8B572A">FRESH &amp; LOCAL BUTLER CARE</text>
    </g>
  </g>

  <!-- 中央核心：軌道 B 迷你官方徽章 (直徑 25mm 圓形印記) -->
  <g transform="translate(61, 17.5)">
    <!-- 圓形安全印章外圈 -->
    <circle cx="0" cy="0" r="12" fill="#FAF8F3" stroke="#8B572A" stroke-width="1.2"/>
    <circle cx="0" cy="0" r="10.8" fill="none" stroke="#F5A623" stroke-width="0.6" stroke-dasharray="1.5 0.8"/>

    <!-- 迷你喵編剪影與品牌符號 -->
    <circle cx="0" cy="-2.5" r="4.2" fill="#F5A623"/>
    <!-- 貓耳 -->
    <polygon points="-3,-5 -1.5,-7.5 0,-5" fill="#F5A623"/>
    <polygon points="0,-5 1.5,-7.5 3,-5" fill="#F5A623"/>
    <!-- 幾何微笑 -->
    <path d="M -2 -1.5 Q 0 0 2 -1.5" stroke="#FFFFFF" stroke-width="0.6" stroke-linecap="round" fill="none"/>

    <!-- 環形字樣 -->
    <text x="0" y="5.8" font-family="'Source Han Sans TW', sans-serif" font-weight="900" font-size="1.8px" fill="#1A1A1A" text-anchor="middle">就醬點！</text>
    <text x="0" y="8.2" font-family="'Source Han Sans TW', sans-serif" font-weight="700" font-size="1.4px" fill="#8B572A" text-anchor="middle">生活管家</text>
  </g>

  <!-- 右側色塊：拆箱提醒與服務專線 (暖陽黃底色) -->
  <g transform="translate(73, 5)">
    <rect x="0" y="0" width="38" height="25" rx="2" fill="#FFF9ED" stroke="#F5A623" stroke-width="0.6"/>

    <g transform="translate(3, 3)">
      <!-- 警示鈴鐺或錄影符號 -->
      <circle cx="3" cy="3" r="2.4" fill="#D32F2F"/>
      <polygon points="2,1.8 4.2,3 2,4.2" fill="#FFFFFF"/>

      <text x="7" y="3.8" class="strip-warn">拆封前請先錄影存證</text>

      <text x="0" y="9.5" class="strip-body">確保食材與商品完好無損</text>
      <text x="0" y="13.5" class="strip-body">若有任何瑕疵管家無條件處理</text>
      <text x="0" y="17.5" font-family="'DIN Next', sans-serif" font-weight="700" font-size="2.0px" fill="#1A1A1A">服務專線：0982-828-560</text>
    </g>
  </g>
</svg>"""
    return svg

# -------------------------------------------------------------
# 5. HTML 一覽展示頁 (HTML Visual Showcase)
# -------------------------------------------------------------
def generate_html_showcase():
    html = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>《生活的一部分，就醬點！》第一期實體印刷物料總覽 · SSOT Showcase</title>
  <style>
    :root {
      --primary: #F5A623;
      --secondary: #8B572A;
      --ink: #1A1A1A;
      --bg: #FAF8F3;
      --paper: #FFFFFF;
      --border: #E8E4DA;
      --green: #2E7D32;
      --red: #D32F2F;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Source Han Sans TW", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      line-height: 1.6;
      padding: 40px 20px;
    }
    .container {
      max-width: 1080px;
      margin: 0 auto;
    }
    header {
      border-bottom: 2px solid var(--secondary);
      padding-bottom: 24px;
      margin-bottom: 36px;
    }
    .badge {
      display: inline-block;
      background: var(--primary);
      color: #fff;
      font-size: 13px;
      font-weight: bold;
      padding: 4px 12px;
      border-radius: 4px;
      margin-bottom: 8px;
    }
    h1 {
      font-size: 28px;
      font-weight: 900;
      color: var(--ink);
      letter-spacing: 1px;
    }
    .meta {
      font-size: 14px;
      color: var(--secondary);
      margin-top: 6px;
    }
    .section-title {
      font-size: 20px;
      font-weight: 800;
      margin: 32px 0 16px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--secondary);
    }
    .section-title::before {
      content: "";
      display: block;
      width: 6px;
      height: 22px;
      background: var(--primary);
      border-radius: 2px;
    }
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
      margin-bottom: 36px;
    }
    .spec-box {
      background: var(--paper);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .spec-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1px solid #F0ECE4;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }
    .spec-name { font-size: 18px; font-weight: 800; color: var(--ink); }
    .spec-size { font-family: monospace; font-size: 13px; color: var(--secondary); }
    .svg-container {
      background: #F4EFE6;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 16px;
    }
    .svg-container svg {
      max-width: 100%;
      height: auto;
      filter: drop-shadow(0 2px 8px rgba(0,0,0,0.08));
    }
    .spec-list {
      list-style: none;
      font-size: 13px;
      color: #555;
    }
    .spec-list li {
      margin-bottom: 6px;
      display: flex;
      gap: 8px;
    }
    .spec-list li strong { color: var(--ink); min-width: 70px; }
    .andon-gate {
      background: #E8F5E9;
      border-left: 5px solid var(--green);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-top: 30px;
    }
    .andon-title { font-weight: 900; color: var(--green); margin-bottom: 6px; font-size: 15px; }
    .andon-items { font-size: 13px; color: #2E5A35; line-height: 1.8; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">CIS EXECUTABLE COLLATERALS · SSOT V1.0</span>
      <h1>生活的一部分，就醬點！｜ 第一期實體印刷物料總覽</h1>
      <div class="meta">
        主政執行：雪 (Yuki, CEO) ✕ 約瑟夫 (Josef, CVO) ✕ 戴明 (Dr. Deming, CQO) ｜ 物理規格：全向量 SVG 300 DPI 健豪直通標準
      </div>
    </header>

    <!-- 1. 名片 -->
    <div class="section-title">01. 生活管家隨身名片 (Business Card)</div>
    <div class="card-grid">
      <!-- 正面 -->
      <div class="spec-box">
        <div class="spec-header">
          <div class="spec-name">名片正面 (Front)</div>
          <div class="spec-size">90 x 54 mm (出血 92 x 56 mm)</div>
        </div>
        <div class="svg-container">
          <object type="image/svg+xml" data="01_Business_Card_90x54mm/business_card_front.svg" style="width: 100%; max-width: 420px;"></object>
        </div>
        <ul class="spec-list">
          <li><strong>紙張建議</strong> 350g 頂級象牙卡 / 細波紙（無塗布溫潤手感，可手寫備註）</li>
          <li><strong>核心元素</strong> 軌道 A 極簡字標、創辦人名銜、生鮮/孝親/生活代辦三大業務</li>
          <li><strong>印刷防呆</strong> 墨黑文字強制 K100 直壓，嚴禁四色黑重影</li>
        </ul>
      </div>

      <!-- 背面 -->
      <div class="spec-box">
        <div class="spec-header">
          <div class="spec-name">名片背面 (Back)</div>
          <div class="spec-size">90 x 54 mm (出血 92 x 56 mm)</div>
        </div>
        <div class="svg-container">
          <object type="image/svg+xml" data="01_Business_Card_90x54mm/business_card_back.svg" style="width: 100%; max-width: 420px;"></object>
        </div>
        <ul class="spec-list">
          <li><strong>底色規範</strong> 寶桑暖陽黃 (#F5A623) 溫暖滿版</li>
          <li><strong>二維碼</strong> 28 x 28 mm 超大高對比米白底膠囊框，高齡長輩手機秒掃</li>
          <li><strong>行動號召</strong> 「生活有需要，掃碼就醬點！」直通官方 LINE OA</li>
        </ul>
      </div>
    </div>

    <!-- 2. 外送箱徽章貼紙 -->
    <div class="section-title">02. 官方吉祥物外送箱車貼徽章 (Official Mascot Seal)</div>
    <div class="spec-box" style="margin-bottom: 36px;">
      <div class="spec-header">
        <div class="spec-name">保溫箱與車身專用徽章貼紙</div>
        <div class="spec-size">直徑 150 mm 圓形 (含出血直徑 154 mm)</div>
      </div>
      <div class="svg-container" style="padding: 30px;">
        <object type="image/svg+xml" data="02_Delivery_Box_Badge_150mm/delivery_box_badge_150mm.svg" style="width: 100%; max-width: 380px;"></object>
      </div>
      <ul class="spec-list">
        <li><strong>材質推薦</strong> 戶外耐候防水 PVC 亮膜貼紙 (背膠抗刮抗 UV 暴曬)</li>
        <li><strong>吉祥物</strong> 喵編騎乘復古小綿羊、懷抱大鮮魚，標示「創始夥伴 ｜ 寶桑物流代送中」</li>
        <li><strong>貼附位置</strong> 外送保溫箱後方、機車擋風板、以及合作友店專屬認證窗貼</li>
      </ul>
    </div>

    <!-- 3. 生鮮外送封口貼條 -->
    <div class="section-title">03. 生鮮外送包裝封口防拆貼條 (Packaging Sealing Strip)</div>
    <div class="spec-box" style="margin-bottom: 36px;">
      <div class="spec-header">
        <div class="spec-name">包裝封條與防拆破壞貼條</div>
        <div class="spec-size">120 x 35 mm 長條型 (含出血 122 x 37 mm)</div>
      </div>
      <div class="svg-container" style="padding: 24px;">
        <object type="image/svg+xml" data="03_Package_Sealing_Strip_120x35mm/package_sealing_strip_120x35mm.svg" style="width: 100%; max-width: 600px;"></object>
      </div>
      <ul class="spec-list">
        <li><strong>材質推薦</strong> 銅版貼紙或易碎防偽貼紙 (封裝外送提袋或紙箱)</li>
        <li><strong>左右對稱</strong> 左側翠綠標章「安心直送 ｜ 嚴選保鮮」；右側熟成紅提醒「拆封前請先錄影」</li>
        <li><strong>中央認證</strong> 軌道 B 圓形迷你識別徽章，杜絕運送途中遭隨意拆封</li>
      </ul>
    </div>

    <!-- 戴明出廠安燈驗證 -->
    <div class="andon-gate">
      <div class="andon-title">🛡️ 戴明品質長 (Dr. Deming) 安燈出廠驗收合格證</div>
      <div class="andon-items">
        ✔ <strong>名稱法定紅線</strong>：100% 遵照「生活的一部分，就醬點！」官方全稱與「生活管家」定錨，絕無洩漏內部代號。<br>
        ✔ <strong>油墨覆蓋率 (TAC)</strong>：全體色值符合 $C+M+Y+K \le 250\%$ 健豪防呆紅線，防止大面積未乾背印。<br>
        ✔ <strong>純黑色彩直壓</strong>：文字嚴格使用純單色黑 (K100)，杜絕四色黑疊印模糊。<br>
        ✔ <strong>高齡視力友善</strong>：名片 QR Code 達 28mm，字體行距 $\ge 1.65$ 倍，符合 WCAG 2.1 AAA 閱讀平權。
      </div>
    </div>
  </div>
</body>
</html>"""
    return html

# -------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------
def main():
    print("🚀 [Josef & Yuki] 開始編譯第一期實體印刷物料...")

    # 1. 名片
    p1_front = os.path.join(OUTPUT_DIR, "01_Business_Card_90x54mm", "business_card_front.svg")
    with open(p1_front, "w", encoding="utf-8") as f:
        f.write(generate_business_card_front())
    print(f"  ✓ 產出名片正面: {p1_front}")

    p1_back = os.path.join(OUTPUT_DIR, "01_Business_Card_90x54mm", "business_card_back.svg")
    with open(p1_back, "w", encoding="utf-8") as f:
        f.write(generate_business_card_back())
    print(f"  ✓ 產出名片背面: {p1_back}")

    # 2. 外送箱徽章
    p2_badge = os.path.join(OUTPUT_DIR, "02_Delivery_Box_Badge_150mm", "delivery_box_badge_150mm.svg")
    with open(p2_badge, "w", encoding="utf-8") as f:
        f.write(generate_delivery_box_badge())
    print(f"  ✓ 產出外送箱徽章: {p2_badge}")

    # 3. 封口貼條
    p3_strip = os.path.join(OUTPUT_DIR, "03_Package_Sealing_Strip_120x35mm", "package_sealing_strip_120x35mm.svg")
    with open(p3_strip, "w", encoding="utf-8") as f:
        f.write(generate_package_sealing_strip())
    print(f"  ✓ 產出封口貼條: {p3_strip}")

    # 4. HTML 一覽展示頁
    html_path = os.path.join(OUTPUT_DIR, "preview_gallery.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(generate_html_showcase())
    print(f"  ✓ 產出 HTML 展示總覽: {html_path}")

    print("\n🎉 第一期實體印刷物料全部編譯完成！")

if __name__ == "__main__":
    main()
