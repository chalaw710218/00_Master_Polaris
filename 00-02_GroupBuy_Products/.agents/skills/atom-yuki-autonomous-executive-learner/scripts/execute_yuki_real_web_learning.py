#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""執行長雪·真實受控上網研習執行器 (Yuki Real Web Learning Pipeline v2.0 通用版)

恪守創辦人（品碩）最高法旨與極星第一公理：
「寧要一寸真實的粗糙，也不要一尺虛假的精美」

本腳本規範（四項硬指標與安全規格）：
1. 透過 --input <json檔> 傳入任務規格：包含 topic, sources (1~3個), usefulness_for_polaris。
2. 預設啟用嚴格 SSL 憑證校驗；若遭遇政府網站憑證鏈異常，退回備用連線並標記 ssl_verified=false，絕不全域關閉。
3. 歷史網址排重：同一個網址若已存在於認知存摺歷史中，強制阻斷，不得重複研習入帳。
4. 原句文字佐證：數字只能照抄來源裡的並附原句，必須能在原始網頁中完全匹配，否則剔除；無數字留空，嚴禁自行編造。
5. 零連線絕對攔截：該輪若無任何可成功打開的網址（有效數=0），一票否決，不得入帳（絕對不呼叫 cycle_ledger.tick）！
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


def get_historical_vault_urls() -> set[str]:
    """收集認知存摺歷史中已入帳的所有網址，防止重複刷輪次"""
    seen_urls = set()
    for vault_path in (OFFICE_VAULT, SKILL_VAULT):
        if not vault_path.exists():
            continue
        try:
            with open(vault_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    # 舊格式 source (單一字串) 或新格式 sources (列表)
                    if "sources" in data and isinstance(data["sources"], list):
                        for s in data["sources"]:
                            if isinstance(s, dict) and s.get("url"):
                                seen_urls.add(s["url"].strip())
                    elif "source" in data and isinstance(data["source"], str) and data["source"].startswith("http"):
                        seen_urls.add(data["source"].strip())
        except Exception as e:
            print(f"⚠️ 讀取歷史存摺警告：{e}")
    return seen_urls


def fetch_url(url: str, timeout: int = 15) -> tuple[bool, int, bytes, str, str, bool]:
    """執行真實 HTTP GET 請求。
    回傳 (is_ok, status_code, raw_bytes, clean_text, error_msg, ssl_verified)
    依創辦人規定：優先嚴格校驗 SSL 憑證；若遇特定憑證鏈異常，退回備用連線並標記 ssl_verified=False。
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 PolarisBionicLearner/6.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)

    # 1. 優先嘗試嚴格 SSL 驗證
    ctx_strict = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx_strict) as r:
            status_code = r.getcode()
            if status_code != 200:
                return False, status_code, b"", "", f"HTTP 狀態碼非 200 ({status_code})", True
            raw_bytes = r.read()
            clean_text = _extract_clean_text(raw_bytes)
            return True, status_code, raw_bytes, clean_text, "", True
    except (ssl.SSLError, ssl.CertificateError) as ssl_err:
        # 2. 僅對 SSL 憑證異常站台進行降級重試，標記 ssl_verified=False
        print(f"  ⚠️ 偵測到 SSL 憑證鏈校驗異常 ({ssl_err})，啟動單一站台容錯探測，標記 ssl_verified=False...")
        ctx_lax = ssl.create_default_context()
        ctx_lax.check_hostname = False
        ctx_lax.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx_lax) as r:
                status_code = r.getcode()
                if status_code != 200:
                    return False, status_code, b"", "", f"HTTP 狀態碼非 200 ({status_code})", False
                raw_bytes = r.read()
                clean_text = _extract_clean_text(raw_bytes)
                return True, status_code, raw_bytes, clean_text, "", False
        except Exception as e2:
            return False, 0, b"", "", f"SSL 降級連線仍失敗：{e2}", False
    except Exception as e:
        return False, 0, b"", "", str(e), True


def _extract_clean_text(raw_bytes: bytes) -> str:
    """嘗試多種編碼解碼並清洗 HTML 為純文字"""
    html = ""
    for enc in ("utf-8", "big5", "cp950", "latin1"):
        try:
            html = raw_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())


def execute_cycle_from_spec(spec_data: dict) -> tuple[bool, dict]:
    """依據任務規格執行單輪真實學習，回傳 (success, audit_summary)"""
    topic = spec_data.get("topic", "").strip()
    target_sources = spec_data.get("sources", [])
    usefulness = spec_data.get("usefulness_for_polaris", "").strip()

    if not topic:
        return False, {"error": "主題 (topic) 不得為空"}
    if not target_sources or not isinstance(target_sources, list):
        return False, {"error": "來源 (sources) 必須為 1~3 個非空清單"}
    if len(target_sources) > 3:
        return False, {"error": "來源數量不得超過 3 個"}

    current_count = cycle_ledger.cycle_count("yuki")
    next_cycle = current_count + 1

    print("==================================================")
    print(f"👑 [執行長 雪 · 第 {next_cycle} 輪受控上網研習啟動]")
    print(f"📌 主題：{topic}")
    print("==================================================")

    if cycle_ledger.is_locked("yuki"):
        msg = f"雪的帳本當前處於停機鎖定狀態（第 {current_count} 輪），必須先完成創辦人十輪審計簽章解鎖！"
        print(f"❌ 【戴明安燈攔截】{msg}")
        return False, {"cycle": next_cycle, "topic": topic, "passed": False, "reason": msg}

    historical_urls = get_historical_vault_urls()
    validated_sources = []
    source_results = []

    for item in target_sources:
        url = item.get("url", "").strip()
        title = item.get("title", "未命名來源").strip()
        key_takeaways = item.get("key_takeaways", "").strip()
        quoted_metrics_input = item.get("quoted_metrics", [])

        if not url:
            print("  ⚠️ 發現空網址，直接跳過！")
            continue

        # 門禁 3：歷史網址排重
        if url in historical_urls:
            print(f"  ❌ 網址已被歷史輪次入帳過：{url} ➔ 依規範不得重複研習，直接剔除！")
            source_results.append({
                "url": url,
                "title": title,
                "http_status": "DUPLICATE",
                "passed": False,
                "reason": "網址已於歷史輪次入帳過，依規範不得重複"
            })
            continue

        print(f"\n🌐 正在真實連線網址：{url}")
        ok, code, raw, clean_text, err, ssl_verified = fetch_url(url)
        fetched_at = datetime.now().isoformat()

        if not ok:
            print(f"  ❌ 連線失敗：{err}（狀態碼：{code}）➔ 依規範剔除！")
            source_results.append({
                "url": url,
                "title": title,
                "http_status": code if code != 0 else "CONNECTION_ERROR",
                "passed": False,
                "reason": err
            })
            continue

        sha256_hash = hashlib.sha256(raw).hexdigest()
        print(f"  ✅ 連線成功：HTTP {code} ｜ 內文：{len(raw):,} bytes ｜ SSL驗證: {ssl_verified} ｜ SHA256: {sha256_hash[:16]}...")

        # 嚴格原句文字佐證
        verified_metrics = []
        for m in quoted_metrics_input:
            num = m.get("number", "").strip()
            quote = m.get("original_quote", "").strip()
            if quote:
                norm_quote = " ".join(quote.split())
                if norm_quote in clean_text:
                    verified_metrics.append({
                        "number": num,
                        "original_quote": quote,
                        "verified_in_source": True
                    })
                    print(f"  🔍 物理文字佐證通過：『{quote[:35]}...』")
                else:
                    print(f"  ⚠️ 警告：原句未在網頁純文字中完全匹配，依規範降級剔除該數字：『{quote[:30]}』")
            elif num:
                print(f"  ⚠️ 警告：僅有數字無原句，依法旨留空剔除：{num}")

        validated_sources.append({
            "url": url,
            "title": title,
            "fetched_at": fetched_at,
            "status_code": code,
            "ssl_verified": ssl_verified,
            "raw_sha256": sha256_hash,
            "bytes_length": len(raw),
            "key_takeaways": key_takeaways,
            "quoted_metrics": verified_metrics
        })

        source_results.append({
            "url": url,
            "title": title,
            "http_status": code,
            "ssl_verified": ssl_verified,
            "passed": True,
            "metrics_count": len(verified_metrics)
        })

    # 門禁 4：該輪沒有任何可打開的網址，就不得入帳
    if not validated_sources:
        reason = "本輪無任何可成功打開之新網址（有效可連線數 = 0）！"
        print(f"\n🚨 【戴明安燈物理攔截】{reason}")
        print("依創辦人最高法旨：嚴禁入帳，不呼叫 cycle_ledger.tick。本輪終止！")
        return False, {
            "cycle": next_cycle,
            "topic": topic,
            "passed": False,
            "sources": source_results,
            "reason": reason
        }

    print(f"\n🎯 門禁合格：本輪成功打開並驗證 {len(validated_sources)} 個真實來源！")

    # 寫入物理證據檔案
    evidence_filename = f"yuki_cycle_{next_cycle:02d}_evidence.json"
    office_ev_path = OFFICE_EVIDENCE_DIR / evidence_filename
    core_ev_path = CORE_EVIDENCE_DIR / evidence_filename

    evidence_data = {
        "cycle": next_cycle,
        "office": "yuki",
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "sources": validated_sources,
        "usefulness_for_polaris": usefulness if usefulness else "無",
        "validation_status": "真實網路來源驗證合格 (HTTP 200 + SHA256)"
    }

    with open(office_ev_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, ensure_ascii=False, indent=2)
    with open(core_ev_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, ensure_ascii=False, indent=2)
    print(f"📁 物理證據檔案已存檔：{office_ev_path.name}")

    # 寫入認知存摺
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
                "ssl_verified": s["ssl_verified"],
                "title": s["title"],
                "key_takeaways": s["key_takeaways"],
                "quoted_metrics": s["quoted_metrics"]
            }
            for s in validated_sources
        ],
        "usefulness_for_polaris": usefulness if usefulness else "無",
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

    return True, {
        "cycle": tick_n,
        "topic": topic,
        "passed": True,
        "sources": source_results,
        "evidence_file": office_ev_path.name,
        "usefulness": usefulness if usefulness else "無"
    }


def main():
    parser = argparse.ArgumentParser(description="執行長雪·真實受控上網研習執行器 (v2.0 通用版)")
    parser.add_argument("--input", required=True, type=str, help="輸入任務 JSON 規格檔案路徑")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 錯誤：找不到指定的任務檔案：{args.input}")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except Exception as e:
        print(f"❌ 錯誤：解析任務 JSON 失敗：{e}")
        sys.exit(1)

    ok, summary = execute_cycle_from_spec(spec)
    print("\n================== 執行總結 ==================")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("==============================================")

    if not ok:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
