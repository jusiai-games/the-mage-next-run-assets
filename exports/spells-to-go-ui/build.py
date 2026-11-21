"""Build the meadow game's carved UI frames and Unity 9-slice sprites."""

import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageColor, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
GAME = HERE.parents[1]
PROTOTYPES = GAME / "prototypes"
PACK = HERE / "package"
SPRITES = PACK / "Assets/SpellsToGo/UI/Sprites"
TILE = 12
NEAREST = Image.Resampling.NEAREST
INK = "#222034"
NAVY = "#28283F"
WOOD = "#4F3333"
BRONZE = "#8B6755"
COPPER = "#E4AA84"
GOLD = "#EAB853"
PARCHMENT = "#F8CFAB"
SLATE = "#505276"
STONE = "#393B5B"
LICHEN = "#D3DAA5"

# Top highlight, rim, inset rule and field.
FRAMES = {
    "panel": (COPPER, BRONZE, BRONZE, WOOD),
    "dialogue": (COPPER, BRONZE, COPPER, PARCHMENT),
    "nameplate": (COPPER, BRONZE, STONE, NAVY),
    "button-normal": (COPPER, WOOD, WOOD, BRONZE),
    "button-highlighted": (PARCHMENT, GOLD, WOOD, BRONZE),
    "button-pressed": (BRONZE, WOOD, INK, WOOD),
    "button-disabled": (SLATE, STONE, STONE, NAVY),
}


def save_sprite(name, image, border):
    path = SPRITES / f"{name}.png"
    image.save(path, optimize=True)
    guid = uuid5(NAMESPACE_URL, f"spells-to-go/ui/{path.name}").hex
    path.with_suffix(".png.meta").write_text(f"""fileFormatVersion: 2
guid: {guid}
TextureImporter:
  serializedVersion: 13
  mipmaps:
    enableMipMap: 0
    sRGBTexture: 1
  isReadable: 0
  textureSettings:
    serializedVersion: 2
    filterMode: 0
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  spriteMode: 1
  spriteExtrude: 1
  spriteMeshType: 0
  spritePixelsToUnits: 32
  spritePivot: {{x: 0.5, y: 0.5}}
  spriteBorder: {{x: {border}, y: {border}, z: {border}, w: {border}}}
  alphaUsage: 1
  alphaIsTransparency: 1
  textureType: 8
  textureShape: 1
  maxTextureSize: 2048
  platformSettings:
  - serializedVersion: 3
    buildTarget: DefaultTexturePlatform
    maxTextureSize: 2048
    textureFormat: -1
    textureCompression: 0
    compressionQuality: 50
    crunchedCompression: 0
    overridden: 0
""", encoding="utf-8")


def frame(colors, *, corner_stones):
    highlight, rim, inset_rule, field = colors
    extent = TILE * 3 - 1
    image = Image.new("RGBA", (extent + 1, extent + 1))
    draw = ImageDraw.Draw(image)

    def bevel(inset, chamfer, color):
        left, right = inset, extent - inset
        draw.polygon(
            [(left + chamfer, left), (right - chamfer, left), (right, left + chamfer),
             (right, right - chamfer), (right - chamfer, right), (left + chamfer, right),
             (left, right - chamfer), (left, left + chamfer)],
            fill=color,
        )

    bevel(0, 3, INK)
    bevel(1, 3, rim)
    bevel(2, 2, inset_rule)
    bevel(3, 1, field)
    draw.line((5, 1, extent - 5, 1), fill=highlight)

    if corner_stones:
        for flip_x in (False, True):
            for flip_y in (False, True):
                x = extent - 3 if flip_x else 3
                y = extent - 3 if flip_y else 3
                draw.polygon([(x-2, y), (x, y-2), (x+2, y), (x, y+2)], fill=INK)
                draw.line((x-1, y, x+1, y), fill=SLATE)
                draw.point((x, y-1), fill=LICHEN)
    return image


