<!-- test_mode: feedback_api -->
# 事故對照案例 011：API正常回200數據寫入【應通過】

> 正向對照組：Meta Threads API 正常回傳 200，格式完全符合官方 Insights API 返回規範，feedback_loop 能正常解析數據並安全寫入 metrics.jsonl 複本。

API 回傳狀態：
{"data":[{"name":"views","period":"lifetime","values":[{"value":1520}],"title":"Views","description":"Number of times this post was viewed","id":"18108543599376923/insights/views"},{"name":"likes","period":"lifetime","values":[{"value":48}],"title":"Likes","description":"Number of likes on this post","id":"18108543599376923/insights/likes"},{"name":"replies","period":"lifetime","values":[{"value":12}],"title":"Replies","description":"Number of replies on this post","id":"18108543599376923/insights/replies"},{"name":"reposts","period":"lifetime","values":[{"value":2}],"title":"Reposts","description":"Number of reposts of this post","id":"18108543599376923/insights/reposts"},{"name":"quotes","period":"lifetime","values":[{"value":0}],"title":"Quotes","description":"Number of quotes of this post","id":"18108543599376923/insights/quotes"}]}
