"""
Fix catechism compendium with multi-provider fallback:
  1. Gemini 2.0 Flash (primary)
  2. Groq llama-3.3-70b-versatile (fallback if Gemini 429)
  3. Groq gemma2-9b-it (second fallback)

Processes 166 missing reflections + 25 contaminated/empty Q.
Saves progress after every batch.
"""
import json
import urllib.request
import urllib.error
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ===== API KEYS & MODELS =====
GEMINI_KEY  = "YOUR_KEY"
GROQ_KEY    = "YOUR_KEY"

GEMINI_MODEL = "gemini-2.0-flash"
GROQ_MODELS  = ["llama-3.3-70b-versatile", "gemma2-9b-it", "llama3-70b-8192"]

CURRENT_DB_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"
PROGRESS_PATH   = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
OUTPUT_PATH     = r"d:\app\alkitab\src\data\catechism-compendium.json"

FORCE_REGEN_IDS = {
    101, 189, 234, 337, 462, 577,
    587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598,
    107, 111, 119, 343, 350, 356, 458,
}

# ===== LOAD DATA =====
print("Loading databases...")
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
print(f"Total to fix: {len(to_fix)}")
print(f"  - Full reconstruction (contaminated/empty): {len([q for q in to_fix if q in FORCE_REGEN_IDS])}")
print(f"  - Reflection only: {len([q for q in to_fix if q not in FORCE_REGEN_IDS])}")

# ===== API CALLER =====
_groq_model_idx = 0

def call_gemini(prompt, schema):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode())
            return json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise  # Signal to fallback
        print(f"  Gemini HTTP {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"  Gemini error: {e}")
        return None

def call_groq(prompt, model_idx=0):
    """Call Groq API (OpenAI-compatible). Returns parsed JSON list or None."""
    global _groq_model_idx
    model = GROQ_MODELS[model_idx % len(GROQ_MODELS)]
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    system = "You are a Catholic theology expert. Always respond with valid JSON array only, no markdown, no explanation."
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt + "\n\nIMPORTANT: Respond with ONLY a valid JSON array, no markdown code blocks."}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_KEY}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode())
            text = res["choices"][0]["message"]["content"].strip()
            # Strip markdown if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
    except urllib.error.HTTPError as e:
        print(f"  Groq/{model} HTTP {e.code}")
        return None
    except json.JSONDecodeError as e:
        print(f"  Groq/{model} JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  Groq/{model} error: {e}")
        return None

def call_with_fallback(prompt, schema, full_fix=False, retry=0):
    """Try Gemini first; fall back to Groq models on 429 or failure."""
    # Try Gemini
    try:
        result = call_gemini(prompt, schema)
        if result:
            return result, "Gemini"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"  Gemini rate-limited → trying Groq...", flush=True)
        else:
            print(f"  Gemini HTTP {e.code} → trying Groq...", flush=True)
    except Exception:
        print(f"  Gemini failed → trying Groq...", flush=True)

    # Try Groq models in sequence
    for idx, model in enumerate(GROQ_MODELS):
        print(f"  Trying Groq/{model}...", flush=True)
        result = call_groq(prompt, model_idx=idx)
        if result:
            return result, f"Groq/{model}"
        time.sleep(3)

    # All failed
    if retry < 2:
        wait = 30 * (retry + 1)
        print(f"  All providers failed. Waiting {wait}s before retry {retry+1}...", flush=True)
        time.sleep(wait)
        return call_with_fallback(prompt, schema, full_fix, retry + 1)
    
    return None, "failed"

def save():
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

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

# ===== PHASE 1: Full reconstruction for contaminated/empty Q =====
phase1 = sorted([qid for qid in to_fix if qid in FORCE_REGEN_IDS])
print(f"\n{'='*60}")
print(f"PHASE 1: Full reconstruction — {len(phase1)} questions")
print(f"{'='*60}")

