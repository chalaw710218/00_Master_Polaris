"""
Polaris AI Cabinet - Facebook One-Time Login Helper
===================================================
引導創辦人完成一次性安全登入，完成後自動偵測並儲存永久 Session 鑰匙。
"""

import os
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

USER_DATA_DIR = os.path.expanduser(r"~\.gemini\polaris_fb_browser_data")

def main():
    print("=" * 60, flush=True)
    print("極星 AI 託管瀏覽器 —— 一次性安全登入助手", flush=True)
    print("=" * 60, flush=True)
    print("[*] 正在為您拉起 Chrome 視窗...", flush=True)
    print("[*] 設定檔存放於:", USER_DATA_DIR, flush=True)
    print("\n👉 請在彈出的瀏覽器視窗中登入您的 Facebook 個人帳號。", flush=True)
    print("👉 登入成功後，本程式會自動偵測並為您妥善保存鑰匙，隨後自動關閉視窗！\n", flush=True)

    os.makedirs(USER_DATA_DIR, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport=None
        )
        
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto("https://www.facebook.com", wait_until="domcontentloaded", timeout=90000)
        except Exception as e:
            print(f"[*] 頁面導航提醒: {e}", flush=True)
        
        logged_in = False
        print("[*] 視窗已就緒，等待登入中（最多等待 5 分鐘）...", flush=True)
        for i in range(150):
            time.sleep(2)
            try:
                content = page.content()
                has_login_box = 'id="email"' in content or 'name="email"' in content
                is_login_url = "login" in page.url
                
                # 若已經不在登入頁面，且進入 facebook.com 主畫面
                if not has_login_box and not is_login_url and "facebook.com" in page.url:
                    logged_in = True
                    break
            except:
                pass
                
        if logged_in:
            print("\n" + "=" * 60, flush=True)
            print("🎉 恭喜！偵測到 Facebook 登入成功！", flush=True)
            print("🔒 Session 鑰匙已永久鎖定於極星安全環境中。", flush=True)
            print("=" * 60, flush=True)
            time.sleep(3)
        else:
            print("\n[-] 逾時或尚未完成登入。如需重新登入，請再次執行本程式。", flush=True)
            
        ctx.close()

if __name__ == "__main__":
    main()
