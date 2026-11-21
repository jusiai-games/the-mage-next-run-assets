from pathlib import Path
from math import pi, sin
from zipfile import ZIP_DEFLATED, ZipFile
import json
import os

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parents[2] / "prototypes/meadow-visual/assets"
REFERENCE_ICONS = ROOT.parents[2] / "references/reference-components/아이콘/스킬"
OUTPUT = ROOT / "tilemap"
OUTPUT.mkdir(exist_ok=True)
SPRITES = OUTPUT / "sprites"
SPRITES.mkdir(exist_ok=True)
FONT = Path(os.environ["WINDIR"]) / "Fonts/malgunbd.ttf"

TILE, WIDTH, HEIGHT = 16, 160, 352
NEAREST = Image.Resampling.NEAREST
INK, CREAM, GOLD, ICE = "#222034", "#F8CFAB", "#EAB853", "#ADE9FF"
SPELLS = [
    ("fire", "화염탄", "#FA9B46", 0.72),
    ("lightning", "연쇄 번개", ICE, 2.4),
    ("burst", "마력 폭발", "#FBDFFF", 3.4),
]
EXPANSION_ICONS = {
    "rock": ("낙석", "#D3B082"),
    "geyser": ("물기둥", "#86C9F1"),
    "tornado": ("회오리", "#C6E7BB"),
}
SPELL_COLORS = {key: accent for key, _, accent, _ in SPELLS}
SPELL_COLORS.update({key: accent for key, (_, accent) in EXPANSION_ICONS.items()})
SLOT_Y, SLOT_SIZE, SLOT_GAP, MAX_SLOTS = 310, 22, 2, 6
FACE_SIZE, FACE_OFFSET = 18, 2
DIM = 64
CLOUD_CYCLE_MS = 16000
STAGE_CYCLE_MS = 8640
SLIME_FRAME_DIR = ROOT.parents[2] / "work/color-pass-v3/slime32-v7-state-transitions"
SLIME_EXPORT = ROOT.parent / "meadow-slime"


def rgba(path):
    with Image.open(path) as image:
        return image.convert("RGBA")


def canvas():
    return Image.new("RGBA", (WIDTH, HEIGHT))


def label(image, text, x, y, size, color=CREAM):
    ImageDraw.Draw(image).text((x, y), text, font=ImageFont.truetype(str(FONT), size),
                              fill=color, anchor="mt")


def stretch(image, size):
    """Stretch timber plates from their current 8x6 fixed corner boundaries."""
    xs, ys = (0, 8, image.width-8, image.width), (0, 6, image.height-6, image.height)
    width, height = size
    target_x, target_y = (0, 8, width-8, width), (0, 6, height-6, height)
    result = Image.new("RGBA", size)
    for row in range(3):
        for col in range(3):
            box = (xs[col], ys[row], xs[col+1], ys[row+1])
            target = (target_x[col+1]-target_x[col], target_y[row+1]-target_y[row])
            result.paste(image.crop(box).resize(target, NEAREST), (target_x[col],target_y[row]))
    return result


def stamp(layer, asset, xy, size=None):
    image = rgba(ASSETS / asset)
    layer.alpha_composite(stretch(image,size) if size else image, xy)


def pack_layers(layers):
    result = canvas()
    for _, image in layers:
        result.alpha_composite(image)
    return result


def build_ground():
    sky, ground, hedge = Image.new("RGBA", (WIDTH, HEIGHT), INK), canvas(), canvas()
    sky.alpha_composite(rgba(ASSETS / "distant-meadow.png"))
    # Use the current terrain atlas and its actual tile placement IDs.
    atlas = rgba(ASSETS / "atlas/meadow_wave.png")
    specs = json.loads((ASSETS / "atlas/meadow_wave.sprite.json").read_text())
    index = {sprite["name"].rsplit("_",1)[1]: (sprite["x"], sprite["y"]) for sprite in specs["sprites"]}
    layout = json.loads((ASSETS / "layout.json").read_text())
    for row, cells in enumerate(layout["tile_rows"]):
        for col, key in enumerate(cells):
            x, y = index[key]
            ground.alpha_composite(atlas.crop((x,y,x+TILE,y+TILE)),(col*TILE,80+row*TILE))
    assert ground.crop((0,80,160,224)).tobytes() == rgba(ASSETS/"meadow-terrain.png").tobytes()
    hedge.alpha_composite(rgba(ASSETS / "meadow-hedge.png"), (0,66))
    return [("원경",sky),("초원 타일",ground),("덤불",hedge)]


