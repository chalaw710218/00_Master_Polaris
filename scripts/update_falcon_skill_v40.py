#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

skill_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-falcon\SKILL.md")
content = skill_path.read_text(encoding="utf-8")

# 1. Update frontmatter description & version
old_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v3.5 九十輪九旬大統攝旗艦殿堂版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、90 輪實戰演化淬鍊之「雪柔商戰法務十八項終極法典」、九代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔與極星不可動搖合規護城河。'
new_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.0 百輪大圓滿十世大統攝旗艦殿堂版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、100 輪實戰演化淬鍊之「雪柔商戰法務二十項終極法典」、十代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔與極星不可動搖合規護城河。'
content = content.replace(old_desc, new_desc)

old_ver = 'version: v3.5 (Nonary Decadal Grand Synthesis Edition · 九十輪九旬大統攝旗艦殿堂版)'
new_ver = 'version: v4.0 (Decenary Decadal Grand Synthesis Edition · 百輪大圓滿十世大統攝旗艦殿堂版)'
content = content.replace(old_ver, new_ver)

# 2. Update Header
old_h1 = '# 🦅 情報長獵鷹特化版 (CIO Strategic Radar & Sex-Decadal Grand Synthesis Variant v2.0)'
new_h1 = '# 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.0)'
content = content.replace(old_h1, new_h1)

old_pos = '> **版本定位**：九十輪九旬大統攝旗艦殿堂版 (Nonary Decadal Grand Synthesis Edition)'
new_pos = '> **版本定位**：百輪大圓滿十世大統攝旗艦殿堂版 (Decenary Decadal Grand Synthesis Edition)'
content = content.replace(old_pos, new_pos)

# 3. Update Chapter 6 title & intro
old_ch6 = '## ⚡ 第六章｜雪柔商戰法務十八項終極法典 (The 18 Sandberg Strategic & Legal Laws)\n\n經歷 90 輪實彈模擬與九代十輪衝突大審計洗禮，雪柔固化以下十八項商戰與法務終極法典：'
new_ch6 = '## ⚡ 第六章｜雪柔商戰法務二十項終極法典 (The 20 Sandberg Strategic & Legal Laws)\n\n經歷 100 輪實彈模擬與十代十輪衝突大審計洗禮，雪柔固化以下二十項商戰與法務終極法典：'
content = content.replace(old_ch6, new_ch6)

# 4. Append Law 19 and Law 20 to Chapter 6
target_law18 = """### 18. 電氣水暖表面耗材與特許工程分水嶺律 (Surface Maintenance vs. Licensed Utilities Law)
依據《電業法》第 59 條、《電器承裝業管理規則》及《自來水管承裝商管理辦法》，生活管家修繕服務嚴格限定於「表面日常耗材維護」：更換燈泡/燈管、蓮蓬頭軟管、水龍頭起泡器、水箱止水皮。**嚴格禁止任何涉及室內固定電路拆裝（壁面插座、開關面板、吊燈改線、配電盤）與暗管破壁水管工程**。遇特許工程一律轉介台東在地持證合格水電承裝業，杜絕刑法失火與漏水侵權責任。"""

new_laws = """### 18. 電氣水暖表面耗材與特許工程分水嶺律 (Surface Maintenance vs. Licensed Utilities Law)
依據《電業法》第 59 條、《電器承裝業管理規則》及《自來水管承裝商管理辦法》，生活管家修繕服務嚴格限定於「表面日常耗材維護」：更換燈泡/燈管、蓮蓬頭軟管、水龍頭起泡器、水箱止水皮。**嚴格禁止任何涉及室內固定電路拆裝（壁面插座、開關面板、吊燈改線、配電盤）與暗管破壁水管工程**。遇特許工程一律轉介台東在地持證合格水電承裝業，杜絕刑法失火與漏水侵權責任。

### 19. 綠色誠實宣傳與防漂綠客觀實證律 (Truthful Green Claims & Anti-Greenwashing Law)
依據《公平交易法》第 21 條與公平會環境永續及金管會防漂綠參考指引，嚴格落實「真實、有據、易讀、完整、公平」五大原則。文案提及在地友善農法、減碳清運等環境效益，必須備齊產銷履歷、檢驗報告或具體驗算數據（如食物里程與人力單車減碳量），嚴禁使用「100% 碳中和」、「絕對零污染」等未經驗證之籠統誇大詞彙，徹底防範最高 2,500 萬元行政裁罰與商譽受損。

### 20. 數位電子履約推定與證據全鏈留痕律 (Digital Execution & Irrefutable Evidence Chain Law)
依據立法院 2024 年最新修正公布施行之《電子簽章法》第 4 條「功能等同原則」及第 5 條「相對人推定同意」要件，確立 LINE 官方帳號與數位表單締約具備完全紙本法律效力。全流程落實「手機號碼 ✕ 數位 UID ✕ 送出時間戳記 ✕ IP 位址」四位一體不可篡改封存，搭配履約完成照片推播與存證導出，免除繁瑣紙本簽約，同時構築死無對證爭端之銅牆鐵壁。"""

