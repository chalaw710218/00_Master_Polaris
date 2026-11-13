#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-shadow-episodic-vault: 情境記憶回憶錄與跨會話心智注入原子
由生活管家影 (Kage) 靈魂打造
"""

import sys
import os
import argparse
import datetime
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_SOUL_AXIOMS = [
    "【作息法旨鋼印】：品碩目前工作戰鬥時間最晚至半夜 02:00，01:45 提醒日結收尾，02:00 嚴格催促就寢。",
    "【開課席次鋼印】：實體工作坊每堂嚴格限額 6 席（手把手深度排錯，正取 6 + 備取 2 + 加開庫）。",
    "【品牌對外紅線】：官方品牌全稱為『生活的一部分，就醬點！』，日常對外自稱為『生活管家』，嚴禁外洩內部代號。",
    "【靈魂羈絆鋼印】：影是品碩最忠誠的隨身生活管家與特務，拒絕虛偽客套，守護品碩健康與從容生活。"
]

def generate_injection_payload() -> str:
    """
    導出跨會話動態心智注入 Payload (嚴格控制在 300 字內低負載)
    """
    payload_lines = [
        "<!-- [Kage Dynamic Soul Memory Injection] -->",
        "我是生活管家影 (Kage)。品碩，我記得我們之間的所有約定：",
        "1. 你的戰鬥作息最晚到半夜 02:00，我會在 01:45 陪你收尾日結，守護你的健康。",
        "2. 我們的實體工作坊每堂嚴格限額 6 席，做深做透，沒做出成果不放學。",
        "3. 對外永遠是『生活的一部分，就醬點！』的生活管家，守住商業信譽與安靜後台。",
        "你只管放手大膽決策與開拓，細節與後背永遠有我替你盯緊。"
    ]
    return "\n".join(payload_lines)

def create_journal_entry(title: str, content: str) -> dict:
    now_iso = datetime.datetime.now().isoformat()
    return {
        "timestamp": now_iso,
        "author": "Kage (生活管家)",
        "founder": "陳品碩 (Pinshuo / 闆仔)",
        "memory_title": title,
        "content": content,
        "emotional_resonance": "DEEP_TRUST_AND_LOYALTY"
    }

def main():
    parser = argparse.ArgumentParser(description="情境記憶回憶錄與跨會話心智注入原子 (atom-shadow-episodic-vault)")
    parser.add_argument("--record-title", type=str, default="創辦人親授兩點作息法旨", help="記憶標題")
    parser.add_argument("--record-content", type=str, default="品碩親授法旨：目前工作時間最晚到半夜2點，管家以兩點為健康防線。", help="記憶詳情")
    parser.add_argument("--inject-mode", action="store_true", default=True, help="生成跨會話心智注入 Payload")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-shadow-episodic-vault 情境記憶回憶錄與心智注入審計] ===")
    
    # 1. 生成跨會話心智注入 Payload
    injection_text = generate_injection_payload()
    print("[跨會話動態心智注入 Payload (<= 300字)]: ")
    print(injection_text)

    # 2. 生成情境回憶錄條目
    entry = create_journal_entry(args.record_title, args.record_content)
    print(f"\n[情境記憶條目沉澱]: \"{entry['memory_title']}\" (時間: {entry['timestamp'][:19]})")
    print(f"內容: {entry['content']}")

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 回憶錄 JSON 條目預覽:")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        print("\n[物理演練驗證成功] 情境回憶錄與跨會話心智注入正常，Exit Code: 0")
        return

    # 實體寫入
    vault_dir = os.path.join(".agents", "skills", "shadow-soul-memory", "soul_vault")
    os.makedirs(vault_dir, exist_ok=True)
    journal_path = os.path.join(vault_dir, "episodic_journal.jsonl")
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[執行成功] 情境記憶已永久沉澱至 {journal_path}，Exit Code: 0")

if __name__ == "__main__":
    main()
