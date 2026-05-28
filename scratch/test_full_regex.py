import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_text_file = r"d:\app\alkitab\scratch\full_raw_text.txt"

with open(raw_text_file, "r", encoding="utf-8") as f:
    text = f.read()

# Let's clean up hyphenations
text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', text)

# Let's search for any occurrence of \d+\. followed by spaces and a capital letter
# We can match: (\d+)\.\s+([A-Z].*?)
# Let's make sure it handles cases where the number is glued to a word (e.g. Gu115., dosa293.)
matches = list(re.finditer(r'(\d+)\.\s+([A-Z\u201c\u201d\u2018\u2019\"\'\s].*?)(?=\n|$)', text))
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
            # If the number was glued to a word, the next question match start will contain that glued word prefix.
            # We want to remove the glued word from the end of the previous answer!
            # The next match start position is next_m.start().
            # Let's look back to see if there is a word glued to next_num.
            break
            
    answer_block = text[start_pos:end_pos].strip()
    
    # If the answer block ends with a glued word, let's clean it up!
    # For example, for 114, the next match is 115. which starts at "di Gu115."
    # So the answer of 114 would end with "di Gu".
    # Let's clean up any word prefix glued to the next number.
    # The next number was found at `end_pos`.
    # Let's look at the end of the answer_block. If it has a word fragment, we can trim it if needed.
    # Usually it's fine, but let's see how much we can clean.
    
    questions_db[num] = {
        "question": q_line,
        "raw_answer": answer_block
    }

print(f"Extracted {len(questions_db)} unique Indonesian questions.")
missing = [n for n in range(1, 599) if n not in questions_db]
print(f"Missing numbers: {missing}")

for i in [115, 293, 446]:
    if i in questions_db:
        print(f"\n[{i}] Q: {questions_db[i]['question']}")
        print(f"A: {questions_db[i]['raw_answer'][:250]}...")
