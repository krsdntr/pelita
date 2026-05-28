"""
Build per-book mini search indexes.
Strategy: One tiny JSON per book with just (chapter, verse, first_80_chars).
User types -> we lazy-load only books that match the search term.

Also build a tiny metadata index: [{b, n, firstVerse}] for fast book-level search.
"""
import json
import os

books_dir = 'd:/app/alkitab/src/data/books/'
metadata_path = 'd:/app/alkitab/src/data/bible-metadata.json'
output_dir = 'd:/app/alkitab/public/search/'

os.makedirs(output_dir, exist_ok=True)

with open(metadata_path, 'r', encoding='utf-8') as f:
    book_meta = json.load(f)

# Build a tiny book-level manifest listing books + their first verse (for instant search of book names)
manifest = []

for book in book_meta:
    book_id = book['id']
    book_name = book['name']
    filepath = os.path.join(books_dir, f"{book_id}.json")
    
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        chapters = json.load(f)
    
    # Build per-book mini index: list of [chapter, verse, text_snippet]
    entries = []
    for ch in chapters:
        chapter_num = ch.get('chapter')
        for v in ch.get('verses', []):
            verse_num = v.get('verse')
            text = v.get('text', '').strip()
            
            if not text or 'sedang diunduh' in text:
                continue
            
            snippet = text[:100] + ('…' if len(text) > 100 else '')
            entries.append([chapter_num, verse_num, snippet])
    
    # Save per-book index to public/search/{book_id}.json
    book_index_path = os.path.join(output_dir, f"{book_id}.json")
    with open(book_index_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, separators=(',', ':'))
    
    size_kb = os.path.getsize(book_index_path) / 1024
    
    # Add to manifest
    first_verse = entries[0][2] if entries else ''
    manifest.append({"id": book_id, "name": book_name, "count": len(entries)})
    print(f"  {book_name}: {len(entries)} verses, {size_kb:.1f}KB")

# Save manifest
manifest_path = os.path.join(output_dir, 'manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, separators=(',', ':'))

print(f"\nManifest: {os.path.getsize(manifest_path)} bytes")
print(f"Done! Per-book indexes saved to {output_dir}")
