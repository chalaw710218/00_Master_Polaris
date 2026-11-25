import re
from pathlib import Path

# 1. Update atom-motion-overlay-safezone
p_motion = Path('_proposed/做短影音/atom-motion-overlay-safezone/SKILL.md')
txt_motion = p_motion.read_text(encoding='utf-8')
if '350px' not in txt_motion:
    txt_motion = txt_motion.replace(
        "1. **社群原生 UI 安全邊界避讓 (Social Safe Zone Guard)**：",
        "1. **社群原生 UI 安全邊界避讓 (Social Safe Zone Guard)**：\n   - 避開底部 350px 文案區與右側 120px 互動區，預留安全留白。"
    )
    p_motion.write_text(txt_motion, encoding='utf-8')
    print("Updated atom-motion-overlay-safezone with 350px and 120px")

# 2. Update atom-supplychain-layer-deconstructor
p_supply = Path('_proposed/選品審計/atom-supplychain-layer-deconstructor/SKILL.md')
txt_supply = p_supply.read_text(encoding='utf-8')
if '20%' not in txt_supply:
    txt_supply = txt_supply.replace(
        "1. **四層階層毛利數學倒推架構 (4-Layer Supply Chain Decomposition)**：",
        "1. **四層階層毛利數學倒推架構 (4-Layer Supply Chain Decomposition)**：\n   - 考量物理加工修清與失水損耗 (5%~20%)，精算真實還原成本。"
    )
    p_supply.write_text(txt_supply, encoding='utf-8')
    print("Updated atom-supplychain-layer-deconstructor with 20%")
