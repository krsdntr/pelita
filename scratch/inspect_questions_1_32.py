import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
reader = pypdf.PdfReader(pdf_path)

output_file = r"d:\app\alkitab\scratch\pages_15_30.txt"
print(f"Extracting pages 15 to 30 to {output_file}...")

with open(output_file, "w", encoding="utf-8") as f:
    for p in range(14, 30):
        text = reader.pages[p].extract_text()
        f.write(f"=== PAGE {p+1} ===\n")
        f.write(text)
        f.write("\n\n" + "="*40 + "\n\n")

print("Done!")
