<!-- test_mode: feedback_api -->
# 事故案例 010：API回傳錯誤數據不覆蓋【應退回】

預期原因：Threads Insights API 失敗 (HTTP 400)

> 真實事故還原：Meta Threads API 發生 Token 過期異常回傳 code 190（HTTP 400），呼叫 feedback_loop 抓數據時應立即拋出例外並停止，且 metrics.jsonl 複本的 SHA-256 在執行前後必須完全相同，嚴禁覆蓋既有數據。

API 回傳狀態：
{"error":{"message":"Error validating access token: Session has expired on Sunday, 22-Nov-26 09:00:00 PST. The current time is Sunday, 22-Nov-26 15:39:32 PST.","code":190,"type":"OAuthException","error_subcode":0,"fbtrace_id":"AFEP1N6of0CaqkErEp2du9V"}}
