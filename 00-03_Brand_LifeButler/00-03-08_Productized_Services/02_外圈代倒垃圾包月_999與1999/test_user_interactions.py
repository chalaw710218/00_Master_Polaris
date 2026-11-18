# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

ONLINE_URL = "https://chalaw710218.github.io/taitung-trash-radar/"

console_logs = []
page_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 414, "height": 896})
    page.on("console", lambda m: console_logs.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    page.goto(ONLINE_URL, wait_until="networkidle")
    time.sleep(2)

    # 模擬操作 1：切換出發時間
    print("Testing time input change...")
    page.fill("#trashTimeInput", "18:30")
    page.dispatch_event("#trashTimeInput", "change")
    time.sleep(1)

    # 模擬操作 2：點擊切換【一般垃圾 ＋ 資源回收】雙收
    print("Testing recycle toggle...")
    page.click("#recycleBox")
    time.sleep(1)

    # 模擬操作 3：切換交通工具 (機車 -> 走路 -> 開車)
    print("Testing travel mode switch...")
    page.click("button:has-text('步行')")
    time.sleep(1)
    page.click("button:has-text('開車')")
    time.sleep(1)
    page.click("button:has-text('騎機車')")
    time.sleep(1)

    browser.close()

print(f"Post-interaction Page Errors: {len(page_errors)}")
for err in page_errors:
    print("❌", err)

assert len(page_errors) == 0, "Interaction caused page errors!"
print("🟢 All user interactions (time, recycle, travelMode) executed with ZERO errors!")
