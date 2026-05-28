with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("1.  Apa rencana Allah")
if pos != -1:
    print("=== Found Q1 context ===")
    print(text[pos-200:pos+1500])
else:
    print("Q1 not found")
