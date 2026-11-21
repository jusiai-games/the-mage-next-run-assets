"""Rebuild the meadow color pass from the original exports and current Unity PNGs."""

import hashlib
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw, ImageSequence

VERSION = sys.argv[1] if len(sys.argv) > 1 else "v2"
if VERSION not in {"v2", "v3"}:
    raise ValueError("expected color pass v2 or v3")
WORK = Path(__file__).resolve().parent.with_name("color-pass-" + VERSION)
GAME = WORK.parents[1]
PRODUCTION = GAME.parent / "pixel-art-production"
UNITY = GAME.parent / "the-mage-next-run"
OLD = GAME / "exports"
OUT = OLD / ("meadow-color-" + VERSION)
BUNDLE = OUT / ("meadow-color-" + VERSION + "-unity.zip")
TOOL_DIR = PRODUCTION / "plugins/pixel-art-production/scripts/pixel-art"
sys.path.insert(0, str(TOOL_DIR))
from color_space import oklch, to_srgb
from color_style import hex_color, histogram, recolor, write_json
from style_review import rgb


def colors(value):
    return [rgb("#" + item) for item in value.split()]


def map_colors(old, new):
    return dict(zip(colors(old), colors(new), strict=True))


def cli(*args, expected=(0,)):
    result = subprocess.run([sys.executable, str(TOOL_DIR / "pixel_art.py"), *map(str, args)])
    if result.returncode not in expected:
        raise RuntimeError(f"{args[0]} failed ({result.returncode})")
    return result.returncode


def ramp(reference, material, base, sources):
    folder = WORK / (reference + "-ramp")
    if not folder.exists():
        cli("color-ramp", GAME / "styles/reference-colors-v1/profile.json", folder,
            "--reference", reference, "--material", material, "--base", base)
    return dict(zip(colors(sources), map(rgb, json.loads((folder / "palette.json").read_text())), strict=True))


def rgb_shift(old, values):
    result = {}
    for source, (light, chroma, hue) in zip(colors(old), values, strict=True):
        result[source] = to_srgb(light, chroma, hue)
    return result


def rgba(path):
    with Image.open(path) as image:
        return image.convert("RGBA")


def save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_pixels(before, after, palette=None):
    assert before.size == after.size
    assert before.getchannel("A").tobytes() == after.getchannel("A").tobytes()
    if palette is not None:
        used = {pixel[:3] for pixel in before.getdata() if pixel[3]}
        assert used <= palette.keys(), [hex_color(color) for color in sorted(used - palette.keys())]
        assert len({palette[color] for color in used}) == len(used)
        for source, target in zip(before.getdata(), after.getdata(), strict=True):
            assert target[:3] == (palette[source[:3]] if source[3] else source[:3])


def relink_sidecar(source, target, metadata=None):
    if metadata is None:
        metadata = json.loads(source.with_suffix(".sprite.json").read_text(encoding="utf-8-sig"))
    assert metadata["sha256"] == hash_file(source)
    metadata = {**metadata, "sha256": hash_file(target)}
    write_json(target.with_suffix(".sprite.json"), metadata)


def preview(old, maps):
    scene = old.resize((160, 352), Image.Resampling.NEAREST)
    mobile = OLD / "meadow-wave-mobile"
    distant = rgba(mobile / "distant-meadow.png")
    hedge = rgba(mobile / "meadow-hedge.png")
    global_map, far_map, hedge_map = maps
    output = recolor(scene, global_map)
    for y in range(85):
        for x in range(160):
            pixel = scene.getpixel((x, y))
            if y >= 66 and pixel == hedge.getpixel((x, y - 66)) and pixel[3]:
                output.putpixel((x, y), (*hedge_map[pixel[:3]], pixel[3]))
            elif y < 80 and pixel == distant.getpixel((x, y)) and pixel[3]:
                output.putpixel((x, y), (*far_map[pixel[:3]], pixel[3]))
    return output.resize(old.size, Image.Resampling.NEAREST)


def compare_scene(before, after):
    images = [source.resize((320, 704), Image.Resampling.NEAREST) for source in (before, after)]
    canvas = Image.new("RGB", (664, 742), "#E9E7DB")
    draw = ImageDraw.Draw(canvas)
    labels = ("Original", "Meadow color pass") if VERSION == "v2" else ("v2", "v3")
    for left, image, label in zip((8, 336), images, labels, strict=True):
        draw.text((left, 9), label, fill="#272639", font_size=15)
        canvas.paste(image, (left, 30))
    return canvas


def recolor_gif(source, target, mapping):
    with Image.open(source) as animation:
        frames, durations = [], []
        loop = animation.info.get("loop", 0)
        for frame in ImageSequence.Iterator(animation):
            durations.append(frame.info.get("duration", 100))
            frames.append(recolor(frame.convert("RGBA"), mapping))
    frames[0].save(target, save_all=True, append_images=frames[1:], duration=durations,
                   loop=loop, optimize=False)
    with Image.open(target) as result:
        assert result.size == frames[0].size
        assert sum(frame.info.get("duration", 0) for frame in ImageSequence.Iterator(result)) == sum(durations)


