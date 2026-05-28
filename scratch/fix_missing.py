import urllib.request
from bs4 import BeautifulSoup
import json
import os
import re
import time
import glob

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

def fetch_chapter_with_retry(book_im, chapter, retries=3):
    url = f"https://www.imankatolik.or.id/alkitab.php?k={book_im}&b={chapter}&a1=1&a2=200"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                
                verses = []
                tds_v = soup.find_all('td', class_='v')
                for i in range(0, len(tds_v)-1, 2):
                    ref_td = tds_v[i]
                    text_td = tds_v[i+1]
                    ref_text = ref_td.text.strip().replace('\xa0', ' ')
                    match = re.search(r':(\d+[a-zA-Z]*)$', ref_text)
                    if match:
                        verse_num = match.group(1)
                        verse_text = text_td.text.strip()
                        verses.append({"verse": verse_num, "text": verse_text})
                
                if verses:
                    return verses
                else:
                    return []
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {book_im} {chapter}: {e}")
            time.sleep(2)
            
    return []

def main():
    books_dir = 'd:/app/alkitab/src/data/books/'
    files = glob.glob(os.path.join(books_dir, '*.json'))
    
    total_fixed = 0
    
    for filepath in files:
        book_id = os.path.basename(filepath).replace('.json', '')
        book_im = ID_MAPPING.get(book_id, book_id)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
            
        modified = False
        
        for ch in book_data:
            # Check if verses are missing or have the fallback text
            is_missing = False
            if not ch.get("verses") or len(ch["verses"]) == 0:
                is_missing = True
            elif len(ch["verses"]) == 1 and "Teks tidak tersedia" in ch["verses"][0].get("text", ""):
                is_missing = True
                
            if is_missing:
                print(f"Fixing missing chapter {book_id} {ch['chapter']}...")
                verses = fetch_chapter_with_retry(book_im, ch["chapter"], retries=3)
                if not verses and ch["chapter"] == 1:
                    verses = fetch_chapter_with_retry(book_im, "", retries=3)
                    
                if verses:
                    ch["verses"] = verses
                    modified = True
                    total_fixed += 1
                    print(f" -> Fixed {book_id} {ch['chapter']} (got {len(verses)} verses)")
                else:
                    print(f" -> Failed again to fetch {book_id} {ch['chapter']}")
                    
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(book_data, f, indent=2, ensure_ascii=False)
                
    print(f"Completed fixing missing chapters! Fixed {total_fixed} chapters.")

if __name__ == '__main__':
    main()
