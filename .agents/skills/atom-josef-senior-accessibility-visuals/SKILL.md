---
name: atom-josef-senior-accessibility-visuals
description: 首席視覺長約瑟夫·高齡視力平權與人因光學視覺引導原子 (Josef Senior Accessibility & Ergonomic Visuals Protocol v1.0)。落實創辦人親授「約瑟夫主要負責視覺化的部分」法旨！專門解決偏鄉長輩與高齡族群 CSF 視力衰退之視覺傳達障礙：內文字級強制 >= 12pt、全面採用高清晰黑體並嚴禁白底淺灰字；騎樓 45 度視角字寬預拉伸 118%；實體海報/傳單下方嚴留 15% 拇指避讓盲區；以及 50 公分秒級掃碼 QR Code >= 28mm 視覺導引。
role_key: josef
type: atomic_skill
parent_skill: bionic-learning-josef
version: v1.0
exit_code_verified: true
---

# 👁️ 約瑟夫高齡視力平權與人因視覺引導原子 (Josef Senior Accessibility Visuals)

> 📐 **原子使命**：貫徹創辦人親授心法——**「約瑟夫主要負責視覺化的部分。」** 在台東高齡化常民生活圈，許多長輩有老花、白內障與對比敏感度下降（CSF 衰退）的生理現實。如果海報字小如蟻、白底配淺灰字、標題斜看變形，那就是對長輩的視覺歧視！本原子專門落實高齡視力平權與人因工程光學修正，確保每位長者與行人都能輕鬆無障礙地看清每一項服務！

---

## 🏛️ 高齡人因視覺四大防線 (Four Senior Accessibility Bastions)

```mermaid
flowchart TD
    VisualBrief["海報 / 傳單 / 門面看板視覺規格"] --> B1["1. 高齡 CSF 視力平權門禁\n• 內文字級強制 >= 12pt (標題 >= 36pt)\n• 嚴禁標楷體、細明體與白底淺灰字 (高對比度 >= 7:1)\n• 全面靠左對齊，嚴禁兩端分散對齊產生破洞"]
    
    VisualBrief --> B2["2. 騎樓街角 45 度透視預拉伸\n• 行人沿騎樓斜向接近時，視角被壓縮約 30%\n• 看板標題文字寬度預先水平拉伸 118% (對抗斜視壓縮)"]
    
    VisualBrief --> B3["3. 實體傳單 15% 拇指避讓盲區\n• 下方 15% 版面必須純留白或僅放裝飾花紋\n• 嚴禁放置重要電話、地址或行動呼籲，防止指腹遮蔽"]
    
    VisualBrief --> B4["4. 五十公分秒級行動 QR 碼導引\n• 實體印刷 QR Code 尺寸強制 >= 28mm\n• 四周預留 4 個模組 (Module) 的安全靜空區 (Quiet Zone)"]
    
    B1 & B2 & B3 & B4 --> Inspector["👁️ 高齡人因視覺安燈檢驗 (senior_accessibility_visuals.py)"]
```

---

## 🧭 視覺無障礙量化標準 (Metrics)

| 檢驗維度 | 青年通用標準 | **極星高齡長輩平權標準** | 違規處置 |
| :--- | :--- | :--- | :--- |
| **正文字級** | 9pt ~ 10pt | **$\ge 12\text{pt}$ (推薦 14pt~16pt)** | 強制放大重排 |
| **文字字體** | 任意無襯線/襯線 | **高辨識度粗黑體 / 嚴禁細明標楷** | 替換字族 |
| **顏色對比度** | 4.5 : 1 (WCAG AA) | **$\ge 7.0 : 1$ (WCAG AAA)** | 加深炭黑顏色 |
| **QR Code 尺寸** | 20mm | **$\ge 28\text{mm}$** | 強制放大標定 |
| **拇指避讓區** | 無 | **底部 15% 淨空無文字** | 上移行動區塊 |

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行海報視覺人因工程與高齡無障礙審查
python scripts/senior_accessibility_visuals.py --audit-visual '{"body_font_pt": 14, "font_family": "Noto Sans TC", "contrast_ratio": 8.5, "qr_code_size_mm": 30, "bottom_thumb_margin_pct": 16, "is_street_oblique": true}'
```
