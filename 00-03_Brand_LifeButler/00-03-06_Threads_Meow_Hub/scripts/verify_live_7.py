import sys
from pathlib import Path

MASTER_BIONIC_CORE_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
if str(MASTER_BIONIC_CORE_DIR) not in sys.path:
    sys.path.append(str(MASTER_BIONIC_CORE_DIR))

from evidence_gate import fetch_page_text, quote_in_page
import json

data = json.load(open('data/_本批待簽.json', encoding='utf-8'))
print("=== 基準批次 7 條即時連網逐字驗證結果 ===")
for idx, e in enumerate(data['entries'], 1):
    url = e['url']
    quote = e['quote']
    try:
        page = fetch_page_text(url)
        ok, reason = quote_in_page(quote, page)
        status = "✅ 逐字驗證 PASS" if ok else f"❌ FAIL ({reason})"
    except Exception as ex:
        status = f"❌ 抓取錯誤 ({ex})"
    print(f"[{idx:02d}/07] {e['title']}")
    print(f"       網址: {url}")
    print(f"       結果: {status}")
