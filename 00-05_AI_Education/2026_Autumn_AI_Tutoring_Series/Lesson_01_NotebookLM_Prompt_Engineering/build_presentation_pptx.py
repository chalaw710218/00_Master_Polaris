import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. Colors Definition (Polaris Dark & Amber Theme)
BG_COLOR = RGBColor(15, 23, 42)        # #0F172A Slate Dark
CARD_BG = RGBColor(30, 41, 59)         # #1E293B Slate Medium
CARD_BORDER = RGBColor(71, 85, 105)    # #475569 Slate Light
TEXT_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Pure White
TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Muted Grey
AMBER = RGBColor(245, 158, 11)         # #F59E0B Amber Gold
AMBER_LIGHT = RGBColor(251, 191, 36)   # #FBBF24 Amber Light
CYAN = RGBColor(56, 189, 248)          # #38BDF8 Cyan Light
EMERALD = RGBColor(16, 185, 129)       # #10B981 Emerald Green
ROSE = RGBColor(244, 63, 94)           # #F43F5E Rose Red

FONT_HEADING = "Microsoft JhengHei"
FONT_BODY = "Microsoft JhengHei"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = BG_COLOR
    bg_shape.line.fill.background()
    return bg_shape

def add_badge(slide, text, x, y, width=Inches(3.2), height=Inches(0.4), color=AMBER):
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(24, 34, 52)
    badge.line.color.rgb = color
    badge.line.width = Pt(1.5)
    tf = badge.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = FONT_HEADING
    p.alignment = PP_ALIGN.CENTER
    return badge

def add_header(slide, badge_text, title, subtitle="", badge_color=AMBER):
    set_slide_background(slide)
    add_badge(slide, badge_text, Inches(0.8), Inches(0.55), width=Inches(3.4), height=Inches(0.36), color=badge_color)
    
    # Title Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.font.name = FONT_HEADING
    
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MUTED
        p2.font.name = FONT_BODY
        p2.space_before = Pt(4)

def add_card(slide, x, y, width, height, title="", title_color=AMBER_LIGHT, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.3)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.25)
    
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.font.name = FONT_HEADING
        p.space_after = Pt(10)
    return card

# ==================== SLIDE 1: Cover ====================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)
add_badge(s1, "POLARIS AI MASTERCLASS · LESSON 01", Inches(0.8), Inches(1.3), width=Inches(3.8), height=Inches(0.4), color=AMBER)

title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.9), Inches(11.5), Inches(2.2))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "NotebookLM 深度應用與"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.font.name = FONT_HEADING

p2 = tf.add_paragraph()
p2.text = "「漏斗式三層深挖」提示法"
p2.font.size = Pt(44)
p2.font.bold = True
p2.font.color.rgb = AMBER_LIGHT
p2.font.name = FONT_HEADING
p2.space_before = Pt(6)

p3 = tf.add_paragraph()
p3.text = "告別「一上來就亮底牌問出罐頭廢話」的直覺誤區 ｜ 現場手把手鍛造專屬私密智囊"
p3.font.size = Pt(16)
p3.font.color.rgb = TEXT_MUTED
p3.font.name = FONT_BODY
p3.space_before = Pt(16)

# Meta info card
info_card = add_card(s1, Inches(0.8), Inches(4.8), Inches(11.7), Inches(1.8), border_color=AMBER)
tf = info_card.text_frame
p = tf.paragraphs[0]
p.text = "👑 主講人：陳品碩（闆仔） ＆ 雪 (CEO)  ｜  🏫 地點：生活管家 · 家宅總部"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p2 = tf.add_paragraph()
p2.text = "⏱️ 上課節奏：14:00 - 15:00 觀念拆解與實機示範  ｜  15:00 - 16:00 現場巡桌排錯，做完成果才下課！"
p2.font.size = Pt(13)
p2.font.color.rgb = CYAN
p2.space_before = Pt(8)

