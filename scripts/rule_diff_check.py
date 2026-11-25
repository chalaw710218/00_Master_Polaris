#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/rule_diff_check.py
======================================================================
極星技能重構「規則不遺失」審查工具 (Rule Diff & Zero-Loss Checker v2.1)
======================================================================
專門驗證母體技能拆分至原子技能（atom-*）過程中，所有物理參數、
工程數值、單位、比例、色票、閘門代碼與實質規則是否 100% 被保留（只能搬家，不可遺失）。

特性 (v2.1):
1. 【完整邊界比對】：精確鎖定前後邊界，防範偽匹配（例如「50%」絕不因提案中有「250%」而誤判通過）。
2. 【4-gram 逐行語義比對】：
   - 提取原始檔案每一行（去除空白與標點後長度 >= 12 字者），切分成 4 字片段。
   - 計算在提案檔案中的覆蓋比例，比例 < 0.6 之行視為潛在遺失規則。
3. 【嚴格白名單審批狀態機】：
   - 標註「品碩核准刪除」：判定為合法刪除，通過。
   - 標註「待品碩核准」：列出為待審批項目，一律視為未通過 (Exit Code 1)。
   - 未在白名單中者：列為違規遺失，一律視為未通過 (Exit Code 1)。
4. 【通用參數介面】：
   python scripts/rule_diff_check.py --orig 原檔1 原檔2 ... --prop 提案1 提案2 ...
   若未帶參數，預設檢查「做海報組」。
