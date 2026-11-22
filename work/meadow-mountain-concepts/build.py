from pathlib import Path
from math import sin, tau
import argparse
import json
import os
import random
from runpy import run_path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ORIGINAL = HERE.parents[1] / "exports/v1/meadow-tilemap/tilemap"
STAGE_EXPORT = ORIGINAL.parent / "stages"
STAGE_NAMES = {"flower": "들꽃 언덕", "jade": "솔바람 고개", "sunset": "노을마루"}
H = 352
STYLES = {
    "flower": dict(sky="#b5dfd8", cloud="#e7f2da", light="#fff4d2",
        mountains=("#a3c9bc", "#7ab0a4", "#598d83", "#8fbbaa"), hills=("#80aa85", "#638e70"),
        grass=("#8ab67b", "#7ba56c", "#5c885e", "#a6c48a"),
        path=("#d9b183", "#edcea0", "#a67f61", "#c49b74"), flower=("#fff1c8", "#e5a0aa")),
    "jade": dict(sky="#bedce1", cloud="#dfeef0", light="#f8f2dc",
        mountains=("#91b9c5", "#668f9c", "#4c7283", "#a8c9d0"), hills=("#658e8b", "#487572"),
        grass=("#709b83", "#648973", "#486d63", "#8eb39a"),
        path=("#b0aea1", "#d0c9b3", "#6f807a", "#929487"), flower=("#c8d7cc", "#e4d8aa")),
    "sunset": dict(sky="#e5b5a9", cloud="#f5d0ae", light="#ffe9ae",
        mountains=("#c5a0a7", "#a67e91", "#82697f", "#eab39c"), hills=("#a09575", "#817e67"),
        grass=("#a6a477", "#938e65", "#716f58", "#bfba83"),
        path=("#d4a47e", "#efc299", "#96735d", "#b78b71"), flower=("#fbe0a0", "#e8a887")),
}
PROFILES = {
    "flower": ([(0,104),(21,82),(39,88),(61,57),(75,53),(86,62),(104,84),(123,87),(144,107),(160,104)],
               [(0,121),(22,108),(44,96),(60,101),(83,115),(112,104),(135,95),(160,121)]),
    "jade": ([(0,107),(19,84),(33,91),(53,66),(67,77),(87,48),(97,44),(121,78),(143,88),(160,107)],
             [(0,117),(23,111),(44,101),(63,119),(85,94),(102,89),(125,109),(160,117)]),
    "sunset": ([(0,105),(18,90),(38,82),(54,86),(75,70),(95,73),(112,87),(135,88),(160,105)],
               [(0,115),(28,112),(51,103),(70,107),(92,111),(115,101),(141,107),(160,115)]),
}

def canvas(width):
    return Image.new("RGBA", (width, H))

def wrapped(draw, width, x, y, points, color):
    for shift in (-width, 0, width):
        draw.polygon([(x + dx + shift, y + dy) for dx, dy in points], fill=color)

