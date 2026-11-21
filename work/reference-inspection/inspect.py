from collections import Counter, defaultdict
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import json

from PIL import Image, ImageDraw, ImageFont, ImageOps

work = Path(__file__).resolve().parent
groups = defaultdict(list)
with ZipFile(Path.home() / "Downloads/REFERENCE.zip") as archive:
    assert not archive.testzip()
    names = [PurePosixPath(i.filename) for i in archive.infolist() if not i.is_dir()]
    print(Counter(p.suffix.lower() for p in names))
    for p in names:
        parts = p.parts[1:]
        if p.suffix.lower() != ".png":
            print(p)
            if p.name.lower() in {"license.txt", "readme.txt"}:
                print(archive.read(str(p)).decode("utf-8-sig", errors="replace"))
            if p.name == "asset_map.json":
                data = json.loads(archive.read(str(p)))
                print(json.dumps(data)[:800])
            continue
        if parts[0].startswith("Questwood"):
            if parts[1] in ("PNG_1x", "PNG_2x", "PNG_4x"):
                if parts[1] != "PNG_1x":
                    base = PurePosixPath(*p.parts[:2], "PNG_1x", *p.parts[3:])
                    with Image.open(BytesIO(archive.read(str(base)))) as image, Image.open(BytesIO(archive.read(str(p)))) as scaled:
                        expected = image.convert("RGBA").resize(scaled.size, Image.Resampling.NEAREST)
                        if expected.tobytes() != scaled.convert("RGBA").tobytes() or scaled.width != image.width * int(parts[1][4]):
                            groups["scale-differences"].append(p)
                    continue
                section = "questwood-" + parts[2].lower()
            else:
                section = "questwood-atlases"
        elif parts[0].startswith("Foozle"):
            section = "magic"
        elif parts[0] == "color-tone-blog":
            section = "color-tone"
        elif "card" in parts[0].lower():
            section = "cards"
        else:
            section = "other"
        groups[section].append(p)
    font = ImageFont.truetype("consola.ttf", 13)
    for group, paths in groups.items():
        print(group, len(paths))
        large = group in {"questwood-atlases", "other", "color-tone"}
        cell_w = 350 if large else 160
        cell_h = 228 if large else 114
        cols = 4 if large else 7
        per_page = cols * (4 if large else 8)
        for start in range(0, len(paths), per_page):
            subset = paths[start:start+per_page]
            board = Image.new("RGB", (cell_w*cols, cell_h*((len(subset)+cols-1)//cols)), "#303241")
            draw = ImageDraw.Draw(board)
            for i, p in enumerate(subset):
                x, y = (i % cols) * cell_w, (i // cols) * cell_h
                with Image.open(BytesIO(archive.read(str(p)))) as file:
                    pic = file.convert("RGBA")
                if pic.getbbox():
                    pic = pic.crop(pic.getbbox())
                factor = min((cell_w-14)/pic.width, (cell_h-29)/pic.height)
                pic = pic.resize((max(1,int(pic.width*factor)), max(1,int(pic.height*factor))), Image.Resampling.NEAREST)
                draw.rectangle((x+3,y+3,x+cell_w-4,y+cell_h-25), fill="#53596e")
                board.paste(pic,(x+(cell_w-pic.width)//2,y+3+(cell_h-27-pic.height)//2),pic)
                label = p.name
                if group == "magic" and p.stem.isdigit():
                    label = f"{p.parent.name} {p.stem}"
                draw.text((x+5,y+cell_h-22),label[:(cell_w-8)//7],font=font,fill="white")
            board.save(work / f"{group}-{start//per_page+1}.png")

