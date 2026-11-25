"""
bionic_knowledge_gate.py
雪柔仿生學習系統知識入庫與出處檢驗程式 (Bionic Knowledge Ingestion Gatekeeper) v4.0

規格升級（創辦人主權簽章接軌版）：
1. add 改為寫入 01_Cognitive_Log/00_待簽章區.md，不再直接寫入事實庫；validate_entry 物理核驗全部照舊。
2. sign 指令（由創辦人品碩親自執行）：
   a. 列出待簽章區所有條目明細（反盲簽展示）
   b. payload = {"action":"fact_ingest","office":"falcon","entries_sha256":<每條條目文字的sha256清單>}
   c. 呼叫 founder_auth.sign_founder_action(payload)
   d. 簽章成功後將條目搬進 01_事實庫.md，簽章存到 01_事實庫.sigs.jsonl，清空待簽章區
3. check 加上創辦人簽章驗證：
   事實庫中每一條的 sha256，都必須出現在某一行已通過 verify_founder_action 的簽章批次中；找不到或驗簽失敗印出行號並 Exit Code 1。
   （若事實庫為空，條目數為 0，則直接 Exit Code 0）。
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# 強制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
SNAP_DIR = HERE / "snapshots"
BIONIC_CORE = WORKSPACE / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(BIONIC_CORE))

from evidence_gate import quote_in_page, fetch_page_text, _normalize
import founder_auth

LOG_DIR = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log"
PENDING_BANK_PATH = LOG_DIR / "00_待簽章區.md"
FACT_BANK_PATH = LOG_DIR / "01_事實庫.md"
SIGS_PATH = LOG_DIR / "01_事實庫.sigs.jsonl"


def canon_entry_text(title: str, source: str, url: str, quote: str) -> str:
    """條目標準化字串格式（用於精確計算 sha256）"""
    return f"### {title.strip()}\n出處：{source.strip()} {url.strip()}\n原文：「{quote.strip()}」"


def compute_entry_sha256(title: str, source: str, url: str, quote: str) -> str:
    return hashlib.sha256(canon_entry_text(title, source, url, quote).encode("utf-8")).hexdigest()


def get_snapshot_path(url: str) -> Path:
    norm_url = url.strip()
    h = hashlib.sha1(norm_url.encode("utf-8")).hexdigest()[:12]
    return SNAP_DIR / f"{h}.txt"


def get_page_text(url: str) -> str:
    snap = get_snapshot_path(url)
    if snap.exists():
        return snap.read_text(encoding="utf-8")
    text = fetch_page_text(url)
    if text and text.strip():
        SNAP_DIR.mkdir(parents=True, exist_ok=True)
        snap.write_text(text, encoding="utf-8")
    return text


def extract_page_title(page_text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", page_text, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    for line in page_text.splitlines():
        line = line.strip()
        if line and not line.startswith("<!--"):
            return line
    return ""


def validate_entry(source: str, url: str, quote: str, page_text: str) -> (bool, str):
    """
    統一驗證知識條目（add 與 check 共用）：
    1. 參數完整性
    2. 黑名單部分比對（網路、待補、N/A、無、-、空白）
    3. 法規名稱檢查：比對網頁標題行（防範導覽列熱門詞彙滲漏與不完整簡稱）
    4. 條號連續性檢查
    5. quote_in_page 原文摘句物理核驗
    """
    if not source or not source.strip():
        return False, "出處名稱不得為空"
    if not url or not url.strip() or not re.match(r"^https?://", url.strip()):
        return False, "網址無效或不得為空"
    if not quote or not quote.strip():
        return False, "原文摘句不得為空"
    if not page_text or not page_text.strip():
        return False, "網頁內容為空，拒絕入庫"

    s = source.strip()
    u = url.strip()
    q = quote.strip()

    # 1. 黑名單部分比對
    s_clean = re.sub(r"\s+", "", s)
    s_lower = s_clean.lower()
    if any(k in s_lower for k in ["網路", "待補", "n/a"]):
        return False, f"出處名稱 '{s}' 包含禁用關鍵字（網路/待補/N/A）"
    if s_clean in ["無", "-", "空白", "none", "null"]:
        return False, f"出處名稱 '{s}' 屬於禁用出處"

    # 2. 網頁標題與法規名稱完全比對
    page_title = extract_page_title(page_text)
    if not page_title:
        return False, "快照/網頁中找不到有效的標題行，拒絕入庫"

    clean_title = re.sub(r"\s+", "", page_title)
    clean_page = re.sub(r"\s+", "", page_text)

    # 出處包含「法規名稱 第 N 條」
    m_law_art = re.search(r"^(.+?)\s*第\s*([0-9\-一二三四五六七八九十]+)\s*條", s)
    if m_law_art:
        law_name = m_law_art.group(1).strip()
        art_no = m_law_art.group(2).strip()
        clean_law = re.sub(r"\s+", "", law_name)
        target_art = f"第{art_no}條"

        # 嘗試從標題行中提取完整法定法規名稱（以 &#167; 或 § 分隔）
        m_full_law = re.split(r"&#167;|§", clean_title)
        if len(m_full_law) >= 2 and m_full_law[0]:
            expected_full_law = m_full_law[0].strip()
            # 必須完全等於法定完整法規名稱（徹底阻斷 B10「條例」、B11「觀光」等不完整縮寫）
            if clean_law != expected_full_law:
                return False, f"出處法規名稱 '{clean_law}' 不完整或不符，法定完整名稱為 '{expected_full_law}'"
        else:
            # 標題行無 &#167; 或 § 時，回退至標題行包含比對
            if clean_law and clean_law not in clean_title:
                return False, f"出處所載法規名稱 '{clean_law}' 未在網頁標題（{page_title}）中出現"

        # 條號必須出現在網頁文字上
        if target_art not in clean_page:
            return False, f"出處所載條號 '{target_art}' 去除空白後未在網頁文字中連續出現"
    else:
        m_article = re.search(r"第\s*([0-9\-一二三四五六七八九十]+)\s*條", s)
        if m_article:
            target_art = f"第{m_article.group(1)}條"
            if target_art not in clean_page:
                return False, f"出處所載條號 '{target_art}' 去除空白後未在網頁文字中連續出現"

    # 3. quote_in_page 物理摘句核驗
    ok, why = quote_in_page(q, page_text)
    if not ok:
        return False, f"摘句比對失敗：{why}"

    return True, "驗證合格"


def init_buffers():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not PENDING_BANK_PATH.exists():
        header_pending = """# ⏳ 雪柔·法務認知待簽章區 (Sheryl Pending Ingestion Buffer)

