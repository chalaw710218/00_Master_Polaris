# -*- coding: utf-8 -*-
"""
scripts/execute_write_step5.py
執行第 5 步技能組正式寫入：
1. 針對 9 組技能中每一份正式 SKILL.md，備份至同層 _archive/SKILL_20261126_規範前.md
2. 備份檔內若有明文 Token，全面脫敏為 [REDACTED_FB_PAGE_TOKEN]
3. 用 _proposed/ 下的新版取代正式檔案
4. sharp-groupbuy-analyzer 與 facebook-publisher 寫回 00-02 原位置，facebook-publisher 同步寫回 .agents/skills/
5. 將 _proposed/ 下的 9 個組別資料夾移至 _proposed/_done/
"""

import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(".")
PROPOSED_DIR = BASE_DIR / "_proposed"
DONE_DIR = PROPOSED_DIR / "_done"
DONE_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_PATTERN = re.compile(r"EAA[0-9a-zA-Z]{30,}")

# 定義 9 組提案與正式路徑的映射
# 格式: (組別目錄名, 技能名稱, [正式 SKILL.md 路徑清單])
TARGET_MAPPINGS = [
    # 5D定價
    ("5D定價", "atom-pricing-5d-calculator", [Path(".agents/skills/atoms/atom-pricing-5d-calculator/SKILL.md")]),
    ("5D定價", "atom-pricing-bulletproof-clause", [Path(".agents/skills/atoms/atom-pricing-bulletproof-clause/SKILL.md")]),
    ("5D定價", "polaris-5d-pricing-engine", [Path(".agents/skills/polaris-5d-pricing-engine/SKILL.md")]),

    # 做短影音
    ("做短影音", "atom-motion-camera-engine", [Path(".agents/skills/atoms/atom-motion-camera-engine/SKILL.md")]),
    ("做短影音", "atom-motion-overlay-safezone", [Path(".agents/skills/atoms/atom-motion-overlay-safezone/SKILL.md")]),
    ("做短影音", "polaris-motion-reels", [Path(".agents/skills/polaris-motion-reels/SKILL.md")]),

    # 商品化
    ("商品化", "atom-product-redteam-audit", [Path(".agents/skills/atoms/atom-product-redteam-audit/SKILL.md")]),
    ("商品化", "atom-product-trio-scaffolder", [Path(".agents/skills/atoms/atom-product-trio-scaffolder/SKILL.md")]),
    ("商品化", "polaris-productization-master", [Path(".agents/skills/polaris-productization-master/SKILL.md")]),

    # 客戶端抗逆
    ("客戶端抗逆", "atom-client-offline-heartbeat", [Path(".agents/skills/atoms/atom-client-offline-heartbeat/SKILL.md")]),
    ("客戶端抗逆", "atom-client-resilient-transport", [Path(".agents/skills/atoms/atom-client-resilient-transport/SKILL.md")]),
    ("客戶端抗逆", "polaris-client-architect", [Path(".agents/skills/polaris-client-architect/SKILL.md")]),

    # 生活管家
    ("生活管家", "atom-care-order-dispatcher", [Path(".agents/skills/atoms/atom-care-order-dispatcher/SKILL.md")]),
    ("生活管家", "atom-care-telehealth-card", [Path(".agents/skills/atoms/atom-care-telehealth-card/SKILL.md")]),
    ("生活管家", "lifebutler-care-artisan", [Path(".agents/skills/lifebutler-care-artisan/SKILL.md")]),

    # 發臉書
    ("發臉書", "atom-fb-feed-dispatcher", [Path(".agents/skills/atoms/atom-fb-feed-dispatcher/SKILL.md")]),
    ("發臉書", "atom-fb-preflight-gate", [Path(".agents/skills/atoms/atom-fb-preflight-gate/SKILL.md")]),
    ("發臉書", "facebook-publisher", [
        Path("00-02_GroupBuy_Products/.agents/skills/facebook-publisher/SKILL.md"),
        Path(".agents/skills/facebook-publisher/SKILL.md")
    ]),

    # 管家選品
    ("管家選品", "atom-groupbuy-cost-auditor", [Path(".agents/skills/atoms/atom-groupbuy-cost-auditor/SKILL.md")]),
    ("管家選品", "atom-groupbuy-four-prism-copy", [Path(".agents/skills/atoms/atom-groupbuy-four-prism-copy/SKILL.md")]),
    ("管家選品", "atom-supplychain-layer-deconstructor", [Path(".agents/skills/atoms/atom-supplychain-layer-deconstructor/SKILL.md")]),
    ("管家選品", "atom-supplychain-tactical-negotiator", [Path(".agents/skills/atoms/atom-supplychain-tactical-negotiator/SKILL.md")]),
    ("管家選品", "sharp-groupbuy-analyzer", [Path("00-02_GroupBuy_Products/.agents/skills/sharp-groupbuy-analyzer/SKILL.md")]),

    # 開課營運
    ("開課營運", "atom-course-enrollment-pipeline", [Path(".agents/skills/atoms/atom-course-enrollment-pipeline/SKILL.md")]),
    ("開課營運", "atom-course-syllabus-scaffolder", [Path(".agents/skills/atoms/atom-course-syllabus-scaffolder/SKILL.md")]),
    ("開課營運", "polaris-course-master", [Path(".agents/skills/polaris-course-master/SKILL.md")]),

    # 飛輪總控
    ("飛輪總控", "atom-flywheel-event-router", [Path(".agents/skills/atoms/atom-flywheel-event-router/SKILL.md")]),
    ("飛輪總控", "atom-flywheel-launch-cockpit", [Path(".agents/skills/atoms/atom-flywheel-launch-cockpit/SKILL.md")]),
    ("飛輪總控", "polaris-flywheel-orchestrator", [Path(".agents/skills/polaris-flywheel-orchestrator/SKILL.md")]),
]

