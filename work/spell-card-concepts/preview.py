from pathlib import Path
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps

game = Path(__file__).resolve().parents[2]
prototype = game / "prototypes/meadow-visual"
out = game / "prototypes/spell-card-concepts"
out.mkdir(parents=True, exist_ok=True)
fonts = Path(os.environ["WINDIR"]) / "Fonts"
NEAREST = Image.Resampling.NEAREST

W, H, SCALE = 44, 64, 3
INK = "#181726"
PAPER = "#E9CDA3"

spells = (
    ("fire", "화염탄", "강화 · 피해 증가", "#552B30", "#AE6237", "#F2AD63"),
    ("lightning", "연쇄 번개", "신규 · 두 마리 타격", "#203D59", "#477C9D", "#AFEBFF"),
    ("burst", "마력 폭발", "신규 · 별 그리기", "#3F2D58", "#70558D", "#E7BDFF"),
)
variants = (
    ("A", "마법서", "양피지 · 삽화와 주문 설명", "주문 효과를 읽고 비교하기 좋은 구성"),
    ("B", "봉인", "짙은 카드지 · 룬 원과 주문 문양", "손패가 작아도 주문 문양을 먼저 찾는 구성"),
    ("C", "원소", "큰 삽화 · 원소마다 다른 색 띠", "색과 삽화로 불·번개·마력을 구분하는 구성"),
)


def font(size, bold=False):
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    return ImageFont.truetype(str(fonts / name), size)


def clipped(draw, x, y, right, bottom, fill, notch=2):
    draw.polygon(
        ((x+notch,y),(right-notch,y),(right,y+notch),(right,bottom-notch),
         (right-notch,bottom),(x+notch,bottom),(x,bottom-notch),(x,y+notch)), fill=fill
    )


def center_text(draw, center, y, text, size, ink, bold=False):
    draw.text((center, y), text, font=font(size, bold), fill=ink, anchor="mt")


