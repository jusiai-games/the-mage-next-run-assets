"""Stage the production art pass from the original exports into a scratch directory."""

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw


def ramp(original, revised):
    return dict(zip(
        (ImageColor.getrgb("#" + value) for value in original.split()),
        (ImageColor.getrgb("#" + value) for value in revised.split()),
        strict=True,
    ))


WORLD = {
    # Blue-violet cloth, walnut, bronze and cool stone.
    **ramp("222034 28283f 393b5b 454568 505276 6a4757",
           "1d2035 292d49 3c456b 4a547d 626b97 754858"),
    **ramp("4f3333 8b6755 e4aa84 f8cfab eab853",
           "4a2d29 906047 f1b087 ffdbad f5c66c"),
    # Sky haze, hedge, turf and sunlit grass.
    **ramp("91c7c0 68865c 749466 7ca06e 8faf74 99b77d aac586 d3daa5",
           "a3c9d0 587a61 708d65 829b69 a3b478 aeba80 bec98a e1dfab"),
    **ramp("9cbb60 82a852 a9c568 547d51 a6c06f caa163",
           "b2be72 8fa360 c3ca82 5a8158 bac480 d7a66d"),
    **ramp("95d5e9 83ac86 94ba94 9ec29a b0cca5 ece5bb 769e7d 6c9175",
           "a3c9d0 809b8c 91aa97 9eb19a aebeaa e1dfbc 728e84 627d75"),
    # Cool jelly shadows and translucent mint speculars.
    **ramp("23361e 48643c 638752 86a866 bedd90",
           "193b36 285954 368471 5eac8f b8edc7"),
    **ramp("1d3a30 215d42 34815d 55a373 8bd99d",
           "193b36 285954 368471 5eac8f b8edc7"),
    # Cast flash and primary lightning bolt.
    **ramp("367cb0 589dc8 78cbf4 ade9ff f0fcff",
           "456cbd 579fe4 78dcff b9f4ff f7ffff"),
}

ELEMENTS = {
    "fire": ramp("4f3333 6a4757 8b6755 d88475 eab853 f8cfab f0fcff",
                 "3e2734 6b3542 a74739 ec6942 ffad54 ffd78f fff6dc"),
    "cold": ramp("222034 28283f 354568 393b5b 505276 367cb0 589dc8 78cbf4 91c7c0 ade9ff f0fcff",
                 "212b50 242e52 334e75 3c5590 506eb2 447ebc 64b8d8 8be7eb 97dad8 b8fff5 ecfffa"),
    "lightning": ramp("222034 28283f 393b5b 505276 367cb0 589dc8 78cbf4 ade9ff f0fcff",
                      "262044 302952 493e83 6464a5 5553bf 807af2 a8a1ff d9c6ff fbf5ff"),
}


def palette_for(path):
    if len(path.parts) > 4 and path.parts[1] == "sorceress-vfx" and path.parts[3] in ELEMENTS:
        return ELEMENTS[path.parts[3]]
    return WORLD


def apply_palette(rgba, palette):
    @lru_cache(maxsize=4096)
    def recolor(pixel):
        r, g, b, alpha = pixel
        if alpha:
            return (*palette.get((r, g, b), (r, g, b)), alpha)
        return pixel

    result = Image.new("RGBA", rgba.size)
    result.putdata([recolor(pixel) for pixel in rgba.get_flattened_data()])
    return result


def recolor_png(source, target, palette):
    with Image.open(source) as original:
        rgba = original.convert("RGBA")
    result = apply_palette(rgba, palette)
    if source.name == "game-title-background.png":
        result = title_sky(result)
    if source.name == "meadow-terrain.png":
        detail_meadow(result, 0, result.height, meadow_tile_ids())
    if source.name == "meadow_wave.png":
        detail_meadow(result, 0, result.height, range(88))
    if result.tobytes() == rgba.tobytes():
        return False
    result.save(target, optimize=True)
    with Image.open(target) as saved:
        assert saved.size == rgba.size
        assert saved.getchannel("A").tobytes() == rgba.getchannel("A").tobytes()
    return True


