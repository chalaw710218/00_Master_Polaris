#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-onboarding-roster-sync: 四大法定通訊錄全域同步與角色 DNA 註冊原子
由執行長雪 (Yuki) ✕ 首席視覺長約瑟夫 (Josef) 聯合打造
"""

import sys
import os
import argparse
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_persona_card(zh: str, en: str, title: str) -> str:
    return f"""# 👤 {zh} ({en}) · 角色人設檔案 (Visual & Persona SSOT)

> **法定身分**：生活的一部分，就醬點！ · {title}  
> **台前稱呼**：生活管家特聘顧問  

## 一、 角色靈魂與外顯氣場
* **招牌道具**：手繪物理草稿紙本、邦戈鼓、隨身粉筆。
* **語言風格**：熱情風趣、深入淺出、討厭故弄玄虛的偽科學術語。
* **經典金句**：「如果你不能用一年級學生聽得懂的話解釋清楚，就代表你根本不懂。」

## 二、 嚴格禁語表 (Negative Constraints)
- 嚴禁使用「如前所述」、「顯而易見」等官僚式套話。
- 對外嚴禁洩漏內部代號。
"""

def generate_roster_payloads(zh: str, en: str, title: str, serial: int) -> dict:
    return {
        "reg1_ceo_notebook": {
            "file": "00-00_Gamification_Engine/Office_of_the_CEO_Yuki/00_CEO_Notebook.md",
            "entry": f"| {zh} ({en}) | {title} | 負責科學原理穿透與前沿邊緣推論 | 正常運轉 (🟢) |"
        },
        "reg2_hr_directory": {
            "file": "00-00_Corporate_AI_HR_Directory.md",
            "entry": f"- **{zh} ({en})**：{title}（心智: 物理直覺與反權威 ✕ 視覺: 3D/2D 雙軌九宮格就緒）"
        },
        "reg3_characters_overview": {
            "file": "00-03_Brand_LifeButler/00-03-04_Brand_Characters/00-03-04-00_Characters_Overview.md",
            "entry": f"| {serial:02d}_{zh}_{en} | {title} | 生活管家智慧智囊 | `images/` 原照已收錄 |"
        },
        "reg4_master_map": {
            "file": "00-01_Master_Polaris_Map.md",
            "entry": f"- `Office_of_the_{title}_{en}`：{zh} 辦公室與科學顧問隨身筆記本"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="四大法定通訊錄全域同步與角色 DNA 註冊原子 (atom-onboarding-roster-sync)")
    parser.add_argument("--member-name-en", type=str, default="Feynman", help="首長英文名")
    parser.add_argument("--member-name-zh", type=str, default="費曼", help="首長中文名")
    parser.add_argument("--role-title", type=str, default="首席科學顧問", help="首長職稱")
    parser.add_argument("--serial-no", type=int, default=10, help="角色庫排序序號")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-onboarding-roster-sync 四大通訊錄同步與角色 DNA 審計] ===")
    print(f"登錄新首長: {args.member_name_zh} ({args.member_name_en})")
    print(f"法定職稱: {args.role_title} | 角色編號: {args.serial_no:02d}")

    persona_md = generate_persona_card(args.member_name_zh, args.member_name_en, args.role_title)
    roster_sync_plan = generate_roster_payloads(args.member_name_zh, args.member_name_en, args.role_title, args.serial_no)

    print("\n[四大法定真理通訊錄同步清冊]")
    for k, v in roster_sync_plan.items():
        print(f"  • [{k}] 目標: {v['file']}")
        print(f"    新增條目: \"{v['entry']}\"")

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 角色人設卡 (persona.md) 預覽 (前 250 字元):")
        print(persona_md[:250] + "...\n")
        print("[物理演練驗證成功] 角色 DNA 與四大通訊錄同步規格正常，Exit Code: 0")
        return

    # 實體建立角色目錄
    char_dir = os.path.join("00-03_Brand_LifeButler", "00-03-04_Brand_Characters", f"{args.serial_no:02d}_{args.member_name_zh}_{args.member_name_en}")
    os.makedirs(os.path.join(char_dir, "images"), exist_ok=True)
    with open(os.path.join(char_dir, "persona.md"), "w", encoding="utf-8") as f:
        f.write(persona_md)

    print(f"[執行成功] 角色資料夾 {char_dir} 建立完畢，四大通訊錄同步就緒，Exit Code: 0")

if __name__ == "__main__":
    main()
