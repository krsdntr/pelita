import pypdf
import sys

# Reconfigure stdout to support utf-8 just in case
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
reader = pypdf.PdfReader(pdf_path)

output_file = r"d:\app\alkitab\scratch\pages_30_60.txt"
print(f"Extracting pages 30 to 60 and writing to {output_file}...")

with open(output_file, "w", encoding="utf-8") as f:
    for p in range(30, 60):
        text = reader.pages[p].extract_text()
        f.write(f"=== PAGE {p+1} ===\n")
        f.write(text)
        f.write("\n\n" + "="*40 + "\n\n")

print("Done! File written successfully.")
