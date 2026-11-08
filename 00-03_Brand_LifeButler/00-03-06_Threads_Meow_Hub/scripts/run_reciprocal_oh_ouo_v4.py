import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path("scripts/threads_session.json")
screenshot_dir = Path("scripts/screenshots")
screenshot_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    target_url = "https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP"
    print(f"前往目標貼文: {target_url}")
    page.goto(target_url, wait_until="networkidle")
    page.wait_for_timeout(4000)
    
    # 點擊對話氣泡以激活輸入框
    bubble = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"]').first
    if bubble.is_visible():
        bubble.click(force=True)
        page.wait_for_timeout(1500)
    
    # 聚焦輸入框
    reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
    reply_box.click(force=True)
    page.wait_for_timeout(500)
    
    warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
    
    page.keyboard.type(warm_comment, delay=25)
    page.wait_for_timeout(1500)
    
    # 尋找那個 36x36 的圓形發布按鈕
    buttons = page.locator('div[role="button"]').all()
    submit_btn = None
    for b in buttons:
        if b.is_visible():
            box = b.bounding_box()
            if box:
                # 黑色圓形向上箭頭按鈕寬高通常是 36x36 (或 32~40 之間)，且 y 在 550 ~ 650 之間
                if 30 <= box['width'] <= 42 and 30 <= box['height'] <= 42 and 550 <= box['y'] <= 650:
                    print(f"🎯 鎖定 36x36 發布按鈕: pos=({box['x']}, {box['y']}, w={box['width']}, h={box['height']})")
                    submit_btn = b
                    break
                    
    if submit_btn:
        print("點擊發布按鈕！")
        submit_btn.click(force=True)
    else:
        print("未精確匹配到 36x36 按鈕，點擊座標 (792, 597)...")
        page.mouse.click(792, 597)
        
    print("等待 7 秒等待發布與頁面渲染...")
    page.wait_for_timeout(7000)
    
    final_proof = screenshot_dir / "reciprocal_oh_ouo_verified.png"
    page.screenshot(path=str(final_proof))
    print(f"🎉 最終成果截圖已保存: {final_proof.name}")
    
    # 同時另存至 brain artifacts 目錄供報告使用
    artifact_proof = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\reciprocal_oh_ouo_verified.png")
    page.screenshot(path=str(artifact_proof))
    print(f"📸 已同步至 Artifacts 目錄: {artifact_proof.name}")

    browser.close()