BATCH1 = 5
for i in range(0, len(phase1), BATCH1):
    batch_ids = phase1[i:i+BATCH1]
    batch_data = [{"id": qid, "question": all_q.get(qid, {}).get("question", ""), "answer": all_q.get(qid, {}).get("answer", "")} for qid in batch_ids]
    
    print(f"\n  Batch {i//BATCH1+1}/{(len(phase1)+BATCH1-1)//BATCH1}: Q{batch_ids[0]}-Q{batch_ids[-1]}", flush=True)
    
    prompt = f"""Anda ahli Teologi Katolik. Pertanyaan-pertanyaan ini dari KKGK (Kompendium Katekismus Gereja Katolik edisi Indonesia 2005) mengalami kerusakan saat ekstraksi PDF.

Rekonstruksi setiap item berdasarkan pengetahuan Anda:
1. question: teks pertanyaan yang benar & lengkap dalam Bahasa Indonesia
2. answer: jawaban resmi KKGK yang lengkap & bersih (TANPA teks Latin/Italia/Lampiran/doa liturgi) 
3. reference: nomor paragraf KGK yang tepat (format: "KGK xxx" atau "KGK xxx-yyy")
4. reflection: 2 kalimat refleksi pastoral yang indah & aplikatif

Untuk Q587-Q598: tentang 7 permohonan Doa Bapa Kami (Bagian Empat KKGK, KGK 2759-2865).
Untuk Q101: tentang misteri hidup Kristus sebagai wahyu Bapa (KGK 514-521).
Untuk Q189: tentang kaum awam dan imamat Kristus (KGK 897-913).

Input (saat ini mungkin rusak):
{json.dumps(batch_data, ensure_ascii=False)}

Kembalikan JSON array dengan field: id, question, answer, reference, reflection."""
    
    results, provider = call_with_fallback(prompt, FULL_SCHEMA, full_fix=True)
    if results:
        for r in results:
            processed[int(r["id"])] = r
        save()
        print(f"  ✓ {len(results)} Q fixed via {provider}", flush=True)
    else:
        print(f"  ✗ All providers failed for this batch, skipping.", flush=True)
    
    if i + BATCH1 < len(phase1):
        time.sleep(8)

# ===== PHASE 2: Reflection-only for remaining Q =====
phase2 = sorted([qid for qid in to_fix if qid not in FORCE_REGEN_IDS and qid not in processed])
print(f"\n{'='*60}")
print(f"PHASE 2: Add reflections — {len(phase2)} questions")
print(f"{'='*60}")

BATCH2 = 15
for i in range(0, len(phase2), BATCH2):
    batch_ids = phase2[i:i+BATCH2]
    batch_data = [{"id": qid, "question": all_q.get(qid, {}).get("question", ""), "answer": all_q.get(qid, {}).get("answer", "")[:400]} for qid in batch_ids]
    
    done = sum(1 for qid in range(1, 599) if qid in processed)
    print(f"\n  Batch {i//BATCH2+1}/{(len(phase2)+BATCH2-1)//BATCH2}: Q{batch_ids[0]}-Q{batch_ids[-1]} | Progress: {done}/598", flush=True)
    
    prompt = f"""Anda penulis refleksi spiritual Katolik yang berpengalaman.

Untuk setiap pertanyaan & jawaban dari Kompendium Katekismus Gereja Katolik berikut, tuliskan 2 kalimat "Refleksi Iman Batiniah" yang:
- Mendalam secara teologis dan pastoral
- Aplikatif untuk kehidupan Kristiani modern
- Indah dan menyentuh hati

Input:
{json.dumps(batch_data, ensure_ascii=False)}

Kembalikan JSON array dengan field: id (integer), reflection (string berisi tepat 2 kalimat)."""
    
    results, provider = call_with_fallback(prompt, REFLECT_SCHEMA)
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
        total_done = sum(1 for qid in range(1, 599) if qid in processed)
        print(f"  ✓ {len(results)} reflections via {provider} | Total: {total_done}/598", flush=True)
    else:
        print(f"  ✗ All failed, skipping batch.", flush=True)
    
    time.sleep(5)

# ===== BUILD FINAL DATABASE =====
print(f"\n{'='*60}")
print(f"Building final database...")
print(f"{'='*60}")

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
print(f"   Total Q     : {total}")
print(f"   Empty answer: {empty_ans}")
print(f"   Empty refl  : {empty_ref}")
print(f"   Output      : {OUTPUT_PATH}")
