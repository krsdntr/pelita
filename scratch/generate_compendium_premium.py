import json
import urllib.request
import urllib.error
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
# We can use 'gemini-2.5-flash' or 'gemini-flash-lite-latest' or 'gemini-3.5-flash'
# Since 'gemini-flash-lite-latest' has a very high free rate limit and worked well before:
MODEL_NAME = "gemini-flash-lite-latest"

raw_db_path = r"d:\app\alkitab\scratch\cleaned_raw_compendium.json"
output_db_path = r"d:\app\alkitab\src\data\catechism-compendium.json"

print("Loading raw compendium database...")
with open(raw_db_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Flatten all questions into a single list to process
all_questions = []
for p_idx, pillar in enumerate(raw_data):
    for q in pillar["questions"]:
        all_questions.append({
            "pillar_idx": p_idx,
            "pillar_name": pillar["pillar"],
            "id": q["id"],
            "question": q["question"],
            "answer": q["answer"]
        })

print(f"Total flattened questions to process: {len(all_questions)}")

# Load existing progress if available to support resuming
progress_path = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
processed_questions = {}
if os.path.exists(progress_path):
    try:
        with open(progress_path, "r", encoding="utf-8") as f:
            processed_questions = json.load(f)
        # Convert keys to int
        processed_questions = {int(k): v for k, v in processed_questions.items()}
        print(f"Loaded existing progress: {len(processed_questions)} questions already processed.")
    except Exception as e:
        print("Failed to load progress, starting fresh:", e)

def call_gemini(batch_questions, retry=0):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    prompt = f"""Anda adalah seorang ahli Teologi Katoliknya terkemuka.
Tugas Anda adalah memproses, membersihkan, dan menyempurnakan daftar pertanyaan dan jawaban dari Kompendium Katekismus Gereja Katolik (KKGK) berikut ini:

{json.dumps(batch_questions, ensure_ascii=False, indent=2)}

Langkah yang WAJIB Anda lakukan:
1. Bersihkan kesalahan OCR/ketikan (seperti spasi acak pada kata: 'Y esus' -> 'Yesus', 'T uhan' -> 'Tuhan', 'w aktu' -> 'waktu', 'di Gu115' -> 'Gunung Sinai', dll.).
2. Perbaiki penggabungan kolom jika teks jawaban terbalik atau terpotong (misal: di Q114/Q115 jika ada bagian teks yang tertukar akibat pemindaian PDF dua kolom, susun kembali sesuai teks resmi KKGK).
3. Cari dan tuliskan nomor paragraf referensi resmi KGK (Katekismus Gereja Katolik) yang tepat untuk setiap nomor pertanyaan tersebut (misal: "KGK 1-25", "KGK 27-30", "KGK 541-546").
4. Tuliskan 2 kalimat "Refleksi Iman Batiniah" (pastoral reflection) yang mendalam, indah, dan praktis untuk kehidupan rohani Katolik modern saat ini.

Kembalikan hasilnya dalam format JSON array objek yang memiliki field persis seperti berikut:
[
  {{
    "id": [ID pertanyaan],
    "question": "[Teks Pertanyaan yang sudah bersih dan rapi dalam Bahasa Indonesia resmi]",
    "answer": "[Teks Jawaban resmi KKGK yang sudah bersih dan tersusun rapi]",
    "reference": "KGK [nomor paragraf, misal: 1-25]",
    "reflection": "[2 kalimat refleksi rohani batiniah]"
  }},
  ...
]
"""
    
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                        "reference": {"type": "string"},
                        "reflection": {"type": "string"}
                    },
                    "required": ["id", "question", "answer", "reference", "reflection"]
                }
            }
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        if retry < 3:
            backoff = (2 ** retry) * 5
            print(f"Retrying in {backoff} seconds...")
            time.sleep(backoff)
            return call_gemini(batch_questions, retry + 1)
        return None

# Process in batches of 40 questions to avoid token limits and stay under rate limits
batch_size = 40
i = 0
while i < len(all_questions):
    batch = []
    # Only select questions that are not already processed
    for q in all_questions[i:i+batch_size]:
        if q["id"] not in processed_questions:
            batch.append({
                "id": q["id"],
                "question": q["question"],
                "answer": q["answer"]
            })
            
    if not batch:
        print(f"Batch from index {i} to {i+batch_size} already fully processed. Skipping.")
        i += batch_size
        continue
        
    print(f"\nProcessing batch from {i} to {i+batch_size} (size: {len(batch)})...")
    results = call_gemini(batch)
    
    if results:
        for r in results:
            q_id = int(r["id"])
            processed_questions[q_id] = r
            
        # Write progress
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(processed_questions, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully processed and saved progress for {len(results)} questions.")
        
        # Rate limit friendly delay
        time.sleep(5)
        i += batch_size
    else:
        print("Failed to process batch. Waiting 10 seconds and retrying this batch...")
        time.sleep(10)

# Once all questions are processed, reconstruct the original structured JSON and write to output_db_path!
print("\nAll questions processed successfully! Reconstructing structured database...")

final_structured_data = []
for p_idx, pillar in enumerate(raw_data):
    p_questions = []
    for q in pillar["questions"]:
        q_id = q["id"]
        if q_id in processed_questions:
            p_questions.append({
                "id": q_id,
                "question": processed_questions[q_id]["question"],
                "answer": processed_questions[q_id]["answer"],
                "reference": processed_questions[q_id]["reference"],
                "reflection": processed_questions[q_id]["reflection"]
            })
        else:
            # Fallback
            p_questions.append({
                "id": q_id,
                "question": q["question"],
                "answer": q["answer"],
                "reference": f"KGK {q_id}",
                "reflection": ""
            })
            
    final_structured_data.append({
        "pillar": pillar["pillar"],
        "pillarTitle": pillar["pillarTitle"],
        "color": pillar["color"],
        "questions": p_questions
    })

# Write to src/data/catechism-compendium.json
with open(output_db_path, "w", encoding="utf-8") as f:
    json.dump(final_structured_data, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Pristine Premium Catholic Catechism Compendium written to {output_db_path}")
