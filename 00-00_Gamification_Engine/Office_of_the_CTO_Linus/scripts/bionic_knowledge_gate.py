"""
bionic_knowledge_gate.py
技術長林納斯之仿生學習系統知識入庫與出處檢驗程式 (Bionic Knowledge Ingestion & Signature Gatekeeper) v4.1

【創辦人簽章硬化 (Founder Signature Gatekeeper)】
1. 林納斯的事實庫嚴禁直接 add（add 指令已廢止，一律退出 Exit Code 1）。
2. 入庫強制採取兩階段流水線：
   a. prepare: 讀取 _待入庫.md，逐條連網驗證原文與格式，生成 _本批待簽.json。
   b. sign: 由創辦人在真實終端機親自執行，在輸入口令前：
      - 重新核算 entries 雜湊與 batch_sha256（防竄改）
      - 重新逐條連網物理驗證網頁原文（防盲簽）
      - 完整展示每條「標題｜網址｜逐字摘句」
      - 簽章寫入 logs/ingest_signatures.jsonl 並安全寫入事實庫。
3. check: 全域白名單與簽章檢核。
   - 驗證每筆簽章之 entry_hashes 必須重算等於 payload 之 batch_sha256 且數量等於 count，任一不符整筆簽章作廢！
   - 事實庫裡每一條的內容雜湊，都必須出現在驗收合格的批次中。找不到或改過任一字一律阻斷，Exit Code 1！
"""

import os
import sys
import re
import json
import hashlib
import argparse
import tempfile
from pathlib import Path
from datetime import datetime

DEFAULT_EXPERIENCES_PATH = Path(__file__).resolve().parent.parent / "01_Cognitive_Log" / "01_Experiences_and_Evidence.md"
DEFAULT_PENDING_PATH = Path(__file__).resolve().parent.parent / "01_Cognitive_Log" / "_待入庫.md"
DEFAULT_TO_SIGN_PATH = Path(__file__).resolve().parent.parent / "01_Cognitive_Log" / "_本批待簽.json"
DEFAULT_SIGNATURES_PATH = Path(__file__).resolve().parent.parent / "logs" / "ingest_signatures.jsonl"

# 引入母版 bionic_core 之 evidence_gate 與 founder_auth
MASTER_BIONIC_CORE_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
if str(MASTER_BIONIC_CORE_DIR) not in sys.path:
    sys.path.append(str(MASTER_BIONIC_CORE_DIR))

try:
    from evidence_gate import quote_in_page, fetch_page_text, _normalize
except ImportError:
    def fetch_page_text(url: str, timeout: int = 20) -> str:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (evidence_gate)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="ignore")
        return re.sub(r"(?s)<[^>]+>", " ", raw)

    def quote_in_page(quote: str, page_text: str, min_fragment: int = 20) -> tuple:
        q = quote.strip().lower()
        p = page_text.strip().lower()
        if len(q) < min_fragment:
            return False, f"摘句太短，無法驗證（至少 {min_fragment} 字元）"
        if q not in p:
            return False, f"網頁中找不到這段摘句：「{quote[:60]}」"
        return True, ""

    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()

try:
    import founder_auth
except ImportError:
    from bionic_core import founder_auth


class SourceValidationError(Exception):
    """當出處不符合規格、屬於假出處或未通過母版證據檢查時拋出"""
    pass


def is_valid_source(source: str) -> bool:
    if not source or not isinstance(source, str):
        return False
    s = source.strip()
    if not s:
        return False

    if re.search(r'https?://[^\s/$.?#].[^\s]*', s, re.IGNORECASE):
        return True

    if re.search(r'\bpp?\.\s*\d+', s, re.IGNORECASE):
        return True

    if re.search(r'([0-9]+|[一二三四五六七八九十百]+)\s*頁', s) or re.search(r'第\s*([0-9]+|[一二三四五六七八九十百]+)\s*頁', s):
        return True

    if re.search(r'\bChapter\s*([0-9]+|[IVXLCDM]+)\b', s, re.IGNORECASE):
        return True

    if re.search(r'第\s*([0-9]+|[一二三四五六七八九十百]+)\s*章', s):
        return True

    return False


