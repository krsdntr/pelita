with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("114. ")
if pos != -1:
    print("=== Q114 Context ===")
    print(text[pos-100:pos+1500])
    
pos2 = text.find("115. ")
if pos2 != -1:
    print("\n=== Q115 Context ===")
    print(text[pos2-100:pos2+1500])
