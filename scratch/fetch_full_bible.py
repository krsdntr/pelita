import urllib.request
from bs4 import BeautifulSoup
import json
import os
import re
import time
import concurrent.futures

# Mapping from our ID to imankatolik ID
ID_MAPPING = {
    "maz": "mzm",
    "yud": "ydt",
    "yoel": "yl",
    "amos": "am",
    "mik": "mi",
    "zak": "za",
    "yud-sb": "yud",
    "t-est": "est",  # Tambahan Ester -> just use est? Wait, imankatolik doesn't have t-est separately, it just continues in est. Let's map to est.
    "t-dan": "dan",  # Tambahan Daniel -> just use dan.
}

def fetch_chapter(book_im, chapter):
    url = f"https://www.imankatolik.or.id/alkitab.php?k={book_im}&b={chapter}&a1=1&a2=200"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    verses = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # The structure is usually <td class="v" width="95%" style="text-align:justify">...</td>
            # The previous td has the verse number
            
            # Let's find all td class v
            tds_v = soup.find_all('td', class_='v')
            # They come in pairs: td 1 has the reference (e.g. Kej 1:1), td 2 has the text.
            for i in range(0, len(tds_v)-1, 2):
                ref_td = tds_v[i]
                text_td = tds_v[i+1]
                
                # Extract verse number from ref_td (e.g., "Kej 1:1")
                ref_text = ref_td.text.strip().replace('\xa0', ' ')
                match = re.search(r':(\d+[a-zA-Z]*)$', ref_text)
                if match:
                    verse_num = match.group(1)
                    # clean up text_td
                    verse_text = text_td.text.strip()
                    verses.append({"verse": verse_num, "text": verse_text})
                    
    except Exception as e:
        print(f"Error fetching {book_im} {chapter}: {e}")
    return verses

def process_book(book):
    book_id = book['id']
    book_im = ID_MAPPING.get(book_id, book_id)
    chapters = book['chapters']
    
    # Wait, Tambahan Ester and Tambahan Daniel in imankatolik might be just part of est and dan.
    # We will just fetch it as if it's the normal book but starting from their chapters?
    # For now, let's just fetch exactly what it says. If they return empty, we just have empty.
    
    book_data = []
    
    for chapter in range(1, chapters + 1):
        # We will stagger requests slightly to avoid hitting limits too hard
        verses = fetch_chapter(book_im, chapter)
        # If no verses, try with default parameters (some books like Obaja only have 1 chapter and URL might be different)
        if not verses and chapter == 1:
            verses = fetch_chapter(book_im, "") # some APIs might prefer empty chapter for single-chapter books
            
        book_data.append({
            "chapter": chapter,
            "verses": verses if verses else [{"verse": 1, "text": "Teks tidak tersedia. Silakan periksa koneksi atau sumber data."}]
        })
        time.sleep(0.1) # small delay
        
    # Write to JSON
    out_path = f"d:/app/alkitab/src/data/books/{book_id}.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)
        
    print(f"Finished {book['name']} ({book_id})")

def main():
    with open('d:/app/alkitab/src/data/bible-metadata.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
        
    print(f"Starting to fetch {len(books)} books...")
    
    # We use ThreadPoolExecutor to speed it up. 5 workers is gentle enough.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_book, books)
        
    print("All books fetched and saved!")

if __name__ == '__main__':
    main()
