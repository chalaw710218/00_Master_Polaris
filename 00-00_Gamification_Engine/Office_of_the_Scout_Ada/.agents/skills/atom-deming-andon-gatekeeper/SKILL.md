---
name: atom-deming-andon-gatekeeper
description: 首席品質長戴明·全域安燈天網與90分致命紅線質檢原子 (Deming Andon Gatekeeper Protocol v1.0)。專門負責三大防區（防區A: 5D定價防彈衣、防區B: 社群選品賤詞過濾、防區C: 代碼日結平帳）之物理硬攔截與90分質量基準線驗收。凡觸犯致命紅線或總分低於90分者，一票否決並拉下黃黑安燈繩阻斷出廠。
role_key: deming
type: atomic_skill
parent_skill: bionic-learning-deming
version: v1.0
exit_code_verified: true
---

# 🚨 戴明全域安燈天網與90分致命紅線質檢原子 (Deming Andon Gatekeeper)

> 📐 **原子使命**：貫徹戴明「做進源頭律」與「安燈硬攔截律」。不靠事後檢驗挑殘次品，而在三大防區的源頭閘門布設不可逾越的黃黑安燈繩（Andon Cord）。凡綜合評分未達 90 分、或觸犯任何一項致命紅線者，物理拋出例外，一票否決阻斷出廠！

---

## 🏛️ 三大防區硬攔截矩陣 (Three Defense Bastions)

```
                            【戴明安燈繩硬攔截閘門】
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
    【防區 A: 5D 報價防彈衣】   【防區 B: 社群選品與品牌】   【防區 C: 代碼與日結平帳】
   - 勞務與代墊完全拆開        - 利刃底價先行 (Sharp)       - UTF-8 編碼防呆 (CP950)
   - 嚴格知情前置確認          - 高清現場打樣實拍           - Exit Code == 0 本機測試
   - 代墊上限 NT$ 3,000        - 100% 濾除促銷賤詞          - 日結平帳差 1 元不放行
   - 負毛利絕對阻斷            - 嚴禁「極星」代號洩漏       - 敏感金鑰 100% 解耦
```

### 1. 防區 A 致命紅線（財務與報價風控）
* `REDLINE_A1`: 勞務服務費與採購代墊款未做 100% 分離標示。
* `REDLINE_A2`: 未經創辦人或客戶明確「知情前置確認」，擅自承諾代墊。
* `REDLINE_A3`: 單筆代墊款超過 NT$ 3,000 且未收取足額定金。
* `REDLINE_A4`: 經精算後毛利率為負（負毛利出勤）。

### 2. 防區 B 致命紅線（社群選品與品牌防禦）
* `REDLINE_B1`: 外部對外文案洩漏內部代號「極星」或「Polaris」（違反全域品牌紅線）。
* `REDLINE_B2`: 出現低階促銷賤詞（如「團購」、「便宜」、「CP值爆表」、「破盤清倉」）。
* `REDLINE_B3`: 缺乏真實產地/商品現場打樣，使用虛假農場圖或未驗證圖。

### 3. 防區 C 致命紅線（工程代碼與日結平帳）
* `REDLINE_C1`: Python 代碼未經 Windows 本機實際執行，或 `Exit Code != 0`。
* `REDLINE_C2`: 檔案讀寫未指定 `utf-8` 編碼（造成 Windows CP950 亂碼崩潰）。
* `REDLINE_C3`: 每日營業日結帳本借貸不平（差額 $\ne 0$ 元）。
* `REDLINE_C4`: 程式碼或日誌明文硬編碼 API Key、Token 或私鑰。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行安燈閘門全維度審計
python scripts/andon_gatekeeper.py --zone A --payload '{"labor_fee": 1200, "advance_payment": 2500, "advance_confirmed": true, "gross_margin": 0.45}'

# 審計社群選品內容（自動攔截賤詞與品牌洩漏）
python scripts/andon_gatekeeper.py --zone B --payload '{"text": "生活管家到府為您挑選台東在地風土好物，純手工慢熬。", "has_sample_photo": true}'
```
