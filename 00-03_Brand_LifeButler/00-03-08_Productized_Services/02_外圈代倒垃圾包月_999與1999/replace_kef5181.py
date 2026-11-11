# -*- coding: utf-8 -*-
import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine")
HTML_PATH = os.path.join(ENGINE_DIR, "index.html")
SEED_PATH = os.path.join(ENGINE_DIR, "taitung_trash_routes_seed.json")

# 1. 更新 taitung_trash_routes_seed.json
with open(SEED_PATH, "r", encoding="utf-8") as f:
    seed_data = json.load(f)

for r in seed_data["routes"]:
    if r["truck_plate"] == "KEH-5201":
        r["truck_plate"] = "KEF-5181"
        r["route_name"] = "新站/興航岩灣線"
        r["notes"] = "台東市公所清運E點通官方核定車號 KEF-5181"
        # 修正為官方真實清運節點
        r["stops"] = [
            { "stop_id": "S05_01", "name": "新站路98巷口（近興航街）", "lat": 22.7932, "lon": 121.1218, "scheduled_time": "19:45", "notes": "台東市公所官方清運點 (新站路/興航街生活圈)" },
            { "stop_id": "S05_02", "name": "新站一街與興安路口", "lat": 22.7930, "lon": 121.1225, "scheduled_time": "19:20", "notes": "台東市公所官方清運點 (台東火車站特區)" },
            { "stop_id": "S05_03", "name": "志航路一段403號前", "lat": 22.7880, "lon": 121.1270, "scheduled_time": "18:50", "notes": "台東市公所官方清運點 (近志航陸橋)" },
            { "stop_id": "S05_04", "name": "岩灣眷村聚落前", "lat": 22.7980, "lon": 121.1250, "scheduled_time": "20:20", "notes": "台東市公所官方清運點 (岩灣社區)" }
        ]

with open(SEED_PATH, "w", encoding="utf-8") as f:
    json.dump(seed_data, f, ensure_ascii=False, indent=2)

print("Updated taitung_trash_routes_seed.json with KEF-5181")

# 2. 生成 JavaScript LOCAL_SEED_ROUTES
routes_js_lines = ["    const LOCAL_SEED_ROUTES = ["]
for r in seed_data["routes"]:
    routes_js_lines.append("      {")
    routes_js_lines.append(f'        route_name: "{r["route_name"]}", truck_plate: "{r["truck_plate"]}", has_recycling: {str(r["has_recycling"]).lower()},')
    routes_js_lines.append("        stops: [")
    for s in r["stops"]:
        time_val = s.get("scheduled_time") or s.get("time")
        note_val = s.get("notes", "")
        routes_js_lines.append(f'          {{ name: "{s["name"]}", lat: {s["lat"]}, lon: {s["lon"]}, time: "{time_val}", notes: "{note_val}" }},')
    routes_js_lines.append("        ]")
    routes_js_lines.append("      },")
routes_js_lines.append("    ];")
new_routes_js = "\n".join(routes_js_lines)

# 3. 更新 index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 替換 LOCAL_SEED_ROUTES
routes_pattern = re.compile(r'const LOCAL_SEED_ROUTES = \[.*?\];', re.DOTALL)
assert routes_pattern.search(content), "Cannot find LOCAL_SEED_ROUTES pattern"
content = routes_pattern.sub(new_routes_js.strip(), content)

# 替換所有殘留的 KEH-5201
content = content.replace("KEH-5201", "KEF-5181")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully replaced KEH-5201 with KEF-5181 in index.html!")
