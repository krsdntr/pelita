import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_text_file = r"d:\app\alkitab\scratch\full_raw_text.txt"

with open(raw_text_file, "r", encoding="utf-8") as f:
    text = f.read()

# Let's clean up some hyphenations first
text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', text)

# Let's split by page first to inspect
pages = text.split("=== PAGE ")

# A dictionary to store questions by number
questions_db = {}

# Heuristic to check if a line is in Italian
def is_italian(s):
    italian_words = ["qual", "disegno", "dell", "perche", "desiderio", "ragione", "mistero", "rivelazione", "basta", "luce", "nell", "con", "alla", "sola", "creazione", "mondo", "uomo", "dio", "fede", "chiesa", "padre", "figlio", "spirito", "santo", "peccato", "salvezza", "sacramento", "liturgia", "morale", "preghiera"]
    s_lower = s.lower()
    matches = 0
    for w in italian_words:
        if re.search(r'\b' + w + r'\b', s_lower):
            matches += 1
    return matches >= 2

# We will scan the entire text for patterns
# Let's find matches of: \n\s*(\d+)\.\s*(.*?)\n
# where the question number is found.
# Let's write a robust extraction loop.

print("Scanning for question starts...")
matches = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*(.*?)(?=\n)', text))
print(f"Found {len(matches)} potential question start markers.")

for idx, m in enumerate(matches):
    num = int(m.group(1))
    q_line = m.group(2).strip()
    
    # Skip Italian repeating headers
    if is_italian(q_line) or "disegno di dio" in q_line.lower() or "desiderio di dio" in q_line.lower() or "della ragione" in q_line.lower() or "luce della" in q_line.lower():
        continue
        
    start_pos = m.end()
    # The end of the answer is either the start of the next match (which is not Italian) or the end of the text
    end_pos = len(text)
    for next_m in matches[idx+1:]:
        next_num = int(next_m.group(1))
        next_q_line = next_m.group(2).strip()
        if not (is_italian(next_q_line) or "disegno di dio" in next_q_line.lower() or "desiderio di dio" in next_q_line.lower() or "della ragione" in next_q_line.lower()):
            end_pos = next_m.start()
            break
            
    answer_block = text[start_pos:end_pos].strip()
    
    # Save the question
    if num not in questions_db:
        questions_db[num] = {
            "question": q_line,
            "raw_answer": answer_block
        }
    else:
        # If we have multiple matches, we might want to check which one is Indonesian
        # Since we skipped Italian, if the existing one is short or empty, we replace it
        if len(q_line) > len(questions_db[num]["question"]):
            questions_db[num]["question"] = q_line
            questions_db[num]["raw_answer"] = answer_block

print(f"Successfully extracted {len(questions_db)} unique Indonesian questions.")

# Let's print questions 1 to 10
print("\n--- Questions 1 to 10 ---")
for i in range(1, 11):
    if i in questions_db:
        q = questions_db[i]
        print(f"\n[{i}] Q: {q['question']}")
        print(f"A (first 300 chars): {q['raw_answer'][:300]}...")
    else:
        print(f"\n[{i}] NOT FOUND")
