#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/product_trio_scaffolder.py
三合一商品化交付套版自動裝配引擎
自動生成 01_SOP_標準作業流程.md、02_產品規格與定價手冊.md、03_行銷文案與地推銷售話術.md
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

TEMPLATE_SOP = """# 📋 {service_name} · 01_SOP 標準作業流程

> **主政單位**：生活管家 營運部  
> **版本**：v1.0 (戴明品質安燈版)  
> **核心使命**：消滅繁瑣雜事，確保每一次到府與交付零差錯、零客訴、活得從容。

---

## 一、出發前準備清單 (Pre-Flight Checklist)
- [ ] 委託人與收件人姓名、聯絡電話、送達地址已核對確認
- [ ] 委託項目之規格、代購明細、特殊需求（如低溫、禁忌）已白紙黑字建檔
- [ ] 查理·蒙格代墊款風控查核：貨款若超過 NT$ 2,000 元已收取全額預付款
- [ ] 裝備齊全：生活管家保溫保鮮袋、專用紙袋、備用零錢、手機電量 > 80%

---

## 二、標準履約五步法 (Standard Delivery Protocol)
1. **【出發啟程】**：出發前透過 LINE 傳送預計抵達時間給收件人。
2. **【現場取件/採買】**：依循商品選品標準檢視品質，取得實體發票或收據拍照回傳。
3. **【專車保鮮配送】**：遵循平穩騎乘/駕駛原則，避免急煞與顛簸造成物品受損。
4. **【到府溫暖交付】**：抵達按門鈴/電話聯繫，親手遞交長輩或委託人，表達生活管家關心。
5. **【現場結清與回報】**：憑發票結清代買款項與服務費，於系統標記完工歸檔。

---

## 三、現場排錯與例外狀況處置 (Troubleshooting)
- **狀況 A：現場電話無人接聽**
  - 嚴格啟動【現場等候 5 分鐘上限律】：積極電話撥打 2 次，等候滿 5 分鐘後啟動二次出勤保護。
  - 將物品妥善收回保管，發送標準溫柔通知，後續安排二次配送並收取 NT$ 100~150 元二次出勤費。
- **狀況 B：採購店家缺貨**
  - 第一時間致電委託人提供 2 種同級替代方案，未獲授權絕不擅自作主替換。
- **狀況 C：物品意外破損**
  - 誠實面對，拍照留證，依據責任限額全額理賠或重採買，絕不推卸。
"""

TEMPLATE_SPEC = """# 💰 {service_name} · 02_產品規格與定價手冊

> **主政單位**：生活管家 財務部 (算盤)  
> **版本**：v1.0 (5D 價值矩陣版)  
> **核心使命**：明碼標價、保障雙方、杜絕做白工與情緒勒索。

---

## 一、服務範圍與邊界 (Service Boundaries)
### ✅ 我們包含的服務：
- 台東在地專人專車到府履約與長輩安心照護
- 專業代購、全程低溫保鮮裝箱與專案追蹤
- 實報實銷發票收據全透明對帳

### ❌ 我們堅決不承接的項目：
- 違法禁運物品、醫療侵入性行為、任何涉及法律風險之請託
- 未經雙方書面確認之大額無抵押代墊 (超過 NT$ 2,000 元強制預付)

---

## 二、5D 矩陣明碼定價手冊 (Pricing Schedule)
| 服務模態 | 基礎基數 | 5D 連乘乘數 | 建議收費標價 | 備註說明 |
| :--- | :--- | :---: | :---: | :--- |
| **市區標準出勤 (30-45m)** | 0.75 小時 | 1.8x ~ 2.2x | **NT$ 250 ~ 350** | 起步保底價 NT$ 200 |
| **跨區深旅行程 (60-90m)** | 1.50 小時 | 2.0x ~ 2.5x | **NT$ 500 ~ 750** | 包含偏遠鄉鎮交通補貼 |
| **二次出勤配送** | 現場等候超時 | - | **NT$ 100 ~ 150** | 補貼二次油資與工時 |

> 📌 **【代墊款解耦鐵律】**：代買之食材、商品、藥品費用憑店家收據「實報實銷」，款項與管家勞務費分立計算。

---

## 三、門市取貨與家宅地理座標
- **門市地址**：台東市正氣北路166巷90號
- **服務熱線**：089-123456
- **老夥伴免單與審查繳費政策**：長期合作在地友店享有專屬合作折扣或審查後按月匯款制。
"""

