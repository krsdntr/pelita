import urllib.request

url = "https://www.imankatolik.or.id/alkitab.php?k=kej&b=1&a1=1&a2=200"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
        with open('d:/app/alkitab/scratch/kej1.html', 'w', encoding='utf-8') as f:
            f.write(html)
except Exception as e:
    print(f"Error: {e}")
