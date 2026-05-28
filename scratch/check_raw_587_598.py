"""
Fix the compendium comprehensively:
1. Identify all 166 missing reflections
2. Check the raw content for Q587-Q598
3. Use Gemini API to fix all issues
"""
import json
import urllib.request
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Load the cleaned raw compendium
with open(r"d:\app\alkitab\scratch\cleaned_raw_compendium.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Flatten
all_q_raw = []
for pillar in raw:
    for q in pillar["questions"]:
        all_q_raw.append(dict(q))
        all_q_raw[-1]["pillar"] = pillar["pillar"]

raw_by_id = {q["id"]: q for q in all_q_raw}

print("=== Raw answers for Q587-Q598 ===")
for qid in range(587, 599):
    q = raw_by_id.get(qid, {})
    print(f"\nQ{qid}: {q.get('question', 'N/A')[:80]}")
    ans = q.get('answer', 'N/A')
    print(f"  Answer ({len(ans)} chars): {ans[:300]}")
