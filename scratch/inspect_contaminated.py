import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    db = json.load(f)

ids_to_inspect = [101, 189, 234, 337, 462, 577, 107, 111, 119, 343, 350, 356, 458, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598]

for pillar in db:
    for q in pillar["questions"]:
        if q["id"] in ids_to_inspect:
            print(f'Q{q["id"]} - Question: {q["question"]}')
            print(f'Answer: {repr(q["answer"])}')
            print(f'Reference: {q.get("reference")}')
            print(f'Reflection: {repr(q.get("reflection"))}')
            print("-" * 50)
