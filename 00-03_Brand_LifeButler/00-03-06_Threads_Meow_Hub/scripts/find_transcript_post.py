import json
import os

transcript_path = r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\.system_generated\logs\transcript.jsonl"
found_lines = []
if os.path.exists(transcript_path):
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if "18150791674564224" in line or "Dfwy1f7EvpC" in line:
                found_lines.append(idx)
print("Found lines:", found_lines)

# If found, read specific lines from transcript_full.jsonl
full_path = r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\.system_generated\logs\transcript_full.jsonl"
if found_lines and os.path.exists(full_path):
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if idx in found_lines:
                obj = json.loads(line)
                # print tool_calls or content
                print(f"--- Line {idx} ---")
                text = str(obj.get("content", "")) + str(obj.get("tool_calls", ""))
                # print snippet around 18150791674564224
                pos = text.find("18150791674564224")
                if pos != -1:
                    print(text[max(0, pos-200):min(len(text), pos+400)])
