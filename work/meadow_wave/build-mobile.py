from pathlib import Path
from collections import Counter
import json
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont, ImageColor

game = Path(__file__).resolve().parents[2]
pixel_art = game.parent / 'pixel-art-production/tools/pixel-art/pixel_art.py'
work = game / 'work/meadow_wave/mobile'
source = game / 'sources/meadow_wave/01'
out = game / 'exports/meadow-wave-mobile'
approved = game / 'approved/meadow_wave_mobile'
for folder in (out, approved, work / 'tiles'):
    folder.mkdir(parents=True, exist_ok=True)

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

def palette(name):
    return json.loads((game / 'palettes' / f'{name}.json').read_text())

meadow = palette('hood_staff_32_meadow')
wizard_colors = palette('hood_staff_32_quick')
effects = palette('hood_staff_32_cast_quick')
slime_source = game / 'approved/meadow_slime_combat32_v7/advance'
slime_frames = [Image.open(slime_source / f'slime32_advance_left_{index:02}.png').convert('RGBA')
                for index in (0, 7, 15)]
slime_colors = sorted({'#%02X%02X%02X' % pixel[:3] for frame in slime_frames for pixel in frame.get_flattened_data() if pixel[3]})
colors = list(dict.fromkeys(meadow + effects + slime_colors))
write_json(work / 'palette.json', colors)

old = game / 'exports/hood-staff-32-final/meadow'
quick = game / 'exports/hood-staff-32-quick-cast'
terrain = Image.open(old / 'terrain.png').convert('RGBA').crop((64,16,224,160))
terrain.save(out / 'meadow-terrain.png')
wizard = Image.open(quick / 'idle/hood_staff_idle.png').convert('RGBA').crop((0,0,32,32))
wizard.save(out / 'wizard-idle.png')

# Sample the generated horizon on the game's pixel grid and use only existing colors.
sky_source = Image.open(source / 'generated.png').convert('RGB')
sample = sky_source.resize((160, 84), Image.Resampling.BOX).crop((0, 0, 160, 80))
sky = Image.new('RGBA', sample.size)
bg_colors = [ImageColor.getrgb(c) for c in meadow if c != '#D88475']
for y in range(80):
    for x in range(160):
        pixel = sample.getpixel((x,y))
        nearest = min(bg_colors, key=lambda c: sum((a-b)**2 for a,b in zip(pixel,c)))
        sky.putpixel((x,y), (*nearest,255))
