with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("101. Dalam arti apa hidup Kristus adalah sebuah misteri?")
with open(r"d:\app\alkitab\scratch\q101_context.txt", "w", encoding="utf-8") as out:
    if pos != -1:
        out.write("=== Found Q101 ===\n")
        out.write(text[pos-1000:pos+3000])
    else:
        out.write("Q101 not found")
