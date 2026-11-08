import json

def read_step(file_path, target_indices):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
                idx = d.get('step_index')
                if idx in target_indices:
                    print(f"=== Step {idx} ===")
                    print("Role/Type:", d.get('type'))
                    print("Content:\n", d.get('content'))
            except Exception:
                pass

read_step('C:/Users/lenovo/.gemini/antigravity/brain/62615c83-54cd-4585-ac6a-95745b9ac34a/.system_generated/logs/transcript_full.jsonl', [8757, 8758, 8759, 8760, 8761, 8762])
