# -*- coding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree as ET

url = "https://www.bstruck.hinet.net/MIS/subsystem/XML/Appcarlocation.ashx?customer_id=22&key=1"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        text = resp.read().decode('utf-8', errors='ignore')
        print(f"Appcarlocation length: {len(text)}")
        root = ET.fromstring(text)
        cars = root.findall(".//Car")
        print(f"Total cars in XML: {len(cars)}")
        for c in cars:
            print(f"car_no={c.get('car_no')} | name={c.get('name')} | run_id={c.get('run_id')} | status={c.get('car_status')}")
except Exception as e:
    print(f"Error: {e}")
