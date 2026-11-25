#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_scanner.py
================
極星宇宙全內閣技能架構盤點與《00-00 格式規範 v1.0》合規掃描程式 (只讀不改)
執行者：執行長 雪 (Yuki)
================
功能：
1. 遞歸掃描整個 00_Master_Polaris 尋找所有技能檔與資料檔。
2. 排除 Office_of_the_Scout_Ada/.agents/skills 鏡像交會點 (Junction)。
3. 排除 SKILL_MAP.md、SKILL_ISSUES.md（不當作 SKILL_*.md 舊版）。
4. _archive/、_master_history/ 裡的檔案和備份檔，不列入任何問題統計。
5. 特化版（bionic-learning-xxx）沒被母版點名，不算問題。
6. 依《00-00 極星格式規範 v1.0》執行技能檔 8 項 ❌ 錯誤與 4 項 ⚠️ 提醒檢核。
7. 執行全專案資料檔 UTF-8 編碼 (❌) 與工作資料夾殘留垃圾 (⚠️) 檢核。
8. 產出結構化 SKILL_MAP.md 與包含合規總覽之 SKILL_ISSUES.md。
9. 全程 Exit Code 0（只報告、不攔截），嚴禁移動、刪除或修改任何被掃描檔案。
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
import yaml

# 設定標準輸出編碼為 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def clean_markdown_field(val: str) -> str:
    """清理 Markdown 格式（去除反引號、星號、引號、跳轉連結等）"""
    if not val:
        return ""
    val = str(val).strip()
    m_link = re.match(r'^\[(.*?)\]\(.*?\)$', val)
    if m_link:
        val = m_link.group(1).strip()
    val = val.strip("`'\"*_ ")
    return val


