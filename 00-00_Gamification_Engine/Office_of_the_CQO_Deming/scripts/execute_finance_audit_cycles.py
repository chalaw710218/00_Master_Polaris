import sys
from pathlib import Path

# 加入腳本路徑
script_dir = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CQO_Deming\scripts")
sys.path.insert(0, str(script_dir))

from bionic_knowledge_gate import add_entry, check_file_whitelist, DEFAULT_EXPERIENCES_PATH

items = [
    {
        'title': '班佛定律與首位數字舞弊鑑識 (Benford\'s Law)',
        'url': 'https://en.wikipedia.org/wiki/Benford%27s_law',
        'quote': 'the leading digit is likely to be small',
        'fact': '班佛定律（首位數字定律）指出在自然產生的數值數據集中，首位數字為 1 的機率約為 30.1%，數字越大概率遞減；審計人員常以此統計規律檢驗財務數字是否經過人為編造或捏造。',
        'source': 'https://en.wikipedia.org/wiki/Benford%27s_law'
    },
    {
        'title': '會計對帳與跨帳戶一致性校驗 (Accounting Reconciliation)',
        'url': 'https://en.wikipedia.org/wiki/Reconciliation_(accounting)',
        'quote': 'process of ensuring that two sets of records',
        'fact': '會計對帳（Reconciliation）為確保兩套獨立紀錄（例如企業銀行存款日記帳與銀行對帳單）之帳面餘額相互一致的核對程序，用以查明跨期未達帳與記帳錯誤。',
        'source': 'https://en.wikipedia.org/wiki/Reconciliation_(accounting)'
    },
    {
        'title': '複式簿記與借貸平衡原則 (Double-entry Bookkeeping)',
        'url': 'https://en.wikipedia.org/wiki/Double-entry_bookkeeping',
        'quote': 'recorded with equal and opposite entries',
        'fact': '複式簿記為每筆交易均以相等且相反的借方（Debits）與貸方（Credits）分錄同時記錄之記帳方法，確保會計恆等式（資產 = 負債 + 業主權益）恆常平衡。',
        'source': 'https://en.wikipedia.org/wiki/Double-entry_bookkeeping'
    },
    {
        'title': '試算表借貸相等性驗算 (Trial Balance)',
        'url': 'https://en.wikipedia.org/wiki/Trial_balance',
        'quote': 'lists the adjusted closing balances of all the general ledger accounts',
        'fact': '試算表（Trial Balance）為內部財務編制表，彙總列出總分類帳中所有借方與貸方帳戶之期末餘額，透過「借方總額 = 貸方總額」之數學一致性檢驗數學加總與過帳差錯。',
        'source': 'https://en.wikipedia.org/wiki/Trial_balance'
    },
    {
        'title': '現金流量表三大活動現金流分解 (Cash Flow Statement)',
        'url': 'https://en.wikipedia.org/wiki/Cash_flow_statement',
        'quote': 'how changes in balance sheet accounts and income affect cash',
        'fact': '現金流量表展示資產負債表科目變動與損益表利潤如何影響現金及約當現金，將現金流嚴格劃分為營業活動、投資活動與籌資活動三大板塊進行動態勾稽。',
        'source': 'https://en.wikipedia.org/wiki/Cash_flow_statement'
    },
    {
        'title': '資產負債表財務狀況摘要 (Balance Sheet)',
        'url': 'https://en.wikipedia.org/wiki/Balance_sheet',
        'quote': 'summary of the financial balances of an individual or organization',
        'fact': '資產負債表（財務狀況表）為企業在特定時點之財務餘額靜態摘要，揭示企業所擁有的經濟資源（資產）、承擔的債務義務（負債）與所有者淨權益。',
        'source': 'https://en.wikipedia.org/wiki/Balance_sheet'
    },
    {
        'title': '損益表營收費用與淨利潤轉結 (Income Statement)',
        'url': 'https://en.wikipedia.org/wiki/Income_statement',
        'quote': 'shows the company\'s revenues and expenses during a particular period',
        'fact': '損益表（利潤表）反映企業在特定會計期間之收入與各項費用成本，其最終結算之淨利潤（Net Income）直接轉結至資產負債表之保留盈餘與現金流量表營業活動起點。',
        'source': 'https://en.wikipedia.org/wiki/Income_statement'
    },
    {
        'title': '財務報表結構與三表跨表勾稽 (Financial Statements)',
        'url': 'https://en.wikipedia.org/wiki/Financial_statement',
        'quote': 'formal records of the financial activities and position',
        'fact': '財務報表為實體財務活動與財務狀況之正式紀錄，資產負債表、損益表與現金流量表三者透過保留盈餘與期末現金餘額形成閉環數學勾稽，單表造假必然導致跨表失衡。',
        'source': 'https://en.wikipedia.org/wiki/Financial_statement'
    },
    {
        'title': '鑑識會計與財務舞弊調查 (Forensic Accounting)',
        'url': 'https://en.wikipedia.org/wiki/Forensic_accounting',
        'quote': 'specialty practice area of accounting that investigates',
        'fact': '鑑識會計（Forensic Accounting）為結合會計學、審計學與調查技術之專業領域，專門調查企業是否存在財務報告舞弊、虛假交易或數字編造，產出可用於法律訴訟之實質證據。',
        'source': 'https://en.wikipedia.org/wiki/Forensic_accounting'
    },
    {
        'title': '內部控制流程與目標保障 (Internal Control)',
        'url': 'https://en.wikipedia.org/wiki/Internal_control',
        'quote': 'process for assuring of an organization\'s objectives in operational effectiveness',
        'fact': '內部控制為組織確保營運效能與效率、財務報告可靠性及法規合規性的系統性流程防禦機制，透過職能分離與授權審批防止未授權操作與虛報平帳。',
        'source': 'https://en.wikipedia.org/wiki/Internal_control'
    }
]

print("=== 開始執行數字查核與三表勾稽 10 輪仿生學習入庫 (條目 21 ~ 30) ===\n")

for idx, it in enumerate(items, 21):
    print(f"--- [輪次 {idx}] 正在入庫：{it['title']} ---")
    add_entry(
        title=it['title'],
        fact=it['fact'],
        source=it['source'],
        url=it['url'],
        quote=it['quote'],
        filepath=DEFAULT_EXPERIENCES_PATH
    )

print("\n=== 10 輪入庫完成，開始執行結束後白名單 check ===\n")
check_file_whitelist(DEFAULT_EXPERIENCES_PATH)
