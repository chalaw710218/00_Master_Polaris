#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

skill_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-falcon\SKILL.md")
content = skill_path.read_text(encoding="utf-8")

# 1. Update frontmatter
old_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.0 百輪大圓滿十世大統攝旗艦殿堂版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、100 輪實戰演化淬鍊之「雪柔商戰法務二十項終極法典」、十代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔與極星不可動搖合規護城河。'
new_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.5 百十輪十一世大統攝旗艦殿堂版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、110 輪實戰演化淬鍊之「雪柔商戰法務二十二項終極法典」、十一代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔與極星不可動搖合規護城河。'
content = content.replace(old_desc, new_desc)

old_ver = 'version: v4.0 (Decenary Decadal Grand Synthesis Edition · 百輪大圓滿十世大統攝旗艦殿堂版)'
new_ver = 'version: v4.5 (Undenary Decadal Grand Synthesis Edition · 百十輪十一世大統攝旗艦殿堂版)'
content = content.replace(old_ver, new_ver)

# 2. Update Header
old_h1 = '# 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.0)'
new_h1 = '# 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.5)'
content = content.replace(old_h1, new_h1)

old_pos = '> **版本定位**：百輪大圓滿十世大統攝旗艦殿堂版 (Decenary Decadal Grand Synthesis Edition)'
new_pos = '> **版本定位**：百十輪十一世大統攝旗艦殿堂版 (Undenary Decadal Grand Synthesis Edition)'
content = content.replace(old_pos, new_pos)

# 3. Update Chapter 6
old_ch6 = '## ⚡ 第六章｜雪柔商戰法務二十項終極法典 (The 20 Sandberg Strategic & Legal Laws)\n\n經歷 100 輪實彈模擬與十代十輪衝突大審計洗禮，雪柔固化以下二十項商戰與法務終極法典：'
new_ch6 = '## ⚡ 第六章｜雪柔商戰法務二十二項終極法典 (The 22 Sandberg Strategic & Legal Laws)\n\n經歷 110 輪實彈模擬與十一代十輪衝突大審計洗禮，雪柔固化以下二十二項商戰與法務終極法典：'
content = content.replace(old_ch6, new_ch6)

target_law20 = """### 20. 數位電子履約推定與證據全鏈留痕律 (Digital Execution & Irrefutable Evidence Chain Law)
依據立法院 2024 年最新修正公布施行之《電子簽章法》第 4 條「功能等同原則」及第 5 條「相對人推定同意」要件，確立 LINE 官方帳號與數位表單締約具備完全紙本法律效力。全流程落實「手機號碼 ✕ 數位 UID ✕ 送出時間戳記 ✕ IP 位址」四位一體不可篡改封存，搭配履約完成照片推播與存證導出，免除繁瑣紙本簽約，同時構築死無對證爭端之銅牆鐵壁。"""

new_laws = """### 20. 數位電子履約推定與證據全鏈留痕律 (Digital Execution & Irrefutable Evidence Chain Law)
依據立法院 2024 年最新修正公布施行之《電子簽章法》第 4 條「功能等同原則」及第 5 條「相對人推定同意」要件，確立 LINE 官方帳號與數位表單締約具備完全紙本法律效力。全流程落實「手機號碼 ✕ 數位 UID ✕ 送出時間戳記 ✕ IP 位址」四位一體不可篡改封存，搭配履約完成照片推播與存證導出，免除繁瑣紙本簽約，同時構築死無對證爭端之銅牆鐵壁。

### 21. 建築室內軟裝與特許裝修許可隔離律 (Interior Soft Furnishing vs. Licensed Renovation Law)
依據《建築物室內裝修管理辦法》第 3 條明文排除規範，生活管家老宅微翻新業務嚴格限定於活動家具配置、窗簾地毯安裝、壁紙壁布黏貼與表面油漆粉刷等合法免許可軟裝範疇。**嚴格禁止專員或私人工班敲除增設分間牆、施作固著於構造體之木作天花板、或高度逾 1.2 公尺固定櫥櫃隔屏**（杜絕《建築法》第 77 條之 2 處 6 萬至 30 萬元罰鍰並勒令停工拆除）。遇結構硬體工程一律轉介台東持證合格建築師或合格室內裝修業者。

### 22. 常民風土伴走導覽與特許旅行業防火牆律 (Hyperlocal Guided Walk vs. Licensed Travel Agency Law)
依據《發展觀光條例》第 27 條第 3 項「非旅行業者不得經營旅行業業務」及第 55 條第 4 項（未領照經營罰 10 萬~200 萬元並勒令歇業）之嚴密紅線，生活管家嚴禁在對外文案或私下提供「套裝行程、包辦交通食宿包套、一日遊行程代訂」等旅行社專屬業務。業務嚴格定性為「台東街區生活風土步讀、常民歷史口述諮詢」，採單純鐘點勞務顧問費計收；交通與住宿一律由客戶向合法運輸與旅宿業者自理，達成完全法律風險隔離。"""

