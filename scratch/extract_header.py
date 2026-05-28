import re

with open('d:/app/alkitab/dist/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<header class="sacred-topbar".*?</header>', text, re.DOTALL)
if match:
    with open('d:/app/alkitab/scratch/extracted_header.html', 'w', encoding='utf-8') as out:
        out.write(match.group(0))
    print('Found header')
else:
    print('Not found')
