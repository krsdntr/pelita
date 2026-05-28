with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = 0
while True:
    pos = text.find("567", pos)
    if pos == -1:
        break
    print(f"Found '567' at position {pos}:")
    print(text[pos-150:pos+300])
    print("="*40)
    pos += 3
