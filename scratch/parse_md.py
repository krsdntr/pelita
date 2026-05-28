import json
import re

md_path = 'd:/app/alkitab/kompendium indonesia.md'
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

questions = {}
current_qid = None
current_question = ""
current_answer_lines = []
parsing_started = False

def process_current():
    global current_qid, current_question, current_answer_lines
    if current_qid is not None:
        filtered = []
        for line in current_answer_lines:
            line = line.strip()
            if not line:
                continue
            if line.isupper() and len(line) > 5:
                continue
            if line.startswith("Bab ") or line.startswith("Bagian ") or line.startswith("BAB ") or line.startswith("BAGIAN "):
                continue
            # Skip references
            if re.match(r'^((Tahun\s+)?\d+-\d+|\d+(,\s*\d+)*)$', line):
                continue
            filtered.append(line)
        
        answer_text = " ".join(filtered)
        questions[current_qid] = {
            "question": current_question,
            "answer": answer_text
        }
    
    current_qid = None
    current_question = ""
    current_answer_lines = []

for line in lines:
    if not parsing_started:
        if "1. Apa rencana Tuhan bagi manusia?" in line:
            parsing_started = True
        else:
            continue

    m = re.match(r'^(\d+)\.\s+(.*)', line.strip())
    if m:
        qid = int(m.group(1))
        if 1 <= qid <= 598:
            if current_qid is None or qid == current_qid + 1 or qid == current_qid:
                process_current()
                current_qid = qid
                current_question = m.group(2)
                continue
            elif qid > current_qid and qid - current_qid < 5:
                process_current()
                current_qid = qid
                current_question = m.group(2)
                continue
            else:
                if current_qid is not None:
                    current_answer_lines.append(line)
                continue
    else:
        if current_qid is not None:
            current_answer_lines.append(line)

process_current()

print(f"Extracted {len(questions)} questions.")
for i in range(1, 6):
    if i in questions:
        print(f"Q{i}: {questions[i]['question']}")
        print(f"A: {questions[i]['answer'][:100]}...")
        print()

for i in [218, 598]:
    if i in questions:
        print(f"Q{i}: {questions[i]['question']}")
        print(f"A: {questions[i]['answer'][:100]}...")
        print()
