/**
 * Split search-index.json into per-book files so only the needed
 * book's index is downloaded when relevant. Also create a minimal
 * "global" index that only stores book+chapter+verse pointers with
 * first 60 chars of text for quick keyword matching.
 */

const fs = require('fs');
const path = require('path');

console.log('Reading source index...');
const raw = JSON.parse(fs.readFileSync('./public/data/search-index.json', 'utf8'));
console.log(`Total verses: ${raw.length}`);

// --- Strategy: Build a MINIMAL global index ---
// Only keep: book_id, chapter, verse_num, and FIRST 60 CHARS of text
// This is enough for keyword search since COCO only needs short context snippets
// Full text can be fetched on-demand from the per-book JSON files

const minimalIndex = raw.map(e => ({
  b: e.b,
  n: e.n,
  c: e.c,
  v: parseInt(e.v) || e.v,
  t: e.t.substring(0, 120)   // keep first 120 chars only (enough for keyword match + snippet)
}));

const minPath = './public/data/search-index-min.json';
fs.writeFileSync(minPath, JSON.stringify(minimalIndex));
const minSize = fs.statSync(minPath).size;
const origSize = fs.statSync('./public/data/search-index.json').size;

console.log(`\nOriginal: ${(origSize/1024/1024).toFixed(2)} MB`);
console.log(`Minimal:  ${(minSize/1024/1024).toFixed(2)} MB (${(100-minSize/origSize*100).toFixed(1)}% smaller)`);
