import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// CONFIGURATIONS
const API_KEY = process.env.GEMINI_API_KEY || "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM";
const MODEL_NAME = 'gemini-flash-lite-latest'; // Using the active, high-quota Gemini 3.5 Flash
const DELAY_BETWEEN_BOOKS_MS = 4000; // 4 seconds delay to respect rate limit (15 requests per minute free tier)
const MAX_RETRIES = 3;

// Paths
const metadataPath = path.join(__dirname, '../src/data/bible-metadata.json');
const summariesPath = path.join(__dirname, '../src/data/catholic-summaries.json');

// JSON Schema for Gemini Structured Output
const responseSchema = {
  type: "object",
  properties: {
    isPremium: {
      type: "boolean",
      description: "Harus selalu di-set ke true. Menandakan bahwa rangkuman ini dibuat menggunakan format premium tebal."
    },
    quote: { 
      type: "string", 
      description: "Satu kutipan ayat terpenting/terkenal dari kitab ini dalam Bahasa Indonesia Terjemahan Baru (TB)." 
    },
    tagline: { 
      type: "string", 
      description: "Satu kalimat pendek menggugah yang menjadi esensi rohani kitab ini dari perspektif Katolik." 
    },
    overview: { 
      type: "string", 
      description: "Gambaran umum teologis dan editorial yang SANGAT MENDALAM (minimal 3 paragraf detail, minimal 200 kata) mengenai peran kitab ini dalam sejarah keselamatan, alur cerita, dan tema rohani utama." 
    },
    author: { 
      type: "string", 
      description: "Penulis tradisional maupun pandangan akademis modern secara rinci (misal: 'Tradisi Paulin', 'Musa / Redaksi Imamat', dll.)." 
    },
    date: { 
      type: "string", 
      description: "Rentang waktu penulisan historis secara akademis beserta perkiraan tahunnya (misal: 'Abad ke-6 SM (sekitar 587-538 SM)', 'Sekitar 80-85 M')." 
    },
    context: { 
      type: "string", 
      description: "Latar belakang sejarah, sosial, dan teologis yang SANGAT LENGKAP (minimal 2 paragraf detail, minimal 150 kata) mengapa kitab ini ditulis, situasi politik kekaisaran saat itu, dan pergumulan iman jemaat sasaran." 
    },
    theology: { 
      type: "string", 
      description: "Poin-poin teologi Katolik penting yang diajarkan kitab ini. Berikan 3-4 poin teologis yang kaya. Wajib ditulis dalam format list markdown 1. **Judul Poin**: Penjelasan mendalam (minimal 3-4 kalimat panjang per poin) yang dikaitkan langsung dengan Katekismus Gereja Katolik (KGK), sakramen, liturgi, atau tipologi Kristologis Katolik." 
    },
    structure: {
      type: "array",
      description: "Pembagian struktur kitab menjadi 3 sampai 4 bagian narasi/teologis yang logis.",
      items: {
        type: "object",
        properties: {
          chapters: { type: "string", description: "Rentang bab, misal: '1 - 11', '12 - 25', atau '1' jika hanya 1 bab." },
          title: { type: "string", description: "Judul teologis atau naratif bagian ini secara indah." },
          summary: { type: "string", description: "Rangkuman SANGAT DESKRIPTIF (minimal 3-4 kalimat panjang) yang menceritakan peristiwa utama, makna rohani, dan pesan teologis pada bagian bab tersebut." }
        },
        required: ["chapters", "title", "summary"]
      }
    },
    goldenVerses: {
      type: "array",
      description: "Daftar 2 sampai 3 ayat emas terbaik dari kitab ini beserta refleksinya.",
      items: {
        type: "object",
        properties: {
          verse: { type: "string", description: "Referensi ayat lengkap, misal: 'Imamat 19:2' atau 'Roma 8:28'." },
          text: { type: "string", description: "Teks lengkap ayat asli dalam Bahasa Indonesia Terjemahan Baru (TB)." },
          reflection: { type: "string", description: "Refleksi rohani batiniah, teologis, dan pastoral yang SANGAT MENDALAM (minimal 3-4 kalimat meditasi panjang) dari sudut pandang iman dan spiritualitas Katolik." }
        },
        required: ["verse", "text", "reflection"]
      }
    }
  },
  required: [
    "isPremium",
    "quote", 
    "tagline", 
    "overview", 
    "author", 
    "date", 
    "context", 
    "theology", 
    "structure", 
    "goldenVerses"
  ]
};

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to call Gemini API with retry logic and exponential backoff
async function fetchSummaryFromLLM(book, retryCount = 0) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${API_KEY}`;
  
  const prompt = `Anda adalah seorang ahli Teologi Katolik terkemuka, sejarawan Alkitab, dan editor sastra Kristen tingkat tinggi yang mengedepankan keindahan teologis (editorial).
