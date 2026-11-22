"""파이어 볼트와 매직 볼트(Magic Missile) 시트를 약 1.5배 크기로 다시 그린다.

실행: py work/spell-scale-up/build.py
출력: exports/v1/spell-effects/spritesheets/{fire/fire-bolt,arcane/magic-missile}.png
"""
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SHEETS = ROOT / "exports/v1/spell-effects/spritesheets"
COLUMNS = 8


def rgba(hex_color, alpha=255):
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def sheet(frames, cell):
    rows = math.ceil(len(frames) / COLUMNS)
    out = Image.new("RGBA", (cell[0] * COLUMNS, cell[1] * rows))
    for index, frame in enumerate(frames):
        out.alpha_composite(frame, ((index % COLUMNS) * cell[0], (index // COLUMNS) * cell[1]))
    return out


# ---------------------------------------------------------------- 파이어 볼트
FIRE = ["#3E2734", "#6B3542", "#A74739", "#EC6942", "#FFAD54", "#FFD78F", "#FFF6DC"]
FIRE_CELL = (64, 40)
FIRE_HEAD = (44.0, 20.0)
FIRE_FRAMES = 24


def fire_frame(f):
    w, h = FIRE_CELL
    hx, hy = FIRE_HEAD
    phi = 2 * math.pi * f / FIRE_FRAMES
    radius, length = 6.0, 32.0
    image = Image.new("RGBA", FIRE_CELL)
    px = image.load()
    for y in range(h):
        for x in range(w):
            cx, cy = x + 0.5, y + 0.5
            # 진행 방향으로 살짝 눌린 머리
            d = math.hypot((cx - hx) * (1.15 if cx > hx else 0.9), cy - hy)
            head = 1.05 - d / (radius + 1.5)
            tail = 0.0
            dx = hx - cx
            if dx > 0:
                t = dx / length
                if t < 1:
                    centre = hy + 1.2 * math.sin(dx * 0.33 - 2 * phi) * t
                    half = 6.6 * (1 - t) ** 0.6 + 0.8
                    tail = (1 - abs(cy - centre) / half) * (1 - t) ** 0.45
                    noise = (0.12 * math.sin(0.62 * cx + 0.9 * cy + 3 * phi)
                             + 0.09 * math.sin(1.1 * cx - 0.7 * cy + 5 * phi + 1.3)
                             + 0.06 * math.sin(1.9 * cx + 1.7 * cy + 7 * phi + 2.1))
                    tail += noise * (0.3 + 0.8 * t)
            level = max(head, tail)
            if level > 0.86:
                color = FIRE[6]
            elif level > 0.7:
                color = FIRE[5]
            elif level > 0.52:
                color = FIRE[4]
            elif level > 0.36:
                color = FIRE[3]
            elif level > 0.22:
                color = FIRE[2]
            elif level > 0.12 and dx > 4:
                color = FIRE[1]
            else:
                # 머리 주변의 옅은 열기
                if d < radius + 3.5:
                    px[x, y] = rgba(FIRE[4], 56)
                elif d < radius + 6:
                    px[x, y] = rgba(FIRE[3], 32)
                continue
            px[x, y] = rgba(color)

    # 꼬리에서 뒤로 흩어지는 불티
    for i in range(7):
        travel = (f * 2 + i * 9) % 26
        sx = int(hx - 9 - travel)
        sy = int(hy + (-6, 5, -3, 7, 2, -8, 4)[i] + ((-1) ** i) * travel // 9)
        if 0 <= sx < w and 0 <= sy < h and px[sx, sy][3] < 255:
            px[sx, sy] = rgba(FIRE[4] if travel < 10 else FIRE[3] if travel < 18 else FIRE[2])
    return image


# ---------------------------------------------------------------- 매직 볼트
ARCANE = ["#223D77", "#2F61AD", "#378CEE", "#65C6FF", "#B5EBFF", "#F0FCFF"]
MAGIC_CELL = (48, 28)
MAGIC_CORE = (33.0, 14.0)
MAGIC_FRAMES = 16


def wrap(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


def magic_frame(f):
    w, h = MAGIC_CELL
    ox, oy = MAGIC_CORE
    phi = 2 * math.pi * f / MAGIC_FRAMES
    radius = 7.2
    image = Image.new("RGBA", MAGIC_CELL)
    px = image.load()

    # 탄두 뒤의 짧은 원뿔
    for y in range(h):
        for x in range(w):
            cx, cy = x + 0.5, y + 0.5
            dx = ox - cx
            if 0 < dx < 15:
                half = (radius - 1.2) * (1 - dx / 15) ** 1.2
                if abs(cy - oy) <= half:
                    px[x, y] = rgba(ARCANE[2] if abs(cy - oy) < half * 0.45 else ARCANE[1])

    # 길이가 출렁이는 잔광 줄기
    streaks = ((0, 26, 0.0), (-2, 21, 1.7), (2, 20, 3.4), (-4, 14, 0.9), (4, 13, 2.6), (-6, 8, 4.1), (6, 7, 5.2))
    for dy, base, seed in streaks:
        length = base + round(2.5 * math.sin(phi * 2 + seed))
        y = int(oy + dy)
        for step in range(length):
            x = int(ox - 3 - step)
            if not (0 <= x < w and 0 <= y < h):
                continue
            t = step / max(1, length)
            if dy == 0:
                color = ARCANE[4] if t < 0.35 else ARCANE[3] if t < 0.7 else ARCANE[2]
            else:
                color = ARCANE[3] if t < 0.4 else ARCANE[2] if t < 0.75 else ARCANE[1]
            px[x, y] = rgba(color)

    # 떨어져 흐르는 짧은 파편
    for i, (dy, offset) in enumerate(((-5, 0), (3, 7), (-1, 13), (5, 4), (-3, 10))):
        travel = (f * 2 + offset * 2) % 18
        x0 = int(ox - 16 - travel)
        y = int(oy + dy)
        for k in range(2 if travel < 12 else 1):
            x = x0 - k
            if 0 <= x < w and px[x, y][3] == 0:
                px[x, y] = rgba(ARCANE[2] if travel < 9 else ARCANE[1])

    # 둥근 탄두와 안에서 도는 하이라이트
    spin = phi
    for y in range(h):
        for x in range(w):
            cx, cy = x + 0.5, y + 0.5
            d = math.hypot(cx - ox, cy - oy)
            if d > radius:
                continue
            if d > radius - 1.2:
                color = 0
            elif d > radius - 2.4:
                color = 1
            else:
                dh = math.hypot(cx - (ox + 1.6), cy - (oy - 1.4))
                color = 5 if dh < 1.8 else 4 if dh < 3.2 else 3 if dh < 5.0 else 2
                angle = math.atan2(cy - oy, cx - ox)
                if 2.6 < d < 4.9 and min(abs(wrap(angle - spin)), abs(wrap(angle - spin - math.pi))) < 0.45:
                    color = min(5, color + 1)
            px[x, y] = rgba(ARCANE[color])
    return image


def main():
    sheet([fire_frame(f) for f in range(FIRE_FRAMES)], FIRE_CELL).save(SHEETS / "fire/fire-bolt.png", optimize=True)
    sheet([magic_frame(f) for f in range(MAGIC_FRAMES)], MAGIC_CELL).save(SHEETS / "arcane/magic-missile.png", optimize=True)


if __name__ == "__main__":
    main()