def check_transition_maps(mapping, production):
    source_roots = {
        "hood-staff-quick-state-transitions.json": production / "hood-staff-32-quick-cast",
        "slime32-v7-state-transitions.json": production / "meadow_slime_combat32_v7",
    }
    for filename, root in source_roots.items():
        original = json.loads((GAME / filename).read_text(encoding="utf-8-sig"))
        frames = {}
        frame_root = WORK / Path(filename).stem
        frame_root.mkdir(exist_ok=True)
        for sidecar in root.rglob("*.sprite.json"):
            metadata = json.loads(sidecar.read_text(encoding="utf-8-sig"))
            cell = metadata["cell"]
            sheet = rgba(sidecar.with_name(sidecar.name.replace(".sprite.json", ".png")))
            for sprite in metadata["sprites"]:
                name = sprite["name"] + ".png"
                x, y = sprite["x"], sprite["y"]
                frames[name] = frame_root / name
                save(sheet.crop((x, y, x + cell, y + cell)), frames[name])
        for edge in original["edges"]:
            for key in ("from", "to"):
                edge[key] = frames[Path(edge[key]).name].relative_to(WORK).as_posix()
        for key in ("effect_colors", "outline_colors"):
            if key in original:
                original[key] = [hex_color(mapping[rgb(value)]) for value in original[key]]
        source_palette = json.loads((GAME / original["palette"]).read_text(encoding="utf-8-sig"))
        palette_path = frame_root / "palette.json"
        write_json(palette_path, [hex_color(mapping[rgb(value)]) for value in source_palette])
        original["palette"] = palette_path.relative_to(WORK).as_posix()
        path = WORK / filename
        write_json(path, original)
        cli("review-transitions", path, frame_root / "review", expected=(0, 1))
        report = json.loads((frame_root / "review/report.json").read_text())
        yield filename, report


