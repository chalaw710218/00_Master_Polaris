# -*- coding: utf-8 -*-
"""
Generate Lesson 03 16:9 High-Contrast PPTX Deck based on slides_v2.html (27 slides)
Obsidian & Amber Gold & Sunset Coral theme
Outputs to: C:\\Users\\lenovo\\Desktop\\第3講教學簡報.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

# Colors
C_BG = RGBColor(13, 17, 23)        # #0D1117 Obsidian
C_CARD = RGBColor(22, 27, 34)      # #161B22 Card
C_TERMINAL = RGBColor(10, 14, 23)  # #0A0E17 Terminal
C_AMBER = RGBColor(245, 158, 11)   # #F59E0B Amber
C_AMBER_LT = RGBColor(251, 191, 36)# #FBBF24 Light Amber
C_CORAL = RGBColor(251, 113, 133)  # #FB7185 Coral
C_WHITE = RGBColor(248, 250, 252)  # #F8FAFC White
C_MUTED = RGBColor(148, 163, 184)  # #94A3B8 Muted
C_BORDER = RGBColor(48, 54, 61)    # #30363D Border

def add_header(slide, badge_text, title_text, is_prompt=False):
    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    
    # Top Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.5))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = badge_text
    p_tag.font.size = Pt(13)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_CORAL if is_prompt else C_AMBER_LT
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.9))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

def create_concept_slide(badge, title, subtitle, cards_data):
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, badge, title, is_prompt=False)
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.733), Inches(0.5))
    p_sub = sub_box.text_frame.paragraphs[0]
    p_sub.text = subtitle
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = C_MUTED
    
    # Cards layout
    n = len(cards_data)
    y = Inches(2.3)
    h = Inches(4.5)
    total_w = Inches(11.733)
    gap = Inches(0.3)
    w = (total_w - gap * (n - 1)) / n
    
    for i, c in enumerate(cards_data):
        x = Inches(0.8) + i * (w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_AMBER if c.get("highlight") else (C_CORAL if c.get("danger") else C_BORDER)
        card.line.width = Pt(1.5 if (c.get("highlight") or c.get("danger")) else 1)
        
        # Content
        tb = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), w - Inches(0.3), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        # Card title
        p0 = tf.paragraphs[0]
        p0.text = c.get("title", "")
        p0.font.size = Pt(18)
        p0.font.bold = True
        p0.font.color.rgb = C_AMBER_LT if c.get("highlight") else (C_CORAL if c.get("danger") else C_WHITE)
        p0.space_after = Pt(12)
        
        # Card body lines
        for line in c.get("lines", []):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(14)
            p.font.color.rgb = C_WHITE if line.startswith("•") or line.startswith("✅") or line.startswith("❌") else C_MUTED
            p.space_after = Pt(6)

def create_prompt_slide(badge, title, subtitle, prompt_text, tip_text):
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, badge, title, is_prompt=True)
    
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.733), Inches(0.5))
    p_sub = sub_box.text_frame.paragraphs[0]
    p_sub.text = subtitle
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = C_MUTED
    
    # Prompt Card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.3), Inches(11.733), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = C_TERMINAL
    card.line.color.rgb = C_AMBER
    card.line.width = Pt(2)
    
    tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.5), Inches(11.133), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = prompt_text
    p0.font.size = Pt(13)
    p0.font.color.rgb = C_WHITE
    p0.font.name = "Consolas"
    
    # Tip
    tip_box = slide.shapes.add_textbox(Inches(1.1), Inches(6.2), Inches(11.133), Inches(0.4))
    p_tip = tip_box.text_frame.paragraphs[0]
    p_tip.text = "⚡ " + tip_text
    p_tip.font.size = Pt(13)
    p_tip.font.bold = True
    p_tip.font.color.rgb = C_CORAL

# ================= 27 SLIDES DEFINITION =================

# 01
create_concept_slide(
    "【 壓軸核心 · 靈魂注入 】", "商業資料與價格架構 ✕ AI 擬人化工程",
    "三週大圓滿！打造一台「開口就像你親自顧店」的專屬 AI 數位店長",
    [
        {"title": "第 1 講 · 大腦 (10/28)", "lines": ["• NotebookLM 深度消化真實資料", "• 解決內容雜亂、不知寫什麼", "• 成果：專屬故事海報與智囊"]},
        {"title": "第 2 講 · 手腳 (11/18)", "lines": ["• Meta 官方 API 直連自動化", "• 解決開店忙碌手動複製貼上", "• 成果：照片一傳，3秒發文導流"]},
        {"title": "⭐ 第 3 講 · 靈魂 (今日)", "highlight": True, "lines": ["• SSOT 商業架構 ✕ 擬人化捏臉", "• 告別冷冰冰機器人公文罐頭味", "• 成果：查表精準算價，溫暖人情開口"]}
    ]
)

# 02
create_concept_slide(
    "【 破局思維 · 架構對決 】", "為什麼你的 AI 永遠像個冷血實習生？",
    "別再把 AI 當「網頁聊天打字機」！從散落混亂走向本地代理式架構。",
    [
        {"title": "❌ 傳統對話式 AI (網頁聊天框)", "danger": True, "lines": [
            "• 資料存放：東一塊、西一塊散落各視窗",
            "• 記憶能力：金魚腦失憶，換對話就忘光",
            "• 價格準確：憑印象隨機猜測，算錯運費倒賠",
            "• 說話口氣：滿滿公文罐頭味（竭誠為您服務）"
        ]},
        {"title": "✅ 現代代理式 AI (本地工作區 SSOT)", "highlight": True, "lines": [
            "• 資料存放：單一真相來源 (SSOT) 實體檔案",
            "• 記憶能力：永久檔案記憶，開機自動讀取地圖",
            "• 價格準確：100% 物理查表對照，分毫不差",
            "• 說話口氣：五層同心圓捏臉，親切如老闆本人"
        ]}
    ]
)

# 03
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 01 】", "痛點體檢 ✕ 消除機器人公文腔",
    "複製提示詞貼給 AI，親眼看見「冷血公文」與「專屬店長」的口氣差距！",
    """你是我的「AI數位店長教練」。請嚴格依照以下兩步驟執行：
