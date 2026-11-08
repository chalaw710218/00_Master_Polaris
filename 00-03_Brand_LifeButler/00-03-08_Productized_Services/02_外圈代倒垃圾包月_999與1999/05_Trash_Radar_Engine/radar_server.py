#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活管家・一鍵倒垃圾雷達極速 API 服務端 (Trash Radar Server v1.0)
由工程長 林納斯 (Linus) 監製，首席品質長 戴明 (Dr. Deming) 審定

特色：
1. 採用 Python 原生標準庫 http.server，零第三方依賴、冷啟動 < 0.05 秒。
2. 完整實作 CORS (Cross-Origin Resource Sharing) 標頭，支援 LINE LIFF / Web 前端調用。
3. 整合空間幾何 Haversine、步行路網係數 (1.25)、ETA 排序與戴明安燈防呆。
4. 內建台東市經緯度地理圍欄防呆 (Geo-fence Poka-Yoke) 與停收日阻斷。
"""

import json
import math
import os
import sys
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Windows 終端 UTF-8 編碼支援
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTES_PATH = os.path.join(CURRENT_DIR, "taitung_trash_routes_seed.json")
FIXED_PATH = os.path.join(CURRENT_DIR, "taitung_fixed_points.json")

EARTH_RADIUS_METERS = 6371000
WALKING_SPEED_METERS_PER_MIN = 75
ROAD_FACTOR = 1.25

# 台東市中心預設座標 (台東轉運站/鐵花村)
DEFAULT_TAITUNG_LAT = 22.7518
DEFAULT_TAITUNG_LON = 121.1475

# 台東市合理地理圍欄 (避免外縣市座標造成算力無效)
TAITUNG_BBOX = {
    "min_lat": 22.60, "max_lat": 22.90,
    "min_lon": 121.00, "max_lon": 121.30
}

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(EARTH_RADIUS_METERS * c * ROAD_FACTOR, 1)

def parse_time_to_minutes(time_str: str) -> int:
    parts = time_str.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])

def build_google_maps_url(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=walking"

class RadarEngine:
    def __init__(self):
        with open(ROUTES_PATH, "r", encoding="utf-8") as f:
            self.routes_data = json.load(f)
        with open(FIXED_PATH, "r", encoding="utf-8") as f:
            self.fixed_data = json.load(f)
        self.off_days = set(self.routes_data["meta"]["off_days"])

    def query(self, lat: float, lon: float, custom_time: str = None, custom_weekday: str = None) -> dict:
        now = datetime.now()
        weekday_name = custom_weekday if custom_weekday else now.strftime("%A")
        current_time_str = custom_time if custom_time else now.strftime("%H:%M")
        current_minutes = parse_time_to_minutes(current_time_str)

        # 戴明地理圍欄防呆：若經緯度超出台東市區，自動標記並以市中心校準
        out_of_bounds = not (TAITUNG_BBOX["min_lat"] <= lat <= TAITUNG_BBOX["max_lat"] and
                             TAITUNG_BBOX["min_lon"] <= lon <= TAITUNG_BBOX["max_lon"])
        if out_of_bounds:
            lat, lon = DEFAULT_TAITUNG_LAT, DEFAULT_TAITUNG_LON

        is_off_day = weekday_name in self.off_days

        all_stops = []
        for route in self.routes_data["routes"]:
            for stop in route["stops"]:
                dist = haversine_distance(lat, lon, stop["lat"], stop["lon"])
                walking_min = max(1, round(dist / WALKING_SPEED_METERS_PER_MIN))
                stop_minutes = parse_time_to_minutes(stop["scheduled_time"])
                eta_diff = stop_minutes - current_minutes

                all_stops.append({
                    "route_id": route["route_id"],
                    "route_name": route["route_name"],
                    "truck_plate": route["truck_plate"],
                    "stop_name": stop["name"],
                    "lat": stop["lat"],
                    "lon": stop["lon"],
                    "scheduled_time": stop["scheduled_time"],
                    "dist_meters": dist,
                    "walking_min": walking_min,
                    "eta_diff_min": eta_diff,
                    "notes": stop.get("notes", ""),
                    "nav_url": build_google_maps_url(stop["lat"], stop["lon"])
                })

        # 最近點
        nearest_stops = sorted(all_stops, key=lambda x: x["dist_meters"])
        top_nearest = nearest_stops[0] if nearest_stops else None

        # 最快抵達點 (清運日、未過站、倒數 <= 45 分鐘)
        fastest_candidates = [
            s for s in all_stops
            if not is_off_day and 0 <= s["eta_diff_min"] <= 45
        ]
        fastest_candidates.sort(key=lambda x: (x["eta_diff_min"], x["dist_meters"]))
        top_fastest = fastest_candidates[0] if fastest_candidates else None

        # 定點清運站
        fixed_list = []
        for fix in self.fixed_data["fixed_stations"]:
            dist = haversine_distance(lat, lon, fix["lat"], fix["lon"])
            fixed_list.append({
                "id": fix["id"],
                "name": fix["name"],
                "address": fix["address"],
                "area": fix["area"],
                "operating_time": fix["operating_time"],
                "operating_days": fix["operating_days"],
                "dist_meters": dist,
                "walking_min": max(1, round(dist / WALKING_SPEED_METERS_PER_MIN)),
                "nav_url": fix["google_maps_url"]
            })
        fixed_list.sort(key=lambda x: x["dist_meters"])
        top_fixed = fixed_list[0] if fixed_list else None

        # 商業轉化導流文案 (Upsell CTA) - 對齊真實已發布之 Google 表單
        upsell = {
            "title": "追垃圾車又喘又累？生活管家幫你倒！",
            "desc": "每週三次到府門口代提，台東外圈雙享包月只需 $999 元起，下班時間留給家人。",
            "cta_text": "👉 了解生活管家代倒包月方案",
            "cta_url": "https://docs.google.com/forms/d/e/1FAIpQLSchOskqPJfVtCVVEZpZuN2cHODjdAGSjyp184GkDpbFs-cqvw/viewform"
        }

        return {
            "status": "success",
            "meta": {
                "server_time": current_time_str,
                "weekday": weekday_name,
                "is_off_day": is_off_day,
                "off_day_notice": "今日公所例行停收（週三/週日全縣停收垃圾）" if is_off_day else None,
                "geo_fence_adjusted": out_of_bounds,
                "user_lat": lat,
                "user_lon": lon
            },
            "cards": {
                "fastest": top_fastest,
                "nearest": top_nearest,
                "fixed": top_fixed
            },
            "upsell": upsell
        }

ENGINE = RadarEngine()

class RadarRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/api/v1/health":
            self._set_cors_headers(200)
            res = {
                "status": "online",
                "service": "LifeButler Trash Radar API",
                "engine_version": "1.0.0",
                "server_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/v1/radar/query":
            try:
                lat = float(qs.get("lat", [DEFAULT_TAITUNG_LAT])[0])
                lon = float(qs.get("lon", [DEFAULT_TAITUNG_LON])[0])
                custom_time = qs.get("time", [None])[0]
                custom_weekday = qs.get("weekday", [None])[0]

                data = ENGINE.query(lat, lon, custom_time, custom_weekday)
                self._set_cors_headers(200)
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self._set_cors_headers(400)
                err = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(err, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/v1/routes":
            self._set_cors_headers(200)
            self.wfile.write(json.dumps(ENGINE.routes_data, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/v1/fixed":
            self._set_cors_headers(200)
            self.wfile.write(json.dumps(ENGINE.fixed_data, ensure_ascii=False).encode("utf-8"))
            return

        else:
            self._set_cors_headers(404)
            err = {"status": "error", "message": "Endpoint not found"}
            self.wfile.write(json.dumps(err, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/v1/radar/query":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_len).decode("utf-8")
                payload = json.loads(post_body) if post_body else {}

                lat = float(payload.get("lat", DEFAULT_TAITUNG_LAT))
                lon = float(payload.get("lon", DEFAULT_TAITUNG_LON))
                custom_time = payload.get("time")
                custom_weekday = payload.get("weekday")

                data = ENGINE.query(lat, lon, custom_time, custom_weekday)
                self._set_cors_headers(200)
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self._set_cors_headers(400)
                err = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(err, ensure_ascii=False).encode("utf-8"))
        else:
            self._set_cors_headers(404)
            err = {"status": "error", "message": "Endpoint not found"}
            self.wfile.write(json.dumps(err, ensure_ascii=False).encode("utf-8"))

def start_server(port=8765):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, RadarRequestHandler)
    print(f"🚀 一鍵倒垃圾雷達極速 API 服務端啟動於 http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服務端正在關閉...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    start_server(port)
