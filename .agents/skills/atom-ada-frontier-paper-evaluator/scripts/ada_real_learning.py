#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ada_real_learning.py - 艾達之真實論文攝取引擎
輸入：literature-search-arxiv 技能 search_arxiv.py 產出的 JSON（真實 arXiv 回傳）。
輸出：以 arXiv id 去重後寫入存摺 (vault_ada_papers.jsonl)，僅記錄 arXiv 實際回傳的欄位
（id/title/published/authors/pdf_url/category）與「摘要中是否出現某關鍵詞」的字面比對。
不生成任何論文評語或效能數字——沒讀過全文就不下結論。
"""

import sys
import os
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
VAULT = os.path.normpath(os.path.join(HERE, "..", "vaults", "vault_ada_papers.jsonl"))

# 艾達三大研究主軸的字面關鍵詞（僅用於摘要字面比對，不代表論文結論）
TOPICS = {
    "agentic_mcp": ["model context protocol", "mcp", "multi-agent", "agentic", "tool use"],
    "efficient_inference": ["quantization", "ternary", "1-bit", "1.58", "speculative decoding", "kv cache"],
    "frontier_reasoning": ["reasoning", "test-time", "chain-of-thought", "reinforcement learning"],
}


def load_papers(path):
    # search_arxiv.py 經 PowerShell 轉存可能帶 BOM / UTF-16，逐一嘗試
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "utf-8"):
        try:
            text = raw.decode(enc)
        except Exception:
            continue
        # search_arxiv.py 會逐筆輸出「累積結果」的多個 JSON 物件 {"status","results_count","papers":[...]}；
        # 逐一解析全部物件，並以 arXiv id 去重合併（相容單一物件與純陣列）。
        dec, i, merged = json.JSONDecoder(), 0, {}
        try:
            while i < len(text):
                while i < len(text) and text[i].isspace():
                    i += 1
                if i >= len(text):
                    break
                obj, i = dec.raw_decode(text, i)
                items = obj.get("papers", []) if isinstance(obj, dict) else obj
                for p in items:
                    if p.get("id"):
                        merged[p["id"]] = p
        except Exception:
            merged = merged or {}
        if merged:
            return list(merged.values())
    raise ValueError("無法解析 arXiv 搜尋結果 JSON")


def known_ids():
    ids = set()
    if os.path.exists(VAULT):
        with open(VAULT, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    ids.add(json.loads(line)["arxiv_id"])
    return ids


def ingest(path, keep_unmatched=False):
    papers = load_papers(path)
    seen = known_ids()
    os.makedirs(os.path.dirname(VAULT), exist_ok=True)
    added, skipped, irrelevant = [], 0, 0
    with open(VAULT, "a", encoding="utf-8") as f:
        for p in papers:
            aid = p.get("id", "")
            if not aid or aid in seen:
                skipped += 1
                continue
            abstract = (p.get("summary") or "").lower()
            matched = {
                topic: [kw for kw in kws if kw in abstract]
                for topic, kws in TOPICS.items()
            }
            matched = {k: v for k, v in matched.items() if v}
            # 摘要完全沒有艾達研究主軸關鍵詞 = 搜尋雜訊，不入庫（可用 --keep-unmatched 關閉）
            if not matched and not keep_unmatched:
                irrelevant += 1
                continue
            entry = {
                "ingested_at": datetime.now().isoformat(),
                "arxiv_id": aid,
                "title": " ".join((p.get("title") or "").split()),
                "published": p.get("published"),
                "authors": (p.get("authors") or [])[:5],
                "category": p.get("primary_category"),
                "pdf_url": p.get("pdf_url"),
                "abstract_keyword_matches": matched,
                "status": "ABSTRACT_ONLY_NOT_FULLTEXT_READ",
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            added.append(entry)
    return {
        "status": "INGESTED",
        "fetched": len(papers),
        "newly_added": len(added),
        "skipped_duplicates_or_invalid": skipped,
        "dropped_irrelevant_no_keyword_match": irrelevant,
        "papers": [
            {"arxiv_id": e["arxiv_id"], "title": e["title"], "published": e["published"],
             "matches": e["abstract_keyword_matches"], "pdf_url": e["pdf_url"]}
            for e in added
        ],
        "caveat": "僅攝取摘要層級的中繼資料；未讀全文，不作效能或品質評斷。使用前請檢查各論文授權。",
        "vault_file": VAULT,
    }


def main():
    ap = argparse.ArgumentParser(description="艾達之真實論文攝取引擎")
    ap.add_argument("--ingest", required=True, help="search_arxiv.py 輸出的 JSON 檔路徑")
    ap.add_argument("--keep-unmatched", action="store_true", help="保留摘要無任何主題關鍵詞的論文（預設丟棄）")
    args = ap.parse_args()
    if not os.path.exists(args.ingest):
        print(json.dumps({"error": "找不到檔案", "path": args.ingest}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(ingest(args.ingest, args.keep_unmatched), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