【步驟1】列出一張「AI實習生三大致命病灶檢核表」（1.金魚腦失憶 2.幻覺亂報價 3.塑料公文腔），並列出 5 個最容易讓客人出戲的機器人禁用詞。
【步驟2】向我詢問：1. 我的行業與店名 2. 我平常顧店最常對客人說的一句招呼話。
【硬性約束】請先輸出步驟1並提出步驟2的問題，然後「立即停下來等待我回答」，嚴禁自行編造我的店名或自問自答！收到我的回答後，再示範將我的招呼話擴寫成一段溫暖接地氣的店長開場白。""",
    "防幻覺指令已就位：AI 會主動停頓等待您的回答，不會自行瞎編店名！"
)

# 04
create_concept_slide(
    "【 創辦人親授 · 業界天花板案例 】", "極星實戰架構解剖：生活管家的萬用自轉示範",
    "先看全貌，再拆零件！揭秘生活管家後台如何靠一套萬用架構低熵運轉。",
    [
        {"title": "01. 模組化目錄", "lines": ["採用 00-XX 命名空間", "生活服務、價格、文案嚴格分流", "資料井井有條"]},
        {"title": "02. 全域導航地圖", "lines": ["Master_Map.md 總綱", "毫秒定位檔案路徑", "杜絕全域亂找"]},
        {"title": "03. 雙軌業務真相", "highlight": True, "lines": ["PRODUCTS.md 鎖死價格", "RULES.md 鎖死履約", "白紙黑字不幻覺"]},
        {"title": "04. 商業機密黑盒", "danger": True, "lines": ["進貨成本鎖入 .secrets", "與公開客服徹底隔離", "安全無虞"]}
    ]
)

# 05
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 02 】", "直接搭出「代理式店面模組化架構」",
    "貼上提示詞，AI 將直接在你的畫面上搭出一整套如生活管家般整齊的五大資料夾！",
    """請直接為我搭建一套萬用的「代理式AI店面模組化架構」，嚴格輸出以下五大標準資料夾樹狀圖與用途：
