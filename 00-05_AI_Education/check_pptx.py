from pptx import Presentation
prs = Presentation(r"C:\Users\lenovo\Desktop\第2講教學簡報.pptx")
print("PPTX Slide count:", len(prs.slides))
for i, s in enumerate(prs.slides):
    texts = [shape.text_frame.text for shape in s.shapes if shape.has_text_frame]
    t0 = texts[0].replace("\n", " ") if texts else "Empty"
    print(f"Slide {i+1}: {t0[:50]}")
