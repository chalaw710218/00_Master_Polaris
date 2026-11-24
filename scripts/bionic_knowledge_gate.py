"""
bionic_knowledge_gate.py
雪柔仿生學習系統知識入庫與出處檢驗程式 (Bionic Knowledge Ingestion Gatekeeper) v2.0

規格更新：
1. 快照檔名完全依 URL sha1 前 12 碼計算，嚴禁任何硬編碼網址判斷。
2. 法規名稱檢查：source 裡「第 N 條」前面的法規名稱，也必須出現在網頁/快照上。
3. 黑名單部分比對：source 去掉空白後，只要包含 網路、待補、N/A，或全等於 無、-、空白，即拒絕。
4. 標題重複逐行比對：某一行完全等於「### 標題」才算重複。
5. check 物理驗證：重讀快照對每條條目執行 quote_in_page，找不到快照或摘句對不上印出行號並 Exit Code 1。
"""

import argparse
import hashlib
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

FACT_BANK_PATH = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log" / "01_事實庫.md"


def get_snapshot_path(url: str) -> Path:
    norm_url = url.strip()
    h = hashlib.sha1(norm_url.encode("utf-8")).hexdigest()[:12]
    return SNAP_DIR / f"{h}.txt"


def get_page_text(url: str) -> str:
    snap = get_snapshot_path(url)
    if snap.exists():
        return snap.read_text(encoding="utf-8")
    # 無快照時線上抓取並存為快照
    text = fetch_page_text(url)
    if text and text.strip():
        SNAP_DIR.mkdir(parents=True, exist_ok=True)
        snap.write_text(text, encoding="utf-8")
    return text


def init_fact_bank():
    if not FACT_BANK_PATH.exists():
        FACT_BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
        header = """# 🏛️ 雪柔·法務認知事實庫 (Sheryl Legal Ground-Truth Fact Bank)

> 本事實庫為雪柔特化版仿生學習系統唯一法定事實來源。
> 嚴禁手動編輯，所有條目必須透過 `bionic_knowledge_gate.py add` 經物理查核通過後始得寫入。

---
"""
        FACT_BANK_PATH.write_text(header, encoding="utf-8")


def cmd_add(title: str, url: str, quote: str, source: str) -> (bool, str):
    init_fact_bank()

    # 1. 檢查參數非空
    if not title or not title.strip():
        return False, "標題不得為空"
    if not url or not url.strip() or not re.match(r"^https?://", url.strip()):
        return False, "網址無效或不得為空"
    if not quote or not quote.strip():
        return False, "原文摘句不得為空"
    if not source or not source.strip():
        return False, "出處名稱不得為空"

    t = title.strip()
    u = url.strip()
    q = quote.strip()
    s = source.strip()

    # 2. source 黑名單部分比對
    s_clean = re.sub(r"\s+", "", s)
    s_lower = s_clean.lower()
    if any(k in s_lower for k in ["網路", "待補", "n/a"]):
        return False, f"出處名稱 '{s}' 包含禁用關鍵字（網路/待補/N/A）"
    if s_clean in ["無", "-", "空白", "none", "null"]:
        return False, f"出處名稱 '{s}' 屬於禁用出處"

    # 3. 標題重複逐行比對
    bank_text = FACT_BANK_PATH.read_text(encoding="utf-8")
    target_header = f"### {t}"
    for line in bank_text.splitlines():
        if line.strip() == target_header:
            return False, f"標題重複：'{t}' 已存在於事實庫中"

    # 4. 抓取網頁 / 快照（依 URL sha1）
    try:
        page_text = get_page_text(u)
    except Exception as e:
        return False, f"抓不到網頁（{e}），拒絕入庫"

    if not page_text or not page_text.strip():
        return False, "網頁內容為空，拒絕入庫"

    clean_page = re.sub(r"\s+", "", page_text)

    # 5. 法規名稱與條號連續性檢查
    m_law_art = re.search(r"^(.+?)\s*第\s*([0-9\-一二三四五六七八九十]+)\s*條", s)
    if m_law_art:
        law_name = m_law_art.group(1).strip()
        art_no = m_law_art.group(2).strip()
        clean_law = re.sub(r"\s+", "", law_name)
        target_art = f"第{art_no}條"

        # 檢查法規名稱必須出現在網頁文字上
        if clean_law and clean_law not in clean_page:
            return False, f"出處所載法規名稱 '{clean_law}' 未在網頁文字中出現"

        # 檢查條號必須出現在網頁文字上
        if target_art not in clean_page:
            return False, f"出處所載條號 '{target_art}' 去除空白後未在網頁文字中連續出現"
    else:
        # 單純包含「第 X 條」
        m_article = re.search(r"第\s*([0-9\-一二三四五六七八九十]+)\s*條", s)
        if m_article:
            target_art = f"第{m_article.group(1)}條"
            if target_art not in clean_page:
                return False, f"出處所載條號 '{target_art}' 去除空白後未在網頁文字中連續出現"

    # 6. quote_in_page 驗證
    ok, why = quote_in_page(q, page_text)
    if not ok:
        return False, f"摘句比對失敗：{why}"

    # 7. 通過驗證，寫入事實庫
    entry_text = f"\n### {t}\n出處：{s} {u}\n原文：「{q}」\n\n---\n"
    with open(FACT_BANK_PATH, "a", encoding="utf-8") as f:
        f.write(entry_text)

    return True, f"成功寫入條目：{t}"


