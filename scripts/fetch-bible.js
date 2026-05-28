import fs from 'fs';
import path from 'path';
import { XMLParser } from 'fast-xml-parser';

const METADATA_PATH = './src/data/bible-metadata.json';
const OUTPUT_DIR = './public/data/chapters';
const BIBLE_VERSION = 'tb';

const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: ""
});

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchChapter(bookName, chapter) {
    const url = `https://alkitab.sabda.org/api/passage.php?passage=${encodeURIComponent(bookName)}+${chapter}&ver=${BIBLE_VERSION}`;
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const xml = await response.text();
        const jsonObj = parser.parse(xml);
        
        // Structure: bible -> book -> chapter -> verses -> verse[]
        const bibleData = jsonObj.bible;
        if (!bibleData || !bibleData.book || !bibleData.book.chapter || !bibleData.book.chapter.verses) {
            console.warn(`[WARN] No data for ${bookName} ${chapter}`);
            return null;
        }

        const rawVerses = bibleData.book.chapter.verses.verse;
        const versesArray = Array.isArray(rawVerses) ? rawVerses : [rawVerses];

        const formattedVerses = [];
        versesArray.forEach(v => {
            // Handle perikop/heading if present
            if (v.title) {
                formattedVerses.push({
                    type: 'heading',
                    text: v.title
                });
            }
            formattedVerses.push({
                verse: parseInt(v.number),
                text: v.text.trim()
            });
        });

        return formattedVerses;
    } catch (error) {
        console.error(`[ERROR] Failed to fetch ${bookName} ${chapter}:`, error.message);
        return null;
    }
}

async function main() {
    const metadata = JSON.parse(fs.readFileSync(METADATA_PATH, 'utf-8'));
    
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    console.log(`Starting fetch for ${metadata.length} books...`);

    for (const book of metadata) {
        const bookSlug = book.id;
        const bookDir = path.join(OUTPUT_DIR, bookSlug);
        
        if (!fs.existsSync(bookDir)) {
            fs.mkdirSync(bookDir, { recursive: true });
        }

        console.log(`Fetching ${book.name} (${book.chapters} chapters)...`);
        
        for (let ch = 1; ch <= book.chapters; ch++) {
            const filePath = path.join(bookDir, `${ch}.json`);
            
            // Skip if already exists to save time/bandwidth
            if (fs.existsSync(filePath)) {
                // console.log(`  Chapter ${ch} already exists, skipping.`);
                continue;
            }

            const data = await fetchChapter(book.name, ch);
            if (data) {
                fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
                // console.log(`  Saved Chapter ${ch}`);
            }
            
            // Small delay to be polite to the API
            await delay(100);
        }
    }

    console.log('Finished downloading all available chapters.');
}

main();
