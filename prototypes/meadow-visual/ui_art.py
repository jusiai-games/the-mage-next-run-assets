"""Build pixel UI textures from the meadow game's existing UI and spell colors."""
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK = "#222034"
PANEL = "#28283F"
EDGE = "#393B5B"
SLATE = "#505276"
CREAM = "#F8CFAB"
GOLD = "#EAB853"
BRONZE = "#8B6755"
BLUE = "#589DC8"
SKY = "#78CBF4"
ICE = "#ADE9FF"
WHITE = "#F0FCFF"
ROSE = "#E4AA84"
WOOD_DARK = "#4F3333"


def timber_plate(face, board, light, grain, *, panel=False):
    width, height = 32, 32 if panel else 24
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    right, bottom = width - 1, height - 1
    draw.polygon([(3, 0), (right - 4, 0), (right - 4, 1), (right - 2, 1),
                  (right - 2, 2), (right - 1, 2), (right - 1, 4), (right, 4),
                  (right, bottom - 3), (right - 1, bottom - 3), (right - 1, bottom - 1),
                  (right - 3, bottom - 1), (right - 3, bottom), (3, bottom),
                  (3, bottom - 1), (1, bottom - 1), (1, bottom - 3),
                  (0, bottom - 3), (0, 4), (1, 4), (1, 2), (3, 2)], fill=INK)
    draw.rectangle((3, 2, right - 3, bottom - 2), fill=board)
    draw.rectangle((2, 4, right - 2, bottom - 4), fill=board)
    draw.line((6, 1, right - 6, 1), fill=light)
    draw.line((5, bottom - 2, right - 5, bottom - 2), fill=WOOD_DARK)
    draw.rectangle((4, 5, right - 4, bottom - 5), fill=face)
    draw.line((7, 3, right - 7, 3), fill=grain)
    draw.line((8, bottom - 3, right - 8, bottom - 3), fill=board)
    draw.line((5, 2, 12, 2), fill=grain)
    draw.line((right - 10, bottom - 4, right - 6, bottom - 4), fill=board)
    draw.line((3, 7, 3, bottom - 8), fill=grain)
    draw.line((right - 3, 8, right - 3, bottom - 7), fill=grain)

    # Pebbles stay inside the fixed corners when the center or edges stretch.
    draw.polygon([(2, 1), (5, 1), (7, 3), (6, 5), (3, 5), (1, 3)], fill=EDGE)
    draw.polygon([(2, 2), (5, 2), (6, 3), (5, 4), (2, 4), (1, 3)], fill=SLATE)
    draw.line((2, 2, 4, 2), fill="#D3DAA5")
    draw.polygon([(right - 5, bottom - 5), (right - 2, bottom - 4),
                  (right - 1, bottom - 2), (right - 3, bottom - 1),
                  (right - 6, bottom - 2), (right - 7, bottom - 4)], fill=EDGE)
    draw.line((right - 6, bottom - 4, right - 3, bottom - 4), fill=SLATE)
    draw.point((right - 5, bottom - 4), fill="#D3DAA5")
    if panel:
        draw.polygon([(right - 6, 2), (right - 3, 1), (right - 1, 3),
                      (right - 2, 5), (right - 5, 4)], fill=EDGE)
        draw.point((right - 3, 2), fill="#D3DAA5")
        draw.polygon([(2, bottom - 5), (5, bottom - 4), (6, bottom - 2),
                      (2, bottom - 2), (1, bottom - 3)], fill=SLATE)
        draw.point((2, bottom - 4), fill="#D3DAA5")
    return image


def pip(color, edge):
    image = Image.new("RGBA", (9, 9))
    draw = ImageDraw.Draw(image)
    draw.polygon([(1, 0), (7, 0), (8, 1), (8, 4), (4, 8), (0, 4), (0, 1)], fill=INK)
    draw.polygon([(1, 1), (7, 1), (7, 4), (4, 7), (1, 4)], fill=edge)
    draw.polygon([(2, 2), (6, 2), (6, 4), (4, 6), (2, 4)], fill=color)
    return image


