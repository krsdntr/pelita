import json
with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Q1-Q10 in JSON:")
for p in data:
    for q in p['questions']:
        if q['id'] <= 10:
            print(f"ID {q['id']}: {q['question']}")