def title_sky(scene):
    # Put the light inside the ruin so the arch retains the foreground edge.
    magic = Image.new("RGBA", scene.size)
    draw = ImageDraw.Draw(magic)
    draw.ellipse((103, 143, 137, 177), fill="#5d94ac")
    draw.ellipse((107, 147, 133, 173), fill="#82aeb9")
    draw.ellipse((110, 150, 130, 170), fill="#b5c6be")
    draw.ellipse((113, 153, 127, 167), fill="#e9d8a7")
    draw.polygon([(120, 150), (122, 157), (129, 160), (122, 162),
                  (120, 170), (118, 162), (111, 160), (118, 158)], fill="#fff0c1")
    for x, y in [(105, 150), (135, 156), (111, 174), (125, 142), (129, 181), (101, 165)]:
        draw.point((x, y), "#e9d8a7")
        draw.point((x, y + 1), "#82aeb9")
    for y in range(scene.height):
        for x in range(scene.width):
            r, g, b, alpha = scene.getpixel((x, y))
            if b > g + 25 and g > r + 30:
                sky = (round(r * 0.79), round(g * 0.88), round(b * 0.92), alpha)
                mark = magic.getpixel((x, y))
                scene.putpixel((x, y), mark if mark[3] else sky)
    return scene


def meadow_tile_ids():
    layout = Path("exports/meadow-wave-mobile/layout.json")
    rows = json.loads(layout.read_text(encoding="utf-8"))["tile_rows"]
    return [int(tile[1:]) for row in rows for tile in row]