def ward(mode):
    image = Image.new("RGBA", (52, 40))
    draw = ImageDraw.Draw(image)
    arc = [(14, 3), (20, 1), (34, 1), (40, 4), (46, 10), (48, 16),
           (48, 24), (45, 31), (40, 35), (33, 38), (18, 38), (12, 35)]
    draw.polygon(arc + [(6, 30), (3, 22), (4, 15), (8, 8)], fill=(88, 157, 200, 42))
    dark, light = (BRONZE, CREAM) if mode == "weak" else (BLUE, WHITE if mode == "hit" else ICE)
    draw.line(arc[:8], fill=dark, width=3)
    draw.line(arc, fill=light, width=2 if mode == "hit" else 1)
    draw.line([(21, 4), (34, 4), (39, 7), (42, 10)], fill=(173, 233, 255, 116))
    draw.point((6, 12), fill=light)
    draw.point((4, 24), fill=light)
    if mode == "weak":
        for points in [[(46, 11), (41, 14), (44, 17), (39, 21)], [(42, 16), (38, 16), (35, 19)],
                       [(44, 30), (40, 28), (37, 29)]]:
            draw.line(points, fill=CREAM, width=1)
    if mode == "hit":
        for points in [[(47, 9), (50, 14), (50, 25), (46, 32)], [(43, 14), (45, 18), (45, 24), (42, 28)]]:
            draw.line(points, fill=WHITE, width=1)
    return image


def portal():
    image = Image.new("RGBA", (48, 64))
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 1, 45, 62), fill=(80, 82, 118, 150), outline=SLATE, width=2)
    draw.ellipse((5, 3, 42, 60), fill=(34, 32, 52, 210), outline=ICE, width=2)
    draw.arc((9, 7, 38, 56), 20, 280, fill=BLUE, width=2)
    draw.arc((14, 13, 33, 51), 180, 550, fill=SKY, width=2)
    draw.arc((17, 18, 30, 44), 40, 310, fill=ICE, width=2)
    draw.ellipse((21, 24, 26, 39), fill=WHITE)
    for x, y in [(6, 16), (3, 38), (41, 22), (46, 29), (33, 55), (39, 52)]:
        draw.line((x - 1, y, x + 1, y), fill=ICE)
        draw.point((x, y - 1), fill=WHITE)
    return image


def symbol(name):
    image = Image.new("RGBA", (13, 13))
    draw = ImageDraw.Draw(image)
    if name == "rune":
        draw.polygon([(6, 0), (8, 4), (12, 6), (8, 8), (6, 12), (4, 8), (0, 6), (4, 4)], fill=GOLD)
        draw.polygon([(6, 3), (7, 5), (9, 6), (7, 7), (6, 9), (5, 7), (3, 6), (5, 5)], fill=CREAM)
    elif name == "plus":
        draw.rectangle((5, 2, 7, 10), fill=SLATE)
        draw.rectangle((2, 5, 10, 7), fill=SLATE)
        draw.line((2, 5, 10, 5), fill=ICE)
        draw.line((5, 2, 5, 4), fill=ICE)
    elif name == "warning":
        draw.polygon([(3, 0), (9, 0), (12, 3), (12, 9), (9, 12), (3, 12),
                      (0, 9), (0, 3)], fill=INK)
        draw.rectangle((2, 3, 10, 9), fill=GOLD)
        draw.rectangle((4, 2, 8, 10), fill=GOLD)
        draw.rectangle((6, 3, 7, 6), fill=INK)
        draw.rectangle((6, 8, 7, 9), fill=INK)
    else:
        draw.line([(4, 3), (7, 6), (4, 9)], fill=CREAM, width=2)
    return image


def wordmark():
    image = Image.new("RGBA", (153, 51))
    # Rasterize to a binary mask so the title uses the same logical grid as the HUD.
    font = ImageFont.truetype(str(Path(os.environ["WINDIR"]) / "Fonts" / "georgiab.ttf"), 24)
    for text, y, color in [("THE MAGE", -3, CREAM), ("NEXT RUN", 21, GOLD)]:
        mask = Image.new("L", image.size)
        ImageDraw.Draw(mask).text((1, y), text, font=font, fill=255)
        mask = mask.point(lambda value: 255 if value >= 118 else 0)
        shifted = Image.new("L", image.size)
        shifted.paste(mask, (1, 2))
        image.paste(INK, (0, 0, *image.size), shifted)
        image.paste(color, (0, 0, *image.size), mask)
    return image


