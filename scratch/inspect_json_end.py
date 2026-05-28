import json
with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    for q in p['questions']:
        if q['id'] >= 590:
            print(f"ID {q['id']}: {q['question'][:80]}")
