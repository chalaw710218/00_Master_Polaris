#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-reverse-sandbox-triage: 逆向工程沙盒拓荒與多格式解包原子
由 CTO 林納斯 (Linus) 業務主政
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

def get_next_serial_number(lab_dir: str) -> str:
    """
    掃描 00-11 目錄下的資料夾，找出最大流水號並遞增
    """
    if not os.path.exists(lab_dir):
        return "00-11-01"
    
    entries = os.listdir(lab_dir)
    max_num = 0
    for e in entries:
        m = re.match(r"^00-11-(\d+)", e)
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    next_num = max_num + 1
    return f"00-11-{next_num:02d}"

def determine_toolchain(target_type: str) -> dict:
    toolchains = {
        "web_js": {
            "parser": "REA AST & Webpack Reconstruct",
            "pipeline": "靜態 AST 審計 -> 路由表與 API 端點還原",
            "recommended_tools": ["npx rea-agents analyze-javascript-application", "esprima"]
        },
        "electron": {
            "parser": "asar 解包 ✕ IPC 通道監聽",
            "pipeline": "asar extract -> 主進程 IPC 路由分析 -> 前端 Vue/React 逆向",
            "recommended_tools": ["npx asar extract", "electron-decompiler"]
        },
        "har_traffic": {
            "parser": "HAR JSON 流量解構 ✕ 簽名推演",
            "pipeline": "Request Headers 提煉 -> X-Sign 雜湊算法逆推 -> Payload 重放驗證",
            "recommended_tools": ["mitmproxy", "har-extractor", "Python hmac/hashlib"]
        },
        "android_apk": {
            "parser": "JADX / Ghidra 反編譯",
            "pipeline": "APK 解壓 -> smali/dex 轉 Java -> 符號與 xrefs 追蹤",
            "recommended_tools": ["jadx-gui", "apktool", "ghidra"]
        }
    }
    return toolchains.get(target_type, toolchains["web_js"])

def main():
    parser = argparse.ArgumentParser(description="逆向工程沙盒拓荒與多格式解包原子 (atom-reverse-sandbox-triage)")
    parser.add_argument("--target-name", type=str, default="SampleTarget", help="目標系統名稱")
    parser.add_argument("--target-type", type=str, choices=["web_js", "electron", "har_traffic", "android_apk", "auto"], default="har_traffic", help="目標媒介格式")
    parser.add_argument("--base-lab-dir", type=str, default="00-11_Reverse_Engineering_Lab", help="實驗室根目錄")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    # 計算下一個流水號
    serial_str = get_next_serial_number(args.base_lab_dir)
    folder_name = f"{serial_str}_{args.target_name}"
    target_full_path = os.path.join(args.base_lab_dir, folder_name)

    target_type = "web_js" if args.target_type == "auto" else args.target_type
    toolchain_info = determine_toolchain(target_type)

    print("=== [atom-reverse-sandbox-triage 逆向沙盒拓荒與格式解包審計] ===")
    print(f"分配流水編號: {serial_str}")
    print(f"目標專屬目錄: {target_full_path}")
    print(f"媒介類型判定: {target_type.upper()}")
    print(f"推薦解包流程: {toolchain_info['pipeline']}")

    sandbox_manifest = {
        "serial": serial_str,
        "target_name": args.target_name,
        "target_type": target_type,
        "sandbox_path": target_full_path,
        "subdirectories": [
            f"{target_full_path}/target",
            f"{target_full_path}/extracted",
            f"{target_full_path}/analysis_notes"
        ],
        "toolchain": toolchain_info,
        "git_isolation": "Auto-inject .gitignore (*.asar, extracted/, *.apk) to prevent host pollution"
    }

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 沙盒拓荒配置清單 JSON 預覽 (前 250 字元):")
        manifest_str = json.dumps(sandbox_manifest, ensure_ascii=False, indent=2)
        print(manifest_str[:250] + "...\n")
        print("[物理演練驗證成功] 沙盒編號運算與解包工具鏈規劃正常，Exit Code: 0")
        return

    # 若非 dry-run，實體建立目錄
    os.makedirs(os.path.join(target_full_path, "target"), exist_ok=True)
    os.makedirs(os.path.join(target_full_path, "extracted"), exist_ok=True)
    os.makedirs(os.path.join(target_full_path, "analysis_notes"), exist_ok=True)
    with open(os.path.join(target_full_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("# Git Isolation\ntarget/\nextracted/\n*.apk\n*.asar\n*.har\n")

    print(f"[執行成功] 專屬沙盒 {target_full_path} 建立就緒，Exit Code: 0")

if __name__ == "__main__":
    main()