def spell_card(illustration, light):
    """Make a text-free, portrait-shaped card for the reward hand."""
    image = Image.new("RGBA", (44, 64))
    draw = ImageDraw.Draw(image)
    draw.polygon([(3, 0), (40, 0), (43, 3), (43, 60), (40, 63), (3, 63),
                  (0, 60), (0, 3)], fill=INK)
    draw.polygon([(3, 1), (40, 1), (42, 3), (42, 60), (40, 62), (3, 62),
                  (1, 60), (1, 3)], fill=BRONZE)
    draw.rectangle((2, 2, 41, 61), fill=WOOD_DARK)
    draw.rectangle((3, 3, 40, 60), fill=CREAM, outline=GOLD)
    draw.rectangle((3, 4, 40, 27), fill=INK)
    image.paste(illustration, (4, 4))
    draw.line((4, 28, 39, 28), fill=light)
    draw.line((4, 38, 39, 38), fill=BRONZE)
    draw.line((4, 59, 39, 59), fill=ROSE)
    draw.line((3, 4, 3, 59), fill=GOLD)
    draw.line((40, 4, 40, 59), fill=GOLD)
    for x, side in ((4, 1), (39, -1)):
        for y, end in ((4, 1), (59, -1)):
            draw.line([(x, y + 4 * end), (x, y), (x + 5 * side, y)], fill=CREAM)
            draw.line([(x + side, y + 3 * end), (x + 3 * side, y + end)], fill=BRONZE)
            draw.point((x + 2 * side, y + 2 * end), fill=GOLD)
        draw.point((x + side, 33), fill=BRONZE)
    return image


def build_ui(destination):
    destination.mkdir(exist_ok=True)
    # center, board, upper bevel, grain
    plates = {
        "panel": (WOOD_DARK, BRONZE, ROSE, WOOD_DARK),
        "hud": (INK, WOOD_DARK, BRONZE, INK),
        "primary": (BRONZE, WOOD_DARK, ROSE, BRONZE),
        "primary-hover": (BRONZE, WOOD_DARK, CREAM, ROSE),
        "primary-pressed": (WOOD_DARK, WOOD_DARK, BRONZE, INK),
        "secondary": (WOOD_DARK, BRONZE, ROSE, WOOD_DARK),
        "card": (PANEL, WOOD_DARK, BRONZE, INK),
        "focus": (PANEL, BRONZE, GOLD, CREAM),
        "empty": (INK, WOOD_DARK, BRONZE, INK),
        "disabled": (EDGE, WOOD_DARK, SLATE, PANEL),
    }
    images = {key: timber_plate(*colors, panel=key in {"panel", "card", "focus", "empty"})
              for key, colors in plates.items()}
    images.update({f"shield-{mode}": ward(mode) for mode in ("normal", "hit", "weak")})
    images.update({
        "pip-on": pip(ICE, BLUE), "pip-low": pip(CREAM, BRONZE), "pip-off": pip(PANEL, SLATE),
        "portal": portal(), "title-lockup": wordmark(),
    })
    images.update({key: symbol(key) for key in ("plus", "rune", "arrow", "warning")})
    art = Path(__file__).resolve().parent / "assets" / "ui"
    for key, light in (("fire", GOLD), ("lightning", ICE), ("burst", ROSE)):
        with Image.open(art / f"card-art-{key}.png") as illustration:
            assert illustration.size == (36, 24), key
            images[f"hand-{key}"] = spell_card(illustration.convert("RGB"), light)
    manifest = {}
    paths = {}
    for key, image in images.items():
        colors = set(image.get_flattened_data())
        if key not in {"shield-normal", "shield-hit", "shield-weak", "portal"}:
            assert {pixel[3] for pixel in colors} <= {0, 255}, key
        assert image.getbbox() is not None, key
        path = destination / f"{key}.png"
        image.save(path, optimize=True)
        paths[f"ui-{key}"] = path
        manifest[path.name] = {"size": image.size}
        if key in plates:
            manifest[path.name]["border_px"] = {"top": 6, "right": 8, "bottom": 6, "left": 8}
    (destination / "sprites.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    build_ui(parser.parse_args().destination)

