import json
import re

json_path = 'd:/app/alkitab/src/data/catechism-compendium.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_answer(ans):
    # Pattern to match prefixes in Indonesian like "Telepon: 123-456 ", "Nomor telepon 123 ", "Tahun 123-125 ", etc.
    # also matching some standalone references if they got stuck like "1121 "
    
    # Let's loop just in case there are multiple
    while True:
        # Match starting with Telepon, Nomor telepon, Tahun, Tel., etc.
        match = re.match(r'^(?:Telepon\s*:\s*|Telepon\s+|Nomor\s+telepon\s+|Tahun\s+|Tel\.\s*)[0-9\-\,\s]+', ans, flags=re.IGNORECASE)
        if match:
            ans = ans[match.end():].strip()
            continue
            
        # Match starting with just a KGK reference number like "1121 " or "1122-1126 "
        # We should be careful to only strip it if it looks exactly like a reference (a number possibly with hyphen and commas)
        # However, to be safe, maybe we should only strip if the number matches the actual reference of the question?
        # That would be safer.
        break
        
    return ans

def clean_answer_with_ref(ans, ref_str):
    # If the answer starts with something that contains the numbers in ref_str, it's definitely a stray reference.
    ans = clean_answer(ans)
    
    # Extract all numbers from the reference string
    ref_nums = re.findall(r'\d+', ref_str)
    
    if ref_nums:
        first_num = ref_nums[0]
        # check if answer starts with this number
        pattern = r'^' + first_num + r'(?:\s*-\s*\d+)?(?:\s*,\s*\d+(?:\s*-\s*\d+)?)*\s+'
        match = re.match(pattern, ans)
        if match:
            ans = ans[match.end():].strip()
            
    # One more pass of clean_answer in case there was "Telepon 123-124 125-126"
    ans = clean_answer(ans)
    return ans

updated = 0
for pillar in data:
    for q in pillar['questions']:
        old_ans = q['answer']
        ref = q.get('reference', '')
        new_ans = clean_answer_with_ref(old_ans, ref)
        if old_ans != new_ans:
            q['answer'] = new_ans
            updated += 1
            print(f"Q{q['id']} Fixed.")
            print(f"  Old: {old_ans[:80]}")
            print(f"  New: {new_ans[:80]}")
            print("-" * 50)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total answers cleaned: {updated}")