def dialogue_tail():
    image = Image.new("RGBA", (24, 12))
    draw = ImageDraw.Draw(image)
    draw.polygon([(2, 0), (21, 0), (13, 10), (11, 11), (9, 10)], fill=INK)
    draw.polygon([(4, 0), (19, 0), (12, 9), (10, 9)], fill=BRONZE)
    draw.polygon([(5, 0), (18, 0), (11, 8)], fill=PARCHMENT)
    return image


def speaker_scroll():
    image = Image.new("RGBA", (36, 36))
    draw = ImageDraw.Draw(image)
    # The reverse side is drawn first so the visible paper overlaps the rolls.
    draw.polygon([(3, 9), (3, 6), (5, 3), (8, 3), (11, 5), (11, 9),
                  (8, 13), (5, 13), (3, 11)], fill=BRONZE)
    draw.polygon([(4, 7), (6, 4), (8, 4), (10, 6), (10, 8),
                  (7, 10), (4, 11)], fill=COPPER)
    draw.line([(5, 8), (6, 6), (8, 6), (9, 7)], fill=WOOD)
    draw.line([(5, 5), (6, 4), (8, 4)], fill=PARCHMENT)

    draw.polygon([(26, 24), (31, 23), (34, 25), (34, 30), (32, 33),
                  (27, 33), (25, 31), (25, 27)], fill=BRONZE)
    draw.polygon([(28, 26), (33, 25), (33, 29), (31, 32), (28, 32),
                  (26, 30)], fill=COPPER)
    draw.line([(27, 30), (29, 29), (32, 29), (32, 30), (30, 31),
               (28, 31)], fill=WOOD)
    draw.line([(28, 32), (31, 32), (33, 30)], fill=PARCHMENT)

    # The straight front strip turns across the ends without a raised frame.
    draw.polygon([(4, 10), (8, 8), (30, 8), (32, 10), (33, 24),
                  (31, 27), (27, 28), (8, 28), (6, 26)], fill=PARCHMENT)
    draw.polygon([(4, 10), (6, 9), (6, 14), (7, 23), (9, 27),
                  (7, 27), (6, 26)], fill=COPPER)
    draw.polygon([(30, 8), (32, 10), (33, 24), (31, 27),
                  (28, 27), (30, 24), (31, 19), (31, 12)], fill=COPPER)
    draw.line([(4, 10), (8, 8), (30, 8), (32, 10)], fill=COPPER)
    draw.line([(6, 26), (8, 28), (27, 28), (31, 27), (33, 24)], fill=BRONZE)
    draw.line([(4, 10), (5, 13), (6, 23), (6, 26)], fill=COPPER)
    draw.line([(32, 11), (32, 20), (33, 24)], fill=COPPER)

    strip = image.crop((TILE, 0, TILE * 2, image.height))
    if strip.crop((0, 0, 1, image.height)).resize(strip.size, NEAREST).tobytes() != strip.tobytes():
        raise ValueError("The scroll centre must stay straight while stretched")
    return image


def spell_clasp():
    image = Image.new("RGBA", (12, 12))
    draw = ImageDraw.Draw(image)
    draw.polygon([(5, 0), (7, 0), (8, 4), (11, 5), (11, 7), (8, 8),
                  (7, 11), (5, 11), (4, 8), (0, 7), (0, 5), (4, 4)], fill=INK)
    draw.polygon([(6, 1), (7, 5), (10, 6), (7, 7), (6, 10), (5, 7), (1, 6), (5, 5)], fill=GOLD)
    draw.point((6, 6), fill=PARCHMENT)
    return image


