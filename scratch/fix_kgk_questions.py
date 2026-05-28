import json
import re

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
for pillar in data:
    for q in pillar.get('questions', []):
        question = q.get('question', '').strip()
        answer = q.get('answer', '').strip()
        
        if not question.endswith('?'):
            # The question is cut off; find question mark in start of answer
            # Find first '?' in answer
            qmark_idx = answer.find('?')
            if qmark_idx != -1:
                # The missing part is everything before '?' in the answer
                missing_part = answer[:qmark_idx + 1].strip()
                remaining_answer = answer[qmark_idx + 1:].strip()
                
                # Fix the question
                q['question'] = (question + ' ' + missing_part).strip()
                q['answer'] = remaining_answer
                
                # Clean up artifacts in question (stray newlines, single letters)
                q['question'] = re.sub(r'\s+', ' ', q['question']).strip()
                q['answer'] = re.sub(r'^\s*\n+', '', q['answer']).strip()
                
                fixed += 1
                print(f"Fixed Q{q.get('id')}: {q['question'][:80]}...")

print(f"\nTotal fixed: {fixed}")

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved!")