p3 = tf.add_paragraph()
p3.text = "💎 專屬方案：單堂 NT$ 500 元  ｜  老學員享專屬回娘家禮遇 · 免費參加複訓"
p3.font.size = Pt(13)
p3.font.color.rgb = EMERALD
p3.space_before = Pt(6)


# ==================== SLIDE 2: Agenda ====================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "TIME & FLOW · 雙核閉環", "今日 120 分鐘學習路線圖", "拒絕「講師台上炫技、學員回家卡死」；前半段拆透原理，後半段直接巡桌把成果做出來！", CYAN)

c1 = add_card(s2, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5), "🧭 上半場：核心精講 (60 Mins)", AMBER_LIGHT, AMBER)
tf = c1.text_frame
items1 = [
    ("第 1 節 (20m)", "NotebookLM 核心原理與資料接地 (Grounding)"),
    ("第 2 節 (25m)", "靈魂心法——「漏斗式三層深挖提問法」全解析"),
    ("第 3 節 (15m)", "現場實況對照組直擊 ＆ Audio Overview 音訊生成")
]
for title, desc in items1:
    p = tf.add_paragraph()
    p.text = f"🔸 {title}："
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = AMBER_LIGHT
    p.space_before = Pt(12)
    p2 = tf.add_paragraph()
    p2.text = f"    {desc}"
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

c2 = add_card(s2, Inches(6.9), Inches(2.2), Inches(5.6), Inches(4.5), "🛠️ 下半場：實機闖關 ＆ 排錯 (60 Mins)", CYAN, EMERALD)
tf = c2.text_frame
items2 = [
    ("實戰關卡 1 (15m)", "裝載手邊 3~5 份資料，建立個人專屬知識庫"),
    ("實戰關卡 2 (30m)", "三層漏斗提問闖關（解決真實痛點，現場產出）"),
    ("實戰關卡 3 (15m)", "生成雙人音訊 Podcast，一對一巡桌除錯驗收")
]
for title, desc in items2:
    p = tf.add_paragraph()
    p.text = f"🔹 {title}："
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN
    p.space_before = Pt(12)
    p2 = tf.add_paragraph()
    p2.text = f"    {desc}"
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED


# ==================== SLIDE 3: The Pain Point ====================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "THE FATAL TRAP · 痛點直擊", "為什麼你問 AI，永遠只得到「官腔廢話」？", "大家常常把厚厚的文件丟給 AI，敲下一行：『請幫我看看這份資料，給我最落地的行銷破局解法！』", ROSE)

c1 = add_card(s3, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5), "❌ AI 回敬你的「罐頭公文」", ROSE, ROSE)
tf = c1.text_frame
points = [
    "要加強社群宣傳、提升品牌形象",
    "精準鎖定核心客群、擴大曝光渠道",
    "優化客戶服務流程、定期舉辦優惠活動",
    "建立數據監控機制、持續優化營運策略"
]
for pt in points:
    p = tf.add_paragraph()
    p.text = f"• {pt}"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(10)

p_bot = tf.add_paragraph()
p_bot.text = "👉 說了等於沒說，挑不出毛病但完全無法落地！"
p_bot.font.size = Pt(13)
p_bot.font.bold = True
p_bot.font.color.rgb = ROSE
p_bot.space_before = Pt(20)

c2 = add_card(s3, Inches(6.9), Inches(2.2), Inches(5.6), Inches(4.5), "💡 真正的死因到底在哪？", AMBER_LIGHT, AMBER)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "不是 AI 笨，而是我們犯了「太心急、一開始就直接亮底牌單刀直入」的錯誤！"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

p2 = tf.add_paragraph()
p2.text = "就像你剛走進老診所，連坐都還沒坐下、醫生連病歷表都還沒翻開，你就逼著他開特效藥。"
p2.font.size = Pt(13)
p2.font.color.rgb = TEXT_MUTED
p2.space_before = Pt(14)

