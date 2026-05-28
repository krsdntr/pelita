"""
Conservative fix script: 1 request per 70 seconds to stay under Gemini free-tier RPM limit.
Rotates between gemini-2.0-flash and gemini-2.0-flash-lite to spread load.
Saves progress after every single batch.
"""
import json
import urllib.request
import urllib.error
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

GEMINI_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
MODELS = ["gemini-2.0-flash", "gemini-2.0-flash-lite"]

CURRENT_DB_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"
PROGRESS_PATH   = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
OUTPUT_PATH     = r"d:\app\alkitab\src\data\catechism-compendium.json"

FORCE_REGEN_IDS = {
    101, 189, 234, 337, 462, 577,
    587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598,
    107, 111, 119, 343, 350, 356, 458,
}

# ===== LOAD =====
print("Loading...", flush=True)
with open(CURRENT_DB_PATH, "r", encoding="utf-8") as f:
    current_db = json.load(f)

all_q = {}
for pillar in current_db:
    for q in pillar["questions"]:
        all_q[q["id"]] = dict(q)

with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
    processed = {int(k): v for k, v in json.load(f).items()}

for qid in FORCE_REGEN_IDS:
    processed.pop(qid, None)

to_fix = sorted([
    qid for qid in range(1, 599)
    if (not all_q.get(qid, {}).get("reflection", "").strip() or qid in FORCE_REGEN_IDS)
    and qid not in processed
])
print(f"To fix: {len(to_fix)} questions", flush=True)

def save():
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

def call_gemini(prompt, schema, model_idx=0):
    model = MODELS[model_idx % len(MODELS)]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            res = json.loads(r.read().decode())
            return json.loads(res["candidates"][0]["content"]["parts"][0]["text"]), model
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()[:300]
        print(f"  {model} HTTP {e.code}: {body_err[:100]}", flush=True)
        if e.code == 429 and model_idx < len(MODELS) * 2:
            # Try next model
            next_idx = model_idx + 1
            if next_idx < len(MODELS):
                print(f"  Switching to {MODELS[next_idx]}...", flush=True)
                time.sleep(5)
                return call_gemini(prompt, schema, next_idx)
            else:
                # All models 429 — wait a full minute
                print(f"  All models rate-limited. Waiting 70s...", flush=True)
                time.sleep(70)
                return call_gemini(prompt, schema, 0)
        return None, model
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}", flush=True)
        return None, model

arr_schema = lambda props: {
    "type": "array",
    "items": {"type": "object", "properties": props, "required": list(props.keys())}
}

FULL_SCHEMA = arr_schema({
    "id": {"type": "integer"},
    "question": {"type": "string"},
    "answer": {"type": "string"},
    "reference": {"type": "string"},
    "reflection": {"type": "string"}
})
REFLECT_SCHEMA = arr_schema({
    "id": {"type": "integer"},
    "reflection": {"type": "string"}
})

phase1 = sorted([q for q in to_fix if q in FORCE_REGEN_IDS])
phase2 = sorted([q for q in to_fix if q not in FORCE_REGEN_IDS])
total_batches = len(phase1) // 5 + 1 + len(phase2) // 15 + 1

print(f"\n=== PHASE 1: Full reconstruction — {len(phase1)} Q ===", flush=True)
model_counter = 0
BATCH1 = 5
for i in range(0, len(phase1), BATCH1):
    batch_ids = phase1[i:i+BATCH1]
    already = [q for q in batch_ids if q in processed]
    batch_ids = [q for q in batch_ids if q not in processed]
    if not batch_ids:
        continue

    batch_data = [{"id": qid, "question": all_q.get(qid, {}).get("question", ""), "answer": all_q.get(qid, {}).get("answer", "")} for qid in batch_ids]
    done_total = sum(1 for q in range(1, 599) if q in processed)
    print(f"\n  [{done_total}/598] Batch {i//BATCH1+1}: Q{batch_ids[0]}-Q{batch_ids[-1]}...", flush=True)

    prompt = f"""Anda ahli Teologi Katolik. Berikut pertanyaan dari KKGK (Kompendium Katekismus Gereja Katolik edisi Indonesia 2005) yang rusak akibat ekstraksi PDF.

Rekonstruksi setiap item:
1. question: teks pertanyaan KKGK yang benar & lengkap dalam Bahasa Indonesia
2. answer: jawaban resmi KKGK yang lengkap & bersih (TANPA teks Latin/Italia/Lampiran/doa liturgi)
3. reference: nomor paragraf KGK tepat (format: "KGK xxx" atau "KGK xxx-yyy")
4. reflection: 2 kalimat refleksi pastoral yang indah & aplikatif untuk Kristiani modern

Konteks:
- Q587-Q598: tentang 7 permohonan Doa Bapa Kami (Bagian Empat KKGK, KGK 2759-2865)
- Q101: misteri hidup Kristus (KGK 514-521)
- Q189: kaum awam dan imamat Kristus (KGK 897-913)
- Q234: liturgi surgawi (KGK 1137-1139)
- Q337: rencana Allah tentang laki-laki dan perempuan (KGK 1601-1605)
- Q462: keluarga dan kebaikan absolut (KGK 2201-2206)
- Q577: doa Saat Yesus (KGK 2603-2606)

Input (mungkin rusak):
{json.dumps(batch_data, ensure_ascii=False)}

Kembalikan JSON array dengan field: id, question, answer, reference, reflection."""

    results, used_model = call_gemini(prompt, FULL_SCHEMA, model_counter % len(MODELS))
    model_counter += 1
    
    if results:
        for r in results:
            processed[int(r["id"])] = r
        save()
        print(f"  ✓ {len(results)} Q fixed via {used_model}", flush=True)
    else:
        print(f"  ✗ Skipping batch.", flush=True)

    if i + BATCH1 < len(phase1):
        print(f"  Sleeping 70s (rate limit)...", flush=True)
        time.sleep(70)

