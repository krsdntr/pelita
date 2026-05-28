"""
Fix script with proper rate limiting.
- Waits 30 seconds between each API call
- Processes one batch at a time
- Small batch sizes (5-10 questions)
"""
import json
import urllib.request
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
MODEL_NAME = "gemini-2.0-flash"

CURRENT_DB_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"
PROGRESS_PATH = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
OUTPUT_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"

FORCE_REGEN_IDS = {
    101, 189, 234, 337, 462, 577,
    587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598,
    107, 111, 119, 343, 350, 356, 458,
}

print("Loading databases...")
with open(CURRENT_DB_PATH, "r", encoding="utf-8") as f:
    current_db = json.load(f)

all_q_by_id = {}
for pillar in current_db:
    for q in pillar["questions"]:
        all_q_by_id[q["id"]] = dict(q)

with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
    processed = {int(k): v for k, v in json.load(f).items()}

for qid in FORCE_REGEN_IDS:
    if qid in processed:
        del processed[qid]

to_fix = sorted([
    qid for qid in range(1, 599)
    if (not all_q_by_id.get(qid, {}).get("reflection", "").strip() or qid in FORCE_REGEN_IDS)
    and qid not in processed
])
print(f"Total to fix: {len(to_fix)}")

FULL_FIX_IDS = FORCE_REGEN_IDS
REFLECT_ONLY_IDS = [qid for qid in to_fix if qid not in FULL_FIX_IDS]

def call_api(prompt, schema, retry=0):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    except urllib.error.HTTPError as e:
        if e.code == 429:
            wait = 60 * (retry + 1)
            print(f"  Rate limit! Waiting {wait}s...")
            time.sleep(wait)
            if retry < 4:
                return call_api(prompt, schema, retry + 1)
        print(f"  HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        if retry < 2:
            time.sleep(15)
            return call_api(prompt, schema, retry + 1)
        return None

arr_schema = lambda props: {
    "type": "array",
    "items": {"type": "object", "properties": props, "required": list(props.keys())}
}

def save_progress():
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

# ===== PHASE 1: Full fix for contaminated/empty questions =====
full_fix_remaining = sorted([qid for qid in FULL_FIX_IDS if qid not in processed])
print(f"\n=== PHASE 1: Full fix for {len(full_fix_remaining)} contaminated/empty Q ===")

BATCH = 5
for i in range(0, len(full_fix_remaining), BATCH):
    batch_ids = full_fix_remaining[i:i+BATCH]
    batch_data = [{"id": qid, "question": all_q_by_id.get(qid, {}).get("question", ""), "answer": all_q_by_id.get(qid, {}).get("answer", "")} for qid in batch_ids]
    
    print(f"\n  Batch {i//BATCH+1}: Q{batch_ids[0]}-Q{batch_ids[-1]}...", flush=True)
    
    prompt = f"""Anda ahli Teologi Katolik. Berikut pertanyaan dari KKGK yang rusak/tidak lengkap akibat kesalahan ekstraksi PDF.

Rekonstruksi berdasarkan pengetahuan Anda tentang Kompendium Katekismus Gereja Katolik edisi Indonesia (2005):
1. Teks pertanyaan yang benar dan lengkap dalam Bahasa Indonesia
2. Jawaban resmi yang lengkap dan bersih (TANPA teks Latin/Italia/Lampiran/doa liturgi)
3. Nomor referensi paragraf KGK yang tepat
4. 2 kalimat refleksi pastoral yang indah

Input: {json.dumps(batch_data, ensure_ascii=False)}

Catatan untuk Q587-Q598: ini tentang 7 permohonan Doa Bapa Kami (bagian keempat KKGK)."""

    schema = arr_schema({"id": {"type": "integer"}, "question": {"type": "string"}, "answer": {"type": "string"}, "reference": {"type": "string"}, "reflection": {"type": "string"}})
    
    results = call_api(prompt, schema)
    if results:
        for r in results:
            processed[int(r["id"])] = r
        save_progress()
        print(f"  ✓ {len(results)} questions fixed", flush=True)
    else:
        print(f"  ✗ Failed batch, continuing...", flush=True)
    
    if i + BATCH < len(full_fix_remaining):
        print(f"  Waiting 30s before next batch...", flush=True)
        time.sleep(30)

# ===== PHASE 2: Reflection-only for remaining 166 Q =====
reflect_remaining = [qid for qid in REFLECT_ONLY_IDS if qid not in processed]
print(f"\n=== PHASE 2: Add reflections for {len(reflect_remaining)} questions ===")

BATCH2 = 10
for i in range(0, len(reflect_remaining), BATCH2):
    batch_ids = reflect_remaining[i:i+BATCH2]
    batch_data = [{"id": qid, "question": all_q_by_id.get(qid, {}).get("question", ""), "answer": all_q_by_id.get(qid, {}).get("answer", "")[:400]} for qid in batch_ids]
    
    print(f"\n  Batch {i//BATCH2+1}: Q{batch_ids[0]}-Q{batch_ids[-1]} ({len(batch_ids)} Q)...", flush=True)
    
    prompt = f"""Anda penulis refleksi spiritual Katolik. Untuk setiap Q&A dari KKGK berikut, tuliskan 2 kalimat refleksi pastoral yang mendalam, indah, dan aplikatif untuk Kristiani modern.

Input: {json.dumps(batch_data, ensure_ascii=False)}"""

    schema = arr_schema({"id": {"type": "integer"}, "reflection": {"type": "string"}})
    
    results = call_api(prompt, schema)
    if results:
        for r in results:
            qid = int(r["id"])
            q = all_q_by_id.get(qid, {})
            processed[qid] = {
                "id": qid,
                "question": q.get("question", ""),
                "answer": q.get("answer", ""),
                "reference": q.get("reference", f"KGK {qid}"),
                "reflection": r.get("reflection", "")
            }
        save_progress()
        processed_count = sum(1 for qid in range(1, 599) if qid in processed)
        print(f"  ✓ {len(results)} reflections added | Total: {processed_count}/598", flush=True)
    else:
        print(f"  ✗ Failed, continuing...", flush=True)
    
    if i + BATCH2 < len(reflect_remaining):
        print(f"  Waiting 20s...", flush=True)
        time.sleep(20)

# ===== BUILD FINAL DATABASE =====
print(f"\n=== Building final database... ===", flush=True)

final_db = []
for pillar in current_db:
    pq = []
    for q in pillar["questions"]:
        qid = q["id"]
        if qid in processed:
            p = processed[qid]
            pq.append({
                "id": qid,
                "question": p.get("question") or q["question"],
                "answer": p.get("answer") or q["answer"],
                "reference": p.get("reference") or q.get("reference", f"KGK {qid}"),
                "reflection": p.get("reflection", "")
            })
        else:
            pq.append({"id": qid, "question": q["question"], "answer": q["answer"], "reference": q.get("reference", f"KGK {qid}"), "reflection": q.get("reflection", "")})
    final_db.append({"pillar": pillar["pillar"], "pillarTitle": pillar["pillarTitle"], "color": pillar["color"], "questions": pq})

empty_ans = sum(1 for p in final_db for q in p["questions"] if not q["answer"].strip())
empty_ref = sum(1 for p in final_db for q in p["questions"] if not q["reflection"].strip())
total = sum(len(p["questions"]) for p in final_db)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"\n✅ DONE! {total} Q | {empty_ans} empty answers | {empty_ref} empty reflections")
print(f"Output: {OUTPUT_PATH}")
