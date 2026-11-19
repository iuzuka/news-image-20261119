// main.ts
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { copyFile } from 'node:fs/promises';

async function main() {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  const sourcePath = join(process.cwd(), 'entry.png');
  const targetPath = join(outputDir, 'entry.png');

  await mkdir(outputDir, { recursive: true });

  await copyFile(sourcePath, targetPath);

  console.log('File copied successfully');
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});