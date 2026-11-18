import urllib.request
import socket

for host in ['127.0.0.1', 'localhost', '::1']:
    s = socket.socket(socket.AF_INET if ':' not in host else socket.AF_INET6, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, 9222))
        print(f"Socket connected to {host}:9222 successfully!")
        s.close()
    except Exception as e:
        print(f"Failed to connect to {host}:9222 - {e}")

try:
    with urllib.request.urlopen('http://localhost:9222/json', timeout=2) as r:
        print("HTTP /json response length:", len(r.read()))
except Exception as e:
    print("HTTP /json error:", e)
