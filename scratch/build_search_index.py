"""
Builds a lightweight search index for the Bible app.
Strategy: store only first 120 chars of each verse, plus book/chapter/verse reference.
This keeps total index size minimal for on-demand loading.
"""
import json
import os
import glob

books_dir = 'd:/app/alkitab/src/data/books/'
metadata_path = 'd:/app/alkitab/src/data/bible-metadata.json'
output_path = 'd:/app/alkitab/src/data/search-index.json'

with open(metadata_path, 'r', encoding='utf-8') as f:
    book_meta = json.load(f)

book_name_map = {b['id']: b['name'] for b in book_meta}

index = []
total_verses = 0

for book in book_meta:
    book_id = book['id']
    book_name = book['name']
    filepath = os.path.join(books_dir, f"{book_id}.json")
    
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        chapters = json.load(f)
    
    for ch in chapters:
        chapter_num = ch.get('chapter')
        for v in ch.get('verses', []):
            verse_num = v.get('verse')
            verse_text = v.get('text', '').strip()
            
            if not verse_text or verse_text == "Teks sedang diunduh atau tidak tersedia untuk saat ini.":
                continue
            
            # Truncate text to 140 chars for index (enough to show context)
            snippet = verse_text[:140] + ('…' if len(verse_text) > 140 else '')
            
            index.append({
                "b": book_id,       # book id
                "n": book_name,     # book name
                "c": chapter_num,   # chapter
                "v": verse_num,     # verse
                "t": snippet        # text snippet
            })
            total_verses += 1

print(f"Total indexed verses: {total_verses}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, separators=(',', ':'))  # compact format

size_kb = os.path.getsize(output_path) / 1024
print(f"Index size: {size_kb:.1f} KB")
print("Done!")
