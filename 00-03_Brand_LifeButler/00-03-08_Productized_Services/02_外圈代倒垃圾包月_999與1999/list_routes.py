# -*- coding: utf-8 -*-
import sys, io, xml.etree.ElementTree as ET
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

routes_path = r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-11_Reverse_Engineering_Lab\00-11-11_Qingyun_ePoint_GarbageTruck_APK_Reverse\analysis_notes\taitung_routes.xml'
root = ET.parse(routes_path).getroot()

print(f"Total routes: {len(root)}")
for i, r in enumerate(root):
    run_id = r.attrib.get('run_id')
    name = r.attrib.get('name')
    trash = r.attrib.get('trash_day')
    recycle = r.attrib.get('recycle_day')
    route_no = r.attrib.get('route_no')
    print(f"{i+1:02d}: run_id={run_id} no={route_no} name={name} trash={trash} recycle={recycle}")
