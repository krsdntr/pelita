import pypdf
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
reader = pypdf.PdfReader(pdf_path)

# Let's extract text page by page starting from Page 19 (index 18)
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

questions_db = {}
for idx, m in enumerate(matches):
    num = int(m.group(1))
    q_line = m.group(2).strip()
    
    # Skip if question number is not between 1 and 598
    if not (1 <= num <= 598):
        continue
        
    if is_italian(q_line) or "disegno di dio" in q_line.lower() or "desiderio di dio" in q_line.lower() or "della ragione" in q_line.lower() or "luce della" in q_line.lower():
        continue
        
    # We only take the FIRST occurrence of the question number!
    if num in questions_db:
        continue
        
    start_pos = m.end()
    end_pos = len(text_from_19)
    for next_m in matches[idx+1:]:
        next_num = int(next_m.group(1))
        next_q_line = next_m.group(2).strip()
        if not (is_italian(next_q_line) or "disegno di dio" in next_q_line.lower() or "desiderio di dio" in next_q_line.lower() or "della ragione" in next_q_line.lower()):
            end_pos = next_m.start()
            break
            
    answer_block = text_from_19[start_pos:end_pos].strip()
    
    questions_db[num] = {
        "question": q_line,
        "raw_answer": answer_block
    }

print(f"Extracted {len(questions_db)} unique Indonesian questions.")

# Let's print questions 1 to 10
print("\n--- Questions 1 to 10 ---")
for i in range(1, 11):
    if i in questions_db:
        q = questions_db[i]
        print(f"\n[{i}] Q: {q['question']}")
        print(f"A (first 200 chars): {q['raw_answer'][:200]}...")
    else:
        print(f"\n[{i}] NOT FOUND")