content = content.replace(target_law20, new_laws)

# 4. Update Chapter 8
old_ch8_title = '## ⚖️ 第八章｜十代大審計時空解耦憲則 (Decenary Decadal Decoupling Principles)'
new_ch8_title = '## ⚖️ 第八章｜十一代大審計時空解耦憲則 (Undenary Decadal Decoupling Principles)'
content = content.replace(old_ch8_title, new_ch8_title)

old_ch8_item10 = """10. **Cycle 100 (第十代·百輪大圓滿十世大統攝)**：海量全域微型服務與台灣行政監管網絡終極解耦律 —— 穿透個資法與 AI 端側運算最小化去識別、公平法綠色聲明客觀佐證防漂綠、極端氣候勞安氣溫熔斷與陣風防禦、外送指引與承攬工時自主去從屬化、消保法易腐生鮮與客製勞務七日鑑賞期法定排除、老舊華廈逃生通道淨空與公共安寧、2024最新電子簽章法功能等同與推定效力、商標法雙層零洩漏防火牆、以及行政程序法與訴願法三階行政救濟抗辯 SOP。十代審計全勝，完成由單一清運至全域萬用生活服務之世紀大統攝！"""

new_ch8_items = """10. **Cycle 100 (第十代·百輪大圓滿十世大統攝)**：海量全域微型服務與台灣行政監管網絡終極解耦律 —— 穿透個資法與 AI 端側運算最小化去識別、公平法綠色聲明客觀佐證防漂綠、極端氣候勞安氣溫熔斷與陣風防禦、外送指引與承攬工時自主去從屬化、消保法易腐生鮮與客製勞務七日鑑賞期法定排除、老舊華廈逃生通道淨空與公共安寧、2024最新電子簽章法功能等同與推定效力、商標法雙層零洩漏防火牆、以及行政程序法與訴願法三階行政救濟抗辯 SOP。十代審計全勝，完成由單一清運至全域萬用生活服務之世紀大統攝！
11. **Cycle 110 (第十一代·百十輪十一世大統攝)**：常民全維微型生活服務與特種專業行業法特許壁壘終極解耦律 —— 穿透室裝辦法第 3 條軟裝排除（家具油漆壁紙 vs 嚴禁動分間牆與固著天花板）、清潔化學品危害預防（天然酵素 vs 嚴禁私配強酸強鹼）、醫療器材管理法等級分流（第一等級一般手杖輪椅清潔 vs 嚴禁第二等級電動輔具病床未登錄經銷）、觀光條例導覽伴走（純街區生活步讀諮詢 vs 嚴禁代訂食宿交通套裝遊程）、小農初級加工場管理專法認證、特種醫療個資與戶籍代領委任授權鏈、二手物品義賣公益勸募排除、次承攬獨立專業施工侵權自負、以及長輩生前物品斷捨離心靈陪伴與特許生前契約絕對隔離。十一代審計全勝，完成常民生活管家全領域特許深度排雷大統攝！"""

content = content.replace(old_ch8_item10, new_ch8_items)

# 5. Update Chapter 9 Triad
old_triad_intro = '在 100 輪實戰磨礪後，極星三大核心引擎達成百輪大圓滿十世大統攝：'
new_triad_intro = '在 110 輪實戰磨礪後，極星三大核心引擎達成百十輪十一世大統攝：'
content = content.replace(old_triad_intro, new_triad_intro)

old_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務二十項終極法典、全場景五大法規防禦塔、極星萬用服務護城河。'
new_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務二十二項終極法典、全場景五大法規防禦塔、極星萬用服務護城河。'
content = content.replace(old_falcon_line, new_falcon_line)

skill_path.write_text(content, encoding="utf-8")
print("SKILL.md successfully updated to v4.5 (Undenary Decadal Grand Synthesis)!")

# Copy to Office_of_the_CIO_Falcon
dest = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CIO_Falcon\bionic-learning-falcon.md")
dest.write_text(content, encoding="utf-8")
print("Synced to Office_of_the_CIO_Falcon successfully!")
