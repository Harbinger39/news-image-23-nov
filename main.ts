// news-image-23-nov: a one-image summary of Monday 23 November 2026's
// world news, drawn as a newspaper front page ("THE WORLD IN ONE DAY").
// Leads: Nvidia reinstates Jensen Huang; sea drones sink a Russian
// corvette off Libya; Poland summons Russia's envoy over missile debris.
//
// The program is deliberately boring: the picture is the entry, and this
// file just places the bundled entry.png where the grader expects it.
// It runs on Node 22 with the standard library only, reads nothing from
// the network, and writes the exact same bytes on every run.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const src = join(here, 'entry.png');
// Guard: the entry must be a 1024x1024 PNG before it is copied out,
// so a bad regenerate fails loudly instead of shipping a broken image.
const buf = readFileSync(src);
if (buf.length < 33 || buf.toString('latin1', 1, 4) !== 'PNG') {
  throw new Error('entry.png is not a PNG file');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}
if (buf.length > 1048576) {
  throw new Error(`entry.png must be at most 1 MiB, got ${buf.length} bytes`);
}
copyFileSync(src, join(outDir, 'entry.png'));