print(f"\n=== PHASE 2: Reflections only — {len(phase2)} Q ===", flush=True)
BATCH2 = 15
for i in range(0, len(phase2), BATCH2):
    batch_ids = [q for q in phase2[i:i+BATCH2] if q not in processed]
    if not batch_ids:
        continue

    batch_data = [{"id": qid, "question": all_q.get(qid, {}).get("question", ""), "answer": all_q.get(qid, {}).get("answer", "")[:400]} for qid in batch_ids]
    done_total = sum(1 for q in range(1, 599) if q in processed)
    print(f"\n  [{done_total}/598] Batch {i//BATCH2+1}: Q{batch_ids[0]}-Q{batch_ids[-1]} ({len(batch_ids)} Q)...", flush=True)

    prompt = f"""Anda penulis refleksi spiritual Katolik berpengalaman.

Untuk setiap Q&A dari Kompendium Katekismus Gereja Katolik berikut, tuliskan 2 kalimat "Refleksi Iman Batiniah" yang:
- Mendalam secara teologis dan pastoral
- Aplikatif untuk kehidupan Kristiani modern
- Indah dan menyentuh hati

Input:
{json.dumps(batch_data, ensure_ascii=False)}

Kembalikan JSON array dengan field: id (integer), reflection (string, tepat 2 kalimat)."""

    results, used_model = call_gemini(prompt, REFLECT_SCHEMA, model_counter % len(MODELS))
    model_counter += 1

    if results:
        for r in results:
            qid = int(r["id"])
            q = all_q.get(qid, {})
            processed[qid] = {
                "id": qid,
                "question": q.get("question", ""),
                "answer": q.get("answer", ""),
                "reference": q.get("reference", f"KGK {qid}"),
                "reflection": r.get("reflection", "")
            }
        save()
        done_total = sum(1 for q in range(1, 599) if q in processed)
        print(f"  ✓ {len(results)} reflections via {used_model} | Total: {done_total}/598", flush=True)
    else:
        print(f"  ✗ Skipping.", flush=True)

    if i + BATCH2 < len(phase2):
        print(f"  Sleeping 70s...", flush=True)
        time.sleep(70)

# ===== BUILD FINAL DB =====
print(f"\n=== Building final database... ===", flush=True)
final_db = []
for pillar in current_db:
    pq = []
    for q in pillar["questions"]:
        qid = q["id"]
        p = processed.get(qid)
        if p:
            pq.append({
                "id": qid,
                "question": p.get("question") or q["question"],
                "answer":   p.get("answer")   or q["answer"],
                "reference": p.get("reference") or q.get("reference", f"KGK {qid}"),
                "reflection": p.get("reflection", "")
            })
        else:
            pq.append({"id": qid, "question": q["question"], "answer": q["answer"],
                       "reference": q.get("reference", f"KGK {qid}"), "reflection": q.get("reflection", "")})
    final_db.append({"pillar": pillar["pillar"], "pillarTitle": pillar["pillarTitle"],
                     "color": pillar["color"], "questions": pq})

empty_ans = sum(1 for p in final_db for q in p["questions"] if not q["answer"].strip())
empty_ref = sum(1 for p in final_db for q in p["questions"] if not q["reflection"].strip())
total     = sum(len(p["questions"]) for p in final_db)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"\n✅ SELESAI!")
print(f"   Total: {total} | Empty answers: {empty_ans} | Empty reflections: {empty_ref}")
print(f"   Output: {OUTPUT_PATH}")