def cmd_check() -> (bool, int, list):
    if not FACT_BANK_PATH.exists():
        print(f"❌ 錯誤：事實庫檔案不存在：{FACT_BANK_PATH}")
        sys.exit(1)

    lines = FACT_BANK_PATH.read_text(encoding="utf-8").splitlines()
    illegal_lines = []
    
    total_entries = 0
    state = "IDLE"  # IDLE -> EXPECT_SOURCE -> EXPECT_QUOTE -> EXPECT_SEPARATOR

    current_title = ""
    current_url = ""
    current_quote = ""
    url_line_no = 0
    quote_line_no = 0

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.strip()

        # 空行：允許
        if not line:
            continue

        # 頂層標題、二級標題、引言行：允許（僅在非條目中間）
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

        # 分隔線
        if line == "---":
            if state == "EXPECT_SEPARATOR":
                # 執行快照物理核驗
                snap = get_snapshot_path(current_url)
                if not snap.exists():
                    illegal_lines.append((url_line_no, f"找不到出處對應的快照檔案（URL: {current_url}，預期快照: {snap.name}）"))
                else:
                    snap_text = snap.read_text(encoding="utf-8")
                    ok, why = quote_in_page(current_quote, snap_text)
                    if not ok:
                        illegal_lines.append((quote_line_no, f"物理核驗失敗：快照中找不到原文摘句（{why}）"))

                total_entries += 1
                state = "IDLE"
                current_title = ""
                current_url = ""
                current_quote = ""
            elif state == "IDLE":
                pass
            else:
                illegal_lines.append((idx, f"條目未完成即出現分隔線：{raw_line}"))
                state = "IDLE"
            continue

        # 條目標題：### 開頭
        if line.startswith("### "):
            if state != "IDLE":
                illegal_lines.append((idx, f"前一條目未完成即出現新條目標題：{raw_line}"))
            current_title = line[4:].strip()
            state = "EXPECT_SOURCE"
            continue

        # 出處行
        if line.startswith("出處："):
            m_url = re.search(r"https?://\S+", line)
            if m_url and state == "EXPECT_SOURCE":
                current_url = m_url.group(0).strip()
                url_line_no = idx
                state = "EXPECT_QUOTE"
                continue
            else:
                illegal_lines.append((idx, f"出處行格式不合法或非預期位置：{raw_line}"))
                state = "IDLE"
                continue

        # 原文行
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

        # 不在白名單之內的任何其他行
        illegal_lines.append((idx, f"非法行（非白名單格式）：{raw_line}"))

    # 若檔案結尾條目未完成分隔線，但包含完整要素
    if state == "EXPECT_SEPARATOR":
        snap = get_snapshot_path(current_url)
        if not snap.exists():
            illegal_lines.append((url_line_no, f"找不到出處對應的快照檔案（URL: {current_url}）"))
        else:
            snap_text = snap.read_text(encoding="utf-8")
            ok, why = quote_in_page(current_quote, snap_text)
            if not ok:
                illegal_lines.append((quote_line_no, f"物理核驗失敗：快照中找不到原文摘句（{why}）"))
        total_entries += 1
        state = "IDLE"

    return (len(illegal_lines) == 0), total_entries, illegal_lines


def main():
    parser = argparse.ArgumentParser(description="雪柔仿生學習知識入庫與白名單門禁 v2.0")
    subparsers = parser.add_subparsers(dest="command")

    # add
    p_add = subparsers.add_parser("add", help="將驗證過的知識條目寫入事實庫")
    p_add.add_argument("--title", required=True, help="條目標題")
    p_add.add_argument("--url", required=True, help="來源網址")
    p_add.add_argument("--quote", required=True, help="網頁逐字原文摘句")
    p_add.add_argument("--source", required=True, help="出處名稱")

    # check
    p_check = subparsers.add_parser("check", help="檢查事實庫白名單與格式，並重新物理核驗每筆條目")

    args = parser.parse_args()

    if args.command == "add":
        ok, msg = cmd_add(args.title, args.url, args.quote, args.source)
        if ok:
            print(f"✅ [ADD_SUCCESS] {msg}")
            sys.exit(0)
        else:
            print(f"❌ [ADD_REJECTED] {msg}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "check":
        ok, count, illegals = cmd_check()
        print("=" * 60)
        print("bionic_knowledge_gate check 白名單與物理核驗報告")
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
            print("✅ 白名單檢驗與物理核驗全部通過，零違法行！")
            print("Exit Code: 0")
            sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