def detail_meadow(image, top, height, tile_ids):
    # Sparse grass blades in the flat turf. Each cluster stays inside its tile,
    # so the original perimeter pixels still meet at every 16px join.
    pixels = image.load()
    columns = image.width // 16
    assert len(tile_ids) <= columns * (height // 16)
    for index, tile_id in enumerate(tile_ids):
        variation = tile_id % 5
        if variation == 4:
            continue
        x = index % columns * 16 + 3 + variation * 2
        y = top + index // columns * 16 + 4 + variation
        patch = [(x, y), (x, y + 1), (x + 1, y + 1)]
        if all(pixels[point] == (163, 180, 120, 255) for point in patch):
            pixels[patch[0]] = (174, 189, 129, 255)
            pixels[patch[1]] = (151, 169, 109, 255)
            pixels[patch[2]] = (151, 169, 109, 255)


def inventory(stage):
    package = Path("exports/spells-to-go-ui")
    sprites = package / "package/Assets/SpellsToGo/UI/Sprites"
    output = stage / sprites
    ink, walnut, bevel, gold = "#1d2035", "#4a2d29", "#906047", "#f5c66c"
    stone, blue, well = "#626b97", "#b9f4ff", "#272b43"
    template = (sprites / "spell-clasp.png.meta").read_text(encoding="utf-8")

    def save(name, image):
        image.save(output / f"{name}.png")
        guid = hashlib.md5(f"spells-to-go/ui/{name}".encode(), usedforsecurity=False).hexdigest()
        lines = template.splitlines()
        lines[1] = f"guid: {guid}"
        (output / f"{name}.png.meta").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for state in ("normal", "selected", "locked"):
        slot = Image.new("RGBA", (24, 24))
        draw = ImageDraw.Draw(slot)
        draw.rounded_rectangle((0, 0, 23, 23), radius=3, fill=ink)
        draw.rounded_rectangle((1, 1, 22, 22), radius=3, fill=walnut)
        rim = {"normal": bevel, "selected": gold, "locked": stone}[state]
        draw.line((3, 2, 20, 2), rim)
        draw.line((2, 4, 2, 19), rim)
        draw.line((21, 4, 21, 19), "#382c3d")
        draw.rounded_rectangle((3, 3, 20, 20), radius=2, fill=ink)
        draw.rectangle((4, 4, 19, 19), fill=well)
        for xy in [(2, 2), (21, 2), (2, 21), (21, 21)]:
            draw.ellipse((xy[0] - 1, xy[1] - 1, xy[0] + 1, xy[1] + 1), fill=stone)
            draw.point(xy, fill=blue if state == "selected" else "#a0a5b9")
        if state == "locked":
            draw.rectangle((9, 8, 14, 12), outline=stone)
            draw.rectangle((8, 11, 15, 16), fill=stone)
            draw.line((11, 13, 11, 14), ink)
        save(f"inventory-slot-{state}", slot)

    icons = {
        "potion": [
            ([(6, 1), (11, 1), (11, 5), (14, 8), (14, 14), (12, 16),
              (5, 16), (3, 14), (3, 8), (6, 5)], ink),
            ([(6, 6), (11, 6), (13, 9), (13, 13), (11, 15), (6, 15),
              (4, 13), (4, 9)], "#626b97"),
            ([(5, 10), (8, 9), (12, 10), (12, 13), (10, 14), (6, 14), (5, 13)], "#df667b"),
            ([(6, 8), (6, 12), (5, 11), (5, 9)], "#ffdbad"),
            ([(7, 2), (10, 2), (10, 5), (7, 5)], gold),
        ],
        "rune": [
            ([(8, 1), (14, 4), (16, 9), (12, 15), (5, 16), (1, 11), (2, 5)], ink),
            ([(8, 2), (13, 5), (15, 9), (11, 14), (5, 15), (2, 11), (3, 5)], "#46496d"),
            ([(8, 2), (13, 5), (7, 5), (2, 11), (3, 5)], stone),
            ([(8, 5), (11, 8), (9, 8), (11, 11), (8, 13), (5, 10),
              (7, 10), (6, 8)], "#b8edc7"),
        ],
        "scroll": [
            ([(4, 1), (14, 1), (16, 3), (16, 7), (13, 7), (13, 15),
              (11, 17), (2, 17), (0, 15), (0, 12), (3, 12), (3, 3)], ink),
            ([(5, 2), (13, 2), (15, 4), (15, 6), (12, 6), (12, 15),
              (10, 16), (2, 16), (1, 14), (4, 14), (4, 4)], "#d7a66d"),
            ([(6, 3), (12, 3), (11, 6), (11, 13), (5, 13), (5, 5)], "#ffdbad"),
            ([(5, 9), (8, 8), (12, 9), (12, 10), (5, 11)], "#a74761"),
            ([(8, 8), (10, 9), (10, 11), (8, 12), (7, 11), (7, 9)], "#ec6976"),
        ],
    }
    for name, layers in icons.items():
        icon = Image.new("RGBA", (18, 18))
        draw = ImageDraw.Draw(icon)
        for points, color in layers:
            draw.polygon(points, fill=color)
        save(f"inventory-{name}", icon)



def finish_title(stage):
    source = Path("exports/meadow-tilemap/tilemap")
    folder = stage / source
    background = Image.open(folder / "game-title-background.png").convert("RGBA")
    atlas = Image.open(folder / "meadow-ui-tiles.png").convert("RGBA")
    tilemap = json.loads((source / "game-title.tmj").read_text(encoding="utf-8"))
    ids = tilemap["layers"][0]["data"]
    assert len(ids) == len(set(ids)) == 220
    for index, tile in enumerate(ids):
        x, y = (index % 10) * 16, (index // 10) * 16
        atlas.paste(background.crop((x, y, x + 16, y + 16)),
                    (((tile - 1) % 16) * 16, ((tile - 1) // 16) * 16))
    atlas.save(folder / "meadow-ui-tiles.png", optimize=True)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", type=Path)
    args = parser.parse_args()
    args.stage.mkdir(parents=True, exist_ok=False)
    tracked = subprocess.check_output(["git", "ls-files", "-z", "exports"]).decode().split("\0")
    counts = Counter()
    for entry in filter(None, tracked):
        source = Path(entry)
        if not source.is_file() or source.suffix != ".png":
            continue
        # Source art and retrospective comparison sheets are reference material.
        if "sources" in source.parts or source.name == "sorceress-vfx-meadow-review.png":
            continue
        target = args.stage / source
        target.parent.mkdir(parents=True, exist_ok=True)
        if not recolor_png(source, target, palette_for(source)):
            continue
        counts[(source.parts[1], source.suffix)] += 1
        sprite_data = source.with_suffix(".sprite.json")
        if sprite_data.exists():
            original = sprite_data.read_text(encoding="utf-8")
            digest = json.loads(original).get("sha256")
            if digest:
                updated = original.replace(digest, hashlib.sha256(target.read_bytes()).hexdigest(), 1)
                (args.stage / sprite_data).write_text(updated, encoding="utf-8", newline="\n")
    for (package, extension), count in sorted(counts.items()):
        print(f"{package} {extension}: {count}")
    inventory(args.stage)
    finish_title(args.stage)
    slicing = Path("exports/sorceress-vfx/unity-slicing.json")
    data = json.loads(slicing.read_text(encoding="utf-8"))
    for element, colors in data["palettes"].items():
        palette = ELEMENTS[element]
        data["palettes"][element] = [
            "#%02X%02X%02X" % palette.get(ImageColor.getrgb(color), ImageColor.getrgb(color))
            for color in colors
        ]
    (args.stage / slicing).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")


if __name__ == "__main__":
    main()
