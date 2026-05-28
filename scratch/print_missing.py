import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# Print all Q without reflections so agent can see them
for pillar in db:
    for q in pillar["questions"]:
        if not q.get("reflection", "").strip():
            print(f'Q{q["id"]}|{pillar["pillar"]}|{q["question"][:80]}|{q["answer"][:120]}')
