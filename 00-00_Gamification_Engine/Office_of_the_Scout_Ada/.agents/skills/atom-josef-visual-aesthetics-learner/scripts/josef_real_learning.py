#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
josef_real_learning.py - 約瑟夫之真實色彩對比稽核引擎
以 WCAG 2.x 相對亮度公式，實際計算色票組合的對比度，並對照高齡友善門檻：
  - 一般內文：>= 7:1 (WCAG AAA)
  - 大字 (>=24px 或粗體 >=18.66px)：>= 4.5:1 (AAA 大字)
預設稽核 atom-taste-hyperlocal-design-system 腳本輸出的風土色票；亦可 --pair 指定任意色組。
所有對比值皆由公式即時算出。
"""

import sys
import os
import json
import argparse
import subprocess
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SKILLS_DIR = os.path.join(SKILLS_DIR, "skills")
TOKENS_SCRIPT = os.path.join(SKILLS_DIR, "atom-taste-hyperlocal-design-system", "scripts",
                             "hyperlocal_design_system.py")
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "josef_contrast_history.jsonl"))
BODY_MIN, LARGE_MIN = 7.0, 4.5


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(hex_color):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def load_palette():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run([sys.executable, TOKENS_SCRIPT, "--export-tokens", "--format", "tailwind"],
                         capture_output=True, env=env, timeout=120)
    return json.loads(out.stdout.decode("utf-8"))["design_tokens"]["colors"]


def audit(pairs):
    rows = []
    for name_fg, fg, name_bg, bg in pairs:
        c = contrast(fg, bg)
        rows.append({
            "fg": f"{name_fg} {fg}", "bg": f"{name_bg} {bg}",
            "contrast": round(c, 2),
            "body_text_AAA_7": c >= BODY_MIN,
            "large_text_4.5": c >= LARGE_MIN,
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="約瑟夫之真實色彩對比稽核引擎")
    ap.add_argument("--audit-palette", action="store_true", help="稽核風土色票所有前景/背景組合")
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"), help="稽核單一色組，例：#d4af37 #0a1128")
    args = ap.parse_args()

    if args.pair:
        pairs = [("fg", args.pair[0], "bg", args.pair[1])]
    elif args.audit_palette:
        pal = load_palette()
        names = list(pal.items())
        pairs = [(a, ha, b, hb) for a, ha in names for b, hb in names if a != b
                 and luminance(ha) > luminance(hb)]
    else:
        ap.print_help()
        return

    rows = audit(pairs)
    body_ok = [r for r in rows if r["body_text_AAA_7"]]
    large_only = [r for r in rows if not r["body_text_AAA_7"] and r["large_text_4.5"]]
    fails = [r for r in rows if not r["large_text_4.5"]]
    report = {
        "status": "CONTRAST_AUDITED",
        "audited_at": datetime.now().isoformat(),
        "pairs": len(rows),
        "pass_body_text_7": len(body_ok),
        "large_text_only": len(large_only),
        "fail_all": len(fails),
        "best": sorted(rows, key=lambda r: r["contrast"], reverse=True)[:5],
        "key_brand_pairs": [r for r in rows if any(k in r["fg"] + r["bg"] for k in ("chishang-gold", "taimali-sunrise-red"))
                            and any(k in r["fg"] + r["bg"] for k in ("kuroshio-deep-blue", "homely-cream-white"))],
        "formula": "WCAG 2.x 相對亮度；(L1+0.05)/(L2+0.05)",
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({k: report[k] for k in ("audited_at", "pairs", "pass_body_text_7",
                                                   "large_text_only", "fail_all")}, ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