> 本區條目已通過物理證據核驗，等待創辦人（品碩）親自審批並簽章入庫。
> 未經創辦人 Schnorr 密碼學簽章，嚴禁直接併入事實庫。

---
"""
        PENDING_BANK_PATH.write_text(header_pending, encoding="utf-8")

    if not FACT_BANK_PATH.exists():
        header_fact = """# 🏛️ 雪柔·法務認知事實庫 (Sheryl Legal Ground-Truth Fact Bank)

> 本事實庫為雪柔特化版仿生學習系統唯一法定事實來源。
> 嚴禁手動編輯，所有條目必須透過 `bionic_knowledge_gate.py sign` 經創辦人親自審批簽章後始得寫入。

---
"""
        FACT_BANK_PATH.write_text(header_fact, encoding="utf-8")


def parse_entries_from_markdown(content: str) -> list[dict]:
    """解析 Markdown 內容中的所有合規條目"""
    entries = []
    lines = content.splitlines()
    
    current_title = None
    current_source = None
    current_url = None
    current_quote = None
    title_line = 0
    url_line = 0
    quote_line = 0

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("### "):
            current_title = line[4:].strip()
            title_line = idx
            current_source = None
            current_url = None
            current_quote = None
            continue
        if line.startswith("出處："):
            parts = line[3:].strip().split()
            if len(parts) >= 2 and re.match(r"^https?://", parts[-1]):
                current_url = parts[-1].strip()
                current_source = " ".join(parts[:-1]).strip()
                url_line = idx
            continue
        if line.startswith("原文：「") and line.endswith("」"):
            current_quote = line[4:-1].strip()
            quote_line = idx
            if current_title and current_source and current_url and current_quote:
                sha256 = compute_entry_sha256(current_title, current_source, current_url, current_quote)
                entries.append({
                    "title": current_title,
                    "source": current_source,
                    "url": current_url,
                    "quote": current_quote,
                    "title_line": title_line,
                    "url_line": url_line,
                    "quote_line": quote_line,
                    "sha256": sha256
                })
                current_title = None
                current_source = None
                current_url = None
                current_quote = None
            continue
    return entries


def cmd_add(title: str, url: str, quote: str, source: str) -> (bool, str):
    init_buffers()

    if not title or not title.strip():
        return False, "標題不得為空"
    t = title.strip()

    # 標題重複檢查（待簽章區與事實庫都不准重複）
    target_header = f"### {t}"
    if PENDING_BANK_PATH.exists():
        for line in PENDING_BANK_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip() == target_header:
                return False, f"標題重複：'{t}' 已存在於待簽章區中"

    if FACT_BANK_PATH.exists():
        for line in FACT_BANK_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip() == target_header:
                return False, f"標題重複：'{t}' 已存在於事實庫中"

    # 取得網頁 / 快照
    try:
        page_text = get_page_text(url.strip())
    except Exception as e:
        return False, f"抓不到網頁（{e}），拒絕入庫"

    # 呼叫統一驗證函式
    ok, msg = validate_entry(source, url, quote, page_text)
    if not ok:
        return False, msg

    # 寫入待簽章區
    entry_text = f"\n### {t}\n出處：{source.strip()} {url.strip()}\n原文：「{quote.strip()}」\n\n---\n"
    with open(PENDING_BANK_PATH, "a", encoding="utf-8") as f:
        f.write(entry_text)

    return True, f"成功寫入待簽章區：{t}"


def cmd_sign(
    meta_path: Path | None = None,
    _test_passphrase: str | None = None,
    pending_path: Path | None = None,
    fact_path: Path | None = None,
    sigs_path: Path | None = None
) -> (bool, str):
    """創辦人親自審批待簽章區條目並產生密碼學簽章入庫"""
    init_buffers()
    p_path = pending_path or PENDING_BANK_PATH
    f_path = fact_path or FACT_BANK_PATH
    s_path = sigs_path or SIGS_PATH

    if not p_path.exists():
        return False, "待簽章區不存在"
    content = p_path.read_text(encoding="utf-8")
    entries = parse_entries_from_markdown(content)
    
    if not entries:
        return False, "待簽章區為空，無任何條目需簽章"

    # 1. 簽章前先對每一條執行物理快照核驗（嚴禁手動假條目混入待簽章區）
    for idx, e in enumerate(entries, 1):
        snap = get_snapshot_path(e["url"])
        if not snap.exists():
            msg = f"簽章前驗證失敗（第 {idx} 條「{e['title']}」找不到對應快照：{snap.name}），整批拒絕簽章！"
            print(f"❌ [SIGN_PRE_CHECK_FAIL] {msg}", file=sys.stderr)
            return False, msg
        snap_text = snap.read_text(encoding="utf-8")
        ok, why = validate_entry(e["source"], e["url"], e["quote"], snap_text)
        if not ok:
            msg = f"簽章前驗證失敗（第 {idx} 條「{e['title']}」不合規：{why}），整批拒絕簽章！"
            print(f"❌ [SIGN_PRE_CHECK_FAIL] {msg}", file=sys.stderr)
            return False, msg

    print("\n" + "=" * 65)
    print("📜 雪柔待簽章法規條目清單 (反盲簽核對明細)")
    print("=" * 65)
    sha_list = []
    for idx, e in enumerate(entries, 1):
        print(f"[{idx:02d}] 標題：{e['title']}")
        print(f"     出處：{e['source']} ({e['url']})")
        print(f"     原文：{e['quote'][:60]}...")
        print(f"     雜湊：{e['sha256']}")
        print("-" * 65)
        sha_list.append(e["sha256"])

    payload = {
        "action": "fact_ingest",
        "office": "falcon",
        "entries_sha256": sha_list
    }

    try:
        sig_bundle = founder_auth.sign_founder_action(
            payload,
            meta_path=meta_path,
            _test_passphrase=_test_passphrase,
            prompt_label="創辦人（品碩）授權口令："
        )
    except Exception as e:
        return False, f"簽章失敗或取消：{e}"

    # 簽章成功，將待簽章區條目追加進事實庫
    fact_append_lines = []
    for e in entries:
        fact_append_lines.append(f"\n### {e['title']}\n出處：{e['source']} {e['url']}\n原文：「{e['quote']}」\n\n---\n")

    with open(f_path, "a", encoding="utf-8") as f:
        f.write("".join(fact_append_lines))

    # 將簽章紀錄存入 .sigs.jsonl
    sig_record = {
        "payload": payload,
        "sig_bundle": sig_bundle
    }
    with open(s_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(sig_record, ensure_ascii=False) + "\n")

    # 清空待簽章區
    header_pending = """# ⏳ 雪柔·法務認知待簽章區 (Sheryl Pending Ingestion Buffer)

