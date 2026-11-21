import { readFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { buildCustom } from "./custom.mjs";
import { ramps, trees } from "./spells.mjs";

const [root, output] = process.argv.slice(2);
if (!root || !output) throw new Error("Usage: node render.mjs PIXELFX_DIR OUTPUT_DIR");
const fromLibrary = (path) => import(pathToFileURL(resolve(root, path)).href);
const { loadEffect, renderFrames, canvas, upscale, save, writeVideo } = await fromLibrary("tools/lib/fxlib.mjs");
const { encodePNG } = await fromLibrary("tools/lib/png.mjs");
const custom = buildCustom(await fromLibrary("src/core/index.js"));
const allowed = JSON.parse(readFileSync(new URL("../../palettes/project.json", import.meta.url)));
const fps = 20;
const columns = 8;
const background = [33, 36, 53, 255];
const effects = [];
const cards = [];
const json = (value) => JSON.stringify(value, null, 2) + "\n";

function luminance(r, g, b) {
  return (54 * r + 183 * g + 19 * b) / 256;
}

function clean(rendered, palette) {
  const colors = palette.map((entry) => entry.slice(1).match(/../g).map((v) => parseInt(v, 16)));
  const levels = colors.map((c) => luminance(...c));
  const { w, h } = rendered;
  let x0 = w, y0 = h, x1 = 0, y1 = 0;
  const frames = [];
  for (const frame of rendered.frames) {
    const data = frame.clear;
    for (let offset = 0; offset < data.length; offset += 4) {
      const alpha = data[offset + 3];
      if (alpha < 25) {
        data.fill(0, offset, offset + 4);
        continue;
      }
      const luma = luminance(data[offset], data[offset + 1], data[offset + 2]);
      let closest = 0;
      for (let c = 1; c < levels.length; c++) {
        if (Math.abs(levels[c] - luma) < Math.abs(levels[closest] - luma)) closest = c;
      }
      data.set(colors[closest], offset);
      data[offset + 3] = Math.min(255, Math.round(alpha / 32) * 32);
      const x = (offset / 4) % w, y = Math.floor(offset / 4 / w);
      x0 = Math.min(x, x0);
      x1 = Math.max(x + 1, x1);
      y0 = Math.min(y, y0);
      y1 = Math.max(y + 1, y1);
    }
    frames.push(data);
  }
  if (x0 === w) throw new Error("Empty animation");
  return { frames, bounds: [x0, y0, x1, y1] };
}

function crop(frames, sourceWidth, sourceHeight, bounds, origin) {
  const left = Math.min(origin[0], bounds[0]) - 3;
  const top = Math.min(origin[1], bounds[1]) - 3;
  const w = Math.ceil((Math.max(origin[0] + 1, bounds[2]) + 3 - left) / 8) * 8;
  const h = Math.ceil((Math.max(origin[1] + 1, bounds[3]) + 3 - top) / 8) * 8;
  const cropped = frames.map((data) => {
    const out = new Uint8ClampedArray(w * h * 4);
    const fromX = Math.max(0, left), toX = Math.min(sourceWidth, left + w);
    for (let y = Math.max(0, top); y < Math.min(sourceHeight, top + h); y++) {
      out.set(data.subarray((y * sourceWidth + fromX) * 4, (y * sourceWidth + toX) * 4),
        ((y - top) * w + fromX - left) * 4);
    }
    return out;
  });
  return { frames: cropped, w, h, pivot: [origin[0] - left, origin[1] - top] };
}

function exportSheet(file, frames, w, h) {
  const rows = Math.ceil(frames.length / columns);
  const width = w * columns, height = h * rows;
  const rgba = new Uint8ClampedArray(width * height * 4);
  for (const [i, frame] of frames.entries()) {
    const x = (i % columns) * w, y = Math.floor(i / columns) * h;
    for (let row = 0; row < h; row++) {
      rgba.set(frame.subarray(row * w * 4, (row + 1) * w * 4), ((y + row) * width + x) * 4);
    }
  }
  save(file, encodePNG(width, height, rgba));
  return rows;
}

function present(data, w, h) {
  const tile = canvas(w, h, background);
  tile.paste(data, w, h, 0, 0);
  return { color: tile.data };
}

function visualWeight(data) {
  let weight = 0;
  for (let i = 0; i < data.length; i += 4) {
    weight += (data[i + 3] / 255) ** 2 * (luminance(data[i], data[i + 1], data[i + 2]) / 255);
  }
  return weight;
}

function compact(rendered) {
  const w = Math.ceil(rendered.w / 2), h = Math.ceil(rendered.h / 2);
  const frames = rendered.frames.map(({ clear }) => {
    const data = new Uint8ClampedArray(w * h * 4);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        let best = -1, source = 0, alphaSum = 0;
        for (let dy = 0; dy < 2 && y * 2 + dy < rendered.h; dy++) {
          for (let dx = 0; dx < 2 && x * 2 + dx < rendered.w; dx++) {
            const i = ((y * 2 + dy) * rendered.w + x * 2 + dx) * 4;
            const a = clear[i + 3];
            alphaSum += a;
            const weight = a * (0.5 + luminance(clear[i], clear[i + 1], clear[i + 2]) / 255);
            if (weight > best) [best, source] = [weight, i];
          }
        }
        const target = (y * w + x) * 4;
        data.set(clear.subarray(source, source + 3), target);
        data[target + 3] = Math.max(clear[source + 3] * 0.7, alphaSum / 4);
      }
    }
    return { clear: data };
  });
  return { w, h, frames };
}

