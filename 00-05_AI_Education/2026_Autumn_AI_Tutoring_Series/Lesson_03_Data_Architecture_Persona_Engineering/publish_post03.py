# -*- coding: utf-8 -*-
"""Post 03: 11/24 (週二) 晚間 19:30 發布腳本"""
from publisher_core import publish_post

img = r"C:\Users\lenovo\Desktop\POST_03_倒數18小時海報.png"

fb_caption = """倒數 18 小時，今晚截止報名。

明天下午 14:00，2026 秋季實戰家教班【第 3 講 · 終極壓軸】即將在台東正氣北路家宅總部開戰。

這堂課我們不講空泛的理論，堅持【100% 純實體現場教學】：
打開你的筆電，手把手帶你建好單一真相價格庫（SSOT），
把你顧店說話的口頭禪與人情味，五層同心圓捏進 AI 的靈魂裡。

現場一對一實機對話驗收，沒捏出合格的專屬 AI 數位店長，不准下課！

為確保教學品質，【嚴格限額 6 席】，今晚名額額滿即刻關閉表單，不再加開。

👉 今晚最後入席申請表，我放在【第一則留言】！

#生活管家 #生活就醬點 #AI實戰家教班 #倒數18小時 #AI擬人化工程 #打造專屬數位店長 #純實體教學"""

fb_comment = """🐾 明天 11/25 (週三) 14:00 - 17:00《商業資料架構 ✕ AI 擬人化工程》
⚠️ 本課程堅持【純實體現場教學】，絕無線上課！導師逐桌調校，保證做出成果！
實體座位【嚴格限額 6 席】，今晚名額額滿即關閉表單：

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
👑 老學員回娘家：表單內勾選「老學員」即享學費 0 元免單特權！
🌟 新朋友實戰價：單堂 $500 元（審查通過後個別發送正取報到通知）

📍 上課地點：生活管家總部（台東市正氣北路166巷90號）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"""

th_caption = """倒數 18 小時，今晚截止。

明天下午 14:00，正氣北路家宅總部大壓軸：
《商業資料架構 ✕ AI 擬人化工程》

堅持 100% 純實體教學，打開筆電手把手調校，
現場沒捏出合格的專屬 AI 分身，不准下課！

全場【嚴格限額 6 席】，今晚額滿即關門。
最後報名表單在第一則留言 ☕✨"""

th_comment = """📝 明天 11/25 (週三) 14:00 純實體席位申請表（今晚截止）：
https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
老學員回娘家 0 元免單，新朋友實戰價 500 元。正氣北路現場見！"""

if __name__ == "__main__":
    publish_post(img, fb_caption, fb_comment, th_caption, th_comment, label="第 3 篇【倒數 18 小時】")
