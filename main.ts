// main.ts
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

async function main() {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);
  const sourcePath = join(__dirname, 'entry.png');
  const targetPath = join(outputDir, 'entry.png');

  await mkdir(outputDir, { recursive: true });

  await copyFile(sourcePath, targetPath);

  console.log('File copied successfully');
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});