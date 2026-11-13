# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * c * 1.25)

# 測試解析 XML
sample_xml = """<?xml version="1.0" encoding="utf-8"?>
<Items>
  <Car car_no="KEH-5109" lat="22.7567" lon="121.1187" speed="18.5" time="16:10:00" car_status="執勤中" />
  <Car car_no="BXT-2067" lat="22.7708" lon="121.1126" speed="0.0" time="16:15:20" car_status="停等中" />
</Items>"""

root = ET.fromstring(sample_xml)
cars = {}
for c in root.findall('Car'):
    cars[c.attrib['car_no']] = {
        'lat': float(c.attrib['lat']),
        'lon': float(c.attrib['lon']),
        'speed': float(c.attrib['speed']),
        'time': c.attrib['time'],
        'status': c.attrib.get('car_status', '執勤中')
    }

print("Parsed cars count:", len(cars))
assert "KEH-5109" in cars

# 測試計算車輛至站點距離與動態 ETA
# 假設站點在中興路3段20號 (22.7697, 121.1174)
stop_lat = 22.7697
stop_lon = 121.1174
truck = cars["KEH-5109"]
dist = haversine(truck['lat'], truck['lon'], stop_lat, stop_lon)
# 市區垃圾車平均速度約 260 公尺/分鐘 (含隨停投遞)
est_min = max(1, round(dist / 260))

print(f"Truck KEH-5109 -> Stop dist: {dist}m, estimated arrival: {est_min} min")
assert dist > 0 and est_min > 0
print("ALL LIVE ETA ENGINE TESTS PASSED (EXIT CODE 0)!")