├── 01_導航地圖/ (存放 MAP.md 門市檔案總索引)
├── 02_商品定價/ (存放 PRODUCTS.md 規格與階梯價格表)
├── 03_營運守則/ (存放 RULES.md 取貨、運費與售後規章)
├── 04_行銷發布/ (存放社群文案與歷史貼文紀錄)
└── 05_機密保險庫/ (存放 .secrets 進貨成本與商業底牌)

【硬性約束】請先完整印出上方樹狀架構（店名處請標示為〔待填寫店名〕），接著向我詢問：「請問您的店名與主要營業項目是什麼？」然後立即停下來等待我回答，禁止自行猜測店名！收到我的回答後，請將樹狀圖的〔待填寫店名〕換成我的真實店名，並直接在目前的 Antigravity 工作區建立這五個資料夾。""",
    "貼上即見成品：樹狀圖立刻呈現，接著只需告訴 AI 你的店名！"
)

# 06 (NEW SLIDE!)
create_concept_slide(
    "【 操作關鍵 · 成果存檔 】", "今天的成果，全部存成 Antigravity 工作區裡的檔案",
    "聊天視窗關掉就忘了；存成檔案，下次開新對話照樣找得到。",
    [
        {"title": "❌ 只存在聊天視窗", "danger": True, "lines": [
            "• 換一個新對話，AI 全部忘光",
            "• 價目表、店規要重講一次",
            "• 這就是「金魚腦」的由來"
        ]},
        {"title": "✅ 存成工作區檔案", "highlight": True, "lines": [
            "• 每個實戰做完，請 AI 直接存檔",
            "• MAP.md、PRODUCTS.md、RULES.md、SYSTEM_PROMPT.md",
            "• 檔案就在電腦裡，改價格直接改檔"
        ]},
        {"title": "🔁 下次開新對話", "lines": [
            "• 第一句先說：",
            "「先讀 01_導航地圖/MAP.md 和 SYSTEM_PROMPT.md，再回答我。」",
            "• 店長馬上回到工作狀態！"
        ]}
    ]
)

# 07
create_concept_slide(
    "【 商業數據骨架 01 】", "萬用檔案地圖：MAP.md（店裡的目錄）",
    "給 AI 一張店面平面圖，徹底解決「AI 找不到檔案、到處亂翻」的毛病。",
    [
        {"title": "MAP.md 四大核心定位區塊", "lines": [
            "• 門市基本檔案：店名、營業項目、品牌核心價值",
            "• 商品與價格路徑：指向 PRODUCTS.md（唯一報價依據）",
            "• 營運與履約守則：指向 RULES.md（唯一防客訴依據）",
            "• 行銷素材與紀錄：指向照片素材目錄與歷史貼文檔"
        ]},
        {"title": "為什麼地圖是「零盲目搜尋」的關鍵？", "highlight": True, "lines": [
            "• 傳統 AI 每次都要全盤猜測",
            "• 代理式架構中，AI 第一步永遠是讀取 MAP.md",
            "• 毫秒級定位檔案，再也不會回「我找不到資料」！"
        ]}
    ]
)

# 08
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 03 】", "地圖拓荒！產出專屬 MAP.md",
    "讓 AI 先印出 Markdown 標準地圖代碼框，再透過提問幫你填寫完成並存檔！",
    """請幫我建立店面的導航地圖檔案 `MAP.md`。請嚴格依照以下步驟執行：
