#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
from pathlib import Path
from difflib import SequenceMatcher

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

hub_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(hub_dir / "scripts"))
from threads_publisher import THREADS_ACCESS_TOKEN, THREADS_USER_ID, API_BASE

url = f"{API_BASE}/{THREADS_USER_ID}/threads?fields=id,text,timestamp&limit=100&access_token={THREADS_ACCESS_TOKEN}"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

threads = data.get("data", [])
print(f"📡 成功自 Meta 官方 API 拉取自帳前台最新 {len(threads)} 篇貼文進行地毯式比對\n")

# 1. 完全相同查核
seen = {}
exact_duplicates = []
for t in threads:
    txt = (t.get("text") or "").strip()
    if not txt:
        continue
    if txt in seen:
        exact_duplicates.append((t["id"], seen[txt], txt))
    else:
        seen[txt] = t["id"]

# 2. 高相似度查核 (相似度 >= 75%)
high_similarity = []
for i in range(len(threads)):
    t1 = threads[i]
    txt1 = (t1.get("text") or "").strip()
    if not txt1:
        continue
    for j in range(i + 1, len(threads)):
        t2 = threads[j]
        txt2 = (t2.get("text") or "").strip()
        if not txt2:
            continue
        ratio = SequenceMatcher(None, txt1, txt2).ratio()
        if ratio >= 0.70:
            high_similarity.append((t1["id"], t2["id"], ratio, txt1[:50], txt2[:50]))

# 3. 輸出審計結果
print("==================================================")
print("🔍 審計一：【100% 字元完全重複】查核結果")
print("==================================================")
if exact_duplicates:
    print(f"🚨 警報！發現 {len(exact_duplicates)} 組完全相同的重複貼文：")
    for new_id, old_id, content in exact_duplicates:
        print(f"  ❌ 貼文 {new_id} 與舊貼文 {old_id} 內容完全一模一樣！")
        print(f"     內容節錄: {content[:80]}...\n")
else:
    print("✅ 合格：前台 100 篇貼文中，無任何 100% 完全重複的貼文！\n")

print("==================================================")
print("🔍 審計二：【文字相似度 >= 70% 高度撞車】查核結果")
print("==================================================")
if high_similarity:
    print(f"⚠️ 發現 {len(high_similarity)} 組高度相似（相似度 >= 70%）的貼文：")
    for id1, id2, r, c1, c2 in high_similarity:
        print(f"  - 貼文 {id1} vs {id2} ｜ 相似度: {r*100:.1f}%")
        print(f"    篇A: {c1}...")
        print(f"    篇B: {c2}...\n")
else:
    print("✅ 合格：未發現任何相似度高於 70% 的高雷同貼文！\n")

print("==================================================")
print("🔍 審計三：最近 15 篇貼文前 40 字情境掃描")
print("==================================================")
for idx, t in enumerate(threads[:15], 1):
    clean_txt = (t.get("text") or "").replace("\n", " ")
    print(f"{idx:02d}. [{t['id']}] ({t.get('timestamp', '')[:10]}) : {clean_txt[:55]}...")
