import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [root, pack, meadow, output] = process.argv.slice(2);
const { canvas, upscale, save } = await import(pathToFileURL(resolve(root, "tools/lib/fxlib.mjs")).href);
const { effects } = JSON.parse(readFileSync(join(pack, "unity-slicing.json")));
const decode = (path, filters = []) => execFileSync("ffmpeg", [
  "-v", "error", "-i", path, ...filters, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-",
]);

const field = decode(meadow, ["-vf", "scale=160:352:flags=neighbor,crop=160:112:0:88"]);
const placements = {
  fire: [[68,45],[24,65],[34,51],[39,74],[68,45],[91,74],[32,52],[104,66],[24,65],[58,75]],
  cold: [[35,49],[24,65],[64,68],[104,66],[24,65],[68,45],[103,65],[24,65],[73,73],[24,65]],
  lightning: [[34,54],[64,69],[104,54],[64,69],[30,64],[24,66],[64,65],[104,66],[24,65],[24,65]],
};
const board = canvas(168 * 5 + 8, 140 * 6 + 48, [18, 20, 33, 255]);
board.text("SPELLS TO GO / MEADOW COMPOSITES", 8, 8, 3);
board.text("NATIVE 1X   SPELLS SAMPLED AT PEAK   GAMEPLAY FIELD CROP", 8, 29, 1);
for (const [i, spell] of effects.entries()) {
  const [w, h] = spell.cell;
  const frame = spell.contactFrameIndex;
  const frameX = frame % spell.columns * w, frameY = Math.floor(frame / spell.columns) * h;
  const sprite = decode(join(pack, spell.sheet), ["-vf", `crop=${w}:${h}:${frameX}:${frameY}`]);
  const tile = canvas(160, 112);
  tile.paste(field, 160, 112, 0, 0);
  const [x, y] = placements[spell.tree][i % 10];
  tile.paste(sprite, w, h, x - spell.pivotTopLeftPx[0], y - spell.pivotTopLeftPx[1]);
  const left = 8 + i % 5 * 168, top = 47 + Math.floor(i / 5) * 140;
  board.text(spell.name.toUpperCase(), left, top, 2);
  board.paste(tile.data, 160, 112, left, top + 17);
}
const doubled = canvas(board.w * 2, board.h * 2);
doubled.data.set(upscale(board.data, board.w, board.h, 2));
save(output, doubled.png());
