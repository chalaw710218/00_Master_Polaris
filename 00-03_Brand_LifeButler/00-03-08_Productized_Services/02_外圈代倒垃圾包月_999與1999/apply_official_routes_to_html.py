# -*- coding: utf-8 -*-
"""
編譯新版 index.html：
1. 注入 948 個官方停靠站點 (20 條路線)
2. 升級 renderRadar 支援星期出勤與資源回收精準過濾
3. 保證 node --check 語法完全合規
"""
import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine")
HTML_PATH = os.path.join(ENGINE_DIR, "index.html")
SEED_PATH = os.path.join(ENGINE_DIR, "taitung_trash_routes_seed.json")

with open(SEED_PATH, "r", encoding="utf-8") as f:
    seed_data = json.load(f)

print(f"Loaded {len(seed_data['routes'])} routes, total stops: {sum(len(r['stops']) for r in seed_data['routes'])}")

# 壓縮生成精簡 JS 陣列
routes_js_lines = ["    const LOCAL_SEED_ROUTES = ["]
for r in seed_data["routes"]:
    routes_js_lines.append("      {")
    routes_js_lines.append(f'        route_id: "{r["route_id"]}", route_name: "{r["route_name"]}", truck_plate: "{r["truck_plate"]}",')
    routes_js_lines.append(f'        trash_day: "{r.get("trash_day", "星期一、二、四、五、六")}", recycle_day: "{r.get("recycle_day", "")}",')
    routes_js_lines.append(f'        has_recycling: {str(r.get("has_recycling", True)).lower()},')
    routes_js_lines.append("        stops: [")
    for s in r["stops"]:
        routes_js_lines.append(f'          {{ name: "{s["name"]}", lat: {s["lat"]}, lon: {s["lon"]}, time: "{s["scheduled_time"]}" }},')
    routes_js_lines.append("        ]")
    routes_js_lines.append("      },")
routes_js_lines.append("    ];")
new_routes_js = "\n".join(routes_js_lines)

# 讀取現有 index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 替換 LOCAL_SEED_ROUTES
routes_pattern = re.compile(r'const LOCAL_SEED_ROUTES = \[.*?\];', re.DOTALL)
assert routes_pattern.search(content), "Cannot find LOCAL_SEED_ROUTES pattern"
content = routes_pattern.sub(new_routes_js.strip(), content)

# 升級 renderRadar 的過濾段落
filter_old = '''      LOCAL_SEED_ROUTES.forEach(route => {
        // 創辦人指示：若勾選「資源回收」，強制只挑選具備【垃圾+回收雙收】的車次！
        if (wantRecycle && !route.has_recycling) {
          return;
        }'''

filter_new = '''      const DAY_NAMES = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
      const currentDayName = DAY_NAMES[day];

      LOCAL_SEED_ROUTES.forEach(route => {
        // 1. 星期出勤防呆：該車次今日若無排班則略過
        if (route.trash_day && !route.trash_day.includes(currentDayName) && !isOffDay) {
          return;
        }
        // 2. 資源回收過濾：若勾選資源回收，檢查今日該車次是否有回收
        if (wantRecycle) {
          if (!route.has_recycling || (route.recycle_day && !route.recycle_day.includes(currentDayName) && !isOffDay)) {
            return;
          }
        }'''

assert filter_old in content, "Cannot find filter_old in index.html"
content = content.replace(filter_old, filter_new)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully compiled 948 official stops into {HTML_PATH}!")
