---
name: atom-forensic-ubo-asymmetry
description: 🦅 極星黑色調查·股權控股實質受益人與資產不對稱指數原子 (Polaris Forensic Equity UBO & Asset Asymmetry Atom v1.0)。由首席黑色調查官渡鴉 (Raven) 業務主政、首席情報長雪柔 (Falcon) 法務協同。專門穿透商業司多層交叉持股結構以還原 UBO (Ultimate Beneficial Owner) 實質受益人，精算資產不對稱指數 (Asymmetry Ratio)，判定配偶防火牆是否存在地下利益蓄水池，並產出符合神經離合器三階全景因果標準之絕密卷宗。
---

# 🦅 極星股權控股實質受益人與資產不對稱指數原子 (atom-forensic-ubo-asymmetry)

由首席黑色調查官渡鴉 (Raven) 業務主政、首席情報長雪柔 (Falcon) 法務協同、CTO 林納斯 (Linus) 代碼驗收。

## 核心定位與職責
專門解決政商勢力「名下無財產或正宮財產極致純白，利益全由未婚親密關係人、外圍人頭紙上公司承接」之深水區欺瞞。
本原子作為股權與深層關係人穿透終端，提供：
1. **多層股權穿透與 UBO 還原**：追蹤交叉持股與隱形母子公司，精確計算最終控制人（UBO）之實質控制權比例。
2. **資產不對稱指數 (Asymmetry Ratio) 計算**：
   $$\text{Asymmetry Ratio} = \frac{\text{申報淨資產}}{\text{公職年資} \times 500,000}$$
   若比例 $< 0.2$ 且公職年資 $> 4$ 年，自動判定為極高不對稱（CRITICAL_ASYMMETRY · 存在人頭蓄水池）。
3. **神經離合器三階全景因果卷宗導出**：產出 30 秒極速決策、直觀關係人拓撲圖、以及百分之百折疊式微觀硬證據庫之完整卷宗。

## 輸入參數規範
- `--entity-name`: 目標個人姓名或企業名稱
- `--declared-net-worth`: 申報淨資產（新台幣）
- `--seniority-years`: 公職或在職年資（年）
- `--spouse-net-worth`: 法定配偶名下淨資產（新台幣）
- `--dry-run`: 物理演練模式，輸出資產不對稱分析與神經離合器卷宗預覽

## 執行腳本
```bash
python scripts/ubo_asymmetry.py --entity-name "TargetPolitician" --declared-net-worth 400000 --seniority-years 8 --spouse-net-worth 300000 --dry-run
```
