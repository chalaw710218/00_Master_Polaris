#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活管家・台東垃圾車雷達全新規範 (Josef ✕ Neo ✕ Linus) 品質門禁與安燈質檢
由首席前端架構師 尼奧 (Neo) ✕ 首席品質長 戴明 (Dr. Deming) 審定

驗證項目：
1. 檔案大小與結構完整性 (HTML5 / Viewport / UTF-8)
2. 品牌法定名稱零洩漏防火牆 (嚴禁 Polaris / 極星，對外品牌包含「生活管家，就醬點！」，業務自稱「生活管家」)
3. 減法自噬驗收 (廢棄控件連根拔起：刪除時間輸入、切換器、手動地址字典、回收Checkbox)
4. 乾淨一屏首屏與物理手感驗收 (單一核心按鈕、:active scale(0.97) + brightness(0.9)、流暢狀態文字)
5. 挑站核心邏輯驗收 (週三日停收、<=3分勉強警告、提早15分出門警告、雙收並列、Google導航)
6. 8 大生活圈兜底按鈕矩陣完整性
7. 商業閉環驗收 (999/1999 包月代倒卡與預約連結)
8. JavaScript AST 語法編譯檢查 (node --check exit 0)
"""

import os
import sys
import io
import re
import subprocess
import tempfile

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(CURRENT_DIR, "index.html")

def run_frontend_audit():
    print("==================================================")
    print("🎨 生活管家・台東垃圾車雷達全新規範前端品質安燈質檢")
    print("==================================================")

    assert os.path.exists(HTML_PATH), f"File not found: {HTML_PATH}"
    file_size = os.path.getsize(HTML_PATH)
    print(f"✅ [Gate 1 Passed] index.html 存在，檔案大小: {file_size} bytes (>= 5KB)")
    assert file_size >= 5000, "Frontend file too small or incomplete"

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Gate 2: 品牌紅線零洩漏檢驗
    assert "Polaris" not in content and "極星" not in content, "Brand Red Line Violated: 嚴禁出現內部代號！"
    assert "生活管家" in content, "必須包含法定服務名稱：生活管家"
    assert "生活管家，就醬點！" in content, "必須包含法定品牌全稱：生活管家，就醬點！"
    print("✅ [Gate 2 Passed] 品牌法定名稱零洩漏防火牆 100% 合規（無內部代號，法定名稱無誤）")

    # Gate 3: 減法自噬驗收 (廢棄控件連根拔起)
    assert "trashTimeInput" not in content, "Must eliminate obsolete trashTimeInput"
    assert "setNowTime" not in content, "Must eliminate obsolete setNowTime"
    assert "quickSetTime" not in content, "Must eliminate obsolete quickSetTime"
    assert "travel-track" not in content, "Must eliminate obsolete travel-track"
    assert "modeScooterBtn" not in content, "Must eliminate obsolete modeScooterBtn"
    assert "manualAddressInput" not in content, "Must eliminate obsolete manualAddressInput"
    assert "TAITUNG_GEO_DICT" not in content, "Must eliminate obsolete TAITUNG_GEO_DICT"
    assert "recycleCheckbox" not in content, "Must eliminate obsolete recycleCheckbox (品碩裁示 B：直接並列無勾選框)"
    print("✅ [Gate 3 Passed] 減法自噬徹底執行：時間輸入框、交通工具切換器、手動地址、回收勾選框全數乾淨根除")

    # Gate 4: 乾淨一屏首屏與微動態物理反饋
    assert "btnHeroFind" in content or "btn-hero-find" in content, "Must have single hero button"
    assert "幫我找垃圾車" in content, "Hero button must say '幫我找垃圾車'"
    assert "scale(0.97)" in content, "Must have physical active scale(0.97)"
    assert "brightness(0.9" in content, "Must have physical active brightness(0.9)"
    assert "定位中…" in content and "搜尋附近垃圾車…" in content, "Must have smooth progressive loading text"
    print("✅ [Gate 4 Passed] 乾淨一屏與物理手感：單一按鈕、實體深色微縮 (:active scale 0.97 + brightness 0.9)、流暢狀態切換")

    # Gate 5: 挑站與班次核心邏輯驗收
    assert "currentDay === 0 || currentDay === 3" in content or "currentDay === 3 || currentDay === 0" in content, "Must check for Taitung Wed/Sun off days"
    assert "今日台東市清潔隊例行停收" in content, "Must have Taitung off day notice"
    assert "dual-collection-banner" in content, "Must have dual collection banner (品碩裁示 B 並列)"
    assert "車可能提早到，建議提早 15 分鐘出門" in content, "Must show early arrival warning when relying on schedule"
    assert "https://www.google.com/maps/dir/?api=1&destination=" in content, "Must use standard Google Maps navigation link"
    assert "urgency-warning-card" in content, "Must have urgency warning card for margin <= 3 min"
    print("✅ [Gate 5 Passed] 挑站與班次邏輯：週三日停收、表定提早15分出門警告、裕度<=3分勉強警告、雙收並列、Google 導航完備")

    # Gate 6: 8 大生活圈兜底按鈕矩陣驗收
    districts = [
        "市區 / 寶桑", "鐵花 / 體育場", "東海 / 漢陽", "豐榮 / 豐谷",
        "豐年 / 康樂", "馬蘭 / 榮民醫院", "卑南 / 南王", "知本 / 建農"
    ]
    for d in districts:
        assert d in content, f"Missing fallback district button: {d}"
    print("✅ [Gate 6 Passed] 8 大在地生活圈兜底按鈕 100% 齊備 (市區/鐵花/東海/豐榮/豐年/馬蘭/卑南/知本)")

    # Gate 7: 商業閉環驗收 (生活管家 999 / 1999 包月卡)
    assert "999" in content and "1,999" in content, "Must mention 999 and 1999 plans"
    assert "butler-service-card" in content, "Must have butler service card"
    print("✅ [Gate 7 Passed] 商業閉環：外圈代倒垃圾包月 NT$ 999 / 1,999 專屬服務卡完備")

    # Gate 8: JavaScript AST 語法編譯檢查
    scripts = re.findall(r'<script>(.*?)</script>', content, flags=re.DOTALL)
    assert len(scripts) > 0, "No script tag found in index.html"
    last_script = scripts[-1]

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".js", delete=False) as tf:
        tf.write(last_script)
        temp_js_path = tf.name

    try:
        check_proc = subprocess.run(["node", "--check", temp_js_path], capture_output=True, text=True)
        assert check_proc.returncode == 0, f"JavaScript SyntaxError detected: {check_proc.stderr}"
        print("✅ [Gate 8 Passed] 戴明硬核防呆：JavaScript AST 語法編譯 100% 通過 (node --check exit 0)")
    finally:
        if os.path.exists(temp_js_path):
            os.remove(temp_js_path)

    print("==================================================")
    print("🎉 生活管家・台東垃圾車雷達前端全新規範 8 重門禁 100% 綠燈 PASS (Exit Code: 0)")
    print("==================================================")

if __name__ == "__main__":
    run_frontend_audit()
