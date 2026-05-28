"""
Comprehensive fix script for catechism-compendium.json:
1. Fix Q587-Q598 which have contaminated/missing answers
2. Fill in 166 empty reflections
3. Output a clean, complete database

Uses Gemini API to reconstruct authoritative content from KKGK.
"""
import json
import urllib.request
import urllib.error
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# ===== CONFIGURATION =====
API_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
MODEL_NAME = "gemini-2.0-flash"

CURRENT_DB_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"
PROGRESS_PATH = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
OUTPUT_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"

# ===== LOAD DATA =====
print("Loading current database...")
with open(CURRENT_DB_PATH, "r", encoding="utf-8") as f:
    current_db = json.load(f)

# Flatten all questions
all_questions_by_id = {}
for pillar in current_db:
    for q in pillar["questions"]:
        all_questions_by_id[q["id"]] = dict(q)
        all_questions_by_id[q["id"]]["pillar"] = pillar["pillar"]

# Load existing progress
processed = {}
if os.path.exists(PROGRESS_PATH):
    with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
        raw_progress = json.load(f)
    processed = {int(k): v for k, v in raw_progress.items()}
    print(f"Loaded {len(processed)} already-processed questions from progress file.")

# ===== IDENTIFY ISSUES =====

# Questions needing fix: 
# 1. Empty reflections (166 questions)
# 2. Contaminated/truncated answers (Q587-Q598 and others)
# 3. Empty answers (6 questions)

CONTAMINATED_Q = {587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 100, 107, 111, 119, 343, 350, 356, 458, 563}
EMPTY_ANS_Q = {101, 189, 234, 337, 462, 577}

questions_to_fix = set()
for qid, q in all_questions_by_id.items():
    if not q.get("reflection", "").strip():
        questions_to_fix.add(qid)
    if qid in CONTAMINATED_Q or qid in EMPTY_ANS_Q:
        questions_to_fix.add(qid)

print(f"\nTotal questions to fix: {len(questions_to_fix)}")
print(f"Already in progress file: {len([q for q in questions_to_fix if q in processed])}")

# Remove from processed those that are contaminated/empty (force re-generation)
for qid in CONTAMINATED_Q | EMPTY_ANS_Q:
    if qid in processed:
        print(f"  Removing Q{qid} from progress (contaminated/empty, needs re-gen)...")
        del processed[qid]

remaining = sorted(questions_to_fix - set(processed.keys()))
print(f"Questions still needing processing: {len(remaining)}")
print(f"First 20: {remaining[:20]}")

# ===== GEMINI API CALL =====
def call_gemini(batch_questions, retry=0):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    prompt = f"""Anda adalah seorang ahli Teologi Katolik terkemuka dan penulis refleksi spiritual.

Berikut adalah daftar pertanyaan dari Kompendium Katekismus Gereja Katolik (KKGK) Bahasa Indonesia yang perlu Anda perbaiki dan lengkapi:

{json.dumps(batch_questions, ensure_ascii=False, indent=2)}

Tugas Anda untuk SETIAP pertanyaan:
1. Berikan teks PERTANYAAN yang bersih dan lengkap dalam Bahasa Indonesia resmi sesuai KKGK
2. Berikan JAWABAN resmi KKGK yang lengkap, akurat, dan bersih dalam Bahasa Indonesia (bukan terjemahan kasar, melainkan teks resmi yang sudah dipoles)
3. Berikan nomor REFERENSI paragraf resmi KGK/CCC yang tepat (format: "KGK xxx" atau "KGK xxx-yyy")
4. Berikan 2 kalimat REFLEKSI pastoral yang indah, mendalam, dan aplikatif untuk kehidupan Kristiani modern

PENTING untuk jawaban: 
- Jangan sertakan teks bahasa Italia atau Latin dalam jawaban
- Jangan sertakan teks dari lampiran atau bagian doa liturgi yang tidak relevan
- Gunakan pengetahuan Anda tentang Kompendium Katekismus Gereja Katolik (2005) untuk mengisi/memperbaiki jawaban
- Jawaban harus sesuai dengan ajaran resmi Gereja Katolik

Kembalikan hasilnya dalam format JSON array.
"""
    
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
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
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        if retry < 3:
            backoff = (2 ** retry) * 8
            print(f"Retrying in {backoff} seconds...")
            time.sleep(backoff)
            return call_gemini(batch_questions, retry + 1)
        return None

# ===== PROCESS =====
batch_size = 15  # Smaller batches for accuracy
remaining_list = remaining[:]
total_fixed = 0

print(f"\n{'='*60}")
print(f"Starting to process {len(remaining_list)} questions...")
print(f"{'='*60}")

i = 0
while i < len(remaining_list):
    batch_ids = remaining_list[i:i+batch_size]
    
    batch_data = []
    for qid in batch_ids:
        q = all_questions_by_id.get(qid, {})
        batch_data.append({
            "id": qid,
            "question": q.get("question", ""),
            "answer": q.get("answer", ""),
            "current_reflection": q.get("reflection", ""),
            "note": "FIX_NEEDED" if qid in CONTAMINATED_Q or qid in EMPTY_ANS_Q else "ADD_REFLECTION_ONLY"
        })
    
    print(f"\nProcessing batch {i//batch_size + 1}: Q{batch_ids[0]}-Q{batch_ids[-1]} ({len(batch_data)} questions)...")
    
    results = call_gemini(batch_data)
    
    if results:
        for r in results:
            q_id = int(r.get("id", 0))
            if q_id in questions_to_fix:
                processed[q_id] = r
                total_fixed += 1
        
        # Save progress after each batch
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ Saved progress. Total fixed so far: {total_fixed}")
        time.sleep(4)  # Rate limit friendly
    else:
        print(f"  ✗ Batch failed. Waiting 15s before retrying...")
        time.sleep(15)
        continue  # Retry same batch
    
    i += batch_size

# ===== RECONSTRUCT FINAL DATABASE =====
print(f"\n{'='*60}")
print("Reconstructing final clean database...")
print(f"{'='*60}")

final_db = []
for pillar in current_db:
    p_questions = []
    for q in pillar["questions"]:
        qid = q["id"]
        if qid in processed:
            fixed = processed[qid]
            p_questions.append({
                "id": qid,
                "question": fixed.get("question", q["question"]),
                "answer": fixed.get("answer", q["answer"]),
                "reference": fixed.get("reference", q.get("reference", f"KGK {qid}")),
                "reflection": fixed.get("reflection", q.get("reflection", ""))
            })
        else:
            p_questions.append({
                "id": qid,
                "question": q["question"],
                "answer": q["answer"],
                "reference": q.get("reference", f"KGK {qid}"),
                "reflection": q.get("reflection", "")
            })
    
    final_db.append({
        "pillar": pillar["pillar"],
        "pillarTitle": pillar["pillarTitle"],
        "color": pillar["color"],
        "questions": p_questions
    })

# Count issues remaining
empty_ans = sum(1 for p in final_db for q in p["questions"] if not q["answer"].strip())
empty_ref = sum(1 for p in final_db for q in p["questions"] if not q["reflection"].strip())
print(f"\nFinal stats:")
print(f"  Questions with empty answers: {empty_ans}")
print(f"  Questions with empty reflections: {empty_ref}")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"\n✅ SUCCESS! Clean database written to {OUTPUT_PATH}")
print(f"   Total questions: {sum(len(p['questions']) for p in final_db)}")
