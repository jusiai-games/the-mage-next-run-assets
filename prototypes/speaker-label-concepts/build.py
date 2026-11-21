"""Compare speaker treatments in the current Spells to Go dialogue UI."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
GAME = HERE.parents[1]
KIT = GAME / "exports/spells-to-go-ui"
spec = spec_from_file_location("ui_kit", KIT / "build.py")
kit = module_from_spec(spec)
spec.loader.exec_module(kit)
INK, WOOD, BRONZE = kit.INK, kit.WOOD, kit.BRONZE
COPPER, PARCHMENT, LICHEN = kit.COPPER, kit.PARCHMENT, kit.LICHEN
ASSETS = KIT / "package/Assets/SpellsToGo/UI/Sprites"
FONTS = Path("C:/Windows/Fonts")
NAME = "초원 마법 상인"
SCALE = 3


def sprite(name):
    with Image.open(ASSETS / f"{name}.png") as image:
        return image.convert("RGBA")


def text(image, position, value, size, color, *, bold=False, anchor="lt"):
    font = ImageFont.truetype(str(FONTS / ("malgunbd.ttf" if bold else "malgun.ttf")), size)
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1"
    draw.text(position, value, font=font, anchor=anchor, fill=color)


def speaker(image, style):
    draw = ImageDraw.Draw(image)
    if style == "scroll":
        image.alpha_composite(kit.sliced(sprite("speaker-scroll"), 101, 28), (10, 9))
        text(image, (60, 18), NAME, 11, WOOD, bold=True, anchor="mt")
    elif style == "sealed":
        draw.polygon([(15, 16), (64, 15), (107, 16), (112, 20), (110, 24),
                      (112, 28), (109, 34), (101, 35), (101, 37), (95, 35),
                      (88, 36), (85, 35), (14, 36), (11, 31), (13, 27),
                      (11, 24), (14, 21)], fill=BRONZE)
        draw.polygon([(16, 17), (66, 16), (105, 17), (110, 21), (108, 24),
                      (110, 27), (107, 32), (98, 33), (96, 35), (89, 33),
                      (15, 34), (13, 31), (15, 27), (13, 24)], fill=PARCHMENT)
        draw.line([(15, 20), (17, 23), (15, 26), (17, 29)], fill=COPPER)
        draw.line([(97, 17), (104, 24), (104, 30)], fill=COPPER)
        draw.polygon([(101, 23), (106, 23), (109, 26), (109, 31), (105, 34),
                      (101, 33), (98, 30), (98, 26)], fill="#6A4757")
        draw.line([(101, 25), (104, 24), (107, 26)], fill="#D88475")
        draw.line((103, 26, 103, 31), fill=PARCHMENT)
        draw.line((101, 28, 105, 28), fill=PARCHMENT)
        text(image, (20, 20), NAME, 11, WOOD, bold=True)
    elif style == "carved":
        for x in (21, 100):
            draw.line((x, 6, x, 17), fill=INK)
            draw.line((x + 1, 8, x + 1, 15), fill=BRONZE)
        draw.polygon([(12, 16), (17, 12), (101, 12), (108, 16),
                      (108, 29), (103, 33), (17, 33), (12, 29)], fill=INK)
        draw.polygon([(14, 17), (18, 14), (101, 14), (106, 17),
                      (106, 28), (102, 31), (18, 31), (14, 28)], fill=WOOD)
        draw.line([(22, 15), (30, 15), (33, 16), (46, 16)], fill=BRONZE)
        draw.line([(76, 29), (84, 29), (86, 28), (95, 28)], fill=BRONZE)
        for x in (17, 103):
            draw.polygon([(x, 16), (x + 2, 18), (x, 20), (x - 2, 18)], fill=kit.STONE)
            draw.point((x, 17), fill=LICHEN)
        text(image, (23, 18), NAME, 11, PARCHMENT, bold=True)
    elif style == "potion":
        draw.line([(15, 8), (30, 8), (33, 6), (81, 6), (86, 8), (111, 8)], fill=INK, width=2)
        draw.line([(17, 8), (30, 8), (34, 6), (80, 6), (86, 8), (108, 8)], fill=BRONZE)
        draw.polygon([(13, 8), (19, 4), (23, 5), (20, 9)], fill="#86A866")
        draw.polygon([(96, 8), (99, 3), (104, 3), (102, 7)], fill="#86A866")
        draw.line((37, 8, 37, 16), fill=BRONZE)
        draw.line((102, 9, 102, 16), fill=BRONZE)
        draw.polygon([(28, 14), (109, 14), (114, 18), (112, 28),
                      (106, 32), (35, 32), (28, 28)], fill=INK)
        draw.polygon([(29, 16), (108, 16), (112, 19), (110, 27),
                      (105, 30), (35, 30), (29, 27)], fill=WOOD)
        draw.line((32, 16, 108, 16), fill=BRONZE)
        draw.line((19, 8, 19, 15), fill=BRONZE)
        draw.polygon([(16, 12), (22, 12), (22, 17), (25, 20), (25, 28),
                      (22, 31), (16, 31), (13, 28), (13, 21), (16, 17)], fill=INK)
        draw.rectangle((17, 13, 21, 15), fill=COPPER)
        draw.polygon([(17, 17), (21, 17), (23, 21), (23, 27), (21, 29),
                      (17, 29), (15, 27), (15, 21)], fill="#505276")
        draw.polygon([(16, 23), (18, 22), (23, 23), (23, 27), (21, 29),
                      (17, 29), (15, 27)], fill="#78CBF4")
        draw.point((17, 24), fill="#F0FCFF")
        text(image, (34, 19), NAME, 11, PARCHMENT, bold=True)


def sample(backdrop, style, dialogue, action):
    image = backdrop.copy()
    image.alpha_composite(dialogue, (5, 15))
    speaker(image, style)
    text(image, (16, 42), "다음 길에 쓸 주문을 골라 봐.", 10, WOOD)
    image.alpha_composite(action, (89, 64))
    text(image, (122, 73), "주문 고르기", 9, PARCHMENT, bold=True, anchor="mt")
    return image.resize((160 * SCALE, 96 * SCALE), kit.NEAREST)


def build():
    meadow = GAME / "prototypes/meadow-visual/assets/title-meadow.png"
    with Image.open(meadow) as source:
        crop = source.convert("RGBA").crop((64, 33, 224, 129))
    backdrop = Image.blend(crop, Image.new("RGBA", crop.size, INK), 0.42)
    dialogue = kit.sliced(sprite("dialogue"), 150, 44)
    action = kit.sliced(sprite("button-highlighted"), 66, 25)
    sheet = Image.new("RGB", (1040, 746), INK)
    text(sheet, (27, 22), "대화창 이름표 시안", 29, PARCHMENT, bold=True)
    text(sheet, (28, 59), "초원 마법 상인 · 주문 넣고 갑니다", 16, LICHEN)
    options = (
        ("scroll", "A1  말린 양피지 · 선택"),
        ("sealed", "A2  봉인 찍은 양피지"),
        ("carved", "B1  조약돌 못 현판"),
        ("potion", "B2  물약을 매단 현판"),
    )
    for index, (key, label) in enumerate(options):
        x = 27 + (index % 2) * 506
        y = 91 + (index // 2) * 320
        text(sheet, (x, y), label, 20, PARCHMENT, bold=True)
        sheet.paste(sample(backdrop, key, dialogue, action), (x, y + 26))
    sheet.save(HERE / "speaker-label-concepts.png", optimize=True)


if __name__ == "__main__":
    build()
