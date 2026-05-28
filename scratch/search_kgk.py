import json

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for pillar in data:
    for q in pillar.get('questions', []):
        if q.get('id') in [218, 357] or 'liturgi' in q.get('question', '').lower() or 'liturgi' in q.get('answer', '').lower():
            print(f"ID: {q.get('id')}")
            print(f"Question: {q.get('question')}")
            print(f"Answer: {q.get('answer')}")
            print("-" * 40)
