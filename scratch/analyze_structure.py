import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

raw_text_file = r"d:\app\alkitab\scratch\full_raw_text.txt"

with open(raw_text_file, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find all numbered lines
lines = content.split('\n')
numbered_lines = []
for i, line in enumerate(lines):
    match = re.match(r'^\s*(\d+)\.\s*(.*)', line)
    if match:
        num = int(match.group(1))
        text = match.group(2).strip()
        # Keep track of line index, number, and text
        numbered_lines.append((i, num, text, line))

print(f"Total numbered lines found: {len(numbered_lines)}")

# Print some of them
print("\nFirst 40 numbered lines:")
for idx, num, text, line in numbered_lines[:40]:
    print(f"Line {idx}: [{num}] {text[:80]}")

# Let's inspect how many unique question numbers from 1 to 598 we can find
unique_nums = set()
for _, num, _, _ in numbered_lines:
    unique_nums.add(num)

print(f"\nUnique question numbers found: {len(unique_nums)} / 598")

missing = [n for n in range(1, 599) if n not in unique_nums]
print(f"Missing numbers: {missing[:50]} ... ({len(missing)} missing in total)")
