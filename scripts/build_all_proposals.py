#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_all_proposals.py
======================================================================
極星全內閣其餘 10 個技能組標準化重構與批次提案生成引擎
======================================================================
遵循《00-00 極星格式規範 v1.1》：
1. 嚴格落實「只搬家、不刪除」原則（母體刪除之規則 100% 搬入對應 atom）。
2. frontmatter 完整合規（name、description <= 200 字動詞開頭、metadata: group, parent, owner, status: draft, version: "1.0"）。
3. atom 的 description 結尾強制加上「只由 XX 呼叫，不單獨使用。」
4. 選品審計母體不新建，atom parent 填「待品碩決定」。
5. 所有因格式改版產生的 < 0.6 刪除行，自動提取並記錄至 scripts/rule_diff_allowlist.txt 標註「待品碩核准」。
6. 逐組執行 rule_diff_check.py 與 skill_scanner.py，輸出統計報表。
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

# 定義 10 個技能組規格
GROUPS_CONFIG = [
    {
        'group_name': '5D定價',
        'parent_name': 'polaris-5d-pricing-engine',
        'parent_owner': '算盤',
        'parent_orig': Path('.agents/skills/polaris-5d-pricing-engine/SKILL.md'),
        'parent_desc': '精算商業價值、專案成果、數位資產與勞務成本時間矩陣。在需要為服務或專案制定防禦型報價與條款時使用；單純查詢歷史報價時不用。',
        'atoms': [
            {
                'name': 'atom-pricing-5d-calculator',
                'orig': Path('.agents/skills/atoms/atom-pricing-5d-calculator/SKILL.md'),
                'owner': '算盤',
                'desc': '校準 D1 到 D5 價值係數並精算勞務、成果與資產模態定價。在 5D 矩陣數值試算與風控審核時使用；草擬合約條款時不用。只由 polaris-5d-pricing-engine 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-pricing-bulletproof-clause',
                'orig': Path('.agents/skills/atoms/atom-pricing-bulletproof-clause/SKILL.md'),
                'owner': '算盤',
                'desc': '裝配防彈衣四大鐵律條款、超時加收通知與高情商溝通話術。在合約條款草擬、現場等候超時或客戶嫌貴時使用；數值純計算時不用。只由 polaris-5d-pricing-engine 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '做短影音',
        'parent_name': 'polaris-motion-reels',
        'parent_owner': '影',
        'parent_orig': Path('.agents/skills/polaris-motion-reels/SKILL.md'),
        'parent_desc': '合成靜態圖文為具備運鏡緩動與動態字卡之直式短影音。在產出生鮮食材、日常工作隨手拍短影音時使用；單純發布靜態圖文時不用。',
        'atoms': [
            {
                'name': 'atom-motion-camera-engine',
                'orig': Path('.agents/skills/atoms/atom-motion-camera-engine/SKILL.md'),
                'owner': '約瑟夫',
                'desc': '精算電影級運鏡軌跡、平滑緩動曲線與視差逐幀渲染。在微動態短影音運鏡設計與 MP4 編碼輸出時使用；安全區排版時不用。只由 polaris-motion-reels 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-motion-overlay-safezone',
                'orig': Path('.agents/skills/atoms/atom-motion-overlay-safezone/SKILL.md'),
                'owner': '約瑟夫',
                'desc': '精算社群 UI 安全邊界避讓、防眩暗角覆層與字幕時間軸。在短影音覆層合成與字幕動態排版時使用；鏡頭運鏡計算時不用。只由 polaris-motion-reels 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '發臉書',
        'parent_name': 'facebook-publisher',
        'parent_owner': '林納斯',
        'parent_orig': Path('.agents/skills/facebook-publisher/SKILL.md'),
        'parent_desc': '派發與排程圖文貼文至官方臉書粉絲專頁。在確認文案與圖片合格並準備推播發布時使用；撰寫行銷文案階段不用。',
        'atoms': [
            {
                'name': 'atom-fb-preflight-gate',
                'orig': Path('.agents/skills/atoms/atom-fb-preflight-gate/SKILL.md'),
                'owner': '戴明',
                'desc': '審查臉書內文零外部連結、抽離第一留言導流與品牌紅線。在臉書發布前防降權質檢與排程窗口驗證時使用；API 實際推送時不用。只由 facebook-publisher 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-fb-feed-dispatcher',
                'orig': Path('.agents/skills/atoms/atom-fb-feed-dispatcher/SKILL.md'),
                'owner': '林納斯',
                'desc': '上傳多圖暫存池、組合貼文矩陣並執行即時或排程發布。在貼文通過安燈質檢後派發與第一留言秒發時使用；貼文內容質檢時不用。只由 facebook-publisher 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '商品化',
        'parent_name': 'polaris-productization-master',
        'parent_owner': '雪',
        'parent_orig': Path('.agents/skills/polaris-productization-master/SKILL.md'),
        'parent_desc': '封裝非標業務為 SOP、規格手冊與文案話術三合一套版。在新業務、服務或選品準備標準化落地時使用；日常重複性派工時不用。',
        'atoms': [
            {
                'name': 'atom-product-trio-scaffolder',
                'orig': Path('.agents/skills/atoms/atom-product-trio-scaffolder/SKILL.md'),
                'owner': '雪',
                'desc': '自動裝配三合一交付套版物理檔案與結構化規格骨架。在新業務初始化裝配 SOP 與手冊時使用；出廠前黑臉審查時不用。只由 polaris-productization-master 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-product-redteam-audit',
                'orig': Path('.agents/skills/atoms/atom-product-redteam-audit/SKILL.md'),
                'owner': '戴明',
                'desc': '執行四方黑臉交叉審查與戴明防呆安燈出廠驗收。在三合一交付套版完稿準備發布前審核時使用；初稿骨架裝配時不用。只由 polaris-productization-master 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '客戶端抗逆',
        'parent_name': 'polaris-client-architect',
        'parent_owner': '尼奧',
        'parent_orig': Path('.agents/skills/polaris-client-architect/SKILL.md'),
        'parent_desc': '建構前端極限抗逆架構、離線心跳與斷線隊列重放機制。在開發與架構 WebApp、PWA 與 LIFF 客戶端時使用；後端伺服器運維時不用。',
        'atoms': [
            {
                'name': 'atom-client-offline-heartbeat',
                'orig': Path('.agents/skills/atoms/atom-client-offline-heartbeat/SKILL.md'),
                'owner': '尼奧',
                'desc': '生成離線 Service Worker 心跳、本地優先存證與雙層快取。在前端建立離線韌性與本地存證機制時使用；網路傳輸隊列重放時不用。只由 polaris-client-architect 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-client-resilient-transport',
                'orig': Path('.agents/skills/atoms/atom-client-resilient-transport/SKILL.md'),
                'owner': '林納斯',
                'desc': '管理極限弱網傳輸、離線待發隊列與冪等靜默重放狀態機。在暴雨弱網斷線排隊與網路恢復依序上傳時使用；本地 UI 渲染時不用。只由 polaris-client-architect 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '生活管家',
        'parent_name': 'lifebutler-care-artisan',
        'parent_owner': '雪',
        'parent_orig': Path('.agents/skills/lifebutler-care-artisan/SKILL.md'),
        'parent_desc': '封裝高齡孝親與安居生活服務為標準工單與安心圖卡。在接收外地兒女委託或在地長輩照護需求時使用；一般商業選品銷售時不用。',
        'atoms': [
            {
                'name': 'atom-care-order-dispatcher',
                'orig': Path('.agents/skills/atoms/atom-care-order-dispatcher/SKILL.md'),
                'owner': '雪',
                'desc': '封裝五大孝親旗艦模組工單、5D 定價與裝備檢核派工。在產生標準派工單、成本試算與 3PL 排程時使用；繪製兒女安心圖卡時不用。只由 lifebutler-care-artisan 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-care-telehealth-card',
                'orig': Path('.agents/skills/atoms/atom-care-telehealth-card/SKILL.md'),
                'owner': '約瑟夫',
                'desc': '生成瑞士網格外地兒女 3 分鐘安心聽診圖卡與醫囑速記。在長輩陪診或巡檢完畢回報家屬時使用；服務前派工排程時不用。只由 lifebutler-care-artisan 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '開課營運',
        'parent_name': 'polaris-course-master',
        'parent_owner': '雪',
        'parent_orig': Path('.agents/skills/polaris-course-master/SKILL.md'),
        'parent_desc': '封裝實體小班工作坊教案規格、報名表單與履約通知。在籌辦 AI 或營運工作坊並執行招生履約時使用；一般社群發文時不用。',
        'atoms': [
            {
                'name': 'atom-course-syllabus-scaffolder',
                'orig': Path('.agents/skills/atoms/atom-course-syllabus-scaffolder/SKILL.md'),
                'owner': '雪',
                'desc': '裝配實體小班工作坊 4 大硬參數、雙核課綱與 10 題防呆表單。在工作坊開課規格規劃與建表時使用；報名名冊審查與分流時不用。只由 polaris-course-master 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-course-enrollment-pipeline',
                'orig': Path('.agents/skills/atoms/atom-course-enrollment-pipeline/SKILL.md'),
                'owner': '雪',
                'desc': '審查名額三軌分流、發送日曆邀請、24h RSVP 點名與現場驗收。在學員報名後名額調度與課前課後履約時使用；初期課綱規劃時不用。只由 polaris-course-master 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '飛輪總控',
        'parent_name': 'polaris-flywheel-orchestrator',
        'parent_owner': '雪',
        'parent_orig': Path('.agents/skills/polaris-flywheel-orchestrator/SKILL.md'),
        'parent_desc': '解析全域商業需求意圖、智慧路由流水線並組裝決策卡。在接收外部未修飾需求並啟動跨內閣作業時使用；單一業務專項執行時不用。',
        'atoms': [
            {
                'name': 'atom-flywheel-event-router',
                'orig': Path('.agents/skills/atoms/atom-flywheel-event-router/SKILL.md'),
                'owner': '雪',
                'desc': '解析全域業務事件意圖並路由至四大作戰動脈流水線。在需求傳入時進行語義解析與流水線分派時使用；決策卡組裝審批時不用。只由 polaris-flywheel-orchestrator 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-flywheel-launch-cockpit',
                'orig': Path('.agents/skills/atoms/atom-flywheel-launch-cockpit/SKILL.md'),
                'owner': '雪',
                'desc': '組裝 3 秒極簡決策卡、審核安燈質檢並執行一鍵發射。在流水線成果完成準備呈報創辦人審批時使用；初期意圖分發時不用。只由 polaris-flywheel-orchestrator 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '選品審計',
        'parent_name': None, # 不存在，先不新建
        'parent_owner': None,
        'parent_orig': None,
        'parent_desc': None,
        'atoms': [
            {
                'name': 'atom-supplychain-layer-deconstructor',
                'orig': Path('.agents/skills/atoms/atom-supplychain-layer-deconstructor/SKILL.md'),
                'owner': '算盤',
                'desc': '精算供應鏈四層毛利倒推模型、產地出貨價與虛報溢價率。在供應商批發報價成本審計時使用；談判心理攻防時不用。只由 待品碩決定 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-supplychain-tactical-negotiator',
                'orig': Path('.agents/skills/atoms/atom-supplychain-tactical-negotiator/SKILL.md'),
                'owner': '雪柔',
                'desc': '預判盤商操盤手心理動機並產出高情商議價籌碼話術。在掌握底牌數據後進行供應商商務談判時使用；底層純數值拆解時不用。只由 待品碩決定 呼叫，不單獨使用。'
            }
        ]
    },
    {
        'group_name': '選品行銷',
        'parent_name': 'sharp-groupbuy-analyzer',
        'parent_owner': '泰勒絲',
        'parent_orig': Path('C:/Users/lenovo/.gemini/config/skills/sharp-groupbuy-analyzer/SKILL.md'),
        'parent_desc': '執行利刃商品七步分析、逆推上游成本與產出喵編社群圖文。在取得商品照片進行選品調研與行銷企劃時使用；非實體商品專案時不用。',
        'atoms': [
            {
                'name': 'atom-groupbuy-cost-auditor',
                'orig': Path('.agents/skills/atoms/atom-groupbuy-cost-auditor/SKILL.md'),
                'owner': '算盤',
                'desc': '逆推商品產地出貨價、大宗冷鏈耗損摩擦並排查食安合規。在選品初期成本逆推與供應商背調時使用；社群文案折射時不用。只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。'
            },
            {
                'name': 'atom-groupbuy-four-prism-copy',
                'orig': Path('.agents/skills/atoms/atom-groupbuy-four-prism-copy/SKILL.md'),
                'owner': '泰勒絲',
                'desc': '折射喵編人設四大面向選品文案、商城精簡規格與禁語過濾。在選品定價確立後產出社群圖文文案時使用；上游成本逆推時不用。只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。'
            }
        ]
    }
]

def clean_text_for_shingles(text: str) -> str:
    norm = re.sub(r'\\text\{([a-zA-Z%]+)\}', r'\1', text)
    norm = norm.replace(r'^\circ', '°').replace(r'\circ', '°')
    return re.sub(r'[\s\W_]+', '', norm)

def main():
    print("=" * 75)
    print("🚀 極星全內閣其餘 10 個技能組批次提案生成與驗收引擎")
    print("=" * 75)

    allowlist_path = Path("scripts/rule_diff_allowlist.txt")
    allowlist_content = allowlist_path.read_text(encoding="utf-8") if allowlist_path.exists() else ""
    new_pending_allowlist_entries = []

    # 針對每一組產生提案檔案
    results_table = []

    for g in GROUPS_CONFIG:
        g_name = g['group_name']
        print(f"\n📦【正在處理技能組：{g_name}】")
        target_dir = Path(f"_proposed/{g_name}")
        target_dir.mkdir(parents=True, exist_ok=True)

        orig_files = []
        prop_files = []

        # 1. 處理母體（如果存在）
        if g['parent_name'] and g['parent_orig'] and g['parent_orig'].exists():
            orig_files.append(str(g['parent_orig']))
            parent_raw = g['parent_orig'].read_text(encoding='utf-8')
            parent_orig_lines = len(parent_raw.splitlines())

            # 產生符合 v1.1 規範的母體 SKILL.md
            # 建立 atom 呼叫順序段落
            atom_seq_md = "## 🧩 所屬原子技能與調用順序 (Atom Sequence)\n\n"
            atom_seq_md += "本母體按以下先後順序協同原子技能完成全閉環運作：\n\n"
            for idx, a in enumerate(g['atoms'], 1):
                atom_seq_md += f"{idx}. **執行 `{a['name']}`**：負責 {a['desc'].split('。')[0]}。\n"
            atom_seq_md += "\n---\n\n"

            # 替換 frontmatter
            frontmatter_clean = f"""---
name: {g['parent_name']}
description: {g['parent_desc']}
metadata:
  group: {g_name}
  owner: {g['parent_owner']}
  status: draft
  version: "1.0"
---
"""
            # 擷取原始內文（去掉原始 frontmatter）
            body_parts = parent_raw.split('---', 2)
            orig_body = body_parts[2] if len(body_parts) >= 3 else parent_raw

            # 插入 atom 調用順序在第一章或標題之後
            if "# " in orig_body:
                header_idx = orig_body.find("\n---\n")
                if header_idx != -1:
                    new_body = orig_body[:header_idx + 5] + "\n" + atom_seq_md + orig_body[header_idx + 5:]
                else:
                    new_body = atom_seq_md + orig_body
            else:
                new_body = atom_seq_md + orig_body

            parent_prop_dir = target_dir / g['parent_name']
            parent_prop_dir.mkdir(parents=True, exist_ok=True)
            parent_prop_file = parent_prop_dir / "SKILL.md"
            parent_prop_file.write_text(frontmatter_clean + "\n" + new_body.strip() + "\n", encoding='utf-8')
            prop_files.append(str(parent_prop_file))

            parent_new_lines = len(parent_prop_file.read_text(encoding='utf-8').splitlines())
            parent_lines_str = f"{parent_orig_lines} → {parent_new_lines}"
        else:
            parent_lines_str = "不存在（無母體）"

        # 2. 處理 Atoms
        for a in g['atoms']:
            orig_files.append(str(a['orig']))
            atom_raw = a['orig'].read_text(encoding='utf-8')

            # 建立符合 v1.1 的 frontmatter
            parent_val = g['parent_name'] if g['parent_name'] else "待品碩決定"
            atom_fm = f"""---
name: {a['name']}
description: {a['desc']}
metadata:
  group: {g_name}
  parent: {parent_val}
  owner: {a['owner']}
  status: draft
  version: "1.0"
---
"""
            # 擷取原始內文（去掉原始 frontmatter 與舊版所屬技能組引言）
            atom_parts = atom_raw.split('---', 2)
            atom_body = atom_parts[2] if len(atom_parts) >= 3 else atom_raw
            # 清理舊版引言行
            cleaned_atom_body_lines = []
            for line in atom_body.splitlines():
                if line.strip().startswith("> **所屬技能組**：") or line.strip().startswith("> **原技能母體**："):
                    continue
                cleaned_atom_body_lines.append(line)
            atom_body_cleaned = "\n".join(cleaned_atom_body_lines).strip()

            atom_prop_dir = target_dir / a['name']
            atom_prop_dir.mkdir(parents=True, exist_ok=True)
            atom_prop_file = atom_prop_dir / "SKILL.md"
            atom_prop_file.write_text(atom_fm + "\n" + atom_body_cleaned + "\n", encoding='utf-8')
            prop_files.append(str(atom_prop_file))

        # 3. 比對檢驗並收集所有需要進入 allowlist 的行
        # 合併提案文字
        prop_text_combined = "\n".join(Path(p).read_text(encoding='utf-8') for p in prop_files)
        prop_clean_all = clean_text_for_shingles(prop_text_combined)

        group_pending_lines = []
        for orig_p in orig_files:
            orig_path_obj = Path(orig_p)
            lines = orig_path_obj.read_text(encoding='utf-8').splitlines()
            for idx, line in enumerate(lines, 1):
                cl = clean_text_for_shingles(line)
                if len(cl) >= 12:
                    shingles = [cl[i:i+4] for i in range(len(cl) - 3)]
                    matches = sum(1 for s in shingles if s in prop_clean_all)
                    ratio = matches / len(shingles) if shingles else 1.0
                    if ratio < 0.6:
                        # 檢查是否已在 allowlist 中
                        clean_target = cl
                        if not any(clean_target in clean_text_for_shingles(al) for al in allowlist_content.splitlines() if al.strip()):
                            entry = f"[{orig_path_obj.name}:L{idx}] {line.strip()} | 待品碩核准（依《格式規範》v1.1 標準化改寫/改由 metadata 呈現）"
                            group_pending_lines.append(entry)
                            new_pending_allowlist_entries.append(entry)

        # 4. 執行 rule_diff_check.py (帶入參數)
        cmd_diff = ["python", "scripts/rule_diff_check.py", "--orig"] + orig_files + ["--prop"] + prop_files
        res_diff = subprocess.run(cmd_diff, capture_output=True, text=True, encoding='utf-8')
        diff_code = res_diff.returncode

        # 5. 執行 skill_scanner.py 對該組提案掃描
        cmd_scan = ["python", "scripts/skill_scanner.py", str(target_dir)]
        res_scan = subprocess.run(cmd_scan, capture_output=True, text=True, encoding='utf-8')
        # 解析 scanner 錯誤數
        error_count = 0
        warning_count = 0
        for out_line in res_scan.stdout.splitlines():
            if "[E" in out_line and ":" in out_line:
                val = out_line.split(":")[-1].strip()
                if val.isdigit():
                    error_count += int(val)
            if "[W" in out_line and ":" in out_line:
                val = out_line.split(":")[-1].strip()
                if val.isdigit():
                    warning_count += int(val)

        results_table.append({
            'group_name': g_name,
            'lines_change': parent_lines_str,
            'diff_code': diff_code,
            'pending_allowlist_count': len(group_pending_lines),
            'scanner_errors': error_count,
            'scanner_warnings': warning_count
        })

    # 將新的待核准條目追加至 scripts/rule_diff_allowlist.txt
    if new_pending_allowlist_entries:
        with open("scripts/rule_diff_allowlist.txt", "a", encoding="utf-8") as f:
            f.write("\n# --- 批次提案新增待核准條目 (Pending Founder Approval) ---\n")
            for entry in new_pending_allowlist_entries:
                f.write(entry + "\n")
        print(f"\n📝 已成功將 {len(new_pending_allowlist_entries)} 條格式修改行追加寫入 scripts/rule_diff_allowlist.txt 標註「待品碩核准」。")

    print("\n" + "=" * 75)
    print("📊【其餘 10 個技能組批次提案驗收總表】")
    print("=" * 75)
    header = "組名 | 母體行數 前→後 | rule_diff_check 結果 | 待核准 allowlist 條數 | scanner 錯誤數"
    print(header)
    print("-" * len(header))
    for r in results_table:
        diff_res_str = f"Exit Code {r['diff_code']}" + (" (待審批熔斷)" if r['diff_code'] == 1 and r['pending_allowlist_count'] > 0 else "")
        print(f"{r['group_name']} | {r['lines_change']} | {diff_res_str} | {r['pending_allowlist_count']} | {r['scanner_errors']}")

    print("=" * 75)

if __name__ == "__main__":
    main()
