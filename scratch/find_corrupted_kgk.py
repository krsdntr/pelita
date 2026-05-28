import json

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for pillar in data:
    for q in pillar.get('questions', []):
        question = q.get('question', '').strip()
        answer = q.get('answer', '').strip()
        
        if not question.endswith('?'):
            print(f"ID: {q.get('id')} - Missing question mark")
            print(f"Q: {question}")
            print(f"A: {answer[:100]}...")
            print("-" * 40)
