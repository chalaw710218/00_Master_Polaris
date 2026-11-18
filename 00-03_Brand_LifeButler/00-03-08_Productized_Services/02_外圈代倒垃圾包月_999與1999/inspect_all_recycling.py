import json

r = json.load(open('05_Trash_Radar_Engine/data/recycling_routes.json', encoding='utf-8'))
for x in r:
    print(f"run_id={x.get('run_id')} | route_id={x.get('route_id')} | name={x.get('route_name')} | plate={x.get('truck_plate')}")
