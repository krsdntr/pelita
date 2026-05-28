import json
with open('d:/app/alkitab/src/data/search-index.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
print(f"Total verses: {len(d)}")
print(d[0])
