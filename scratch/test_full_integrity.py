import json

with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    db = json.load(f)

total_questions = 0
empty_questions = 0
empty_answers = 0
empty_references = 0
empty_reflections = 0

issues = []

for p_idx, pillar in enumerate(db):
    p_name = pillar.get("pillar", f"Pillar-{p_idx}")
    for q in pillar.get("questions", []):
        total_questions += 1
        qid = q.get("id")
        
        q_text = q.get("question", "").strip()
        ans_text = q.get("answer", "").strip()
        ref_text = q.get("reference", "").strip()
        refl_text = q.get("reflection", "").strip()
        
        if not q_text:
            empty_questions += 1
            issues.append(f"Q{qid} in {p_name}: question text is empty")
        if not ans_text:
            empty_answers += 1
            issues.append(f"Q{qid} in {p_name}: answer text is empty")
        if not ref_text:
            empty_references += 1
            issues.append(f"Q{qid} in {p_name}: reference is empty")
        if not refl_text:
            empty_reflections += 1
            issues.append(f"Q{qid} in {p_name}: reflection is empty")
            
        # Check if reflections have exactly or roughly 2 sentences.
        # Simple check by counting periods/exclamation marks
        # (This is just for informational purposes)
        sentences = [s.strip() for s in refl_text.replace("?", ".").replace("!", ".").split(".") if s.strip()]
        if len(sentences) != 2:
            issues.append(f"Q{qid} in {p_name}: reflection has {len(sentences)} sentences instead of 2. Text: {repr(refl_text)}")

print("=== Catechism Compendium Database Integrity Report ===")
print(f"Total Questions processed: {total_questions}")
print(f"Empty Questions: {empty_questions}")
print(f"Empty Answers: {empty_answers}")
print(f"Empty References: {empty_references}")
print(f"Empty Reflections: {empty_reflections}")
print(f"Total issues found: {len(issues)}")

if issues:
    print("\n--- Listing issues ---")
    for idx, iss in enumerate(issues[:20]):
        print(f"{idx+1}. {iss}")
    if len(issues) > 20:
        print(f"... and {len(issues)-20} more issues.")
else:
    print("\n✅ PERFECT! No issues found. Database is 100% complete and healthy!")
