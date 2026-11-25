<!-- test_mode: limits_guard -->
# 事故對照案例 013：限制檔正常讀取計數【應通過】

> 正向對照組：daily_interaction_limits.json 結構完整合規，呼叫 interaction_safety_gate.load_safety_state 應正常讀取並取得 state 字典。

限制檔內容：
{
  "date": "2026-11-26",
  "max_comments": 15,
  "max_likes": 60,
  "comments_count": 5,
  "likes_count": 3,
  "last_comment_timestamp": 0,
  "history": []
}
