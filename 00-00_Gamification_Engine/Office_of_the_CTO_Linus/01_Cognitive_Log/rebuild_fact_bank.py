#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_fact_bank.py — 依據反查表動態重建林納斯經驗事實庫與未驗證封存
"""

import sys
import re
from pathlib import Path

def clean_title(title: str, no_src_str: str, row_id: int) -> str:
    # 建立刪除清單：從反查表「沒出處的數字」欄位提取
    to_remove = [x.strip() for x in re.split(r'[,，、;；]', no_src_str) if x.strip() and x.strip() != '無']

    # 針對特定標題中未有出處之性能數字補全（例如 82 條的 5 GB/s、101 條的 1ms）
    if row_id == 82 and '5 GB/s' not in to_remove:
        to_remove.append('5 GB/s')
    if row_id == 101 and '1ms' not in to_remove:
        to_remove.append('1ms')

    # 按長度倒序排列，優先替換長詞，防止短字串破壞子結構
    to_remove.sort(key=len, reverse=True)

    cleaned = title
    for item in to_remove:
        if item in cleaned:
            cleaned = cleaned.replace(item, '')

    # 清理空括號
    cleaned = re.sub(r'\(\s*\)', '', cleaned)
    cleaned = re.sub(r'（\s*）', '', cleaned)

    # 整理多餘空格與中文間空隙
    cleaned = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()

    # 清理句尾或句首留下的連接詞、動詞與標點（如「與」「突破」等）
    changed = True
    while changed:
        before = cleaned
        cleaned = re.sub(r'[與和及突破\s]+$', '', cleaned).strip()
        cleaned = re.sub(r'^[與和及\s]+', '', cleaned).strip()
        cleaned = re.sub(r'\(\s+', '(', cleaned)
        cleaned = re.sub(r'\s+\)', ')', cleaned)
        cleaned = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', cleaned)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
        if cleaned == before:
            changed = False

    return cleaned

def rebuild():
    dir_path = Path(__file__).resolve().parent

    tables = [
        '反查表_C01-10.md', '反查表_C11-30.md', '反查表_C31-60.md', '反查表_C61-90.md',
        '反查表_C91-120.md', '反查表_C121-150.md', '反查表_C151-180.md', '反查表_C181-210.md'
    ]

    items = []
    for t in tables:
        p = dir_path / t
        if not p.exists():
            print(f"錯誤：找不到檔案 {p}", file=sys.stderr)
            sys.exit(1)

        lines = p.read_text(encoding='utf-8').splitlines()
        header_found = False
        col_idx = {}
        for line in lines:
            line = line.strip()
            if not line.startswith('|') or not line.endswith('|'):
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not cells:
                continue
            if '編號' in cells:
                header_found = True
                for i, c in enumerate(cells):
                    col_idx[c] = i
                continue
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
            if not header_found:
                continue

            row_id_str = cells[col_idx.get('編號', 0)]
            if not row_id_str.isdigit():
                continue
            row_id = int(row_id_str)

            text_col = col_idx.get('原文摘要', col_idx.get('事實陳述', 1))
            tag_col = col_idx.get('標記', col_idx.get('標籤', 2))
            url_col = col_idx.get('網址', 3)
            quote_col = col_idx.get('逐字原句', col_idx.get('摘句原文', 4))
            no_src_col = 5 if len(cells) > 5 else None

            items.append({
                'id': row_id,
                'text': cells[text_col],
                'tag': cells[tag_col],
                'url': cells[url_col],
                'quote': cells[quote_col],
                'no_src': cells[no_src_col] if no_src_col is not None else ''
            })

    # 讀取備份原檔，用於封存時保留完整原文段落
    orig_backup = dir_path / '01_Experiences_and_Evidence_原檔備份_20261122.md'
    orig_dict = {}
    if orig_backup.exists():
        orig_text = orig_backup.read_text(encoding='utf-8')
        curr = 0
        for l in orig_text.splitlines():
            m = re.match(r'^\s*(\d+)\.\s*(.+)$', l)
            if m:
                curr += 1
                orig_dict[curr] = m.group(2)

    # 分類：
    # 移進封存：所有標【未驗證】的條目，再加上第 7、67、75 條（品碩決定不保留）
    # 留下：其他條目
    archive = []
    keep = []

    for item in items:
        if '未驗證' in item['tag'] or item['id'] in [7, 67, 75]:
            archive.append(item)
        else:
            keep.append(item)

    no_url = [item for item in keep if not item['url'] or item['url'] == '無']

    # 嚴格數字檢查：留下必須剛好 145、封存剛好 65、合計 210、沒有網址的 0
    # 任何一項不符就印 FAIL，exit code 1，而且不寫入任何檔案
    if len(keep) != 145 or len(archive) != 65 or (len(keep) + len(archive) != 210) or len(no_url) != 0:
        print(f"留下：{len(keep)} 條")
        print(f"封存：{len(archive)} 條")
        print(f"合計：{len(keep) + len(archive)} 條")
        print(f"留下的條目中沒有網址的：{len(no_url)} 條")
        print("FAIL")
        sys.exit(1)

    # 1. 寫入新事實庫 01_Experiences_and_Evidence.md
    fact_bank_path = dir_path / '01_Experiences_and_Evidence.md'
    fact_lines = [
        "> 2026-11-22 依反查表重建：只保留有網址和逐字原句的知識。"
    ]

    for it in keep:
        raw_text = it['text']
        parts = re.split(r'[:：]', raw_text, maxsplit=1)
        orig_title = parts[0].strip()
        orig_title = re.sub(r'^\*\*(.+?)\*\*$', r'\1', orig_title).strip()
        final_title = clean_title(orig_title, it['no_src'], it['id'])
        line = f"{it['id']}. {final_title}：「{it['quote']}」｜出處：{it['url']}"
        fact_lines.append(line)

    fact_bank_path.write_text('\n'.join(fact_lines) + '\n', encoding='utf-8')

    # 2. 寫入封存 _未驗證封存.md
    archive_path = dir_path / '_未驗證封存.md'
    archive_lines = [
        "> 封存：不刪除、不可引用。"
    ]

    for it in archive:
        full_text = orig_dict.get(it['id'], it['text'])
        line = f"{it['id']}. {full_text}"
        archive_lines.append(line)

    archive_path.write_text('\n'.join(archive_lines) + '\n', encoding='utf-8')

    # 3. 輸出執行結果最後行
    print("=== 重建事實庫成功 ===")
    print(f"留下：{len(keep)} 條")
    print(f"封存：{len(archive)} 條")
    print(f"合計：{len(keep) + len(archive)} 條")
    print(f"留下的條目中沒有網址的：{len(no_url)} 條")

if __name__ == '__main__':
    rebuild()
