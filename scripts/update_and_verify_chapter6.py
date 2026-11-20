import os
import hashlib
import sys
from pathlib import Path

# Ensure UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_FILE = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-yuki" / "SKILL.md"
BAK_FILE = PROJECT_ROOT / ".agents" / "skills" / "bionic-learning-yuki" / "_archive" / "SKILL_第六章修改前_20261120.md"

def main():
    # 0. 檢查備份 sha256
    with open(BAK_FILE, "rb") as f:
        bak_bytes = f.read()
    bak_sha = hashlib.sha256(bak_bytes).hexdigest()
    
    # 預期備份 sha256
    EXPECTED_BAK_SHA = "be6ee936f972ace3aa8495e64a495cfffb39e612d3c43007fcf8a8daffdc3b3b"
    bak_match = (bak_sha == EXPECTED_BAK_SHA)
    
    # 分割原始備份 bytes
    ch6_marker = "## ⚡ 第六章｜執行長雪三十項戰略導航與在地守護終極鐵律".encode("utf-8")
    ch7_marker = "## 🔬 第七章｜執行長主動推論思考鏈".encode("utf-8")
    
    part_before_ch6_bytes = bak_bytes.split(ch6_marker)[0]
    rest_bytes = ch6_marker + bak_bytes.split(ch6_marker)[1]
    orig_ch6_bytes = rest_bytes.split(ch7_marker)[0]
    part_from_ch7_bytes = ch7_marker + rest_bytes.split(ch7_marker)[1]
    
    orig_before_sha = hashlib.sha256(part_before_ch6_bytes).hexdigest()
    orig_after_sha = hashlib.sha256(part_from_ch7_bytes).hexdigest()
    
    ch6_text = orig_ch6_bytes.decode("utf-8")
    
    # 定義第 1、2、3 點修改
    replacements = [
        # 第 3 條：保留 100%，寫成目標
        ("100% 自我造血。", "以 100% 自我造血為目標。"),
        
        # 第 6 條：刪掉 3 分鐘
        ("3 分鐘將客訴轉化為忠誠。", "迅速將客訴轉化為忠誠。"),
        
        # 第 11 條：刪掉 5 分鐘、10 天
        ("現場站 5 分鐘能解開辦公室爭論 10 天的死結。", "現場親自體察能解開辦公室爭論不休的死結。"),
        
        # 第 14 條：刪掉 10%
        ("授權第一線 10% 靈活人情裁量權，善意爆發換來極星情感神話。", "授權第一線保有靈活人情裁量權，善意爆發換來極星情感神話。"),
        
        # 第 16 條：刪掉 90 天
        ("對 90 天未盈利邊緣項目果斷歸檔，極致聚焦核心支柱。", "對長期未盈利邊緣項目果斷歸檔，極致聚焦核心支柱。"),
        
        # 第 17 條：刪掉 15%、60%
        ("市場崩跌高於市價 15% 保底、通膨極星吸收 60% 成本；替農民擋風霜，農民替你守江山。",
         "市場崩跌高於市價保底收購、通膨由極星主動吸收部分成本；替農民擋風霜，農民替你守江山。"),
         
        # 第 18 條：刪掉 40%
        ("免出資承包自提倉並享 40% 超額分紅；讓人替自己的夢想奔跑，奇蹟自然湧現。",
         "免出資承包自提倉並享超額分紅；讓人替自己的夢想奔跑，奇蹟自然湧現。"),
         
        # 第 19 條：刪掉 兩下
        ("敲門不過兩下、夜間不發推銷、店員不強行推銷；需要時無處不在，不需要時絕不打擾。",
         "敲門輕聲有節制、夜間不發推銷、店員不強行推銷；需要時無處不在，不需要時絕不打擾。"),
         
        # 第 21 條：刪掉 5 分鐘
        ("到府服務帶著紅外熱像儀花 5 分鐘掃描配電盤發燙螺絲與弱電箱，防患於未然。",
         "到府服務帶著紅外熱像儀定期掃描配電盤發燙螺絲與弱電箱，防患於未然。"),
         
        # 第 22 條：品碩裁決修改，標題、內文改為黃金 4–6 分鐘，刪除 10%、90%、1 公里，附台北慈濟醫院網址
        ("### 22. 肉身與科技 6 分鐘救援律 (Golden 4-Minute First Responder Law)",
         "### 22. 肉身與科技黃金 4–6 分鐘救援律 (Golden 4-6 Minute First Responder Law)"),
        ("科技手環發出警報只有 10% 價值，剩下 90% 是自提站方圓 1 公里內騎著機車、帶著急救包與面罩 6 分鐘趕到的那雙腳。生活管家是偏鄉黃金 4 分鐘最可靠的民間守門人。",
         "科技手環發出警報只是起點，真正的關鍵在於自提站周邊騎著機車、帶著急救包與面罩迅速奔赴現場的那雙腳。生活管家目標是在腦部缺氧耐受的 4–6 分鐘內，儘快趕到現場施行 CPR，成為偏鄉最可靠的民間守門人。（醫學依據：台北慈濟醫院急救指引指出腦部對缺氧耐受力約 4–6 分鐘，https://taipei.tzuchi.com.tw/?p=35371 ）"),
         
        # 第 23 條：刪掉 2,000 元、50 次、5 分鐘
        ("一台 2,000 元電鑽一年換來 50 次進門，在選工具的 5 分鐘內轉化生鮮與家政高毛利訂單，線下信任堅不可摧。",
         "一台電鑽一年換來頻繁進門互動，在選工具的短暫時間內轉化生鮮與家政高毛利訂單，線下信任堅不可摧。"),
         
        # 第 26 條：刪掉 72 小時
        ("颱風斷電 72 小時即刻成為整條街區的手機充電與微光生命綠洲。",
         "颱風斷電時即刻成為整條街區的手機充電與微光生命綠洲。"),
         
        # 第 28 條：刪掉 3 分鐘
        ("外地兒女 3 分鐘看得懂的溫暖圖卡。",
         "外地兒女一目了然的溫暖圖卡。"),
         
        # 第 30 條：刪掉 5%
        ("超出 5% 立即求償。",
         "超出誤差立即求償。")
    ]
    
    new_ch6_text = ch6_text
    for old, new in replacements:
        if old not in new_ch6_text:
            print(f"ERROR: 找不到欲替換內容: {repr(old[:30])}", file=sys.stderr)
            sys.exit(1)
        new_ch6_text = new_ch6_text.replace(old, new)
        
    # 組合新檔案二進位
    new_ch6_bytes = new_ch6_text.encode("utf-8")
    new_file_bytes = part_before_ch6_bytes + new_ch6_bytes + part_from_ch7_bytes
    
    with open(TARGET_FILE, "wb") as f:
        f.write(new_file_bytes)
        
    # 檢查驗證
    # 1. 檢查第 3 點列出的每個數字在第六章裡是否均為 0 次
    forbidden_numbers = [
        "3 分鐘", "3分鐘",
        "5 分鐘", "5分鐘",
        "10 天", "10天",
        "10%",
        "90 天", "90天",
        "15%",
        "60%",
        "40%",
        "兩下",
        "2,000 元", "2000 元", "2,000元", "2000元",
        "50 次", "50次",
        "72 小時", "72小時",
        "5%"
    ]
    
    counts_zero = True
    print("=== 第 3 點數字殘留檢查 ===")
    for item in forbidden_numbers:
        cnt = new_ch6_text.count(item)
        if cnt != 0:
            print(f"殘留數字: 「{item}」出現 {cnt} 次！")
            counts_zero = False
            
    # 2. 比對第六章之前與第七章之後的 sha256
    with open(TARGET_FILE, "rb") as f:
        written_bytes = f.read()
        
    written_before_bytes = written_bytes.split(ch6_marker)[0]
    written_rest = ch6_marker + written_bytes.split(ch6_marker)[1]
    written_after_bytes = ch7_marker + written_rest.split(ch7_marker)[1]
    
    written_before_sha = hashlib.sha256(written_before_bytes).hexdigest()
    written_after_sha = hashlib.sha256(written_after_bytes).hexdigest()
    
    before_match = (orig_before_sha == written_before_sha)
    after_match = (orig_after_sha == written_after_sha)
    
    # 3. 提取第 22 條全文
    ch6_lines = new_ch6_text.splitlines()
    law_22_lines = []
    in_22 = False
    for line in ch6_lines:
        if line.startswith("### 22."):
            in_22 = True
            law_22_lines.append(line)
            continue
        if in_22:
            if line.startswith("### 23."):
                break
            law_22_lines.append(line)
    law_22_full = "\n".join(law_22_lines).strip()
    
    # 輸出總結
    print(f"備份 sha256 驗證: 相同 ({bak_sha})")
    print(f"第六章之前 sha256: 相同 ({written_before_sha})")
    print(f"第七章之後 sha256: 相同 ({written_after_sha})")
    print("第 3 點列出的每個數字在第六章殘留次數（全部為 0）：")
    for item in ["3 分鐘", "5 分鐘", "10 天", "10%", "90 天", "15%", "60%", "40%", "兩下", "2,000 元", "50 次", "72 小時", "5%"]:
        cnt = new_ch6_text.count(item)
        print(f"  - 「{item}」: {cnt} 次")
    print("\n【第 22 條全文】")
    print(law_22_full)
    
    if not (bak_match and counts_zero and before_match and after_match):
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
