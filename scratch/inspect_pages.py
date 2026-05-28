import pypdf

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
reader = pypdf.PdfReader(pdf_path)

print("--- Pages 30 to 50 Detailed text ---")
for p in range(30, 50):
    text = reader.pages[p].extract_text()
    print(f"=== PAGE {p+1} ===")
    print(text[:1500]) # First 1500 characters
    print("\n" + "="*40 + "\n")
