from base64 import b64encode
from hashlib import sha256
from pathlib import Path
import json
import shutil
import sys

from PIL import Image, ImageColor, ImageOps
from ui_art import build_ui

GAME = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACK = HERE / "assets"
PACK.mkdir(exist_ok=True)
SCENE = GAME / "exports/meadow-wave-mobile"
SOURCE = GAME / "sources/meadow-screen-art/01/generated.png"
PASS = GAME / "work/color-pass-v3"
NEAREST = Image.Resampling.NEAREST


def open_rgba(path):
    with Image.open(path) as image:
        return image.convert("RGBA")


def save(name, image):
    path = PACK / (name + ".png")
    image.save(path, optimize=True)
    return path


def embed(path):
    return "data:image/png;base64," + b64encode(path.read_bytes()).decode("ascii")


# Keep the decorative plate on the game's logical grid.
title = ImageOps.fit(open_rgba(SOURCE), (320, 180), NEAREST)
title_path = save("title-meadow", title)

# Retain the tile sheet and layout together with the exact terrain they rebuild.
for rel in ("layout.json", "atlas/meadow_wave.sprite.json"):
    target = PACK / rel
    target.parent.mkdir(exist_ok=True)
    shutil.copyfile(SCENE / rel, target)
for name in ("distant-meadow", "spell-panel", "spell-slots"):
    shutil.copyfile(SCENE / (name + ".png"), PACK / (name + ".png"))

# Keep the battle floor quieter than the title grass while matching its sunlight.
colors = {
    "#68865C": "#547D51", "#749466": "#6F9254", "#7CA06E": "#82A852",
    "#8FAF74": "#9CBB60", "#99B77D": "#A9C568", "#AAC586": "#BCD17A",
    "#D3DAA5": "#DADEA2",
}
palette = {ImageColor.getrgb(old): ImageColor.getrgb(new) for old, new in colors.items()}


def meadow_variant(source):
    image = open_rgba(SCENE / source)
    pixels = [
        (*palette.get((r, g, b), (r, g, b)), a)
        for r, g, b, a in image.get_flattened_data()
    ]
    image.putdata(pixels)
    return image


terrain = meadow_variant("meadow-terrain.png")
hedge = meadow_variant("meadow-hedge.png")
save("meadow-terrain", terrain)
save("meadow-hedge", hedge)
atlas_path = save("atlas/meadow_wave", meadow_variant("atlas/meadow_wave.png"))
sprites_path = PACK / "atlas/meadow_wave.sprite.json"
sprites = json.loads(sprites_path.read_text())
sprites["sha256"] = sha256(atlas_path.read_bytes()).hexdigest()
sprites_path.write_text(json.dumps(sprites, indent=2) + "\n")
(PACK / "meadow-palette-remap.json").write_text(json.dumps(colors, indent=2) + "\n")
sky = title.crop((0, 26, 320, 111))
field = Image.new("RGBA", (320, 180))
field.alpha_composite(sky)
field.alpha_composite(terrain, (0, 80))
field.alpha_composite(ImageOps.mirror(terrain), (160, 80))
field.alpha_composite(hedge, (0, 70))
field.alpha_composite(ImageOps.mirror(hedge), (160, 70))
field_path = save("battle-meadow", field)
assert field.getchannel("A").getextrema() == (255, 255)

wizard = PASS / "hood-staff-quick-state-transitions"
slimes = PASS / "slime32-v7-state-transitions"
frames = {
    "mage": wizard / "hood_staff_idle_right_00.png",
    "cast": wizard / "hood_staff_cast_right_02.png",
    "slime": slimes / "slime32_idle_left_00.png",
    "attack": slimes / "slime32_attack_left_01.png",
}
assets = {"title": title_path, "field": field_path}
for key, path in frames.items():
    assets[key] = save(path.stem, open_rgba(path))

fx = GAME / "exports/magic-bolt-electric"
bolt = open_rgba(fx / "flight/magic_bolt_electric.png").crop((64, 0, 96, 32))
impact = open_rgba(fx / "impact/magic_bolt_electric_impact.png").crop((32, 0, 64, 32))
assets["bolt"] = save("magic-bolt-flight", bolt)
assets["impact"] = save("magic-bolt-impact", impact)


def icon(image, colors):
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha:
                index = min(3, (int((red * 2 + green * 5 + blue) / 8) // 64))
                pixels[x, y] = (*colors[index], alpha)
    shape = image.crop(image.getbbox())
    shape.thumbnail((22, 22), NEAREST)
    tile = Image.new("RGBA", (24, 24))
    tile.alpha_composite(shape, ((24 - shape.width) // 2, (24 - shape.height) // 2))
    return tile


assets["fire"] = save("icon-fire", icon(bolt.rotate(42, resample=NEAREST, expand=True), [
    (139, 63, 69), (211, 85, 59), (250, 155, 70), (255, 236, 170)
]))
assets["lightning"] = save("icon-lightning", icon(bolt.rotate(-55, resample=NEAREST, expand=True), [
    (57, 88, 148), (83, 132, 218), (106, 222, 255), (230, 252, 255)
]))
assets["burst"] = save("icon-burst", icon(impact, [
    (102, 57, 136), (136, 81, 185), (204, 139, 245), (251, 219, 255)
]))

atlas = open_rgba(atlas_path)
layout = json.loads((PACK / "layout.json").read_text())
by_id = {s["name"].rsplit("_", 1)[1]: s for s in sprites["sprites"]}
rebuilt = Image.new("RGBA", terrain.size)
for j, row in enumerate(layout["tile_rows"]):
    for i, tile in enumerate(row):
        data = by_id[tile]
        x, y = data["x"], data["y"]
        rebuilt.paste(atlas.crop((x, y, x + 16, y + 16)), (i * 16, j * 16))
assert rebuilt.tobytes() == terrain.tobytes(), "Tile atlas and layout do not recreate the terrain"

source = (HERE / "screen.html").read_text(encoding="utf-8")
assets.update(build_ui(PACK / "ui"))
source = source.replace("__UI_THEME__", (HERE / "theme.css").read_text(encoding="utf-8"))
assert source.count("__ASSETS__") == 1
html = source.replace("__ASSETS__", json.dumps({key: embed(path) for key, path in assets.items()}))
Path(sys.argv[1]).write_text(html, encoding="utf-8")