> 本區條目已通過物理證據核驗，等待創辦人（品碩）親自審批並簽章入庫。
> 未經創辦人 Schnorr 密碼學簽章，嚴禁直接併入事實庫。

---
"""
    p_path.write_text(header_pending, encoding="utf-8")

    return True, f"成功完成 {len(entries)} 筆條目之創辦人簽章入庫！"


def cmd_check(
    fact_bank_path: Path | None = None,
    sigs_path: Path | None = None,
    meta_path: Path | None = None
) -> (bool, int, list):
    fb_path = fact_bank_path or FACT_BANK_PATH
    sig_path = sigs_path or SIGS_PATH

    if not fb_path.exists():
        print(f"❌ 錯誤：事實庫檔案不存在：{fb_path}")
        sys.exit(1)

    content = fb_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    illegal_lines = []
    
    total_entries = 0
    state = "IDLE"

    current_title = ""
    current_source = ""
    current_url = ""
    current_quote = ""
    url_line_no = 0
    quote_line_no = 0

    parsed_entries = []

    # 1. 白名單格式檢查與條目物理核驗
    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# ") or line.startswith("## "):
            if state != "IDLE":
                illegal_lines.append((idx, f"條目結構中斷（出現章節標題）：{raw_line}"))
                state = "IDLE"
            continue

        if line.startswith(">"):
            if state != "IDLE":
                illegal_lines.append((idx, f"條目結構中斷（出現引言）：{raw_line}"))
                state = "IDLE"
            continue

        if line == "---":
            if state == "EXPECT_SEPARATOR":
                # 執行快照物理核驗（找不到快照就 FAIL）
                snap = get_snapshot_path(current_url)
                if not snap.exists():
                    illegal_lines.append((url_line_no, f"找不到出處對應的快照檔案（URL: {current_url}，預期快照: {snap.name}）"))
                else:
                    snap_text = snap.read_text(encoding="utf-8")
                    ok, why = validate_entry(current_source, current_url, current_quote, snap_text)
                    if not ok:
                        illegal_lines.append((quote_line_no, f"條目核驗失敗（法規名稱/條號/摘句不符）：{why}"))

                sha = compute_entry_sha256(current_title, current_source, current_url, current_quote)
                parsed_entries.append({
                    "title": current_title,
                    "sha256": sha,
                    "line_no": quote_line_no
                })
                total_entries += 1
                state = "IDLE"
                current_title = ""
                current_source = ""
                current_url = ""
                current_quote = ""
            elif state == "IDLE":
                pass
            else:
                illegal_lines.append((idx, f"條目未完成即出現分隔線：{raw_line}"))
                state = "IDLE"
            continue

        if line.startswith("### "):
            if state != "IDLE":
                illegal_lines.append((idx, f"前一條目未完成即出現新條目標題：{raw_line}"))
            current_title = line[4:].strip()
            state = "EXPECT_SOURCE"
            continue

        if line.startswith("出處："):
            parts = line[3:].strip().split()
            if len(parts) >= 2 and re.match(r"^https?://", parts[-1]):
                current_url = parts[-1].strip()
                current_source = " ".join(parts[:-1]).strip()
                url_line_no = idx
                state = "EXPECT_QUOTE"
                continue
            else:
                illegal_lines.append((idx, f"出處行格式不合法（需包含出處名稱與網址）：{raw_line}"))
                state = "IDLE"
                continue

        if line.startswith("原文：「") and line.endswith("」"):
            if state == "EXPECT_QUOTE":
                current_quote = line[4:-1].strip()
                quote_line_no = idx
                state = "EXPECT_SEPARATOR"
                continue
            else:
                illegal_lines.append((idx, f"非預期位置出現原文行：{raw_line}"))
                state = "IDLE"
                continue

        illegal_lines.append((idx, f"非法行（非白名單格式）：{raw_line}"))

    if state == "EXPECT_SEPARATOR":
        snap = get_snapshot_path(current_url)
        if not snap.exists():
            illegal_lines.append((url_line_no, f"找不到出處對應的快照檔案（URL: {current_url}）"))
        else:
            snap_text = snap.read_text(encoding="utf-8")
            ok, why = validate_entry(current_source, current_url, current_quote, snap_text)
            if not ok:
                illegal_lines.append((quote_line_no, f"條目核驗失敗（法規名稱/條號/摘句不符）：{why}"))
        sha = compute_entry_sha256(current_title, current_source, current_url, current_quote)
        parsed_entries.append({
            "title": current_title,
            "sha256": sha,
            "line_no": quote_line_no
        })
        total_entries += 1
        state = "IDLE"

    # 2. 創辦人密碼學簽章驗證
    if total_entries == 0:
        # 事實庫為空，無條目需簽章核對，通過
        return (len(illegal_lines) == 0), total_entries, illegal_lines

    # 事實庫非空，必須存在簽章檔且每條條目的 sha256 都在已驗簽的批次中
    if not sig_path.exists():
        illegal_lines.append((1, f"事實庫包含 {total_entries} 筆條目，但找不到創辦人簽章檔案 ({sig_path.name})，全庫未授權！"))
        return False, total_entries, illegal_lines

    verified_sha256_set = set()
    sig_lines = sig_path.read_text(encoding="utf-8").splitlines()
    target_meta_path = meta_path or founder_auth.DEFAULT_META_PATH

    for sig_idx, s_line in enumerate(sig_lines, 1):
        s_line = s_line.strip()
        if not s_line:
            continue
        try:
            record = json.loads(s_line)
            payload = record.get("payload", {})
            sig_bundle = record.get("sig_bundle", {})

            # 門禁安全檢查：負載必須為雪柔法規入庫 (action=fact_ingest, office=falcon)
            act = payload.get("action")
            off = payload.get("office")
            if act != "fact_ingest" or off != "falcon":
                illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行負載不符（預期 action=fact_ingest, office=falcon，實際 action={act}, office={off}），判定為無效簽章！"))
                continue

            ok_sig, why_sig = founder_auth.verify_founder_action(payload, sig_bundle, meta_path=target_meta_path)
            if not ok_sig:
                illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行驗簽失敗：{why_sig}"))
            else:
                for sha in payload.get("entries_sha256", []):
                    verified_sha256_set.add(sha)
        except Exception as e:
            illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行解析異常：{e}"))

    # 逐條檢查事實庫條目是否在合法簽章中
    for item in parsed_entries:
        if item["sha256"] not in verified_sha256_set:
            illegal_lines.append((item["line_no"], f"條目未經創辦人有效簽章授權入庫（標題: {item['title']}，SHA256: {item['sha256'][:16]}...）"))

    return (len(illegal_lines) == 0), total_entries, illegal_lines


def main():
    parser = argparse.ArgumentParser(description="雪柔仿生學習知識入庫與創辦人簽章門禁 v4.0")
    subparsers = parser.add_subparsers(dest="command")

    # add
    p_add = subparsers.add_parser("add", help="將驗證過的知識條目寫入待簽章區")
    p_add.add_argument("--title", required=True, help="條目標題")
    p_add.add_argument("--url", required=True, help="來源網址")
    p_add.add_argument("--quote", required=True, help="網頁逐字原文摘句")
    p_add.add_argument("--source", required=True, help="出處名稱")

    # sign
    p_sign = subparsers.add_parser("sign", help="創辦人親自審批待簽章區並簽章入庫")

    # check
    p_check = subparsers.add_parser("check", help="檢查事實庫白名單、物理快照與創辦人密碼學簽章")

    args = parser.parse_args()

    if args.command == "add":
        ok, msg = cmd_add(args.title, args.url, args.quote, args.source)
        if ok:
            print(f"✅ [ADD_SUCCESS] {msg}")
            sys.exit(0)
        else:
            print(f"❌ [ADD_REJECTED] {msg}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "sign":
        ok, msg = cmd_sign()
        if ok:
            print(f"✅ [SIGN_SUCCESS] {msg}")
            sys.exit(0)
        else:
            print(f"❌ [SIGN_FAILED] {msg}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "check":
        ok, count, illegals = cmd_check()
        print("=" * 60)
        print("bionic_knowledge_gate check 白名單、物理核驗與創辦人簽章報告")
        print("=" * 60)
        print(f"事實庫路徑: {FACT_BANK_PATH}")
        print(f"合格條目總數: {count} 條（由程式計算）")
        print(f"違規行總數: {len(illegals)} 行")
        if illegals:
            print("-" * 60)
            print("違規明細：")
            for line_no, reason in illegals:
                print(f"  [第 {line_no:4d} 行] {reason}")
            print("-" * 60)
            print("❌ 檢驗未通過，Exit Code: 1")
            sys.exit(1)
        else:
            print("=" * 60)
            print("✅ 白名單、物理核驗與創辦人簽章全部驗證通過！")
            print("Exit Code: 0")
            sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
