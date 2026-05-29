import urllib.request
from bs4 import BeautifulSoup
import json
import os
import re
import time

ID_MAPPING = {
    "maz": "mzm",
    "yud": "ydt",
    "yoel": "yl",
    "amos": "am",
    "mik": "mi",
    "zak": "za",
    "yud-sb": "yud",
    "t-est": "est",
    "t-dan": "dan",
}

# The list of 33 truncated chapters (originally found to have exactly 60 verses)
TRUNCATED = [
    ("1mak", 1), ("1mak", 2), ("1mak", 3), ("1mak", 4), ("1mak", 5), 
    ("1mak", 6), ("1mak", 9), ("1mak", 10), ("1mak", 11), ("1raj", 8), 
    ("1taw", 6), ("bil", 7), ("bil", 26), ("dan", 3), ("ezr", 2), 
    ("kej", 24), ("kis", 7), ("luk", 1), ("luk", 9), ("luk", 22), 
    ("mat", 26), ("mat", 27), ("maz", 78), ("maz", 119), ("mrk", 14), 
    ("neh", 7), ("rat", 3), ("t-dan", 3), ("ul", 28), ("yeh", 16), 
    ("yer", 51), ("yoh", 6), ("yos", 15)
]

def fetch_verses_in_blocks(book_im, chapter):
    verses = []
    a1 = 1
    a2 = 60
    
    while True:
        url = f"https://www.imankatolik.or.id/alkitab.php?k={book_im}&b={chapter}&a1={a1}&a2={a2}"
        print(f"  Fetching: {url}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        block_verses = []
        
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                html = response.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                
                tds_v = soup.find_all('td', class_='v')
                
                for i in range(0, len(tds_v)-1, 2):
                    ref_td = tds_v[i]
                    text_td = tds_v[i+1]
                    
                    ref_text = ref_td.text.strip().replace('\xa0', ' ')
                    match = re.search(r':(\d+[a-zA-Z]*)$', ref_text)
                    if match:
                        verse_num = match.group(1)
                        verse_text = text_td.text.strip()
                        block_verses.append({"verse": verse_num, "text": verse_text})
        except Exception as e:
            print(f"    Error: {e}")
            break
            
        if not block_verses:
            break
            
        verses.extend(block_verses)
        print(f"    Found {len(block_verses)} verses in this block (Total so far: {len(verses)})")
        
        # If we got less than 60 verses, it means we reached the end of the chapter
        if len(block_verses) < 60:
            break
            
        a1 += 60
        a2 += 60
        time.sleep(0.3) # Stagger slightly
        
    return verses

def main():
    print(f"Starting to fix {len(TRUNCATED)} truncated chapters...")
    
    for book_id, chapter in TRUNCATED:
        book_im = ID_MAPPING.get(book_id, book_id)
        print(f"\nProcessing {book_id} Bab {chapter}...")
        
        # Fetch the complete verses
        full_verses = fetch_verses_in_blocks(book_im, chapter)
        
        if not full_verses:
            print(f"WARNING: No verses fetched for {book_id} Bab {chapter}. Skipping update.")
            continue
            
        # Update local file
        filepath = f"d:/app/alkitab/src/data/books/{book_id}.json"
        if not os.path.exists(filepath):
            print(f"WARNING: File {filepath} does not exist. Skipping update.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                book_data = json.load(f)
            except Exception as e:
                print(f"ERROR: Could not parse {filepath}: {e}")
                continue
                
        # Find and update the chapter
        updated = False
        for ch_data in book_data:
            if ch_data.get('chapter') == chapter:
                old_count = len(ch_data.get('verses', []))
                ch_data['verses'] = full_verses
                print(f"SUCCESS: Updated {book_id} Bab {chapter} from {old_count} verses to {len(full_verses)} verses!")
                updated = True
                break
                
        if not updated:
            print(f"WARNING: Chapter {chapter} not found in {filepath}. Appending new chapter.")
            book_data.append({
                "chapter": chapter,
                "verses": full_verses
            })
            
        # Save back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, indent=2, ensure_ascii=False)
            
        time.sleep(0.5)

    print("\nAll truncated chapters have been fixed and updated!")

if __name__ == '__main__':
    main()
