import urllib.request
import urllib.parse

url = "https://www.imankatolik.or.id/alkitab.php?k=kej&b=1"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    with open('d:/app/alkitab/scratch/test_alkitab.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved to scratch/test_alkitab.html")
