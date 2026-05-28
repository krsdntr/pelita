import os

src_dir = r"d:\app\alkitab\src"
matches = []

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith(".astro"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                if "StoryReader" in content or "story-reader" in content:
                    matches.append(path)

print("Matches:")
for m in matches:
    print(m)
