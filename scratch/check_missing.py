import json

with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    db = json.load(f)

missing_ids = []
for pillar in db:
    for q in pillar["questions"]:
        if not q.get("reflection", "").strip():
            missing_ids.append(q["id"])

print(f"Total missing reflections: {len(missing_ids)}")
print(f"IDs: {missing_ids}")