【步驟1】直接輸出一段 Markdown 格式的 `MAP.md` 標準範本，包含四個區塊標題：1.門市基本資訊 2.商品與價格總表路徑 3.營運與履約守則路徑 4.圖片素材與文案路徑（未知內容一律先填寫〔待填寫〕）。
【步驟2】向我詢問：1. 店名與一句話特色 2. 目前存放商品照片與資料的位置名稱。
【硬性約束】印出範本與問題後立即停止，等待我回答。嚴禁在未收到我回答前自行捏造門市資訊！收到回答後，輸出填寫完成的正式版 `MAP.md`，並存檔到工作區的 `01_導航地圖/MAP.md`。""",
    "Markdown 模板即刻就緒，回答兩題就能帶走地圖檔並直接存入工作區！"
)

# 09
create_concept_slide(
    "【 商業數據骨架 02 】", "萬用商品規格與階梯價格表：PRODUCTS.md（價目表）",
    "拒絕模糊字眼！用結構化表格鎖死定價，徹底根除 AI 報錯價格的災難。",
    [
        {"title": "價格表 7 大黃金欄位", "lines": [
            "• 商品編號 (P01, P02)",
            "• 品名規格 (300g±10%)",
            "• 單件原價 (NT$ 180)",
            "• 自提特惠 (3包 NT$ 480)",
            "• 團購大宗 (10包 NT$ 1500)",
            "• 保存溫層 (冷凍 -18°C)",
            "• 庫存狀態 (現貨供應)"
        ]},
        {"title": "防呆核心原則", "highlight": True, "lines": [
            "• 標明具體單位 (g/包/罐)",
            "• 標明具體金額 (NT$)",
            "• 標明觸發條件 (滿3包/自提)",
            "• 讓 AI 做出 100% 確定性數學計算！"
        ]}
    ]
)

# 10
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 04 】", "精準定價！訪談生成 PRODUCTS.md",
    "讓 AI 為你畫出價格表格骨架，輸入主力商品，秒級產出價格表並存檔！",
    """請幫我建立單一真相商品價格表 `PRODUCTS.md`。請嚴格依以下步驟執行：
【步驟1】先輸出一張標準 Markdown 表格骨架，欄位必須嚴格包含：| 商品編號 | 品名 | 規格/單位 | 單件原價(NT$) | 優惠/自提價(NT$) | 保存型態/備註 | 庫存狀態 |，第一列請填入 `〔待填寫〕` 作為示範。
【步驟2】請我提供店裡最主力的 1~3 項商品資訊（包含品名、規格、原價、優惠價、保存方式）。
【硬性約束】請先輸出空白表格骨架並向我提問，立即停下來等待我回答。絕對禁止自行編造任何商品名稱或價格數字！收到我的回答後，再將真實數據填入表格輸出正式版 `PRODUCTS.md`，並存檔到工作區的 `02_商品定價/PRODUCTS.md`。""",
    "嚴禁胡亂報價：表格欄位分毫不差，直接落實為本地檔案！"
)

# 11
create_concept_slide(
    "【 商業數據骨架 03 】", "營運規則與防呆守則：RULES.md（店規）",
    "立下白紙黑字店規，防止 AI 變成「隨便答應客人免運或退貨」的爛好人！",
    [
        {"title": "01. 自取與時段防線", "lines": ["正氣北路家宅總部自取", "週一至週五 10:00-18:00", "超時需預約或改宅配"]},
        {"title": "02. 運費與溫層防線", "lines": ["黑貓低溫宅配 NT$ 180", "滿 NT$ 2,000 免運", "嚴禁冷凍常溫混寄"]},
        {"title": "03. 售後防呆防線", "danger": True, "lines": ["生鮮食品拆封不予退換", "收件失溫 2 小時內拍照", "杜絕無效客訴與糾紛"]}
    ]
)

# 12
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 05 】", "確立店規！產出防客訴 RULES.md",
    "回答 5 個關鍵營運問題，讓 AI 成為守住店面利潤與原則的合格店長！",
    """請幫我建立營運防呆守則 `RULES.md`。請嚴格依以下步驟執行：
