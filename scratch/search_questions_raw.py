import re

with open(r"d:\app\alkitab\scratch\full_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

ids_to_find = [101, 189, 234, 337, 462, 577, 107, 111, 119, 343, 350, 356, 458, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598]

with open(r"d:\app\alkitab\scratch\search_results.txt", "w", encoding="utf-8") as out:
    for q_id in ids_to_find:
        # search for e.g. "101." or "101 ." or similar
        pattern = rf'\b{q_id}\b\s*\.\s*(.*?)(?=\n|$)'
        matches = list(re.finditer(pattern, text))
        out.write(f"--- Q{q_id} matches ({len(matches)}) ---\n")
        for idx, m in enumerate(matches):
            start = max(0, m.start() - 100)
            end = min(len(text), m.end() + 1000)
            out.write(f"Match {idx+1} at index {m.start()}:\n")
            out.write(text[start:end])
            out.write("\n" + "="*60 + "\n")
