from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
import json, subprocess, sys, shutil, zipfile

game = Path(__file__).resolve().parents[1]
pixel_art = game.parent / "pixel-art-production/tools/pixel-art/pixel_art.py"
asset = "meadow_slime_combat32_v7"
source = game / "sources" / asset / "01"
work = game / "work" / asset
approved = game / "approved" / asset
exports = game / "exports/v1/meadow-slime"
for directory in (work, approved, exports):
    directory.mkdir(parents=True, exist_ok=True)

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

clips = {}
for state, durations, loop in (
    ("attack", [65, 105, 105, 80, 85, 70], False),
    ("idle", [230, 240, 220], True),
    ("hurt", [55, 80, 70, 65], False),
    ("death", [85, 90, 110, 105], False),
):
    frames = [Image.open(path).convert("RGBA") for path in sorted((source / state).glob("*.png"))]
    assert len(frames) == len(durations), state
    clips[state] = (frames, durations, loop)
rest = clips["idle"][0][0]

# Keep the facial features and lighting anchored to the same pose during the hop.
box = rest.getbbox()
body = rest.crop(box)
width, height = body.size
def hop_pose(width_delta, height_delta, lift):
    pose = Image.new("RGBA", rest.size)
    size = (width + width_delta, height + height_delta)
    shape = body.resize(size, Image.Resampling.NEAREST)
    pose.paste(shape, (box[0] - (width_delta + 1)//2, box[3] - lift - size[1]))
    return pose

hop = [
    (1,-1,0), (2,-2,0), (1,-1,0),
    (0,1,1), (-1,2,3), (-1,2,5),
    (-1,1,6), (0,0,6), (0,0,5),
    (0,0,4), (1,-1,2), (1,-1,1),
    (2,-2,0), (3,-3,0), (2,-2,0), (1,-1,0),
]
advance = [rest, *(hop_pose(*pose) for pose in hop), rest]
advance_timing = [40,30,30,20,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
assert sum(advance_timing) == 540
clips["advance"] = (advance, advance_timing, True)

shadow = Image.new("RGBA",(32,32))
draw = ImageDraw.Draw(shadow)
shadow_color = ImageColor.getrgb("#354568")
draw.ellipse((6,24,28,31), fill=(*shadow_color,56))
draw.ellipse((8,25,26,30), fill=(*shadow_color,93))
draw.ellipse((11,26,23,29), fill=(*shadow_color,118))
shadow.save(approved / "meadow_slime_shadow.png")
shadow.save(exports / "meadow_slime_shadow.png")

def run(*args):
    subprocess.run([sys.executable, str(pixel_art), *map(str,args)],check=True)

def frame_name(state, i):
    return f"slime32_{state}_left_{i:02}.png"

for state, (frames, _, _) in clips.items():
    name = "slime32_" + state
    raw = source / state
    raw.mkdir(exist_ok=True)
    for i, im in enumerate(frames):
        im.save(raw / frame_name(state,i))
    manifest = game / "manifests" / f"{name}_v7.json"
    write_json(manifest, {"kind":"character","name":name,"directions":["left"],"frames_per_direction":len(frames),
                          "palette":"../palettes/meadow_slime_attack.json"})
    review = work / (state + "-review")
    run("review",manifest,game/"styles/default.json",raw,review)
    shutil.copytree(review/"frames", approved/state,dirs_exist_ok=True)
    run("assemble",manifest,approved/state,exports/state)

edges=[]
def add(src,i,dst,j,mode="pose",contact=4):
    edges.append({"id":f"{src}_{i}_to_{dst}_{j}",
                  "from":str((approved/src/frame_name(src,i)).relative_to(game)).replace("\\","/"),
                  "to":str((approved/dst/frame_name(dst,j)).relative_to(game)).replace("\\","/"),
                  "mode":mode, "limits":{"max_contact_shift":contact}})
add("advance",len(advance)-1,"advance",0,"exact")
add("advance",len(advance)-1,"attack",0,"exact")
for i in range(len(advance)-1):
    add("advance",i,"advance",i+1,contact=2)
add("attack",5,"idle",0,"exact")
add("idle",2,"idle",0,"exact")
add("hurt",3,"advance",0,"exact")
add("hurt",3,"idle",0,"exact")
for state in ("advance","attack","idle"):
    for i, frame in enumerate(clips[state][0]):
        contact = max(4, abs(28 - frame.getbbox()[3]) + 2)
        add(state,i,"hurt",0,contact=contact)
        add(state,i,"death",0,contact=contact)
add("hurt",0,"death",0)
add("hurt",1,"death",0)
add("hurt",2,"death",0)
transition_path = game / "slime32-v7-state-transitions.json"
write_json(transition_path, {"palette":"palettes/meadow_slime_attack.json","outline_colors":["#23361E","#48643C"],
                             "limits":{"min_overlap":0.3,"max_color_shift":0.42,"max_cluster_shift":0.23},"edges":edges})
run("review-transitions",transition_path,work/"transitions")
write_json(exports/"animation.json",{
    "frame_size":[32,32],"pivot_top_left":[16,28],"ppu":32,"facing":"front_left",
    "shadow":{"file":"meadow_slime_shadow.png","pivot_top_left":[16,28],"layer":"below body"},
    "clips":{state:{"sheet":f"{state}/slime32_{state}.png","duration_ms":durations,"loop":loop}
             for state,(_,durations,loop) in clips.items()},
    "attack_impact":{"zero_based_frame":3,"time_ms":275},
    "death_end":{"hide_body":True,"hide_shadow":True},
})
terrain = Image.open(game/"approved/meadow_wave_mobile/meadow-terrain.png").convert("RGBA")
print("terrain", terrain.size)
tile = Image.open(game/"work/meadow_wave/mobile/tiles/meadow_wave_t031.png").convert("RGBA")
scene = Image.new("RGBA",(64,40),"#879A5A")
for y in range(0,40,16):
    for x in range(0,64,16):
        scene.alpha_composite(tile,(x,y))
scale = 4
gallery = Image.new("RGB",(640,380),"#222d24")
font = ImageFont.load_default(size=15)
for col,(state,i,label) in enumerate((("advance",7,"ADVANCE"),("attack",3,"ATTACK"),("idle",0,"POST-ATTACK IDLE"),
                                      ("hurt",1,"HURT"),("death",2,"DEATH"),("death",3,"DISSIPATE"))):
    x,y = (col % 3)*210, (col // 3)*188
    cell = scene.crop((10,0,54,39))
    cell.alpha_composite(shadow,(6,3))
    cell.alpha_composite(clips[state][0][i],(6,3))
    gallery.paste(cell.resize((176,156),Image.Resampling.NEAREST),(x+20,y+8))
    ImageDraw.Draw(gallery).text((x+20,y+167),label,fill="#eef3de",font=font)
gallery.save(exports/"slime-preview.png")
movie, delays = [], []
for state, indices in (("advance",range(len(advance))),("attack",range(6)),("idle",range(3)),("hurt",range(4)),("death",range(4))):
    frames,durations,_ = clips[state]
    for i in indices:
        bg = scene.copy()
        active_shadow = shadow.copy()
        if state=="death":
            active_shadow.putalpha(active_shadow.getchannel("A").point(lambda p: p * [1,.78,.45,.17][i]))
        bg.alpha_composite(active_shadow,(16,4))
        bg.alpha_composite(frames[i],(16,4))
        preview = bg.resize((256,160),Image.Resampling.NEAREST).convert("RGB")
        ImageDraw.Draw(preview).text((8,7),state.upper(),fill="#ffffff",stroke_width=2,stroke_fill="#273629",font=font)
        movie.append(preview)
        delays.append(durations[i])
movie.append(scene.resize((256,160),Image.Resampling.NEAREST).convert("RGB"))
delays.append(300)
movie[0].save(exports/"slime-animation.gif",save_all=True,append_images=movie[1:],duration=delays,loop=0,disposal=2,optimize=False)

hop_preview = []
for frame in advance:
    bg = scene.copy()
    bg.alpha_composite(shadow,(16,4))
    bg.alpha_composite(frame,(16,4))
    hop_preview.append(bg.resize((256,160),Image.Resampling.NEAREST).convert("RGB"))
hop_preview[0].save(exports/"slime-hop.gif",save_all=True,append_images=hop_preview[1:],
                    duration=advance_timing,loop=0,disposal=2,optimize=False)

shutil.copyfile(game/"jobs/meadow_slime_combat32_v7.md", exports/"README.md")
archive=game/"exports/meadow-slime-combat-32-v7.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for path in sorted(exports.rglob("*")):
        if path.is_file(): z.write(path,path.relative_to(exports))
    for path in sorted(approved.glob("*/*.png")):
        z.write(path,Path("frames")/path.relative_to(approved))
print(archive.resolve())










