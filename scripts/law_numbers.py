import csv
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Setup import path for evidence_gate
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
GATE_DIR = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

try:
    from evidence_gate import fetch_page_text, quote_in_page
except ImportError as e:
    print(f"無法載入 evidence_gate: {e}", file=sys.stderr)
    sys.exit(1)

SKILL_PATH = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-yuki" / "SKILL.md"
TARGET_CSV = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log" / "_law_numbers.csv"


def build_and_verify():
    # 讀取第六章
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        skill_text = f.read()

    ch6_marker = "## ⚡ 第六章｜執行長雪三十項戰略導航與在地守護終極鐵律"
    ch7_marker = "## 🔬 第七章｜執行長主動推論思考鏈"
    ch6_text = skill_text.split(ch6_marker)[1].split(ch7_marker)[0]

    # 定義所有數字項目的判定資料庫
    # 欄位：條號, 數字前後各10字, 類型, 狀態, 網址, 逐字摘句, 說明
    TZUCHI_URL = "https://taipei.tzuchi.com.tw/%E6%8A%8A%E6%8F%A1%E9%BB%83%E9%87%914%E5%88%86%E9%90%98-%E6%95%91%E5%9B%9E%E7%80%95%E6%AD%BB%E6%82%A3%E8%80%85/"
    TZUCHI_QUOTE = "腦部對缺氧的耐受力僅有4~6分鐘，這段時間即為黃金急救時間，超過之後便會造成不可逆的腦部損傷，輕者記憶力退化、反應遲鈍，重則變成植物人甚至腦死，缺氧時間越久，患者的存活率越低。」因此，理想狀態為4分鐘內進行心肺復甦術以維持腦功能"

    MOL_URL = "https://www.mol.gov.tw/1607/1632/1633/95651/"
    MOL_QUOTE = "更新日期:2026-07-20...《外送員權益保障及外送平臺管理法》（以下簡稱外送專法）將於今（ 115）年7月21日零時正式施行。"

    data = [
        ("1", "的低熵自組織狀態，讓九大天王在各自軌道發揮極", "內部規定", "待品碩確認", "", "", "極星內閣九大天王組織編制"),
        ("2", "捍衛極星最高生命線；三道防線過濾瑣碎雜訊，確", "內部規定", "待品碩確認", "", "", "創辦人時間防護罩三道過濾機制"),
        ("3", "與商業毛利自動撥備，100% 自我造血。", "內部規定", "待品碩確認", "", "", "社企商業造血目標比例"),
        ("5", "戰略耐心三階躍遷律 (Strat", "內部規定", "待品碩確認", "", "", "戰略推進三階段節奏"),
        ("5", " ➡️ 全縣神經網」三階推進，把每顆釘子釘深", "內部規定", "待品碩確認", "", "", "戰略推進三階段節奏"),
        ("6", "群情緒火花秒級反饋，3 分鐘將客訴轉化為忠", "內部規定", "待品碩確認", "", "", "特務影客訴處理內部響應時限"),
        ("7", "；以開源系統為底座，0 行政負擔把政府紅利", "內部規定", "待品碩確認", "", "", "內部系統零行政負擔目標"),
        ("11", "滅系統摩擦；現場站 5 分鐘能解開辦公室爭", "內部規定", "待品碩確認", "", "", "現場一線觀察方法比喻"),
        ("11", "鐘能解開辦公室爭論 10 天的死結。", "內部規定", "待品碩確認", "", "", "辦公室爭論時間比喻"),
        ("12", "eap Law) 以三級節點跳躍替代長途單騎", "內部規定", "待品碩確認", "", "", "物流配送三級跳躍架構"),
        ("14", "理底線，授權第一線 10% 靈活人情裁量權，善", "內部規定", "待品碩確認", "", "", "基層夥伴彈性人情裁量比例"),
        ("15", "十年憲章永續正道律 (D", "內部規定", "待品碩確認", "", "", "極星十年永續經營願景"),
        ("16", "葉消耗根系養分；對 90 天未盈利邊緣項目果", "內部規定", "待品碩確認", "", "", "邊緣業務停損考核天數"),
        ("17", " 市場崩跌高於市價 15% 保底、通膨極星吸收", "內部規定", "待品碩確認", "", "", "產地小農採購保底加價比例"),
        ("17", "保底、通膨極星吸收 60% 成本；替農民擋風霜", "內部規定", "待品碩確認", "", "", "極星自願吸收通膨成本比例"),
        ("18", "出資承包自提倉並享 40% 超額分紅；讓人替自", "內部規定", "待品碩確認", "", "", "自提倉合夥人超額分紅比例"),
        ("19", " Law) 敲門不過兩下、夜間不發推銷、店員", "內部規定", "待品碩確認", "", "", "生活管家服務禮儀敲門次數"),
        ("20", "水化萬物九王大統御律 (All-", "內部規定", "待品碩確認", "", "", "極星內閣九位首長統御架構"),
        ("21", "務帶著紅外熱像儀花 5 分鐘掃描配電盤發燙", "內部規定", "待品碩確認", "", "", "到府預防性檢測標準工時"),
        ("22", "肉身與科技 6 分鐘救援律 (Go", "外部事實", "抵觸", TZUCHI_URL, TZUCHI_QUOTE, "條文標題寫 6 分鐘救援律，同條英文寫 Golden 4-Minute、內文寫黃金 4 分鐘，與急救醫學黃金 4 分鐘標準抵觸"),
        ("22", "律 (Golden 4-Minute Fi", "外部事實", "已驗證", TZUCHI_URL, TZUCHI_QUOTE, "急救醫學標準：心跳停止4分鐘內進行CPR為黃金救援時間"),
        ("22", "技手環發出警報只有 10% 價值，剩下 90%", "內部規定", "待品碩確認", "", "", "科技警報與肉身守護價值對比權重"),
        ("22", "10% 價值，剩下 90% 是自提站方圓 1 ", "內部規定", "待品碩確認", "", "", "科技警報與肉身守護價值對比權重"),
        ("22", "0% 是自提站方圓 1 公里內騎著機車、帶", "內部規定", "待品碩確認", "", "", "自提站救援服務守護半徑"),
        ("22", "、帶著急救包與面罩 6 分鐘趕到的那雙腳。", "外部事實", "抵觸", TZUCHI_URL, TZUCHI_QUOTE, "條文內文寫 6 分鐘趕到，同條又稱黃金 4 分鐘民間守門人，前後抵觸"),
        ("22", "生活管家是偏鄉黃金 4 分鐘最可靠的民間守", "外部事實", "已驗證", TZUCHI_URL, TZUCHI_QUOTE, "急救醫學標準：心跳停止4分鐘內進行心肺復甦術以維持腦功能"),
        ("23", "客流實體觸點零成本槓桿律 (Tool", "內部規定", "待品碩確認", "", "", "共享工具接觸點獲客策略"),
        ("23", "點的終極槓桿。一台 2,000 元電鑽一年換來 5", "內部規定", "待品碩確認", "", "", "共享工具單元成本假設"),
        ("23", " 2,000 元電鑽一年換來 50 次進門，", "內部規定", "待品碩確認", "", "", "工具共享年度效益週期"),
        ("23", "0 元電鑽一年換來 50 次進門，在選工具的", "內部規定", "待品碩確認", "", "", "工具共享年度進門次數假設"),
        ("23", "次進門，在選工具的 5 分鐘內轉化生鮮與家", "內部規定", "待品碩確認", "", "", "顧客在店選工具之停留轉化時間"),
        ("24", "要修得清爽俐落；替 85 歲老農將一生採訪印", "內部規定", "待品碩確認", "", "", "高齡口述歷史服務情境範例年齡"),
        ("26", "收回成本，颱風斷電 72 小時即刻成為整條街", "內部規定", "待品碩確認", "", "", "自提站社區儲能備援設計時長"),
        ("28", "叮嚀轉化為外地兒女 3 分鐘看得懂的溫暖圖", "內部規定", "待品碩確認", "", "", "孝親聽診圖卡閱讀設計時間"),
        ("28", "故鄉父母，構築對手用十倍補貼都撬不走的孝親情", "內部規定", "待品碩確認", "", "", "情感護城河商業競爭比喻"),
        ("29", "g Law) 面對 2026 外送專法，堅決不以", "外部事實", "已驗證", MOL_URL, MOL_QUOTE, "勞動部公告外送專法於民國115年（2026年）施行"),
        ("29", "寶桑 3PL 承攬與開源點餐", "內部規定", "待品碩確認", "", "", "物流車隊定錨為第三方物流(3PL)"),
        ("29", "點餐法規零射程律 (3PL Subcont", "內部規定", "待品碩確認", "", "", "物流車隊定錨為第三方物流(3PL)"),
        ("29", "「傳統第三方物流 (3PL) 承攬車隊」，", "內部規定", "待品碩確認", "", "", "物流車隊定錨為第三方物流(3PL)"),
        ("30", "物理磅秤驗收，超出 5% 立即求償。財務審計", "內部規定", "待品碩確認", "", "", "生鮮進貨物理磅秤驗收容許誤差率"),
        ("30", "管家_系統化管理_V2》，死守單元經濟底線", "內部規定", "待品碩確認", "", "", "內部系統化管理文件版本號"),
    ]

    TARGET_CSV.parent.mkdir(parents=True, exist_ok=True)

    header = ["條號", "數字前後各10字", "類型", "狀態", "網址", "逐字摘句", "說明"]
    with open(TARGET_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

    print(f"已成功寫入 CSV: {TARGET_CSV}")
    print(f"總共抓取 {len(data)} 個數字項目。\n")

    # 執行 verification
    verified_count = 0
    mismatch_count = 0
    unverified_count = 0
    pending_count = 0
    failed_web_count = 0

    # 快取已抓取網頁
    page_cache = {}

    for idx, row in enumerate(data, 1):
        law_no, context, kind, status, url, quote, note = row

        if status == "待品碩確認":
            pending_count += 1
        elif status == "無出處":
            unverified_count += 1
        elif status in ("已驗證", "抵觸"):
            if not url or not quote:
                print(f"❌ [{idx}] 條號 {law_no} 狀態為 {status} 但缺少網址或摘句")
                failed_web_count += 1
                continue

            try:
                if url not in page_cache:
                    page_cache[url] = fetch_page_text(url, timeout=20)
                page_text = page_cache[url]

                ok, err_msg = quote_in_page(quote, page_text)
                if ok:
                    if status == "已驗證":
                        verified_count += 1
                    else:
                        mismatch_count += 1
                else:
                    print(f"❌ [{idx}] 條號 {law_no} 摘句不在網頁上: {err_msg}")
                    failed_web_count += 1
            except Exception as e:
                print(f"❌ [{idx}] 條號 {law_no} 網頁抓取失敗: {e}")
                failed_web_count += 1

    print("=== 統計結果 ===")
    print(f"總數字數: {len(data)}")
    print(f"已驗證: {verified_count}")
    print(f"無出處: {unverified_count}")
    print(f"抵觸: {mismatch_count}")
    print(f"待品碩確認: {pending_count}")

    if failed_web_count > 0:
        print(f"網頁驗證失敗: {failed_web_count}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    build_and_verify()
