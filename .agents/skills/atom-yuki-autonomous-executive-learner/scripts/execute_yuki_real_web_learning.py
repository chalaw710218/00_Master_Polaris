#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""執行長雪·真實受控上網研習執行器 (Yuki Real Web Learning Pipeline v1.0)

恪守創辦人（品碩）最高法旨與極星第一公理：
「寧要一寸真實的粗糙，也不要一尺虛假的精美」

本腳本規範（四項硬指標）：
1. 每一輪使用實際網路請求抓取 1~3 個來源，必須是可以成功打開（HTTP 200）之真實網址。
2. 存入每個來源的網址、抓取時間（ISO）、用雪自己的話寫的 2~3 句重點。數字只能照抄來源裡的並附原句；沒有就留空，嚴禁自行編造數字！
3. 另寫一行「對我們的用處」（沒有就寫「無」）。
4. 該輪若無任何可成功打開的網址，強制拉下安燈繩，一票否決，不得入帳（絕對不呼叫 cycle_ledger.tick）！
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
BIONIC_CORE = ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
YUKI_SKILL_DIR = ROOT_DIR / ".agents" / "skills" / "atom-yuki-autonomous-executive-learner"
YUKI_OFFICE_DIR = ROOT_DIR / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki"

sys.path.insert(0, str(BIONIC_CORE))
import cycle_ledger  # noqa: E402

OFFICE_VAULT = YUKI_OFFICE_DIR / "01_Cognitive_Vault" / "vault_yuki_executive_strategy.jsonl"
SKILL_VAULT = YUKI_SKILL_DIR / "vaults" / "vault_yuki_executive_strategy.jsonl"
OFFICE_EVIDENCE_DIR = YUKI_OFFICE_DIR / "01_Cognitive_Vault" / "cycle_evidence"
CORE_EVIDENCE_DIR = BIONIC_CORE / "vaults" / "cycle_evidence"

