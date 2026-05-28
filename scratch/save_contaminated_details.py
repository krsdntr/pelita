import json, sys

with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    db = json.load(f)

ids_to_inspect = [101, 189, 234, 337, 462, 577, 107, 111, 119, 343, 350, 356, 458, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598]

out_lines = []
for pillar in db:
    for q in pillar["questions"]:
        if q["id"] in ids_to_inspect:
            out_lines.append(f'Q{q["id"]} - Question: {q["question"]}')
            out_lines.append(f'Answer: {repr(q["answer"])}')
            out_lines.append(f'Reference: {q.get("reference")}')
            out_lines.append(f'Reflection: {repr(q.get("reflection"))}')
            out_lines.append("-" * 50)

with open(r"d:\app\alkitab\scratch\contaminated_details.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