def mountain_layer(name, style, stage=False):
    far = canvas(160)
    draw = ImageDraw.Draw(far)
    pale, ridge, shade, highlight = style["mountains"]
    draw.rectangle((0, 0, 159, 155), fill=style["sky"])
    if name == "sunset":
        if stage:
            draw.rectangle((0,48,159,74),fill="#bd9da7")
            draw.rectangle((0,75,159,99),fill="#e1bc9f")
            draw.ellipse((13, 45, 42, 74), fill=style["light"])
            for y, left, right in [(61,1,27),(66,22,51),(72,7,34)]:
                draw.rectangle((left,y,right,y+1),fill="#bd9da7")
        else:
            draw.ellipse((112, 47, 137, 72), fill=style["light"])
    cloud = [(-20, 2),(-17,0),(-11,0),(-8,-4),(-2,-5),(2,-10),(8,-11),(13,-7),(15,-3),(23,-2),(25,1),(19,3),(-15,3)]
    clouds = [(7,31),(139,40),(28,63)]
    if stage:
        clouds = {"flower": [(9,29),(116,43),(43,57)],
                  "jade": [(131,30),(36,48)],
                  "sunset": [(70,34),(145,53)]}[name]
    for x, y in clouds:
        wrapped(draw, 160, x, y, cloud, style["cloud"])
        wrapped(draw, 160, x, y+6, [(-18,0),(-4,0),(-4,1),(-18,1)], style["cloud"])
    ridge_profile, near_profile = PROFILES[name]
    draw.polygon([(0,96),(32,72),(51,81),(73,55),(84,60),(109,72),(129,57),(160,96),(160,155),(0,155)], fill=pale)
    draw.polygon(ridge_profile+[(160,155),(0,155)], fill=ridge)
    peak = {"flower": (75,53), "jade": (97,44), "sunset": (75,70)}[name]
    x, y = peak
    shoulder = {"flower": (123, 87), "jade": (143, 88), "sunset": (135, 88)}[name]
    draw.polygon([(x,y), *[p for p in ridge_profile if x<p[0]<=shoulder[0]], (shoulder[0]+8,120), (x+10,111), (x+11,y+37), (x-1,y+23), (x+3,y+15)], fill=shade)
    draw.polygon([(x-13,y+5 if name=="flower" else y+13),(x,y),(x+10,y+8),(x+14,y+16),(x+5,y+12),(x+1,y+16),(x-4,y+10),(x-11,y+14)], fill=highlight)
    hills = canvas(160)
    draw = ImageDraw.Draw(hills)
    draw.polygon(near_profile+[(160,155),(0,155)], fill=style["hills"][0])
    if stage and name == "flower":
        draw.polygon([(0,124),(17,116),(30,113),(47,115),(68,126),(90,126),
                      (111,117),(126,115),(144,117),(160,124),(160,155),(0,155)],
                     fill=style["hill_light"])
    draw.polygon([(0,136),(23,130),(40,119),(57,120),(84,130),(109,121),(131,122),(160,136),(160,155),(0,155)], fill=style["hills"][1])
    rng = random.Random(27)
    for x in range(4,158,4):
        y = round(138 + 4*sin(x*tau/160)) + rng.randrange(-2,3)
        height = rng.randrange(3,9)
        draw.polygon([(x-2,y),(x,y-height),(x+2,y)], fill=style["hills"][1])
    if stage and name == "jade":
        for x,y,height in [(4,143,12),(13,140,17),(21,143,11),(94,139,12),
                           (102,139,19),(111,141,13),(149,145,13),(157,143,17)]:
            points = [(0,-height),(3,-height+6),(2,-height+6),(5,-3),
                      (3,-3),(6,0),(1,0),(1,3),(-1,3),(-1,0),(-6,0),
                      (-3,-3),(-5,-3),(-2,-height+6),(-3,-height+6)]
            wrapped(draw,160,x,y,points,style["hill_shade"])
    if stage and name == "sunset":
        for x,y,length in [(3,114,32),(59,121,23),(105,111,27),(146,119,22)]:
            wrapped(draw,160,x,y,[(0,0),(length,0),(length-5,1),(4,1)],style["hill_light"])
    return far,hills

def terrain(name, style):
    ground, road = canvas(320), canvas(320)
    g, p = ImageDraw.Draw(ground), ImageDraw.Draw(road)
    lawn, mids, dark, lime = style["grass"]
    dirt, light, rim, shade = style["path"]
    n = {"flower": 1, "jade": 2, "sunset": 3}[name]
    rng = random.Random(718 + n)
    def wave(x, amplitude, phase=0, frequency=2):
        return sin(x*tau*frequency/320 + phase)*amplitude
    def edges(x):
        bend = wave(x, 5, .4, 2) + wave(x, 3, 1, 3)
        if "road_width" in style:
            width = style["road_width"]
            center = 232 + bend * (0.8 if name == "jade" else 1)
            top = round(center-width/2)
            return top, top+width-1
        return round(214+bend+wave(x,2,1,5)), round(248+bend+wave(x,2,0,4))
    for x in range(320):
        y = round(151+wave(x,3,0,3)+wave(x,2,1,8))
        g.line((x,y,x,351), fill=lawn)
        g.line((x,y,x,y+3), fill=mids)
        lo, hi = edges(x)
        p.line((x,lo,x,hi), fill=rim)
        p.line((x,lo+3,x,hi-3), fill=shade)
        p.line((x,lo+5,x,hi-5), fill=dirt)
        p.point((x,lo+5), fill=light)
    tuft = [(-3,0),(-2,-2),(0,-1),(0,-4),(1,-4),(2,-2),(4,-3),(3,0)]
    for x in range(3,320,8):
        y = round(152+wave(x,3,0,3)+wave(x,2,1,8))
        height = rng.randrange(3,9)
        wrapped(g,320,x,y+3,[(-5,0),(-4,-3),(-2,-4),(-1,-height),(2,-height),(4,-3),(6,0)],dark)
        wrapped(g,320,x-1,y-1,[(-2,0),(-1,-2),(2,-2),(3,0)],mids)
    for _ in range(170):
        x, y = rng.randrange(320), rng.randrange(160,352)
        lo, hi = edges(x)
        if lo-1 <= y <= hi+3:
            continue
        color = rng.choice([mids,mids,lime])
        wrapped(g,320,x,y,tuft if rng.random()<.38 else [(0,0),(2,0),(3,1),(0,1)],color)
    for x in range(5,319,5):
        lo, hi = edges(x)
        y = rng.randrange(lo+8,hi-6)
        length = rng.randrange(1,6)
        if name == "jade" and x%3 != 0:
            wrapped(p,320,x,y,[(0,1),(1,-1),(length+2,-1),(length+3,1),(length+1,2),(1,2)],shade)
            wrapped(p,320,x,y,[(1,-1),(length+1,-1),(length+2,0),(1,0)],light)
        else:
            wrapped(p,320,x,y,[(0,0),(length,0),(length+1,1),(1,1)],rng.choice([shade,light]))
    for x in range(12,320,17):
        lo, hi = edges(x)
        y = rng.choice([lo-rng.randrange(6,23),hi+rng.randrange(7,32),rng.randrange(277,350)])
        if name == "jade" or (name == "sunset" and x%2==0):
            wrapped(g,320,x,y,[(-5,1),(-4,-2),(-1,-5),(3,-5),(5,-3),(6,1),(3,3),(-3,3)],dark)
            wrapped(g,320,x,y,[(-3,0),(-2,-3),(1,-5),(3,-4),(4,-2),(2,0)],mids)
            wrapped(g,320,x,y,[(-2,-3),(1,-4),(2,-3),(0,-2),(-2,-2)],lime)
        else:
            for dx, dy in [(0,0),(4,3),(-4,4)]:
                xx, yy = (x+dx)%320, y+dy
                wrapped(g,320,xx,yy,[(0,1),(1,1),(1,5),(0,5)],dark)
                wrapped(g,320,xx,yy,[(0,-2),(1,-2),(1,-1),(2,-1),(2,0),(1,0),(1,1),(0,1),(0,0),(-1,0),(-1,-1),(0,-1)],rng.choice(style["flower"]))
                g.point((xx,yy-1), fill=light if name=="flower" else shade)
    return ground,road

