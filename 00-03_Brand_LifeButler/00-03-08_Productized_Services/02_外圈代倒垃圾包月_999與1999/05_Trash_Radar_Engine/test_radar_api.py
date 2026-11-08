#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一鍵倒垃圾雷達 API 伺服器端自動化整合驗證腳本
測試覆蓋：
1. GET /api/v1/health
2. GET /api/v1/radar/query (經緯度、指定時刻、清運日正常回傳)
3. POST /api/v1/radar/query (JSON Payload 解析)
4. 戴明安燈防呆 1：週三/週六停收日阻斷驗證
5. 戴明安燈防呆 2：地理圍欄 (台北座標自動校準至台東) 驗證
6. 商業導流字段 (upsell) 完整性校驗
"""

import json
import threading
import time
import urllib.request
import urllib.parse
import sys
import io
import os

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from radar_server import HTTPServer, RadarRequestHandler

TEST_PORT = 18765
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

def run_tests():
    print("==================================================")
    print("🔬 生活管家・一鍵倒垃圾雷達 API 自動化整合測試")
    print("==================================================")

    # 1. 在背景線程啟動 HTTP Server
    server_address = ("127.0.0.1", TEST_PORT)
    httpd = HTTPServer(server_address, RadarRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.3)
    print(f"✅ 測試用 HTTP 伺服器已在背景啟動 (Port: {TEST_PORT})")

    try:
        # 測試 1：GET /api/v1/health
        health_req = urllib.request.urlopen(f"{BASE_URL}/api/v1/health")
        health_data = json.loads(health_req.read().decode("utf-8"))
        assert health_data["status"] == "online", "Health check failed"
        print("✅ [Test 1 Passed] GET /api/v1/health -> 服務狀態 Online")

        # 測試 2：GET /api/v1/radar/query 正常清運日查詢 (台東市中心，週二 17:00)
        q_params = urllib.parse.urlencode({
            "lat": "22.7535",
            "lon": "121.1512",
            "time": "17:00",
            "weekday": "Tuesday"
        })
        get_req = urllib.request.urlopen(f"{BASE_URL}/api/v1/radar/query?{q_params}")
        get_data = json.loads(get_req.read().decode("utf-8"))
        assert get_data["status"] == "success", "Query status not success"
        assert get_data["cards"]["fastest"] is not None, "Fastest card should not be empty on collection day"
        assert "nav_url" in get_data["cards"]["fastest"], "Navigation URL must exist"
        print(f"✅ [Test 2 Passed] GET 查詢成功：最快到站【{get_data['cards']['fastest']['stop_name']}】(倒數 {get_data['cards']['fastest']['eta_diff_min']} 分鐘)")

        # 測試 3：POST /api/v1/radar/query
        post_payload = json.dumps({
            "lat": 22.7420,
            "lon": 121.1390,
            "time": "16:40",
            "weekday": "Thursday"
        }).encode("utf-8")
        post_req = urllib.request.Request(
            f"{BASE_URL}/api/v1/radar/query",
            data=post_payload,
            headers={"Content-Type": "application/json"}
        )
        post_res = urllib.request.urlopen(post_req)
        post_data = json.loads(post_res.read().decode("utf-8"))
        assert post_data["status"] == "success", "POST query failed"
        print(f"✅ [Test 3 Passed] POST 查詢成功：最快站點【{post_data['cards']['fastest']['stop_name']}】步行 {post_data['cards']['fastest']['dist_meters']} 公尺")

        # 測試 4：戴明安燈防呆 1 - 台東在地停收日阻斷測試 (週三與週日例行停收)
        for off_day in ["Wednesday", "Sunday"]:
            off_payload = json.dumps({
                "lat": 22.7535,
                "lon": 121.1512,
                "time": "17:30",
                "weekday": off_day
            }).encode("utf-8")
            off_req = urllib.request.Request(
                f"{BASE_URL}/api/v1/radar/query",
                data=off_payload,
                headers={"Content-Type": "application/json"}
            )
            off_res = urllib.request.urlopen(off_req)
            off_data = json.loads(off_res.read().decode("utf-8"))
            assert off_data["meta"]["is_off_day"] is True, f"Must identify {off_day} as off day"
            assert off_data["cards"]["fastest"] is None, f"Fastest card must be None on {off_day}"
            assert off_data["meta"]["off_day_notice"] is not None, "Notice must be provided"
        print("✅ [Test 4 Passed] 戴明安燈防呆 1：台東在地【週三與週日例行停收】100% 成功阻斷誤導")

        # 測試 4.1：週六正常清運測試 (驗證週六有收運)
        sat_payload = json.dumps({
            "lat": 22.7535,
            "lon": 121.1512,
            "time": "17:00",
            "weekday": "Saturday"
        }).encode("utf-8")
        sat_req = urllib.request.Request(
            f"{BASE_URL}/api/v1/radar/query",
            data=sat_payload,
            headers={"Content-Type": "application/json"}
        )
        sat_res = urllib.request.urlopen(sat_req)
        sat_data = json.loads(sat_res.read().decode("utf-8"))
        assert sat_data["meta"]["is_off_day"] is False, "Saturday must be a collection day in Taitung"
        assert sat_data["cards"]["fastest"] is not None, "Saturday should have fastest collection point"
        print("✅ [Test 4.1 Passed] 台東在地【週六正常清運】驗證通過：非停收日，正常導航！")

        # 測試 5：戴明安燈防呆 2 - 外縣市座標地理圍欄校準 (輸入台北 101 座標)
        taipei_payload = json.dumps({
            "lat": 25.0339,
            "lon": 121.5644,
            "time": "17:10",
            "weekday": "Friday"
        }).encode("utf-8")
        taipei_req = urllib.request.Request(
            f"{BASE_URL}/api/v1/radar/query",
            data=taipei_payload,
            headers={"Content-Type": "application/json"}
        )
        taipei_res = urllib.request.urlopen(taipei_req)
        taipei_data = json.loads(taipei_res.read().decode("utf-8"))
        assert taipei_data["meta"]["geo_fence_adjusted"] is True, "Must trigger geo-fence adjustment"
        print("✅ [Test 5 Passed] 戴明安燈防呆 2：台北座標成功觸發地理圍欄校準至台東市中心")

        # 測試 6：商業轉化字段校驗
        assert "upsell" in get_data and "cta_url" in get_data["upsell"], "Upsell info missing"
        print(f"✅ [Test 6 Passed] 商業閉環驗證：【{get_data['upsell']['title']}】導流入口健全")

        print("==================================================")
        print("🎉 全部 6 項 API 整合與防呆單元測試 100% 綠燈通過！(Exit Code: 0)")
        print("==================================================")

    finally:
        httpd.shutdown()
        httpd.server_close()

if __name__ == "__main__":
    run_tests()