TEMPLATE_MARKETING = """# 📣 {service_name} · 03_行銷文案與地推銷售話術

> **主政單位**：生活管家 行銷部 (泰勒絲 ✕ 影)  
> **品牌法定全稱**：生活的一部分，就醬點！  
> **日常業務自稱**：生活管家  
> **版本**：v1.0 (雙軌轉換版)

---

## 一、📘 泰勒絲 (Taylor) Facebook 溫暖長文故事版
（核心：0.8 秒穿透率、留白呼吸感、常民共鳴、嚴格零外部外連避免降權）

```text
生活在台東，有些瑣事看似微小，卻總讓人抽不開身。

長輩習慣吃的那間老店魚湯、突然需要去藥局代領的日常備品，
或是人在外地工作，心裡始終掛念著家裡老人家今天有沒有好好吃飯。

生活管家想幫大家做的，其實不只是跑腿送東西，
而是幫你把那些奔波的時間省下來，好好陪家人喝杯茶、看本書。

專人專車、全程保溫保鮮，親手將這份安心送到家門口。
生活原本就該更從容一些。

👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！
```

### 💬 Facebook 第一則留言 (First Comment 置頂導流)
```text
👉 點擊加入生活管家專屬 LINE 官方帳號（可直接對話預約）：
https://lin.ee/z83YSq6

📍【門市取貨與服務諮詢】
• 地址：台東市正氣北路166巷90號
• 服務區域：台東市區、知本、南王、都蘭、東河專人配送
生活的一部分，就醬點！ 溫暖守護您的每一天
```

---

## 二、📱 影 (Kage) Threads 扎心短文隨筆版
（核心：真實照片、自嘲工作心酸、反 AI 塑料感、單一 Topic Tag）

```text
跑外送跑久了，最怕的其實不是下雨天，
而是按了門鈴，看見阿公慢慢走出來開門時，那種「終於有人來陪我說句話」的眼神。

現代人大家都在忙著賺錢、忙著生活，
有時候一碗熱湯送到長輩手上，幫忙看一眼瓦斯有沒有關好，
那個幾百塊的服務費，買回來的其實是整個晚上的踏實。

生活管家今天也在正氣北路上奔馳著。

生活的一部分，就醬點！
```

---

## 三、🤝 生活管家 面對面高情商地推話術 (Elevator Pitch)
- **遇見鄰里長輩時**：「阿姨您好！我是就醬點的生活管家～平常如果買重物、下雨天不想出門，打通電話給我們，管家幫您專程買好送到客廳，讓您在家吹電扇看電視就好！」
- **遇見在地店家時**：「老闆好！我們是正氣北路的生活管家，專門幫忙在地店家做台東專人外送與客製取貨，讓您專心在廚房出餐，外面的風吹日曬交給我們管家來扛！」
"""

def scaffold_product_trio(target_dir: str, service_name: str, dry_run: bool = False) -> Dict[str, Any]:
    """執行三合一商品化交付套版裝配"""
    dir_path = Path(target_dir)

    sop_content = TEMPLATE_SOP.format(service_name=service_name)
    spec_content = TEMPLATE_SPEC.format(service_name=service_name)
    mkt_content = TEMPLATE_MARKETING.format(service_name=service_name)

    files_to_create = {
        "01_SOP_標準作業流程.md": sop_content,
        "02_產品規格與定價手冊.md": spec_content,
        "03_行銷文案與地推銷售話術.md": mkt_content
    }

    if not dry_run:
        dir_path.mkdir(parents=True, exist_ok=True)
        for filename, content in files_to_create.items():
            fpath = dir_path / filename
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

    return {
        "status": "DRY_RUN_SUCCESS" if dry_run else "SUCCESS",
        "target_dir": str(dir_path),
        "service_name": service_name,
        "created_files": list(files_to_create.keys()),
        "file_count": len(files_to_create)
    }

def main():
    parser = argparse.ArgumentParser(description="三合一商品化交付套版自動裝配引擎")
    parser.add_argument("--target-dir", type=str, default="00-02_Products_Scaffold/00-02-99_SampleService", help="目標資料夾路徑")
    parser.add_argument("--service-name", type=str, default="台東在地慢活居安管家", help="服務或業務名稱")
    parser.add_argument("--dry-run", action="store_true", help="執行檔案裝配模擬")
    args = parser.parse_args()

    res = scaffold_product_trio(args.target_dir, args.service_name, args.dry_run)

    print("==================================================")
    print(f"📦 三合一商品化交付套版裝配完成 (Exit Code: 0) - [{res['status']}]")
    print(f"目標模組資料夾: {res['target_dir']}")
    print(f"服務名稱定錨: {res['service_name']}")
    print("--------------------------------------------------")
    print(f"已裝配標準交付文檔 (共 {res['file_count']} 份):")
    for f in res["created_files"]:
        print(f"  [✓] {f}")
    print("--------------------------------------------------")
    print("✨ 結構保證: 內建排錯檢核清單 ✕ 5D明碼標價 ✕ 蒙格代墊風控 ✕ FB/Threads雙軌文案 ✕ 第一留言閉環")
    print("==================================================")

if __name__ == "__main__":
    main()
