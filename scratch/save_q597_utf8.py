with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("597. Mengapa kita menutup dengan permohonan ")
with open(r"d:\app\alkitab\scratch\q597_context.txt", "w", encoding="utf-8") as out:
    if pos != -1:
        out.write("=== Found Q597 ===\n")
        out.write(text[pos-500:pos+3000])
    else:
        out.write("Q597 not found")
