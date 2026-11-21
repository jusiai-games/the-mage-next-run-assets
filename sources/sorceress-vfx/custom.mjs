const turn = 2 * Math.PI;
const fire = {
  palette: ["#4F3333", "#6A4757", "#8B6755", "#D88475", "#EAB853", "#F8CFAB", "#F0FCFF"],
  seed: 36,
};
const blue = {
  palette: ["#28283F", "#393B5B", "#505276", "#367CB0", "#589DC8", "#78CBF4", "#ADE9FF", "#F0FCFF"],
  seed: 36,
};

function flame(p, c, x, y, width, height, lean) {
  p.poly([[x - width, y], [x - width, y - height * 0.35],
    [x + lean - 2, y - height * 0.72], [x + lean, y - height],
    [x + lean + 1, y - height * 0.59], [x + width, y - height * 0.3],
    [x + width, y]], c[3]);
  p.poly([[x - width * 0.6, y], [x - width * 0.35, y - height * 0.44],
    [x + lean * 0.65, y - height * 0.73], [x + width * 0.67, y]], c[4]);
  p.poly([[x - width * 0.38, y], [x + lean * 0.3, y - height * 0.4],
    [x + width * 0.38, y]], c[5]);
}

function embers(p, c, angle, x, y, count, width) {
  for (let j = 0; j < count; j++) {
    const age = ((angle / turn + j * 0.618) % 1 + 1) % 1;
    if (age > 0.84) continue;
    p.px(x + width * Math.sin(j * 23) + age * Math.cos(j) * 6,
      y - age * (11 + j % 9), c[age < 0.45 ? 5 : 3]);
  }
}

function hydraHead(p, c, t, head) {
  const [baseX, baseY, crownX, crownY, offset, depth] = head;
  const phase = (t + offset) % 1;
  const charge = phase > 0.72 ? (phase - 0.72) / 0.28 : 0;
  const recoil = phase < 0.14 ? Math.sin(Math.PI * phase / 0.14) : 0;
  const sway = Math.sin(turn * (t + offset));
  const x = Math.round(crownX + 2 * sway - 5 * charge - 5 * recoil);
  const y = Math.round(crownY + 2 * Math.cos(turn * (t + offset)) + 3 * charge);
  const jaw = Math.round(1 + 4 * Math.max(charge * 0.7, recoil));
  const neck = [[baseX, baseY], [baseX - 5, baseY - 8],
    [x - 10, y + 14], [x - 8, y + 7], [x - 3, y + 2]];
  for (let i = 1; i < neck.length; i++) {
    const [ax, ay] = neck[i - 1], [bx, by] = neck[i];
    p.beam(ax, ay, bx, by, 11 - i, c[0]);
  }
  for (let i = 1; i < neck.length; i++) {
    const [ax, ay] = neck[i - 1], [bx, by] = neck[i];
    p.beam(ax, ay, bx, by, 8 - i, c[depth ? 2 : 3]);
    p.beam(ax - 1, ay, bx - 1, by, 2, c[depth ? 3 : 4]);
  }
  for (const [dx, dy] of [[-9, 9], [-10, 13], [-9, 17]]) {
    p.poly([[x+dx+1,y+dy+5],[x+dx-6,y+dy-2],[x+dx-1,y+dy]], c[0]);
    p.line(x+dx-4, y+dy-1, x+dx+1, y+dy+2, c[3]);
  }

  // Horns, solid brow, open mouth and a separate lower jaw.
  const shape = (points, color) => p.poly(points.map(([dx, dy]) => [x + dx, y + dy]), color);
  shape([[-10,5],[-11,-5],[-17,-13],[-9,-10],[-6,-6],[-4,-6],[-6,-12],
    [0,-9],[2,-5],[5,-4],[8,-1],[14,-1],[17,2],[16,6],[10,8],
    [10,8+jaw],[4,10+jaw],[-4,10],[-9,8]], c[0]);
  shape([[-10,-5],[-15,-12],[-9,-9],[-6,-4],[-7,0]], c[depth ? 2 : 3]);
  shape([[-4,-6],[-5,-11],[-1,-8],[2,-4],[-2,-3]], c[3]);
  shape([[-9,4],[-8,-3],[-4,-6],[2,-4],[6,-2],[9,1],[14,1],[16,3],
    [13,5],[7,5],[2,7],[-4,8]], c[3]);
  shape([[-8,1],[-5,-4],[1,-3],[5,-1],[2,0],[-3,0],[-5,4]], c[4]);
  shape([[1,4],[6,1],[13,2],[15,3],[12,4],[7,4]], c[depth ? 3 : 4]);
  shape([[-3,8],[4,8+jaw],[10,7+jaw],[14,6+jaw],[11,9+jaw],[5,10+jaw],[-4,10]], c[depth ? 2 : 3]);
  p.line(x + 6, y + 9 + jaw, x + 11, y + 7 + jaw, c[4]);
  p.px(x + 11, y + 3, c[0]);
  p.line(x - 3, y + 1, x, y + 2, c[0]);
  p.px(x - 2, y + 1, c[6]);
  p.px(x - 1, y + 1, c[4]);
  p.px(x + 9, y + 6, c[5]);
  if (jaw > 2) p.px(x + 12, y + 5, c[5]);

  if (charge > 0.2) {
    const radius = 1 + 2.2 * charge;
    p.disc(x + 14, y + 6, radius + 1, c[3], 0.8);
    p.disc(x + 14, y + 6, radius, c[5], 1);
    p.px(x + 14, y + 6, c[6]);
  }
  if (phase < 0.27) {
    const sx = crownX + 13 + 91 * phase, sy = crownY + 6 + phase * 12;
    const size = 4 * (1 - phase / 0.32);
    p.beam(sx - 8, sy + 1, sx - 1, sy, size, c[3]);
    p.disc(sx, sy, size, c[4], 1);
    p.disc(sx + 1, sy - 1, Math.max(1, size - 1), c[6], 1);
    p.px(sx - 9, sy + 2 + sway, c[3]);
    p.px(sx - 12, sy - 1, c[2]);
  }
}

