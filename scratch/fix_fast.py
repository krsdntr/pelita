"""
Fast fix for the 166 missing reflections + contaminated Q587-Q598.
Runs in foreground with clear progress output.
Uses smaller batches for speed.
"""
import json
import urllib.request
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
MODEL_NAME = "gemini-flash-lite-latest"

CURRENT_DB_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"
PROGRESS_PATH = r"d:\app\alkitab\scratch\processed_compendium_progress.json"
OUTPUT_PATH = r"d:\app\alkitab\src\data\catechism-compendium.json"

# Groups of Q that need full reconstruction (contaminated/empty)
FORCE_REGEN_IDS = {
    101, 189, 234, 337, 462, 577,  # empty answers
    587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598,  # last section contaminated
    107, 111, 119, 343, 350, 356, 458,  # appendix contamination
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

# Remove contaminated ones from processed to force regen
removed = 0
for qid in FORCE_REGEN_IDS:
    if qid in processed:
        del processed[qid]
        removed += 1
print(f"Removed {removed} contaminated entries from progress for re-generation.")

# Identify all questions still needing work
to_fix = []
for qid, q in sorted(all_q_by_id.items()):
    needs_fix = False
    if not q.get("reflection", "").strip():
        needs_fix = True
    if qid in FORCE_REGEN_IDS:
        needs_fix = True
    if needs_fix and qid not in processed:
        to_fix.append(qid)

print(f"Total questions to process: {len(to_fix)}")

def call_gemini_reflections_only(batch):
    """Fast mode: only generate reflections for questions with good answers."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    items = json.dumps(batch, ensure_ascii=False, indent=2)
    prompt = f"""Anda adalah seorang ahli Teologi Katolik dan penulis refleksi spiritual.

Untuk setiap pertanyaan & jawaban dari Kompendium Katekismus Gereja Katolik (KKGK) berikut, tuliskan 2 kalimat "Refleksi Iman Batiniah" yang:
- Mendalam dan pastoral
- Aplikatif untuk kehidupan Kristiani modern
- Indah secara bahasa, penuh semangat iman

Input:
{items}

Kembalikan JSON array dengan field: id (integer), reflection (string, 2 kalimat).
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
                        "reflection": {"type": "string"}
                    },
                    "required": ["id", "reflection"]
                }
            }
        }
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        print(f"  Error: {e}")
        return None

def call_gemini_full_fix(batch):
    """Full fix mode: reconstruct Q, A, reference AND reflection."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    items = json.dumps(batch, ensure_ascii=False, indent=2)
    prompt = f"""Anda adalah ahli Teologi Katolik. Berikut pertanyaan dari KKGK yang RUSAK/TIDAK LENGKAP karena kesalahan ekstraksi PDF.

Tugas Anda: berdasarkan nomor ID dan pengetahuan Anda tentang Kompendium Katekismus Gereja Katolik edisi Bahasa Indonesia (2005), rekonstruksi:
1. Teks pertanyaan yang benar dan lengkap
2. Jawaban resmi yang benar, lengkap, dan bersih (TANPA teks Italia/Latin/Appendix)  
3. Nomor referensi paragraf KGK yang tepat
4. 2 kalimat refleksi pastoral yang indah

Input (Q/A saat ini mungkin rusak):
{items}

PENTING:
- Jawaban harus sesuai teks resmi KKGK versi Indonesia, bukan hasil rekayasa bebas
- Jangan sertakan teks Lampiran, doa liturgi, atau teks bahasa Italia/Latin dalam jawaban
- Untuk Q587-Q598 (Doa Bapa Kami), gunakan pengetahuan Anda tentang bagian keempat KKGK

Kembalikan JSON array dengan field: id, question, answer, reference, reflection.
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
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e:
        print(f"  Error: {e}")
        return None

# ===== PHASE 1: Fix contaminated/empty questions (full reconstruction) =====
force_regen_remaining = [qid for qid in sorted(FORCE_REGEN_IDS) if qid not in processed]
print(f"\n=== PHASE 1: Full reconstruction for {len(force_regen_remaining)} contaminated/empty Q ===")

BATCH_SIZE_FULL = 8
for i in range(0, len(force_regen_remaining), BATCH_SIZE_FULL):
    batch_ids = force_regen_remaining[i:i+BATCH_SIZE_FULL]
    batch_data = []
    for qid in batch_ids:
        q = all_q_by_id.get(qid, {})
        batch_data.append({
            "id": qid,
            "question": q.get("question", ""),
            "answer": q.get("answer", ""),
        })
    
    print(f"\n  Batch {i//BATCH_SIZE_FULL + 1}: Q{batch_ids[0]}-Q{batch_ids[-1]}...")
    results = call_gemini_full_fix(batch_data)
    if results:
        for r in results:
            qid = int(r["id"])
            processed[qid] = r
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Done ({len(results)} questions fixed)")
        time.sleep(3)
    else:
        print(f"  ✗ Failed, skipping batch")
        time.sleep(5)

# ===== PHASE 2: Add reflections to remaining 166 questions (reflection only) =====
reflection_only_ids = [qid for qid in to_fix if qid not in FORCE_REGEN_IDS and qid not in processed]
print(f"\n=== PHASE 2: Add reflections to {len(reflection_only_ids)} remaining questions ===")

BATCH_SIZE_REFLECT = 20
for i in range(0, len(reflection_only_ids), BATCH_SIZE_REFLECT):
    batch_ids = reflection_only_ids[i:i+BATCH_SIZE_REFLECT]
    batch_data = []
    for qid in batch_ids:
        q = all_q_by_id.get(qid, {})
        batch_data.append({
            "id": qid,
            "question": q.get("question", ""),
            "answer": q.get("answer", "")[:500]  # trim long answers for token efficiency
        })
    
    print(f"\n  Batch {i//BATCH_SIZE_REFLECT + 1}: Q{batch_ids[0]}-Q{batch_ids[-1]} ({len(batch_data)} Q)...")
    results = call_gemini_reflections_only(batch_data)
    if results:
        for r in results:
            qid = int(r["id"])
            existing = all_q_by_id.get(qid, {})
            processed[qid] = {
                "id": qid,
                "question": existing.get("question", ""),
                "answer": existing.get("answer", ""),
                "reference": existing.get("reference", f"KGK {qid}"),
                "reflection": r.get("reflection", "")
            }
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Done ({len(results)} reflections added)")
        time.sleep(2)
    else:
        print(f"  ✗ Failed, skipping batch")
        time.sleep(5)

# ===== FINAL: Reconstruct database =====
print(f"\n=== FINAL: Reconstructing database ===")
final_db = []
for pillar in current_db:
    p_questions = []
    for q in pillar["questions"]:
        qid = q["id"]
        if qid in processed:
            fixed = processed[qid]
            p_questions.append({
                "id": qid,
                "question": fixed.get("question") or q["question"],
                "answer": fixed.get("answer") or q["answer"],
                "reference": fixed.get("reference") or q.get("reference", f"KGK {qid}"),
                "reflection": fixed.get("reflection", "")
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

empty_ans = sum(1 for p in final_db for q in p["questions"] if not q["answer"].strip())
empty_ref = sum(1 for p in final_db for q in p["questions"] if not q["reflection"].strip())
total_q = sum(len(p["questions"]) for p in final_db)
print(f"\nStats: {total_q} total Q | {empty_ans} empty answers | {empty_ref} empty reflections")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"\n✅ SUCCESS! Database updated: {OUTPUT_PATH}")