# Gradually replace the lower strip with the first row of the terrain.
matrix = ((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
for y in range(72,80):
    for x in range(160):
        if matrix[y%4][x%4] < (y-71)*2:
            sky.putpixel((x,y), terrain.getpixel((x,0)))
sky.save(out / 'distant-meadow.png')

# The hedge overlaps both layers and sits behind the combat sprites.
hedge_source = Image.open(game / 'sources/meadow_wave_hedge/01/generated.png').convert('RGBA')
mask = hedge_source.getchannel('A').point(lambda alpha: 255 if alpha >= 128 else 0)
hedge_source = hedge_source.crop(mask.getbbox())
hedge_sample = hedge_source.resize((160, 19), Image.Resampling.BOX)
hedge = Image.new('RGBA', hedge_sample.size)
hedge_colors = [ImageColor.getrgb(color) for color in ('#68865C', '#749466', '#7CA06E', '#8FAF74', '#99B77D', '#AAC586')]
for y in range(hedge.height):
    for x in range(hedge.width):
        r, g, b, alpha = hedge_sample.getpixel((x, y))
        if alpha >= 128:
            nearest = min(hedge_colors, key=lambda color: sum((a-b)**2 for a,b in zip((r,g,b),color)))
            hedge.putpixel((x,y), (*nearest,255))
hedge_origin = (0, 66)
assert set(hedge.getchannel('A').get_flattened_data()) == {0,255}
hedge.save(out / 'meadow-hedge.png')

dark, rim, steel, shade = '#222034','#505276','#454568','#28283F'
gold, glow, blue, ice, white = '#EAB853','#F8CFAB','#589DC8','#ADE9FF','#F0FCFF'
panel = Image.new('RGBA',(160,128),dark)
d = ImageDraw.Draw(panel)
d.rectangle((0,0,159,1),fill=gold)
d.rectangle((0,2,159,4),fill=rim)
d.rectangle((0,5,159,127),fill=shade)
d.line((5,122,154,122),fill=steel)
for x in (4,155):
    d.point((x,8),fill=gold)
    d.point((x,122),fill=gold)
panel.save(out / 'spell-panel.png')

atlas = Image.new('RGBA',(72,24))
def slot(active):
    im = Image.new('RGBA',(32,32))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((1,2,30,31),radius=3,fill=dark)
    draw.rounded_rectangle((1,0,30,29),radius=3,fill=gold if active else rim)
    draw.rounded_rectangle((3,2,28,27),radius=2,fill=steel)
    draw.rectangle((5,4,26,23),fill=shade)
    draw.line((6,25,25,25),fill=dark,width=2)
    return im
atlas.alpha_composite(slot(True).resize((24,24),Image.Resampling.NEAREST),(0,0))
atlas.alpha_composite(slot(False).resize((24,24),Image.Resampling.NEAREST),(24,0))
d = ImageDraw.Draw(atlas)
d.rectangle((48,0,71,1),fill=blue)
d.line((48,0,71,0),fill=ice)
atlas.save(out / 'spell-slots.png')
write_json(out / 'spell-slots.json', {
    'origin':'top_left','cell_px':24,
    'tiles':{'ready':[0,0,24,24],'cooldown':[24,0,24,24],'fill':[48,0,24,24]},
    'fill_track_local_xywh':[5,18,15,1], 'preview_slot_origins':[[5+25*i,49+30*j] for j in range(2) for i in range(6)],
})
# Spell symbols and example cooldown fill exist only in the composition.
ui = panel.copy()
font = ImageFont.load_default(size=8)
label = Image.new('1', ui.size)
ImageDraw.Draw(label).text((80,35),'SPELLS',font=font,fill=1,anchor='mt')
ui.paste(glow, (0,0,*ui.size), label)
ImageDraw.Draw(ui).rounded_rectangle((16,9,143,28), radius=4, fill=dark, outline=rim)
stats = Image.new('1', ui.size)
ImageDraw.Draw(stats).text((80,14),'HP  100      MANA  30',font=font,fill=1,anchor='mt')
ui.paste(ice,(0,0,*ui.size),stats)
for index in range(12):
    x, y = 5+(index%6)*25, 49+(index//6)*30
    fill = (20,12,6,16,9,4,11,7,0,0,0,0)[index]
    ui.alpha_composite(slot(index==0).resize((24,24),Image.Resampling.NEAREST),(x,y))
    if index >= 8:
        continue
    icon = Image.new('RGBA',(32,32))
    d = ImageDraw.Draw(icon)
    if index % 4 == 0:
        d.polygon([(8,17),(13,12),(13,8),(19,6),(22,10),(23,14),(19,19),(13,19)],fill=blue)
        d.polygon([(11,16),(17,11),(18,8),(21,10),(20,14),(16,17)],fill=ice)
        d.rectangle((18,10,19,12),fill=white)
    elif index % 4 == 1:
        d.polygon([(16,5),(23,9),(22,15),(16,20),(10,15),(9,9)],fill=blue)
        d.polygon([(16,7),(20,10),(19,15),(16,17),(13,14),(12,10)],fill=ice)
        d.line((16,8,16,15),fill=white)
    elif index % 4 == 2:
        d.polygon([(17,5),(18,10),(24,12),(18,14),(16,20),(14,14),(8,12),(14,10)],fill=gold)
        d.rectangle((15,11,17,13),fill=white)
    else:
        d.polygon([(16,5),(22,9),(20,16),(16,20),(12,16),(10,10)],fill=blue)
        d.polygon([(16,6),(19,10),(17,16),(13,13),(12,10)],fill=ice)
        d.point((16,8),fill=white)
    d.rectangle((6,24,5+fill,25),fill=gold if index==0 else blue)
    ui.alpha_composite(icon.resize((24,24),Image.Resampling.NEAREST),(x,y))

preview = Image.new('RGBA',(160,352),dark)
preview.alpha_composite(sky,(0,0))
preview.alpha_composite(terrain,(0,80))
preview.alpha_composite(hedge,hedge_origin)
preview.alpha_composite(ui,(0,224))
pivot = (16,28)
feet = (24,153)
assert wizard.size == (32,32) and json.loads((game/'character-frame.json').read_text())['size'] == 32
assert (28 <= wizard.getbbox()[3] <= 30)
ImageDraw.Draw(preview).ellipse((16,150,34,155),fill='#749466')
preview.alpha_composite(wizard,(feet[0]-pivot[0],feet[1]-pivot[1]))
for frame, (x,y) in zip(slime_frames, ((104,155),(134,131),(146,179))):
    assert frame.size == (32,32) and frame.getbbox()[3] <= 30
    ImageDraw.Draw(preview).ellipse((x-7,y-2,x+7,y+1),fill='#749466')
    preview.alpha_composite(frame,(x-16,y-28))
hud = Image.new('1',preview.size)
ImageDraw.Draw(hud).text((80,13),'WAVE  2 / 15',font=ImageFont.load_default(size=10),fill=1,anchor='mt')
preview.paste(dark,(0,0,*preview.size),hud)
d = ImageDraw.Draw(preview)
d.rounded_rectangle((43,25,116,31),radius=2,fill=steel)
d.rectangle((45,27,75,29),fill=ice)
preview.resize((640,1408),Image.Resampling.NEAREST).save(out/'meadow-wave-preview.png')

# Package the playable terrain on the existing 16px tile convention.
cells = {}
rows = []
for y in range(0,144,16):
    row = []
    for x in range(0,160,16):
        tile = terrain.crop((x,y,x+16,y+16))
        key = tile.tobytes()
        if key not in cells:
            tile_id = f't{len(cells):03}'
            cells[key] = tile_id
            tile.save(work/'tiles'/f'meadow_wave_{tile_id}.png')
        row.append(cells[key])
    rows.append(row)
manifest = work / 'manifest.json'
write_json(manifest, {'name':'meadow_wave','kind':'tile','columns':10,'tiles':list(cells.values()),
                      'palette':'../../../palettes/hood_staff_32_meadow.json'})
layout = {'tile_size_px':16,'width_tiles':10,'height_tiles':9,'origin':'top_left',
          'atlas':'atlas/meadow_wave.png','tile_rows':rows,'scene_size_px':[160,352],
          'layer_origins':{'background':[0,0],'terrain':[0,80],'spell_panel':[0,224]},
          'decorations':[{'sprite':'meadow-hedge.png','origin_px':list(hedge_origin),'collision':False}],
          'wizard_foot_pivot_px':list(pivot),'wizard_feet_scene_px':list(feet),
          'enemy_entry':'right','suggested_enemy_entry_scene_x':159}
write_json(out/'layout.json',layout)
commands = [
    ['validate',str(out/'meadow-hedge.png'),'--size','160','19','--palette',str(game/'palettes/hood_staff_32_meadow.json')],
    
    ['validate',str(out/'meadow-terrain.png'),'--size','160','144','--palette',str(game/'palettes/hood_staff_32_meadow.json')],
    ['validate',str(out/'distant-meadow.png'),'--size','160','80','--palette',str(game/'palettes/hood_staff_32_meadow.json')],
    ['validate',str(out/'wizard-idle.png'),'--kind','character','--palette',str(game/'palettes/hood_staff_32_quick.json')],
    ['validate',str(out/'spell-panel.png'),'--size','160','128','--palette',str(work/'palette.json')],
    ['validate',str(out/'spell-slots.png'),'--size','72','24','--palette',str(work/'palette.json')],
    ['validate',str(out/'meadow-wave-preview.png'),'--size','640','1408','--palette',str(work/'palette.json')],
]
if not (out/'atlas/meadow_wave.png').is_file():
    commands.insert(0,['assemble',str(manifest),str(work/'tiles'),str(out/'atlas')])
logs = []
for args in commands:
    result = subprocess.run([sys.executable,str(pixel_art),*args],capture_output=True,text=True)
    logs.append(result.stdout + result.stderr)
    if result.returncode:
        print(logs[-1])
        raise SystemExit(result.returncode)
atlas_map = Image.open(out/'atlas/meadow_wave.png').convert('RGBA')
metadata = json.loads((out/'atlas/meadow_wave.sprite.json').read_text())
positions = {s['name'].split('_')[-1]:(s['x'],s['y']) for s in metadata['sprites']}
for j,row in enumerate(rows):
    for i,tile_id in enumerate(row):
        x,y = positions[tile_id]
        assert atlas_map.crop((x,y,x+16,y+16)).tobytes() == terrain.crop((i*16,j*16,i*16+16,j*16+16)).tobytes()
assert all(a in (0,255) for a in atlas.getchannel('A').get_flattened_data())
logs.append('Exact atlas reconstruction verified. Binary alpha, 32px character cell, locked (16,28) pivot.')
(work/'validation.txt').write_text('\n'.join(logs),encoding='utf-8')
for filename in ('meadow-terrain.png','distant-meadow.png','meadow-hedge.png','spell-panel.png','spell-slots.png'):
    shutil.copy2(out/filename,approved/filename)
print('\n'.join(logs))







