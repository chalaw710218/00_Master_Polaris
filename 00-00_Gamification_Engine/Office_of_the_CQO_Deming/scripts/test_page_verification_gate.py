"""
test_page_verification_gate.py
測試案例：
1. 網頁文字含「vol. 12」與「18 March」，出處寫「pp. 12-18」→ 應拒絕（不可因分散數字放行）
2. 網頁文字含「vol. 12」與「18 March」，出處寫「Chapter 9」→ 應拒絕（章節必須連續出現）
3. 網頁文字真實存在「pp. 25– 28」，出處寫「pp. 25-28」→ 應通過
4. 純網址出處 → 應通過
"""

import sys
from pathlib import Path

# 加入主程式路徑
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))

import bionic_knowledge_gate
from bionic_knowledge_gate import validate_entry, SourceValidationError

def run_test():
    print("=======================================================")
    print("  戴明出處連續片段查證門禁自動化測試 (Strict Fragment Verification)")
    print("=======================================================\n")

    # 模擬網頁文字：只有 vol. 12 與 18 March，沒有連續的 12-18，也沒有 Chapter 9
    mock_html_text = "Published in Journal of Quality, vol. 12, released on 18 March 2020. This is verbatim quote for testing."
    real_mock_quote = "This is verbatim quote for testing"
    test_url = "https://example.com/test-article"

    orig_fetcher = bionic_knowledge_gate.fetch_page_text
    bionic_knowledge_gate.fetch_page_text = lambda u: mock_html_text

    try:
        # [測試 1] 分散數字欺瞞測試：出處寫 pp. 12-18（應拒絕）
        print("[測試 1] 網頁含 'vol. 12' 與 '18 March'，出處寫 'pp. 12-18'...")
        try:
            validate_entry(
                title="測試_分散數字欺瞞",
                fact="測試核心事實",
                source="Journal of Quality, pp. 12-18",
                url=test_url,
                quote=real_mock_quote
            )
            print("❌ 測試 1 失敗：分散數字未被連續片段門禁攔截，居然放行！")
            sys.exit(1)
        except SourceValidationError as e:
            print(f"✅ 測試 1 通過！成功阻斷分散數字：\n   👉 {e}\n")

        # [測試 2] 未查證章節測試：出處寫 Chapter 9（應拒絕）
        print("[測試 2] 網頁無 Chapter 9，出處寫 'Chapter 9'...")
        try:
            validate_entry(
                title="測試_未查證章節",
                fact="測試核心事實",
                source="Journal of Quality, Chapter 9",
                url=test_url,
                quote=real_mock_quote
            )
            print("❌ 測試 2 失敗：未查證章節未被攔截，居然放行！")
            sys.exit(1)
        except SourceValidationError as e:
            print(f"✅ 測試 2 通過！成功阻斷未查證章節：\n   👉 {e}\n")

        # [測試 3] 單頁前綴欺瞞測試：出處寫 p. 12（網頁只有 vol. 12，無 p. 12，應拒絕）
        print("[測試 3] 網頁只有 'vol. 12'，出處寫 'p. 12'...")
        try:
            validate_entry(
                title="測試_單頁前綴缺失",
                fact="測試核心事實",
                source="Journal of Quality, p. 12",
                url=test_url,
                quote=real_mock_quote
            )
            print("❌ 測試 3 失敗：缺乏頁碼前綴連續片段居然放行！")
            sys.exit(1)
        except SourceValidationError as e:
            print(f"✅ 測試 3 通過！成功阻斷無頁碼前綴之單頁：\n   👉 {e}\n")

        # [測試 4] 純網址出處測試（無頁碼，應通過）
        print("[測試 4] 出處為純網址（無頁碼，應通過）...")
        try:
            entry = validate_entry(
                title="測試_純網址出處",
                fact="測試核心事實",
                source=test_url,
                url=test_url,
                quote=real_mock_quote
            )
            print(f"✅ 測試 4 通過！純網址順利放行：{entry['source']}\n")
        except Exception as e:
            print(f"❌ 測試 4 失敗：純網址被誤拒！{e}")
            sys.exit(1)

    finally:
        bionic_knowledge_gate.fetch_page_text = orig_fetcher

    # [測試 5] 真實網路連線測試：Western Electric 頁面包含真實連續片段「pp. 25– 28」，出處寫 pp. 25-28（應通過）
    print("[測試 5] 真實 Wikipedia 連線測試：Western Electric rules 真實連續頁碼 pp. 25-28...")
    real_wiki_url = "https://en.wikipedia.org/wiki/Western_Electric_rules"
    real_wiki_quote = "decision rules in statistical process control"
    real_source = "Western Electric Company, Statistical Quality Control Handbook (1956), pp. 25-28"

    try:
        entry = validate_entry(
            title="測試_真實連續頁碼",
            fact="測試核心事實",
            source=real_source,
            url=real_wiki_url,
            quote=real_wiki_quote
        )
        print("✅ 測試 5 通過！真實存在之連續頁碼片段成功放行。\n")
    except Exception as e:
        print(f"❌ 測試 5 失敗：真實連續頁碼被誤拒！{e}")
        sys.exit(1)

    print("=======================================================")
    print("🎉 連續片段查證門禁全部測試通過！Exit Code 0。")
    print("=======================================================")

if __name__ == "__main__":
    run_test()