p3 = tf.add_paragraph()
p3.text = "AI 的上下文記憶 (Context) 根本還沒「預熱」，在這種狀態下，它除了在表面關鍵字瞎猜、吐出官僚公文，別無選擇！"
p3.font.size = Pt(13)
p3.font.color.rgb = AMBER_LIGHT
p3.space_before = Pt(14)


# ==================== SLIDE 4: NotebookLM Architecture ====================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "ZERO-HALLUCINATION · 核心工具", "什麼是 NotebookLM？零幻覺的企業第二大腦", "Google 專為知識工作者打造的私密接地智庫，從根源徹底消滅傳統 LLM 瞎掰的毛病！", CYAN)

cards_data = [
    ("🔒 100% 資料接地 (Grounding)", "資料沒寫的，它絕對不瞎掰！回答嚴格鎖定在你上傳的知識邊界內，杜絕 ChatGPT 的胡言亂語。", AMBER_LIGHT),
    ("📑 即時來源標註 (Citations)", "回答末端附帶引用數字，點擊直接跳轉高亮原文段落。所有商業決策有憑有據、100% 憑據可靠。", CYAN),
    ("📂 多來源混合裝載 (Multi-Source)", "單一筆記本可裝載多達 50 份資料，支援 PDF、Google Docs、網頁 URL、音訊轉逐字稿與 YouTube。", EMERALD)
]
for i, (title, desc, col) in enumerate(cards_data):
    x = Inches(0.8 + i * 4.0)
    c = add_card(s4, x, Inches(2.2), Inches(3.7), Inches(3.6), title, col)
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

priv_card = add_card(s4, Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.85), border_color=CYAN)
tf = priv_card.text_frame
p = tf.paragraphs[0]
p.text = "🛡️ 商業級隱私承諾：你上傳的所有專屬文件與對話，絕不會被 Google 拿去訓練公共模型，資料主權 100% 屬於你！"
p.font.size = Pt(12.5)
p.font.color.rgb = CYAN


# ==================== SLIDE 5: The Funnel Overview ====================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "THE CORE METHODOLOGY · 靈魂心法", "「漏斗式三層深挖提問法」架構", "將 AI 提問從「單次碰運氣」升級為「三階步步逼近的精密手術」！", AMBER)

f_steps = [
    ("第一層：廣角鋪陳 · 全景掃描 (Macro Context)", "不急著切入主題、絕不亮底牌！先引導 AI 通讀全文，客觀畫出全域框架與 3 大核心支柱。", CYAN, Inches(0.8), Inches(11.7)),
    ("第二層：層層堆疊 · 垂直深挖 (Meso Probing)", "以子之矛，反向逼問！抓著第一層整理出的骨幹節點，逼問具體客觀數據、底層因果與失敗教訓。", AMBER_LIGHT, Inches(1.3), Inches(10.7)),
    ("第三層：圖窮匕見 · 微觀求解 (Micro Resolution)", "此時上下文已極度高溫預熱！拋出你個人最真實的產品、預算與人手限制，收穫一擊必殺的破局方案。", EMERALD, Inches(1.8), Inches(9.7))
]

for i, (title, desc, col, x, w) in enumerate(f_steps):
    y = Inches(2.2 + i * 1.6)
    c = add_card(s5, x, y, w, Inches(1.4), title, col, col)
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)


# ==================== SLIDE 6: Funnel Layer 1 ====================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "LAYER 1 · 宏觀掃描", "第一層【廣義全景 · 鋪開地圖】", "心法原則：先別告訴 AI 你想幹嘛！不帶任何個人主觀預設立場，先讓 AI 把全域地圖鋪開。", CYAN)

c1 = add_card(s6, Inches(0.8), Inches(2.2), Inches(11.7), Inches(1.5), "🎯 為什麼要這樣做？建立「全域注意力索引」", CYAN)
tf = c1.text_frame
p = tf.add_paragraph()
p.text = "LLM 就像一個需要暖機的大腦。先要求 AI 做宏觀梳理，是為了逼它建立全域注意力索引 (Global Attention Map)。當它先對全局建立完整概念，後續的思考才不會狹隘偏頗或斷章取義！"
p.font.size = Pt(13)
p.font.color.rgb = TEXT_MUTED
p.space_before = Pt(4)

