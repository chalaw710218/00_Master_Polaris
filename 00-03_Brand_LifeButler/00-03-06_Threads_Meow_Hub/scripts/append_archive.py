import sys
from pathlib import Path

content_to_append = """
---
### ☀️ 自動巡邏發文：【週二大太陽逼貓睡午覺・木地板暖光充電】
* **發布時間**：2026-10-27 12:56
* **Post ID**：`18172108393424291`
* **公開網址**：[https://www.threads.com/@hellotaitung/post/De_DLZekyDD](https://www.threads.com/@hellotaitung/post/De_DLZekyDD)
* **審計**：發布前 100/100（threads-growth-auditor 評分）
* **附圖**：`04_Shadow_Kage_Operative/images/meow_tuesday_noon_sunnap.jpg`（已鎖定去重庫）
```text
誰能抗拒週二中午的這塊大太陽？
地板被曬得暖烘烘的，
簡直是上天派來逼貓睡午覺的陷阱。

闆仔剛吃完午餐，
桌上那杯冰紅烏龍的杯壁還在往下淌水珠。

本喵早就鎖定門口那塊長方形的光斑，
整隻貓攤平在木地板上，下巴貼著微溫的木頭，
舒服到連鬍鬚都在發光。

吃飽喝足的台東午後，
連風吹過來都是慵懶的味道。

大家今天中午都吃了什麼好料喵？
吃飽了記得稍微瞇一下眼睛充電唷 🍱☀️🐾
```
"""

with open("03_Published_Archive.md", "a", encoding="utf-8") as f:
    f.write(content_to_append)

print("Archive appended successfully.")
