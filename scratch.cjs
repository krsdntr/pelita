const fs = require('fs');
const data = JSON.parse(fs.readFileSync('./src/data/books/maz.json', 'utf8'));

console.log(`Mazmur has ${data.length} chapters.`);
let sameFound = [];
for(let i=0; i<data.length; i++) {
  if (i > 0 && JSON.stringify(data[i].verses) === JSON.stringify(data[i-1].verses)) {
     sameFound.push(data[i].chapter);
  }
}
console.log(`Chapters with identical verses to previous: ${sameFound.join(', ')}`);
