import json

with open(r"d:\app\alkitab\src\data\catholic-summaries.json", "r", encoding="utf-8") as f:
    data = json.load(f)

im = data["im"]
print("--- im keys ---")
for k in ["quote", "tagline", "overview", "author", "date", "context", "theology"]:
    print(f"[{k.upper()}]:")
    print(im[k][:300])
    print("-" * 30)
