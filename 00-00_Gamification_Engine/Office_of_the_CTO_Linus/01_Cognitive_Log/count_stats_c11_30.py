#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

def count_marks():
    target = Path(__file__).resolve().parent / "反查表_C11-30.md"
    content = target.read_text(encoding="utf-8")
    
    # 統計四種標記
    stats = {
        "【已驗證】": len(re.findall(r"【已驗證】", content)),
        "【對不上】": len(re.findall(r"【對不上】", content)),
        "【概念有出處，數字沒有】": len(re.findall(r"【概念有出處，數字沒有】", content)),
        "【未驗證】": len(re.findall(r"【未驗證】", content)),
    }
    total = sum(stats.values())
    
    print(f"=== 反查統計結果 (總計 {total} 條) ===")
    print(f"已驗證: {stats['【已驗證】']} 條")
    print(f"對不上: {stats['【對不上】']} 條")
    print(f"概念有出處，數字沒有: {stats['【概念有出處，數字沒有】']} 條")
    print(f"未驗證: {stats['【未驗證】']} 條")
    print(f"有效查證覆蓋率: {((total - stats['【未驗證】']) / total * 100):.1f}%")

if __name__ == "__main__":
    count_marks()
