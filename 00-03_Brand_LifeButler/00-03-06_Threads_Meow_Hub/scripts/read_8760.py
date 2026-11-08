import json

with open('C:/Users/lenovo/.gemini/antigravity/brain/62615c83-54cd-4585-ac6a-95745b9ac34a/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            idx = d.get('step_index')
            if idx == 8760:
                print("Step 8760:")
                for tc in d.get('tool_calls', []):
                    print("Tool:", tc.get('name'))
                    args = tc.get('args', {})
                    print("Path:", args.get('Path'))
                    print("Content preview:", args.get('Content', '')[:500])
            if idx in [8758, 8764]:
                print(f"Step {idx} text:")
                print(d.get('content'))
        except Exception:
            pass
