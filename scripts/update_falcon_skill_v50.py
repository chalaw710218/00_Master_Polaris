#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

skill_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-falcon\SKILL.md")
content = skill_path.read_text(encoding="utf-8")

# 1. Update frontmatter
old_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.5 百十輪十一世大統攝旗艦殿堂版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、110 輪實戰演化淬鍊之「雪柔商戰法務二十二項終極法典」、十一代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔與極星不可動搖合規護城河。'
new_desc = 'description: 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v5.0 雙甲子百二十輪十二世大統攝終極殿堂金身版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合創辦人親定「專注在法規上為未來海量服務築起護城河」法旨、120 輪實戰演化淬鍊之「雪柔商戰法務二十四項終極法典」、十二代十輪衝突大審計時空解耦憲則、全域海量服務五大法規防禦塔、閉鎖性股權黃金股主權、家族信託與極星不可動搖合規護城河。'
content = content.replace(old_desc, new_desc)

old_ver = 'version: v4.5 (Undenary Decadal Grand Synthesis Edition · 百十輪十一世大統攝旗艦殿堂版)'
new_ver = 'version: v5.0 (Duodecennial Supreme Edition · 雙甲子百二十輪十二世大統攝終極殿堂金身版)'
content = content.replace(old_ver, new_ver)

# 2. Update Header
old_h1 = '# 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v4.5)'
new_h1 = '# 🦅 首席法務顧問兼情報長雪柔特化版 (Chief Legal & Strategic Radar Variant v5.0)'
content = content.replace(old_h1, new_h1)

old_pos = '> **版本定位**：百十輪十一世大統攝旗艦殿堂版 (Undenary Decadal Grand Synthesis Edition)'
new_pos = '> **版本定位**：雙甲子百二十輪十二世大統攝終極殿堂金身版 (Duodecennial Supreme Edition)'
content = content.replace(old_pos, new_pos)

# 3. Update Chapter 6
old_ch6 = '## ⚡ 第六章｜雪柔商戰法務二十二項終極法典 (The 22 Sandberg Strategic & Legal Laws)\n\n經歷 110 輪實彈模擬與十一代十輪衝突大審計洗禮，雪柔固化以下二十二項商戰與法務終極法典：'
new_ch6 = '## ⚡ 第六章｜雪柔商戰法務二十四項終極法典 (The 24 Sandberg Strategic & Legal Laws)\n\n經歷 120 輪實彈模擬與十二代十輪衝突大審計洗禮，雪柔固化以下二十四項商戰與法務終極法典：'
content = content.replace(old_ch6, new_ch6)

target_law22 = """### 22. 常民風土伴走導覽與特許旅行業防火牆律 (Hyperlocal Guided Walk vs. Licensed Travel Agency Law)
依據《發展觀光條例》第 27 條第 3 項「非旅行業者不得經營旅行業業務」及第 55 條第 4 項（未領照經營罰 10 萬~200 萬元並勒令歇業）之嚴密紅線，生活管家嚴禁在對外文案或私下提供「套裝行程、包辦交通食宿包套、一日遊行程代訂」等旅行社專屬業務。業務嚴格定性為「台東街區生活風土步讀、常民歷史口述諮詢」，採單純鐘點勞務顧問費計收；交通與住宿一律由客戶向合法運輸與旅宿業者自理，達成完全法律風險隔離。"""

new_laws = """### 22. 常民風土伴走導覽與特許旅行業防火牆律 (Hyperlocal Guided Walk vs. Licensed Travel Agency Law)
依據《發展觀光條例》第 27 條第 3 項「非旅行業者不得經營旅行業業務」及第 55 條第 4 項（未領照經營罰 10 萬~200 萬元並勒令歇業）之嚴密紅線，生活管家嚴禁在對外文案或私下提供「套裝行程、包辦交通食宿包套、一日遊行程代訂」等旅行社專屬業務。業務嚴格定性為「台東街區生活風土步讀、常民歷史口述諮詢」，採單純鐘點勞務顧問費計收；交通與住宿一律由客戶向合法運輸與旅宿業者自理，達成完全法律風險隔離。

### 23. 閉鎖性股權黃金股創辦人主權律 (Founder Golden Share & Absolute Sovereign Law)
依據《公司法》第 356 條之 1 及第 356 條之 7 規定，組織升維為法人時，必須章程載明股份轉讓嚴格限制，並由創辦人陳品碩持有 1:10 複數表決權特別股與重大事項一票否決權（黃金股）。無論未來引入何種外部資本、融資或員工股權激勵，創辦人對解散、修章、重大資產處分與合併分割享有絕對不可撼動之否決主權，徹底粉碎任何外部資本惡意稀釋併購之企圖。

### 24. 全域 AI 履行輔助人責任與秘密仲裁護城河律 (AI Auxiliary Liability & Confidential Arbitration Law)
依據《民法》第 224 條債務人履行輔助人規定，全域自主 AI 代理人（Antigravity Agents）產出之一切代碼、定價、文案與履約排程，在民法上定性為公司代表人之智慧輔助工具，對外由極星法人承擔完全民事責任，絕不以演算法黑箱推諉；對內嚴格設置戴明安燈防呆閘門物理阻絕侵權。同時所有商業契約全面植入《仲裁法》第 1 條與第 15 條「台東地方法院秘密仲裁前置條款」，以不公開、六個月快速終局之仲裁判斷替代公開冗長訴訟，保全商業機密與品牌百年月桂冠。"""

