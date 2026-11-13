#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-onboarding-office-scaffolder: 總部大腦辦公室與主權目錄拓荒原子
由執行長雪 (Yuki) ✕ CTO 林納斯 (Linus) 聯合打造
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

def get_next_domain_serial(workspace_dir: str) -> str:
    """
    掃描 workspace_dir 下方 00-XX 開頭的目錄，找出最大數字並遞增
    """
    if not os.path.exists(workspace_dir):
        return "00-14"
    
    entries = os.listdir(workspace_dir)
    max_num = 0
    for e in entries:
        m = re.match(r"^00-(\d+)", e)
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    next_num = max_num + 1
    return f"00-{next_num:02d}"

def generate_office_readme(title: str, name: str, domain_dir: str) -> str:
    return f"""# 🏛️ 極星宇宙 · {title} {name} 辦公室

> **領地歸屬**：`00-00_Gamification_Engine/Office_of_the_{title}_{name}`  
> **最高統帥**：創辦人（品碩）  
> **主理首長**：{name} ({title})  
> **管轄實體陣地**：`{domain_dir}`  

---

## 一、 辦公室憲章與座右銘
* **核心座右銘**：秉持第一原則，實幹興邦，守護台東在地風土與常民尊嚴。
* **主要責任防區**：負責 `{domain_dir}` 之全生命週期研發、運營與安燈管制。
"""

def generate_notebook_md(name: str) -> str:
    return f"""# 📓 {name} 隨身戰略筆記本 (Strategic Notebook)

> **主理人**：{name}  
> **更新頻率**：每次會話動態同步  

## 一、 全域協同與管制標準
- 恪守戴明安燈質檢與品牌法定名稱零洩漏防火牆。
- 與執行長室 (Yuki)、工程長室 (Linus)、品質長室 (Deming) 緊密神經閉環。
"""

def main():
    parser = argparse.ArgumentParser(description="總部大腦辦公室與主權目錄拓荒原子 (atom-onboarding-office-scaffolder)")
    parser.add_argument("--member-name", type=str, default="Feynman", help="首長英文名")
    parser.add_argument("--member-title", type=str, default="Chief_Scientific_Advisor", help="首長職稱")
    parser.add_argument("--domain-name", type=str, default="Deep_Science_Lab", help="實體主權領地名稱")
    parser.add_argument("--workspace-dir", type=str, default=".", help="極星工作區根目錄")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    serial_str = get_next_domain_serial(args.workspace_dir)
    domain_folder_name = f"{serial_str}_{args.domain_name}"
    office_folder_name = f"Office_of_the_{args.member_title}_{args.member_name}"
    office_rel_path = os.path.join("00-00_Gamification_Engine", office_folder_name)

    print("=== [atom-onboarding-office-scaffolder 大腦辦公室與主權目錄拓荒審計] ===")
    print(f"入閣首長: {args.member_name} ({args.member_title})")
    print(f"總部大腦辦公室: {office_rel_path}")
    print(f"劃定實體主權領地: {domain_folder_name}")

    manifest = {
        "member_name": args.member_name,
        "member_title": args.member_title,
        "office_path": office_rel_path,
        "domain_serial": serial_str,
        "domain_path": domain_folder_name,
        "sub_pillars": [
            f"{domain_folder_name}/01_Core_Specs",
            f"{domain_folder_name}/02_Pipelines",
            f"{domain_folder_name}/03_Telemetry",
            f"{domain_folder_name}/04_Playbooks",
            f"{domain_folder_name}/05_Knowledge_Base"
        ],
        "core_files": [
            f"{office_rel_path}/README.md",
            f"{office_rel_path}/00_{args.member_name}_Notebook.md",
            f"{domain_folder_name}/README.md"
        ]
    }

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 領地拓荒清單 JSON 預覽 (前 250 字元):")
        man_str = json.dumps(manifest, ensure_ascii=False, indent=2)
        print(man_str[:250] + "...\n")
        print("[物理演練驗證成功] 流水號計算與辦公室/主權拓荒規格正常，Exit Code: 0")
        return

    # 實體建立
    os.makedirs(office_rel_path, exist_ok=True)
    with open(os.path.join(office_rel_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(generate_office_readme(args.member_title, args.member_name, domain_folder_name))
    with open(os.path.join(office_rel_path, f"00_{args.member_name}_Notebook.md"), "w", encoding="utf-8") as f:
        f.write(generate_notebook_md(args.member_name))

    os.makedirs(domain_folder_name, exist_ok=True)
    for sub in manifest["sub_pillars"]:
        os.makedirs(sub, exist_ok=True)

    print(f"[執行成功] 大腦辦公室與主權領地 {domain_folder_name} 已成功拓荒落地，Exit Code: 0")

if __name__ == "__main__":
    main()
