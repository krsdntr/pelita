import re

try:
    with open('d:/app/alkitab/dist/index.html', 'r', encoding='utf-8') as f:
        text = f.read()

    match = re.search(r'<header class="stats-header.*?.*?</header>', text, re.DOTALL)
    if match:
        with open('d:/app/alkitab/scratch/extracted_header.html', 'w', encoding='utf-8') as out:
            out.write(match.group(0))
        print('Found HTML')
    else:
        print('Not found')
        
    # Also extract JS and CSS if possible
    # Just grab all script tags
    scripts = re.findall(r'<script.*?>.*?</script>', text, re.DOTALL)
    with open('d:/app/alkitab/scratch/extracted_scripts.html', 'w', encoding='utf-8') as out:
        out.write('\n\n'.join(scripts))
except Exception as e:
    print(e)