"""

import sys
import re
import argparse
from pathlib import Path


def normalize_latex(text: str) -> str:
    """清理 LaTeX 語法標籤，便於純文字與數值比對"""
    cleaned = re.sub(r'\\text\{([a-zA-Z%]+)\}', r'\1', text)
    cleaned = cleaned.replace(r'^\circ', '°').replace(r'\circ', '°')
    return cleaned


def clean_text_for_shingles(text: str) -> str:
    """去除所有空白、標點符號與 Markdown 特殊標記，僅保留中英文字與數字"""
    norm = normalize_latex(text)
    return re.sub(r'[\s\W_]+', '', norm)


def extract_tokens(text: str) -> dict:
    """從文本中抽取所有規則、參數、代碼與數值"""
    norm = normalize_latex(text)

    pcts = set(re.findall(r'\b\d+(?:\.\d+)?%', norm))
    unit_pattern = r'\b\d+(?:\.\d+)?\s*(?:pt|mm|cm|gsm|px|DPI|dpi|deg|em)\b'
    units = set(re.findall(unit_pattern, norm, re.IGNORECASE))
    zh_pattern = r'\d+(?:\.\d+)?\s*(?:公尺|公分|度|模組)'
    zh_units = set(re.findall(zh_pattern, norm))
    ratios = set(re.findall(r'\b\d+(?:\.\d+)?:\d+(?:\.\d+)?\b', norm))
    hex_codes = set(re.findall(r'#[0-9a-fA-F]{6}\b', norm))
    g_codes = set(re.findall(r'\bG-\d{2}\b', norm))

    return {
        'Percentages': pcts,
        'Units': units,
        'Chinese Units': zh_units,
        'Ratios': ratios,
        'Hex Codes': hex_codes,
        'Gate Codes': g_codes,
    }


def is_token_in_text_exact(token: str, target_norm: str) -> bool:
    """
    完整邊界精確匹配：
    確保「50%」不會因為目標中有「250%」或「150%」而誤判匹配；
    確保「4mm」不會因為有「24mm」而誤判匹配。
    支援數字與單位間有或無空白 (例如 '300 DPI' 與 '300DPI')。
    """
    clean_token = re.sub(r'\s+', '', token)

    # 1. 色票代碼 (例如 #1A1D20, #F8F9FA)
    if token.startswith('#'):
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(token) + r'(?![0-9a-zA-Z])'
    # 2. 安燈閘門代碼 (例如 G-01, G-11)
    elif token.startswith('G-'):
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(token) + r'(?![0-9a-zA-Z])'
    # 3. 比例 (例如 1:1.18, 7:1, 4:5)
    elif ':' in token:
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(token) + r'(?![0-9a-zA-Z])'
    # 4. 數值加英文/百分比單位 (例如 50%, 300 DPI, 4mm, 12pt, 0.5em)
    elif re.match(r'^(\d+(?:\.\d+)?)\s*([a-zA-Z%]+)$', token):
        num, unit = re.match(r'^(\d+(?:\.\d+)?)\s*([a-zA-Z%]+)$', token).groups()
        suffix_boundary = r'(?![0-9a-zA-Z%])' if unit.endswith('%') else r'(?![0-9a-zA-Z])'
        pattern = r'(?<![0-9a-zA-Z.])' + re.escape(num) + r'\s*' + re.escape(unit) + suffix_boundary
    # 5. 數值加中文單位 (例如 3 公尺, 4 模組, 45 度)
    elif re.match(r'^(\d+(?:\.\d+)?)\s*([\u4e00-\u9fff]+)$', token):
        num, unit = re.match(r'^(\d+(?:\.\d+)?)\s*([\u4e00-\u9fff]+)$', token).groups()
        pattern = r'(?<![0-9a-zA-Z.])' + re.escape(num) + r'\s*' + re.escape(unit) + r'(?![0-9a-zA-Z])'
    # 6. 其他通用代碼
    else:
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(clean_token) + r'(?![0-9a-zA-Z])'

    return bool(re.search(pattern, target_norm, re.IGNORECASE))


def load_allowlist(allowlist_path: Path) -> list:
    """
    載入核准刪除白名單：
    解析每一行及其狀態（'APPROVED': 品碩核准刪除, 'PENDING': 待品碩核准）
    """
    if not allowlist_path.exists():
        return []
    entries = []
    lines = allowlist_path.read_text(encoding="utf-8").splitlines()
    for l in lines:
        l_str = l.strip()
        if not l_str or l_str.startswith("#"):
            continue
        if "品碩核准刪除" in l_str:
            entries.append({'raw': l_str, 'status': 'APPROVED'})
        elif "待品碩核准" in l_str:
            entries.append({'raw': l_str, 'status': 'PENDING'})
    return entries


def is_secret_token_line(line: str) -> bool:
    """判斷是否為敏感密鑰行（如 Meta Access Token, API Key 等）"""
    norm = line.strip()
    return bool(re.search(r"^\s*TOKEN\s*=\s*['\"][A-Za-z0-9_-]{30,}['\"]", norm))


def match_line_against_allowlist(raw_line: str, allowlist_entries: list) -> tuple:
    """檢查某行是否命中白名單，回傳 (狀態, 條目內容)"""
    # 支援敏感金鑰脫敏匹配
    if is_secret_token_line(raw_line):
        for entry in allowlist_entries:
            if "REDACTED" in entry['raw'] and "TOKEN" in entry['raw']:
                return entry['status'], entry['raw']

    clean_target = clean_text_for_shingles(raw_line)
    for entry in allowlist_entries:
        clean_entry = clean_text_for_shingles(entry['raw'])
        if clean_target in clean_entry or clean_entry in clean_target or any(
            s in clean_entry for s in [clean_target[:16], clean_target[-16:]] if len(clean_target) >= 16
        ):
            return entry['status'], entry['raw']
    return 'UNAUTHORIZED', None


def check_rule_diff(orig_paths: list, prop_paths: list, allowlist_path: Path) -> tuple:
    """
    執行規則比對，回傳 (is_success, stats_dict)
    """
    print("=" * 75)
    print("🔍 極星技能重構「規則不遺失」審查工具 (Rule Diff Checker v2.1)")
    print("=" * 75)

    # 零密鑰洩漏安全檢查 (Zero-Secret-Leak Gate)
    secret_pattern = re.compile(r"EAA[0-9a-zA-Z]{30,}")
    for p in prop_paths:
        p_obj = Path(p)
        if p_obj.exists() and secret_pattern.search(p_obj.read_text(encoding="utf-8")):
            print(f"❌ 致命資安紅線：在提案檔案中偵測到明文 Meta Access Token：{p_obj}！")
            return False, {'error': f"明文金鑰外洩: {p_obj}"}
    if allowlist_path.exists() and secret_pattern.search(allowlist_path.read_text(encoding="utf-8")):
        print(f"❌ 致命資安紅線：在白名單檔案中偵測到明文 Meta Access Token：{allowlist_path}！")
        return False, {'error': f"明文金鑰外洩: {allowlist_path}"}

    orig_files_data = []
    for p in orig_paths:
        path_obj = Path(p)
        if not path_obj.exists():
            print(f"❌ 找不到原始檔案：{path_obj}")
            return False, {'error': f"找不到原始檔案: {path_obj}"}
        content = path_obj.read_text(encoding="utf-8")
        orig_files_data.append((path_obj, content))

    prop_text_combined = ""
    for p in prop_paths:
        path_obj = Path(p)
        if not path_obj.exists():
            print(f"❌ 找不到提案檔案：{path_obj}")
            return False, {'error': f"找不到提案檔案: {path_obj}"}
        prop_text_combined += path_obj.read_text(encoding="utf-8") + "\n"

    prop_norm = normalize_latex(prop_text_combined)
    prop_clean_all = clean_text_for_shingles(prop_text_combined)

    allowlist_entries = load_allowlist(allowlist_path)
    print(f"📄 已載入白名單條目：{len(allowlist_entries)} 項")

    # 1. 第一階段：數值與邊界比對
    print("\n----------------------------------------------------------------------")
    print("📊【第一階段：數值與物理標準完整邊界比對】")
    all_orig_text = "\n".join(content for _, content in orig_files_data)
    orig_tokens_by_cat = extract_tokens(all_orig_text)
    all_orig_count = sum(len(s) for s in orig_tokens_by_cat.values())
    print(f"📋 原始技能抽取規則代碼總數：{all_orig_count} 項")

    missing_tokens_by_cat = {}
    for cat, tokens in orig_tokens_by_cat.items():
        missing_in_cat = []
        for token in sorted(tokens):
            if not is_token_in_text_exact(token, prop_norm):
                missing_in_cat.append(token)
        if missing_in_cat:
            missing_tokens_by_cat[cat] = missing_in_cat

    token_pass = len(missing_tokens_by_cat) == 0
    for cat, tokens in orig_tokens_by_cat.items():
        missing = missing_tokens_by_cat.get(cat, [])
        status = "✅ PASS" if not missing else f"❌ MISSING ({len(missing)})"
        print(f"  • {cat:<16}: {len(tokens) - len(missing)}/{len(tokens)} 通過 [{status}]")

    if missing_tokens_by_cat:
        print("\n🚨【第一階段未通過：以下物理參數未在提案中完整保留】：")
        for cat, missing in missing_tokens_by_cat.items():
            print(f"  [{cat}]")
            for m in missing:
                print(f"    - ❌ {m}")

    # 2. 第二階段：4-gram 逐行語義比對 (長度 >= 12)
    print("\n----------------------------------------------------------------------")
    print("📝【第二階段：4-gram 逐行語義完整度比對 (閾值 0.6)】")

    failing_lines = []
    allowed_lines = []
    pending_lines = []
    total_evaluated_lines = 0

    for path_obj, content in orig_files_data:
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            cl = clean_text_for_shingles(line)
            if len(cl) >= 12:
                total_evaluated_lines += 1
                shingles = [cl[i:i+4] for i in range(len(cl) - 3)]
                matches = sum(1 for s in shingles if s in prop_clean_all)
                ratio = matches / len(shingles) if shingles else 1.0

                if ratio < 0.6:
                    status, reason = match_line_against_allowlist(line, allowlist_entries)
                    item_info = {
                        'file': path_obj.name,
                        'line_num': idx,
                        'ratio': ratio,
                        'text': line.strip(),
                        'reason': reason
                    }
                    if status == 'APPROVED':
                        allowed_lines.append(item_info)
                    elif status == 'PENDING':
                        pending_lines.append(item_info)
                    else:
                        failing_lines.append(item_info)

    print(f"📋 逐行審查評估行數 (長度>=12)：{total_evaluated_lines} 行")
    print(f"  • 匹配率 >= 0.6 完全保留    : {total_evaluated_lines - len(failing_lines) - len(allowed_lines) - len(pending_lines)} 行 [✅ PASS]")
    print(f"  • 匹配率 < 0.6 經品碩核准刪除: {len(allowed_lines)} 行 [✅ APPROVED]")
    print(f"  • 匹配率 < 0.6 標註待品碩核准: {len(pending_lines)} 行 [⏳ PENDING]")
    print(f"  • 匹配率 < 0.6 未經核准遺失  : {len(failing_lines)} 行 [{'❌ FAIL' if failing_lines else '✅ 0'}]")

    print("\n----------------------------------------------------------------------")
    print("📋【所有匹配率低於 0.6 之行清單】：")
    if not allowed_lines and not pending_lines and not failing_lines:
        print("  (無任何低於 0.6 之行，100% 行文語義皆已保留)")
    else:
        for item in allowed_lines:
            print(f"  [✅ 核准刪除] [{item['file']}:L{item['line_num']}] (比率 {item['ratio']:.2f}): {item['text']}")
        for item in pending_lines:
            print(f"  [⏳ 待品碩核准] [{item['file']}:L{item['line_num']}] (比率 {item['ratio']:.2f}): {item['text']}")
            if item['reason']:
                print(f"      ↳ 白名單待審項: {item['reason']}")
        for item in failing_lines:
            print(f"  [❌ 違規遺失] [{item['file']}:L{item['line_num']}] (比率 {item['ratio']:.2f}): {item['text']}")

    # 3. 決策輸出
    print("=" * 75)
    success = token_pass and len(failing_lines) == 0 and len(pending_lines) == 0

    stats = {
        'total_tokens': all_orig_count,
        'missing_tokens': len(missing_tokens_by_cat),
        'total_evaluated_lines': total_evaluated_lines,
        'approved_lines': len(allowed_lines),
        'pending_lines': len(pending_lines),
        'failing_lines': len(failing_lines),
    }

    if success:
        print("🎉【零遺失驗收通過 (Exit Code 0)】")
        print(f"  1. 所有 {all_orig_count} 項物理數值、色票、比例與閘門代碼 100% 完整匹配！")
        print(f"  2. 全文 {total_evaluated_lines} 條重要規則語義比對通過（{len(allowed_lines)} 條格式行經品碩核准刪除）！")
        print("=" * 75)
        return True, stats
    else:
        print("❌【驗收未通過 (Exit Code 1)】")
        if not token_pass:
            print("  - 第一階段有物理數值遺失。")
        if pending_lines:
            print(f"  - 第二階段有 {len(pending_lines)} 條標註「待品碩核准」，需創辦人親自審批後方可生效。")
        if failing_lines:
            print(f"  - 第二階段有 {len(failing_lines)} 條文字規則未經核准刪除，嚴禁出廠！")
        print("=" * 75)
        return False, stats


def main():
    parser = argparse.ArgumentParser(description="極星技能重構「規則不遺失」審查工具 (Rule Diff & Zero-Loss Checker v2.1)")
    parser.add_argument("--orig", nargs="+", help="原始檔案清單")
    parser.add_argument("--prop", nargs="+", help="提案檔案清單")
    parser.add_argument("--allowlist", default="scripts/rule_diff_allowlist.txt", help="核准刪除白名單路徑")

    args = parser.parse_args()
    allowlist_path = Path(args.allowlist)

    if args.orig and args.prop:
        orig_files = args.orig
        prop_files = args.prop
    else:
        # 預設做海報組
        orig_files = [
            ".agents/skills/polaris-poster-artisan/_archive/SKILL_20261126_規範前.md",
            ".agents/skills/atoms/atom-poster-print-andon/_archive/SKILL_20261126_規範前.md",
            ".agents/skills/atoms/atom-poster-grid-architect/_archive/SKILL_20261126_規範前.md",
        ]
        prop_files = [
            "_proposed/poster/polaris-poster-artisan/SKILL.md",
            "_proposed/poster/atom-poster-print-andon/SKILL.md",
            "_proposed/poster/atom-poster-grid-architect/SKILL.md",
        ]

    success, _ = check_rule_diff(orig_files, prop_files, allowlist_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
