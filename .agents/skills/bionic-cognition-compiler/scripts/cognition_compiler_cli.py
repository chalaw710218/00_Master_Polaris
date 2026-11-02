#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris Bionic Cognition Compiler CLI (極星認知存摺自動編譯器 CLI)
將全體內閣近 200 輪仿生自進化存摺（事實、信念、好奇心）確定性編譯為：
- 戴明神級防呆 SOP 檢核表 (Poka-Yoke Checklists)
- 在地走心社群選題庫 (Social Editorial Banks)
- 全域認知存摺健康度全息儀表板 (Cognitive Dashboard)
"""

import sys
import os
import re
import argparse
import json
from datetime import datetime

# Windows console cp950 encoding defense
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

OFFICES = {
    "yuki": {
        "name": "執行長 雪 (CEO Yuki)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CEO_Yuki/01_Cognitive_Log"
    },
    "abacus": {
        "name": "財務長 算盤 (CFO Abacus)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CFO_Abacus/01_Cognitive_Log"
    },
    "deming": {
        "name": "首席品質長 戴明 (CQO Deming)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CQO_Deming/01_Cognitive_Log"
    },
    "falcon": {
        "name": "市場情報長 獵鷹 (CIO Falcon)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CIO_Falcon/01_Cognitive_Log"
    },
    "josef": {
        "name": "首席視覺長 約瑟夫 (CVO Josef)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CVO_Josef/01_Cognitive_Log"
    },
    "kage": {
        "name": "特務兼生活管家 影 (Operative Kage)",
        "dir": "00-00_Gamification_Engine/Office_of_the_Operative_Kage/01_Cognitive_Log"
    },
    "linus": {
        "name": "首席工程長 林納斯 (CTO Linus)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CTO_Linus/01_Cognitive_Log"
    },
    "taylor": {
        "name": "首席行銷長 泰勒絲 (CMO Taylor)",
        "dir": "00-00_Gamification_Engine/Office_of_the_CMO_Taylor/01_Cognitive_Log"
    },
    "raven": {
        "name": "首席黑色調查官 渡鴉 (Forensic Raven)",
        "dir": "00-00_Gamification_Engine/Office_of_the_Forensic_Raven/01_Cognitive_Log"
    },
    "meow": {
        "name": "看板娘兼傲嬌生活博主 喵編 (Mascot Meow)",
        "dir": "00-00_Gamification_Engine/Lounge_of_the_Mascot_Meow/01_Cognitive_Log"
    }
}

def scan_all(verbose=False):
    print("\n========================================================")
    print("極星全域認知存摺全息掃描儀表板 (Cognitive Health Scan)")
    print("========================================================")
    
    total_facts = 0
    total_beliefs = 0
    total_curiosities = 0
    total_bytes = 0

    results = []

    for key, info in OFFICES.items():
        cdir = info["dir"]
        if not os.path.exists(cdir):
            continue

        facts_count = 0
        beliefs_count = 0
        curiosities_count = 0
        office_bytes = 0

        # Scan 01_Experiences_and_Evidence.md / 01_Facts.md
        for fname in ["01_Experiences_and_Evidence.md", "01_Facts.md"]:
            p = os.path.join(cdir, fname)
            if os.path.exists(p):
                sz = os.path.getsize(p)
                office_bytes += sz
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                    # Count bullet points or headers
                    facts_count += len(re.findall(r"(?:^|\n)\s*(?:\*|\d+\.)\s+\*\*", txt))

        # Scan 02_Belief_Evolution.md / 02_Beliefs.md
        for fname in ["02_Belief_Evolution.md", "02_Beliefs.md"]:
            p = os.path.join(cdir, fname)
            if os.path.exists(p):
                sz = os.path.getsize(p)
                office_bytes += sz
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                    b_matches = re.findall(r"(?:### 信念\s*#?\d+|^\s*\d+\.\s+\*\*關於)", txt, re.MULTILINE)
                    beliefs_count += len(b_matches)

        # Scan 03_Curiosities_and_Questions.md / 03_Curiosities.md
        for fname in ["03_Curiosities_and_Questions.md", "03_Curiosities.md"]:
            p = os.path.join(cdir, fname)
            if os.path.exists(p):
                sz = os.path.getsize(p)
                office_bytes += sz
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                    c_matches = re.findall(r"(?:### 好奇心\s*#?\d+|^\s*\d+\.\s+\*\*)", txt, re.MULTILINE)
                    curiosities_count += len(c_matches)

        total_facts += facts_count
        total_beliefs += beliefs_count
        total_curiosities += curiosities_count
        total_bytes += office_bytes

        kb = office_bytes / 1024
        results.append({
            "key": key,
            "name": info["name"],
            "facts": facts_count,
            "beliefs": beliefs_count,
            "curiosities": curiosities_count,
            "kb": kb
        })

        print(f"• {info['name']}: {kb:6.1f} KB | 事實: {facts_count:3d} 筆 | 信念: {beliefs_count:2d} 條 | 好奇心: {curiosities_count:2d} 個")

    print("--------------------------------------------------------")
    print(f"全域總計容量: {total_bytes / 1024:6.1f} KB")
    print(f"全域客觀事實: {total_facts} 筆")
    print(f"全域深層信念: {total_beliefs} 條")
    print(f"全域探索好奇: {total_curiosities} 個")
    print("========================================================\n")
    return results

def compile_sop(role="yuki", output_path="reports/compiled_deming_sop.md"):
    if role not in OFFICES:
        print(f"錯誤：未知角色 '{role}'")
        sys.exit(1)

    info = OFFICES[role]
    cdir = info["dir"]
    belief_files = ["02_Belief_Evolution.md", "02_Beliefs.md"]
    bpath = None
    for f in belief_files:
        p = os.path.join(cdir, f)
        if os.path.exists(p):
            bpath = p
            break

    if not bpath:
        print(f"錯誤：找不到 {info['name']} 的信念存摺。")
        sys.exit(1)

    with open(bpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Parse sections: ### 信念 #XX：標題
    pattern = r"### 信念\s*#(\d+)：([^\n]+)\n(.*?)(?=(?:### 信念\s*#\d+|$))"
    matches = re.findall(pattern, content, re.DOTALL)

    sop_items = []
    for idx_str, title, body in matches:
        # Extract 實踐修正 or 核心教訓
        fix_match = re.search(r"\*\s*\*\*實踐修正\*\*：([^\n]+)", body)
        fix_text = fix_match.group(1).strip() if fix_match else "嚴格恪守物理真值標準與第一線反饋。"
        
        # Extract 舊信念/誤區
        old_match = re.search(r"\*\s*\*\*信念\*\*：([^\n]+)", body)
        old_text = old_match.group(1).strip() if old_match else "避免過往直覺經驗偏誤。"

        sop_items.append({
            "id": int(idx_str),
            "title": title.strip(),
            "mistake": old_text,
            "action": fix_text
        })

    if not sop_items:
        # Fallback to general headers
        print("未偵測到標準 '### 信念 #XX' 格式，執行通用條目解析...")

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None

    # Red team filter: strip out "極星" if any
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    md_out = f"""# 📐 戴明神級防呆現場作業檢核表 (Poka-Yoke SOP Checklist)

