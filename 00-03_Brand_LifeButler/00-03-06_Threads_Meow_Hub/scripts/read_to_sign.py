import json

data = json.load(open('data/_本批待簽.json', encoding='utf-8'))
print('office:', data.get('office'))
print('action:', data.get('action'))
print('count:', data.get('count'))
print('batch_sha256:', data.get('batch_sha256'))
print('entries count:', len(data.get('entries', [])))
for e in data.get('entries', []):
    print(f"- [{e.get('index')}] {e.get('title')}: hash={e.get('entry_hash')[:16]}... url={e.get('url')}")