def compute_entry_hash(title: str, fact: str, source: str, url: str = None, quote: str = None) -> str:
    """計算單一事實條目的內容雜湊（不受序號影響，保證內容唯一性）"""
    t = re.sub(r'^\s*\d+\.\s*', '', title).strip().strip('*')
    canonical = (
        f"title={t}\n"
        f"fact={fact.strip()}\n"
        f"source={source.strip()}\n"
        f"url={(url or '').strip()}\n"
        f"quote={(quote or '').strip()}"
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_batch_sha256(entries: list[dict]) -> str:
    """計算整個批次的雜湊簽章"""
    hashes = [e["entry_hash"] for e in entries]
    return hashlib.sha256("".join(hashes).encode("utf-8")).hexdigest()


def nums_missing(fact: str, quote: str) -> list:
    """核心事實裡的數字，必須以完整數字出現在摘句裡（1 不能靠 11B 蒙混）"""
    q = quote.replace(',', '')
    return [x for x in re.findall(r'\d+(?:\.\d+)?', fact.replace(',', ''))
            if not re.search(r'(?<!\d)(?<!\d\.)' + re.escape(x) + r'(?!\d|\.\d)', q)]


def validate_entry(title: str, fact: str, source: str, url: str = None, quote: str = None) -> dict:
    if not title or not title.strip():
        raise ValueError("條目標題 (title) 不得為空")
    if not fact or not fact.strip():
        raise ValueError("核心事實 (fact) 不得為空")
    if not source or not source.strip():
        raise SourceValidationError("出處 (source) 為空，拒絕入庫！")
    
    if not is_valid_source(source):
        raise SourceValidationError(
            f"出處「{source}」不合格！必須包含有效網址 (http/https) 或帶數字之頁碼/章節 (p.數字, pp.數字, 數字頁, Chapter 數字, 第…章)。假出處一律退回！"
        )
    
    # 母版 v6.5 證據檢查：若提供 url 和 quote，執行逐字匹配查核
    if url is not None or quote is not None:
        if not url or not url.strip():
            raise ValueError("必填欄位 --url 不得為空")
        if not quote or not quote.strip():
            raise ValueError("必填欄位 --quote 不得為空")

        u = url.strip()
        q = quote.strip()

        if not re.match(r"^https?://\S+\.\S+", u):
            raise SourceValidationError(f"無效的 URL 格式：{u}")

        # 摘句片段長度門禁（每一段 ≥ 20 字）
        frags = [f.strip(" \"'.") for f in re.split(r"\.\.\.|…", q)]
        frags = [f for f in frags if f]
        short_frags = [f for f in frags if len(f) < 20]
        if short_frags:
            raise SourceValidationError(
                f"【入庫拒絕】摘句片段不足 20 字：「{short_frags[0]}」（長度 {len(short_frags[0])} < 20），無法有效證明逐字原文！"
            )

        # 抓取網頁實際文字
        try:
            page_text = fetch_page_text(u)
        except Exception as e:
            raise SourceValidationError(f"【入庫拒絕】無法抓取網頁進行驗證（{e}），拒絕入庫！")

        # 呼叫母版 evidence_gate.quote_in_page 進行逐字驗證
        ok, why = quote_in_page(q, page_text)
        if not ok:
            raise SourceValidationError(f"【入庫拒絕】母版證據檢查未通過！{why}")

        # 核心事實原子性數字門禁：核心事實裡的每個數字，都必須出現在逐字摘句裡
        clean_fact_for_num = fact.replace(',', '')
        clean_quote_for_num = q.replace(',', '')
        fact_nums = re.findall(r'\d+(?:\.\d+)?', clean_fact_for_num)
        quote_nums = set(re.findall(r'\d+(?:\.\d+)?', clean_quote_for_num))
        unmatched_nums = nums_missing(fact, quote)
        if unmatched_nums:
            raise SourceValidationError(
                f"【入庫拒絕】核心事實包含摘句中未出現之數字：{unmatched_nums}！核心事實只能陳述逐字摘句中已證實之數據，不可自行推論或增添數字！"
            )

        # 頁碼連續片段查證門禁
        page_pattern = re.compile(r'\bpp?\.\s*([0-9]+(?:\s*[\–\-]\s*[0-9]+)?)|([0-9]+)\s*頁', re.IGNORECASE)
        page_matches = list(page_pattern.finditer(source))
        if page_matches:
            norm_page = _normalize(page_text)
            norm_page_clean = re.sub(r'\s*-\s*', '-', norm_page)
            found_page = False
            for pm in page_matches:
                raw_ref = pm.group(0)
                num_part = pm.group(1) or pm.group(2)
                if '-' in num_part or '–' in num_part:
                    clean_range = re.sub(r'\s*[\–\-]\s*', '-', _normalize(num_part))
                    clean_raw = re.sub(r'\s*[\–\-]\s*', '-', _normalize(raw_ref))
                    if clean_range in norm_page_clean or clean_raw in norm_page_clean:
                        found_page = True
                        break
                else:
                    clean_raw = _normalize(raw_ref)
                    alt_forms = [
                        clean_raw,
                        f"p.{num_part}",
                        f"p. {num_part}",
                        f"page {num_part}",
                        f"pp. {num_part}",
                        f"{num_part}頁",
                        f"{num_part} 頁"
                    ]
                    if any(f in norm_page for f in alt_forms):
                        found_page = True
                        break
            if not found_page:
                raw_ref_str = page_matches[0].group(0)
                raise SourceValidationError(
                    f"【入庫拒絕】出處包含頁碼「{raw_ref_str}」，但證據網頁中找不到該連續頁碼片段！未查證之頁碼禁止入庫，請改用「網址」作為出處。"
                )

        # 章節連續片段查證門禁
        chapter_pattern = re.compile(r'\bChapter\s*([0-9]+|[IVXLCDM]+)\b|第\s*([0-9]+|[一二三四五六七八九十百]+)\s*章', re.IGNORECASE)
        chap_matches = list(chapter_pattern.finditer(source))
        if chap_matches:
            norm_page = _normalize(page_text)
            found_chap = False
            for cm in chap_matches:
                raw_chap = cm.group(0)
                num_chap = cm.group(1) or cm.group(2)
                clean_chap = _normalize(raw_chap)
                alt_chap_forms = [
                    clean_chap,
                    f"chapter {num_chap.lower()}",
                    f"第{num_chap}章",
                    f"第 {num_chap} 章"
                ]
                if any(f in norm_page for f in alt_chap_forms):
                    found_chap = True
                    break
            if not found_chap:
                raw_chap_str = chap_matches[0].group(0)
                raise SourceValidationError(
                    f"【入庫拒絕】出處包含章節「{raw_chap_str}」，但證據網頁中找不到該連續章節片段！未查證之章節禁止入庫，請改用「網址」作為出處。"
                )

    clean_title = re.sub(r'^\s*\d+\.\s*', '', title).strip().strip('*')
    eh = compute_entry_hash(clean_title, fact, source, url, quote)
    return {
        "title": clean_title,
        "fact": fact.strip(),
        "source": source.strip(),
        "url": url.strip() if url else None,
        "quote": quote.strip() if quote else None,
        "entry_hash": eh
    }


def parse_pending_markdown(filepath: Path) -> list[dict]:
    if not filepath.exists():
        raise FileNotFoundError(f"找不到待入庫檔案：{filepath}")
    
    content = filepath.read_text(encoding="utf-8")
    sections = re.split(r'\n(?=##\s+第\s*\d+\s*輪｜)', content)
    items = []
    
    for sec in sections:
        sec = sec.strip()
        if not sec.startswith("##"):
            continue
        
        m_title = re.search(r'^##\s+(.+)$', sec, re.MULTILINE)
        m_url = re.search(r'^\s*[-*]\s+網址：\s*(.+)$', sec, re.MULTILINE)
        m_quote = re.search(r'^\s*[-*]\s+逐字摘句：\s*(.+)$', sec, re.MULTILINE)
        m_fact = re.search(r'^\s*[-*]\s+核心事實：\s*(.+)$', sec, re.MULTILINE)
        
        if m_title and m_url and m_quote and m_fact:
            title = m_title.group(1).strip()
            url = m_url.group(1).strip()
            quote = m_quote.group(1).strip()
            fact = m_fact.group(1).strip()
            items.append({
                "title": title,
                "url": url,
                "quote": quote,
                "fact": fact,
                "source": url
            })
    return items


def parse_experiences_markdown(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    entries = []
    curr = None
    
    for raw in lines:
        s = raw.strip()
        m_title = re.match(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*：\s*$', raw)
        if m_title:
            if curr:
                entries.append(curr)
            curr = {
                "index": int(m_title.group(1)),
                "title": m_title.group(2).strip(),
                "fact": "",
                "source": "",
                "url": None,
                "quote": None
            }
            continue
        if curr:
            m_f = re.match(r'^\s*[-*]\s+\*\*核心事實\*\*：\s*(.+)$', raw)
            if m_f:
                curr["fact"] = m_f.group(1).strip()
                continue
            m_s = re.match(r'^\s*[-*]\s+\*\*出處\*\*：\s*(.+)$', raw)
            if m_s:
                curr["source"] = m_s.group(1).strip()
                continue
            m_u = re.match(r'^\s*[-*]\s+\*\*證據網址\*\*：\s*(.+)$', raw)
            if m_u:
                curr["url"] = m_u.group(1).strip()
                continue
            m_q = re.match(r'^\s*[-*]\s+\*\*原文摘句\*\*：\s*(.+)$', raw)
            if m_q:
                curr["quote"] = m_q.group(1).strip()
                continue
    if curr:
        entries.append(curr)
    
    for e in entries:
        e["entry_hash"] = compute_entry_hash(e["title"], e["fact"], e["source"], e.get("url"), e.get("quote"))
    return entries


def prepare_cmd(pending_path: Path = DEFAULT_PENDING_PATH, to_sign_path: Path = DEFAULT_TO_SIGN_PATH, is_baseline: bool = False, vault_path: Path = DEFAULT_EXPERIENCES_PATH) -> tuple[int, int, list]:
    print(f"=== 開始執行入庫預檢 (prepare) ===")
    
    if is_baseline:
        print(f"模式：現有事實庫基準批次預備 -> {vault_path}")
        entries = parse_experiences_markdown(vault_path)
        if not entries:
            print("❌ 事實庫無現有條目，無法建立基準批次")
            sys.exit(1)
        batch_sha = compute_batch_sha256(entries)
        pack = {
            "office": "linus",
            "action": "ingest_batch",
            "is_baseline": True,
            "created_at": datetime.now().isoformat(),
            "count": len(entries),
            "batch_sha256": batch_sha,
            "entry_hashes": [e["entry_hash"] for e in entries],
            "entries": entries
        }
        to_sign_path.parent.mkdir(parents=True, exist_ok=True)
        to_sign_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 成功預備基準批次待簽檔：{to_sign_path}")
        print(f"   總條目數：{len(entries)} 條，批次雜湊：{batch_sha[:16]}...")
        return len(entries), 0, []

    items = parse_pending_markdown(pending_path)
    n_sec = len(re.findall(r'^##\s', pending_path.read_text(encoding="utf-8"), re.MULTILINE))
    bad_titles = [i["title"] for i in items if not re.match(r'^第\s*\d+\s*輪｜', i["title"])]
    if n_sec == 0 or n_sec != len(items) or bad_titles:
        print(f"❌ 待入庫檔有 {n_sec} 段，合格解析 {len(items) - len(bad_titles)} 條：有段落格式不完整（標題要「## 第 N 輪｜」，網址／逐字摘句／核心事實都要有）。Exit Code 1")
        sys.exit(1)
    # 只檢查新條目：新條目和事實庫重複、或新條目彼此重複（事實庫裡原有的重複不影響）
    _old = parse_experiences_markdown(vault_path)
    old_titles = {e["title"] for e in _old}
    new_titles = [i["title"] for i in items]
    dup = sorted({t for t in new_titles if t in old_titles or new_titles.count(t) > 1})
    if dup:
        print(f"❌ 標題重複：{dup}。Exit Code 1")
        sys.exit(1)
    old_keys = {((e.get("url") or "").strip().rstrip("/"), (e.get("quote") or "").strip()) for e in _old}
    new_keys = [(i["url"].strip().rstrip("/"), i["quote"].strip()) for i in items]
    dupk = [k for k in new_keys if k in old_keys or new_keys.count(k) > 1]
    if dupk:
        print(f"❌ 同一網址＋同一摘句重複：{dupk[0][0]}。Exit Code 1")
        sys.exit(1)
    if not items:
        print(f"❌ 未在 {pending_path} 中找到任何待入庫條目！")
        sys.exit(1)

    passed_entries = []
    rejected = []

    for idx, item in enumerate(items, 1):
        print(f"[{idx:02d}/{len(items):02d}] 正在檢驗：{item['title']} ...", end=" ")
        try:
            entry = validate_entry(item["title"], item["fact"], item["source"], url=item.get("url"), quote=item.get("quote"))
            passed_entries.append(entry)
            print("✅ 通過")
        except Exception as e:
            print("❌ 退回")
            rejected.append((item["title"], str(e)))

    if rejected:
        print("\n❌ 退回條目清單：")
        for title, reason in rejected:
            print(f"  👉 「{title}」: {reason}")
        print("\n❌ 有條目被退回，整批不產生待簽檔。Exit Code 1")
        sys.exit(1)

    if passed_entries:
        batch_sha = compute_batch_sha256(passed_entries)
        pack = {
            "office": "linus",
            "action": "ingest_batch",
            "is_baseline": False,
            "created_at": datetime.now().isoformat(),
            "count": len(passed_entries),
            "batch_sha256": batch_sha,
            "entry_hashes": [e["entry_hash"] for e in passed_entries],
            "entries": passed_entries
        }
        to_sign_path.parent.mkdir(parents=True, exist_ok=True)
        to_sign_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n✅ 成功產生待簽檔案：{to_sign_path}")
        print(f"   通過條數：{len(passed_entries)} 條，退回條數：{len(rejected)} 條，批次雜湊：{batch_sha[:16]}...")
    else:
        print("\n❌ 所有條目皆未通過檢驗，未產生待簽檔案。")

    return len(passed_entries), len(rejected), rejected


def sign_cmd(to_sign_path: Path = DEFAULT_TO_SIGN_PATH, signatures_path: Path = DEFAULT_SIGNATURES_PATH, vault_path: Path = DEFAULT_EXPERIENCES_PATH, meta_path: Path = None, _test_passphrase: str = None) -> bool:
    print(f"=== 開始執行創辦人簽章與入庫 (sign) ===")
    if not to_sign_path.exists():
        print(f"❌ 找不到待簽檔案：{to_sign_path}，請先執行 prepare")
        sys.exit(1)

    data = json.loads(to_sign_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not entries:
        print("❌ 待簽檔案中無任何條目！")
        sys.exit(1)

    # 1. 嚴格防竄改防線：重新計算每條雜湊與整批 batch_sha256
    recomputed_hashes = []
    for idx, e in enumerate(entries, 1):
        eh = compute_entry_hash(e["title"], e["fact"], e["source"], e.get("url"), e.get("quote"))
        if eh != e.get("entry_hash"):
            print(f"❌ [安全阻斷] 條目 {idx} 雜湊不符！記錄值={e.get('entry_hash')} vs 實算值={eh}，檔案疑似遭篡改！")
            sys.exit(1)
        recomputed_hashes.append(eh)

    calc_batch_sha = hashlib.sha256("".join(recomputed_hashes).encode("utf-8")).hexdigest()
    if calc_batch_sha != data.get("batch_sha256"):
        print(f"❌ [安全阻斷] 整批 batch_sha256 不符！記錄值={data.get('batch_sha256')} vs 實算值={calc_batch_sha}，停止簽署！")
        sys.exit(1)

    if len(entries) != data.get("count"):
        print(f"❌ [安全阻斷] 條目數量不符！記錄值={data.get('count')} vs 實算值={len(entries)}，停止簽署！")
        sys.exit(1)

    # 2. 嚴格防盲簽防線：重新逐條連網驗證網頁原文（若有提供 url 和 quote）
    if not data.get("is_baseline", False):
        print("\n🔍 正在重新進行物理網頁驗證，防止盲簽...")
        for idx, e in enumerate(entries, 1):
            try:
                validate_entry(e["title"], e["fact"], e["source"], url=e.get("url"), quote=e.get("quote"))
            except Exception as ex:
                print(f"❌ [安全阻斷] 條目 {idx}「{e['title']}」重新驗證失敗：{ex}，停止簽署！")
                sys.exit(1)
        print("✅ 全數條目物理網頁重檢通過！\n")

    # 3. 完整列印給創辦人親自核對之明細清單 (Anti-Blind-Signing)
    print("=" * 70)
    print("📜 創辦人審批待簽事實條目清單 (Anti-Blind-Signing)")
    print("⚠️  請確認每條核心事實沒有超出摘句的內容")
    print("=" * 70)
    for idx, e in enumerate(entries, 1):
        print(f"[{idx:02d}] 標題：{e['title']}")
        if e.get("url"):
            print(f"     網址：{e['url']}")
        if e.get("quote"):
            print(f"     逐字摘句：{e['quote']}")
        print(f"     核心事實：{e['fact']}")
        print("-" * 70)
    print(f"總計待簽條數：{len(entries)} 條  ｜  整批雜湊：{calc_batch_sha}")
    print("=" * 70)

    payload = {
        "action": "ingest_batch",
        "office": data.get("office", "linus"),
        "batch_sha256": calc_batch_sha,
        "count": len(entries)
    }

    sig_bundle = founder_auth.sign_founder_action(payload, meta_path=meta_path, _test_passphrase=_test_passphrase)
    
    # 寫入 signatures log
    record = {
        "payload": payload,
        "sig": sig_bundle,
        "batch_sha256": calc_batch_sha,
        "count": len(entries),
        "entry_hashes": recomputed_hashes,
        "is_baseline": data.get("is_baseline", False),
        "created_at": datetime.now().isoformat()
    }
    signatures_path.parent.mkdir(parents=True, exist_ok=True)
    with open(signatures_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"✅ 創辦人簽章已記錄至：{signatures_path}")

    # 若非 baseline，寫入事實庫
    if not data.get("is_baseline", False):
        if not vault_path.exists():
            vault_path.parent.mkdir(parents=True, exist_ok=True)
            vault_path.write_text("# 技術長林納斯之核心事實與客觀證據庫 (Experiences & Evidence)\n\n---\n", encoding="utf-8")
        
        vault_content = vault_path.read_text(encoding="utf-8")
        existing_nums = [int(m) for m in re.findall(r'^\s*(\d+)\.\s+\*\*', vault_content, re.MULTILINE)]
        next_idx = (max(existing_nums) + 1) if existing_nums else 1

        new_text_blocks = []
        for e in entries:
            blk = f"\n\n{next_idx}. **{e['title']}**：\n   - **核心事實**：{e['fact']}\n   - **出處**：{e['source']}"
            if e.get("url"):
                blk += f"\n   - **證據網址**：{e['url']}"
            if e.get("quote"):
                blk += f"\n   - **原文摘句**：{e['quote']}"
            new_text_blocks.append(blk)
            next_idx += 1

        with open(vault_path, "a", encoding="utf-8") as f:
            f.write("".join(new_text_blocks))
        print(f"✅ 成功將 {len(entries)} 條條目正式追加寫入事實庫：{vault_path}")
    else:
        print(f"✅ 基準批次簽章完成，現有 {len(entries)} 條事實已完成主權認證！")

    return True


def check_file_whitelist(filepath: Path = DEFAULT_EXPERIENCES_PATH, signatures_path: Path = DEFAULT_SIGNATURES_PATH, meta_path: Path = None) -> bool:
    print(f"開始執行白名單與創辦人簽章嚴格檢驗：{filepath}")
    if not filepath.exists():
        print(f"❌ 錯誤：檔案不存在：{filepath}")
        sys.exit(1)
        
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    state = "IDLE"
    current_entry = {}
    valid_entries = []
    illegal_lines = []

    for line_idx, raw_line in enumerate(lines, 1):
        stripped = raw_line.strip()
        
        if not stripped:
            if state in ["EXPECT_OPTIONAL_EVIDENCE"]:
                state = "IDLE"
            continue
            
        if stripped.startswith('#'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現標題）：{raw_line}"))
            state = "IDLE"
            continue

        if stripped.startswith('>'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現引言）：{raw_line}"))
            state = "IDLE"
            continue

        if stripped.startswith('---'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現分隔線）：{raw_line}"))
            state = "IDLE"
            continue

        m_title = re.match(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*：\s*$', raw_line)
        if m_title:
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"前一條目缺少出處行，即出現新條目：{raw_line}"))
            state = "EXPECT_FACT"
            current_entry = {
                "line_no": line_idx,
                "index": int(m_title.group(1)),
                "title": m_title.group(2).strip(),
                "url": None,
                "quote": None
            }
            continue

        m_fact = re.match(r'^\s*[-*]\s+\*\*核心事實\*\*：\s*(.+)$', raw_line)
        if m_fact:
            if state == "EXPECT_FACT":
                current_entry["fact"] = m_fact.group(1).strip()
                state = "EXPECT_SOURCE"
                continue
            else:
                illegal_lines.append((line_idx, f"非預期位置出現核心事實行：{raw_line}"))
                state = "IDLE"
                continue

        m_source = re.match(r'^\s*[-*]\s+\*\*出處\*\*：\s*(.+)$', raw_line)
        if m_source:
            if state == "EXPECT_SOURCE":
                source_val = m_source.group(1).strip()
                current_entry["source"] = source_val
                if not is_valid_source(source_val):
                    illegal_lines.append((line_idx, f"出處不合格（需帶網址或頁碼/章節數字）：{raw_line}"))
                    state = "DISCARD_REMAINDER"
                else:
                    valid_entries.append(current_entry)
                    state = "EXPECT_OPTIONAL_EVIDENCE"
                continue
            else:
                illegal_lines.append((line_idx, f"非預期位置出現出處行：{raw_line}"))
                state = "IDLE"
                continue

        if state == "DISCARD_REMAINDER":
            m_url = re.match(r'^\s*[-*]\s+\*\*證據網址\*\*：\s*(.+)$', raw_line)
            m_quote = re.match(r'^\s*[-*]\s+\*\*原文摘句\*\*：\s*(.+)$', raw_line)
            if m_url or m_quote:
                continue
            state = "IDLE"

        if state == "EXPECT_OPTIONAL_EVIDENCE":
            m_url = re.match(r'^\s*[-*]\s+\*\*證據網址\*\*：\s*(.+)$', raw_line)
            if m_url:
                valid_entries[-1]["url"] = m_url.group(1).strip()
                continue
            m_quote = re.match(r'^\s*[-*]\s+\*\*原文摘句\*\*：\s*(.+)$', raw_line)
            if m_quote:
                valid_entries[-1]["quote"] = m_quote.group(1).strip()
                continue

        illegal_lines.append((line_idx, f"不在白名單內的非法行：{raw_line}"))
        state = "IDLE"

    if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
        illegal_lines.append((len(lines), f"檔案結尾條目不完整（缺少核心事實或出處行）"))

    if illegal_lines:
        print("\n❌ [安燈阻斷] 發現非白名單行或結構殘缺，拒絕通過！")
        for l_num, err in illegal_lines:
            print(f"  👉 第 {l_num} 行：{err}")
        print("\nExit Code 1。\n")
        sys.exit(1)

    if not valid_entries:
        print("❌ 錯誤：未在檔案中解析到任何有效合格條目！Exit Code 1。\n")
        sys.exit(1)

    print(f"✅ 格式白名單檢驗通過，共 {len(valid_entries)} 條合格結構。")

    # === 創辦人簽章驗簽檢核 (Signature Verification) ===
    print("正在檢核創辦人主權簽章 (ingest_signatures.jsonl) ...")
    verified_hashes = set()
    if signatures_path.exists():
        with open(signatures_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    payload = rec.get("payload")
                    sig = rec.get("sig")
                    entry_hashes = rec.get("entry_hashes", [])
                    
                    # 1. 驗證密碼學簽章
                    ok, why = founder_auth.verify_founder_action(payload, sig, meta_path=meta_path)
                    if not ok:
                        print(f"⚠️ [警告] 第 {line_no} 筆簽章批次驗簽失敗：{why}")
                        continue

                    # 2. 嚴格防塞入漏洞檢查 (Anti-Tampering Integrity Check)：
                    # 重新計算 entry_hashes 的 batch_sha256，必須與 payload 完全一致且條數相符！
                    calc_batch_sha = hashlib.sha256("".join(entry_hashes).encode("utf-8")).hexdigest()
                    if calc_batch_sha != payload.get("batch_sha256") or len(entry_hashes) != payload.get("count"):
                        print(f"⚠️ [安全阻斷] 第 {line_no} 筆簽章之 entry_hashes 遭竄改或塞入雜湊！整筆作廢（實算雜湊={calc_batch_sha[:16]}... vs 簽章={payload.get('batch_sha256')[:16]}...，條數={len(entry_hashes)} vs {payload.get('count')}）")
                        continue

                    for h in entry_hashes:
                        verified_hashes.add(h)

                except Exception as ex:
                    print(f"⚠️ [警告] 解析簽章記錄失敗 (line {line_no})：{ex}")
    else:
        print(f"⚠️ 找不到簽章檔案：{signatures_path}")

    unsigned_entries = []
    for entry in valid_entries:
        eh = compute_entry_hash(entry["title"], entry["fact"], entry["source"], entry.get("url"), entry.get("quote"))
        if eh not in verified_hashes:
            unsigned_entries.append((entry, eh))

    if unsigned_entries:
        print("\n❌ [安燈阻斷] 發現未經創辦人簽章（或簽章後內容被篡改）的條目！")
        for entry, eh in unsigned_entries:
            print(f"  👉 條目 {entry['index']:02d} | **{entry['title']}** (hash: {eh[:16]}...)")
        print(f"\n共 {len(unsigned_entries)} 條條目未通過創辦人簽章查驗！Exit Code 1。\n")
        sys.exit(1)

    print(f"\n🎉 全域白名單與創辦人簽章驗簽完全通過！共 {len(valid_entries)} 條條目皆具備有效創辦人簽章憑證。Exit Code 0。\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="技術長林納斯之仿生知識門禁守門員 (創辦人簽章對齊版)")
    subparsers = parser.add_subparsers(dest="command", help="子指令")

    # prepare 指令
    prep_parser = subparsers.add_parser("prepare", help="預檢待入庫條目並產生待簽檔案")
    prep_parser.add_argument("--file", default=str(DEFAULT_PENDING_PATH), help="待入庫 Markdown 檔案路徑")
    prep_parser.add_argument("--output", default=str(DEFAULT_TO_SIGN_PATH), help="輸出之待簽 JSON 檔案路徑")
    prep_parser.add_argument("--baseline", action="store_true", help="將現有事實庫打包為基準待簽批次")
    prep_parser.add_argument("--vault", default=str(DEFAULT_EXPERIENCES_PATH), help="現有事實庫檔案路徑")

    # sign 指令
    sign_parser = subparsers.add_parser("sign", help="創辦人親自簽章並正式入庫")
    sign_parser.add_argument("--input", default=str(DEFAULT_TO_SIGN_PATH), help="待簽 JSON 檔案路徑")
    sign_parser.add_argument("--signatures", default=str(DEFAULT_SIGNATURES_PATH), help="簽章日誌存放路徑")
    sign_parser.add_argument("--vault", default=str(DEFAULT_EXPERIENCES_PATH), help="事實庫檔案路徑")
    sign_parser.add_argument("--meta", default=None, help="創辦人 meta 設定檔路徑")

    # check 指令
    check_parser = subparsers.add_parser("check", help="白名單與創辦人簽章驗簽檢核")
    check_parser.add_argument("--file", default=str(DEFAULT_EXPERIENCES_PATH), help="事實庫檔案路徑")
    check_parser.add_argument("--signatures", default=str(DEFAULT_SIGNATURES_PATH), help="簽章日誌存放路徑")
    check_parser.add_argument("--meta", default=None, help="創辦人 meta 設定檔路徑")

    # 廢止 add 指令
    add_parser = subparsers.add_parser("add", help="已廢止之舊指令")

    args, unknown = parser.parse_known_args()

    if args.command == "prepare":
        try:
            prepare_cmd(
                pending_path=Path(args.file),
                to_sign_path=Path(args.output),
                is_baseline=args.baseline,
                vault_path=Path(args.vault)
            )
            sys.exit(0)
        except Exception as e:
            print(f"❌ prepare 失敗：{e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "sign":
        try:
            sign_cmd(
                to_sign_path=Path(args.input),
                signatures_path=Path(args.signatures),
                vault_path=Path(args.vault),
                meta_path=Path(args.meta) if args.meta else None
            )
            sys.exit(0)
        except Exception as e:
            print(f"❌ sign 失敗：{e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "check":
        try:
            check_file_whitelist(
                filepath=Path(args.file),
                signatures_path=Path(args.signatures),
                meta_path=Path(args.meta) if args.meta else None
            )
            sys.exit(0)
        except SystemExit as se:
            sys.exit(se.code)
        except Exception as e:
            print(f"❌ check 異常：{e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "add":
        print("❌ [指令廢止] 林納斯的事實庫嚴禁直接 add！請改用 prepare + sign 兩階段創辦人簽章流程。")
        sys.exit(1)

    else:
        check_file_whitelist()
        sys.exit(0)


if __name__ == "__main__":
    main()
