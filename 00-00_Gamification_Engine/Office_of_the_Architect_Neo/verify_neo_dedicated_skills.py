#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_neo_dedicated_skills.py
驗證尼奧兩大專屬實戰技能 (polaris-gentle-ui, polaris-client-architect)
與存摺突觸代謝精煉 (00_Neo_Axiom_Index.md) 之物理完整性。
【採用 Python 3 原生標準庫，絕無第三方依賴】
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def parse_simple_frontmatter(text):
    parts = text.split("---")
    if len(parts) < 3:
        return {}
    fm_lines = parts[1].strip().split("\n")
    data = {}
    for line in fm_lines:
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip()
    return data

def verify():
    print("=" * 60)
    print(" [NEO] 專屬技能與突觸代謝物理驗證 (Exit Code: 0 質檢)")
    print("=" * 60)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # 1. 檢查 00_Neo_Axiom_Index.md
    axiom_path = os.path.join(base_dir, "00-00_Gamification_Engine", "Office_of_the_Architect_Neo", "01_Cognitive_Log", "00_Neo_Axiom_Index.md")
    assert os.path.exists(axiom_path), f"找不到金律索引: {axiom_path}"
    with open(axiom_path, "r", encoding="utf-8") as f:
        axiom_content = f.read()
    assert "尼奧核心架構直覺金律精煉索引" in axiom_content
    assert "30." in axiom_content, "缺少第 30 條神聖金律"
    print("  [Gate 1: PASS] 00_Neo_Axiom_Index.md 存在且包含 30 條直覺金律")

    # 2. 檢查 polaris-gentle-ui
    gentle_ui_path = os.path.join(base_dir, ".agents", "skills", "polaris-gentle-ui", "SKILL.md")
    assert os.path.exists(gentle_ui_path), f"找不到技能: {gentle_ui_path}"
    with open(gentle_ui_path, "r", encoding="utf-8") as f:
        gentle_content = f.read()
    
    frontmatter = parse_simple_frontmatter(gentle_content)
    assert frontmatter.get("name") == "polaris-gentle-ui", f"技能名稱錯誤: {frontmatter.get('name')}"
    assert frontmatter.get("role_key") == "neo", f"角色鍵錯誤: {frontmatter.get('role_key')}"
    assert "陳品碩" in frontmatter.get("authorized_by", ""), "授權人錯誤"
    assert "flowchart TD" in gentle_content, "缺少 Mermaid 架構圖"
    assert "GentleButton" in gentle_content, "缺少 GentleButton 代碼規格"
    assert "生活的一部分，就醬點！" in gentle_content, "缺少法定品牌命名"
    print("  [Gate 2: PASS] polaris-gentle-ui 結構與參數驗證通過")

    # 3. 檢查 polaris-client-architect
    architect_path = os.path.join(base_dir, ".agents", "skills", "polaris-client-architect", "SKILL.md")
    assert os.path.exists(architect_path), f"找不到技能: {architect_path}"
    with open(architect_path, "r", encoding="utf-8") as f:
        arch_content = f.read()
    
    frontmatter_arch = parse_simple_frontmatter(arch_content)
    assert frontmatter_arch.get("name") == "polaris-client-architect", f"技能名稱錯誤: {frontmatter_arch.get('name')}"
    assert frontmatter_arch.get("role_key") == "neo", f"角色鍵錯誤: {frontmatter_arch.get('role_key')}"
    assert "陳品碩" in frontmatter_arch.get("authorized_by", ""), "授權人錯誤"
    assert "flowchart TD" in arch_content, "缺少 Mermaid 架構圖"
    assert "service-worker-heartbeat" in arch_content, "缺少 Service Worker 代碼規格"
    assert "生活的一部分，就醬點！" in arch_content, "缺少法定品牌命名"
    print("  [Gate 3: PASS] polaris-client-architect 結構與參數驗證通過")

    # 4. 品牌紅線防護檢查
    assert "生活管家" in gentle_content
    assert "管家選品" in gentle_content
    print("  [Gate 4: PASS] 品牌法定名稱與出廠攔截防線檢驗通過")

    print("=" * 60)
    print(" 🎯 全部檢驗閘門 100% 通過！Exit Code: 0")
    print("=" * 60)

if __name__ == "__main__":
    verify()
