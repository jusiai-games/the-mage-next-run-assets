from pathlib import Path
from random import Random
from math import sin
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
W = 160
STAGES = [
    ("들꽃 언덕", ("#859eaa","#a1b8b8","#d0d1b8"), ("#a4ada7","#7e9497","#596e7e","#a1aaa0"),
     ("#7b9277","#687f72","#a0a784","#536961"), ("#829370","#708367","#9fa780","#b39b77","#5e6c63","#dbc09d")),
    ("솔바람 고개", ("#7e95ac","#9aafc2","#c5cbc7"), ("#98a7b3","#748a9e","#526581","#a1afbd"),
     ("#738e87","#58776e","#98a79a","#425e62"), ("#718f83","#607e75","#94a99a","#9d9a91","#506871","#ccc0a7")),
    ("노을마루", ("#93869f","#bd9da7","#e1bc9f"), ("#ac99a7","#86748c","#62546d","#c5a1a1"),
     ("#a1977f","#817a6e","#b3a08c","#665d66"), ("#9a8e73","#857a69","#b1a083","#bf9b7c","#6a5f67","#e2bc98")),
]
CLUSTER_SHADOWS = ("#65796a", "#526f6a", "#776c67")
RIDGES = [
    [(0,48),(15,43),(29,31),(37,28),(46,31),(58,41),(70,42),(86,36),(94,34),(110,45),(129,43),(146,35),(159,40)],
    [(0,48),(15,40),(25,35),(36,43),(55,37),(70,24),(79,18),(86,23),(98,39),(113,37),(129,29),(138,25),(150,36),(159,38)],
    [(0,44),(17,43),(34,36),(48,36),(64,41),(79,36),(98,29),(112,30),(132,35),(144,40),(159,41)],
]
ROAD_WIDTHS = (24, 20, 22)
SLIME_FEET = (129, 153)
SLIME_SCALE = 0.75

def poly(draw, points, fill):
    draw.polygon(points,fill=fill)

def ridge(draw, points, bottom, fill):
    poly(draw, points+[(159,bottom),(0,bottom)],fill)

def mountain(stage, sky, rock):
    image = Image.new("RGBA",(W,80))
    d = ImageDraw.Draw(image)
    for y in range(80):
        d.line((0,y,159,y),fill=sky[0 if y<19 else 1 if y<39 else 2])
    if stage == 2:
        d.ellipse((21,18,36,33),fill="#f1d5ab")
    for x,y in [(5,15),(39,21),(109,12),(147,19)]:
        poly(d,[(x-15,y),(x-9,y-1),(x-5,y-4),(x+1,y-4),(x+5,y-7),
                (x+11,y-6),(x+14,y-3),(x+21,y-1),(x+20,y),(x+4,y+1)],sky[2])
    ridge(d,[(0,40),(17,33),(31,40),(51,31),(65,35),(84,31),(102,32),
             (124,23),(136,29),(151,28),(159,35)],79,rock[0])
    profile = RIDGES[stage]
    ridge(d,profile,79,rock[1])
    for i,(x,y) in enumerate(profile[1:-2],1):
        previous = profile[i-1]
        following = profile[i+1]
        if y > previous[1] or y >= following[1]:
            continue
        width = min(12,following[0]-x)
        poly(d,[(x,y),(x+width,y+5),(x+width+6,y+14),(x+width+5,y+20),
                (x+5,y+17),(x+6,y+12),(x,y+9),(x+2,y+5)],rock[2])
        poly(d,[(x-7,y+5),(x,y),(x+4,y+3),(x+1,y+3),(x+2,y+6),
                (x-2,y+5),(x-6,y+9)],rock[3])
        d.line((x+7,y+17,x+15,y+24),fill=rock[2])
    for x,y,length in [(4,53,29),(41,49,20),(77,51,33),(127,47,27),(115,55,15)]:
        poly(d,[(x,y),(x+length,y),(x+length-4,y+1),(x+4,y+1)],rock[0])
    return image