p_box = add_card(s6, Inches(0.8), Inches(3.9), Inches(11.7), Inches(2.8), "📋 第一層示範 PROMPT（現場可直接套用）", AMBER_LIGHT, AMBER)
tf = p_box.text_frame
prompt_text = (
    "「請先不要給我任何業務建議或下結論。\n"
    "請全面閱讀我上傳的這幾份資料，用中立客觀的視角幫我梳理：\n"
    "這幾份文件最核心探討的 3 個主要面向是什麼？各自的核心論點與架構框架為何？」"
)
p = tf.add_paragraph()
p.text = prompt_text
p.font.size = Pt(13.5)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(6)

p_sub = tf.add_paragraph()
p_sub.text = "👉 成果檢核：AI 應該會條列出清晰的 3 大面向骨幹，這就是我們下一步垂直深挖的基石！"
p_sub.font.size = Pt(12)
p_sub.font.color.rgb = CYAN
p_sub.space_before = Pt(10)


# ==================== SLIDE 7: Funnel Layer 2 ====================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "LAYER 2 · 垂直深挖", "第二層【層層堆疊 · 垂直深挖】", "心法原則：檢視 AI 第一層整理出來的架構節點，挑選最要害的章節，要求它提供「數據」與「因果」。", AMBER)

c1 = add_card(s7, Inches(0.8), Inches(2.2), Inches(5.6), Inches(1.5), "⛏️ 逼出資料裡的「隱性知識」", AMBER_LIGHT)
tf = c1.text_frame
p = tf.add_paragraph()
p.text = "很多報告最精華的其實是「客觀摩擦成本」與「曾嘗試過但失敗的教訓」。我們要逼 AI 把藏在字裡行間的真實障礙翻出來！"
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

c2 = add_card(s7, Inches(6.9), Inches(2.2), Inches(5.6), Inches(1.5), "🔥 上下文完全預熱 (Context Saturation)", EMERALD)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "此時 AI 已經從表面文章通讀，深入到具體條款與因果細節，它的神經元狀態已經調整至「專案專家」模式！"
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

p_box = add_card(s7, Inches(0.8), Inches(3.9), Inches(11.7), Inches(2.8), "📋 第二層示範 PROMPT（以子之矛反向逼問）", AMBER_LIGHT, AMBER)
tf = p_box.text_frame
prompt_text = (
    "「在剛剛提到的第 2 點（例如：顧客回流率偏低與配送摩擦成本）之中：\n"
    "1. 原文中具體提到了哪些客觀數據或案例？\n"
    "2. 造成這些現象的底層因果鏈是什麼？\n"
    "3. 資料中是否有提及過去曾嘗試過、但成效不彰的解法？」"
)
p = tf.add_paragraph()
p.text = prompt_text
p.font.size = Pt(13.5)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(6)


# ==================== SLIDE 8: Funnel Layer 3 ====================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "LAYER 3 · 終極求解", "第三層【圖窮匕見 · 微觀求解】", "心法原則：在深厚脈絡完全飽和後，這時才把你的「真實限制」與「私人困局」拋出來！", EMERALD)

p_box = add_card(s8, Inches(0.8), Inches(2.2), Inches(11.7), Inches(2.6), "📋 第三層示範 PROMPT（圖窮匕見 · 直擊痛點）", EMERALD, EMERALD)
tf = p_box.text_frame
prompt_text = (
    "「很好！現在完全立足於前面梳理出的全域框架，以及第 2 層深挖到的失敗教訓與摩擦成本：\n\n"
    "我目前正遇到［具體描述我的產品 / 現有預算 / 時間與人手限制］，\n"
    "請站在這份資料的角度，為我量身制定一套最可執行的 3 步破局方案，並說明為何能避開剛剛提到的坑。」"
)
p = tf.add_paragraph()
p.text = prompt_text
p.font.size = Pt(13.5)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(6)

