#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-radar-first-principles: 第一原則解剖與台東抗逆沙盒原子
由首席科技偵察官艾達 (Ada) ✕ 首席品質長戴明 (Dr. Deming) 聯合打造
"""

import sys
import os
import argparse
import re
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HYPE_BUZZWORDS = [
    r"革命性突破",
    r"顛覆性創新",
    r"完全取代人類",
    r"無限算力",
    r"100% 準確率",
    r"降維打擊"
]

def scan_hype_slop(text: str) -> list[str]:
    found = []
    for pat in HYPE_BUZZWORDS:
        if re.search(pat, text):
            found.append(pat)
    return found

def audit_taitung_sandbox(power_watts: float, offline_capable: bool, ip_rating: str) -> dict:
    """
    台東風土抗逆沙盒測試：
    1. 功耗牆 <= 5W
    2. 100% 離線運行能力
    3. 防護等級 >= IP65 (耐太平洋鹽霧與溫泉硫磺)
    """
    tests = {
        "5w_power_wall": {
            "claimed_watts": power_watts,
            "pass": power_watts <= 5.0,
            "desc": "符合微電網/太陽能涓流 5W 功耗牆" if power_watts <= 5.0 else f"超標 ({power_watts}W > 5W)，脫離市電無法孤島生存"
        },
        "30d_offline_island": {
            "pass": offline_capable,
            "desc": "具備 100% 本機端側離線推論能力" if offline_capable else "強制依賴外部中央雲端 API，土石流斷網即癱瘓"
        },
        "salt_mist_rating": {
            "rating": ip_rating,
            "pass": "67" in ip_rating or "68" in ip_rating or "65" in ip_rating,
            "desc": "具備密封耐鹽霧與高濕防腐蝕能力" if ("67" in ip_rating or "68" in ip_rating or "65" in ip_rating) else "工業防護等級不足，金屬接點在沿海鹽霧下易氧化失效"
        }
    }
    all_passed = all(t["pass"] for t in tests.values())
    return {
        "sandbox_passed": all_passed,
        "details": tests
    }

def main():
    parser = argparse.ArgumentParser(description="第一原則解剖與台東抗逆沙盒原子 (atom-radar-first-principles)")
    parser.add_argument("--tech-name", type=str, default="縱谷風土常民邊緣感知盒", help="技術或硬體品名")
    parser.add_argument("--tech-claim", type=str, default="採用超低功耗微感測器，革命性突破長輩防跌，離線運算守護居家安全", help="廠商文宣或技術摘要")
    parser.add_argument("--claimed-power-watts", type=float, default=2.8, help="整機工作功耗 (W)")
    parser.add_argument("--offline-capability", action="store_true", default=True, help="是否支援 100% 離線運行")
    parser.add_argument("--ip-rating", type=str, default="IP67", help="防水防腐防塵等級")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-radar-first-principles 第一原則解剖與台東抗逆沙盒審計] ===")
    print(f"評審標的: {args.tech_name}")
    print(f"宣稱摘要: \"{args.tech_claim}\"")

    # 1. 行銷忽悠話術掃描
    hypes = scan_hype_slop(args.tech_claim)
    if hypes:
        print(f"[戴明安燈警報] 檢出高風險忽悠詞令: {', '.join(hypes)} (已觸發防泡沫審查！)")
    else:
        print("[逆熱度濾網] 文宣真實客觀，無浮誇泡沫詞彙。")

    # 2. 台東風土抗逆沙盒審查
    sandbox_res = audit_taitung_sandbox(args.claimed_power_watts, args.offline_capability, args.ip_rating)
    print("\n[台東風土極限抗逆沙盒三項大考驗]")
    for k, v in sandbox_res["details"].items():
        status = "PASS" if v["pass"] else "FAIL"
        print(f"  • [{status}] {k}: {v['desc']}")

    overall_decision = "APPROVED_FOR_EDGE_DEPLOY" if (sandbox_res["sandbox_passed"] and len(hypes) <= 1) else "REJECTED_OR_NEEDS_HARDENING"
    print(f"\n[硬核裁決]: {overall_decision}")

    report = {
        "tech_name": args.tech_name,
        "hype_buzzwords_detected": hypes,
        "first_principles_audit": {
            "power_watts": args.claimed_power_watts,
            "offline_ready": args.offline_capability,
            "ip_rating": args.ip_rating
        },
        "sandbox_results": sandbox_res,
        "decision": overall_decision
    }

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 科技審查數據結構 JSON 預覽 (前 250 字元):")
        rep_str = json.dumps(report, ensure_ascii=False, indent=2)
        print(rep_str[:250] + "...\n")
        print("[物理演練驗證成功] 第一原則與風土抗逆沙盒機制正常，Exit Code: 0")
        return

    print("[執行成功] 技術審定完畢，Exit Code: 0")

if __name__ == "__main__":
    main()
