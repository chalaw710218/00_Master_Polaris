# -*- coding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree as ET
import json

RECYCLING_RUN_IDS = [
    "1595", "1601", "1612", "1594", "1490", "1618",
    "1606", "1609", "1615", "1613", "1602", "1605",
    "1617", "1604", "1616", "1610", "1575", "1603"
]

results = {}

for rid in RECYCLING_RUN_IDS:
    url = f"https://taitung-trash-proxy.chalaw710218.workers.dev/schedule?run_id={rid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            root = ET.fromstring(text)
            car_nos = set()
            for item in root.findall(".//ScheduleTime"):
                c = item.get("car_no")
                if c and c.strip():
                    car_nos.add(c.strip())
            results[rid] = list(car_nos)
            print(f"run_id={rid} -> car_no: {list(car_nos)}")
    except Exception as e:
        print(f"run_id={rid} error: {e}")

print("\nFinal Results:")
print(json.dumps(results, indent=2, ensure_ascii=False))