c1 = add_card(s8, Inches(0.8), Inches(5.0), Inches(5.6), Inches(1.8), "🌟 產出答案的降維升級", EMERALD)
tf = c1.text_frame
p = tf.add_paragraph()
p.text = "• 不再是空泛的「加強宣傳」，而是運用資料裡的具體工具\n• 主動提醒你避開過去踩過的失敗路徑\n• 精確吻合你的時間與資源預算限制"
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED
p.space_before = Pt(4)

c2 = add_card(s8, Inches(6.9), Inches(5.0), Inches(5.6), Inches(1.8), "⚡ 關鍵心智躍遷", AMBER_LIGHT)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "你不再是向一個「無知機器人」碰運氣問路，而是向一位「已經通讀你全部機密、又了解你限制的頂級顧問」做閉門諮詢！"
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED
p.space_before = Pt(4)


# ==================== SLIDE 9: Real Case Comparison ====================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "SHOWCASE · 現場實況對照", "實機對照：兩種問法的天壤之別", "以「生活管家 5D 報價單與客服談判」為例，現場投影實測對比：", ROSE)

c1 = add_card(s9, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5), "❌ 傳統直覺問法 (單刀直入)", ROSE, ROSE)
tf = c1.text_frame
p = tf.add_paragraph()
p.text = "提問：「我客戶嫌貴想砍價，我該怎麼回？」"
p.font.size = Pt(13)
p.font.color.rgb = AMBER_LIGHT
p.space_before = Pt(6)

p2 = tf.add_paragraph()
p2.text = (
    "\n【AI 典型回覆】：\n"
    "您好，您可以向客戶強調服務品質好、技術專業，或者適度給予 9 折優惠維持長期合作關係，並提供售後服務保障……\n\n"
    "👉 毫無防禦力的退讓廢話！除了教你割肉打折，毫無實戰價值。"
)
p2.font.size = Pt(12)
p2.font.color.rgb = TEXT_MUTED

c2 = add_card(s9, Inches(6.9), Inches(2.2), Inches(5.6), Inches(4.5), "✅ 漏斗三層深挖法 (層層堆疊)", EMERALD, EMERALD)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "提問：通讀 5D 憲綱 ➔ 追問 D1 隱形工時 ➔ 求解"
p.font.size = Pt(13)
p.font.color.rgb = CYAN
p.space_before = Pt(6)

p2 = tf.add_paragraph()
p2.text = (
    "\n【AI 犀利回覆】：\n"
    "依據您的 5D 憲綱：\n"
    "1. 堅持「勞務與採買分離」，堅決拒絕打折！\n"
    "2. 調出 D1 採買隱形工時清單禮貌展示給客戶。\n"
    "3. 提供選擇：若預算有限，可刪減 D5 隨行安心項目，絕不委屈降價！\n\n"
    "👉 刀刀見血的高情商防禦話術，守住利潤與尊嚴！"
)
p2.font.size = Pt(12)
p2.font.color.rgb = TEXT_MUTED


# ==================== SLIDE 10: Audio Overview ====================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "BONUS FEATURE · 黑科技加碼", "Audio Overview：生硬報告變雙人 Podcast", "開車通勤、做家事沒空讀長篇資料？讓兩位美式幽默 AI 主持人「聊」給你聽！", CYAN)

c1 = add_card(s10, Inches(0.8), Inches(2.2), Inches(6.5), Inches(4.5), "🎙️ 什麼是 Audio Overview？", CYAN)
tf = c1.text_frame
bullets = [
    ("一鍵生成對談", "NotebookLM 獨家語音功能，自動把所有筆記轉成 8~15 分鐘雙人廣播。"),
    ("語氣極致逼真", "兩位主持人會互相吐槽、開玩笑、抓出最有趣的對比與核心痛點。"),
    ("通勤無痛吸收", "開車戴耳機，像聽知名 Podcast 一樣輕鬆聽完一整份幾萬字的報告！")
]
for title, desc in bullets:
    p = tf.add_paragraph()
    p.text = f"• {title}："
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = AMBER_LIGHT
    p.space_before = Pt(12)
    p2 = tf.add_paragraph()
    p2.text = f"    {desc}"
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

