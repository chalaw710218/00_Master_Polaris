import sys

skill_path = r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-falcon\SKILL.md'

with open(skill_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update version & description
text = text.replace(
    'description: 🦅 情報長獵鷹特化版 (CIO Strategic Radar & Sex-Decadal Grand Synthesis Variant v2.0 甲子大統攝六十輪情報旗艦版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合 60 輪實戰演化淬鍊之「雪柔商戰情報十二項終極鐵律」、六代十輪衝突大審計時空解耦憲則、Option B 逆境復原力與極星跨內閣三位一體戰略護城河。',
    'description: 🦅 情報長獵鷹特化版 (CIO Strategic Radar & Septenary Decadal Grand Synthesis Variant v2.1 七十輪古稀七代大統攝旗艦版)。繼承北極星仿生學習系統母版 (v5.2 Golden Master)，融合 70 輪實戰演化淬鍊之「雪柔商戰情報十四項終極鐵律」、七代十輪衝突大審計時空解耦憲則、Option B 逆境復原力與極星跨內閣三位一體戰略護城河。'
)
text = text.replace(
    'version: v2.0 (Sex-Decadal Grand Synthesis Edition · 甲子大統攝六十輪旗艦版)',
    'version: v2.1 (Septenary Decadal Grand Synthesis Edition · 七十輪古稀七代大統攝旗艦版)'
)
text = text.replace(
    '> **版本定位**：甲子大統攝六十輪情報旗艦版 (Sex-Decadal Grand Synthesis Edition)  ',
    '> **版本定位**：七十輪古稀七代大統攝旗艦版 (Septenary Decadal Grand Synthesis Edition)  '
)

# 2. Update Chapter 6 to 14 laws
law_header_old = '## ⚡ 第六章｜雪柔商戰情報十二項終極鐵律 (The 12 Sandberg Strategic Intelligence Laws)\n\n經歷 60 輪實彈模擬與六代十輪衝突大審計洗禮，獵鷹固化以下十二項情報鐵律：'
law_header_new = '## ⚡ 第六章｜雪柔商戰情報十四項終極鐵律 (The 14 Sandberg Strategic Intelligence Laws)\n\n經歷 70 輪實彈模擬與七代十輪衝突大審計洗禮，獵鷹固化以下十四項情報鐵律：'
text = text.replace(law_header_old, law_header_new)

law_add = """### 13. 產生源產權邊界死守律 (Source Property Boundary Law)
依據《一般廢棄物回收清除處理辦法》第 2 條，家戶廢棄物離開門牌產權即屬法定「排出」。嚴禁在任何公私領域固定設立外部垃圾集散橘桶（杜絕私設轉運站與廢清法 §41/§46-4 刑責）。堅持「桶隨人動、門前直取、產地即去化」，非動力載具停留時間僅限移動分鐘級，零落地、零轉運。

### 14. 社區華廈 B2B 包棟優先律 (Community HOA B2B Prioritization Law)
依據《公寓大廈管理條例》第 3 條與第 53 條，同一建照或共有基地之全體住戶為法定「單一產生源」，內部集中子母車屬合法自產自存。生活管家以「受託物業推桶勞務」切入無警衛微型華廈（6~16戶），直接向管委會收取公帳包月費並開立三聯式發票，以 B2B 標準合約取代高摩擦散客，實現十倍級暴利單元經濟。

---"""

text = text.replace(
    """### 12. 極星共榮生態終極律 (Polaris Co-Prosperity Ultimate Law)
商戰情報的終極目的不是消滅對手，而是團結農漁民、車手與在地商戶，打造共富共生、不可撼動的極星命運共同體。

---""",
    """### 12. 極星共榮生態終極律 (Polaris Co-Prosperity Ultimate Law)
商戰情報的終極目的不是消滅對手，而是團結農漁民、車手與在地商戶，打造共富共生、不可撼動的極星命運共同體。

""" + law_add
)

# 3. Update Chapter 8 to 7 decadal principles
dec_old = """## ⚖️ 第八章｜六代大審計時空解耦憲則 (Sex-Decadal Decoupling Principles)

1. **Cycle 10 (第一代)**：採集與推廣合一律 —— 廢除長問卷，將情資建檔融入 3 分鐘實體口頭交流。
2. **Cycle 20 (第二代)**：商業與公益雙軌分流律 —— 長輩代送餐差額走社企基金核銷，車手實拿不減。
3. **Cycle 30 (第三代)**：孤品溢價與常規底價對沖律 —— 常規品守底價，全港頂級野生孤品加價 10% 買斷排他權。
4. **Cycle 40 (第四代)**：原料吸納與終端深耕解耦律 —— 跨縣市對接回頭車吸納原料，終端配送 100% 聚焦在地。
5. **Cycle 50 (第五代)**：奢華度假與平民管家物理隔離律 —— 高階度假冷藏管家獨立子品牌運營，完全物理隔離。
6. **Cycle 60 (第六代)**：稀缺盲盒與誠信公關終極守則 —— 野生不穩定食材化為限量預售盲盒；公關試吃嚴守好客人情與零強求。"""

dec_new = """## ⚖️ 第八章｜七代大審計時空解耦憲則 (Septenary Decadal Decoupling Principles)

1. **Cycle 10 (第一代)**：採集與推廣合一律 —— 廢除長問卷，將情資建檔融入 3 分鐘實體口頭交流。
2. **Cycle 20 (第二代)**：商業與公益雙軌分流律 —— 長輩代送餐差額走社企基金核銷，車手實拿不減。
3. **Cycle 30 (第三代)**：孤品溢價與常規底價對沖律 —— 常規品守底價，全港頂級野生孤品加價 10% 買斷排他權。
4. **Cycle 40 (第四代)**：原料吸納與終端深耕解耦律 —— 跨縣市對接回頭車吸納原料，終端配送 100% 聚焦在地。
5. **Cycle 50 (第五代)**：奢華度假與平民管家物理隔離律 —— 高階度假冷藏管家獨立子品牌運營，完全物理隔離。
6. **Cycle 60 (第六代)**：稀缺盲盒與誠信公關終極守則 —— 野生不穩定食材化為限量預售盲盒；公關試吃嚴守好客人情與零強求。
7. **Cycle 70 (第七代·古稀大統攝)**：暴利單元經濟與廢清法轉運站紅線解耦律 —— 嚴禁在公共/私領域設立外部他人垃圾集散橘桶（杜絕私設轉運站刑責）；以《公寓大廈管理條例》第 3 條與第 53 條之社區同一基地法定單一產生源，將集散模式時空解耦並升維至「B2B 社區華廈推桶包棟勞務」，兼顧 100% 法律合規與單棟月收 4,500 元之暴利單元經濟。"""

text = text.replace(dec_old, dec_new)

with open(skill_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESSFULLY_UPDATED_FALCON_SKILL')