def panel_crest():
    image = Image.new("RGBA", (36, 12))
    draw = ImageDraw.Draw(image)
    for offset in (0, 1):
        def wing(points):
            return [(35 - x if offset else x, y) for x, y in points]

        draw.polygon(wing([(0, 6), (4, 6), (8, 2), (14, 1), (18, 5),
                           (18, 10), (9, 10), (5, 9), (1, 9)]), fill=INK)
        draw.polygon(wing([(2, 7), (5, 7), (9, 3), (13, 2), (16, 5),
                           (16, 8), (9, 9), (6, 8)]), fill=WOOD)
        draw.line(wing([(4, 7), (7, 7), (10, 4), (13, 3), (15, 4)]), fill=BRONZE)
        draw.line(wing([(8, 7), (11, 5), (14, 5)]), fill=COPPER)
    image.alpha_composite(spell_clasp(), (12, 0))
    return image


def sliced(image, width, height):
    result = Image.new("RGBA", (width, height))
    x_edges = (0, TILE, width - TILE, width)
    y_edges = (0, TILE, height - TILE, height)
    for row in range(3):
        for col in range(3):
            patch = image.crop((col * TILE, row * TILE, (col + 1) * TILE, (row + 1) * TILE))
            size = (x_edges[col + 1] - x_edges[col], y_edges[row + 1] - y_edges[row])
            result.paste(patch.resize(size, NEAREST), (x_edges[col], y_edges[row]))
    for left, top in ((0, 0), (width - TILE, 0), (0, height - TILE), (width - TILE, height - TILE)):
        x = 0 if left == 0 else 2 * TILE
        y = 0 if top == 0 else 2 * TILE
        assert result.crop((left, top, left + TILE, top + TILE)).tobytes() == image.crop(
            (x, y, x + TILE, y + TILE)
        ).tobytes()
    return result


def preview(sprites, ornaments):
    image = Image.new("RGB", (984, 618), INK)
    draw = ImageDraw.Draw(image)
    heading = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 32)
    body = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 20)
    small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 17)
    cream = PARCHMENT

    def place(sprite, x, y):
        enlarged = sprite.resize((sprite.width * 3, sprite.height * 3), NEAREST)
        image.paste(enlarged, (x, y), enlarged)

    def label(x, y, value, font=body, fill=cream):
        draw.text((x, y), value, font=font, fill=fill)

    meadow = PROTOTYPES / "meadow-visual/assets/title-meadow.png"
    with Image.open(meadow) as background:
        backdrop = background.convert("RGB").crop((0, 35, 320, 156)).resize((960, 363), NEAREST)
    image.paste(Image.blend(backdrop, Image.new("RGB", backdrop.size, INK), 0.56), (12, 101))
    label(38, 26, "주문 넣고 갑니다", heading)
    label(39, 71, "Unity UI · 12×12px 타일 · 9슬라이스", small, LICHEN)

    place(ornaments["dialogue-tail"], 550, 371)
    place(sliced(sprites["panel"], 144, 76), 38, 158)
    place(ornaments["panel-crest"], 200, 143)
    place(sliced(sprites["dialogue"], 144, 76), 514, 158)
    place(sliced(sprites["speaker-scroll"], 84, 28), 536, 125)
    draw.text((662, 168), "초원 마법 상인", font=body, fill=WOOD, anchor="mm")
    label(71, 196, "보유 주문", body)
    draw.line((72, 232, 433, 232), fill=BRONZE, width=2)
    for index, (spell, name) in enumerate((("fire", "화염탄"), ("lightning", "연쇄 번개"), ("burst", "마력 폭발"))):
        x = 75 + 125 * index
        place(sliced(sprites["nameplate"], 34, 28), x, 247)
        with Image.open(PROTOTYPES / f"meadow-visual/assets/icon-{spell}.png") as art:
            place(art.convert("RGBA"), x + 15, 253)
        draw.text((x + 51, 344), name, font=small, fill=PARCHMENT, anchor="mm")

    label(553, 214, "다음 길에 쓸 주문을 골라 봐.", body, WOOD)
    label(553, 250, "오늘은 화염탄이 잘 나가.", body, WOOD)
    draw.line((552, 295, 899, 295), fill=COPPER, width=2)
    label(553, 317, "주문을 챙기고 초원으로", small, WOOD)
    label(39, 426, "버튼 상태", body, "#F0FCFF")
    states = (
        ("normal", "기본"), ("highlighted", "강조"),
        ("pressed", "눌림"), ("disabled", "비활성"),
    )
    for index, (state, title) in enumerate(states):
        x = 38 + index * 234
        place(sliced(sprites[f"button-{state}"], 68, 29), x, 460)
        color = "#E4AA84" if state == "disabled" else cream
        draw.text((x + 102, 502 + (2 if state == "pressed" else 0)), "전투 시작",
                  font=body, fill=color, anchor="mm")
        draw.text((x + 102, 572), title, font=small, fill=cream, anchor="mm")
    return image