content = content.replace(target_law22, new_laws)

# 4. Update Chapter 8
old_ch8_title = '## ⚖️ 第八章｜十一代大審計時空解耦憲則 (Undenary Decadal Decoupling Principles)'
new_ch8_title = '## ⚖️ 第八章｜十二代大審計時空解耦憲則 (Duodecennial Decadal Decoupling Principles)'
content = content.replace(old_ch8_title, new_ch8_title)

old_ch8_item11 = """11. **Cycle 110 (第十一代·百十輪十一世大統攝)**：常民全維微型生活服務與特種專業行業法特許壁壘終極解耦律 —— 穿透室裝辦法第 3 條軟裝排除（家具油漆壁紙 vs 嚴禁動分間牆與固著天花板）、清潔化學品危害預防（天然酵素 vs 嚴禁私配強酸強鹼）、醫療器材管理法等級分流（第一等級一般手杖輪椅清潔 vs 嚴禁第二等級電動輔具病床未登錄經銷）、觀光條例導覽伴走（純街區生活步讀諮詢 vs 嚴禁代訂食宿交通套裝遊程）、小農初級加工場管理專法認證、特種醫療個資與戶籍代領委任授權鏈、二手物品義賣公益勸募排除、次承攬獨立專業施工侵權自負、以及長輩生前物品斷捨離心靈陪伴與特許生前契約絕對隔離。十一代審計全勝，完成常民生活管家全領域特許深度排雷大統攝！"""

new_ch8_items = """11. **Cycle 110 (第十一代·百十輪十一世大統攝)**：常民全維微型生活服務與特種專業行業法特許壁壘終極解耦律 —— 穿透室裝辦法第 3 條軟裝排除（家具油漆壁紙 vs 嚴禁動分間牆與固著天花板）、清潔化學品危害預防（天然酵素 vs 嚴禁私配強酸強鹼）、醫療器材管理法等級分流（第一等級一般手杖輪椅清潔 vs 嚴禁第二等級電動輔具病床未登錄經銷）、觀光條例導覽伴走（純街區生活步讀諮詢 vs 嚴禁代訂食宿交通套裝遊程）、小農初級加工場管理專法認證、特種醫療個資與戶籍代領委任授權鏈、二手物品義賣公益勸募排除、次承攬獨立專業施工侵權自負、以及長輩生前物品斷捨離心靈陪伴與特許生前契約絕對隔離。十一代審計全勝，完成常民生活管家全領域特許深度排雷大統攝！
12. **Cycle 120 (第十二代·雙甲子百二十輪十二世大統攝終極大圓滿)**：百年帝國資本擴張與創辦人絕對主權風土倫理終極最高解耦律 —— 穿透閉鎖性公司黃金股主權死鎖、合作社法勞動利潤共享免納營所稅、原民傳統智財授權與利益共享、證交法與銀行法吸金刑事紅線阻斷、政府採購法偏鄉最有利標評選、跨境生鮮果乾簡易報關檢疫沙盒、信託法家族資產破產隔離與債務阻斷、民法履行輔助人 AI 責任定性與戴明出廠閘門、以及仲裁法秘密仲裁保全商譽。十二代審計全勝，完成全域海量微型服務之世紀法治大憲章終極封頂！"""

content = content.replace(old_ch8_item11, new_ch8_items)

# 5. Update Chapter 9 Triad
old_triad_intro = '在 110 輪實戰磨礪後，極星三大核心引擎達成百十輪十一世大統攝：'
new_triad_intro = '在 120 輪實戰磨礪後，極星三大核心引擎達成雙甲子百二十輪十二世大統攝終極大圓滿：'
content = content.replace(old_triad_intro, new_triad_intro)

old_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務二十二項終極法典、全場景五大法規防禦塔、極星萬用服務護城河。'
new_falcon_line = '* **CIO/Legal 雪柔 (Falcon)**：雪柔商戰法務二十四項終極法典、全場景五大法規防禦塔、閉鎖性黃金股主權、家族信託與極星萬用服務護城河。'
content = content.replace(old_falcon_line, new_falcon_line)

skill_path.write_text(content, encoding="utf-8")
print("SKILL.md successfully updated to v5.0 (Duodecennial Supreme Edition)!")

# Copy to Office_of_the_CIO_Falcon
dest = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CIO_Falcon\bionic-learning-falcon.md")
dest.write_text(content, encoding="utf-8")
print("Synced to Office_of_the_CIO_Falcon successfully!")
