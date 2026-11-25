from pathlib import Path

groups = [
    {
        'id': '5D定價',
        'parent': Path('.agents/skills/polaris-5d-pricing-engine/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-pricing-bulletproof-clause/SKILL.md'),
            Path('.agents/skills/atoms/atom-pricing-5d-calculator/SKILL.md')
        ]
    },
    {
        'id': '做短影音',
        'parent': Path('.agents/skills/polaris-motion-reels/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-motion-camera-engine/SKILL.md'),
            Path('.agents/skills/atoms/atom-motion-overlay-safezone/SKILL.md')
        ]
    },
    {
        'id': '發臉書',
        'parent': Path('.agents/skills/facebook-publisher/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-fb-feed-dispatcher/SKILL.md'),
            Path('.agents/skills/atoms/atom-fb-preflight-gate/SKILL.md')
        ]
    },
    {
        'id': '商品化',
        'parent': Path('.agents/skills/polaris-productization-master/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-product-redteam-audit/SKILL.md'),
            Path('.agents/skills/atoms/atom-product-trio-scaffolder/SKILL.md')
        ]
    },
    {
        'id': '客戶端抗逆',
        'parent': Path('.agents/skills/polaris-client-architect/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-client-offline-heartbeat/SKILL.md'),
            Path('.agents/skills/atoms/atom-client-resilient-transport/SKILL.md')
        ]
    },
    {
        'id': '生活管家',
        'parent': Path('.agents/skills/lifebutler-care-artisan/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-care-order-dispatcher/SKILL.md'),
            Path('.agents/skills/atoms/atom-care-telehealth-card/SKILL.md')
        ]
    },
    {
        'id': '開課營運',
        'parent': Path('.agents/skills/polaris-course-master/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-course-enrollment-pipeline/SKILL.md'),
            Path('.agents/skills/atoms/atom-course-syllabus-scaffolder/SKILL.md')
        ]
    },
    {
        'id': '飛輪總控',
        'parent': Path('.agents/skills/polaris-flywheel-orchestrator/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-flywheel-launch-cockpit/SKILL.md'),
            Path('.agents/skills/atoms/atom-flywheel-event-router/SKILL.md')
        ]
    },
    {
        'id': '選品審計',
        'parent': None, # does not exist
        'atoms': [
            Path('.agents/skills/atoms/atom-supplychain-tactical-negotiator/SKILL.md'),
            Path('.agents/skills/atoms/atom-supplychain-layer-deconstructor/SKILL.md')
        ]
    },
    {
        'id': '選品行銷',
        'parent': Path('C:/Users/lenovo/.gemini/config/skills/sharp-groupbuy-analyzer/SKILL.md'),
        'atoms': [
            Path('.agents/skills/atoms/atom-groupbuy-four-prism-copy/SKILL.md'),
            Path('.agents/skills/atoms/atom-groupbuy-cost-auditor/SKILL.md')
        ]
    }
]

for g in groups:
    print(f"=== {g['id']} ===")
    if g['parent'] and g['parent'].exists():
        lines = g['parent'].read_text(encoding='utf-8').splitlines()
        print(f"  Parent: {g['parent']} ({len(lines)} lines)")
    else:
        print(f"  Parent: [None / 不存在]")
    for a in g['atoms']:
        if a.exists():
            lines = a.read_text(encoding='utf-8').splitlines()
            print(f"  Atom: {a} ({len(lines)} lines)")
        else:
            print(f"  Atom: [NOT FOUND: {a}]")
