import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from reciprocal_visitor import visit_and_reply_page, SESSION_PATH

def main():
    target = "janietaichung"
    comment = "早安！看你分享的生活步調很舒服～新的一週開工順利，工作忙碌之餘也要記得給自己留一杯茶的休息時間喔！🍵✨"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH) if SESSION_PATH.exists() else None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        print(f"🚀 啟動登門回訪: @{target}")
        success = visit_and_reply_page(page, target, comment)
        print(f"回訪結果: {success}")
        browser.close()

if __name__ == "__main__":
    main()
