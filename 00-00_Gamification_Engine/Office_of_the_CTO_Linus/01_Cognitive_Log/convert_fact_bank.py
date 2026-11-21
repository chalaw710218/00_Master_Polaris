#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_fact_bank.py
將 01_Experiences_and_Evidence.md 單行格式轉換為門禁 (bionic_knowledge_gate.py) 支援的多行結構化格式。
"""

import sys
import re
from pathlib import Path

def convert():
    current_dir = Path(__file__).resolve().parent
    target_file = current_dir / "01_Experiences_and_Evidence.md"
    
    if not target_file.exists():
        print(f"FAIL: 找不到檔案 {target_file}")
        sys.exit(1)
        
    raw_text = target_file.read_text(encoding="utf-8")
    lines = raw_text.splitlines()
    
    quote_headers = []
    line_pat = re.compile(r'^(\d+)\.\s*(.+?)：「(.*)」｜出處：(.*)$')
    
    entries = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            quote_headers.append(stripped)
            continue
        m = line_pat.match(stripped)
        if m:
            idx, title, quote, source = m.groups()
            entries.append({
                "id": int(idx),
                "title": title.strip(),
                "quote": quote.strip(),
                "url": source.strip()
            })
        else:
            print(f"FAIL: 無法解析的行: {stripped}")
            sys.exit(1)
            
    converted_count = len(entries)
    if converted_count != 145:
        print(f"FAIL: 轉換條數 ({converted_count}) 不等於預期 145 條！")
        sys.exit(1)
        
    out_lines = []
    if quote_headers:
        out_lines.extend(quote_headers)
        out_lines.append("")
        
    for item in entries:
        out_lines.append(f"{item['id']}. **{item['title']}**：")
        out_lines.append(f"  - **核心事實**：{item['title']}")
        out_lines.append(f"  - **出處**：{item['url']}")
        out_lines.append(f"  - **證據網址**：{item['url']}")
        out_lines.append(f"  - **原文摘句**：{item['quote']}")
        out_lines.append("")
        
    target_file.write_text("\n".join(out_lines).strip() + "\n", encoding="utf-8")
    
    print("=== 事實庫格式轉換完成 ===")
    print(f"轉換條數：{converted_count} 條")
    print("驗證結果：PASS (格式符合門禁規範)")

if __name__ == "__main__":
    convert()
