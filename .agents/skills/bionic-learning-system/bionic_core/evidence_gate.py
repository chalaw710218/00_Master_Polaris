"""
evidence_gate.py — 仿生學習入帳前的證據檢查（只用 Python 標準庫）

用法：
    from evidence_gate import check_evidence
    ok, reasons = check_evidence("kage_cycle_11_real.json")
    if not ok:
        raise ValueError("入帳拒絕：" + "；".join(reasons))

證據 JSON 必要欄位：
    source_url    : 來源網址（http/https）
    quote_status  : "verbatim"（逐字原文摘句）或 "summary_only"（僅有搜尋摘要）
    quote         : 摘句或摘要內容

規則：
    1. 沒有 source_url → 拒絕
    2. quote_status 不是兩種之一 → 拒絕
    3. verbatim：程式實際抓網頁，摘句必須出現在網頁文字裡，對不上 → 拒絕
       （網頁抓不到也拒絕，請改標 summary_only）
    4. summary_only：內容不准出現百分比數字（數字只能來自逐字原文）
"""

import html
import json
import re
import sys
import urllib.request

STATUS_ALIASES = {
    "verbatim": "verbatim", "逐字原文摘句": "verbatim", "【逐字原文摘句】": "verbatim",
    "summary_only": "summary_only", "僅有搜尋摘要": "summary_only", "【僅有搜尋摘要】": "summary_only",
}


def _normalize(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("engagement-bait", "engagement bait")
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def fetch_page_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (evidence_gate)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="ignore")
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    return re.sub(r"(?s)<[^>]+>", " ", raw)


def quote_in_page(quote: str, page_text: str, min_fragment: int = 20) -> tuple:
    """摘句可用 ... 或 … 省略中段；每一段（≥ min_fragment 字元）都必須出現在網頁裡。"""
    page = _normalize(page_text)
    fragments = [f.strip(" \"'.") for f in re.split(r"\.\.\.|…", _normalize(quote))]
    fragments = [f for f in fragments if len(f) >= min_fragment]
    if not fragments:
        return False, "摘句太短，無法驗證（每段至少 %d 字元）" % min_fragment
    missing = [f for f in fragments if f not in page]
    if missing:
        return False, "網頁中找不到這段摘句：「%s」" % missing[0][:60]
    return True, ""


def check_evidence(path: str, fetcher=fetch_page_text) -> tuple:
    reasons = []
    try:
        with open(path, encoding="utf-8") as f:
            ev = json.load(f)
    except Exception as e:
        return False, ["證據檔讀取失敗：%s" % e]

    url = str(ev.get("source_url", "")).strip()
    status = STATUS_ALIASES.get(str(ev.get("quote_status", "")).strip())
    quote = str(ev.get("quote", "")).strip()

    if not re.match(r"^https?://\S+\.\S+", url):
        reasons.append("缺少有效的 source_url")
    if status is None:
        reasons.append("quote_status 必須是 verbatim 或 summary_only")
    if not quote:
        reasons.append("quote 是空的")
    if reasons:
        return False, reasons

    if status == "verbatim":
        try:
            page = fetcher(url)
        except Exception as e:
            return False, ["抓不到網頁（%s），無法證明是逐字原文；請改標 summary_only" % e]
        ok, why = quote_in_page(quote, page)
        if not ok:
            reasons.append(why)
    else:
        if re.search(r"\d+(\.\d+)?\s*%", quote):
            reasons.append("僅有搜尋摘要的內容不准出現百分比數字")

    return (not reasons), reasons


if __name__ == "__main__":
    # 命令列：python evidence_gate.py kage_cycle_*.json
    all_ok = True
    for p in sys.argv[1:]:
        ok, why = check_evidence(p)
        all_ok &= ok
        print(("✅ " if ok else "❌ ") + p + ("" if ok else "：" + "；".join(why)))
    sys.exit(0 if all_ok else 1)