Tugas Anda adalah menghasilkan rangkuman teologis dan pastoral yang SANGAT MENDALAM, INDAH, dan KAYA AKAN KONTEKS PENUH untuk kitab di bawah ini:

Kitab: "${book.name}"
Kategori/Bagian: "${book.category}"
Sub-Kategori/Kelompok: "${book.subCategory}"
Jumlah Bab: ${book.chapters}

Instruksi Konten Rangkuman (WAJIB MEMENUHI BATASAN PANJANG):
1. **isPremium**: Selalu berikan nilai boolean true.
2. **quote**: Kutipan ayat paling terkenal atau representatif dari kitab ini dalam bahasa Indonesia Terjemahan Baru (TB).
3. **tagline**: Satu kalimat pendek menggugah yang menjadi esensi rohani kitab ini dari kacamata Katolik.
4. **overview**: Tulis ulasan yang SANGAT MENDALAM (minimal 3 paragraf tebal, minimal 200 kata). Paragraf 1 membahas peranan kitab ini dalam sejarah keselamatan. Paragraf 2 membahas ringkasan alur cerita/pesan sastra. Paragraf 3 membahas signifikansi teologisnya dalam kehidupan jemaat.
5. **author**: Penulisan tradisional maupun pandangan ilmiah modern/historis-kritis secara rinci (misal: "Tradisi Paulin", "Musa/Redaksi Priestly", dll.).
6. **date**: Rentang waktu penulisan historis secara akademis beserta perkiraan tahunnya (misal: "Abad ke-6 SM (sekitar 587-538 SM)", "Sekitar 80-85 M").
7. **context**: Latar belakang sejarah, sosial, dan teologis yang SANGAT LENGKAP (minimal 2 paragraf tebal, minimal 150 kata) mengapa kitab ini ditulis, situasi politik kekaisaran saat itu, dan pergumulan iman jemaat sasaran.
8. **theology**: Poin-poin teologi Katolik yang sangat kuat di dalam kitab ini, hubungkan dengan Katekismus Gereja Katolik (KGK), tradisi sakramen, liturgi, atau tipologi Kristologis Katolik. Wajib ditulis dalam format list markdown 1. **Judul Poin**: Penjelasan teologis yang sangat tebal (minimal 3-4 kalimat panjang per poin). Berikan 3-4 poin teologis.
9. **structure**: Bagi kitab ini menjadi 3-4 bagian narasi yang logis dan memiliki alur pesan rohani. Untuk setiap bagian:
   - "chapters": Rentang bab (misal: "1 - 11", atau "1" jika hanya 1 bab).
   - "title": Judul teologis bagian tersebut yang indah.
   - "summary": Rangkuman SANGAT DESKRIPTIF (minimal 3-4 kalimat panjang) yang menceritakan peristiwa utama, makna rohani, dan pesan teologis pada bagian bab tersebut.
10. **goldenVerses**: Berikan 2 sampai 3 ayat emas Katolik terbaik dari kitab ini. Setiap ayat emas harus menyertakan:
   - "verse": Referensi ayat lengkap (misal: "Matius 16:18" atau "Roma 8:28").
   - "text": Teks ayat asli dalam Bahasa Indonesia Terjemahan Baru (TB).
   - "reflection": Refleksi teologis, praktis, dan pastoral yang SANGAT MENDALAM (minimal 3-4 kalimat meditasi panjang) dari perspektif spiritualitas Katolik.