def package_review():
    profile = OUT / "color-profile"
    if not profile.exists():
        cli("color-build", WORK / "color-sources.json", profile)
    files = ("README.md", "meadow-before-after.png", "color-mapping.json", "palette.json",
             "runtime-coverage.json", "transition-reports.json")
    with ZipFile(BUNDLE, "a", ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(OUT / name, f"ColorPassDocs/{name}")
        for folder in ("exports", "color-profile"):
            for file in sorted((OUT / folder).rglob("*")):
                if file.is_file():
                    archive.write(file, "ColorPassDocs/" + file.relative_to(OUT).as_posix())


def main():
    wizard = ramp("hood_wizard", "robe", "#4D507C", "28283F 393B5B 454568 505276")
    wizard |= map_colors("222034 4F3333 6A4757 8B6755 E4AA84 F8CFAB",
                         "242338 503638 704B5D 926F57 E5AD88 F9D4B4")
    slime = ramp("meadow_slime", "gel", "#5D9D76" if VERSION == "v2" else "#55A373",
                 "48643C 638752 86A866 BEDD90")
    slime |= map_colors("23361E", "1D3A30")
    terrain = rgb_shift("68865C 749466 7CA06E 8FAF74 99B77D AAC586 D3DAA5 91C7C0 D88475", [
        (.595, .055, 124), (.645, .062, 123), (.678, .064, 119), (.735, .065, 115),
        (.759, .064, 115), (.8, .067, 113), (.887, .055, 103), (.805, .041, 200), (.71, .088, 40),
    ])
    far = rgb_shift("68865C 749466 7CA06E 8FAF74 99B77D AAC586 D3DAA5 91C7C0", [
        (.635, .043, 154), (.668, .046, 150), (.700, .045, 146), (.745, .047, 145),
        (.767, .046, 143), (.802, .043, 139), (.895, .034, 100), (.837, .034, 208),
    ])
    hedge = rgb_shift("68865C 749466 7CA06E 8FAF74", [
        (.596, .057, 137), (.635, .058, 136), (.671, .064, 134), (.72, .062, 132),
    ])
    effects = map_colors("367CB0 589DC8 78CBF4 ADE9FF F0FCFF", "3D76B8 619CDD 84CCFC B6E9FF F2FAFF")
    accents = map_colors("EAB853 354568", "DEB66F 384767")
    if VERSION == "v3":
        terrain = rgb_shift("68865C 749466 7CA06E 8FAF74 99B77D AAC586 D3DAA5 91C7C0 D88475", [
            (.585, .077, 133), (.633, .083, 130), (.677, .087, 127), (.730, .094, 123),
            (.758, .092, 122), (.802, .090, 119), (.888, .075, 106), (.827, .067, 208), (.716, .110, 36),
        ])
        far = rgb_shift("68865C 749466 7CA06E 8FAF74 99B77D AAC586 D3DAA5 91C7C0", [
            (.620, .058, 152), (.660, .065, 150), (.704, .070, 147), (.750, .068, 145),
            (.776, .067, 142), (.815, .062, 137), (.916, .055, 99), (.837, .070, 219),
        ])
        hedge = rgb_shift("68865C 749466 7CA06E 8FAF74", [
            (.575, .075, 142), (.622, .083, 140), (.670, .087, 136), (.718, .086, 133),
        ])
        accents = map_colors("EAB853 354568", "E6B961 384767")
    palette = wizard | slime | terrain | effects | accents
    assert len(set(palette.values())) == len(palette)
    for old, group in (("23361E 48643C 638752 86A866 BEDD90", slime),
                       ("222034 28283F 393B5B 454568 505276", wizard),
                       ("68865C 749466 7CA06E 8FAF74 99B77D AAC586 D3DAA5", terrain),
                       ("367CB0 589DC8 78CBF4 ADE9FF F0FCFF", effects)):
        levels = [oklch(group[color])[0] for color in colors(old)]
        assert all(left < right for left, right in zip(levels, levels[1:]))
    production = OUT / "exports"
    production.mkdir(parents=True)
    by_hash = {}
    previous_hashes = {}
    source_files = [
        path for path in OLD.rglob("*")
        if path.is_file() and not path.relative_to(OLD).parts[0].startswith("meadow-color-")
    ]
    for source in sorted(source_files):
        relative = source.relative_to(OLD)
        target = production / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == ".png":
            before = rgba(source)
            selected = far if source.name == "distant-meadow.png" else hedge if source.name == "meadow-hedge.png" else palette
            if source.name == "meadow-wave-preview.png":
                after = preview(before, (palette, far, hedge))
                comparison = before if VERSION == "v2" else rgba(
                    OLD / "meadow-color-v2/exports/meadow-wave-mobile/meadow-wave-preview.png"
                )
                save(compare_scene(comparison, after), OUT / "meadow-before-after.png")
                matching_pixels(before, after)
            else:
                after = recolor(before, selected)
                matching_pixels(before, after, None if source.name == "slime-preview.png" else selected)
            assert before.tobytes() != after.tobytes()
            save(after, target)
            by_hash[hash_file(source)] = target
            if VERSION == "v3":
                previous = OLD / "meadow-color-v2/exports" / relative
                if previous.is_file():
                    previous_hashes[hash_file(previous)] = target
        elif source.suffix == ".gif":
            recolor_gif(source, target, palette)
        elif source.suffix == ".zip" or source.name.endswith(".sprite.json") or "transition-review" in relative.parts:
            continue
        else:
            target.write_bytes(source.read_bytes())
    for source in (file for file in source_files if file.name.endswith(".sprite.json")):
        original_png = source.with_name(source.name.replace(".sprite.json", ".png"))
        relink_sidecar(original_png, production / original_png.relative_to(OLD))

    source_package = OLD / "meadow-slime-combat-32-v7.zip"
    slime_export = production / "meadow_slime_combat32_v7"
    with ZipFile(source_package) as before, ZipFile(production / source_package.name, "w", ZIP_DEFLATED) as after:
        for name in before.namelist():
            if name.startswith("frames/"):
                with Image.open(BytesIO(before.read(name))) as source:
                    original = source.convert("RGBA")
                corrected = recolor(original, palette)
                matching_pixels(original, corrected, palette)
                data = BytesIO()
                corrected.save(data, format="PNG")
                after.writestr(name, data.getvalue())
            else:
                after.write(slime_export / name, name)
    runtime = []
    with ZipFile(BUNDLE, "w", ZIP_DEFLATED) as archive:
        for source in sorted((UNITY / "Assets/Art/PixelArt").rglob("*.png")):
            relative = source.relative_to(UNITY)
            source_hash = hash_file(source)
            target = (by_hash | previous_hashes)[source_hash]
            archive.write(target, relative.as_posix())
            metadata = json.loads(source.with_suffix(".sprite.json").read_text(encoding="utf-8-sig"))
            assert metadata["sha256"] == source_hash
            archive.writestr(relative.with_suffix(".sprite.json").as_posix(),
                             json.dumps({**metadata, "sha256": hash_file(target)}, indent=2) + "\n")
            runtime.append({"path": relative.as_posix(), "before": source_hash, "after": hash_file(target)})
    assert len(runtime) == 15
    write_json(OUT / "runtime-coverage.json", runtime)
    write_json(OUT / "color-mapping.json", {
        name: {hex_color(old): hex_color(new) for old, new in mapping.items()}
        for name, mapping in (("wizard", wizard), ("slime", slime), ("terrain", terrain), ("distant", far),
                              ("hedge", hedge), ("lightning", effects), ("accents_shadow", accents))
    })
    exact_palette = set()
    for target in by_hash.values():
        if "preview" not in target.stem:
            exact_palette.update(pixel[:3] for pixel in rgba(target).getdata() if pixel[3])
    write_json(OUT / "palette.json", sorted(map(hex_color, exact_palette)))
    reports = dict(check_transition_maps(palette, production))
    write_json(OUT / "transition-reports.json", reports)
    package_review()
    print(f"{len(by_hash)} exported PNGs, {len(runtime)} runtime replacements")


if __name__ == "__main__":
    main()