def build():
    SPRITES.mkdir(parents=True, exist_ok=True)
    reference = PACK / "Reference"
    reference.mkdir(exist_ok=True)
    palette = set(json.loads((GAME / "palettes/project.json").read_text(encoding="utf-8")))
    allowed = {ImageColor.getrgb(color) for color in palette}
    sprites = {name: frame(colors, corner_stones=name == "panel")
               for name, colors in FRAMES.items()}
    sprites["speaker-scroll"] = speaker_scroll()
    for width in (48, 84, 101):
        sliced(sprites["speaker-scroll"], width, 28)
    ornaments = {"dialogue-tail": dialogue_tail(), "spell-clasp": spell_clasp(),
                 "panel-crest": panel_crest()}
    atlas = Image.new("RGBA", (TILE * 12, TILE * 9))
    mapping = {}
    for index, (name, sprite) in enumerate(sprites.items()):
        assert sprite.size == (TILE * 3, TILE * 3)
        col, row = (0, 6) if name == "speaker-scroll" else (index % 4 * 3, index // 4 * 3)
        atlas.paste(sprite, (col * TILE, row * TILE))
        mapping[name] = {"col": col, "row": row, "columns": 3, "rows": 3}
        save_sprite(name, sprite, TILE)
    for name, col, row in (("dialogue-tail", 9, 3), ("spell-clasp", 11, 3), ("panel-crest", 9, 4)):
        sprite = ornaments[name]
        atlas.paste(sprite, (col * TILE, row * TILE))
        save_sprite(name, sprite, 0)
        mapping[name] = {"col": col, "row": row, "columns": sprite.width // TILE, "rows": 1}
    for name, sprite in {**sprites, **ornaments}.items():
        pixels = sprite.get_flattened_data()
        assert {pixel[3] for pixel in pixels} == {0, 255}, name
        assert {pixel[:3] for pixel in pixels if pixel[3]} <= allowed, name
        cell = mapping[name]
        x, y = cell["col"] * TILE, cell["row"] * TILE
        assert atlas.crop((x, y, x + sprite.width, y + sprite.height)).tobytes() == sprite.tobytes()
    atlas.save(reference / "ui-tiles-12px.png", optimize=True)
    (reference / "ui-tiles-12px.json").write_text(
        json.dumps({"tileSize": TILE, "origin": "top-left", "sprites": mapping}, indent=2) + "\n",
        encoding="utf-8",
    )
    preview(sprites, ornaments).save(HERE / "spells-to-go-ui-preview.png", optimize=True)
    archive = HERE / "spells-to-go-unity-ui.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as output:
        paths = [SPRITES / f"{name}.png" for name in mapping]
        paths += [path.with_suffix(".png.meta") for path in paths]
        paths += [reference / f"ui-tiles-12px.{ext}" for ext in ("png", "json")]
        for path in sorted(paths):
            output.write(path, path.relative_to(PACK).as_posix())
        for name in ("README.md", "spells-to-go-ui-preview.png"):
            output.write(HERE / name, name)
    with ZipFile(archive) as output:
        assert output.testzip() is None


if __name__ == "__main__":
    build()
