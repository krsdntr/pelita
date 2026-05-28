import json

with open(r"d:\app\alkitab\src\data\catholic-summaries.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data["im"], indent=2, ensure_ascii=False))