OFFICE_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
CORE_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
SKILL_VAULT.parent.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, timeout: int = 15) -> tuple[bool, int, bytes, str, str]:
    """執行真實 HTTP GET 請求，回傳 (is_ok, status_code, raw_bytes, clean_text, error_msg)"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 PolarisBionicLearner/6.5",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            status_code = r.getcode()
            if status_code != 200:
                return False, status_code, b"", "", f"HTTP 狀態碼非 200 ({status_code})"
            raw_bytes = r.read()
            # 嘗試解碼
            html = ""
            for enc in ("utf-8", "big5", "cp950", "latin1"):
                try:
                    html = raw_bytes.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            # 清洗純文字
            text = re.sub(r"<script.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<[^>]+>", " ", text)
            clean_text = " ".join(text.split())
            return True, status_code, raw_bytes, clean_text, ""
    except Exception as e:
        return False, 0, b"", "", str(e)


def run_real_learning_cycle(
    topic: str,
    target_sources: list[dict],
    usefulness_for_polaris: str,
) -> int:
    """執行單輪真實學習並檢驗門禁入帳"""
    print("==================================================")
    print("👑 [執行長 雪 · 真實受控上網研習管線啟動]")
    print(f"📌 主題：{topic}")
    print("==================================================")

    current_count = cycle_ledger.cycle_count("yuki")
    next_cycle = current_count + 1
    print(f"📊 當前帳本輪次：{current_count} ➔ 即將攻堅輪次：第 {next_cycle} 輪")

    if cycle_ledger.is_locked("yuki"):
        print("❌ 【戴明安燈攔截】雪的帳本當前處於停機鎖定狀態，必須先完成十輪審計解鎖！")
        sys.exit(1)

    validated_sources = []
    
    for item in target_sources:
        url = item["url"]
        print(f"\n🌐 正在真實連線網址：{url}")
        ok, code, raw, clean_text, err = fetch_url(url)
        fetched_at = datetime.now().isoformat()
        
        if not ok:
            print(f"  ❌ 連線失敗：{err}（狀態碼：{code}）➔ 依規範剔除！")
            continue
            
        sha256_hash = hashlib.sha256(raw).hexdigest()
        print(f"  ✅ 連線成功：HTTP {code} ｜ 內文長度：{len(raw):,} bytes ｜ SHA256: {sha256_hash[:16]}...")
        
        # 嚴格驗證原句與數字（如果提供了 quoted_metrics，必須能在 clean_text 中字元完全匹配）
        verified_metrics = []
        for m in item.get("quoted_metrics", []):
            num = m.get("number", "").strip()
            quote = m.get("original_quote", "").strip()
            if quote:
                # 模糊空白比對以容忍換行
                norm_quote = " ".join(quote.split())
                if norm_quote in clean_text:
                    verified_metrics.append({
                        "number": num,
                        "original_quote": quote,
                        "verified_in_source": True
                    })
                    print(f"  🔍 物理文字佐證核驗通過：『{quote[:40]}...』")
                else:
                    print(f"  ⚠️ 警告：原句未在網頁原始文字中找到完全匹配，依規範降級剔除該數字：『{quote[:30]}』")
            elif num:
                print(f"  ⚠️ 警告：僅有數字無原句，依創辦人法旨留空剔除：{num}")
        
        validated_sources.append({
            "url": url,
            "title": item.get("title", "未命名來源"),
            "fetched_at": fetched_at,
            "status_code": code,
            "raw_sha256": sha256_hash,
            "bytes_length": len(raw),
            "key_takeaways": item.get("key_takeaways", ""),
            "quoted_metrics": verified_metrics
        })

    # 門禁 4：該輪沒有任何可打開的網址，就不得入帳（不呼叫 cycle_ledger.tick）
    if not validated_sources:
        print("\n🚨 【戴明安燈物理攔截 (Poka-Yoke)】")
        print("本輪無任何可成功打開之真實網址（可連線數 = 0）！")
        print("依創辦人最高法旨：嚴禁入帳，不呼叫 cycle_ledger.tick。系統退出！")
        sys.exit(1)

    print(f"\n🎯 門禁檢驗合格：本輪成功打開並驗證 {len(validated_sources)} 個真實來源！")

    # 封裝證據檔案
    evidence_filename = f"yuki_cycle_{next_cycle:02d}_evidence.json"
    office_ev_path = OFFICE_EVIDENCE_DIR / evidence_filename
    core_ev_path = CORE_EVIDENCE_DIR / evidence_filename

    evidence_data = {
        "cycle": next_cycle,
        "office": "yuki",
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "sources": validated_sources,
        "usefulness_for_polaris": usefulness_for_polaris if usefulness_for_polaris.strip() else "無",
        "validation_status": "真實網路來源驗證合格 (HTTP 200 + SHA256)"
    }

    # 寫入證據檔案
    with open(office_ev_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, ensure_ascii=False, indent=2)
    with open(core_ev_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, ensure_ascii=False, indent=2)
    print(f"📁 物理證據檔案已存檔：{office_ev_path.name}")

    # 寫入認知存摺 vault_yuki_executive_strategy.jsonl
    vault_entry = {
        "timestamp": datetime.now().isoformat(),
        "cycle": next_cycle,
        "learner": "Yuki (Chief Executive Officer)",
        "topic": topic,
        "sources": [
            {
                "url": s["url"],
                "fetched_at": s["fetched_at"],
                "status_code": s["status_code"],
                "title": s["title"],
                "key_takeaways": s["key_takeaways"],
                "quoted_metrics": s["quoted_metrics"]
            }
            for s in validated_sources
        ],
        "usefulness_for_polaris": usefulness_for_polaris if usefulness_for_polaris.strip() else "無",
        "evidence_file": str(office_ev_path.relative_to(ROOT_DIR)).replace("\\", "/"),
        "validation_status": "真實網路來源驗證合格"
    }

    entry_line = json.dumps(vault_entry, ensure_ascii=False) + "\n"
    with open(OFFICE_VAULT, "a", encoding="utf-8") as f:
        f.write(entry_line)
    with open(SKILL_VAULT, "a", encoding="utf-8") as f:
        f.write(entry_line)
    print(f"📓 認知存摺已入帳：{OFFICE_VAULT.name}")

    # 呼叫輪次帳本 tick
    summary = f"Cycle {next_cycle}: {topic}（真實際上網驗證 {len(validated_sources)} 個來源）"
    tick_n = cycle_ledger.tick("yuki", summary=summary, evidence=str(office_ev_path))
    print(f"⛓️ 輪次帳本不可篡改雜湊鏈已寫入：第 {tick_n} 輪 Tick 成功！")
    print("==================================================")
    print("🎉 恭喜！執行長雪 第 11 輪真實際上網學習閉環交付成功！")
    print("==================================================")
    return tick_n


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="執行長雪·真實受控上網研習執行器")
    parser.add_argument("--demo-cycle11", action="store_true", help="執行第 11 輪真實上網研習示範")
    args = parser.parse_args()

    if args.demo_cycle11:
        # 第 11 輪真實研習題材：台東在地緊急災難醫療與偏鄉照護韌性體系
        demo_topic = "台東偏鄉緊急災難救護與公衛韌性實務 (Taitung Disaster Medical Assistance & Public Health Resilience)"
        demo_sources = [
            {
                "url": "https://www.taitung.gov.tw/News_Content.aspx?n=13370&s=134812",
                "title": "臺東首度跨區及國際災難醫療救護隊聯合演練！饒慶鈴親臨DMAT演練 強化救災能力",
                "key_takeaways": "臺東縣政府首次結合花東、北區與國際醫療團隊進行跨區災難醫療演練，模擬地震發生後的急救與公衛應變。演練特別將災後3至5天的災民心理輔導、情緒支持與公共衛生防護列為關鍵任務，降低二次健康危機。",
                "quoted_metrics": [
                    {
                        "number": "1至3天",
                        "original_quote": "昨日模擬災情剛發生1至3天，由跨縣市團隊支援，現場開設兩個急救站處理傷患、進行醫療救治等"
                    },
                    {
                        "number": "3至5天",
                        "original_quote": "今日則模擬災後3至5天，進行災民收容、為受災民眾提供心理輔導和情緒支持等"
                    }
                ]
            }
        ]
        demo_usefulness = "生活管家在台東推行偏鄉到府服務與孤老探訪時，可借鑑演練中『災後 3~5 天心理輔導與防範二次公衛危機』架構，在豪雨或地震等孤島情境下，優先為獨居長輩提供物資順路帶與身心安撫，成為官方醫療隊抵達前之超在地微型守護節點。"

        run_real_learning_cycle(
            topic=demo_topic,
            target_sources=demo_sources,
            usefulness_for_polaris=demo_usefulness
        )
