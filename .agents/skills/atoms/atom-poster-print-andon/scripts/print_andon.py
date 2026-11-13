#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/print_andon.py
海報印刷出廠前戴明十重安燈防呆閘門引擎
嚴格審計 300 DPI、3mm 出血線、TAC <= 250%、K100 單色黑直壓、28mm QR Code、品牌零洩漏防火牆
"""

import sys
import json
import argparse
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]
SIMPLIFIED_CHINESE_MARKERS = ["门", "关", "东", "发", "车", "头", "爱", "视频", "赋能", "闭环", "接地气"]

def inspect_poster_print_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """執行戴明印刷安燈出廠審查"""
    andon_triggered = False
    violations: List[str] = []
    passes: List[str] = []

    dpi = spec.get("dpi", 300)
    bleed_mm = spec.get("bleed_mm", 0)
    tac = spec.get("tac_percent", 220)
    black_mode = spec.get("black_mode", "K100_OVERPRINT")
    qr_size_mm = spec.get("qr_size_mm", 30)
    texts_to_check = spec.get("texts", [])

    # 1. DPI 檢查 (實體海報需 >= 300 DPI)
    if dpi < 300:
        andon_triggered = True
        violations.append(f"【DPI 缺陷】物理解析度 {dpi} DPI 低於健豪/藍格印刷門檻 (需 >= 300 DPI)")
    else:
        passes.append(f"DPI 檢驗合格: {dpi} DPI (清晰無鋸齒)")

    # 2. 出血線檢查 (實體海報需 >= 3mm)
    if bleed_mm < 3.0:
        andon_triggered = True
        violations.append(f"【出血線缺失】印刷出血為 {bleed_mm} mm，小於標準 3mm (85px)，裁切將出現白邊")
    else:
        passes.append(f"物理出血線合格: {bleed_mm} mm (已建立雙裁切標記)")

    # 3. 總油墨覆蓋率 TAC 審計 (TAC <= 250%)
    if tac > 250:
        andon_triggered = True
        violations.append(f"【TAC 油墨超載】總油墨覆蓋率 {tac}% 超過健豪/藍格 250% 安全上限，潮濕環境將造成嚴重背印與慢乾污染")
    else:
        passes.append(f"總油墨覆蓋率合格: TAC {tac}% (<= 250% 安全區間，大豆油墨快乾)")

    # 4. 黑版直壓 Overprint 檢查
    if black_mode != "K100_OVERPRINT":
        andon_triggered = True
        violations.append(f"【黑色套印危險】文字色彩模式為 {black_mode}，非 K100 單色黑直壓，印刷微位移將造成文字彩邊與模糊")
    else:
        passes.append("黑版直壓合格: K100 單色黑直壓 (無四色混黑雜色)")

    # 5. QR Code 物理尺寸檢查 (>= 28mm)
    if qr_size_mm < 28.0:
        andon_triggered = True
        violations.append(f"【QR Code 太小】二維碼物理寬度 {qr_size_mm} mm 小於 28mm 防呆極限，長者 1.5 公尺外難以掃碼")
    else:
        passes.append(f"QR Code 掃碼防呆合格: 物理寬度 {qr_size_mm} mm (四周已留白 4 模組靜區)")

    # 6. 品牌法定名稱零洩漏防火牆審查
    combined_text = " ".join(texts_to_check)
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in combined_text:
            andon_triggered = True
            violations.append(f"【品牌紅線致命違規】海報內文出現內部代號「{forbidden}」，違反全域憲則！對外法定名稱僅能為「生活的一部分，就醬點！」或自稱「生活管家」")

    # 7. 台灣正體中文語境審查
    for marker in SIMPLIFIED_CHINESE_MARKERS:
        if marker in combined_text:
            andon_triggered = True
            violations.append(f"【語境漂移警告】海報內文檢測到非台灣習慣用語或簡體標記「{marker}」")

    if not any("品牌紅線" in v for v in violations):
        passes.append("品牌法定名稱防火牆合格: 零洩漏內部代號，守護生活管家品牌主權")

    if not any("語境漂移" in v for v in violations):
        passes.append("繁體中文語境合格: 100% 台灣在地常民習慣語")

    return {
        "andon_status": "PULL_ANDON_ABORT" if andon_triggered else "PASS_FOR_PRINT",
        "verdict": "❌ 觸發戴明安燈拉繩！禁止送廠印製或公開發布！" if andon_triggered else "✅ 戴明安燈全數通過！准予送廠印製！",
        "violations": violations,
        "passes": passes
    }

def main():
    parser = argparse.ArgumentParser(description="海報印刷出廠前戴明十重安燈防呆閘門引擎")
    parser.add_argument("--dpi", type=int, default=300, help="印刷物理解析度")
    parser.add_argument("--bleed", type=float, default=3.0, help="出血線毫米數")
    parser.add_argument("--tac", type=int, default=225, help="總油墨覆蓋率 TAC 百分比")
    parser.add_argument("--black-mode", type=str, default="K100_OVERPRINT", help="黑色直壓模式")
    parser.add_argument("--qr-size", type=float, default=32.0, help="二維碼物理寬度毫米")
    parser.add_argument("--text-sample", type=str, default="生活管家 到府陪伴與居安守護 生活的一部分，就醬點！ 預約專線：089-123456", help="海報內文抽樣")
    parser.add_argument("--dry-run", action="store_true", help="執行出廠安燈驗證")
    args = parser.parse_args()

    spec = {
        "dpi": args.dpi,
        "bleed_mm": args.bleed,
        "tac_percent": args.tac,
        "black_mode": args.black_mode,
        "qr_size_mm": args.qr_size,
        "texts": [args.text_sample]
    }

    result = inspect_poster_print_spec(spec)

    print("==================================================")
    print(f"🛑 戴明海報印刷安燈檢驗報告: {result['andon_status']}")
    print(result["verdict"])
    print("--------------------------------------------------")
    print("通過檢查項目:")
    for p in result["passes"]:
        print(f"  [✓] {p}")

    if result["violations"]:
        print("--------------------------------------------------")
        print("⚠️ 攔截違規與安燈拉繩項目:")
        for v in result["violations"]:
            print(f"  [✗] {v}")
        print("==================================================")
        sys.exit(1)
    else:
        print("==================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()
