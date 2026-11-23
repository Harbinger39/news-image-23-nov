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

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