def remove_readonly(func, path, excinfo):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

print("🚀 開始執行第 5 步技能正式寫入...")
written_count = 0
archived_count = 0

for group_name, skill_name, target_paths in TARGET_MAPPINGS:
    prop_skill_md = PROPOSED_DIR / group_name / skill_name / "SKILL.md"
    if not prop_skill_md.exists():
        print(f"❌ 找不到提案檔案：{prop_skill_md}")
        continue
    
    new_content = prop_skill_md.read_text(encoding="utf-8")
    
    for target_path in target_paths:
        # 1. 備份現有檔案至同層 _archive/SKILL_20261126_規範前.md
        if target_path.exists():
            archive_dir = target_path.parent / "_archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            archive_file = archive_dir / "SKILL_20261126_規範前.md"
            
            orig_content = target_path.read_text(encoding="utf-8")
            # 2. 封存檔中若有明文 Token，全面脫敏為 [REDACTED_FB_PAGE_TOKEN]
            sanitized_orig = TOKEN_PATTERN.sub("[REDACTED_FB_PAGE_TOKEN]", orig_content)
            archive_file.write_text(sanitized_orig, encoding="utf-8")
            archived_count += 1
            print(f"  📦 已備份脫敏存檔: {archive_file}")
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 3. 寫入新版檔案
        target_path.write_text(new_content, encoding="utf-8")
        written_count += 1
        print(f"  ✍️ 已成功寫入正式檔: {target_path}")

print(f"\n✅ 檔案寫入完成：共備份 {archived_count} 份，成功寫入 {written_count} 份正式檔。")

# 4. 遷移完成之提案目錄至 _proposed/_done/
groups_to_move = [
    "5D定價", "做短影音", "商品化", "客戶端抗逆", "生活管家",
    "發臉書", "管家選品", "開課營運", "飛輪總控"
]

print("\n📦 開始將已完成提案遷移至 _proposed/_done/...")
for g in groups_to_move:
    src_dir = PROPOSED_DIR / g
    dst_dir = DONE_DIR / g
    if src_dir.exists():
        if dst_dir.exists():
            shutil.rmtree(dst_dir, onerror=remove_readonly)
        shutil.move(str(src_dir), str(dst_dir))
        print(f"  🚚 已遷移: {g} -> _proposed/_done/{g}")

print("\n🎉 第 5 步正式寫入與歸檔遷移全部圓滿完成！")
