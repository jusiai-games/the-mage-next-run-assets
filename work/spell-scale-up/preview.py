"""기본 주문 5종 미리보기 GIF, 분할 데이터, ZIP을 갱신한다.

실행: py work/spell-scale-up/preview.py (build.py 다음에 실행)
"""
import json
import math
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FX = ROOT / "exports/v1/spell-effects"
V1 = ROOT / "exports/v1"
NEAREST = Image.Resampling.NEAREST
BG = (60, 84, 72, 255)
ROW = (188, 50)
WIZARD_FEET = (22, 44)
SLIME_FEET = (164, 44)
STAFF = (31, 28)

slicing = json.loads((FX / "unity-slicing.json").read_text(encoding="utf-8"))
effects = {e["name"]: e for e in slicing["effects"]}


def update_slicing():
    updates = {
        "Fire Bolt": {"cell": [64, 40], "rows": 3, "pivotTopLeftPx": [44, 20]},
        "Magic Missile": {"cell": [48, 28], "rows": 2, "pivotTopLeftPx": [33, 14]},
    }
    for name, values in updates.items():
        effect = effects[name]
        effect.update(values)
        w, h = effect["cell"]
        px, py = effect["pivotTopLeftPx"]
        effect["pivotUnity"] = [px / w, 1 - py / h]
    effects["Fire Bolt"]["source"] = "Original project pixel art (work/spell-scale-up/build.py)"
    effects["Magic Missile"]["source"] = "Original project pixel art (work/spell-scale-up/build.py)"
    (FX / "unity-slicing.json").write_text(json.dumps(slicing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frames(name):
    effect = effects[name]
    w, h = effect["cell"]
    with Image.open(FX / effect["sheet"]) as sheet:
        sheet = sheet.convert("RGBA")
        cells = [sheet.crop(((i % 8) * w, (i // 8) * h, (i % 8) * w + w, (i // 8) * h + h))
                 for i in range(effect["frameCount"])]
    return cells, effect["pivotTopLeftPx"]


def strip(path, cell=32):
    with Image.open(path) as sheet:
        sheet = sheet.convert("RGBA")
        return [sheet.crop((i * cell, 0, i * cell + cell, cell)) for i in range(sheet.width // cell)]


WIZARD = strip(V1 / "wizard/idle/hood_staff_idle.png")
SLIME = strip(V1 / "meadow-slime/idle/slime32_idle.png")


def stage(t):
    image = Image.new("RGBA", ROW, BG)
    image.alpha_composite(WIZARD[(t // 4) % len(WIZARD)], (WIZARD_FEET[0] - 16, WIZARD_FEET[1] - 28))
    image.alpha_composite(SLIME[(t // 5) % len(SLIME)], (SLIME_FEET[0] - 16, SLIME_FEET[1] - 28))
    return image


def put(image, cell, pivot, at, angle=0.0):
    if angle:
        big = Image.new("RGBA", (cell.width * 3, cell.height * 3))
        big.alpha_composite(cell, (cell.width, cell.height))
        center = (cell.width + pivot[0], cell.height + pivot[1])
        big = big.rotate(-math.degrees(angle), resample=NEAREST, center=center)
        image.alpha_composite(big, (round(at[0] - center[0]), round(at[1] - center[1])))
    else:
        image.alpha_composite(cell, (round(at[0] - pivot[0]), round(at[1] - pivot[1])))


def projectile(name, total, t, curve=0.0):
    cells, pivot = frames(name)
    image = stage(t)
    flight = 30
    step = t % total
    if step < flight:
        s = step / flight
        x = STAFF[0] + (SLIME_FEET[0] - 10 - STAFF[0]) * s
        y = STAFF[1] + (32 - STAFF[1]) * s - curve * math.sin(math.pi * s)
        dy = (32 - STAFF[1]) / flight - curve * math.pi * math.cos(math.pi * s) / flight
        dx = (SLIME_FEET[0] - 10 - STAFF[0]) / flight
        put(image, cells[t % len(cells)], pivot, (x, y), math.atan2(dy, dx) if curve else 0.0)
    return image


def ice(total, t):
    cells, pivot = frames("Ice Bolt")
    image = stage(t)
    if t % total < len(cells):
        put(image, cells[t % total], pivot, (STAFF[0] - 4, STAFF[1] + 8))
    return image


def charged(total, t):
    cells, pivot = frames("Charged Bolt Orb")
    image = stage(t)
    for i, (phase, amp) in enumerate(((0, 6), (2.1, 9), (4.2, 5))):
        s = ((t + i * 9) % 36) / 36
        x = STAFF[0] + 120 * s
        y = STAFF[1] + 2 + amp * math.sin(s * 9 + phase)
        put(image, cells[(t + i * 4) % len(cells)], pivot, (x, y))
    return image


def shield(total, t):
    loop, pivot = frames("Magic Shield")
    block, _ = frames("Magic Shield Block")
    image = stage(t)
    put(image, loop[t % len(loop)], pivot, WIZARD_FEET)
    hit = t % 40
    if hit < len(block):
        put(image, block[hit], pivot, WIZARD_FEET)
    return image


def label(image, text, scale):
    out = image.resize((image.width * scale, image.height * scale), NEAREST)
    font = ImageFont.truetype("arial.ttf", 9 * scale)
    ImageDraw.Draw(out).text((4 * scale, 1 * scale), text, font=font, fill=(232, 236, 220))
    return out


def save_gif(path, images, duration):
    rgb = [im.convert("RGB") for im in images]
    rgb[0].save(path, save_all=True, append_images=rgb[1:], duration=duration, loop=0, optimize=False)


def main():
    update_slicing()
    total = 80
    rows = [
        ("Fire Bolt", lambda t: projectile("Fire Bolt", 40, t)),
        ("Ice Bolt", lambda t: ice(total, t)),
        ("Charged Bolt", lambda t: charged(total, t)),
        ("Magic Bolt", lambda t: projectile("Magic Missile", 40, t, curve=10)),
        ("Magic Shield", lambda t: shield(total, t)),
    ]
    images = []
    for t in range(total):
        board = Image.new("RGBA", (ROW[0] * 2, ROW[1] * 2 * len(rows)))
        for index, (title, draw) in enumerate(rows):
            board.alpha_composite(label(draw(t), title, 2), (0, index * ROW[1] * 2))
        images.append(board)
    save_gif(FX / "preview-basic-spells.gif", images, 50)

    magic = [label(projectile("Magic Missile", 40, t, curve=10), "Magic Bolt", 3) for t in range(40)]
    save_gif(FX / "preview-magic-bolt.gif", magic, 50)

    with zipfile.ZipFile(FX / "basic-spells.zip") as old:
        names = old.namelist()
    with zipfile.ZipFile(FX / "basic-spells.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(FX / name, name)


if __name__ == "__main__":
    main()
