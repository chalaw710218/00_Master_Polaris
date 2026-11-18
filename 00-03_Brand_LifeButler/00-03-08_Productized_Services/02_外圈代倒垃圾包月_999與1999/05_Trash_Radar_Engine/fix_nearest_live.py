# -*- coding: utf-8 -*-
with open("05_Trash_Radar_Engine/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
# 替換掉任何對 nearestLive 的引用
old_pattern = r"\$\{nearestLive[^}]*\}"
replacement = "${topNearest.officialEst || '依官方表定'}"
new_text = re.sub(old_pattern, replacement, text)

with open("05_Trash_Radar_Engine/index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Replaced nearestLive occurrences successfully!")