export function buildCustom(core) {
  const { hex } = core;
  const define = (id, size, origin, duration, loop, options, draw) => {
    const meta = { size, origin, duration, loop, options, fps: 20, bg: "none" };
    return {
      id: "custom/" + id, meta,
      mod: { meta, draw: (p, t, o) => draw(p, t / duration, o.palette.map(hex)) },
    };
  };
  return {
    "frozen-armor": define("frozen-armor", [48, 48], [24, 38], 1.2, true, blue, (p, t, c) => {
      for (const side of [-1, 1]) {
        for (let i = 0; i < 4; i++) {
          const pulse = (t + i / 4 + (side > 0 ? 0.5 : 0)) % 1;
          const x = side * (12 + (i % 2) * 2), y = -4 - i * 6;
          const height = 4 + i % 2;
          p.poly([[x - side * 2, y + 3], [x - side, y - height],
            [x + side * 2, y - height - 2], [x + side * 4, y - 1],
            [x + side * 2, y + 4]], c[3], 0.8);
          p.line(x + side * 2, y - height - 1, x - side, y + 2, c[pulse < 0.22 ? 7 : 5]);
        }
      }
    }),
    blizzard: define("blizzard", [94, 70], [47, 53], 1.5, true, blue, (p, t, c) => {
      for (let i = 0; i < 13; i++) {
        const phase = (t + i * 0.618) % 1;
        const x = Math.sin(i * 21) * 36, floor = Math.cos(i * 8) * 12;
        if (phase < 0.42) {
          const d = 1 - phase / 0.42;
          const headX = x - 13 * d, headY = floor - 38 * d;
          p.poly([[headX, headY], [headX - 5, headY - 8], [headX - 5, headY - 13],
            [headX - 1, headY - 9]], c[3]);
          p.line(headX, headY, headX - 3, headY - 8, c[6]);
          continue;
        }
        if (phase >= 0.76) continue;
        const age = (phase - 0.42) / 0.34;
        p.ellipse(x, floor, 2 + 7 * age, 1 + 3 * age, c[4], 0.6 * (1 - age));
        for (const spread of [-1, 0, 1]) {
          const sx = x + spread * age * 9, sy = floor - Math.sin(Math.PI * age) * (spread ? 5 : 9);
          p.line(sx, sy, sx + spread * 2, sy + 2, c[age < 0.37 ? 7 : 5], 1 - age);
        }
      }
    }),
    warmth: define("warmth", [58, 58], [29, 46], 1.5, true, fire, (p, t, c) => {
      const a = turn * t;
      for (let j = 0; j < 42; j++) {
        const age = (t * 2 + j * 0.618) % 1;
        const phase = a + j * 0.52 + age * 2.4;
        const radius = 17 - 8 * age;
        const x = Math.cos(phase) * radius, y = -age * 33 + Math.sin(phase) * 5;
        if (age < 0.94) p.px(x, y, c[age < 0.2 ? 3 : 4 + (j % 2)]);
        if (j % 7 === 0 && age < 0.8) p.px(x, y - 1, c[6]);
      }
      for (let j = 0; j < 32; j++) {
        const phase = a + j * turn / 32;
        p.px(Math.cos(phase) * 19, Math.sin(phase) * 5, c[3 + j % 3]);
      }
    }),
    "shiver-armor": define("shiver-armor", [66, 62], [33, 45], 1.2, true, blue, (p, t, c) => {
      for (let j = 0; j < 10; j++) {
        const a = Math.PI + j * turn / 10;
        const x = Math.cos(a) * 20, y = Math.sin(a) * 8;
        const lean = Math.cos(a) * 6;
        const h = 17 + 7 * Math.sin(turn * t + j * 2);
        p.poly([[x - 4, y], [x - 4, y - 6], [x + lean, y - h],
          [x + 5, y - 4], [x + 3, y + 1]], c[3]);
        p.poly([[x - 3, y - 1], [x + lean, y - h], [x + 1, y - 4]], c[6]);
        p.line(x + lean, y - h, x - 2, y - 3, c[7], 0.6);
      }
    }),
    "static-field": define("static-field", [118, 74], [59, 37], 0.85, false, blue, (p, t, c) => {
      if (t >= 0.96) return;
      const radius = 5 + 47 * (1 - (1 - t) ** 2);
      for (let j = 0; j < 64; j++) {
        const a = j * turn / 64;
        const b = (j + 1) * turn / 64;
        const flicker = Math.sin(j * 6 + t * 36);
        if (flicker < -0.1 && t > 0.4) continue;
        const x = Math.cos(a) * radius, y = Math.sin(a) * radius * 0.43 + flicker * 2;
        const nx = Math.cos(b) * radius, ny = Math.sin(b) * radius * 0.43;
        p.beam(x, y, nx, ny, 3, c[3], 1 - t);
        p.line(x, y, nx, ny, c[j % 4 ? 5 : 7], 1 - t * 0.8);
      }
    }),
    blaze: define("blaze", [70, 40], [35, 29], 1, true, fire, (p, t, c) => {
      const angle = turn * t;
      for (let j = 0; j < 7; j++) {
        const x = -20 + j * 6, y = 2 - j;
        const height = 5 + 4 * (1 + Math.sin(angle * (j % 2 + 1) + j * 2)) / 2;
        flame(p, c, x, y, 3 + j % 2, height, -2);
      }
      embers(p, c, angle, 0, -4, 20, 20);
    }),
    "fire-wall": define("fire-wall", [112, 64], [56, 50], 1.2, true, fire, (p, t, c) => {
      const a = turn * t;
      for (let j = 0; j < 15; j++) {
        const x = (j - 7) * 6;
        const end = 1 - (Math.abs(j - 7) / 8) ** 3;
        const h = end * (16 + 7 * Math.sin(2 * a + j * 3) + 5 * Math.cos(a + j));
        flame(p, c, x, -3, 4, h, 3 * Math.cos(a + j));
      }
      for (let j = 0; j < 14; j++) {
        const x = (j - 6.5) * 6;
        flame(p, c, x, 1 + j % 2, 4, 6 + 3 * Math.sin(a * 2 + j), -1);
      }
      embers(p, c, a, 0, -15, 38, 43);
    }),
    hydra: define("hydra", [128, 88], [57, 69], 1.8, true, fire, (p, t, c) => {
      const a = turn * t;
      p.ellipse(-3, 0, 27, 8, c[0], 0.8);
      p.ellipse(-3, 0, 21, 5, c[2], 0.7);
      for (let i = 0; i < 40; i++) {
        const b = i * turn / 40;
        if (Math.sin(b * 5 + a) > -0.3) {
          p.px(-3 + 24 * Math.cos(b), 7 * Math.sin(b), c[3 + i % 2]);
        }
      }
      for (const head of [[-14,-2,-24,-38,2/3,1],[3,-2,0,-48,0,1],[11,3,21,-32,1/3,0]]) {
        hydraHead(p, c, t, head);
      }
      for (let j = 0; j < 7; j++) {
        const x = j * 6 - 21;
        const y = 3 + Math.sin(j * 2) * 3;
        flame(p, c, x, y, 2.4, 4 + 3 * Math.sin(a * 2 + j), -1);
      }
      embers(p, c, a, -3, 1, 24, 25);
    }),
    "charged-bolt": define("charged-bolt", [110, 56], [13, 28], 0.85, false, blue, (p, t, c) => {
      if (t >= 0.98) return;
      for (let j = -1; j <= 1; j++) {
        const x = 4 + t * 72, y = j * (3 + t * 16);
        const length = Math.min(15, 5 + 22 * t, (1 - t) * 70);
        for (let s = 0; s < 4; s++) {
          const y1 = y + Math.sin(t * 46 + j * 2 + s * 2) * (s === 0 ? 0 : 3.5);
          const y2 = y + Math.sin(t * 46 + j * 2 + (s + 1) * 2) * 3.5;
          p.beam(x - s * length / 4, y1, x - (s + 1) * length / 4, y2, 3, c[4]);
          p.line(x - s * length / 4, y1, x - (s + 1) * length / 4, y2, c[s < 2 ? 7 : 5]);
        }
      }
    }),
    telekinesis: define("telekinesis", [80, 68], [40, 34], 0.8, false, blue, (p, t, c) => {
      if (t >= 0.94) return;
      const reach = (1 - t) ** 1.6 * 29 + 2;
      for (let j = 0; j < 4; j++) {
        const a = j * turn / 4 + t * 1.1;
        const x = Math.cos(a) * reach, y = Math.sin(a) * reach * 0.7;
        const side = Math.min(8, reach * 0.7);
        for (const sign of [-1, 1]) {
          const ex = x + sign * side * Math.sin(a) + side * Math.cos(a);
          const ey = y - sign * side * Math.cos(a) + side * Math.sin(a);
          p.beam(x, y, ex, ey, 4, c[3]);
          p.line(x, y, ex, ey, c[6]);
        }
      }
      if (t > 0.36 && t < 0.75) {
        const r = 2 + 6 * Math.sin((t - 0.36) * Math.PI / 0.39);
        p.poly([[0, -r], [r, 0], [0, r], [-r, 0]], c[5]);
        p.poly([[0, -r / 2], [r / 2, 0], [0, r / 2], [-r / 2, 0]], c[7]);
      }
    }),
  };
}