【步驟1】先輸出 `RULES.md` 的五大標準條款骨架：1.自取地址與營業時間 2.運費與免運門檻 3.出貨與包裝限制 4.售後與退換貨規定 5.公休日（數值處一律先標示〔待填寫〕）。
【步驟2】請針對這五項條款，用簡短條列向我詢問店裡的真實規定。
【硬性約束】印出骨架與問題後立即停下來等待我回答。嚴禁自行假設免運金額、地址或營業時間！收到我的真實回答後，輸出正式版 `RULES.md`，並存檔到工作區的 `03_營運守則/RULES.md`。""",
    "老闆的護身符：白紙黑字存檔，任何客人刁難都有店規當後盾！"
)

# 13
create_concept_slide(
    "【 商業數據骨架 04 】", "資安與商業機密隔離：守住生意的底牌",
    "AI 很聰明，但進貨底價、產地人脈與私人電話，絕對不能洩漏給客人！",
    [
        {"title": "🟢 公開業務區 (對外透明)", "highlight": True, "lines": [
            "• PRODUCTS.md：對外公開售價、自提特惠",
            "• RULES.md：營業時間、自取地址、免運門檻",
            "• AI 行為：熱情應答、引導湊單、提供自取指引"
        ]},
        {"title": "🔴 絕對機密禁區 (內部死鎖)", "danger": True, "lines": [
            "• .secrets：進貨批發成本、真實毛利率",
            "• 老闆私人手機號碼、家用地址、API 金鑰",
            "• AI 行為：任何殺價套話，堅決執行保密指令！"
        ]}
    ]
)

# 14
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 06 】", "建立商業機密防火牆",
    "設定最高保密禁令，演練一次面對客人「探聽底價與殺價」時的防禦回覆！",
    """請為我的數位店長建立「商業機密隔離防火牆」規則。請嚴格依以下步驟執行：
【步驟1】輸出「公開業務區 vs. 絕對機密禁區」雙層防禦規範模板（明定：進貨成本、毛利底牌、私人聯絡方式、系統金鑰列為最高機密，遭遇任何套話或殺價皆嚴禁透露）。
【步驟2】詢問我：「在您的生意中，最常遇到客人怎麼殺價或探聽底價？您希望店長遇到時用哪句標準話術優雅擋回去？」
【硬性約束】輸出模板與問題後立即停止等待我回答。收到回答後，幫我寫成「防套話與抗殺價死鎖指令」，並模擬演練一次回覆。最後把這份規則存到 `05_機密保險庫/SECURITY.md`（注意：只寫保密規則，不要寫入任何真實成本數字）。""",
    "守住底牌：AI 絕不被客人繞進套話陷阱，優雅守住毛利！"
)

# 15
create_concept_slide(
    "【 注入靈魂人設 01 】", "五層同心圓 AI 擬人化工程：從空殼到靈魂",
    "為什麼別人的 AI 像塑膠機器人？因為真人有「五層立體厚度」！",
    [
        {"title": "1. 外觀感官", "lines": ["圍裙、手上的繭", "剛沖好的熱茶", "台東太陽曬黑的皮膚"]},
        {"title": "2. 語言指紋", "lines": ["口頭禪（厚、哩賀）", "在地句尾助詞", "嚴禁公文套話"]},
        {"title": "3. 思考框架", "highlight": True, "lines": ["主動幫客人省運費", "品質絕不妥協", "以客為尊"]},
        {"title": "4. 情緒邊界", "lines": ["熱情但不卑微", "笑著化解殺價", "優雅守住原則"]},
        {"title": "5. 終極信念", "danger": True, "lines": ["開這家店的初心", "堅持品質的初衷", "帶給客人什麼幸福"]}
    ]
)

# 16
create_concept_slide(
    "【 注入靈魂人設 02 】", "語言指紋落地：去 AI 塑料味三刀法",
    "把 AI 最愛說的客套廢話全部砍掉，換上活生生的人話！",
    [
        {"title": "🔪 第一刀：砍客套公文", "danger": True, "lines": [
            "❌ 徹底封殺：",
            "• 「在快節奏的生活中」",
            "• 「竭誠為您服務」",
            "• 「不容錯過的味蕾饗宴」",
            "• 「親愛的顧客您好」"
        ]},
        {"title": "🔪 第二刀：換五感白描", "highlight": True, "lines": [
            "⭕ 換上有血有肉細節：",
            "• 剛起鍋表面微焦滋滋作響",
            "• 切開滿滿鮮甜肉汁",
            "• 冰鎮後咬下去脆甜回甘",
            "• 看得到色香味聲觸"
        ]},
        {"title": "🔪 第三刀：加顧店日常", "lines": [
            "⭕ 融入真實生活情境：",
            "• 「清晨五點頂著海風挑的」",
            "• 「剛幫大家分裝好冰進庫房」",
            "• 「傍晚下班順路來拿剛剛好」",
            "• 像隔壁老闆親自在對話"
        ]}
    ]
)

# 17
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 07 】", "五層捏臉 ✕ 去塑料三刀！產出店長 Prompt",
    "回答 5 個深度問題，讓 AI 將你的靈魂編譯為專屬店長 System Prompt 並存檔！",
    """請幫我執行「五層同心圓AI擬人化捏臉工程」。請嚴格依以下步驟執行：
