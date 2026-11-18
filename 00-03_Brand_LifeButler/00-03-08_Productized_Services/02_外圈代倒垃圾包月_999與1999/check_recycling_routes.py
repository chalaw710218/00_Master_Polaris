import json

with open('05_Trash_Radar_Engine/data/recycling_routes.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)

print(f"Total recycling routes count: {len(routes)}")
for i, r in enumerate(routes):
    print(f"{i+1:2d}. run_id={r.get('run_id')} plate={r.get('truck_plate')} name={r.get('route_name')}")
