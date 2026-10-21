import sys
import time
from pathlib import Path

# 確保 Windows 終端機支援 Emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def login_and_save_session():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 請先安裝 Playwright: pip install playwright && playwright install chromium")
        return False

    session_path = Path(__file__).resolve().parent / "threads_session.json"

    print("==================================================")
    print("🔑 [北極星 Threads Web 登入憑證授權精靈]")
    print("==================================================")
    print("即將啟動瀏覽器視窗，請在跳出的視窗中完成 Threads 帳號登入。")
    print("登入成功後，系統會自動捕捉 Session 並存檔，日後即可完全無人值守自動留言！\n")

    with sync_playwright() as p:
        # 啟動可視化瀏覽器供創辦人登入
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            locale="zh-TW"
        )
        page = context.new_page()
        page.goto("https://www.threads.net/login")

        print("🌐 瀏覽器已開啟登入頁面，請在視窗內完成登入...")
        print("💡 提示：若您已登入完成看到 Threads 動態牆，請在終端機按下 [Enter] 鍵繼續，或等待系統自動偵測...")

        # 循環偵測登入狀態
        logged_in = False
        start_time = time.time()
        while time.time() - start_time < 300: # 最多等待 5 分鐘
            cookies = context.cookies()
            cookie_names = [c["name"] for c in cookies]
            # 檢查關鍵驗證 Cookie
            if "sessionid" in cookie_names or "ds_user_id" in cookie_names:
                # 再次確認不在 login 頁面
                if "login" not in page.url:
                    logged_in = True
                    break
            time.sleep(2)

        if logged_in:
            print("\n🎉 偵測到登入成功！正在固化 Session 憑證...")
            time.sleep(3) # 等待完整 token 寫入
            context.storage_state(path=str(session_path))
            print(f"✅ 憑證已成功保存至: {session_path}")
            browser.close()
            return True
        else:
            print("\n⚠️ 等待超時或尚未完成登入。")
            browser.close()
            return False

if __name__ == "__main__":
    login_and_save_session()