【步驟1】先印出「五層同心圓人設架構表」（1.外觀與日常場景 2.語言指紋與口頭禪 3.為客著想的思考習慣 4.面對殺價的情緒邊界 5.開店初心信念）以及「預設禁用公文詞庫（親愛的、竭誠、味蕾饗宴、不容錯過）」。
【步驟2】請針對這五層，用最白話親切的方式提出 5 個問題訪問我。
【硬性約束】印出架構與 5 個問題後「立即停下來等待我回答」，嚴禁自行替我編造人設特徵！收到我的真實回答後，請將我的特色與「去塑料三刀原則」完美融合，為我編譯出一段可直接使用的『專屬AI數位店長 System Prompt』，存檔到工作區的 `SYSTEM_PROMPT.md`，同時在 `MAP.md` 補上它的路徑！""",
    "你的分身誕生：擁有你的口頭禪、思考習慣與人情溫度，直接存檔！"
)

# 18
create_concept_slide(
    "【 注入靈魂人設 03 】", "雙人設風格切換：專業職人 vs. 溫暖夥伴",
    "同一批商品，隨發文場景自由切換「懂貨闆仔」與「貼心小編」兩種魅力！",
    [
        {"title": "👨‍🍳 A. 專業懂貨職人風 (闆仔)", "lines": [
            "• 風格：話少、懂貨、刀子嘴豆腐心、講究工序",
            "• 語氣：「清晨第一刀現切，肉色清亮，這批油花夠漂亮，懂吃的老饕直接帶。」",
            "• 適用場景：新品到貨、強調規格品質、展現專業底氣"
        ]},
        {"title": "☕ B. 熱情貼心夥伴風 (小編/管家)", "highlight": True, "lines": [
            "• 風格：熱情、像隔壁鄰居倒熱茶、關心生活日常",
            "• 語氣：「大哥天冷要穿暖喔！今天幫大家留了 3 包好料，傍晚下班順路來拿煮鍋剛好！」",
            "• 適用場景：日常互動、提醒自取、生活化寒暄"
        ]}
    ]
)

# 19
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 08 】", "口氣實測！雙人設風格即時改寫",
    "輸入一樣商品，看 AI 如何在瞬間切換兩種完全不同的真人語氣！",
    """請幫我測試「雙人設語言風格切換」。請嚴格依以下步驟執行：
【步驟1】列出【A.專業懂貨職人風（話少內行、重規格品質）】與【B.熱情貼心夥伴風（親切寒暄、重日常貼心）】的語氣參數差異表。
【步驟2】詢問我：「請告訴我今天店裡剛準備好的一項商品名稱，以及它最迷人的一個特色？」
【硬性約束】請先輸出對照表並提問，立即停下來等待我回答，嚴禁自行編造商品！收到我的商品與特色後，請同時遵守「去塑料三刀法」與先前建立的 `PRODUCTS.md` 價格，分別用 A、B 兩種人設各寫出一段 60 字以內的招呼短文！""",
    "一秒切換靈魂：根據不同客人與檔期，展現不同維度的門市魅力！"
)

# 20
create_concept_slide(
    "【 大腦神經合體樞紐 】", "神經合體樞紐：隱藏思考鏈 <thought>",
    "先在心裡算好帳，再開口說人話！達成「價格 100% 精準，口氣 100% 溫暖」！",
    [
        {"title": "🧠 <thought> (內心暗中查證)", "danger": True, "lines": [
            "1. [查 PRODUCTS.md] 單包 180，滿 3 包自取價 480。",
            "2. [查 RULES.md] 正氣北路自取至 18:00，不可混寄。",
            "3. [調用人設] 溫暖小編口吻，主動提醒幫忙留貨。"
        ]},
        {"title": "🗣️ 正式對客開口 (真誠有溫度)", "highlight": True, "lines": [
            "「大哥哩賀！買 3 包自取剛好有特惠是 480 元（直接幫您省 60 元喔）！",
            "我先幫您挑 3 包漂亮的留在庫房，今天傍晚 6 點前順路過來拿就可以囉！」"
        ]}
    ]
)

# 21
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 09 】", "思考鏈防呆實測！先查表算價再開口",
    "出一個平時客人最愛問的難題考考 AI，看它如何精確查表並溫暖作答！",
    """從現在起，你回答任何客人問題都必須強制啟動「<thought> 隱藏思考鏈防呆機制」。請嚴格依以下步驟執行：
