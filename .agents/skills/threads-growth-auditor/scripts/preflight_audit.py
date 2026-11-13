"""第一軌：發布前質量閘門 (Pre-Flight Quality Gate) · 仿生閉環升級版

全面接入影 (Kage) 與泰勒絲 (Taylor) 的真實數據存摺，終結靜態硬編碼與假進化。

用法：
  python preflight_audit.py --file draft.txt [--persona meow|shadow] [--threshold 90]
  python preflight_audit.py --text "草稿內容..."
  echo 草稿 | python preflight_audit.py

退出碼：0 = 通過 (>= threshold 且無致命項)；1 = 打回重寫。
"""
import argparse
import sys
from pathlib import Path

# 確保引用同目錄之 bionic_closed_loop_gatekeeper
try:
    from bionic_closed_loop_gatekeeper import audit_draft, load_bionic_vaults
except ImportError:
    from .bionic_closed_loop_gatekeeper import audit_draft, load_bionic_vaults


def audit(text, persona="meow"):
    """相容舊版介面：回傳 (score, fatal, items)"""
    profile = load_bionic_vaults()
    return audit_draft(text, persona=persona, profile=profile)


def main():
    ap = argparse.ArgumentParser(description="Threads 發布前質量閘門（仿生學習動態閉環版）")
    ap.add_argument("--file")
    ap.add_argument("--text")
    ap.add_argument("--persona", default="meow", choices=["meow", "shadow"])
    ap.add_argument("--threshold", type=int, default=90)
    a = ap.parse_args()

    if a.file:
        text = open(a.file, "r", encoding="utf-8").read()
    elif a.text:
        text = a.text
    else:
        text = sys.stdin.read()

    score, fatal, items = audit(text, a.persona)
    print(f"🏆 發布前審計分數：{score} / 100（門檻 {a.threshold}）")
    for lvl, msg in items:
        print(f"  {lvl} {msg}")
    if fatal or score < a.threshold:
        print("\n🛑 打回重寫：" + ("；".join(fatal) if fatal else f"分數低於門檻 {a.threshold}"))
        sys.exit(1)
    print("\n🟢 通過仿生質量閘門，准予發布。")


if __name__ == "__main__":
    main()