> **編譯來源**：{info['name']} 認知存摺 (`02_Belief_Evolution.md`)  
> **編譯時間**：{now_str} ｜ **版本**：v1.0 (Compiled by bionic-cognition-compiler)  
> **品質長戴明審定**：杜絕事後挑毛病，落實不可做錯之物理/數位機關防呆！

---

## 📋 現場作戰與防呆核心指引

| 序號 | 業務防呆場景 / 信念真理 | 舊思維誤區 (嚴格禁止) | 戴明防呆現場強制動作 (Poka-Yoke Action) |
| :---: | :--- | :--- | :--- |
"""

    for item in sop_items:
        clean_title = item['title'].replace("極星", "生活管家")
        clean_mistake = item['mistake'].replace("極星", "生活管家")
        clean_action = item['action'].replace("極星", "生活管家")
        md_out += f"| **{item['id']:02d}** | **{clean_title}** | {clean_mistake} | ✅ **{clean_action}** |\n"

    md_out += """
---

### 🛑 戴明安燈出廠紅線
1. 每一項檢核均為現場物理真實動作，嚴禁空洞口號。
2. 凡涉及長輩安全、配電盤溫度或食品保存，若檢驗未達標，任何第一線夥伴均擁有拉下「安燈繩 (Andon Cord)」暫停作業之權利！
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_out)

    print(f"\n✅ 戴明防呆 SOP 編譯完成！")
    print(f"• 來源角色: {info['name']}")
    print(f"• 萃取條目數: {len(sop_items)} 條")
    print(f"• 輸出檔案: {output_path}\n")