def normalize_parent_target(raw_parent: str) -> str:
    """
    去掉括號版本字（例如 (v6.5-MASTER)），再用資料夾名稱比對。
    """
    if not raw_parent:
        return ""
    cleaned = re.sub(r'[\(（][^\)）]*[\)）]', '', str(raw_parent)).strip()
    cleaned = clean_markdown_field(cleaned)

    posix = cleaned.replace("\\", "/").rstrip("/")
    if "/" in posix or posix.endswith(".md"):
        p = Path(posix)
        if p.suffix == ".md":
            return p.parent.name
        return p.name
    return cleaned


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """解析 YAML Frontmatter，回傳 (frontmatter_dict, body_text)"""
    m = re.match(r'^\ufeff?---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.DOTALL)
    if not m:
        return {}, text

    fm_raw = m.group(1)
    body_text = m.group(2)

    # 優先嘗試標準 YAML 解析
    try:
        data = yaml.safe_load(fm_raw)
        if isinstance(data, dict):
            return data, body_text
    except Exception:
        pass

    # 容錯：行級別備用解析器（可處理非標準引號與未轉義冒號）
    res = {}
    lines = fm_raw.splitlines()
    curr_key = None
    curr_val = []
    in_metadata = False
    meta_dict = {}

    for line in lines:
        stripped = line.strip()
        if stripped == "metadata:":
            if curr_key:
                res[curr_key] = "\n".join(curr_val).strip()
                curr_key = None
            in_metadata = True
            continue

        if in_metadata:
            # 檢查是否仍在 metadata 的縮排子欄位
            m_sub = re.match(r'^\s+([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line)
            if m_sub:
                meta_dict[m_sub.group(1)] = m_sub.group(2).strip("'\" ")
                continue
            elif re.match(r'^[a-zA-Z0-9_-]+\s*:', line):
                in_metadata = False
                res["metadata"] = meta_dict

        m_top = re.match(r'^([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line)
        if m_top:
            if curr_key:
                res[curr_key] = "\n".join(curr_val).strip()
            curr_key = m_top.group(1)
            curr_val = [m_top.group(2)]
        else:
            if curr_key:
                curr_val.append(line)

    if curr_key:
        res[curr_key] = "\n".join(curr_val).strip()
    if in_metadata:
        res["metadata"] = meta_dict

    return res, body_text


def scan_skill_file(filepath: Path, workspace_root: Path) -> dict:
    """掃描單一技能檔案，擷取各項指標與中繼資料"""
    rel_path = filepath.relative_to(workspace_root)
    file_bytes = filepath.read_bytes()
    size_bytes = len(file_bytes)

    # 編碼檢查
    is_utf8 = True
    encoding_error = None
    try:
        content = file_bytes.decode("utf-8")
    except UnicodeDecodeError as ex:
        is_utf8 = False
        encoding_error = str(ex)
        content = file_bytes.decode("utf-8", errors="replace")

    lines = content.splitlines()
    line_count = len(lines)

    # 解析 Frontmatter
    fm, body = parse_frontmatter(content)
    if not isinstance(fm, dict):
        fm = {}

    name = str(fm.get("name", "")).strip("'\" ")
    if not name and filepath.name == "SKILL.md":
        name = filepath.parent.name

    desc = str(fm.get("description", "")).strip("'\" ")
    metadata = fm.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    # 內文「所屬技能組」與「原技能母體」
    skill_group = str(metadata.get("group", "")).strip("'\" ")
    if not skill_group:
        m_group = re.search(r'(?:\*\*|__)?所屬技能組(?:\*\*|__)?\s*[：:]\s*(.+)$', body, re.MULTILINE)
        if m_group:
            skill_group = clean_markdown_field(m_group.group(1))

    parent_skill = str(metadata.get("parent", "")).strip("'\" ")
    if not parent_skill:
        m_parent = re.search(r'(?:\*\*|__)?原技能母體(?:\*\*|__)?\s*[：:]\s*(.+)$', body, re.MULTILINE)
        if m_parent:
            parent_skill = clean_markdown_field(m_parent.group(1))
        elif fm.get("parent_skill"):
            parent_skill = str(fm.get("parent_skill")).strip("'\" ")
        elif fm.get("base_master"):
            parent_skill = str(fm.get("base_master")).strip("'\" ")

    normalized_parent = normalize_parent_target(parent_skill)

    # 一句話用途
    purpose = desc
    if not purpose:
        m_quote = re.search(r'^>\s*(.+)$', body, re.MULTILINE)
        if m_quote:
            purpose = clean_markdown_field(m_quote.group(1))
        else:
            purpose = "無描述"
    purpose = re.sub(r'\s+', ' ', purpose).strip()
    if len(purpose) > 120:
        purpose = purpose[:117] + "..."

    posix_rel = str(rel_path).replace("\\", "/").lower()
    is_mirror = ("office_of_the_scout_ada/.agents/skills" in posix_rel) or ("00-02_groupbuy_products/.agents/skills" in posix_rel)
    is_archived = ("_archive" in posix_rel) or ("_master_history" in posix_rel)
    is_backup = (filepath.name.startswith("SKILL_") and filepath.name.endswith(".md"))

    return {
        "path": filepath,
        "rel_path": rel_path,
        "posix_rel": str(rel_path).replace("\\", "/"),
        "filename": filepath.name,
        "name": name,
        "description": desc,
        "metadata": metadata,
        "fm": fm,
        "skill_group": skill_group,
        "parent_skill": parent_skill,
        "normalized_parent": normalized_parent,
        "purpose": purpose,
        "size_bytes": size_bytes,
        "line_count": line_count,
        "is_utf8": is_utf8,
        "encoding_error": encoding_error,
        "is_backup": is_backup,
        "is_mirror": is_mirror,
        "is_archived": is_archived,
        "raw_content": content,
    }


def find_all_workspace_files(root: Path):
    """
    尋找所有技能檔、備份檔、資料檔與殘留檔案
    排除 .git、排除 Ada 鏡像、排除 SKILL_MAP.md 與 SKILL_ISSUES.md
    """
    skill_files = []
    data_files = []
    residual_artifacts = []
    mirror_skill_count = 0

    target_data_exts = {".md", ".txt", ".json", ".jsonl", ".py"}

    for dirpath, dirnames, filenames in os.walk(root):
        posix_dir = Path(dirpath).as_posix().lower()
        if ".git" in dirnames:
            dirnames.remove(".git")
        if "office_of_the_scout_ada/.agents/skills" in posix_dir or "00-02_groupbuy_products/.agents/skills" in posix_dir:
            # 計算鏡像技能檔數量後略過 (Junction 目錄聯結，非實體重複)
            for f in filenames:
                if f == "SKILL.md" or (f.startswith("SKILL_") and f.endswith(".md")):
                    if f not in ("SKILL_MAP.md", "SKILL_ISSUES.md"):
                        mirror_skill_count += 1
            continue

        # 排除 _proposed 提案留存目錄
        if "_proposed" in posix_dir:
            continue

        # 排除 00-11 逆向研究樣本（target/ 資料夾，非閣員技能）
        if "00-11_reverse_engineering_lab" in posix_dir:
            if "/target" in posix_dir or posix_dir.endswith("/target"):
                continue
            if "target" in dirnames:
                dirnames.remove("target")

        # 檢測 __pycache__
        if "__pycache__" in dirnames:
            rel_dir = Path(dirpath, "__pycache__").relative_to(root)
            if "_archive" not in posix_dir and "_master_history" not in posix_dir:
                residual_artifacts.append({"type": "__pycache__ 快取資料夾", "path": rel_dir})

        for f in filenames:
            p = Path(dirpath) / f
            p_posix = p.as_posix().lower()

            # 排除自產報表
            if f in ("SKILL_MAP.md", "SKILL_ISSUES.md"):
                continue

            # 排除封存資料夾（規範第三條：_archive/、_master_history/ 裡的檔案，掃描程式會略過）
            if "_archive" in p_posix or "_master_history" in p_posix:
                # 舊版技能檔若已在 _archive 內，記錄為備份技能供 E8 比對
                if f.startswith("SKILL_") and f.endswith(".md"):
                    skill_files.append(p)
                continue

            # 技能檔判定
            if f == "SKILL.md" or (f.startswith("SKILL_") and f.endswith(".md")):
                skill_files.append(p)

            # 資料檔判定 (用於 UTF-8 檢查，僅限工作目錄)
            if p.suffix.lower() in target_data_exts:
                data_files.append(p)

            # 殘留檔案判定 (.bak, .pyc)
            if f.endswith(".bak") or f.endswith(".pyc"):
                residual_artifacts.append({
                    "type": f"殘留檔案 (*{p.suffix})",
                    "path": p.relative_to(root)
                })

    skill_files.sort()
    data_files.sort()
    return skill_files, data_files, residual_artifacts, mirror_skill_count


def audit_skills_and_data(active_skills, backup_skills, all_data_files, residual_artifacts, workspace_root: Path):
    """
    依《00-00 極星格式規範 v1.0》執行全面審計
    """
    # 建立目錄名稱與技能名稱索引
    folder_to_skills = defaultdict(list)
    name_to_skills = defaultdict(list)
    for s in active_skills:
        folder_to_skills[s["path"].parent.name].append(s)
        name_to_skills[s["name"]].append(s)

    # 1. 技能檔錯誤 (❌) 與提醒 (⚠️)
    skill_issues = defaultdict(lambda: {"errors": [], "warnings": []})

    # 各規則統計計數
    rule_counts = {
        # ❌ 錯誤
        "E1_missing_name_or_desc": 0,
        "E2_invalid_name_format": 0,
        "E3_name_folder_mismatch": 0,
        "E4_desc_over_1024": 0,
        "E5_invalid_status": 0,
        "E6_invalid_evidence": 0,
        "E7_atom_missing_group_or_parent": 0,
        "E8_backup_outside_archive": 0,
        "E9_non_utf8_data": 0,
        # ⚠️ 提醒
        "W1_desc_over_200": 0,
        "W2_missing_owner_or_version": 0,
        "W3_extra_top_level_fields": 0,
        "W4_lines_over_500": 0,
        "W5_residual_artifacts": len(residual_artifacts),
    }

    # 檢核現役 SKILL.md
    for s in active_skills:
        name = s["name"]
        desc = s["description"]
        meta = s["metadata"]
        folder_name = s["path"].parent.name
        rel_posix = s["posix_rel"]

        # ❌ E1: 缺少 name 或 description
        if not name or not desc:
            rule_counts["E1_missing_name_or_desc"] += 1
            skill_issues[rel_posix]["errors"].append("❌ 缺少 name 或 description")

        # ❌ E2: name 不是小寫英文、數字、連字號，或超過 64 字元
        if not re.match(r'^[a-z0-9-]+$', name) or len(name) > 64:
            rule_counts["E2_invalid_name_format"] += 1
            skill_issues[rel_posix]["errors"].append(f"❌ name 格式不合格（只能小寫英文/數字/連字號且<=64字）：`{name}`")

        # ❌ E3: name 跟所在資料夾名稱不同
        if name != folder_name:
            rule_counts["E3_name_folder_mismatch"] += 1
            skill_issues[rel_posix]["errors"].append(f"❌ name (`{name}`) 與所在資料夾 (`{folder_name}`) 不符")

        # ❌ E4: description 超過 1024 字元
        if len(desc) > 1024:
            rule_counts["E4_desc_over_1024"] += 1
            skill_issues[rel_posix]["errors"].append(f"❌ description 長度超過 1024 字元（目前 {len(desc)} 字）")

        # ❌ E5: metadata.status 不是 active / draft / archived
        status = str(meta.get("status", "")).strip().lower()
        if status not in ("active", "draft", "archived"):
            rule_counts["E5_invalid_status"] += 1
            skill_issues[rel_posix]["errors"].append(f"❌ metadata.status 非法（需為 active/draft/archived，目前為 `{status or '未填'}`）")

        # ❌ E6: status 是 active，但沒有 metadata.evidence 或檔案不存在
        if status == "active":
            evidence = str(meta.get("evidence", "")).strip()
            if not evidence:
                rule_counts["E6_invalid_evidence"] += 1
                skill_issues[rel_posix]["errors"].append("❌ active 技能缺少 metadata.evidence 憑證路徑")
            else:
                ev_local = s["path"].parent / evidence
                ev_root = workspace_root / evidence
                if not ev_local.exists() and not ev_root.exists():
                    rule_counts["E6_invalid_evidence"] += 1
                    skill_issues[rel_posix]["errors"].append(f"❌ metadata.evidence 指向之檔案不存在：`{evidence}`")

        # ❌ E7: atom-* 技能缺少 metadata.group 或 metadata.parent
        if name.startswith("atom-"):
            m_group = meta.get("group")
            m_parent = meta.get("parent")
            if not m_group or not m_parent:
                rule_counts["E7_atom_missing_group_or_parent"] += 1
                missing_fields = []
                if not m_group: missing_fields.append("metadata.group")
                if not m_parent: missing_fields.append("metadata.parent")
                skill_issues[rel_posix]["errors"].append(f"❌ atom 技能缺少必填中繼資料：{', '.join(missing_fields)}")

        # ⚠️ W1: description 超過 200 字
        if len(desc) > 200:
            rule_counts["W1_desc_over_200"] += 1
            skill_issues[rel_posix]["warnings"].append(f"⚠️ description 建議控制在 200 字以內（目前 {len(desc)} 字）")

        # ⚠️ W2: 缺少 metadata.owner 或 metadata.version
        m_owner = meta.get("owner")
        m_ver = meta.get("version")
        if not m_owner or not m_ver:
            rule_counts["W2_missing_owner_or_version"] += 1
            missing_w = []
            if not m_owner: missing_w.append("metadata.owner")
            if not m_ver: missing_w.append("metadata.version")
            skill_issues[rel_posix]["warnings"].append(f"⚠️ 缺少建議欄位：{', '.join(missing_w)}")

        # ⚠️ W3: frontmatter 最外層有規範以外的欄位，應搬進 metadata
        allowed_top = {"name", "description", "metadata"}
        extra_keys = sorted(list(set(s["fm"].keys()) - allowed_top))
        if extra_keys:
            rule_counts["W3_extra_top_level_fields"] += 1
            skill_issues[rel_posix]["warnings"].append(f"⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`{extra_keys}`")

        # ⚠️ W4: SKILL.md 超過 500 行
        if s["line_count"] > 500:
            rule_counts["W4_lines_over_500"] += 1
            skill_issues[rel_posix]["warnings"].append(f"⚠️ 技能內文超過 500 行（目前 {s['line_count']} 行），建議將理論移至 references/")

    # ❌ E8: 舊版 SKILL_*.md 不在 _archive/ 或 _master_history/ 裡
    illegal_backups = []
    for b in backup_skills:
        posix_b = str(b.relative_to(workspace_root)).replace("\\", "/")
        if "_archive" not in posix_b and "_master_history" not in posix_b:
            rule_counts["E8_backup_outside_archive"] += 1
            illegal_backups.append(posix_b)

    # ❌ E9: .md, .txt, .json, .jsonl, .py 不是 UTF-8 編碼
    non_utf8_files = []
    for f in all_data_files:
        try:
            f.read_bytes().decode("utf-8")
        except UnicodeDecodeError as ex:
            rule_counts["E9_non_utf8_data"] += 1
            non_utf8_files.append({
                "path": str(f.relative_to(workspace_root)).replace("\\", "/"),
                "error": str(ex)
            })

    # 結構性檢查：標註的原技能母體不存在
    missing_parent_issues = []
    parent_missing_atom_issues = []

    for s in active_skills:
        norm_parent = s["normalized_parent"]
        if norm_parent:
            # 特化版（bionic-learning-xxx）沒被母版點名，不算問題
            parent_matches = folder_to_skills.get(norm_parent, [])
            if not parent_matches:
                parent_matches = name_to_skills.get(norm_parent, [])

            if not parent_matches:
                missing_parent_issues.append({
                    "skill": s["name"],
                    "path": s["posix_rel"],
                    "raw_parent": s["parent_skill"],
                    "normalized_parent": norm_parent
                })
            else:
                # 檢查母體是否有點名 atom
                atom_name = s["name"]
                # 豁免：特化版不需被母版點名
                if norm_parent == "bionic-learning-system" and atom_name.startswith("bionic-learning-"):
                    continue

                mentioned = any(atom_name in p_rec["raw_content"] for p_rec in parent_matches)
                if not mentioned:
                    parent_missing_atom_issues.append({
                        "atom": atom_name,
                        "atom_path": s["posix_rel"],
                        "parent": norm_parent,
                        "parent_path": parent_matches[0]["posix_rel"]
                    })

    # 計算合規度
    total_active_skills = len(active_skills)
    fully_compliant_count = 0
    zero_error_count = 0

    for s in active_skills:
        rel = s["posix_rel"]
        errs = skill_issues[rel]["errors"]
        warns = skill_issues[rel]["warnings"]
        if len(errs) == 0:
            zero_error_count += 1
            if len(warns) == 0:
                fully_compliant_count += 1

    return {
        "total_active_skills": total_active_skills,
        "fully_compliant_count": fully_compliant_count,
        "zero_error_count": zero_error_count,
        "rule_counts": rule_counts,
        "skill_issues": skill_issues,
        "illegal_backups": illegal_backups,
        "non_utf8_files": non_utf8_files,
        "missing_parent_issues": missing_parent_issues,
        "parent_missing_atom_issues": parent_missing_atom_issues,
        "residual_artifacts": residual_artifacts,
    }


def generate_skill_map(active_records: list[dict], mirror_count: int, archived_count: int, output_path: Path):
    """產生 00_Master_Polaris/SKILL_MAP.md（排除鏡像與封存檔案）"""
    groups_dict = defaultdict(list)
    ungrouped = []

    for r in active_records:
        if r["skill_group"]:
            groups_dict[r["skill_group"]].append(r)
        else:
            ungrouped.append(r)

    lines = []
    lines.append("# 🗺️ 極星宇宙全內閣技能全景地圖 (SKILL MAP)")
    lines.append("")
    lines.append("> ⚠️ **本檔由 `skill_scanner.py` 自動產生，請勿手改**  ")
    lines.append(f"> 執行者：**執行長 雪 (Yuki)** ｜ 依據：《00-00 極星格式規範 v1.0》  ")
    lines.append(f"> 現役技能總數：**{len(active_records)}** 份（已排除鏡像 **{mirror_count}** 份、封存 **{archived_count}** 份）  ")
    lines.append(f"> 技能組總數：**{len(groups_dict)}** 組 ｜ 未歸類技能：**{len(ungrouped)}** 份")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📑 技能組索引目錄 (Group Directory)")
    lines.append("")
    for idx, g_name in enumerate(sorted(groups_dict.keys()), 1):
        count = len(groups_dict[g_name])
        slug = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '', g_name.lower())
        lines.append(f"{idx}. [{g_name}](#{slug}) ({count} 個技能)")
    lines.append(f"{len(groups_dict) + 1}. [未歸類技能組（獨立/未標註技能）](#未歸類技能組獨立未標註技能) ({len(ungrouped)} 個技能)")
    lines.append("")
    lines.append("---")
    lines.append("")

    for g_name in sorted(groups_dict.keys()):
        slug = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '', g_name.lower())
        lines.append(f'<a id="{slug}"></a>')
        lines.append(f"## 🧩 技能組：{g_name}")
        lines.append("")
        lines.append("| 技能名稱 (Name) | 狀態 | 相對路徑 (Path) | 一句話用途 (Description) | 原技能母體 |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")

        for r in sorted(groups_dict[g_name], key=lambda x: x["name"]):
            status = r["metadata"].get("status", "draft")
            parent = f"`{r['normalized_parent']}`" if r["normalized_parent"] else "-"
            lines.append(f"| **`{r['name']}`** | `{status}` | [{r['posix_rel']}]({r['posix_rel']}) | {r['purpose']} | {parent} |")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append('<a id="未歸類技能組獨立未標註技能"></a>')
    lines.append("## 📦 未歸類技能組（獨立/未標註技能）")
    lines.append("")
    lines.append("| 技能名稱 (Name) | 狀態 | 相對路徑 (Path) | 一句話用途 (Description) |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for r in sorted(ungrouped, key=lambda x: x["name"]):
        status = r["metadata"].get("status", "draft")
        lines.append(f"| **`{r['name']}`** | `{status}` | [{r['posix_rel']}]({r['posix_rel']}) | {r['purpose']} |")

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_skill_issues(audit_res: dict, mirror_count: int, archived_count: int, output_path: Path):
    """產生 00_Master_Polaris/SKILL_ISSUES.md"""
    rc = audit_res["rule_counts"]
    total = audit_res["total_active_skills"]
    compliant = audit_res["fully_compliant_count"]
    zero_err = audit_res["zero_error_count"]

    lines = []
    lines.append("# 🚨 極星宇宙全內閣技能架構與格式規範檢核報告 (SKILL ISSUES)")
    lines.append("")
    lines.append("> ⚠️ **本檔由 `skill_scanner.py` 自動產生，請勿手改**  ")
    lines.append(f"> 執行者：**執行長 雪 (Yuki)** ｜ 依據：《00-00 極星格式規範 v1.0》  ")
    lines.append(f"> 掃描檔案總數：現役 **{total}** 份（已排除鏡像 **{mirror_count}** 份、封存 **{archived_count}** 份）")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 規範合規總覽
    lines.append("## 🎯 格式規範合規總覽 (Format Standard Compliance Summary)")
    lines.append("")
    lines.append(f"- **完全合規技能數（0 錯誤 0 提醒）**：**{compliant}** / **{total}** ({compliant/total*100:.1f}%)")
    lines.append(f"- **無嚴重錯誤技能數（0 錯誤，含過渡提醒）**：**{zero_err}** / **{total}** ({zero_err/total*100:.1f}%)")
    lines.append("")
    lines.append("### 📋 規則違規統計清冊")
    lines.append("")
    lines.append("| 規則代號 | 規範項目 | 嚴重度 | 違反數量 | 處置方向 |")
    lines.append("| :--- | :--- | :---: | :---: | :--- |")
    lines.append(f"| **E1** | 缺少 name 或 description | ❌ 錯誤 | `{rc['E1_missing_name_or_desc']}` 份 | 補齊 Frontmatter 必填欄位 |")
    lines.append(f"| **E2** | name 格式非法（只能小寫/數字/連字號，<=64字） | ❌ 錯誤 | `{rc['E2_invalid_name_format']}` 份 | 重新命名為小寫連字號格式 |")
    lines.append(f"| **E3** | name 與所在資料夾名稱不一致 | ❌ 錯誤 | `{rc['E3_name_folder_mismatch']}` 份 | 校正 name 使其與資料夾完全一致 |")
    lines.append(f"| **E4** | description 超過 1024 字元 | ❌ 錯誤 | `{rc['E4_desc_over_1024']}` 份 | 簡化描述至精簡字數 |")
    lines.append(f"| **E5** | metadata.status 非 active/draft/archived | ❌ 錯誤 | `{rc['E5_invalid_status']}` 份 | 正確設定狀態標籤 |")
    lines.append(f"| **E6** | active 技能缺少 evidence 憑證或檔案不存在 | ❌ 錯誤 | `{rc['E6_invalid_evidence']}` 份 | 補齊測試程式或降回 draft |")
    lines.append(f"| **E7** | atom-* 技能缺少 metadata.group 或 parent | ❌ 錯誤 | `{rc['E7_atom_missing_group_or_parent']}` 份 | 於 metadata 補齊組別與母體標籤 |")
    lines.append(f"| **E8** | 舊版 SKILL_*.md 滯留於非封存目錄 | ❌ 錯誤 | `{rc['E8_backup_outside_archive']}` 份 | 移入同層之 `_archive/` 目錄 |")
    lines.append(f"| **E9** | 資料檔非 UTF-8 編碼 (.md/.txt/.json/.py) | ❌ 錯誤 | `{rc['E9_non_utf8_data']}` 份 | 轉換為標準 UTF-8 編碼 |")
    lines.append(f"| **W1** | description 超過 200 字（建議精簡） | ⚠️ 提醒 | `{rc['W1_desc_over_200']}` 份 | 精簡為做什麼/何時用/何時不用 |")
    lines.append(f"| **W2** | 缺少 metadata.owner 或 metadata.version | ⚠️ 提醒 | `{rc['W2_missing_owner_or_version']}` 份 | 補齊負責閣員與版本標籤 |")
    lines.append(f"| **W3** | frontmatter 存在自訂欄位未收入 metadata | ⚠️ 提醒 | `{rc['W3_extra_top_level_fields']}` 份 | 將自訂鍵搬入 metadata 底下 |")
    lines.append(f"| **W4** | SKILL.md 內文超過 500 行 | ⚠️ 提醒 | `{rc['W4_lines_over_500']}` 份 | 將理論背景拆分至 references/ |")
    lines.append(f"| **W5** | 工作資料夾存在殘留檔案 (.bak/.pyc/__pycache__) | ⚠️ 提醒 | `{rc['W5_residual_artifacts']}` 處 | 執行清理或封存 |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 詳細違規清冊：技能檔 ❌ 錯誤
    lines.append("## ❌ 一、技能檔嚴格違規清冊 (Skill Errors)")
    lines.append("")
    has_err = False
    for path, data in sorted(audit_res["skill_issues"].items()):
        if data["errors"]:
            has_err = True
            lines.append(f"### 📄 [{path}]({path})")
            for e in data["errors"]:
                lines.append(f"- {e}")
            lines.append("")
    if not has_err:
        lines.append("✅ **零違規**：所有現役技能檔皆無任何嚴重錯誤！\n")
    lines.append("---")
    lines.append("")

    # 詳細違規清冊：滯留之舊版檔
    lines.append("## ❌ 二、未歸檔之舊版技能檔 (Backups outside _archive/)")
    lines.append("")
    if audit_res["illegal_backups"]:
        lines.append("| 滯留舊版路徑 | 處置建議 |")
        lines.append("| :--- | :--- |")
        for b_path in audit_res["illegal_backups"]:
            lines.append(f"| [{b_path}]({b_path}) | 移至同層 `_archive/` |")
    else:
        lines.append("✅ **零滯留**：所有舊版與歷史檔皆已妥善存放於 `_archive/` 或 `_master_history/`。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 詳細違規清冊：非 UTF-8 資料檔
    lines.append("## ❌ 三、非 UTF-8 資料檔清冊 (Non-UTF-8 Data Files)")
    lines.append("")
    if audit_res["non_utf8_files"]:
        lines.append("| 異常檔案路徑 | 解碼錯誤原因 |")
        lines.append("| :--- | :--- |")
        for nf in audit_res["non_utf8_files"]:
            lines.append(f"| [{nf['path']}]({nf['path']}) | `{nf['error']}` |")
    else:
        lines.append("✅ **零異常**：全工作區所有 `.md`、`.txt`、`.json`、`.jsonl`、`.py` 檔案皆為 100% 正確的 UTF-8 編碼。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 詳細提醒清冊：技能檔 ⚠️ 提醒
    lines.append("## ⚠️ 四、技能檔格式提醒清冊 (Skill Format Warnings)")
    lines.append("")
    has_warn = False
    for path, data in sorted(audit_res["skill_issues"].items()):
        if data["warnings"]:
            has_warn = True
            lines.append(f"### 📄 [{path}]({path})")
            for w in data["warnings"]:
                lines.append(f"- {w}")
            lines.append("")
    if not has_warn:
        lines.append("✅ **零提醒**：所有技能皆完全符合最新推薦格式！\n")
    lines.append("---")
    lines.append("")

    # 詳細提醒清冊：殘留檔案
    lines.append("## ⚠️ 五、工作資料夾殘留垃圾清冊 (Residual Artifacts)")
    lines.append("")
    if audit_res["residual_artifacts"]:
        lines.append("| 殘留類型 | 檔案相對路徑 | 建議動作 |")
        lines.append("| :--- | :--- | :--- |")
        for r in audit_res["residual_artifacts"]:
            p_str = str(r["path"]).replace("\\", "/")
            lines.append(f"| {r['type']} | [{p_str}]({p_str}) | 刪除或移至 _archive/ |")
    else:
        lines.append("✅ **零殘留**：工作資料夾乾淨整潔，無任何 `.bak`、`.pyc` 或快取垃圾。")
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    workspace_root = Path(__file__).resolve().parent.parent
    scan_root = workspace_root
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg_path = Path(sys.argv[1]).resolve()
        if arg_path.exists():
            scan_root = arg_path

    print("=" * 70)
    print("🛠️  極星宇宙全內閣技能架構與格式規範合規掃描程式 (CEO Yuki Edition)")
    print(f"📂 掃描目標目錄：{scan_root}")
    print("=" * 70)

    # 1. 尋找所有檔案
    skill_files, data_files, residual_artifacts, mirror_skill_count = find_all_workspace_files(scan_root)

    # 2. 逐一解析每份技能檔
    all_skill_records = []
    for p in skill_files:
        rec = scan_skill_file(p, scan_root)
        all_skill_records.append(rec)

    # 分流：封存、非封存備份、正規現役
    archived_skills = [s for s in all_skill_records if s["is_archived"]]
    active_skills = [s for s in all_skill_records if not s["is_archived"] and not s["is_backup"]]
    backup_skills = [s for s in skill_files if s.name.startswith("SKILL_") and s.name.endswith(".md")]

    # 3. 執行全域審計
    audit_res = audit_skills_and_data(
        active_skills,
        backup_skills,
        data_files,
        residual_artifacts,
        scan_root
    )

    # 4. 產出 SKILL_MAP.md
    map_output_path = scan_root / "SKILL_MAP.md"
    generate_skill_map(active_skills, mirror_skill_count, len(archived_skills), map_output_path)
    print(f"✅ 成功產出技能全景地圖：{map_output_path.name}")

    # 5. 產出 SKILL_ISSUES.md
    issues_output_path = scan_root / "SKILL_ISSUES.md"
    generate_skill_issues(audit_res, mirror_skill_count, len(archived_skills), issues_output_path)
    print(f"✅ 成功產出架構與規範合規報告：{issues_output_path.name}\n")

    # 6. 終端匯報
    rc = audit_res["rule_counts"]
    total = audit_res["total_active_skills"]
    compliant = audit_res["fully_compliant_count"]

    print("=" * 70)
    print("📊【《00-00 極星格式規範 v1.0》合規掃描總結】")
    print(f"  • 現役技能總數 (Active Skills)     : {total} 份（排除鏡像 {mirror_skill_count} 份、封存 {len(archived_skills)} 份）")
    print(f"  • 完全合規技能數 (0 錯誤 0 提醒)  : {compliant} / {total} ({compliant/total*100:.1f}%)")
    print(f"  • 零嚴重錯誤技能數 (0 錯誤)       : {audit_res['zero_error_count']} / {total} ({audit_res['zero_error_count']/total*100:.1f}%)")
    print("----------------------------------------------------------------------")
    print("🚨【❌ 嚴重錯誤 (Errors) 統計】")
    print(f"  [E1] 缺少 name 或 description              : {rc['E1_missing_name_or_desc']}")
    print(f"  [E2] name 格式非法 (只能小寫/數字/-, <=64)  : {rc['E2_invalid_name_format']}")
    print(f"  [E3] name 與所在資料夾名稱不一致            : {rc['E3_name_folder_mismatch']}")
    print(f"  [E4] description 超過 1024 字元            : {rc['E4_desc_over_1024']}")
    print(f"  [E5] metadata.status 非 active/draft/archived: {rc['E5_invalid_status']}")
    print(f"  [E6] active 缺少 evidence 或憑證檔案不存在   : {rc['E6_invalid_evidence']}")
    print(f"  [E7] atom-* 缺少 metadata.group 或 parent   : {rc['E7_atom_missing_group_or_parent']}")
    print(f"  [E8] 舊版 SKILL_*.md 滯留於非封存目錄      : {rc['E8_backup_outside_archive']}")
    print(f"  [E9] 非 UTF-8 資料檔 (.md/.txt/.json/.py)   : {rc['E9_non_utf8_data']}")
    print("----------------------------------------------------------------------")
    print("⚠️【⚠️ 格式提醒 (Warnings) 統計】")
    print(f"  [W1] description 超過 200 字 (建議精簡)      : {rc['W1_desc_over_200']}")
    print(f"  [W2] 缺少 metadata.owner 或 metadata.version : {rc['W2_missing_owner_or_version']}")
    print(f"  [W3] frontmatter 最外層有自訂欄位待搬遷     : {rc['W3_extra_top_level_fields']}")
    print(f"  [W4] SKILL.md 超過 500 行 (建議拆分理論)     : {rc['W4_lines_over_500']}")
    print(f"  [W5] 工作資料夾殘留垃圾 (.bak/.pyc/快取)     : {rc['W5_residual_artifacts']}")
    print("======================================================================")
    print("🎉 掃描盤點與規範審計順利完成！Exit Code 0。\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
