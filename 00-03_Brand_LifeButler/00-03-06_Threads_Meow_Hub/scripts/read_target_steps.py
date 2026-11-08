import json

transcript_path = 'C:/Users/lenovo/.gemini/antigravity/brain/62615c83-54cd-4585-ac6a-95745b9ac34a/.system_generated/logs/transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            idx = d.get('step_index')
            if 8755 <= idx <= 8765:
                print(f"=== Step {idx} ({d.get('type')}) ===")
                content = d.get('content', '')
                if content:
                    print(content[:1500])
                    if len(content) > 1500:
                        print("...[truncated]...")
        except Exception as e:
            pass