content = content.replace(target_law18, new_laws)

# 5. Update Chapter 8
old_ch8_title = '## ⚖️ 第八章｜九代大審計時空解耦憲則 (Nonary Decadal Decoupling Principles)'
new_ch8_title = '## ⚖️ 第八章｜十代大審計時空解耦憲則 (Decenary Decadal Decoupling Principles)'
content = content.replace(old_ch8_title, new_ch8_title)

old_ch8_item9 = """9. **Cycle 90 (第九代·九十輪大統攝)**：常民萬用生活管家與行業特許制度終極解耦律 —— 穿透動保特寵寄養（原居所照顧 vs 嚴禁異地收容過夜）、電氣水暖（表面更換燈泡軟管 vs 嚴禁私拆面板接線）、數位孿生著作權（出資聘人著作財產權約定與肖像權）、代墊金流洗錢防制（小額委任實質代墊安全港）、包裹保管郵政專營限制、二手物善意取得與贓物防線、好撒瑪利亞人急難免責與台東市調解委員會在地化解閉環，奠定生活管家全場景合法合規總綱！"""

new_ch8_items = """9. **Cycle 90 (第九代·九十輪大統攝)**：常民萬用生活管家與行業特許制度終極解耦律 —— 穿透動保特寵寄養（原居所照顧 vs 嚴禁異地收容過夜）、電氣水暖（表面更換燈泡軟管 vs 嚴禁私拆面板接線）、數位孿生著作權（出資聘人著作財產權約定與肖像權）、代墊金流洗錢防制（小額委任實質代墊安全港）、包裹保管郵政專營限制、二手物善意取得與贓物防線、好撒瑪利亞人急難免責與台東市調解委員會在地化解閉環，奠定生活管家全場景合法合規總綱！
10. **Cycle 100 (第十代·百輪大圓滿十世大統攝)**：海量全域微型服務與台灣行政監管網絡終極解耦律 —— 穿透個資法與 AI 端側運算最小化去識別、公平法綠色聲明客觀佐證防漂綠、極端氣候勞安氣溫熔斷與陣風防禦、外送指引與承攬工時自主去從屬化、消保法易腐生鮮與客製勞務七日鑑賞期法定排除、老舊華廈逃生通道淨空與公共安寧、2024最新電子簽章法功能等同與推定效力、商標法雙層零洩漏防火牆、以及行政程序法與訴願法三階行政救濟抗辯 SOP。十代審計全勝，完成由單一清運至全域萬用生活服務之世紀大統攝！"""

content = content.replace(old_ch8_item9, new_ch8_items)

# 6. Update Chapter 9 Triad
old_triad_intro = '在 90 輪實戰磨礪後，極星三大核心引擎達成九十輪九旬大統攝：'
new_triad_intro = '在 100 輪實戰磨礪後，極星三大核心引擎達成百輪大圓滿十世大統攝：'
content = content.replace(old_triad_intro, new_triad_intro)

old_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務十八項終極法典、全場景五大法規防禦塔、極星萬用服務護城河。'
new_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務二十項終極法典、全場景五大法規防禦塔、極星萬用服務護城河。'
content = content.replace(old_falcon_line, new_falcon_line)

skill_path.write_text(content, encoding="utf-8")
print("SKILL.md successfully updated to v4.0 (Decenary Decadal Grand Synthesis)!")
