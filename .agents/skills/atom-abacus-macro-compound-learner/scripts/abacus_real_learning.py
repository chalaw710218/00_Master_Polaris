#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
abacus_real_learning.py - 算盤之真實帳本毛利與包冰還原引擎
輸入：您提供的帳本 CSV（--ledger）。欄位（UTF-8，含表頭）：
  item,nominal_cost_per_kg,ice_glaze_pct,sell_price_per_kg,logistics_cost_per_order,orders_per_kg_basis
輸出全部由輸入計算，不內建任何價格：
  真實純肉成本 = nominal_cost / (1 - ice_pct/100)
  每公斤單位物流攤提 = logistics_cost_per_order / orders_per_kg_basis
  毛利率 = (sell - true_cost - logistics_per_kg) / sell
每次執行寫入歷史 (vaults/abacus_margin_history.jsonl)，同一品項多次快照可看毛利趨勢。
門檻 --min-margin 為您指定的參數（預設 15%），並非系統定律。
"""

import sys
import os
import csv
import json
import argparse
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
HISTORY = os.path.normpath(os.path.join(HERE, "..", "vaults", "abacus_margin_history.jsonl"))
REQUIRED = ["item", "nominal_cost_per_kg", "ice_glaze_pct", "sell_price_per_kg",
            "logistics_cost_per_order", "orders_per_kg_basis"]


def analyze_row(r, min_margin):
    nominal = float(r["nominal_cost_per_kg"])
    ice = float(r["ice_glaze_pct"])
    sell = float(r["sell_price_per_kg"])
    logi = float(r["logistics_cost_per_order"])
    basis = float(r["orders_per_kg_basis"])
    if not (0 <= ice < 100):
        raise ValueError("ice_glaze_pct 必須在 [0,100)")
    if sell <= 0 or basis <= 0:
        raise ValueError("sell_price_per_kg 與 orders_per_kg_basis 必須 > 0")
    true_cost = nominal / (1 - ice / 100.0)
    logi_kg = logi / basis
    margin = (sell - true_cost - logi_kg) / sell * 100
    return {
        "item": r["item"],
        "true_meat_cost_per_kg": round(true_cost, 2),
        "water_premium_paid_per_kg": round(true_cost - nominal, 2),
        "logistics_per_kg": round(logi_kg, 2),
        "gross_margin_pct": round(margin, 2),
        "below_min_margin": margin < min_margin,
    }


def previous_margins():
    prev = {}
    if os.path.exists(HISTORY):
        with open(HISTORY, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    for it in rec.get("items", []):
                        prev[it["item"]] = it["gross_margin_pct"]
    return prev


def main():
    ap = argparse.ArgumentParser(description="算盤之真實帳本毛利與包冰還原引擎")
    ap.add_argument("--ledger", help="帳本 CSV 路徑（UTF-8，含表頭）")
    ap.add_argument("--min-margin", type=float, default=15.0, help="警戒毛利率 %%（您指定的參數，預設 15）")
    args = ap.parse_args()
    if not args.ledger:
        ap.print_help()
        return
    if not os.path.exists(args.ledger):
        print(json.dumps({"error": "找不到帳本", "path": args.ledger}, ensure_ascii=False))
        sys.exit(1)
    with open(args.ledger, "r", encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (rd.fieldnames or [])]
        if missing:
            print(json.dumps({"error": "缺少欄位", "missing": missing, "required": REQUIRED}, ensure_ascii=False))
            sys.exit(1)
        rows = list(rd)
    prev = previous_margins()
    items, errors = [], []
    for i, r in enumerate(rows, start=2):
        try:
            it = analyze_row(r, args.min_margin)
            if it["item"] in prev:
                it["margin_change_vs_last_snapshot_pp"] = round(it["gross_margin_pct"] - prev[it["item"]], 2)
            items.append(it)
        except Exception as e:
            errors.append({"csv_line": i, "item": r.get("item"), "error": str(e)})
    report = {
        "status": "LEDGER_ANALYZED",
        "analyzed_at": datetime.now().isoformat(timespec="seconds"),
        "ledger": args.ledger,
        "min_margin_pct": args.min_margin,
        "rows_ok": len(items),
        "rows_error": errors,
        "below_min_margin": [i["item"] for i in items if i["below_min_margin"]],
        "items": items,
    }
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"analyzed_at": report["analyzed_at"], "ledger": args.ledger,
                            "items": [{"item": i["item"], "gross_margin_pct": i["gross_margin_pct"]} for i in items]},
                           ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
