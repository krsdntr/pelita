with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("119. Dengan cara apa Kristus menyerahkan Diri-Nya kepada Bapa?")
with open(r"d:\app\alkitab\scratch\q119_context.txt", "w", encoding="utf-8") as out:
    if pos != -1:
        out.write("=== Found Q119 ===\n")
        out.write(text[pos-500:pos+2500])
    else:
        out.write("Q119 not found")