def tilemap(ground, road, output, stage=False):
    cells, indices = [], {}
    layers = []
    for index,(name,source) in enumerate((("풀밭",ground),("오솔길",road)),1):
        gids = []
        for y in range(0,H,16):
            for x in range(0,320,16):
                cell = source.crop((x,y,x+16,y+16))
                if cell.getbbox() is None:
                    gids.append(0)
                    continue
                key = cell.tobytes()
                if key not in indices:
                    indices[key] = len(cells) + 1
                    cells.append(cell)
                gids.append(indices[key])
        layers.append(dict(id=index,name=name,type="tilelayer",width=20,height=22,
                           x=0,y=0,visible=True,opacity=1,data=gids))
    columns = 16
    atlas = Image.new("RGBA",(columns*16,((len(cells)+columns-1)//columns)*16))
    for i, cell in enumerate(cells):
        atlas.paste(cell,((i%columns)*16,(i//columns)*16))
    atlas.save(output/"terrain-tiles.png")
    tmj = dict(type="map", orientation="orthogonal", renderorder="right-down",
        infinite=False, width=20, height=22, tilewidth=16, tileheight=16,
        nextlayerid=3,nextobjectid=1,version="1.10",layers=layers,
        tilesets=[dict(firstgid=1,name="terrain",image="terrain-tiles.png",
                       imagewidth=atlas.width,imageheight=atlas.height,margin=0,spacing=0,
                       tilewidth=16,tileheight=16,columns=columns,tilecount=len(cells))])
    (output/"terrain.tmj").write_text(json.dumps(tmj,indent=2), encoding="utf-8")
    for layer,source in zip(layers,(ground,road)):
        restored = canvas(320)
        for index,gid in enumerate(layer["data"]):
            if gid:
                i=gid-1
                u,v=(i%columns)*16,(i//columns)*16
                restored.paste(atlas.crop((u,v,u+16,v+16)),((index%20)*16,(index//20)*16))
        assert restored.tobytes()==source.tobytes()
    if stage:
        images = [
            dict(id=i,type="imagelayer",name=name,image=file,x=0,y=0,
                 opacity=1,visible=True,repeatx=True)
            for i,(name,file) in enumerate((("산 원경","stage-mountains-loop.png"),
                                            ("중간 언덕","stage-foothills-loop.png")),3)
        ]
        scene = dict(tmj,layers=images+layers,nextlayerid=5)
        (output/"stage-start.tmj").write_text(json.dumps(scene,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def stage_styles():
    battle = run_path(str(ORIGINAL.parents[1]/"meadow-wave-mobile/detailed/build.py"))
    for (key,original),(_,sky,rock,hill,ground),width in zip(
            STYLES.items(),battle["STAGES"],battle["ROAD_WIDTHS"]):
        base, mid, light, dirt, deep, accent = ground
        yield key, dict(original,sky=sky[0],cloud=sky[2],mountains=rock,
                        hills=hill[:2],hill_light=hill[2],hill_shade=hill[3],
                        grass=(base,mid,deep,light),path=(dirt,accent,deep,mid),
                        road_width=width)

def window(layer, x, width=160):
    repeated = canvas(layer.width*2)
    repeated.paste(layer,(0,0))
    repeated.paste(layer,(layer.width,0))
    x %= layer.width
    return repeated.crop((x,0,x+width,H))

def stage_foreground(template, number, name):
    image = template.copy()
    draw = ImageDraw.Draw(image)
    for y in range(45,56):
        draw.line((59,y,100,y),fill=template.getpixel((57,y)))
    for y in range(64,89):
        draw.line((0,y,159,y),fill=template.getpixel((0,y)))
    font = Path(os.environ["WINDIR"]) / "Fonts/malgunbd.ttf"
    draw.text((80,45),f"스테이지 {number}",font=ImageFont.truetype(str(font),8),
              fill="#ade9ff",anchor="mt")
    draw.text((80,65),name,font=ImageFont.truetype(str(font),17),
              fill="#f0fcff",anchor="mt",stroke_width=1,stroke_fill="#38454e")
    return image

def main(stage=False):
    template = Image.open(ORIGINAL/"stage-start-foreground.png").convert("RGBA")
    sheet = Image.open(ORIGINAL/"stage-slime-hop.png").convert("RGBA")
    slime = sheet.crop((0,0,32,32))
    board = Image.new("RGB",(1016,780),"#172527")
    label = ImageDraw.Draw(board)
    font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf",23)
    stages = []
    for i,(name,style) in enumerate(stage_styles() if stage else STYLES.items()):
        out = STAGE_EXPORT/f"stage-{i+1:02}" if stage else HERE/name
        out.mkdir(parents=True,exist_ok=True)
        mountains,hills = mountain_layer(name,style,stage)
        far = Image.alpha_composite(mountains,hills)
        grass,road = terrain(name,style)
        ground = Image.alpha_composite(grass,road)
        assert ground.getchannel("A").crop((0,156,320,H)).getextrema() == (255,255)
        for layer,file,size in [(far,"stage-far-loop.png",(160,H)),(ground,"stage-ground-loop.png",(320,H)),(road,"stage-path-strip.png",(320,H))]:
            assert layer.size==size and set(layer.getchannel("A").tobytes())=={0,255}
            layer.save(out/file)
        tilemap(grass,road,out,stage)
        if stage:
            mountains.save(out/"stage-mountains-loop.png")
            hills.save(out/"stage-foothills-loop.png")
        phase_px = 0 if stage and name == "sunset" else 40
        scene = Image.alpha_composite(window(far,phase_px),window(ground,phase_px*2))
        shadow = canvas(160)
        box = (68,230,84,233) if stage else (65,229,86,233)
        ImageDraw.Draw(shadow).ellipse(box,fill=(47,41,55,100))
        scene.alpha_composite(shadow)
        if stage:
            scene.alpha_composite(slime.resize((24,24),Image.Resampling.NEAREST),(64,211))
        else:
            scene.alpha_composite(slime,(60,204))
        foreground = stage_foreground(template,i+1,STAGE_NAMES[name]) if stage else template
        if stage:
            foreground.save(out/"stage-start-foreground.png")
            stages.append(dict(number=i+1,name=STAGE_NAMES[name],directory=out.name,
                               path_width_px=style["road_width"]))
        scene.alpha_composite(foreground)
        scene.save(out/"preview.png")
        x = 20+i*328
        board.paste(scene.resize((320,704),Image.Resampling.NEAREST),(x,55))
        caption = f"{i+1}   {STAGE_NAMES[name]}" if stage else ["A   꽃초원","B   청록 산길","C   노을 고개"][i]
        label.text((x,14),caption,font=font,fill="#f2ead7")
    if stage:
        manifest = dict(viewport_px=[160,352], tile_px=16, loop_ms=8640,
            layers=[
                dict(file="stage-far-loop.png", size_px=[160,352], scroll_left_px_per_second=160/8.64),
                dict(file="stage-ground-loop.png", size_px=[320,352], scroll_left_px_per_second=320/8.64),
                dict(file="stage-start-foreground.png", size_px=[160,352]),
            ],
            split_far_layers=["stage-mountains-loop.png","stage-foothills-loop.png"],
            path_overlay="stage-path-strip.png", tiled_map="terrain.tmj",scene_map="stage-start.tmj",
            slime_sheet="../tilemap/stage-slime-hop.png", slime_timing="../tilemap/stage-slime-hop.json",
            slime_feet_px=[76,232], slime_presentation_scale=0.75, stages=stages)
        (STAGE_EXPORT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    board.save((STAGE_EXPORT/"preview.png") if stage else (HERE/"comparison.png"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stages",action="store_true")
    main(parser.parse_args().stages)