def compile_topics(role="yuki", output_path="reports/compiled_social_topics.md"):
    if role not in OFFICES:
        print(f"錯誤：未知角色 '{role}'")
        sys.exit(1)

    info = OFFICES[role]
    cdir = info["dir"]
    cfiles = ["03_Curiosities_and_Questions.md", "03_Curiosities.md"]
    cpath = None
    for f in cfiles:
        p = os.path.join(cdir, f)
        if os.path.exists(p):
            cpath = p
            break

    if not cpath:
        print(f"錯誤：找不到 {info['name']} 的好奇心存摺。")
        sys.exit(1)

    with open(cpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Parse sections: ### 好奇心 #XX：標題
    pattern = r"### 好奇心\s*#(\d+)：([^\n]+)\n(.*?)(?=(?:### 好奇心\s*#\d+|$))"
    matches = re.findall(pattern, content, re.DOTALL)

    topics = []
    for idx_str, title, body in matches:
        prop_match = re.search(r"\*\s*\*\*探索命題\*\*：([^\n]+)", body)
        prop_text = prop_match.group(1).strip() if prop_match else body.strip()[:120]
        topics.append({
            "id": int(idx_str),
            "title": title.strip(),
            "angle": prop_text
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    md_out = f"""# 📱 Threads & FB 在地走心社群選題庫 (Authentic Social Editorial Bank)

> **編譯來源**：{info['name']} 好奇心存摺 (`03_Curiosities_and_Questions.md`)  
> **編譯時間**：{now_str} ｜ **監製**：泰勒絲 (CMO) ✕ 影 (Kage) ✕ 約瑟夫 (CVO)  
> **風格守則**：100% 杜絕 AI 腔，嚴禁出現「極星」；自稱「生活管家」或「喵編」，專注土地呼吸與真情實感。

---

## 💡 精選在地高共鳴選題清單

"""

    for t in topics:
        clean_title = t['title'].replace("極星", "生活管家")
        clean_angle = t['angle'].replace("極星", "生活管家")
        md_out += f"""### 【選題 #{t['id']:02d}】{clean_title}
* **核心切角與故事火花**：{clean_angle}
* **建議發布平台**：Threads (日常生活手記 / 喵編傲嬌隨筆) ＆ Facebook (深度在地故事)
* **第一則留言掛載建議**：
  > *「正氣北路生活管家，這不只是一件服務，是我們替台東街坊鄰居順手帶的一份安心。需要聊聊請點 LINE：https://lin.ee/z83YSq6」*

---
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_out)

    print(f"\n✅ 社群爆款選題庫編譯完成！")
    print(f"• 來源角色: {info['name']}")
    print(f"• 萃取選題數: {len(topics)} 個")
    print(f"• 輸出檔案: {output_path}\n")

def main():
    parser = argparse.ArgumentParser(description="Polaris Bionic Cognition Compiler CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("scan", help="全息掃描全體內閣存摺健康度與統計")

    sop_p = subparsers.add_parser("compile-sop", help="將深層信念編譯為戴明防呆現場檢核表")
    sop_p.add_argument("--role", default="yuki", choices=list(OFFICES.keys()), help="目標角色 (預設: yuki)")
    sop_p.add_argument("--output", default="reports/compiled_deming_sop.md", help="輸出檔案路徑")

    top_p = subparsers.add_parser("compile-topics", help="將前瞻好奇心編譯為社群爆款選題庫")
    top_p.add_argument("--role", default="yuki", choices=list(OFFICES.keys()), help="目標角色 (預設: yuki)")
    top_p.add_argument("--output", default="reports/compiled_social_topics.md", help="輸出檔案路徑")

    args = parser.parse_args()
    if args.command == "scan":
        scan_all()
    elif args.command == "compile-sop":
        compile_sop(args.role, args.output)
    elif args.command == "compile-topics":
        compile_topics(args.role, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
