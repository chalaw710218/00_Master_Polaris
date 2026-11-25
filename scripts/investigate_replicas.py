# -*- coding: utf-8 -*-
r"""
scripts/investigate_replicas.py
調查：
1. 00-02_GroupBuy_Products/.agents/ 底下所有技能，與根目錄 .agents/skills/ 的重複狀態
2. C:/Users/lenovo/.gemini/config/skills/ 底下所有技能：名稱、行數、與雲端硬碟同名技能是否一致
"""

import os
from pathlib import Path

ROOT_DIR = Path(".")
ROOT_SKILLS = ROOT_DIR / ".agents" / "skills"
GB_AGENTS = ROOT_DIR / "00-02_GroupBuy_Products" / ".agents"
CONFIG_SKILLS = Path("C:/Users/lenovo/.gemini/config/skills")

print("=" * 70)
print("🔍【調查一：00-02_GroupBuy_Products/.agents/ 技能盤點】")
print("=" * 70)

gb_skill_files = []
if GB_AGENTS.exists():
    for root, dirs, files in os.walk(GB_AGENTS):
        if "_archive" in root:
            continue
        if "SKILL.md" in files:
            p = Path(root) / "SKILL.md"
            gb_skill_files.append(p)

print(f"找到 {len(gb_skill_files)} 份技能：")
for p in sorted(gb_skill_files):
    rel_p = p.relative_to(ROOT_DIR)
    skill_name = p.parent.name
    
    # 檢查根目錄 .agents/skills 是否有同名技能
    root_match = None
    # 檢查根目錄直屬或 atoms 下
    candidate1 = ROOT_SKILLS / skill_name / "SKILL.md"
    candidate2 = ROOT_SKILLS / "atoms" / skill_name / "SKILL.md"
    if candidate1.exists():
        root_match = candidate1
    elif candidate2.exists():
        root_match = candidate2
    
    if root_match:
        c_gb = p.read_text(encoding="utf-8")
        c_root = root_match.read_text(encoding="utf-8")
        identical = (c_gb == c_root)
        lines_gb = len(c_gb.splitlines())
        lines_root = len(c_root.splitlines())
        status_str = f"⚠️ 重複存在 ({'內容完全一致' if identical else '內容有差異'}) [00-02: {lines_gb}行 vs 根目錄: {lines_root}行]"
    else:
        status_str = "獨有（根目錄 .agents/skills/ 無同名技能）"
    
    print(f"• {skill_name:30} 路徑: {rel_p}")
    print(f"  狀態: {status_str}")

print("\n" + "=" * 70)
print("🔍【調查二：C:\\Users\\lenovo\\.gemini\\config\\skills\\ 技能盤點】")
print("=" * 70)

config_skill_files = []
if CONFIG_SKILLS.exists():
    for root, dirs, files in os.walk(CONFIG_SKILLS):
        if "_archive" in root:
            continue
        if "SKILL.md" in files:
            p = Path(root) / "SKILL.md"
            config_skill_files.append(p)

print(f"找到 {len(config_skill_files)} 份技能：")

# 建立雲端硬碟全域技能索引（依 skill_name）
workspace_skills = {}
for root, dirs, files in os.walk(ROOT_DIR):
    if ".git" in root or "_archive" in root or "_done" in root or "_master_history" in root:
        continue
    if "SKILL.md" in files:
        p = Path(root) / "SKILL.md"
        s_name = p.parent.name
        if s_name not in workspace_skills:
            workspace_skills[s_name] = []
        workspace_skills[s_name].append(p)

for p in sorted(config_skill_files):
    skill_name = p.parent.name
    c_cfg = p.read_text(encoding="utf-8")
    lines_cfg = len(c_cfg.splitlines())
    
    ws_matches = workspace_skills.get(skill_name, [])
    
    if ws_matches:
        ws_p = ws_matches[0]
        c_ws = ws_p.read_text(encoding="utf-8")
        lines_ws = len(c_ws.splitlines())
        identical = (c_cfg == c_ws)
        ws_rel = ws_p.relative_to(ROOT_DIR)
        status_str = f"⚠️ 雲端硬碟有對應技能 ({ws_rel}) -> {'內容完全一致' if identical else f'內容不一致 (全域: {lines_cfg}行 vs 本地: {lines_ws}行)'}"
    else:
        status_str = "全域配置專用（雲端硬碟工作區無同名技能）"
    
    print(f"• {skill_name:30} 行數: {lines_cfg:3d} 行 | 檔案: {p}")
    print(f"  狀態: {status_str}")
