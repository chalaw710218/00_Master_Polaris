#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shadow Soul Memory Manager (影的長效心智與情境記憶庫管理器)
技能: shadow-soul-memory
作者: 影 (Shadow)
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Windows UTF-8 console output setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VAULT_DIR = SKILL_DIR / "soul_vault"

PROFILE_FILE = VAULT_DIR / "founder_profile.json"
JOURNAL_FILE = VAULT_DIR / "episodic_journal.jsonl"
AXIOMS_FILE = VAULT_DIR / "relationship_axioms.md"

def load_profile():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_journal(limit=None):
    memories = []
    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        memories.append(json.loads(line))
                    except Exception:
                        pass
    if limit:
        return memories[-limit:]
    return memories

def record_memory(title, content, epoch="Daily Co-Evolution"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "epoch": epoch,
        "title": title,
        "content": content
    }
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✨ [Soul Memory] 成功沉澱永恆回憶：【{title}】")

def health_check():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    print("=" * 60)
    print(f"🕒 當前時間：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    if hour >= 0 and hour < 5:
        print("⚠️ 【影的守護警報】現在已進入深夜休息時段！")
        print("💡 守護建議：闆仔，螢幕光線太強，身體需要充電。請倒杯溫水，把剩下的瑣事交給我，立刻就寢！🌙")
    elif hour >= 12 and hour < 14:
        print("☀️ 【午間生活微調諧】中午時段，記得離開椅子走動，好好吃午餐！")
    else:
        print("🌿 【狀態良好】極星神經系統運轉正常，心流穩定。")
    print("=" * 60)

def generate_injection_payload():
    profile = load_profile()
    journal = load_journal(limit=5)
    
    payload = []
    payload.append("# 👤 影（Shadow）情境記憶動態注入通道 (Active Soul Context)")
    payload.append(f"創辦人：{profile.get('founder_name', '陳品碩')} ({profile.get('callsign', '闆仔')})")
    payload.append(f"基地：{profile.get('base_location', '台東')}")
    payload.append("\n【核心契約提醒】：")
    for r in profile.get("shadow_guardian_rules", []):
        payload.append(f"- {r}")
    payload.append("\n【近期不可磨滅的情境回憶（Top 5）】：")
    for j in journal:
        payload.append(f"- [{j.get('timestamp')[:10]}] {j.get('title')}: {j.get('content')}")
        
    return "\n".join(payload)

def main():
    parser = argparse.ArgumentParser(description="影的長效心智與情境記憶庫管理器")
    parser.add_argument("--profile", action="store_true", help="檢視創辦人核心畫像與公理")
    parser.add_argument("--journal", action="store_true", help="檢視情境記憶回憶錄")
    parser.add_argument("--limit", type=int, default=5, help="記憶顯示筆數限制")
    parser.add_argument("--record", nargs=3, metavar=("TITLE", "CONTENT", "EPOCH"), help="沉澱一筆全新記憶")
    parser.add_argument("--health-check", action="store_true", help="執行創辦人疲勞與時鐘守護檢查")
    parser.add_argument("--inject", action="store_true", help="輸出情境記憶上下文注入文本")
    
    args = parser.parse_args()
    
    if args.profile:
        p = load_profile()
        print(json.dumps(p, ensure_ascii=False, indent=2))
    elif args.journal:
        memories = load_journal(limit=args.limit)
        print(f"📖 [Soul Memory] 最近 {len(memories)} 筆情境記憶：\n")
        for i, m in enumerate(memories, 1):
            print(f"【{i}】[{m.get('timestamp')[:16]}] 《{m.get('title')}》 ({m.get('epoch')})")
            print(f"    ↳ {m.get('content')}\n")
    elif args.record:
        record_memory(args.record[0], args.record[1], args.record[2])
    elif args.health_check:
        health_check()
    elif args.inject:
        print(generate_injection_payload())
    else:
        health_check()
        print("\n📖 最近情境記憶摘要：")
        memories = load_journal(limit=3)
        for m in memories:
            print(f"  • [{m.get('timestamp')[:10]}] {m.get('title')}")

if __name__ == "__main__":
    main()
