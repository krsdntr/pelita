"""
Compare the original PDF content with our catechism-compendium.json database.
Focus on:
1. Total question count (should be 598)
2. Completeness of answers (truncated or partial)
3. Contamination from Italian column or Appendix text
4. Missing/corrupted questions
"""
import json
import re

# Load our JSON database
with open(r"d:\app\alkitab\src\data\catechism-compendium.json", "r", encoding="utf-8") as f:
    pillars = json.load(f)

print("=" * 70)
print("ANALYSIS: catechism-compendium.json vs Original PDF")
print("=" * 70)

# Flatten all questions
all_questions = []
for pillar in pillars:
    for q in pillar["questions"]:
        q["pillar"] = pillar["pillar"]
        all_questions.append(q)

print(f"\nTotal questions in JSON: {len(all_questions)}")
print(f"Expected: 598")
print()

# Check for questions with empty answers
empty_answers = [q for q in all_questions if not q["answer"].strip()]
print(f"Questions with EMPTY answers: {len(empty_answers)}")
for q in empty_answers:
    print(f"  Q{q['id']}: {q['question'][:60]}...")

# Check for questions with very short answers (< 50 chars = probably truncated)
short_answers = [q for q in all_questions if len(q["answer"].strip()) < 80 and q["answer"].strip()]
print(f"\nQuestions with VERY SHORT answers (<80 chars): {len(short_answers)}")
for q in short_answers:
    print(f"  Q{q['id']}: answer='{q['answer'][:60]}...'")

# Check for answers contaminated with Italian text
italian_markers = ["dell'", "della", "degli", "nella", "nella", "alla", "allo", "Dio,", "è ", "è stato", "si è"]
contaminated = []
for q in all_questions:
    ans = q["answer"]
    if any(marker in ans for marker in italian_markers):
        # Check if the answer has both Italian and Indonesian text
        # Look for typical Italian grammar: articles + noun patterns
        if re.search(r'\b(dell|della|degli|nella|alla|allo|eius|nobis|Deum|Dóminus)\b', ans):
            contaminated.append(q)

print(f"\nQuestions potentially CONTAMINATED with Italian/Latin: {len(contaminated)}")
for q in contaminated[:10]:
    print(f"  Q{q['id']}: {q['answer'][:80]}...")

# Check for Latin text contamination
latin_markers = ["Dóminus", "Patris", "Filio", "Spiritu", "Sancto", "grátia", "misericórdiæ", "æterna"]
latin_contaminated = [q for q in all_questions if any(m in q["answer"] for m in latin_markers)]
print(f"\nQuestions contaminated with LATIN text: {len(latin_contaminated)}")
for q in latin_contaminated:
    print(f"  Q{q['id']}: {q['answer'][:80]}...")

# Check for questions with APPENDIX text leaking in
appendix_markers = ["Lampiran", "Bagian Empat  2", "Kompendium \n", "Seksi Dua:", "Salam Maria", "Tanda Salib"]
appendix_contaminated = [q for q in all_questions if any(m in q["answer"] for m in appendix_markers)]
print(f"\nQuestions CONTAMINATED with Appendix/Liturgy text: {len(appendix_contaminated)}")
for q in appendix_contaminated:
    print(f"  Q{q['id']}: {q['answer'][:100]}...")

# Check for questions where question text is truncated/partial
truncated_questions = [q for q in all_questions if q["question"].endswith('"') == False and (q["question"].endswith("?") == False and not q["question"].endswith("...")) and q["question"].strip()]
suspicious_questions = [q for q in all_questions if len(q["question"]) < 20 or q["question"].endswith('"')]
print(f"\nQuestions with SUSPICIOUS/PARTIAL question text: {len(suspicious_questions)}")
for q in suspicious_questions[:10]:
    print(f"  Q{q['id']}: '{q['question']}'")

# Check for empty reflections (these were supposed to be generated)
empty_reflections = [q for q in all_questions if not q["reflection"].strip()]
print(f"\nQuestions with EMPTY reflections: {len(empty_reflections)}")
if empty_reflections:
    print(f"  IDs: {[q['id'] for q in empty_reflections]}")

# Range analysis
all_ids = sorted([q["id"] for q in all_questions])
print(f"\nQuestion ID range: {min(all_ids)} to {max(all_ids)}")
expected_ids = set(range(1, 599))
missing_ids = expected_ids - set(all_ids)
duplicate_ids = [id for id in all_ids if all_ids.count(id) > 1]
print(f"Missing IDs: {sorted(missing_ids)}")
print(f"Duplicate IDs: {sorted(set(duplicate_ids))}")

print("\n" + "=" * 70)
print("SUMMARY OF ISSUES FOUND")
print("=" * 70)
