with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("101. Dalam arti apa hidup Kristus adalah sebuah misteri?")
if pos != -1:
    print("=== Found Q101 ===")
    print(text[pos-1000:pos+3000])
else:
    print("Q101 not found")