def paint_icon(card, key, size, y, *, stamp=None):
    with Image.open(prototype / f"assets/icon-{key}.png") as file:
        art = file.convert("RGBA")
    if stamp:
        mask = art.getchannel("A")
        tonal = ImageOps.grayscale(art).point(lambda value: 255 if value > 155 else 0)
        ink = Image.new("RGBA", art.size, stamp[0])
        ink.paste(stamp[1], (0, 0, 24, 24), tonal)
        ink.putalpha(mask)
        art = ink
    art = ImageOps.contain(art.crop(art.getbbox()), (size, size), NEAREST)
    card.alpha_composite(art, ((W-art.width)//2, y+(size-art.height)//2))


def arcane_sparks(draw, index, count, area, colors):
    rng = random.Random(index)
    x0, y0, x1, y1 = area
    for _ in range(count):
        x, y = rng.randint(x0,x1), rng.randint(y0,y1)
        color = rng.choice(colors)
        draw.point((x,y), fill=color)
        if rng.random() < .22 and x < x1:
            draw.point((x+1,y), fill=color)


def face(variant, index):
    key, name, detail, dark, color, light = spells[index]
    card = Image.new("RGBA",(W,H))
    draw = ImageDraw.Draw(card)
    clipped(draw,0,0,43,63,INK,3)
    if variant == "A":
        clipped(draw,1,1,42,62,"#8B6755")
        clipped(draw,3,3,40,60,PAPER)
        draw.rectangle((5,5,38,38), fill="#9E8069", outline="#5B4647")
        draw.rectangle((6,6,37,37), fill="#BC9C7A")
        draw.rectangle((8,8,35,34), outline="#D4B894")
        draw.line((8,34,35,34), fill="#8B6755")
        for offset in (0, 3, 6):
            draw.line((8+offset,32,16+offset,25), fill="#B08D70")
            draw.line((28+offset//3,17,33+offset//3,12), fill="#D4B894")
        draw.rectangle((4,39,39,48), fill="#634848")
        draw.line((5,49,38,49), fill="#9A765F")
        draw.line((13,59,30,59), fill="#B19277")
        paint_icon(card,key,26,8,stamp=(dark,color))
        label, sub, title_y, details_y = "#F8DBB6", "#463342", 42, 52
    elif variant == "B":
        clipped(draw,1,1,42,62,"#836A59")
        clipped(draw,2,2,41,61,"#25233D")
        draw.rectangle((4,4,39,59), outline="#605470")
        draw.rectangle((6,6,37,57), outline="#383347")
        draw.ellipse((6,9,37,39), outline=color, fill=dark)
        draw.ellipse((8,11,35,37), outline="#957264")
        draw.line((22,7,22,41), fill="#65526E")
        draw.line((4,24,39,24), fill="#65526E")
        for x,y in ((22,7),(37,24),(22,40),(6,24)):
            draw.polygon(((x,y-2),(x+2,y),(x,y+2),(x-2,y)), fill=light)
        arcane_sparks(draw,index+22,16,(9,13,34,34),(color,light))
        paint_icon(card,key,26,11)
        draw.rectangle((5,43,38,50), fill="#312941")
        draw.line((8,52,35,52), fill="#6E5C72")
        label, sub, title_y, details_y = light, "#D5C4D5", 44, 54
    else:
        clipped(draw,1,1,42,62,"#A27A60")
        clipped(draw,2,2,41,61,"#EDCBA3")
        draw.rectangle((4,4,39,44), fill=dark)
        draw.rectangle((5,8,38,36), fill=color)
        draw.polygon(((5,29),(11,23),(14,26),(22,18),(27,25),(33,22),(38,26),(38,43),(5,43)), fill=dark)
        draw.polygon(((5,34),(15,28),(18,33),(31,27),(38,31),(38,42),(5,42)), fill=color)
        draw.polygon(((5,42),(16,32),(23,38),(29,33),(38,37),(38,44),(5,44)), fill=dark)
        arcane_sparks(draw,index+124,28,(5,6,38,37),(dark,color,light))
        paint_icon(card,key,29,9)
        draw.rectangle((3,42,40,51), fill=dark)
        draw.line((5,42,38,42), fill=light)
        draw.rectangle((5,52,38,59), fill="#E6C9A6")
        label, sub, title_y, details_y = "#FAF5EB", "#493747", 45, 54

    card = card.resize((W*SCALE,H*SCALE), NEAREST)
    draw = ImageDraw.Draw(card)
    center_text(draw,W*SCALE//2,title_y*SCALE,name,17,label,True)
    center_text(draw,W*SCALE//2,details_y*SCALE,detail,10,sub)
    return card


def spread(board, x, y, variant):
    for i, offset, lift in ((0,0,14),(2,226,14),(1,113,0)):
        card = face(variant,i)
        if i != 1:
            card = card.rotate(5 if i == 0 else -5, expand=True, resample=NEAREST)
        shadow = Image.new("RGBA",card.size,"#0C0D19")
        shadow.putalpha(card.getchannel("A").point(lambda value: (value*2)//3))
        board.alpha_composite(shadow,(x+offset+2,y+lift+7))
        board.alpha_composite(card,(x+offset,y+lift))


board = Image.new("RGBA",(1312,742),"#1A1A28")
draw = ImageDraw.Draw(board)
draw.text((34,24),"주문 장착 · 손패 카드 시안",font=font(31,True),fill="#F8E0BB")
draw.text((36,69),"화염탄, 연쇄 번개, 마력 폭발을 같은 크기로 비교",font=font(16),fill="#C2BACB")
with Image.open(prototype / ".qa/equip.png") as shot:
    # Keep only the current screen's top and its original three equipment slots.
    crop = shot.crop((280, 18, 835, 276)).convert("RGBA")
    crop.thumbnail((396,168), Image.Resampling.LANCZOS)
draw.rounded_rectangle((34,110,1277,304),radius=7,fill="#232335",outline="#443D50")
board.alpha_composite(crop,(894,122))
draw.text((58,150),"장착 슬롯 3개",font=font(22,True),fill="#F5DFC4")
draw.text((58,189),"현재 배치 기준",font=font(15),fill="#C2BACB")
draw.line((58,227,832,227),fill="#443D50")
draw.text((58,241),"손패에서 가운데 카드가 들리고, 양옆 카드가 살짝 포개집니다.",font=font(17),fill="#D6CCD9")
for idx,(key,title,tag,note) in enumerate(variants):
    x = 34 + idx*422
    draw.rounded_rectangle((x,329,x+399,695),radius=7,fill="#222335",outline="#443C51")
    draw.rectangle((x+21,351,x+52,380),fill="#3B3044")
    center_text(draw,x+37,357,key,14,"#F4D5AC",True)
    draw.text((x+65,345),title,font=font(26,True),fill="#F8E0BB")
    draw.text((x+22,393),tag,font=font(15),fill="#C4BCCF")
    spread(board,x+14,426,key)
    draw.text((x+22,658),note,font=font(14),fill="#D7CAD6")
board.convert("RGB").save(out/"spell-card-directions.png", optimize=True)
print(out/"spell-card-directions.png")

