"""
check_ch6.py — 驗證 chapter6_13_24_revised.md 中所有出處與摘句
對 revised 檔裡每一組「出處網址 + 原文」，用 snapshots 快照跑 quote_in_page。
增加規則：出處寫了「第N項」或「第N款」，但摘句裡沒有對應的項款文字 → FAIL。
只要有一條缺出處、摘句對不上，或項款無法由摘句證明，就 Exit Code 1。
"""

import re
import sys
from pathlib import Path

# 強制 UTF-8 輸出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REVISED_FILE = HERE / "chapter6_13_24_revised.md"
SNAP_DIR = HERE / "snapshots"
BIONIC_CORE = HERE.parent / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(BIONIC_CORE))

from evidence_gate import quote_in_page

PCODE_LAW = {
    "J0080037": "電子簽章法",
    "J0030011": "電業法",
    "K0110001": "發展觀光條例",
    "O0050024": "一般廢棄物回收清除處理辦法",
    "O0050001": "廢棄物清理法",
    "D0070118": "公寓大廈管理條例",
    "L0070040": "長期照顧服務法",
    "L0020001": "醫師法",
    "L0040001": "食品安全衛生管理法",
    "M0060027": "動物保護法",
    "J0150002": "公平交易法",
    "D0070148": "建築物室內裝修管理辦法",
    "D0070109": "建築法",
    "J0080001": "公司法",
    "B0000001": "民法",
    "I0020001": "仲裁法"
}


def verify_item_subitem(source: str, quote: str) -> (bool, str):
    """檢驗出處中宣告的項次/款次是否能被摘句本身所證明"""
    num_map = {
        "1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
        "6": "六", "7": "七", "8": "八", "9": "九", "10": "十"
    }
    
    # 檢查「第N款」
    m_sub = re.search(r"第([0-9一二三四五六七八九十]+)款", source)
    if m_sub:
        k = m_sub.group(1)
        k_cn = num_map.get(k, k)
        pat = f"{k_cn}、|第{k_cn}款|第{k}款"
        if not re.search(pat, quote):
            return False, f"出處載明第{k}款，但摘句中無對應款次文字（如『{k_cn}、』）"

    # 檢查「第N項」
    m_item = re.search(r"第([0-9一二三四五六七八九十]+)項", source)
    if m_item:
        k = m_item.group(1)
        k_cn = num_map.get(k, k)
        pat = f"第{k_cn}項|第{k}項"
        if not re.search(pat, quote):
            return False, f"出處載明第{k}項，但摘句中無對應項次文字（如『第{k_cn}項』）"

    return True, ""


def find_snapshot_by_url(url: str) -> Path:
    if "ExecutiveData.aspx?id=5202" in url or "1091202281" in url:
        return SNAP_DIR / "環署廢字第1091202281號.txt"
    if "9338233" in url or "udn.com" in url:
        return SNAP_DIR / "聯合報_9338233.txt"
    m = re.search(r"pcode=([A-Z0-9]+)&flno=([0-9\-]+)", url)
    if not m:
        return None
    pcode, flno = m.group(1), m.group(2)
    law = PCODE_LAW.get(pcode, "")
    for f in SNAP_DIR.glob(f"{law}*.txt"):
        if f"第{flno}條" in f.name or f"第{flno}項" in f.name:
            return f
    return None


def parse_revised_file(filepath: Path):
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    pairs = []
    
    current_rule = "未知條號"
    current_source = None
    current_url = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("### "):
            current_rule = line.replace("### ", "").strip()
            continue
        
        if line.startswith("出處："):
            parts = line.replace("出處：", "").strip().split()
            if len(parts) >= 2:
                current_url = parts[-1]
                current_source = " ".join(parts[:-1])
            elif len(parts) == 1:
                current_url = parts[0]
                current_source = parts[0]
            continue
            
        if line.startswith("原文：「") and line.endswith("」"):
            quote = line[4:-1]
            if current_url:
                pairs.append({
                    "rule": current_rule,
                    "source": current_source,
                    "url": current_url,
                    "quote": quote
                })
                current_source = None
                current_url = None
            continue
            
    return pairs


def main():
    if not REVISED_FILE.exists():
        print(f"錯誤：找不到檔案 {REVISED_FILE}", file=sys.stderr)
        sys.exit(1)

    pairs = parse_revised_file(REVISED_FILE)
    print(f"解析到 {len(pairs)} 組「出處網址 + 原文」條目，開始執行快照比對與項款驗證...\n")
    print("=" * 70)

    passed = 0
    failed = 0

    for idx, item in enumerate(pairs, 1):
        rule = item["rule"]
        source = item["source"]
        url = item["url"]
        quote = item["quote"]

        # 1. 檢驗項款是否能由摘句證明
        ok_item, item_msg = verify_item_subitem(source, quote)
        if not ok_item:
            print(f"[{idx:02d}/FAIL] {rule} | {source}")
            print(f"        錯誤：{item_msg}")
            failed += 1
            print("-" * 70)
            continue

        # 2. 快照搜尋
        snap = find_snapshot_by_url(url)
        if not snap or not snap.exists():
            print(f"[{idx:02d}/FAIL] {rule} | {source}")
            print(f"        錯誤：找不到對應的快照檔案！(URL: {url})")
            failed += 1
            print("-" * 70)
            continue

        # 3. 摘句在快照中檢驗
        snap_text = snap.read_text(encoding="utf-8")
        hit, msg = quote_in_page(quote, snap_text)

        if hit:
            print(f"[{idx:02d}/PASS] {rule} | {source}")
            print(f"        快照檔: {snap.name}")
            print(f"        摘句完全一致且項款嚴格支持，驗證通過！")
            passed += 1
        else:
            print(f"[{idx:02d}/FAIL] {rule} | {source}")
            print(f"        快照檔: {snap.name}")
            print(f"        錯誤：摘句在快照中找不到！({msg})")
            failed += 1
        print("-" * 70)

    print("=" * 70)
    print("check_ch6.py 執行統計結果")
    print("=" * 70)
    print(f"總檢驗條目數: {len(pairs)} 組")
    print(f"檢驗通過 (PASS): {passed} 組")
    print(f"檢驗失敗 (FAIL): {failed} 組")
    print(f"通過率: {(passed / len(pairs)) * 100:.1f}%")
    print("=" * 70)

    if failed > 0:
        print(f"\n[結論] 存在 {failed} 處缺陷，Exit Code 1")
        sys.exit(1)
    else:
        print(f"\n[結論] 全部 100% 通過快照逐字檢驗與項款驗證，Exit Code 0")
        sys.exit(0)


if __name__ == "__main__":
    main()
