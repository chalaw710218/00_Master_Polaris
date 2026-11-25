import os
from pathlib import Path

groups = {
    '5d_pricing': {
        'title': '5D 定價',
        'dir_name': '5d_pricing',
        'parent_name': 'polaris-5d-pricing-engine',
        'atoms': ['atom-pricing-bulletproof-clause', 'atom-pricing-5d-calculator']
    },
    'motion_reels': {
        'title': '做短影音',
        'dir_name': 'motion_reels',
        'parent_name': 'polaris-motion-reels',
        'atoms': ['atom-motion-camera-engine', 'atom-motion-overlay-safezone']
    },
    'facebook_publisher': {
        'title': '發臉書',
        'dir_name': 'facebook_publisher',
        'parent_name': 'facebook-publisher',
        'atoms': ['atom-fb-feed-dispatcher', 'atom-fb-preflight-gate']
    },
    'productization': {
        'title': '商品化',
        'dir_name': 'productization',
        'parent_name': 'polaris-productization-master',
        'atoms': ['atom-product-redteam-audit', 'atom-product-trio-scaffolder']
    },
    'client_resilience': {
        'title': '客戶端抗逆',
        'dir_name': 'client_resilience',
        'parent_name': 'polaris-client-architect',
        'atoms': ['atom-client-offline-heartbeat', 'atom-client-resilient-transport']
    },
    'lifebutler_care': {
        'title': '生活管家',
        'dir_name': 'lifebutler_care',
        'parent_name': 'lifebutler-care-artisan',
        'atoms': ['atom-care-order-dispatcher', 'atom-care-telehealth-card']
    },
    'course_master': {
        'title': '開課營運',
        'dir_name': 'course_master',
        'parent_name': 'polaris-course-master',
        'atoms': ['atom-course-enrollment-pipeline', 'atom-course-syllabus-scaffolder']
    },
    'flywheel': {
        'title': '飛輪總控',
        'dir_name': 'flywheel',
        'parent_name': 'polaris-flywheel-orchestrator',
        'atoms': ['atom-flywheel-launch-cockpit', 'atom-flywheel-event-router']
    },
    'supplychain_audit': {
        'title': '選品審計',
        'dir_name': 'supplychain_audit',
        'parent_name': 'ai-pricing-auditor',
        'atoms': ['atom-supplychain-tactical-negotiator', 'atom-supplychain-layer-deconstructor']
    },
    'groupbuy_marketing': {
        'title': '選品行銷',
        'dir_name': 'groupbuy_marketing',
        'parent_name': 'sharp-groupbuy-analyzer',
        'atoms': ['atom-groupbuy-four-prism-copy', 'atom-groupbuy-cost-auditor']
    }
}

for k, v in groups.items():
    print(f"=== {v['title']} ({k}) ===")
    parent_path = None
    for p in [Path(f".agents/skills/{v['parent_name']}/SKILL.md"), Path(f"C:/Users/lenovo/.gemini/config/skills/{v['parent_name']}/SKILL.md")]:
        if p.exists():
            parent_path = p
            break
    print(f"  Parent ({v['parent_name']}): {parent_path}")
    for atom in v['atoms']:
        atom_path = None
        for p in [Path(f".agents/skills/atoms/{atom}/SKILL.md"), Path(f".agents/skills/{atom}/SKILL.md")]:
            if p.exists():
                atom_path = p
                break
        print(f"  Atom ({atom}): {atom_path}")
