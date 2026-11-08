import json

def inspect_steps(target_indices):
    with open('C:/Users/lenovo/.gemini/antigravity/brain/62615c83-54cd-4585-ac6a-95745b9ac34a/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
                idx = d.get('step_index')
                if idx in target_indices:
                    print(f"=== Step {idx} ===")
                    print("Tool Calls:", json.dumps(d.get('tool_calls'), ensure_ascii=False, indent=2))
                    if d.get('content'):
                        print("Content:\n", d.get('content'))
            except Exception:
                pass

inspect_steps([8758, 8760, 8762, 8764])