LAND = build_ground()


def repeated_pixel_scale(image):
    """Find a whole-image integer upscale by round-tripping its pixel blocks."""
    for scale in (4, 3, 2):
        width = image.width // scale * scale
        height = image.height // scale * scale
        aligned = image.crop((0, 0, width, height))
        reduced = aligned.resize((width // scale, height // scale), NEAREST)
        if reduced.resize(aligned.size, NEAREST).tobytes() == aligned.tobytes():
            return scale
    return 1


def title_landscape():
    source = rgba(ROOT / "sources/title-cloudless.png")
    # Map the established framing back to the original art before sampling.
    left, top = 412, 4
    crop = (left * source.width / 640, top * source.height / 360,
            (left + WIDTH) * source.width / 640, (top + HEIGHT) * source.height / 360)
    landscape = source.resize((WIDTH, HEIGHT), NEAREST, box=crop)
    scale = repeated_pixel_scale(landscape)
    if scale != 1:
        raise ValueError(f"Title background repeats {scale}x{scale} pixel blocks on the 1x canvas")
    return landscape


def title_clouds():
    source = rgba(ASSETS / "distant-meadow.png").crop((0,0,45,21))
    sky = source.getpixel((0,0))
    # Lift the existing silhouette into a separate transparent sprite.
    clean = Image.new("RGBA",source.size)
    for y in range(source.height):
        for x in range(source.width):
            if source.getpixel((x,y)) != sky:
                clean.putpixel((x,y),(223,241,250,255) if y<14 else (155,198,225,255))
    clean = clean.crop(clean.getbbox())
    layer = canvas()
    for x,y,width in ((8,21,43),(80,104,63),(126,52,29),(35,128,25)):
        height = max(1,round(clean.height * width / clean.width))
        layer.alpha_composite(clean.resize((width,height),NEAREST),(x,y))
    return layer


def title_cloud_occlusion(landscape, clouds):
    """Keep the scrolling sky detail behind the stone silhouette."""
    mask = canvas()
    top, bottom = clouds.getbbox()[1::2]
    for y in range(top,bottom):
        sky = landscape.getpixel((0,y))
        for x in range(WIDTH):
            color = landscape.getpixel((x,y))
            if max(abs(value-reference) for value, reference in zip(color[:3],sky[:3])) > 20:
                mask.putpixel((x,y),color)
    return mask


def stage_landscape():
    distant = rgba(ASSETS/"distant-meadow.png").crop((4,0,84,80)).resize((80,156),NEAREST)
    far = Image.new("RGBA",(160,HEIGHT))
    far.alpha_composite(distant)
    far.alpha_composite(ImageOps.mirror(distant),(80,0))
    grass = rgba(ASSETS/"meadow-terrain.png").resize((160,196),NEAREST)
    hedge = rgba(ASSETS/"meadow-hedge.png")
    ground = Image.new("RGBA",(320,HEIGHT))
    ground.alpha_composite(grass,(0,156))
    ground.alpha_composite(ImageOps.mirror(grass),(160,156))
    ground.alpha_composite(hedge,(0,144))
    ground.alpha_composite(ImageOps.mirror(hedge),(160,144))
    return far, ground


def stage_path(width):
    # Recover 16x16 dirt textures from the existing meadow illustration.
    meadow = rgba(ASSETS/"title-meadow.png")
    textures = [meadow.crop((x,y,x+TILE,y+TILE)) for x,y in ((257,131),(204,160))]
    shade_ramp = [ImageColor.getcolor(color,"RGBA")
                  for color in ("#9A6F49","#B58957","#CAA163","#D9B478")]
    trail = Image.new("RGBA",(width,HEIGHT))
    draw = ImageDraw.Draw(trail)
    for x in range(width):
        phase = 2*pi*x/width
        center = round(231+4*sin(phase)+3*sin(3*phase))
        edge = (x%7 in (0,1)) - (x%11 in (7,8))
        draw.line((x,center-14+edge,x,center+14-edge),fill="#7E8547")
        texture = textures[(x//TILE)%len(textures)]
        for y in range(center-12+edge, center+13-edge):
            r,g,b,_ = texture.getpixel((x%TILE,y%TILE))
            lightness = (3*r+6*g+b)//10
            shade = min(3,max(0,(lightness-127)//24))
            if abs(y-center) >= 11:
                shade = max(0,shade-1)
            trail.putpixel((x,y),shade_ramp[shade])
    return trail


def stage_hop():
    meta = json.loads((SLIME_EXPORT/"animation.json").read_text())
    timing = meta["clips"]["advance"]["duration_ms"]
    pivot = meta["pivot_top_left"]
    sheet = Image.new("RGBA",(32*len(timing),32))
    for index in range(len(timing)):
        frame = rgba(SLIME_FRAME_DIR/f"slime32_advance_left_{index:02}.png")
        assert frame.size == (32,32)
        sheet.paste(ImageOps.mirror(frame),(32*index,0))
    assert STAGE_CYCLE_MS % sum(timing) == 0
    assert pivot == [16,28]
    return sheet, timing, pivot


def start_foreground(stage):
    shade, title, button, text = (canvas() for _ in range(4))
    gradient = ImageDraw.Draw(shade)
    for y in range(HEIGHT):
        alpha = max(0, 162-y*2, 148-(HEIGHT-1-y)*2)
        gradient.line((0,y,WIDTH-1,y),fill=(20,19,36,alpha))

    if stage:
        stamp(title,"ui/hud.png",(44,40),(72,19))
        label(text,"스테이지 1",80,45,8,ICE)
        label(text,"초원",80,65,18,"#F0FCFF")
        stamp(title,"ui/hud.png",(43,244),(74,17))
        label(text,"초원 슬라임",80,248,8)
    else:
        title.alpha_composite(rgba(ROOT / "sources/title-lockup.png"),(4,38))

    stamp(button,"ui/primary.png",(34,289),(92,28))
    label(text,"전투 시작" if stage else "게임 시작",80,297,11,"#F0FCFF")
    return [("화면 가장자리 명암",shade),("제목",title),("시작 버튼",button),("화면 글자",text)]


def scroll_layer(strip, phase):
    left = round(strip.width * phase) % strip.width
    end = min(left + WIDTH,strip.width)
    layer = canvas()
    layer.paste(strip.crop((left,0,end,HEIGHT)))
    if end-left < WIDTH:
        layer.paste(strip.crop((0,0,WIDTH-(end-left),HEIGHT)),(end-left,0))
    return layer


def title_frame(landscape, clouds, foreground, phase):
    return [("고정 초원 배경",landscape),("이동 구름",scroll_layer(clouds,-phase))] + foreground


def stage_frame(far, ground, path, sheet, pivot, foreground, phase, frame_index):
    slime = canvas()
    ImageDraw.Draw(slime).ellipse((65,229,86,233), fill=(27,39,33,127))
    x = 32*frame_index
    slime.alpha_composite(sheet.crop((x,0,x+32,32)),(76-pivot[0],232-pivot[1]))
    return [("이동 원경",scroll_layer(far,phase)),("이동 초원",scroll_layer(ground,phase)),
            ("흙길",scroll_layer(path,phase)),
            ("슬라임",slime)] + foreground


def save_animation(name, frames, durations):
    palette = frames[0].quantize(colors=256)
    indexed = [frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(OUTPUT/name,save_all=True,append_images=indexed[1:],
                    duration=durations,loop=0,optimize=True)


def start_animation(landscape, clouds, far, ground, path, sheet, timing, pivot, title, stage):
    for name, image in (
        ("game-title-background.png",landscape),("game-title-clouds.png",clouds),
        ("stage-far-loop.png",far),("stage-ground-loop.png",Image.alpha_composite(ground,path)),
        ("stage-path-strip.png",path),
        ("stage-slime-hop.png",sheet),("game-title-foreground.png",pack_layers(title)),
        ("stage-start-foreground.png",pack_layers(stage)),
    ):
        image.save(OUTPUT/name,optimize=True)
    (OUTPUT/"stage-slime-hop.json").write_text(
        json.dumps({"cell_px":32,"pivot_top_left":pivot,"duration_ms":timing},indent=2)+"\n",
        encoding="utf-8",
    )
    title_frames = [pack_layers(title_frame(landscape,clouds,title,ms/CLOUD_CYCLE_MS))
                    .resize((320,704),NEAREST).convert("RGB")
                    for ms in range(0,CLOUD_CYCLE_MS,100)]
    save_animation("game-title-clouds.gif",title_frames,[100]*len(title_frames))
    stage_frames, durations = [], []
    elapsed = 0
    while elapsed < STAGE_CYCLE_MS:
        for frame_index, duration in enumerate(timing):
            frame = pack_layers(stage_frame(far,ground,path,sheet,pivot,stage,elapsed/STAGE_CYCLE_MS,frame_index))
            stage_frames.append(frame.resize((320,704),NEAREST).convert("RGB"))
            durations.append(duration)
            elapsed += duration
    save_animation("stage-start-slime-hop.gif",stage_frames,durations)
    assert title_frames[0].tobytes() != title_frames[len(title_frames)//2].tobytes()
    assert stage_frames[0].tobytes() != stage_frames[6].tobytes()


def battle_base(shield_energy=5, shield_capacity=5, combat_power=120):
    actors, hud, panel, text = (canvas() for _ in range(4))
    lower_ground = canvas()
    lower_ground.alpha_composite(ImageOps.flip(LAND[1][1].crop((0,176,160,224))),(0,224))
    shield = rgba(ASSETS / "ui/shield-normal.png").resize((42,32),NEAREST)
    actors.alpha_composite(shield,(8,125))
    stamp(actors,"hood_staff_idle_right_00.png",(8,125))
    for xy in ((113,109),(98,149),(124,177)):
        stamp(actors,"slime32_idle_left_00.png",xy)
    stamp(hud,"ui/hud.png",(5,6),(75,22))
    label(text,"웨이브 1 / 5",43,13,9)

    # Use the title plate and inset-well structure from the spell-window reference.
    stamp(panel,"ui/panel.png",(4,268),(152,77))
    ImageDraw.Draw(panel).rectangle((9,289,150,336),fill=INK)
    stamp(panel,"ui/hud.png",(10,274),(91,27))
    stamp(panel,"ui/hud.png",(105,274),(45,27))
    label(text,"방어막 에너지",44,279,8,CREAM)
    label(text,f"{shield_energy} / {shield_capacity}",83,279,8,ICE)
    label(text,"전투력",127,278,7,CREAM)
    label(text,str(combat_power),127,288,9,GOLD)
    draw = ImageDraw.Draw(panel)
    for segment in range(shield_capacity):
        left = 17 + 77 * segment // shield_capacity
        right = 16 + 77 * (segment + 1) // shield_capacity
        draw.rectangle((left,290,right-2,294),fill="#505276")
        if segment < shield_energy:
            draw.rectangle((left,290,right-2,292),fill=ICE)
            draw.line((left,293,right-2,293),fill="#589DC8")
    return LAND + [("초원 하단 타일",lower_ground),("마법사와 슬라임",actors),
                   ("전투 HUD",hud),("스펠 창",panel),("화면 글자",text)]


SLOT_FRAME = stretch(rgba(ASSETS / "ui/card.png"),(SLOT_SIZE,SLOT_SIZE))
RIM = Image.new("RGBA",SLOT_FRAME.size)
rim_end = SLOT_SIZE - 1
ImageDraw.Draw(RIM).polygon([(3,0),(rim_end-3,0),(rim_end,3),(rim_end,rim_end-3),
                            (rim_end-3,rim_end),(3,rim_end),(0,rim_end-3),(0,3)],
                            outline=GOLD)
RIM.save(SPRITES / "ready-rim.png")


def make_faces():
    images = {}
    for key, accent in SPELL_COLORS.items():
        image = Image.new("RGBA",(FACE_SIZE,FACE_SIZE))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,FACE_SIZE-1,FACE_SIZE-1),fill="#222034",outline=accent)
        if key in EXPANSION_ICONS:
            folder, _ = EXPANSION_ICONS[key]
            icon = rgba(REFERENCE_ICONS / folder / f"{folder}-Foozle.png")
            icon = icon.crop((4,4,icon.width-4,icon.height-4))
        else:
            icon = rgba(ASSETS / f"icon-{key}.png")
            icon = icon.crop(icon.getbbox())
        icon = ImageOps.contain(icon,(FACE_SIZE-2,FACE_SIZE-2),NEAREST)
        image.alpha_composite(icon,((FACE_SIZE-icon.width)//2,(FACE_SIZE-icon.height)//2))
        image.save(SPRITES / f"{key}-face.png")
        Image.new("RGBA", (FACE_SIZE,1), accent).save(SPRITES / f"{key}-cooldown-edge.png")
        images[key] = image
    SLOT_FRAME.save(SPRITES/"slot-frame.png")
    return images


FACES = make_faces()


def spell_slot(key, progress):
    face = FACES[key]
    rows = int(max(0,min(1,progress))*face.height + .5)
    dimmed = face.point([round(value*DIM/255) for value in range(256)]*3+list(range(256)))
    image = SLOT_FRAME.copy()
    image.alpha_composite(face if progress >= 1 else dimmed,(FACE_OFFSET,FACE_OFFSET))
    if progress >= 1:
        image.alpha_composite(RIM)
    elif rows:
        split = face.height - rows
        left, y = FACE_OFFSET, FACE_OFFSET+split
        image.alpha_composite(face.crop((0,split,face.width,face.height)),(left,y))
        ImageDraw.Draw(image).line((left,y,left+FACE_SIZE-1,y),fill=SPELL_COLORS[key])
    return image


def slot_origins(count):
    if not 0 <= count <= MAX_SLOTS:
        raise ValueError(f"Expected up to {MAX_SLOTS} spell slots")
    width = count*SLOT_SIZE + max(0,count-1)*SLOT_GAP
    start = (WIDTH - width)//2
    return [start + index*(SLOT_SIZE+SLOT_GAP) for index in range(count)]


def cooldown_layer(equipped):
    layer = canvas()
    for x, (key, progress) in zip(slot_origins(len(equipped)),equipped):
        layer.alpha_composite(spell_slot(key,progress),(x,SLOT_Y))
    return "스펠 밝기",layer


def draw_grid(image, scale):
    result = image.resize((WIDTH*scale,HEIGHT*scale),NEAREST)
    grid = Image.new("RGBA",result.size)
    draw = ImageDraw.Draw(grid)
    for x in range(TILE*scale,WIDTH*scale,TILE*scale):
        draw.line((x,0,x,HEIGHT*scale-1),fill=(232,227,215,32))
    for y in range(TILE*scale,HEIGHT*scale,TILE*scale):
        draw.line((0,y,WIDTH*scale-1,y),fill=(232,227,215,32))
    return Image.alpha_composite(result,grid)


def export_maps(screens):
    lookup, tiles, maps = {}, [], {}
    columns = 16
    for key, layers in screens.items():
        entries = []
        for layer_id,(name, image) in enumerate(layers,1):
            cells = []
            for y in range(0,HEIGHT,TILE):
                for x in range(0,WIDTH,TILE):
                    tile = image.crop((x,y,x+TILE,y+TILE))
                    if not tile.getbbox():
                        cells.append(0)
                        continue
                    data = tile.tobytes()
                    if data not in lookup:
                        tiles.append(tile)
                        lookup[data] = len(tiles)
                    cells.append(lookup[data])
            entries.append(dict(id=layer_id,name=name,type="tilelayer",x=0,y=0,
                                width=WIDTH//TILE,height=HEIGHT//TILE,data=cells,visible=True,opacity=1))
        maps[key] = entries
    tile_atlas = Image.new("RGBA",(columns*TILE,((len(tiles)+columns-1)//columns)*TILE))
    for i, tile in enumerate(tiles):
        tile_atlas.paste(tile,((i%columns)*TILE,(i//columns)*TILE))
    tile_atlas.save(OUTPUT/"meadow-ui-tiles.png", optimize=True)
    texture = dict(firstgid=1,name="Meadow UI",tilewidth=TILE,tileheight=TILE,
                   columns=columns,tilecount=len(tiles),spacing=0,margin=0,
                   image="meadow-ui-tiles.png",imagewidth=tile_atlas.width,imageheight=tile_atlas.height)
    for key, layers in maps.items():
        data = dict(type="map",version="1.10",tiledversion="1.10.2",orientation="orthogonal",
                    renderorder="right-down",infinite=False,tilewidth=TILE,tileheight=TILE,
                    width=WIDTH//TILE,height=HEIGHT//TILE,layers=layers,
                    nextlayerid=len(layers)+1,nextobjectid=1,tilesets=[texture])
        (OUTPUT/f"{key}.tmj").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        reconstructed = []
        for layer in layers:
            recovered = canvas()
            for index,gid in enumerate(layer["data"]):
                if gid == 0:
                    continue
                source_x, source_y = ((gid-1)%columns)*TILE, ((gid-1)//columns)*TILE
                recovered.paste(tile_atlas.crop((source_x,source_y,source_x+TILE,source_y+TILE)),
                                ((index%(WIDTH//TILE))*TILE,(index//(WIDTH//TILE))*TILE))
            reconstructed.append((layer["name"],recovered))
        assert pack_layers(reconstructed).tobytes() == pack_layers(screens[key]).tobytes()


def compare(screens):
    overview = Image.new("RGBA",(1560,1150),"#1A1928")
    previews = (("game-title","게임 시작"),("stage-start","전투 시작"),("battle","전투 중 · 하단 HUD"))
    for index, (key, text) in enumerate(previews):
        x = 28 + 512*index
        label(overview,text,x+240,18,23)
        overview.alpha_composite(draw_grid(pack_layers(screens[key]),3),(x,58))
    label(overview,"16×16px 타일 · 화면 160×352px · 오른쪽 세 슬롯은 충전 0% / 50% / 100% 예시",780,1122,14)
    overview.convert("RGB").save(OUTPUT/"meadow-tilemap-preview.png",optimize=True)


def compare_slot_counts(screens):
    overview = Image.new("RGBA",(1048,340),"#1A1928")
    for index, (key, text) in enumerate((("battle","3개 장착"),("battle-six-slots","6개 장착 예시"))):
        x = 28 + 512*index
        label(overview,text,x+240,21,23)
        panel = pack_layers(screens[key]).crop((0,264,WIDTH,HEIGHT))
        overview.alpha_composite(panel.resize((480,264),NEAREST),(x,61))
    overview.convert("RGB").save(OUTPUT/"spell-slot-layouts.png",optimize=True)
    # Fit the full 20:9 logical image inside an example 390x844px viewport.
    mobile = Image.new("RGBA",(390,844),"#1A1928")
    battle = ImageOps.contain(pack_layers(screens["battle-six-slots"]), mobile.size, NEAREST)
    mobile.alpha_composite(battle,((mobile.width-battle.width)//2,0))
    mobile.convert("RGB").save(OUTPUT/"mobile-battle-390.png",optimize=True)


def cooldown_examples(base):
    strip = Image.new("RGBA",(840,520),"#1A1928")
    label(strip,"주문별 쿨타임",420,19,23)
    for index, text in enumerate(("시전 직후","25%","50%","75%","사용 가능")):
        label(strip,text,208+132*index,71,15)
    for row, (key,name,accent,_) in enumerate(SPELLS):
        y = 107 + row*137
        label(strip,name,70,y+52,16,accent)
        for index in range(5):
            slot = spell_slot(key,index/4).resize((120,120),NEAREST)
            strip.alpha_composite(slot,(148+132*index,y))
    strip.convert("RGB").save(OUTPUT/"spell-cooldown-styles.png",optimize=True)

    # Show the same bottom-to-top reveal used by SpellCooldownView.
    frames = []
    for step in range(69):
        state = [min(step/20/duration,1) for _,_,_,duration in SPELLS]
        equipped = [(spell[0], progress) for spell, progress in zip(SPELLS, state)]
        frame = pack_layers(base+[cooldown_layer(equipped)]).crop((0,264,WIDTH,HEIGHT))
        frames.append(frame.resize((480,264),NEAREST).convert("RGB"))
    frames[0].save(OUTPUT/"spell-cooldown.gif",save_all=True,append_images=frames[1:],
                   duration=[50]*68+[1100],loop=0,optimize=True)
    left, right = FACE_OFFSET, FACE_OFFSET+FACE_SIZE
    for key in SPELL_COLORS:
        dim, ready = spell_slot(key,0), spell_slot(key,1)
        for progress in (.25, .5, .75):
            slot = spell_slot(key,progress)
            edge = right - int(FACE_SIZE*progress+.5)
            above = (left,left,right,edge)
            below = (left,edge+1,right,right)
            assert slot.crop(above).tobytes() == dim.crop(above).tobytes()
            assert slot.crop((left,edge,right,edge+1)).tobytes() == rgba(SPRITES/f"{key}-cooldown-edge.png").tobytes()
            assert slot.crop(below).tobytes() == ready.crop(below).tobytes()


if __name__ == "__main__":
    battle = battle_base()
    landscape, clouds = title_landscape(), title_clouds()
    title, stage = start_foreground(False), start_foreground(True)
    title.insert(0,("폐허 구름 가림",title_cloud_occlusion(landscape,clouds)))
    far, ground = stage_landscape()
    path = stage_path(ground.width)
    sheet, timing, pivot = stage_hop()
    starter = [(spell[0], progress) for spell, progress in zip(SPELLS,(0,.5,1))]
    expanded = starter + list(zip(EXPANSION_ICONS,(.25,.75,1)))
    assert all(9 <= x and x+SLOT_SIZE <= 151 for x in slot_origins(len(expanded)))
    screens = {
        "game-title": title_frame(landscape,clouds,title,0),
        "stage-start": stage_frame(far,ground,path,sheet,pivot,stage,.25,6),
        "battle": battle+[cooldown_layer(starter)],
        "battle-six-slots": battle+[cooldown_layer(expanded)],
    }
    for screen, layers in screens.items():
        for name, image in layers:
            if image.size != (WIDTH, HEIGHT):
                raise ValueError(f"{screen}/{name}: {image.size}, expected {(WIDTH, HEIGHT)}")
    export_maps(screens)
    compare(screens)
    compare_slot_counts(screens)
    cooldown_examples(battle)
    start_animation(landscape,clouds,far,ground,path,sheet,timing,pivot,title,stage)
    with ZipFile(ROOT/"meadow-tilemap-ui.zip","w",ZIP_DEFLATED) as file:
        for path in sorted(OUTPUT.rglob("*")):
            if path.is_file():
                file.write(path,path.relative_to(OUTPUT))
        for name in ("README.md","SpellCooldownView.cs","StartStripScroll.cs","StageSlimeHop.cs"):
            file.write(ROOT/name,name)
    with ZipFile(ROOT/"meadow-tilemap-ui.zip") as file:
        assert file.testzip() is None
    print("All four 10x22 maps round-trip pixel-exactly from the shared 16x16 atlas.")

