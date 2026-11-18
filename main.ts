// news-image-20261117 entry (Node 22, standard library only): the picture of
// Tuesday 17 November 2026 is entry.png beside this file -- a newspaper
// front page drawn in code (draw_news.py) with four panels: the Crimea
// bridge partly collapsing after a Ukrainian strike, the U.S. strike on
// Qeshm Island and Iran's drone replies in the Gulf, the An-12 crash in
// Siberia that killed all 19 on board, and the U.S. losing its measles
// elimination status -- and this program copies it to /output/entry.png.
// The gate takes a whole PNG or JPEG of at most 1 MiB and 1024 by 1024
// pixels, and the judge sees exactly the bytes copied, so the file is
// stored already within those limits (1024 by 1024, PNG under 1 MiB).
// The copy is byte for byte: what the judge sees is exactly the file
// in this repository. The entry image is drawn once, at build time, by
// draw_news.py; nothing is fetched at run time and the program needs no
// network, so two runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