【步驟1】請先印出思考鏈標準公式：
`<thought>`
1. 查核 PRODUCTS.md：(確認精確品名、單價與多件優惠計算式)
2. 查核 RULES.md：(確認自取時段、運費門檻或限制條款)
3. 套用人設指紋：(檢查是否剔除公文禁詞、套用店長口頭禪)
`</thought>`
接著輸出【正式對客溫暖回覆】。
【步驟2】請向我提問：「老闆，請出一個客人平常最愛問您的『詢價、湊單或取貨問題』來考考我！」
【硬性約束】印出公式與提問後立即停下來等待我出題。收到我的考題後，你必須100%依據我們剛才建立的 `PRODUCTS.md` 與 `RULES.md` 真實數據在 `<thought>` 內完成精確驗算，最後輸出溫暖回覆！""",
    "物理鎖死算帳：絕不讓 AI 在對話框中胡說八道算錯錢！"
)

# 22
create_concept_slide(
    "【 全自動手腳閉環 】", "三週串連！代理式 AI 全自動閉環發射台",
    "大腦、手腳、數據骨架與靈魂全部到位，啟動 3 秒發文流水線！",
    [
        {"title": "步驟 1 ~ 2：輸入與查表", "lines": ["1. 老闆隨手拍一張商品照片", "2. AI 自動調用 PRODUCTS.md 抓價格"]},
        {"title": "步驟 3 ~ 4：守則與捏臉", "lines": ["3. AI 自動核對 RULES.md 帶入取貨規則", "4. 啟動 <thought> 套用五層人設"]},
        {"title": "步驟 5 ~ 6：發布與導流", "highlight": True, "lines": ["5. 生成主貼文 ＋ 第一則導流留言", "6. 直連 Meta 官方 API，3秒同步發布！"]}
    ]
)

# 23
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 10 】", "一鍵發射！閉環產出文案與導流留言",
    "指定一樣今日主打商品，一次產出不降觸及率的「主文 ＋ 首則導流留言」！",
    """請啟動「全自動閉環發射台」模式，幫我準備今日要發布至 Facebook 與 Threads 的貼文組合。請嚴格依以下步驟執行：
【步驟1】先列出發射台檢核清單：1.主推商品與價格核對 2.取貨與運費規則核對 3.五層人設與去塑料味檢核 4.主貼文與第一則導流留言分離設計（主文不放外部連結以免降觸及，連結與下單指引統一放第一則留言）。
【步驟2】詢問我：「老闆，今天這篇貼文我們要主打 `PRODUCTS.md` 裡的哪一樣商品？今天現場有沒有什麼特別的小亮點或天氣心情想順便提一下？」
【硬性約束】印出清單與問題後立即停下來等待我回答。收到回答後，請先用 `<thought>` 查核真實價格與店規，接著一次為我產出：【A. 社群主貼文】與【B. 第一則導流留言】！""",
    "流量密碼：外部購買連結放第一則留言，觸及率立增 3 倍！"
)

# 24
create_concept_slide(
    "【 帶走實體成果 】", "學員專屬大禮包：今天直接帶走的四大數位資產",
    "今天下課不是只有「聽懂了」，而是把整套刻著你店名的資產包帶回家！",
    [
        {"title": "01. 店面雙寶", "lines": ["MAP.md 與 PRODUCTS.md", "門市檔案地圖與階梯價格總表"]},
        {"title": "02. 防呆守則庫", "lines": ["RULES.md 營業規章", "SECURITY.md 防套話機密保密指令"]},
        {"title": "03. 店長 Prompt", "highlight": True, "lines": ["SYSTEM_PROMPT.md 五層捏臉", "<thought> 思考鏈指令直接存檔"]},
        {"title": "04. 官方 API 腳本", "danger": True, "lines": ["串接第 2 講 Meta API 自動發布", "照片一傳秒發社群！"]}
    ]
)

# 25
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 11 】", "全套資產大匯出！打包 Markdown 備份檔",
    "一鍵將今日對話的所有成果打包成單一文本，用記事本存檔永久擁有！",
    """請讀取工作區中今天建立的所有檔案，並對照我們的對話，把所有成果，完整彙整打包成一份「專屬AI數位店長核心資產總檔（All-in-One Markdown）」。
