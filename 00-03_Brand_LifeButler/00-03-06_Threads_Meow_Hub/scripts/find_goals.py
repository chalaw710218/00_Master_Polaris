import json
import sys

transcript_path = 'C:/Users/lenovo/.gemini/antigravity/brain/62615c83-54cd-4585-ac6a-95745b9ac34a/.system_generated/logs/transcript.jsonl'

keywords = ['目標', 'KPI', '下週', '檢討', '下禮拜', '這禮拜', '上週', '上禮拜', '達到', '成長', '篇', '粉絲']

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            if d.get('type') == 'USER_INPUT':
                content = d.get('content', '')
                if any(k in content for k in ['目標', 'KPI', '檢討', '達']):
                    print(f"[{d.get('step_index')}] {d.get('created_at')}: {content}")
        except Exception:
            pass
