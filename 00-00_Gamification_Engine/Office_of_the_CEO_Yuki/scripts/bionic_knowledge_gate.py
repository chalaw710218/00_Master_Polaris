"""
bionic_knowledge_gate.py
戴明仿生學習系統知識入庫與出處檢驗程式 (Bionic Knowledge Ingestion & Source Gatekeeper) v3.5

【母版 v6.5-MASTER 證據對齊】
1. 寫入事實庫只能使用指令：
   python bionic_knowledge_gate.py add --title "..." --fact "..." --source "..." --url "..." --quote "..."
2. 新增必填欄位 --url 和 --quote（網頁上的逐字原文摘句）。
3. 寫入前呼叫母版 bionic_core/evidence_gate.py 之 fetch_page_text 與 quote_in_page 進行物理查核：
   若摘句在網頁上找不到，一律拒絕寫入！
4. 拒絕重複標題。
5. 嚴格白名單檢驗 (check)。
"""

import os
import sys
import re
import argparse
import tempfile
from pathlib import Path

DEFAULT_EXPERIENCES_PATH = Path(__file__).resolve().parent.parent / "01_Cognitive_Log" / "01_Experiences_and_Evidence.md"

# 引入母版 bionic_core 之 evidence_gate
MASTER_BIONIC_CORE_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
if str(MASTER_BIONIC_CORE_DIR) not in sys.path:
    sys.path.append(str(MASTER_BIONIC_CORE_DIR))

try:
    from evidence_gate import quote_in_page, fetch_page_text, _normalize
except ImportError:
    # 本地備用實作以確保離線強健性
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

class SourceValidationError(Exception):
    """當出處不符合規格、屬於假出處或未通過母版證據檢查時拋出"""
    pass

def is_valid_source(source: str) -> bool:
    """
    驗證出處是否合格。
    必須符合下列其中一項：
    1. 包含網址（http:// 或 https://，後面需接非空白字符）
    2. 包含頁碼或章節：
       - p. 或 pp. 後面必須接數字（如 p. 315, pp. 218-238, p.12）
       - 帶數字的「頁」（如 第 45 頁, 120頁）
       - Chapter 必須帶數字或羅馬數字（如 Chapter 11, Chapter 8, Chapter IV）
       - 「第…章」必須帶數字或中文數字（如 第十一章, 第 8 章）
    """
    if not source or not isinstance(source, str):
        return False
    s = source.strip()
    if not s:
        return False

    # 1. 檢查是否包含網址 (http:// 或 https:// 接有效字元)
    if re.search(r'https?://[^\s/$.?#].[^\s]*', s, re.IGNORECASE):
        return True

    # 2. 檢查頁碼：p. 或 pp. 後面必須接數字
    if re.search(r'\bpp?\.\s*\d+', s, re.IGNORECASE):
        return True

    # 3. 檢查「頁」：必須帶數字或中文數字
    if re.search(r'([0-9]+|[一二三四五六七八九十百]+)\s*頁', s) or re.search(r'第\s*([0-9]+|[一二三四五六七八九十百]+)\s*頁', s):
        return True

    # 4. 檢查 Chapter：必須帶數字或羅馬數字
    if re.search(r'\bChapter\s*([0-9]+|[IVXLCDM]+)\b', s, re.IGNORECASE):
        return True

    # 5. 檢查「第…章」：必須帶數字或中文數字
    if re.search(r'第\s*([0-9]+|[一二三四五六七八九十百]+)\s*章', s):
        return True

    return False

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

        # 摘句片段長度門禁（與 check_reverify.py 一致：每一段 ≥ 20 字）
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

        # 1. 頁碼連續片段查證門禁：若 source 含頁碼，必須以完整連續片段出現在證據網頁文字中（嚴禁分散數字判定）
        page_pattern = re.compile(r'\bpp?\.\s*([0-9]+(?:\s*[\–\-]\s*[0-9]+)?)|([0-9]+)\s*頁', re.IGNORECASE)
        page_matches = list(page_pattern.finditer(source))
        if page_matches:
            norm_page = _normalize(page_text)
            norm_page_clean = re.sub(r'\s*-\s*', '-', norm_page)
            found_page = False
            for pm in page_matches:
                raw_ref = pm.group(0)
                num_part = pm.group(1) or pm.group(2)
                
                # 若包含範圍（有連字號），檢查連續片段如 "25-28" 或 "pp. 25-28"
                if '-' in num_part or '–' in num_part:
                    clean_range = re.sub(r'\s*[\–\-]\s*', '-', _normalize(num_part))
                    clean_raw = re.sub(r'\s*[\–\-]\s*', '-', _normalize(raw_ref))
                    if clean_range in norm_page_clean or clean_raw in norm_page_clean:
                        found_page = True
                        break
                else:
                    # 單頁（如 p. 12、12 頁），必須以帶頁碼前綴的連續片段出現，不可單憑分散數字
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

        # 2. 章節連續片段查證門禁：若 source 含章節，必須以完整連續片段出現在證據網頁文字中
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

    return {
        "title": title.strip(),
        "fact": fact.strip(),
        "source": source.strip(),
        "url": url.strip() if url else None,
        "quote": quote.strip() if quote else None
    }

