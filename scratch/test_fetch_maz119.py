import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.imankatolik.or.id/alkitab.php?k=mzm&b=119&a1=61&a2=120"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        tds_v = soup.find_all('td', class_='v')
        verses = []
        for i in range(0, len(tds_v)-1, 2):
            ref_td = tds_v[i]
            text_td = tds_v[i+1]
            ref_text = ref_td.text.strip().replace('\xa0', ' ')
            match = re.search(r':(\d+[a-zA-Z]*)$', ref_text)
            if match:
                verse_num = match.group(1)
                verse_text = text_td.text.strip()
                verses.append((verse_num, verse_text))
        print(f"Total verses found for 61-120: {len(verses)}")
        if verses:
            print("First 3 verses:")
            for v in verses[:3]:
                print(f"  {v[0]}: {v[1][:60]}...")
            print("Last 3 verses:")
            for v in verses[-3:]:
                print(f"  {v[0]}: {v[1][:60]}...")
except Exception as e:
    print(f"Error: {e}")
