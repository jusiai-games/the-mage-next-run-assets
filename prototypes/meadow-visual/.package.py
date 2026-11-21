from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

root = Path(__file__).resolve().parent
assets = root / "assets"
font_root = Path(os.environ["WINDIR"]) / "Fonts"
heading = ImageFont.truetype(str(font_root / "georgiab.ttf"), 42)
label = ImageFont.truetype(str(font_root / "malgunbd.ttf"), 18)
body = ImageFont.truetype(str(font_root / "malgun.ttf"), 17)
screens = [
    ("title", "타이틀"), ("intro", "전투 시작"), ("battle", "웨이브 1 전투"),
    ("reward", "주문 보상"), ("equip", "카드 장착"), ("later", "웨이브 2–5 전투"),
    ("trace", "별 그리기"), ("retreat", "실드 붕괴 · 강화"), ("retry", "재도전"),
    ("clear", "스테이지 클리어"), ("road", "다음 지역 선택"),
]
sheet = Image.new("RGB", (1440, 1580), "#191626")
draw = ImageDraw.Draw(sheet)
draw.text((40, 32), "The Mage Next Run", font=heading, fill="#FFE2A8")
draw.text((42, 89), "스테이지 1 · 초원 / 전체 화면", font=body, fill="#D9CEDF")
for i, (scene, name) in enumerate(screens):
    x, y = 40 + (i % 3) * 461, 134 + (i // 3) * 352
    draw.rectangle((x, y, x + 438, y + 328), fill="#211A2E", outline="#56465F")
    draw.text((x + 14, y + 10), f"{i + 1:02}  {name}", font=label, fill="#EFDFC7")
    with Image.open(root / ".qa" / f"{scene}.png") as shot:
        thumb = ImageOps.contain(shot.convert("RGB"), (420, 276), Image.Resampling.LANCZOS)
    sheet.paste(thumb, (x + (438 - thumb.width) // 2, y + 43 + (276 - thumb.height) // 2))
overview = root / "mage-next-run-screens.png"
sheet.save(overview, optimize=True)

excluded = {"distant-meadow.png", "spell-panel.png", "spell-slots.png"}
archive = root / "mage-next-run-meadow-pack.zip"
with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=9) as output:
    for path in (root / "README.md", root / "mage-next-run-visual.html", root / "ui_art.py", overview):
        output.write(path, path.name)
    for path in sorted(assets.rglob("*")):
        if path.is_file() and path.name not in excluded:
            output.write(path, path.relative_to(root).as_posix())
with ZipFile(archive) as output:
    assert output.testzip() is None
    print(f"{len(output.namelist())} files; {archive.stat().st_size:,} bytes")