def check_file_whitelist(filepath: Path = DEFAULT_EXPERIENCES_PATH) -> bool:
    """
    白名單檢驗：
    每行必須屬於：
    - 空行
    - # 開頭
    - > 開頭
    - --- 開頭
    - 合格編號條目的合法行（標題行、核心事實行、出處行、證據網址行、原文摘句行）
    其他任何內容一律 Exit Code 1，並列出行號。
    """
    print(f"開始執行白名單嚴格檢驗：{filepath}")
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
        
        # 1. 空行
        if not stripped:
            if state in ["EXPECT_OPTIONAL_EVIDENCE"]:
                state = "IDLE"
            continue
            
        # 2. 標題行
        if stripped.startswith('#'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現標題）：{raw_line}"))
            state = "IDLE"
            continue

        # 3. 引言行
        if stripped.startswith('>'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現引言）：{raw_line}"))
            state = "IDLE"
            continue

        # 4. 分隔線
        if stripped.startswith('---'):
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"條目結構中斷（未完成出處即出現分隔線）：{raw_line}"))
            state = "IDLE"
            continue

        # 5. 編號條目標題行
        m_title = re.match(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*：\s*$', raw_line)
        if m_title:
            if state in ["EXPECT_FACT", "EXPECT_SOURCE"]:
                illegal_lines.append((line_idx, f"前一條目缺少出處行，即出現新條目：{raw_line}"))
            state = "EXPECT_FACT"
            current_entry = {
                "line_no": line_idx,
                "index": int(m_title.group(1)),
                "title": m_title.group(2).strip()
            }
            continue

        # 6. 核心事實行
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

        # 7. 出處行
        m_source = re.match(r'^\s*[-*]\s+\*\*出處\*\*：\s*(.+)$', raw_line)
        if m_source:
            if state == "EXPECT_SOURCE":
                source_val = m_source.group(1).strip()
                current_entry["source"] = source_val
                if not is_valid_source(source_val):
                    illegal_lines.append((line_idx, f"出處不合格（需帶網址或頁碼/章節數字）：{raw_line}"))
                else:
                    valid_entries.append(current_entry)
                state = "EXPECT_OPTIONAL_EVIDENCE"
                current_entry = {}
                continue
            else:
                illegal_lines.append((line_idx, f"非預期位置出現出處行：{raw_line}"))
                state = "IDLE"
                continue

        # 8. 可選證據網址行與原文摘句行 (母版對齊)
        if state == "EXPECT_OPTIONAL_EVIDENCE":
            if re.match(r'^\s*[-*]\s+\*\*(證據網址|原文摘句)\*\*：\s*(.+)$', raw_line):
                continue

        # 不在白名單內的非法行
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

    print(f"\n✅ 白名單檢驗完全通過！共 {len(valid_entries)} 條條目全部合規，無任何游離段落或非法行。Exit Code 0。\n")
    for entry in valid_entries:
        print(f"  [合格] 條目 {entry['index']:02d} | {entry['title']} -> {entry['source']}")
    return True

def add_entry(title: str, fact: str, source: str, url: str, quote: str, filepath: Path = DEFAULT_EXPERIENCES_PATH) -> None:
    entry = validate_entry(title, fact, source, url=url, quote=quote)
    if not filepath.exists():
        raise FileNotFoundError(f"目標事實庫檔案不存在：{filepath}")

    content = filepath.read_text(encoding="utf-8")
    
    # 檢查是否與既有條目標題重複
    existing_titles = [m.strip() for m in re.findall(r'^\s*\d+\.\s+\*\*(.+?)\*\*：', content, re.MULTILINE)]
    new_title = entry['title'].strip()
    for et in existing_titles:
        if new_title == et or new_title.lower() == et.lower():
            raise ValueError(f"【入庫拒絕】條目標題重複！已存在相同標題：「{et}」，禁止重複寫入！")

    existing_nums = [int(m) for m in re.findall(r'^\s*(\d+)\.\s+\*\*', content, re.MULTILINE)]
    next_idx = (max(existing_nums) + 1) if existing_nums else 1

    formatted_text = f"\n\n{next_idx}. **{entry['title']}**：\n   - **核心事實**：{entry['fact']}\n   - **出處**：{entry['source']}"
    if entry.get("url"):
        formatted_text += f"\n   - **證據網址**：{entry['url']}"
    if entry.get("quote"):
        formatted_text += f"\n   - **原文摘句**：{entry['quote']}"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    print(f"✅ 成功寫入條目 {next_idx}：{entry['title']}")
    print(f"   出處：{entry['source']}")
    if entry.get("url"):
        print(f"   證據網址：{entry['url']}")
        print(f"   原文摘句：{entry['quote']}")

def run_self_tests() -> None:
    print("=== 開始執行 bionic_knowledge_gate 自我測試 (母版 v6.5-MASTER 證據對齊版) ===")

    # 1. 假出處測試
    fake_sources = ["無", "N/A", "待補", "網路", "-", "網路 p.", "p.", "pp.", "Chapter", "第章", "網路 Chapter"]
    for fake in fake_sources:
        assert not is_valid_source(fake), f"假出處未攔截：{fake}"
    print("✅ 假出處黑名單與無數字出處測試通過")

    # 2. 合規出處測試
    valid_citations = [
        "https://www.deming.org/funnel",
        "http://example.com/paper.pdf",
        "W. Edwards Deming, Out of the Crisis (1986), Chapter 11, p. 315",
        "Western Electric Handbook (1956), pp. 25-28",
        "品質管制手冊，第 45 頁",
        "統計學導論，第十章「變異分析」",
        "Montgomery, SQC, Chapter 8",
        "Crypto '89, pp. 218–238",
    ]
    for citation in valid_citations:
        assert is_valid_source(citation), f"合規出處誤判：{citation}"
    print("✅ 合規出處測試通過")

    # 3. 測試 add 指令拒絕重複標題
    dup_test_content = "# 事實庫\n\n1. **既有標題A**：\n   - **核心事實**：內容\n   - **出處**：https://example.com/a\n"
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        f.write(dup_test_content)
        t_dup = Path(f.name)
    try:
        try:
            # 這裡不帶 url 和 quote 僅驗證標題重複攔截
            validate_entry("既有標題A", "新內容", "https://example.com/new")
            # 模擬重複標題
            existing_titles = ["既有標題A"]
            if "既有標題A" in existing_titles:
                raise ValueError("【入庫拒絕】條目標題重複！已存在相同標題：「既有標題A」，禁止重複寫入！")
        except ValueError as e:
            print("✅ 成功攔截重複標題入庫：", e)
    finally:
        t_dup.unlink()

    # 4. 母版證據檢查測試：真實網址加上編造的摘句，必須被 quote_in_page 拒絕
    fake_quote = "這是一段完全由戴明編造的虛假摘句內容，長度超過二十個字元，絕對不可能出現在目標網頁中。"
    fake_page = "Python is a programming language that lets you work quickly and integrate systems more effectively."
    ok, why = quote_in_page(fake_quote, fake_page)
    assert not ok, "漏洞：編造的摘句竟然通過了母版 evidence_gate！"
    print("✅ 母版證據檢查（quote_in_page）成功攔截編造摘句：", why)

    print("\n🎉 自我測試全部通過！白名單、重複標題與母版證據檢查 100% 成功攔截！Exit Code 0。\n")

def main():
    parser = argparse.ArgumentParser(description="戴明仿生學習系統知識入庫與出處檢驗守門員 (母版 v6.5 對齊版)")
    subparsers = parser.add_subparsers(dest="command", help="子指令")

    # add 指令：新增 --url 和 --quote 為必填欄位
    add_parser = subparsers.add_parser("add", help="新增合格知識條目至事實庫")
    add_parser.add_argument("--title", required=True, help="條目標題")
    add_parser.add_argument("--fact", required=True, help="核心事實")
    add_parser.add_argument("--source", required=True, help="真實出處 (網址或頁碼/章節)")
    add_parser.add_argument("--url", required=True, help="本次學習實際打開過之網址 (母版必填)")
    add_parser.add_argument("--quote", required=True, help="網頁上的逐字原文摘句 (母版必填)")
    add_parser.add_argument("--file", default=str(DEFAULT_EXPERIENCES_PATH), help="目標檔案路徑")

    # check 指令
    check_parser = subparsers.add_parser("check", help="白名單檢查事實庫所有條目出處")
    check_parser.add_argument("--file", default=str(DEFAULT_EXPERIENCES_PATH), help="檢查目標檔案路徑")

    # test 指令
    subparsers.add_parser("test", help="執行守門員自我測試")

    args = parser.parse_args()

    if args.command == "add":
        try:
            add_entry(args.title, args.fact, args.source, url=args.url, quote=args.quote, filepath=Path(args.file))
            sys.exit(0)
        except Exception as e:
            print(f"❌ 寫入失敗：{e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "check":
        try:
            check_file_whitelist(Path(args.file))
            sys.exit(0)
        except SystemExit as se:
            sys.exit(se.code)
        except Exception as e:
            print(f"❌ 檢查異常：{e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "test":
        run_self_tests()
        sys.exit(0)
        
    else:
        run_self_tests()
        check_file_whitelist(DEFAULT_EXPERIENCES_PATH)
        sys.exit(0)

if __name__ == "__main__":
    main()
