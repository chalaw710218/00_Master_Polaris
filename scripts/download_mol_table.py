import urllib.request
import fitz

url = "https://www.mol.gov.tw/media/a3tjzyan/%E5%8B%9E%E5%8B%95%E5%A5%91%E7%B4%84%E8%AA%8D%E5%AE%9A%E6%8C%87%E5%B0%8E%E5%8E%9F%E5%89%87%E9%99%84%E4%BB%B6-%E5%8B%9E%E5%8B%95%E5%A5%91%E7%B4%84%E5%BE%9E%E5%B1%AC%E6%80%A7%E5%88%A4%E6%96%B7%E6%AA%A2%E6%A0%B8%E8%A1%A8.pdf?mediaDL=true"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, timeout=15).read()
doc = fitz.open(stream=content, filetype="pdf")
print("Page count:", len(doc))
full_text = []
for i, page in enumerate(doc):
    txt = page.get_text()
    full_text.append(txt)
    print(f"=== Page {i+1} === (length {len(txt)})")
    print(txt[:600])

all_txt = "\n".join(full_text)
with open("c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/scripts/mol_check_table.txt", "w", encoding="utf-8") as f:
    f.write(all_txt)
print("Saved to mol_check_table.txt, total length:", len(all_txt))