c2 = add_card(s10, Inches(7.8), Inches(2.2), Inches(4.7), Inches(4.5), "🎧 現場體驗任務", AMBER_LIGHT, AMBER)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "現場戴耳機試聽！"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(10)

p2 = tf.add_paragraph()
p2.text = (
    "下半場實作時，每個人都會現場點擊「Generate」按鈕！\n\n"
    "當你戴上耳機，聽見兩位專業主持人幽默討論「你自己的公司與商品」時，那種震撼感只有親身體會才能懂！"
)
p2.font.size = Pt(13)
p2.font.color.rgb = TEXT_MUTED
p2.space_before = Pt(14)


# ==================== SLIDE 11: Hands-on Drill ====================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "HANDS-ON DRILL · 下半場實作", "下半場：60 分鐘現場闖關實戰", "請打開你的筆記型電腦！創辦人與幕僚現場巡桌排錯，保證帶著成果下課！", EMERALD)

drills = [
    ("🎯 關卡一：建立智庫 (15m)", "挑選 3~5 份個人現有文件（產品型錄、企劃案、客戶對話紀錄），匯入 NotebookLM 建立索引，點擊確認 Citation 跳轉正常。", CYAN),
    ("🎯 關卡二：三層漏斗提問 (30m)", "套用講義 Prompt：\n1. 輸入第 1 層鋪開全貌\n2. 輸入第 2 層追問因果\n3. 輸入自己最頭痛的難題，取得落地解法並截圖存檔！", AMBER_LIGHT),
    ("🎯 關卡三：生成播客 ＆ 驗收 (15m)", "點擊生成 Audio Overview，戴耳機試聽專屬廣播；現場巡桌一對一排錯，邀請 2 位學員投影分享！", EMERALD)
]
for i, (title, desc, col) in enumerate(drills):
    x = Inches(0.8 + i * 4.0)
    c = add_card(s11, x, Inches(2.2), Inches(3.7), Inches(4.5), title, col, col)
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(10)


# ==================== SLIDE 12: Summary ====================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "SUMMARY & NEXT STEPS", "今日收穫回顧 ＆ 下週預告", "恭喜各位！你今天已經正式告別了「AI 幻覺與被動找資料」的時代。", AMBER)

c1 = add_card(s12, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5), "✅ 今日帶走的 3 大資產", AMBER_LIGHT, AMBER)
tf = c1.text_frame
assets = [
    "一套專屬於你企業/業務的 NotebookLM 零幻覺私密智庫",
    "一套終生受用的「漏斗式三層深挖提問法」心智模型",
    "一支可以直接通勤收聽的專屬 Audio Overview 雙人廣播"
]
for a in assets:
    p = tf.add_paragraph()
    p.text = f"• {a}"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(14)

c2 = add_card(s12, Inches(6.9), Inches(2.2), Inches(5.6), Inches(4.5), "🚀 下週三 (11/04) 第 2 講預告", CYAN, CYAN)
tf = c2.text_frame
p = tf.add_paragraph()
p.text = "Antigravity 操作與 Meta 自動發文串接"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(10)

p2 = tf.add_paragraph()
p2.text = (
    "掌握 Google Antigravity 終端代理操作；\n"
    "串接 Facebook Graph API 與 Threads 官方排程，\n"
    "打造 24/7 自動發布社群的「全自動數位印鈔機」！"
)
p2.font.size = Pt(13)
p2.font.color.rgb = TEXT_MUTED
p2.space_before = Pt(14)

# Save presentation
output_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_01_NotebookLM_Prompt_Engineering\slides.pptx"
prs.save(output_path)
print(f"Successfully generated: {output_path}")
