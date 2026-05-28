import fs from 'node:fs';
import path from 'node:path';

function moveFiles() {
  console.log('Rearranging Astro 6 output for Cloudflare Pages (V1 structure)...');
  
  // 1. Rename dist/client to dist_temp
  fs.renameSync('dist/client', 'dist_temp');

  // 2. Rename dist/server to dist/_worker.js
  fs.renameSync('dist/server', 'dist/_worker.js');
  
  // 3. Rename entry.mjs to index.js so Cloudflare recognizes it as the worker entry point
  fs.renameSync('dist/_worker.js/entry.mjs', 'dist/_worker.js/index.js');

  // 4. Move all files from dist_temp to dist
  function copyDir(src, dest) {
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);
      if (entry.isDirectory()) {
        fs.mkdirSync(destPath, { recursive: true });
        copyDir(srcPath, destPath);
      } else {
        fs.renameSync(srcPath, destPath);
      }
    }
  }

  copyDir('dist_temp', 'dist');

  // 5. Cleanup
  fs.rmSync('dist_temp', { recursive: true, force: true });
  
  console.log('Successfully rearranged assets for Cloudflare Pages!');
}

try {
  moveFiles();
} catch (err) {
  console.error('Error during postbuild:', err);
  process.exit(1);
}
