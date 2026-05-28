import pypdf
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
reader = pypdf.PdfReader(pdf_path)

# Scan from Page 19 onwards
pages_data = []
for p in range(18, len(reader.pages)):
    pages_data.append((p+1, reader.pages[p].extract_text()))

def is_italian(s):
    italian_words = ["qual", "disegno", "dell", "perche", "desiderio", "ragione", "mistero", "rivelazione", "basta", "luce", "nell", "con", "alla", "sola", "creazione", "mondo", "uomo", "dio", "fede", "chiesa", "padre", "figlio", "spirito", "santo", "peccato", "salvezza", "sacramento", "liturgia", "morale", "preghiera"]
    s_lower = s.lower()
    matches = 0
    for w in italian_words:
        if re.search(r'\b' + w + r'\b', s_lower):
            matches += 1
    return matches >= 2

text_from_19 = ""
for page_num, page_text in pages_data:
    page_text_clean = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', page_text)
    text_from_19 += f"\n=== PAGE {page_num} ===\n" + page_text_clean

matches = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*(.*?)(?=\n)', text_from_19))

found_nums = set()
for idx, m in enumerate(matches):
    num = int(m.group(1))
    q_line = m.group(2).strip()
    
    if not (1 <= num <= 598):
        continue
    if is_italian(q_line) or "disegno di dio" in q_line.lower() or "desiderio di dio" in q_line.lower() or "della ragione" in q_line.lower() or "luce della" in q_line.lower():
        continue
    
    found_nums.add(num)

missing = [n for n in range(1, 599) if n not in found_nums]
print(f"Missing question numbers: {missing}")

# Let's search the text around the missing numbers to see how they are formatted
for m_num in missing:
    print(f"\n--- Searching for missing question {m_num} ---")
    # Let's find any occurrences of the number followed by a dot in the raw text
    pos = 0
    while True:
        pos = text_from_19.find(f"{m_num}.", pos)
        if pos == -1:
            break
        print(f"Found occurrence of '{m_num}.' at position {pos}. Surrounding text:")
        print(text_from_19[max(0, pos-100):min(len(text_from_19), pos+300)])
        print("="*30)
        pos += len(str(m_num)) + 2
