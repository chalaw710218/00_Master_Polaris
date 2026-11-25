#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
senior_accessibility_visuals.py - 約瑟夫高齡視力平權與人因光學視覺引導引擎
版權所有 (c) 2026 極星內閣 - 首席視覺長約瑟夫 (Josef / CVO)
"""

import sys
import json
import argparse

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def audit_senior_accessibility(data: dict) -> dict:
    """審核視覺設計之高齡 CSF 視力平權與人因光學規格"""
    body_font_pt = data.get("body_font_pt", 12.0)
    font_family = data.get("font_family", "Noto Sans TC")
    contrast = data.get("contrast_ratio", 7.0)
    qr_size = data.get("qr_code_size_mm", 28.0)
    thumb_margin = data.get("bottom_thumb_margin_pct", 15)
    is_oblique = data.get("is_street_oblique", False)
    
    violations = []
    score = 100
    
    # 1. 內文字級檢驗 (>= 12pt)
    if body_font_pt < 12.0:
        violations.append(f"內文字級僅 {body_font_pt}pt，低於高齡平權標準 12pt，長輩閱讀極易疲勞！")
        score -= 30
        
    # 2. 字體家族排查 (嚴禁細明體、標楷體)
    banned_fonts = ["ming", "kai", "細明", "新細明", "標楷", "楷書"]
    if any(bf in font_family.lower() for bf in banned_fonts):
        violations.append(f"使用了禁忌字型 '{font_family}'！襯線與筆鋒在長者退化眼中易產生斷筆與光暈！")
        score -= 25
        
    # 3. 對比度檢驗 (>= 7.0:1)
    if contrast < 7.0:
        violations.append(f"色彩對比度僅 {contrast:.1f}:1，低於高齡友善 AAA 標準 7.0:1！嚴禁白底淺灰字！")
        score -= 25
        
    # 4. QR Code 尺寸檢驗 (>= 28mm)
    if qr_size < 28.0:
        violations.append(f"QR Code 物理尺寸僅 {qr_size}mm，低於五十公分秒掃標準 28mm！")
        score -= 15
        
    # 5. 實體拇指避讓盲區 (底部 >= 15%)
    if thumb_margin < 15:
        violations.append(f"底部拇指避讓留白僅 {thumb_margin}%，低於 15% 門禁，拿取時易被指腹遮蔽行動點！")
        score -= 15
        
    # 6. 騎樓斜角透視拉伸判定
    stretch_recommendation = (
        "已套用騎樓 45 度視角字寬預拉伸 118%，對抗行人斜視幾何壓縮！"
        if is_oblique else
        "正向視角排版，無需額外斜向幾何拉伸。"
    )
    
    is_passed = len(violations) == 0
    verdict = (
        "👑 高齡視力平權與人因光學檢驗 100% 通過！長輩看得清楚、行動無障礙！"
        if is_passed else
        f"⚠️ 人因視覺審查未達標！扣至 {max(0, score)} 分，存在 {len(violations)} 項長者閱讀障礙，需立即修正！"
    )

    return {
        "senior_accessibility_score": max(0, score),
        "is_passed": is_passed,
        "violations": violations,
        "optical_metrics": {
            "body_font_pt": body_font_pt,
            "contrast_ratio": contrast,
            "qr_code_size_mm": qr_size,
            "bottom_thumb_margin_pct": f"{thumb_margin}%",
            "street_perspective_status": stretch_recommendation
        },
        "josef_verdict": verdict
    }

def main():
    parser = argparse.ArgumentParser(description="約瑟夫高齡視力平權視覺引導引擎")
    parser.add_argument("--audit-visual", type=str, required=True, help="受檢視覺參數 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.audit_visual)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = audit_senior_accessibility(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
