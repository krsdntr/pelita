import json

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Q218
for pillar in data:
    for q in pillar.get('questions', []):
        if q.get('id') == 218:
            print(f"ID: {q['id']}")
            print(f"QUESTION: {q['question']}")
            print(f"ANSWER: {q['answer'][:500]}")
            print("---")
        if q.get('id') in [215, 216, 217, 219, 220]:
            print(f"ID: {q['id']}")
            print(f"Q: {q['question']}")
            print(f"A: {q['answer'][:200]}")
            print("---")