for (const [tree, spells] of Object.entries(trees)) {
  const palette = ramps[tree];
  if (palette.some((entry) => !allowed.includes(entry))) throw new Error("Unapproved " + tree + " color");
  for (const [name, id, use, options] of spells) {
    const slug = name.toLowerCase().replaceAll(" ", "-");
    const prefix = tree + "/" + slug;
    const fx = id.startsWith("custom/") ? custom[basename(id)] : await loadEffect(id);
    const margin = 12;
    let rendered = renderFrames(fx, {
      fps, margin, bg: "none", actor: false,
      options: { palette, ...options },
    });
    let origin = fx.meta.origin.map((v) => v + margin);
    if (!id.startsWith("custom/") || id === "custom/hydra") {
      rendered = compact(rendered);
      origin = origin.map((v) => Math.round(v / 2));
    }
    const { frames: cleaned, bounds } = clean(rendered, palette);
    const { frames, w, h, pivot } = crop(cleaned, rendered.w, rendered.h, bounds, origin);
    if (!fx.meta.loop) frames[frames.length - 1].fill(0);
    const rows = exportSheet(join(output, "spritesheets", prefix + ".png"), frames, w, h);
    const gif = join(output, "gifs", prefix + ".gif");
    const preview = frames.map((frame) => present(frame, w, h));
    if (!fx.meta.loop) preview.push(...Array(4).fill(preview.at(-1)));
    if (!writeVideo(gif, { w, h, frames: preview, fps }, 2)) throw new Error("FFmpeg is required");
    const peak = frames.reduce((best, frame, i) => {
      const score = visualWeight(frame);
      return score > best.score ? { score, i } : best;
    }, { score: -1, i: 0 }).i;
    cards.push({ name, tree, frame: frames[peak], w, h });
    effects.push({
      name, tree, source: id, recommendedUse: use,
      sheet: "spritesheets/" + prefix + ".png", gif: "gifs/" + prefix + ".gif",
      cell: [w, h], columns, rows, frameCount: frames.length, fps, loop: Boolean(fx.meta.loop),
      pivotTopLeftPx: pivot, pivotUnity: [pivot[0] / w, 1 - pivot[1] / h],
      contactFrameIndex: peak,
    });
    console.log(`${name}: ${w}x${h}, ${frames.length} frames`);
  }
}

const panelWidth = 308, panelHeight = 202, padding = 18;
const contact = canvas(5 * panelWidth + 2 * padding, 6 * panelHeight + 110, [18, 20, 33, 255]);
contact.text("SPELLS TO GO", padding, 16, 5, [240, 252, 255]);
contact.text("30 PIXEL ART SPELL EFFECTS   /   FIRE  +  COLD  +  LIGHTNING", padding, 52, 2, [173, 233, 255]);
for (const [i, card] of cards.entries()) {
  const x = padding + (i % 5) * panelWidth, y = 82 + Math.floor(i / 5) * panelHeight;
  const accent = { fire: [234, 184, 83], cold: [173, 233, 255], lightning: [120, 203, 244] }[card.tree];
  contact.rect(x, y, panelWidth - 8, panelHeight - 8, background);
  contact.rect(x, y, panelWidth - 8, 2, [...accent, 255]);
  contact.text(card.tree.toUpperCase(), x + 9, y + 12, 1, accent);
  contact.text(card.name.toUpperCase(), x + 9, y + 23, 2, [240, 252, 255]);
  const scale = card.w <= 142 && card.h <= 74 ? 2 : 1;
  const w = card.w * scale, h = card.h * scale;
  contact.paste(upscale(card.frame, card.w, card.h, scale), w, h,
    x + Math.floor((panelWidth - 8 - w) / 2), y + 40 + Math.floor((149 - h) / 2));
}
save(join(output, "contact-sheet.png"), contact.png());
save(join(output, "unity-slicing.json"), json({ pixelsPerUnit: 32, frameOrder: "row-major, top-left first", palettes: ramps, effects }));
