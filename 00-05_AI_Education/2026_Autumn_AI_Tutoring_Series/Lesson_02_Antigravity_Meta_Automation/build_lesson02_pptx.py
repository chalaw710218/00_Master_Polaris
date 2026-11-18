# -*- coding: utf-8 -*-
"""
生成極簡高清晰教學簡報 (PPTX) - 創辦人精煉極簡版
特點：
- 字數大幅精簡 70%，只留關鍵名詞、點擊步驟與核心口訣
- 字級加大（標題 26pt、卡片標題 18pt、內文 15pt），投影一目了然
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BG_COLOR = RGBColor(10, 15, 29)          # #0A0F1D 深藍黑
CARD_BG = RGBColor(18, 26, 47)           # #121A2F 卡片深藍
CARD_BORDER = RGBColor(56, 189, 248)     # #38BDF8 青藍
TEXT_WHITE = RGBColor(248, 250, 252)     # 純白
TEXT_MUTED = RGBColor(203, 213, 225)     # 淺灰（提高對比度）
AMBER = RGBColor(245, 158, 11)           # 琥珀金
EMERALD = RGBColor(16, 185, 129)         # 翡翠綠
ROSE = RGBColor(244, 63, 94)             # 玫瑰紅
PURPLE = RGBColor(168, 85, 247)          # 紫色

FONT_HEADING = "Microsoft JhengHei"
FONT_BODY = "Microsoft JhengHei"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_bg(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = BG_COLOR
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, tag_text, title, subtitle="", tag_color=CARD_BORDER):
    set_bg(slide)
    
    # Tag Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.2), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(20, 30, 55)
    badge.line.color.rgb = tag_color
    badge.line.width = Pt(1.5)
    tf = badge.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = tag_text
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = tag_color
    p.font.name = FONT_HEADING
    p.alignment = PP_ALIGN.CENTER
    
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.02), Inches(11.7), Inches(0.75))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.font.name = FONT_HEADING
    
    # Subtitle
    if subtitle:
        s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.45))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.size = Pt(14)
        p_s.font.color.rgb = CARD_BORDER
        p_s.font.name = FONT_BODY

def add_card(slide, x, y, width, height, title, items, border_color=CARD_BORDER, title_color=TEXT_WHITE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.28)
    
    # Card Title
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = title_color
    p0.font.name = FONT_HEADING
    p0.space_after = Pt(12)
    
    # Items
    for item in items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = FONT_BODY
        p.space_after = Pt(8)
    return card

# ==========================================
# Slide 1: 封面 (Cover)
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_bg(s1)
add_card(s1, Inches(1.5), Inches(1.3), Inches(10.33), Inches(4.8),
         "生活管家 · 2026 秋季實戰家教班 · 第 2 講",
         [
             "🚀 告別手動複製貼上！把社群發射台交給 AI",
             "🔗 Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads)",
             "",
             "📍 地點：台東市正氣北路166巷90號（家宅總部）",
             "⏰ 時間：2026-11-18 (週三) 14:00 - 16:00",
             "🎯 目標：現場實機走通，帶走專屬自動發射台！"
         ], AMBER, AMBER)

# ==========================================
# Slide 2: 溫故知新 (Review)
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "溫故知新 · 邏輯承接", "上週做好了故事海報與文案，然後呢？", "好內容已經誕生，為什麼我們依然感覺被社群折磨？")
add_card(s2, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🎉【上週的驕傲戰果】",
         [
             "• NotebookLM 深度消化真實資料",
             "• 親手產出：專屬故事海報 ＋ 文案",
             "• 智囊大腦已經就位！",
             "",
             "✨ 我們已經擁有產出高品質內容的能力！"
         ], EMERALD, EMERALD)
add_card(s2, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "⚠️【今天面臨的現實卡點】",
         [
             "• 海報躺在電腦裡，不會自己飛出去",
             "• 開店忙備料招呼客人，沒空天天發",
             "• 一旦漏發，社群觸及直接斷線！",
             "",
             "🚀 今天的使命：裝上「全自動發射引擎」！"
         ], ROSE, ROSE)

# ==========================================
# Slide 3: 創辦人心法 (Cognitive Anchor) - 品碩親授精煉版
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "創辦人心法 · 認知定錨", "AI 的應用取決於認知，學好 AI 取決於熟練度", "工具不會自動改變生意，唯有你的認知與熟練，才是真正護城河！")
add_card(s3, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🧠【認知決定高度：AI 不是神話，是數位分身】",
         [
             "• 你怎麼看待 AI，AI 就怎麼回報你",
             "• ❌ 當聊天玩具 ➔ 只會講笑話",
             "• ⭕ 當發射總機 ➔ 替你扛起全天候運營",
             "",
             "💡 思維躍升：從手動搬運工 ➔ 數位指揮官！"
         ], PURPLE, PURPLE)
add_card(s3, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "⚡【熟練成就護城河：天天交代，勝過狂讀】",
         [
             "• 熟練不是背代碼，而是養成「交代 AI」的習慣",
             "• 每天對話 10 分鐘，勝過狂讀 10 小時",
             "• 越常使用，你的數位神經反射就越快",
             "",
             "🎯 今天的實戰：把認知化為身體的肌肉記憶！"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 4: 什麼是 Antigravity？
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "核心概念 · 定位解密", "Antigravity 究竟是什麼？", "它不是一般的聊天網頁，它是住在你筆電裡的「24 小時數位發射員」")
add_card(s4, Inches(0.8), Inches(2.4), Inches(3.6), Inches(4.5),
         "❌ 傳統網頁 AI",
         [
             "• 關在瀏覽器框框裡",
             "• 看不到你電腦的檔案",
             "• 無法替你執行發布指令",
             "• 每次都要手動複製貼上"
         ], ROSE, ROSE)
add_card(s4, Inches(4.8), Inches(2.4), Inches(3.6), Inches(4.5),
         "⚡ Antigravity 核心能力",
         [
             "• 長住在你的本機電腦中",
             "• 直接讀取桌面的圖片文案",
             "• 自帶手腳：能跑發射腳本",
             "• 直連 Meta 官方發布貼文"
         ], CARD_BORDER, CARD_BORDER)
add_card(s4, Inches(8.8), Inches(2.4), Inches(3.6), Inches(4.5),
         "🎯 你的數位發射台",
         [
             "• 如店裡請了全職發射員",
             "• 丟進資料夾",
             "• 自動打包 ➔ 定時",
             "• 一鍵推上社群時間軸！"
         ], AMBER, AMBER)

# ==========================================
# Slide 5: 現場演示 (Live Demo)
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "現場表演 · 震撼見證", "現場實機演示：倒數 3 秒，全自動發射！", "請大家拿出手機，打開我們的 Facebook 粉絲專頁與 Threads……")
add_card(s5, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🎬【現場實機演示流程】",
         [
             "1. 電腦資料夾：一張照片 ＋ 一段文字",
             "2. 完全不開 FB / Threads 網頁",
             "3. 終端機按一行：python launch_my_post.py",
             "4. ⚡ 3 秒完成：上傳圖片 ➔ 發布 ➔ 掛留言！"
         ], AMBER, AMBER)
add_card(s5, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "📱【請大家看手機驗收】",
         [
             "• Facebook 粉專：新貼文秒級上線！",
             "• Threads：同步推播，演算法曝光！",
             "• 第一則留言：自動附帶購買連結（防降權）！",
             "",
             "✨「每天半小時的折磨，電腦 3 秒做完！」"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 6: 為什麼絕對走官方 API？
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "安全第一 · 法規護城河", "為什麼絕對不用外掛？Meta 官方 API 是唯一合法保險", "做生意粉專是命根子！絕不拿辛苦累積的資產冒險")
add_card(s6, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "❌ 坊間黑心爬蟲 / 外掛",
         [
             "• 模擬真人點擊，Meta 系統天天抓",
             "• 隨時面臨永久封號、資產歸零！",
             "• 帳密外洩風險，恐遭盜刷或綁架"
         ], ROSE, ROSE)
add_card(s6, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "⭕ Meta 官方 Graph API 直連",
         [
             "• 官方正式核發的合法通行證",
             "• 永不封號，受 Meta 官方正式保障",
             "• 金鑰鎖在本地 .secrets.env，主權在握！"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 7: 品碩親授 · 10 步黃金發射台 SOP (關鍵點擊步驟)
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "品碩親授 · 避坑指南", "Meta 官方自動發文 · 10 步黃金發射台 SOP", "口訣：「5 步選對案例，8 步給對權限，9 步切換門牌，10 步鎖定長效！」")
add_card(s7, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🚀【前半段：建立總機發射台】",
         [
             "01. 打開：developers.facebook.com",
             "02. 點擊：右上角【我的應用程式】",
             "03. 點擊：【建立應用程式】選【企業商家】",
             "04. 命名：輸入【我的AI小編助理】",
             "05. 案例：⭐ 必勾【管理粉絲專頁的所有內容】(⚑)",
             "    （關鍵！選對才能解鎖發文權限）"
         ], AMBER, AMBER)
add_card(s7, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "🔑【後半段：調用金鑰與延期】",
         [
             "06. 點擊：頂部導航列【工具】",
             "07. 進入：【圖形 API 測試工具】",
             "08. 拉權限：勾選 pages_manage_posts",
             "09. 切換粉專：點產生權杖 ➔ 選單切換至【你的粉專】",
             "10. 延期：進入【偵錯工具】點延長 ➔ 升級 60 天金鑰！"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 8: 1 個 App 對應多個粉專 (架構解密)
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "架構解密 · 商業賦能", "一個應用程式，能不能同時管理多個粉專？", "答案是：絕對可以！單一中央發射台，掌控無數品牌門牌！")
add_card(s8, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🏢【1 對多發射台架構】",
         [
             "• 應用程式 (App) = 中央通訊發射台",
             "• 用戶權杖 (User Token) = 主通行證",
             "• 粉專權杖 (Page Token) = 各粉專獨立鑰匙",
             "",
             "👉 一個 App 可同時取得 5 個、10 個粉專金鑰！"
         ], CARD_BORDER, CARD_BORDER)
add_card(s8, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "💼【生活管家代操商業價值】",
         [
             "• 免為每個小農或分店重複申請 App",
             "• 只要將帳號設為協同管理員，即可代發",
             "",
             "🚀 實測驗證：已成功打通生活管家、阿美族學學會、獨賣早餐、雙饗丼等 5 大粉專！"
         ], PURPLE, PURPLE)

# ==========================================
# Slide 9: 發射原理（行李托運）
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "發射原理 · 核心機制", "為什麼發文要分兩段？社群 API 行李托運定律", "出國托運行李，不能把行李箱直接塞進登機證！")
add_card(s9, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🧳【第一階段：上傳圖片拿吊牌】",
         [
             "• 呼叫 POST /PAGE_ID/photos (published=false)",
             "• 先把照片送上 Meta 傳送帶",
             "• 取得官方號碼牌：Media ID",
             "• （照片暫存雲端，尚未公開）"
         ], AMBER, AMBER)
add_card(s9, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "🚀【第二階段：合體推播 ＋ 暗樁】",
         [
             "• 呼叫 POST /PAGE_ID/feed",
             "• 文案 ＋ Media ID 合體發射 ➔ 貼文秒級上線！",
             "• 💬 自動暗樁：1 秒後自動留第一則留言",
             "• 外部連結放留言，主文觸及率 100% 不降權！"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 10: 讓 AI 助教帶你做 (對話流)
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "高維進化 · 人機協同", "步驟太多記不住？讓 AI 助教坐在電腦裡帶你做！", "今天不用背代碼！打開對話框，Agent 手把手帶你完成")
add_card(s10, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🤖【專屬助教的 4 大主動能力】",
         [
             "1. 主動指引：手把手問「建好 App 了嗎？」",
             "2. 保管金鑰：貼上 Token，自動存入保險箱",
             "3. 素材排版：自動看桌面照片與文案",
             "4. 一鍵發射：你說「確認發射」，立刻推送！"
         ], PURPLE, PURPLE)
add_card(s10, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "💬【現場實機開練 3 步】",
         [
             "01 輸入通關密語：",
             "   「請一步一步帶我打造社群發射台」",
             "02 依序貼上 Token 交代照片與文案",
             "03 說一聲：「確認發射！」",
             "",
             "⚠️ 講師與助教全場巡桌，排錯到底！"
         ], EMERALD, EMERALD)

# ==========================================
# Slide 11: 總結與帶走資產
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "總結與帶走資產 · 下週預告", "今天帶走的不是一張證書，而是一套自轉系統！", "恭喜大家跨過數位轉型最高的一道門檻！")
add_card(s11, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.5),
         "🎁【今天帶回家的 3 大數位資產】",
         [
             "1. 實體自動發射台：丟圖丟字一鍵發布",
             "2. Meta 官方 60 天合規通行證：永不封號",
             "3. 買回時間的主權：省下時間顧店與生活！"
         ], EMERALD, EMERALD)
add_card(s11, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.5),
         "🔮【下週預告 · 第 3 講】",
         [
             "《數據架構 ✕ 品牌人設工程：打造專屬語氣的 AI 管家》",
             "",
             "• 自動發文搞定了，文案怎麼越寫越像你？",
             "• 讓 AI 像「闆娘親自說話」一樣接地氣！",
             "• 下週三下午 14:00，正氣北路家宅總部見！"
         ], AMBER, AMBER)

desktop_pptx = r"C:\Users\lenovo\Desktop\第2講教學簡報.pptx"
prs.save(desktop_pptx)
print("PPTX Saved successfully with high-clarity concise cards:", desktop_pptx)
