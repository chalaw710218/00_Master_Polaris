# -*- coding: utf-8 -*-
with open('05_Trash_Radar_Engine/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 確保同時具備 travelmode=walking 且支援機車導航
pattern = re = None
import re
c = re.sub(
    r'<a class="nav-btn secondary" href="https://www\.google\.com/maps/dir/\?api=1&destination=\${topNearest\.lat},\${topNearest\.lon}&travelmode=.*?" target="_blank">',
    r'<a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topNearest.lat},${topNearest.lon}&travelmode=walking" target="_blank">',
    c
)

with open('05_Trash_Radar_Engine/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated travelmode=walking')
