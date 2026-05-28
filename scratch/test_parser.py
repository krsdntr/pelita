import urllib.request
from bs4 import BeautifulSoup
import json
import re

url = "https://www.imankatolik.or.id/alkitab.php?k=kej&b=1"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # The text structure on imankatolik is usually in a list or table or just plain paragraphs.
        # Often it uses <tr> with <td> for verse number and <td> for text.
        # Let's find all rows.
        verses = []
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 2:
                # possible verse row
                num_text = tds[0].text.strip()
                if re.match(r'^\d+$', num_text) or re.match(r'^\d+\w?$', num_text):
                    verse_text = tds[1].text.strip()
                    verses.append({"verse": num_text, "text": verse_text})
        
        # fallback if not in tr/td
        if not verses:
            for b in soup.find_all('b'):
                # sometimes verse numbers are bold
                num = b.text.strip()
                if re.match(r'^\d+$', num):
                    text_node = b.next_sibling
                    if text_node and isinstance(text_node, str):
                        verses.append({"verse": num, "text": text_node.strip()})

        print(json.dumps(verses[:5], indent=2))
        print(f"Total verses extracted: {len(verses)}")

except Exception as e:
    print(f"Error: {e}")
