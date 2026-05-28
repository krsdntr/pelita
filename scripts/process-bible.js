import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read metadata
const metaPath = path.join(__dirname, '../src/data/bible-metadata.json');
const books = JSON.parse(fs.readFileSync(metaPath, 'utf8'));

const outDir = path.join(__dirname, '../src/data/books');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Function to generate dummy verses based on standard verse length map
function generateVerses(bookId, chapter) {
  // We use fixed counts to make it somewhat realistic
  const verseCountMap = {
    kej: 30, maz: 10, mat: 25, yoh: 20
  };
  const count = verseCountMap[bookId] || (15 + (chapter % 10)); // randomish

  let verses = [];
  for (let i = 1; i <= count; i++) {
    verses.push({
      verse: i,
      text: bookId === 'kej' && i === 1 
            ? "Pada mulanya Allah menciptakan langit dan bumi." 
            : bookId === 'yoh' && i === 1 
            ? "Pada mulanya adalah Firman; Firman itu bersama-sama dengan Allah dan Firman itu adalah Allah."
            : `Ini adalah teks simulasi untuk ayat ke-${i} dari pasal ${chapter} kitab ini. Untuk mendapatkan teks Terjemahan Baru secara resmi, harap integrasikan dengan API sah dan ubah sumber skrip ini.`
    });
  }

  // Add dummy headings
  if (verses.length > 5 && chapter === 1) {
      verses.splice(0, 0, { type: 'heading', text: "Permulaan" });
  }

  return verses;
}

books.forEach(book => {
  const bookData = [];
  
  for (let c = 1; c <= book.chapters; c++) {
    bookData.push({
      chapter: c,
      verses: generateVerses(book.id, c)
    });
  }

  const filePath = path.join(outDir, `${book.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(bookData, null, 2));
  console.log(`Generated mock data for ${book.name} (${book.chapters} chapters)`);
});

console.log("Mock data generation complete.");