def hills(stage, colors):
    image = Image.new("RGBA",(W,32))
    d = ImageDraw.Draw(image)
    a,b,c,shade = colors
    ridge(d,[(0,11),(13,6),(26,5),(40,10),(56,13),(72,9),(82,6),
             (99,5),(116,10),(132,13),(144,8),(159,8)],31,c)
    ridge(d,[(0,17),(19,15),(39,17),(53,14),(67,12),(80,13),(101,18),
             (113,18),(135,13),(150,11),(159,12)],31,a)
    ridge(d,[(0,23),(20,21),(34,23),(48,25),(64,22),(92,20),
             (109,21),(125,25),(145,23),(159,20)],31,b)
    poly(d,[(0,25),(19,24),(31,26),(44,27),(54,26),(62,27),(76,25),
            (94,23),(104,25),(111,26),(124,29),(137,28),(149,25),(159,24),
            (159,31),(0,31)],CLUSTER_SHADOWS[stage])
    for x,y in [(8,20),(13,19),(32,23),(49,23),(61,22),(76,20),(91,19),
                (111,22),(126,24),(140,22),(151,20)]:
        for dx,h in [(-2,3),(0,6),(3,4)]:
            if stage == 1:
                poly(d,[(x+dx,y-h),(x+dx-2,y-1),(x+dx+2,y-1)],shade)
                d.point((x+dx,y),fill=shade)
            else:
                poly(d,[(x+dx-2,y),(x+dx-1,y-h//2),(x+dx+1,y-h//2),
                        (x+dx+3,y)],shade)
    for x,y in [(16,10),(30,11),(56,17),(90,11),(100,13),(135,17),(149,8)]:
        d.line((x,y,x+6,y),fill=a)
    if stage == 0:
        d.line([(123,19),(117,23),(111,24),(107,27),(99,28)],fill=c)
    elif stage == 1:
        for x,y,h in [(19,25,9),(23,25,12),(26,26,8),(104,24,13),(109,26,10),(113,26,7)]:
            for offset in (0,3,5):
                poly(d,[(x,y-h+offset),(x-2-offset//2,y-h+offset+4),
                        (x+2+offset//2,y-h+offset+4)],shade)
            d.line((x,y-2,x,y),fill=shade)
    else:
        d.line([(66,25),(72,24),(79,24),(86,26),(93,26)],fill=c)
        d.line((95,28,112,28),fill=a)
    return image

def terrain(stage, colors):
    base, shadow, highlight, dirt, deep, sparkle = colors
    image = Image.new("RGBA",(W,144),base)
    d = ImageDraw.Draw(image)
    rng = Random(301+stage)
    road_edges = []
    for x in range(W):
        bend = (3*sin(x/25), 2*sin(x/17)+sin(x/8), 4*sin(x/30+0.5))[stage]
        top = round(73+bend-ROAD_WIDTHS[stage]/2)
        bottom = top+ROAD_WIDTHS[stage]-1
        road_edges.append((top,bottom))
        d.line((x,top-2,x,bottom+2),fill=shadow)
        d.line((x,top,x,bottom),fill=dirt)
        d.point((x,top+1),fill=highlight)
    for x,y,w,h in [(3,16,21,9),(54,11,20,9),(96,31,19,7),(138,16,21,8),
                    (4,127,26,10),(47,113,18,8),(85,124,27,8),(126,113,25,11)]:
        poly(d,[(x,y+2),(x+4,y),(x+w-6,y-1),(x+w,y+2),
                (x+w-3,y+h-1),(x+8,y+h),(x+2,y+h-2)],shadow)
        d.line((x+5,y+1,x+w-7,y+1),fill=base)
        poly(d,[(x+3,y+h-4),(x+9,y+h-2),(x+w-5,y+h-3),
                (x+w-3,y+h-1),(x+8,y+h),(x+2,y+h-2)],CLUSTER_SHADOWS[stage])
        for dx,dy in ((5,2),(9,3),(14,2)):
            d.line((x+dx,y+dy+1,x+dx+1,y+dy-1),fill=highlight)
    for x in range(4,W-4,6):
        top,bottom = road_edges[x]
        for y in (top+3,bottom-3):
            y += rng.randrange(-2,3)
            width = rng.randrange(2,6)
            d.line((x,y,x+width,y),fill=base)
            if rng.randrange(3)==0:
                d.line((x+1,y-1,x+width-1,y-1),fill=highlight)
    for i in range(360):
        x,y = rng.randrange(W),rng.randrange(144)
        top,bottom = road_edges[x]
        if top+3 <= y <= bottom-3:
            if i%4 == 0:
                d.line((x,y,x+rng.randrange(1,4),y),fill=base if stage!=1 else shadow)
            continue
        if top-3 <= y <= bottom+3:
            continue
        color = rng.choice((shadow,highlight,base))
        d.line((x,y,x+rng.randrange(1,4),y),fill=color)
        if i%5==0:
            d.line((x+1,y,x+2,y-2),fill=color)
    for x,y in [(9,17),(26,35),(39,16),(52,37),(74,22),(101,31),(131,14),
                (148,37),(14,113),(32,124),(56,110),(70,132),(100,117),(120,131),(145,113)]:
        if stage==1 or (stage==2 and x%2==0):
            poly(d,[(x-5,y+1),(x-4,y-2),(x-1,y-4),(x+3,y-4),(x+6,y),
                    (x+4,y+2),(x-3,y+2)],deep)
            poly(d,[(x-4,y-1),(x-1,y-4),(x+3,y-4),(x+5,y-1),(x+1,y)],dirt)
            d.line((x-2,y-3,x+2,y-3),fill=highlight)
        else:
            for dx,dy in [(-4,2),(0,-1),(4,1)]:
                xx,yy=x+dx,y+dy
                d.line((xx,yy,xx-1,yy+3),fill=deep)
                d.line((xx-1,yy,xx+1,yy),fill=sparkle)
                d.point((xx,yy-1),fill=sparkle if stage==2 else "#d7aeb0")
    for x in (12,34,61,87,115,143):
        top,bottom = road_edges[x]
        if stage == 0:
            for dx,dy in ((0,0),(3,2),(6,-1)):
                px,py = x+dx,bottom+7+dy
                d.line((px,py,px-1,py+3),fill=deep)
                d.point((px,py-1),fill="#e0b2ad")
                d.point((px+1,py),fill=sparkle)
        elif stage == 1:
            for dx,dy in ((0,0),(4,1),(7,-2)):
                px,py = x+dx,top-5+dy
                d.line((px,py,px+2,py),fill=highlight)
                d.line((px+1,py+1,px+3,py+1),fill=deep)
        else:
            for dx,h in ((0,4),(3,6),(6,3)):
                px,py = x+dx,bottom+8
                d.line((px,py,px-1,py-h),fill=deep)
                d.point((px-1,py-h),fill=sparkle)
    for x in (7,45,72,104,135):
        top,_ = road_edges[x]
        y = top+2
        d.line((x,y,x+3,y),fill=deep)
        d.line((x+1,y-1,x+3,y-1),fill=sparkle)
    return image

def tilemap(image, out):
    columns, width, height = 10, 10, 9
    atlas = Image.new("RGBA",(columns*16,height*16))
    gids = []
    for y in range(height):
        for x in range(width):
            box = x*16,y*16,(x+1)*16,(y+1)*16
            atlas.paste(image.crop(box),box[:2])
            gids.append(len(gids)+1)
    assert atlas.tobytes() == image.tobytes()
    atlas.save(out/"terrain-tiles.png")
    metadata = dict(type="map",version="1.10",orientation="orthogonal",renderorder="right-down",
        infinite=False,width=width,height=height,tilewidth=16,tileheight=16,nextlayerid=2,nextobjectid=1,
        layers=[dict(type="tilelayer",id=1,name="전장 지면",x=0,y=0,width=width,height=height,
                     visible=True,opacity=1,data=gids)],
        tilesets=[dict(firstgid=1,name="terrain",tilewidth=16,tileheight=16,columns=columns,
                       tilecount=len(gids),image="terrain-tiles.png",imagewidth=160,imageheight=144,
                       margin=0,spacing=0)])
    (out/"terrain.tmj").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    image_layers = [
        dict(type="imagelayer",id=i,name=name,image=file,x=0,y=0,
             offsetx=0,offsety=y,visible=True,opacity=1)
        for i,(name,file,y) in enumerate((("산 원경","mountains.png",0),
                                        ("중간 언덕","foothills.png",55)),2)
    ]
    terrain_layer = dict(metadata["layers"][0],offsetx=0,offsety=80)
    scene_map = dict(metadata,height=22,nextlayerid=4,layers=image_layers+[terrain_layer])
    (out/"battle.tmj").write_text(json.dumps(scene_map,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
    font = ImageFont.truetype(str(Path(os.environ["WINDIR"])/"Fonts/malgunbd.ttf"),20)
    board = Image.new("RGB",(1000,505),"#202933")
    labels = ImageDraw.Draw(board)
    wizard = Image.open(HERE.parent/"wizard-idle.png").convert("RGBA")
    sheet_path = HERE.parents[1]/"meadow-tilemap/tilemap/stage-slime-hop.png"
    slime = Image.open(sheet_path).convert("RGBA").crop((0,0,32,32)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    slime_size = round(32*SLIME_SCALE)
    slime = slime.resize((slime_size,slime_size),Image.Resampling.NEAREST)
    slime_origin = (SLIME_FEET[0]-round(16*SLIME_SCALE),
                    SLIME_FEET[1]-round(28*SLIME_SCALE))
    panel = Image.open(HERE.parent/"spell-panel.png").convert("RGBA")
    for index,(name,sky,rock,hill,ground) in enumerate(STAGES):
        out = HERE/f"stage-{index+1:02}"
        out.mkdir(exist_ok=True)
        scene = Image.new("RGBA",(W,352))
        for filename,image,origin in [
            ("mountains",mountain(index,sky,rock),(0,0)),
            ("foothills",hills(index,hill),(0,55)),
            ("battlefield",terrain(index,ground),(0,80)),
        ]:
            image.save(out/f"{filename}.png")
            scene.alpha_composite(image,origin)
            if filename == "battlefield":
                tilemap(image,out)
        assert scene.getchannel("A").crop((0,0,160,224)).getextrema() == (255,255)
        shadows = Image.new("RGBA",scene.size)
        draw = ImageDraw.Draw(shadows)
        draw.ellipse((16,150,31,154),fill=(47,41,55,78))
        draw.ellipse((121,150,136,154),fill=(47,41,55,68))
        scene.alpha_composite(shadows)
        scene.alpha_composite(wizard,(8,125))
        scene.alpha_composite(slime,slime_origin)
        scene.alpha_composite(panel,(0,224))
        scene.save(out/"preview.png")
        x=13+index*330
        labels.text((x,10),f"{index+1}  {name}",font=font,fill="#f0e5d0")
        board.paste(scene.crop((0,0,160,224)).resize((320,448),Image.Resampling.NEAREST),(x,43))
    board.save(HERE/"preview.png")
    manifest = dict(viewport_px=[160,352],tile_px=[16,16],grid=[10,9],
        layers=[
            dict(file="mountains.png",origin_px=[0,0],size_px=[160,80]),
            dict(file="foothills.png",origin_px=[0,55],size_px=[160,32],collision=False),
            dict(file="battlefield.png",origin_px=[0,80],size_px=[160,144]),
        ],terrain_map="terrain.tmj",scene_map="battle.tmj",wizard_feet_px=[24,153],
        slime_presentation=dict(scale=SLIME_SCALE,preview_feet_px=SLIME_FEET),
        shared_spell_panel=dict(file="../spell-panel.png",origin_px=[0,224]),
        stages=[dict(number=i+1,name=stage[0],directory=f"stage-{i+1:02}",
                     path_width_px=ROAD_WIDTHS[i]) for i,stage in enumerate(STAGES)])
    (HERE/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__":
    main()

