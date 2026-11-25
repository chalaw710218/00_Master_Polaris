<!-- test_mode: limits_guard -->
# 事故案例 012：限制檔讀取失敗不覆蓋【應退回】

預期原因：安全門禁讀檔失敗

> 真實事故還原：daily_interaction_limits.json 讀取損毀 JSON 時，呼叫 interaction_safety_gate.load_safety_state 必須硬性停止並拋出例外，且檔案 SHA-256 在執行前後必須完全相同，嚴禁覆蓋或重置原檔以保護歷史記錄。

限制檔內容：
{"date": "2026-11-25", "corrupted_json_content": invalid_json_syntax...
