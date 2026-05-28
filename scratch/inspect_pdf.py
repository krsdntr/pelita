import pypdf
import sys

pdf_path = r"d:\app\alkitab\archive_compendium-ccc_id.pdf"
print("Opening PDF...")
reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total pages: {total_pages}")

# Let's search for "Kompendium" or look at the first few pages
print("\n--- Inspecting first 15 pages ---")
for i in range(min(15, total_pages)):
    text = reader.pages[i].extract_text()
    first_few_chars = text[:200].replace('\n', ' ')
    print(f"Page {i+1}: {first_few_chars}...")

# Let's search for "1." or "PERTANYAAN" to find where Q&A starts
print("\n--- Searching for questions ---")
found = 0
for i in range(total_pages):
    text = reader.pages[i].extract_text()
    if "rencana Allah" in text.lower() or "diciptakan" in text.lower():
        print(f"Page {i+1} might contain Q&As! Found 'rencana Allah' or 'diciptakan'. Snippet:")
        print(text[:500])
        found += 1
        if found >= 3:
            break
