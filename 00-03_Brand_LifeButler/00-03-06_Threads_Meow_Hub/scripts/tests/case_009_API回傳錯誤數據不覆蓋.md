<!-- test_mode: data_integrity -->
# 事故案例 009：API回傳錯誤數據不覆蓋【應退回】

預期原因：API回傳錯誤中斷，保留歷史數據不覆蓋

> 真實事故還原：Meta Threads API 發生 token 異常回傳空值，歷史 metrics 被覆蓋歸零。

API 回傳狀態：
{"status": "error", "error_code": 190, "message": "Invalid OAuth access token."}
