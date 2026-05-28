import json
import re

# 1. Parse Markdown
md_path = 'd:/app/alkitab/kompendium indonesia.md'
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

md_qs = {}
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
            if re.match(r'^((Tahun\s+)?\d+-\d+|\d+(,\s*\d+)*)$', line):
                continue
            filtered.append(line)
        
        md_qs[current_qid] = {
            "question": current_question.strip(),
            "answer": " ".join(filtered).strip()
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

print(f"Parsed {len(md_qs)} questions from markdown.")

# 2. Update JSON
json_path = 'd:/app/alkitab/src/data/catechism-compendium.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for pillar in data:
    for q in pillar['questions']:
        qid = q['id']
        if qid in md_qs:
            q['question'] = md_qs[qid]['question']
            q['answer'] = md_qs[qid]['answer']
            updated_count += 1
            
            # Fix reflections for Q1-Q6 which were originally custom intro questions
            if qid == 1:
                q['reflection'] = "Rencana keselamatan Allah selalu melibatkan kebahagiaan sejati manusia. Mari kita membuka hati terhadap panggilan ilahi ini."
            elif qid == 2:
                q['reflection'] = "Di dalam lubuk hati kita terdalam, ada kerinduan yang hanya bisa diisi oleh Tuhan. Jangan pernah berhenti mencari wajah-Nya."
            elif qid == 3:
                q['reflection'] = "Akal budi adalah anugerah Tuhan yang memampukan kita melihat jejak-jejak Sang Pencipta dalam keindahan alam semesta."
            elif qid == 4:
                q['reflection'] = "Meskipun akal budi kita hebat, kita tetap membutuhkan wahyu ilahi untuk memahami kedalaman kasih dan misteri Tuhan yang tak terselami."
            elif qid == 5:
                q['reflection'] = "Bahasa manusia selalu terbatas untuk menggambarkan Tuhan. Oleh karena itu, kita diajak untuk mendekati-Nya dengan kerendahan hati dan kekaguman."
            elif qid == 6:
                q['reflection'] = "Melalui Kristus, Allah yang tak terlihat menjadi nyata. Kasih yang sejak kekal direncanakan kini diberikan secara penuh kepada kita."

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully updated {updated_count} questions in {json_path}.")