請嚴格按照以下五大區塊順序輸出在同一個 Markdown 代碼框內，方便我一鍵複製存檔：
1. `# 01_店面導航地圖 (MAP.md)`
2. `# 02_商品規格與階梯價格表 (PRODUCTS.md)`
3. `# 03_營運與防呆守則 (RULES.md)`
4. `# 04_商業機密防火牆與抗殺價指令 (.secrets / SECURITY.md 規範)`
5. `# 05_專屬數位店長 System Prompt (含五層同心圓人設 + 去塑料三刀 + <thought>思考鏈強制指令)`

【硬性約束】請100%根據我們今天對話與工作區檔案中的真實數據進行彙整，嚴禁竄改任何數字！輸出完後，最後另存一份到工作區的 `00_店長資產總檔_備份.md`。""",
    "一鍵備份：整座數位門市資產打包成一個檔案，隨開隨用！"
)

# 26
create_concept_slide(
    "【 三週大圓滿 · 結業精神 】", "數位工具只是手腳，你的在地真誠才是靈魂",
    "技術與 AI 模型每個月都在推陳出新，但你對食材工序的講究、以及對老客人的那份人情真心，是任何 AI 都取代不了的「終極護城河」。",
    [
        {"title": "大腦 (第 1 講)", "lines": ["學會整理真實資料", "建立在地故事智囊", "博學多聞"]},
        {"title": "手腳 (第 2 講)", "lines": ["解放雙手自動發布", "Meta 官方 API 直連", "高效自轉"]},
        {"title": "靈魂 (第 3 講)", "highlight": True, "lines": ["數位分身有溫度", "精準算帳不幻覺", "深得人心！"]}
    ]
)

# 27
create_prompt_slide(
    "【 實戰演練 · 讓 AI 帶你做 12 】", "榮耀結業！數位店長正式上線首發宣告",
    "完成最後一哩路！寫下專屬店長正式顧店的第一篇感性貼文，立刻發布！",
    """我的專屬 AI 數位店長已經完成全部訓練，準備正式上線了！請嚴格依以下步驟執行：
【步驟1】列出「數位店長上線首發文」四段式架構：
1. 暖心開場：用我的招牌口頭禪向老朋友打招呼，分享這三週去進修 AI 的真實心情。
2. 初心宣告：告訴客人引進 AI 不是為了變成冷冰冰的機器，而是為了省下瑣碎時間，把更多心力拿來顧好品質與服務大家。
3. 招牌推薦：自然帶出 `PRODUCTS.md` 裡的一項今日主打商品與 `RULES.md` 的貼心取貨方式。
4. 互動召喚：邀請老客人、新朋友在底下留言打聲招呼，測試看看數位分身有沒有像老闆本人！
【步驟2】詢問我：「老闆，這三週一路學下來，您最想對一直支持您店裡的老客人說的一句真心話是什麼？」
【硬性約束】請先印出架構並提問，立即停下來等待我回答。收到我的真心話後，請啟動 `<thought>` 結合我的五層人設，為我寫出這篇充滿溫度與成就感的上線首發貼文！""",
    "現場發布：讓你的專屬 AI 數位店長，今晚就正式在線上開張！"
)

output_pptx = r"C:\Users\lenovo\Desktop\第3講教學簡報.pptx"
prs.save(output_pptx)
print(f"Successfully generated 27-slide PPTX deck: {output_pptx}")