Pastikan semua teks ditulis dalam Bahasa Indonesia yang formal, puitis, editorial (berbobot), dan sarat dengan kekayaan rohani Katolik. Hindari penjelasan yang singkat, umum, atau repetitif. Kita ingin memberikan konteks penuh, tebal, dan bernilai edukasi iman tinggi.`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: prompt }
            ]
          }
        ],
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: responseSchema
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    const textResponse = data.candidates[0].content.parts[0].text;
    
    // Parse the JSON structure
    const parsedData = JSON.parse(textResponse);
    return parsedData;

  } catch (error) {
    console.error(`\x1b[31m[ERROR] Gagal memproses Kitab ${book.name}: ${error.message}\x1b[0m`);
    
    if (retryCount < MAX_RETRIES) {
      const backoffTime = Math.pow(2, retryCount) * 5000; // 5s, 10s, 20s
      console.log(`\x1b[33m[RETRY] Mencoba kembali dalam ${backoffTime / 1000} detik... (Percobaan ${retryCount + 1}/${MAX_RETRIES})\x1b[0m`);
      await delay(backoffTime);
      return fetchSummaryFromLLM(book, retryCount + 1);
    }
    
    return null;
  }
}

async function main() {
  if (!API_KEY || API_KEY === "YOUR_GEMINI_API_KEY") {
    console.error("\x1b[31m[CRITICAL] API Key Gemini tidak ditemukan! Harap masukkan API key di skrip atau set environment variable GEMINI_API_KEY.\x1b[0m");
    process.exit(1);
  }

  console.log("\x1b[36m====================================================\x1b[0m");
  console.log("\x1b[36m   UPGRADE: GENERATOR RANGKUMAN ALKITAB PREMIUM LLM  \x1b[0m");
  console.log("\x1b[36m====================================================\x1b[0m");

  // Read files
  const books = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
  let currentSummaries = {};
  
  if (fs.existsSync(summariesPath)) {
    try {
      currentSummaries = JSON.parse(fs.readFileSync(summariesPath, 'utf8'));
      console.log(`\x1b[32m[INFO] Berhasil memuat ${Object.keys(currentSummaries).length} rangkuman yang sudah ada.\x1b[0m`);
    } catch (e) {
      console.warn("\x1b[33m[WARN] File catholic-summaries.json kosong atau rusak. Membuat data baru...\x1b[0m");
    }
  }

  let successCount = 0;
  let skippedCount = 0;

  for (let i = 0; i < books.length; i++) {
    const book = books[i];
    const progress = `[${i + 1}/${books.length}]`;
    
    const existingSummary = currentSummaries[book.id];
    
    // Check if the current summary is already premium
    const isAlreadyPremium = existingSummary && existingSummary.isPremium === true;

    if (isAlreadyPremium) {
      console.log(`\x1b[33m${progress} Kitab ${book.name} (${book.id}) sudah PREMIUM tebal. Melewati...\x1b[0m`);
      skippedCount++;
      continue;
    }

    console.log(`\x1b[36m${progress} Menghasilkan rangkuman Katolik PREMIUM untuk Kitab ${book.name} (${book.id})...\x1b[0m`);

    const summaryData = await fetchSummaryFromLLM(book);
    
    if (summaryData) {
      // Merge with basic metadata to ensure book information is persistent and complete
      currentSummaries[book.id] = {
        id: book.id,
        name: book.name,
        category: book.category,
        subCategory: book.subCategory,
        chapters: book.chapters,
        ...summaryData
      };

      // Write immediately to file (Checkpointing)
      fs.writeFileSync(summariesPath, JSON.stringify(currentSummaries, null, 2));
      console.log(`\x1b[32m  -> [BERHASIL] Rangkuman PREMIUM Kitab ${book.name} disimpan ke file!\x1b[0m`);
      successCount++;
      
      // Delay to respect rate limit
      console.log(`  -> Menunggu ${DELAY_BETWEEN_BOOKS_MS / 1000} detik sebelum kitab berikutnya...`);
      await delay(DELAY_BETWEEN_BOOKS_MS);
    } else {
      console.error(`\x1b[31m  -> [GAGAL] Melewati Kitab ${book.name} setelah beberapa kali percobaan gagal.\x1b[0m`);
    }
  }

  console.log("\x1b[36m====================================================\x1b[0m");
  console.log("\x1b[32m         PROSES UPGRADE PREMIUM SELESAI             \x1b[0m");
  console.log(`  - Berhasil diperbarui: ${successCount} Kitab`);
  console.log(`  - Dilewati (Sudah Premium): ${skippedCount} Kitab`);
  console.log(`  - Total Kitab Sekarang: ${Object.keys(currentSummaries).length}/73 Kitab`);
  console.log("\x1b[36m====================================================\x1b[0m");
}

main();
