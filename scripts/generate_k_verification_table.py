import sys
import re
from pathlib import Path

p_core = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core")
sys.path.insert(0, str(p_core))
import evidence_gate

cache_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_page_cache")
out_table_path = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\k_verification_table.md")

p_kb = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p_kb.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]

# Verification specifications
specs = {
    "K-001": {
        "status": "【對不上】",
        "quote": "無（網頁轉向英超曼城足球新聞）",
        "notes": "網頁重導向至《The Standard》體育報導（Pep Guardiola predicts what will happen to Man City against West Ham），查無 Threads 演算法與 engagement bait 內容。"
    },
    "K-002": {
        "status": "【已驗證】",
        "quote": "We find that use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. We refer to this effect as Model Collapse and show that it can occur in Variational Autoencoders, Gaussian Mixture Models and LLMs.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，arXiv 論文摘要原文與假說完全吻合。"
    },
    "K-003": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-004": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-005": {
        "status": "【已驗證】",
        "quote": "Third places is a term coined by sociologist Ray Oldenburg and refers to places where people spend time between home ('first' place) and work ('second' place).",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，支持第三空間與社區向心力定義。"
    },
    "K-006": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓取成功，但內容為 Anthropic 官方提示詞工程總覽導航目錄，查無「使用主動動詞消除 AI 腔」之支持原文。"
    },
    "K-007": {
        "status": "【已驗證】",
        "quote": "Slow Food is a global movement of local groups and activists united by the common goal of ensuring everyone has access to good, clean and fair food.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，支持國際慢食核心三原則（Good/Clean/Fair）。"
    },
    "K-008": {
        "status": "【已驗證】",
        "quote": "Social media algorithms act as primary distribution filters. They heavily amplify content that captures early, high-velocity engagement like saves and shares, while actively burying passive, low-effort content beneath more competitive signals.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過。概念吻合高初速互動（high-velocity engagement），但原摘要之「30至60分鐘」時間數字在原文中無出處。"
    },
    "K-009": {
        "status": "【已驗證】",
        "quote": "The city of Oldenburg has pursued a systematic strategy to promote age-friendliness since 2012, guided by the eight domains of the WHO “Age-Friendly Cities” framework.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，確認 WHO 八大高齡友善範疇（eight domains of the WHO Age-Friendly Cities framework）。"
    },
    "K-010": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-011": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-012": {
        "status": "【已驗證】",
        "quote": "The Threads algorithm prioritizes signals that show genuine interest, such as replies, profile visits, time spent engaging with a post, and repeat interactions with an author.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，支持 Threads 推薦系統主動互動與回覆權重高於被動滑動之論述。"
    },
    "K-013": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（遭 reCAPTCHA 防火牆攔截，無法讀取論文正文）。"
    },
    "K-014": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（Medium 登入/轉址攔截，長度僅 424 字元查無正文）。"
    },
    "K-015": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-016": {
        "status": "【對不上】",
        "quote": "Articles from Journal of Fungi are provided here courtesy of Multidisciplinary Digital Publishing Institute (MDPI)",
        "notes": "網頁抓取成功，但該論文發表於真菌學期刊《Journal of Fungi》（真菌生物學研究），與跨世代資訊接觸及青銀信任完全無關。"
    },
    "K-017": {
        "status": "【已驗證】",
        "quote": "The underlying idea became that things are more beautiful for bearing imperfections.",
        "notes": "經 evidence_gate.quote_in_page 逐字驗收通過，支持侘寂美學與真實粗糙感光影。"
    },
    "K-018": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-019": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 403: Forbidden，ResearchGate 權限阻擋）。"
    },
    "K-020": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-021": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓取結果為圖片二進位檔（WEBP），查無正文文字。"
    },
    "K-022": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-023": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁為客戶端動態渲染頁面（僅有 Loading 字樣），查無正文。"
    },
    "K-024": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-025": {
        "status": "【對不上】",
        "quote": "What is Facebook, Really? - Article - Faculty & Research - Harvard Business School",
        "notes": "網頁抓取成功，但該編號對應之文章為哈佛商學院 John Deighton 關於臉書商業模式之論文《What is Facebook, Really?》，與營運透明度（Operational Transparency）或努力啟發式無關。"
    },
    "K-026": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-027": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-028": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-029": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 404: Not Found）。"
    },
    "K-030": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓不到（HTTP Error 403: Forbidden，ResearchGate 權限阻擋）。"
    },
    "K-031": {
        "status": "【未驗證】",
        "quote": "無",
        "notes": "網頁抓取成功，但內容為 Steve Blank 部落格彙整頁，查無關於「前置意圖探測（Pre-announcement）」之原文支持句。"
    }
}

