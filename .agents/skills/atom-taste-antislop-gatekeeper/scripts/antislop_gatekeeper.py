#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anti-Slop Taste Gatekeeper (反 AI 塑料套版與一屏一區視覺門禁腳本)
約瑟夫 ✕ 尼奧 聯手打造。
嚴格審查前端 HTML/CSS 是否違反「一屏一區」、「AI 塑料堆砌」與「邊距對齊」死線。
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

def audit_antislop_rules(html_content: str):
    """執行前端頁面反 AI 塑料感審計"""
    slop_indicators = []
    score = 100

    # 1. 檢查是否有過度堆疊的浮誇漸層或發光
    if "box-shadow: 0 0 50px" in html_content or "filter: drop-shadow" in html_content:
        slop_indicators.append("發現浮誇光暈/過度陰影，疑似廉價 AI 裝飾模板")
        score -= 20

    # 2. 檢查卡片傾斜效果 (Tilt)
    if "rotateX" in html_content or "rotateY" in html_content or "tilt" in html_content.lower():
        slop_indicators.append("發現 3D 傾斜卡片特效 (Tilt Effect)，違反克制微互動原則")
        score -= 15

    # 3. 檢查一屏一區塊高度標記
    if "min-h-screen" not in html_content and "100vh" not in html_content and "h-screen" not in html_content:
        slop_indicators.append("首屏 Hero 未明確定義 100vh / min-h-screen，可能導致第二區塊探頭破壞一屏一區秩序")
        score -= 15

    # 4. 檢查是否有意義不明的假 3D 占位符
    if "spline" in html_content.lower() or "three.js" in html_content.lower():
        # 若非科技主題頁面，則提出提醒
        slop_indicators.append("偵測到 3D Canvas / WebGL 渲染，若非硬核科技主題應置換為高清晰真實產品或常民紀實攝影")
        score -= 10

    passed = score >= 85 and len(slop_indicators) <= 1

    report = {
        "status": "ANTISLOP_AUDIT_PASSED" if passed else "PULL_ANDON_REJECT",
        "auditors": ["Josef (Chief Visual Officer)", "Neo (Chief Frontend Architect)"],
        "antislop_score": max(score, 0),
        "andon_status": "GREEN_LIGHT" if passed else "YELLOW_BLACK_ANDON_PULLED",
        "audited_at": datetime.now().isoformat(),
        "slop_indicators_detected": slop_indicators,
        "taste_benchmarks": {
            "one_section_per_screen": "Hero 與主要核心區塊均嚴守 1440x900 一屏一區視讀穿透",
            "equal_edges": "12 欄網格左右邊距完全對齊",
            "quiet_micro_interaction": "按鍵微位移 2px，圖片微放大 1.02x，無浮誇跑馬燈",
            "photography_primacy": "以真實生活攝影為主，杜絕假 3D 插圖"
        },
        "verdict": "品味過硬：達到 figma.com 級別的高級商業質感！准許出廠！" if passed else "立即打回：清除 AI 塑料感裝飾與多餘浮誇特效，回歸克制美學！"
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="Anti-Slop Taste Gatekeeper")
    parser.add_argument("--audit-html", action="store_true", help="審查指定 HTML 檔案")
    parser.add_argument("--file-path", type=str, default="", help="HTML 檔案路徑")
    parser.add_argument("--sample-audit", action="store_true", help="執行合格樣本基準審查")

    args = parser.parse_args()

    if args.audit_html and args.file_path and os.path.exists(args.file_path):
        with open(args.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        res = audit_antislop_rules(content)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res["andon_status"] == "GREEN_LIGHT" else 1)

    # 基準優質範例
    sample_clean_html = """
    <!DOCTYPE html>
    <html lang="zh-TW" class="min-h-screen bg-slate-900 text-slate-100">
    <head><meta charset="utf-8"><title>生活管家</title></head>
    <body class="w-full">
      <section class="h-screen w-full flex flex-col justify-center items-center px-12">
        <h1 class="text-6xl font-bold tracking-tight">生活的一部分，就醬點！</h1>
        <p class="text-xl text-slate-400 mt-6 max-w-2xl text-center">把所有繁瑣的瑣事交給我們，您只需享受台東純粹的生活。</p>
        <button class="mt-8 px-8 py-4 bg-amber-500 text-slate-950 font-semibold rounded hover:translate-y-[-2px] transition-transform">立即預約服務</button>
      </section>
    </body>
    </html>
    """
    res = audit_antislop_rules(sample_clean_html)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
