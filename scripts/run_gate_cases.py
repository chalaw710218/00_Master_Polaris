import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
YUKI_SCRIPTS_DIR = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "scripts"
if str(YUKI_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(YUKI_SCRIPTS_DIR))

try:
    from bionic_knowledge_gate import validate_entry, SourceValidationError
except ImportError as e:
    print(f"無法載入 bionic_knowledge_gate: {e}", file=sys.stderr)
    sys.exit(1)

TESTS_DIR = PROJECT_ROOT / "scripts" / "tests"


def parse_case_file(filepath: Path) -> dict:
    content = filepath.read_text(encoding="utf-8")
    
    # 提取預期判定
    expected = None
    if "【應退回】" in content:
        expected = "應退回"
    elif "【應通過】" in content:
        expected = "應通過"
        
    # 提取網址
    url = None
    m_url = re.search(r'(?:[-*]\s+)?(?:\*\*)?網址(?:\*\*)?[：:]\s*(https?://\S+)', content)
    if m_url:
        url = m_url.group(1).strip()
        
    # 提取出處
    source = None
    m_src = re.search(r'(?:[-*]\s+)?(?:\*\*)?出處(?:\*\*)?[：:]\s*(.+)', content)
    if m_src:
        source = m_src.group(1).strip()
        
    # 提取摘句（摘句：或摘句內容：）
    quote = None
    m_quote = re.search(r'(?:[-*]\s+)?(?:\*\*)?摘句(?:內容)?(?:\*\*)?[：:]\s*(.+)', content)
    if m_quote:
        quote = m_quote.group(1).strip()
        
    return {
        "filename": filepath.name,
        "expected": expected,
        "url": url,
        "source": source,
        "quote": quote
    }


def main():
    if not TESTS_DIR.exists():
        print(f"❌ 測試目錄不存在：{TESTS_DIR}", file=sys.stderr)
        sys.exit(1)
        
    case_files = sorted(list(TESTS_DIR.glob("case_*.md")))
    if not case_files:
        print(f"❌ 找不到任何測試案例檔案在 {TESTS_DIR}", file=sys.stderr)
        sys.exit(1)
        
    print(f"開始執行門禁案例驗證，共找到 {len(case_files)} 個案例檔案...\n")
    
    all_matched = True
    
    for case_file in case_files:
        case_info = parse_case_file(case_file)
        fname = case_info["filename"]
        expected = case_info["expected"]
        url = case_info["url"]
        source = case_info["source"]
        quote = case_info["quote"]
        
        print(f"--- 測試案例: {fname} ---")
        if not expected:
            print(f"❌ [判定失敗] {fname} 未標註【應退回】或【應通過】！")
            all_matched = False
            continue
            
        if not url:
            print(f"❌ [判定失敗] {fname} 找不到網址！")
            all_matched = False
            continue
            
        if not source:
            print(f"❌ [判定失敗] {fname} 找不到出處！")
            all_matched = False
            continue
            
        if not quote:
            print(f"❌ [判定失敗] {fname} 找不到摘句內容！")
            all_matched = False
            continue
            
        # 執行 validate_entry
        actual_result = None
        error_msg = ""
        try:
            res = validate_entry(
                title=f"測試案例_{fname}",
                fact=quote,
                source=source,
                url=url,
                quote=quote
            )
            actual_result = "應通過"
        except (SourceValidationError, ValueError) as e:
            actual_result = "應退回"
            error_msg = str(e)
        except Exception as e:
            actual_result = "未預期例外"
            error_msg = str(e)
            
        is_match = (actual_result == expected)
        print(f"預期結果: 【{expected}】 | 實際結果: 【{actual_result}】 | 一致性: {is_match}")
        if not is_match:
            print(f"❌ 錯誤詳細資訊: {error_msg}")
            all_matched = False
        else:
            if actual_result == "應退回":
                print(f"   (退回原因: {error_msg})")
            else:
                print(f"   (成功通過物理查核)")
        print()
        
    if all_matched:
        print("✅ 所有門禁測試案例與標註完全一致！Exit Code 0。")
        sys.exit(0)
    else:
        print("❌ 部分案例與標註不一致或格式錯誤！Exit Code 1。")
        sys.exit(1)


if __name__ == "__main__":
    main()
