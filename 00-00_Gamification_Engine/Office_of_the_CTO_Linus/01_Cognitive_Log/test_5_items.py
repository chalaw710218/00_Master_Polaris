import sys
from pathlib import Path

root = Path('c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris')
sys.path.insert(0, str(root / '.agents/skills/bionic-learning-system/bionic_core'))
from evidence_gate import fetch_page_text, quote_in_page

# 62 React Native
t62 = fetch_page_text('https://en.wikipedia.org/wiki/React_Native')
print('62 len:', len(t62))
for line in t62.split('\n'):
    if 'JavaScript Interface' in line or 'JSI' in line:
        print('62 line:', line[:100])
        break

# 76 SQLite WAL
t76 = fetch_page_text('https://www.sqlite.org/wal.html')
for line in t76.split('\n'):
    if 'write-ahead log' in line.lower() and len(line.strip()) > 30:
        print('76 line:', line.strip()[:100])
        break

# 77 seccomp
t77 = fetch_page_text('https://docs.kernel.org/userspace-api/seccomp_filter.html')
for line in t77.split('\n'):
    if 'seccomp' in line.lower() and 'filter' in line.lower() and len(line.strip()) > 30:
        print('77 line:', line.strip()[:100])
        break

# 79 WebTransport
t79 = fetch_page_text('https://en.wikipedia.org/wiki/WebTransport')
print('79 len:', len(t79))
for line in t79.split('\n'):
    if 'webtransport' in line.lower() and len(line.strip()) > 30:
        print('79 line:', line.strip()[:100])
        break

# 85 LoRa
t85 = fetch_page_text('https://en.wikipedia.org/wiki/LoRa')
for line in t85.split('\n'):
    if 'long range' in line.lower() or 'lorawan' in line.lower():
        if len(line.strip()) > 30:
            print('85 line:', line.strip()[:100])
            break
