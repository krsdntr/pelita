import os
import json

books_dir = "d:/app/alkitab/src/data/books"
truncated = []

for filename in os.listdir(books_dir):
    if not filename.endswith('.json'):
        continue
    filepath = os.path.join(books_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            chapters = json.load(f)
            for ch_data in chapters:
                chapter = ch_data.get('chapter')
                verses = ch_data.get('verses', [])
                if len(verses) == 60:
                    # Let's check if the last verse is literally verse '60'
                    if verses[-1].get('verse') == '60':
                        truncated.append((filename.replace('.json', ''), chapter, len(verses)))
        except Exception as e:
            print(f"Error reading {filename}: {e}")

print(f"Found {len(truncated)} potentially truncated chapters:")
for item in truncated:
    print(f"  Kitab: {item[0]}, Bab: {item[1]}, Jumlah Ayat: {item[2]}")
