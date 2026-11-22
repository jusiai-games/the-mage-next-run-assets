from pathlib import Path
import json

from PIL import Image, ImageDraw


package = Path(__file__).resolve().parents[3] / "exports/v1/meadow-tilemap"
home = package / "chapter-01-home"
preview = Image.open(home / "preview.png").convert("RGBA")
assert Image.open(home / "background.png").size == preview.size

# Crop the original button along its beveled frame.
left, top, right, bottom = 227, 1426, 743, 1529
button = preview.crop((left, top, right, bottom))
mask = Image.new("L", button.size)
ImageDraw.Draw(mask).polygon(
    [(13,0),(502,0),(515,12),(515,90),(502,102),(13,102),(0,90),(0,12)],
    fill=255,
)
button.putalpha(mask)
button.save(home / "button-game-start.png")

home_manifest = dict(
    canvas_px=list(preview.size),
    background="background.png",
    button=dict(file="button-game-start.png", top_left_px=[left, top],
                size_px=list(button.size), label="게임 시작"),
    title="주문 넣고 갑니다",
    subtitle="Spells to Go",
    chapter="CHAPTER 1",
)
(home / "manifest.json").write_text(
    json.dumps(home_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

stages = package / "stages"
manifest_path = stages / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
button_rect = (34,289,126,317)
manifest["split_ui"] = dict(
    foreground_without_button="stage-start-title.png",
    shared_button="button-battle-start.png",
    button_top_left_px=list(button_rect[:2]), button_size_px=[92,28],
)
for stage in manifest["stages"]:
    directory = stages / stage["directory"]
    foreground = Image.open(directory / "stage-start-foreground.png").convert("RGBA")
    button = foreground.crop(button_rect)
    title = foreground.copy()
    for y in range(button.height):
        shade = foreground.getpixel((0,button_rect[1]+y))
        for x in range(button.width):
            if button.getpixel((x,y)) == shade:
                button.putpixel((x,y),(0,0,0,0))
        title.paste(shade,(button_rect[0],button_rect[1]+y,button_rect[2],button_rect[1]+y+1))
    shared = stages / "button-battle-start.png"
    if stage["number"] == 1:
        button.save(shared)
    else:
        assert button.tobytes() == Image.open(shared).tobytes()
    title.save(directory / "stage-start-title.png")
    restored = title.copy()
    restored.paste(button,button_rect[:2],button.getchannel("A").point(lambda a: 255 if a else 0))
    assert restored.tobytes() == foreground.tobytes()

manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