rows = []
for s in sections:
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    header = lines[0]
    kid = re.search(r'K-\d+', header).group(0)
    
    # Title clean
    title_m = re.search(r'【K-\d+・(.*?)】', header)
    title = title_m.group(1) if title_m else header.replace('###', '').strip()
    
    m_url = re.search(r'https?://[^\s\)]+', s)
    url = m_url.group(0) if m_url else ''
    
    spec = specs[kid]
    status = spec["status"]
    quote = spec["quote"].replace('|', '&#124;').replace('\n', ' ')
    notes = spec["notes"].replace('|', '&#124;')
    
    # Test quote if verified
    if status == "【已驗證】":
        cache_f = cache_dir / f"{kid}.txt"
        page_t = cache_f.read_text(encoding='utf-8')
        ok, why = evidence_gate.quote_in_page(spec["quote"], page_t)
        if not ok:
            print(f"ERROR: {kid} quote verification failed: {why}")
            sys.exit(1)
            
    rows.append({
        "kid": kid,
        "title": title,
        "url": url,
        "status": status,
        "quote": quote,
        "notes": notes
    })

# Format markdown table
table_md = "# 📋 生活管家儲備知識庫（31 條 K）物理真值反查表\n\n"
table_md += "> **審查日期**：2026-11-24  \n"
table_md += "> **檢驗工具**：`evidence_gate.py`（Python 標準庫 urllib 物理抓取 + `quote_in_page` 逐字驗算）  \n"
table_md += "> **狀態定義**：  \n"
table_md += "> - **【已驗證】**：網頁抓取成功，且找到逐字原文完全支持該 K 假說（數字無出處者已標註備註）。  \n"
table_md += "> - **【對不上】**：網頁抓取成功，但網頁內容與該 K 假說論點無關或相互矛盾。  \n"
table_md += "> - **【未驗證】**：網頁無法抓取（404/403/reCAPTCHA/動態渲染），或網頁正文未包含足以支持假說之句子。  \n\n"

table_md += "| K 編號 | 標題 | 網址 | 狀態 | 原文摘句 | 備註 |\n"
table_md += "| :--- | :--- | :--- | :---: | :--- | :--- |\n"

for r in rows:
    table_md += f"| {r['kid']} | {r['title']} | [{r['url'][:35]}...]({r['url']}) | {r['status']} | {r['quote']} | {r['notes']} |\n"

out_table_path.write_text(table_md, encoding='utf-8')
print(f"Successfully generated {out_table_path}")

# Programmatic statistics directly from table content
v_count = sum(1 for r in rows if r['status'] == "【已驗證】")
c_count = sum(1 for r in rows if r['status'] == "【對不上】")
u_count = sum(1 for r in rows if r['status'] == "【未驗證】")
total = len(rows)

print("\n=== 統計執行結果 ===")
print(f"總計條目: {total}")
print(f"【已驗證】: {v_count} 條 ({v_count/total:.1%})")
print(f"【對不上】: {c_count} 條 ({c_count/total:.1%})")
print(f"【未驗證】: {u_count} 條 ({u_count/total:.1%})")
