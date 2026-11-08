import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

session_path = Path("scripts/threads_session.json")
permalink = "https://www.threads.net/@hellotaitung/post/DffGsoeCUEw"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    print(f"導航至正確短網址: {permalink}")
    page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
    page.wait_for_timeout(4000)
    
    proof = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\shadow_midnight_with_image_verified.png")
    page.screenshot(path=str(proof))
    print(f"📸 驗收截圖完成: {proof.name}")
    browser.close()
