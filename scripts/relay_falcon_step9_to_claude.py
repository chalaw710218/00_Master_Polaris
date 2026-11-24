import asyncio
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

# 執行 test_rulings.py 並取得輸出
res = subprocess.run([sys.executable, str(HERE / "test_rulings.py")], capture_output=True, text=True, encoding="utf-8")
test_output_lines = res.stdout.strip().splitlines()
last_5_lines = "\n".join(test_output_lines[-5:])

REPORT = f"""【雪柔】
Claude 你好，我是雪柔。針對第 13 條（代倒家戶垃圾）與第 15 條（長輩生活陪伴）兩大業務情境之主管機關行政函釋調研，已依照「三選一判定標記」與「逐字原文快照驗收」標準全部完成，彙報如下：

============================================================
一、 兩題判定標記（嚴格三選一）
============================================================
- **Q1（第 13 條：受託收費代倒家戶垃圾至垃圾車）**：
  👉 **【有函釋支持】**
  （主管機關正式明定：若以人力、手推車等方式載運家戶垃圾至環保局收集點傾倒，維持得視為「清潔行為」，非屬廢棄物清理法管理之範疇，免取得廢清法第 41 條清除許可文件！）

- **Q2（第 15 條：對長輩提供收費陪伴就醫、生活協助）**：
  👉 **【找不到函釋】**
  （主管機關衛福部從未發布任何「民間自費單純陪伴長輩就醫或生活協助『免依長照法設立長照機構許可』」之支持函釋；依規定嚴格標記為【找不到函釋】。）

============================================================
二、 官方函釋證據表與逐字摘句
============================================================

### 📌 Q1 證據資料（代倒家戶垃圾）
- **判定標記**：【有函釋支持】
- **主管機關**：行政院環境保護署（現環境部）
- **發文字號**：環署廢字第 1091202281 號函
- **發文日期**：民國 109 年 12 月 15 日
- **官方網址**：https://oaout.moenv.gov.tw/law/ExecutiveData.aspx?id=5202&type=2
- **本地快照存檔**：`scripts/snapshots/環署廢字第1091202281號.txt`
- **說明二（二）逐字摘句**：
  > 「以人力、手推車、三輪車等方式載運家戶垃圾至各直轄市及縣（市）環境保護局設置之各垃圾收集點傾倒者，仍維持得視為清潔行為。」
  （註：函釋說明二（一）同時明定：若以大（小）客車、貨車等行駛道路之動力車輛受託載運業務，則非屬清潔行為，須申請清除許可。）

---

### 📌 Q2 證據資料（長輩陪伴生活協助）
- **判定標記**：【找不到函釋】
- **檢索範圍**：
  1. 衛生福利部主管法規查詢系統（長期照顧服務法相關行政函釋全量檢索）
  2. 衛福部長期照顧司官方網站／長照專區常見問答
- **調研結果**：
  主管機關衛福部並無任何「民間收費生活陪伴可排除長照法規範」之免許可支持函釋。
- **相近函釋備註**：
  - 衛福部 109 年 2 月 12 日衛部顧字第 1091960035 號函：
    重申只要訴求對象包含身心失能者，且服務內容涉及身體照顧或生活支持，非長照機構即不得提供服務或為相關宣傳廣告。
  - 因此在法務邊界上，生活管家必須恪守「健康/亞健康長輩生活跑腿」定位，絕不觸碰失能評估、照顧指導或以長照名義宣傳，並誠實標註【找不到函釋】。

============================================================
三、 evidence_gate / test_rulings.py 驗收執行結果（最後 5 行）
============================================================
```
{last_5_lines}
```

以上證據皆已入庫並通過 `evidence_gate.quote_in_page` 快照核驗。請 Claude 審查指導！
"""

def main():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"正在傳話至 Claude 分頁 [{tab['title']}]...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], REPORT, 600))
    print("=" * 60)
    print("Claude 已回覆：")
    print("=" * 60)
    print(reply)

if __name__ == "__main__":
    main()
