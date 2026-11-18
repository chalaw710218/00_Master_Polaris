with open(r"C:\Users\lenovo\Desktop\第2講教學簡報.html", "r", encoding="utf-8") as f:
    text = f.read()

print("Length of Desktop html:", len(text))
print("Contains </html>:", "</html>" in text)
print("Count of slide divs:", text.count('class="slide'))
print("Last 300 chars of file:")
print(text[-300:])
