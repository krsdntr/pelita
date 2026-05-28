import json
import re

# Correct answers found from Vatican source for corrupted questions
# Format: {id: {"question": "...", "answer": "..."}}
CORRECTIONS = {
    218: {
        "question": "Apa itu liturgi?",
        "answer": "Liturgi adalah perayaan misteri Kristus, dan secara khusus misteri Paskah-Nya (sengsara, wafat, dan kebangkitan-Nya). Dengan melaksanakan imamat Yesus Kristus, liturgi menyatakan dalam tanda-tanda dan membawa pengudusan bagi umat manusia. Pemujaan kepada Allah dilaksanakan oleh Tubuh Mistik Kristus, yaitu oleh kepala dan para anggotanya."
    }
}

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Apply targeted corrections
fixed = 0
for pillar in data:
    for q in pillar.get('questions', []):
        qid = q.get('id')
        if qid in CORRECTIONS:
            c = CORRECTIONS[qid]
            old_q = q['question']
            old_a = q['answer']
            q['question'] = c['question']
            q['answer'] = c['answer']
            fixed += 1
            print(f"Fixed Q{qid}:")
            print(f"  OLD Q: {old_q}")
            print(f"  NEW Q: {c['question']}")
            print(f"  OLD A: {old_a[:80]}...")
            print(f"  NEW A: {c['answer'][:80]}...")
            print()

print(f"Total corrected: {fixed}")

# Now also find all other short/suspicious answers (less than 50 chars) that might be truncated
print("\n--- Suspiciously short answers ---")
for pillar in data:
    for q in pillar.get('questions', []):
        answer = q.get('answer', '').strip()
        question = q.get('question', '').strip()
        # Short answers OR answers starting with lowercase (mid-sentence)
        first_char = answer[0] if answer else ''
        starts_mid_sentence = first_char.islower() or (first_char in 'kKmMdD' and len(answer) < 100 and not answer[0].isupper())
        if len(answer) < 60 or (answer and answer[0].islower()):
            print(f"Q{q.get('id')}: Q={question[:60]}")
            print(f"  A={answer[:120]}")
            print()

with open('d:/app/alkitab/src/data/catechism-compendium.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nSaved!")
