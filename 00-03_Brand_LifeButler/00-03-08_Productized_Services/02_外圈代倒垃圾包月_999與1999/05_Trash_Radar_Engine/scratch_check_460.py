import json
import math

with open('05_Trash_Radar_Engine/data/garbage_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

print('Routes count:', len(routes))
for r in routes:
    for st in r.get('stops', []):
        if '460號' in st.get('name', ''):
            print(f"Found: route={r.get('route_name')}, plate={r.get('truck_plate')}, time={st.get('time')}, lat={st.get('lat')}, lon={st.get('lon')}, trash_day={r.get('trash_day')}")
