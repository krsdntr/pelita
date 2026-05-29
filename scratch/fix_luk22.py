import urllib.request
from bs4 import BeautifulSoup
import json
import os
import re

book_id = "luk"
chapter = 22
book_im = "luk"

def fetch_verses_in_blocks():
    verses = []
    a1 = 1
    a2 = 60
    
    while True:
        url = f"https://www.imankatolik.or.id/alkitab.php?k={book_im}&b={chapter}&a1={a1}&a2={a2}"
        print(f"Fetching: {url}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        block_verses = []
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
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
            print(f"Error: {e}")
            break
            
        if not block_verses:
            break
            
        verses.extend(block_verses)
        print(f"Found {len(block_verses)} verses in this block (Total so far: {len(verses)})")
        
        if len(block_verses) < 60:
            break
            
        a1 += 60
        a2 += 60
        
    return verses

def main():
    full_verses = fetch_verses_in_blocks()
    if not full_verses:
        print("Failed to fetch.")
        return
        
    filepath = f"d:/app/alkitab/src/data/books/{book_id}.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
        
    for ch_data in book_data:
        if ch_data.get('chapter') == chapter:
            old_count = len(ch_data.get('verses', []))
            ch_data['verses'] = full_verses
            print(f"SUCCESS: Updated {book_id} Bab {chapter} from {old_count} verses to {len(full_verses)} verses!")
            break
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
