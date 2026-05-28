import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_text_file = r"d:\app\alkitab\scratch\full_raw_text.txt"

with open(raw_text_file, "r", encoding="utf-8") as f:
    text = f.read()

# Let's clean up hyphenations
text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', text)

# Let's find matches of: (\d+)\.\s+(.*?)(?=\n|$)
# This time we allow any character (including lowercase) at the start of the question
matches = list(re.finditer(r'(\d+)\.\s+(.*?)(?=\n|$)', text))
print(f"Total potential question starts: {len(matches)}")

def is_italian(s):
    italian_words = ["qual", "disegno", "dell", "perche", "desiderio", "ragione", "mistero", "rivelazione", "basta", "luce", "nell", "con", "alla", "sola", "creazione", "mondo", "uomo", "dio", "fede", "chiesa", "padre", "figlio", "spirito", "santo", "peccato", "salvezza", "sacramento", "liturgia", "morale", "preghiera"]
    s_lower = s.lower()
    matches = 0
    for w in italian_words:
        if re.search(r'\b' + w + r'\b', s_lower):
            matches += 1
    return matches >= 2

questions_db = {}
for idx, m in enumerate(matches):
    num = int(m.group(1))
    q_line = m.group(2).strip()
    
    if not (1 <= num <= 598):
        continue
        
    if is_italian(q_line) or "disegno di dio" in q_line.lower() or "desiderio di dio" in q_line.lower() or "della ragione" in q_line.lower() or "luce della" in q_line.lower():
        continue
        
    if num in questions_db:
        continue
        
    start_pos = m.end()
    end_pos = len(text)
    for next_m in matches[idx+1:]:
        next_num = int(next_m.group(1))
        next_q_line = next_m.group(2).strip()
        if 1 <= next_num <= 598 and not (is_italian(next_q_line) or "disegno di dio" in next_q_line.lower() or "desiderio di dio" in next_q_line.lower() or "della ragione" in next_q_line.lower()):
            end_pos = next_m.start()
            break
            
    answer_block = text[start_pos:end_pos].strip()
    
    questions_db[num] = {
        "question": q_line,
        "raw_answer": answer_block
    }

print(f"Extracted {len(questions_db)} unique Indonesian questions.")
missing = [n for n in range(1, 599) if n not in questions_db]
print(f"Missing numbers: {missing}")

if 567 in questions_db:
    print(f"\n[567] Q: {questions_db[567]['question']}")
    print(f"A: {questions_db[567]['raw_answer'][:250]}...")
