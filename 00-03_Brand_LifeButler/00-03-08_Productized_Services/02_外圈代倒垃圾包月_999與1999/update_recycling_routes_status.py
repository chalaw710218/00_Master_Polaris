# -*- coding: utf-8 -*-
import json

path = '05_Trash_Radar_Engine/data/recycling_routes.json'
with open(path, 'r', encoding='utf-8') as f:
    routes = json.load(f)

verified_count = 0
unverified_count = 0

for r in routes:
    rid = str(r.get('run_id', ''))
    if rid == '1618':
        r['truck_plate'] = '109-UL'
        r['is_plate_verified'] = True
        r['plate_verification'] = '已查證（官方 APP 實機截圖核實）'
        verified_count += 1
    else:
        r['is_plate_verified'] = False
        r['plate_verification'] = '未查證（暫沿用垃圾車配對車號）'
        unverified_count += 1

with open(path, 'w', encoding='utf-8') as f:
    json.dump(routes, f, ensure_ascii=False, indent=2)

print(f"Update complete! Total: {len(routes)} 條，已查證: {verified_count} 條，未查證: {unverified_count} 條")
