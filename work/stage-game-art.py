"""Prepare the visual changes for the Unity project without writing into it."""

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from runpy import run_path

from PIL import Image, ImageColor, ImageDraw

ART = run_path(str(Path(__file__).with_name("polish-exports.py")))
PIXEL_ART = Path("Assets/Art/PixelArt")
SCREENS = Path("Assets/Scripts/Screens")
RESOURCES = Path("Assets/Resources/SpellsToGo")


def stage_text(project, stage, file, source, replacement):
    text = (project / file).read_text(encoding="utf-8")
    if text.count(source) != 1:
        raise ValueError(f"Unexpected code in {file}")
    target = stage / file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.replace(source, replacement), encoding="utf-8")


def card_sprites(stage, exports):
    package = exports / "spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites"
    target = stage / RESOURCES
    target.mkdir(parents=True)
    panel_meta = Path("exports/v1/spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites/panel.png.meta")
    for name, color, icon in [
        ("Fire", "#ef986b", [(16, 2), (19, 5), (18, 8), (14, 8), (13, 5), (15, 6)]),
        ("Wind", "#93dab2", [(13, 6), (16, 3), (20, 3), (18, 5), (20, 6), (17, 8)]),
        ("Ice", "#a7e4f1", [(16, 2), (19, 5), (16, 9), (13, 5)]),
        ("Lightning", "#f2cd78", [(17, 2), (14, 6), (16, 6), (15, 9), (20, 4), (17, 4)]),
    ]:
        image = Image.new("RGBA", (34, 44))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 33, 43), radius=3, fill="#151726")
        draw.rounded_rectangle((1, 1, 32, 42), radius=2, fill=color)
        draw.rounded_rectangle((2, 2, 31, 41), radius=2, fill="#383652")
        draw.rectangle((3, 10, 30, 29), fill="#23283e")
        draw.rectangle((3, 31, 30, 40), fill="#1a1d30")
        draw.line((4, 30, 29, 30), "#565372")
        draw.line((4, 5, 10, 5), color)
        draw.line((22, 5, 29, 5), color)
        draw.polygon(icon, fill=color)
        for point in [(2, 2), (31, 2), (2, 41), (31, 41)]:
            draw.point(point, "#fff0c9")
        image.save(target / f"Card{name}.png")
    shutil.copyfile(package / "panel.png", target / "DialogPanel.png")
    for file in target.glob("*.png"):
        guid = hashlib.sha256(str(file.relative_to(stage)).replace("\\", "/").encode()).hexdigest()[:32]
        meta = re.sub(r"(?m)^guid: \w+", f"guid: {guid}", panel_meta.read_text(encoding="utf-8"))
        if file.stem.startswith("Card"):
            meta = meta.replace("{x: 12, y: 12, z: 12, w: 12}", "{x: 0, y: 0, z: 0, w: 0}")
        file.with_suffix(".png.meta").write_text(meta, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("exports", type=Path)
    parser.add_argument("stage", type=Path)
    args = parser.parse_args()
    project, exports, stage = args.project, args.exports, args.stage
    stage.mkdir(parents=True, exist_ok=False)

    base = ART["WORLD"]
    mapping = json.loads(Path("palettes/meadow-color-v2-mapping.json").read_text(encoding="utf-8"))
    updated_v2 = {}
    for role in ("wizard", "slime", "lightning", "accents_shadow"):
        for old, v2 in mapping[role].items():
            rgb = ImageColor.getrgb(old)
            if rgb in base:
                updated_v2[ImageColor.getrgb(v2)] = base[rgb]

    title = ART["ramp"]("9bc6e1 dff1fa", "95b6cd e7e6d9")
    for source in (project / PIXEL_ART).rglob("*.png"):
        relative = source.relative_to(project)
        dest = stage / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        palette = {**base, **updated_v2, **title}
        # Keep the live atlas and its extra rows. It differs from the Tiled export.
        if not ART["recolor_png"](source, dest, palette):
            continue
        sidecar = relative.with_suffix(".sprite.json")
        if not (project / sidecar).is_file():
            continue
        original = (project / sidecar).read_text(encoding="utf-8")
        data = json.loads(original)
        assert Image.open(dest).size == (data["width"], data["height"])
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        (stage / sidecar).write_text(original.replace(data["sha256"], digest, 1), encoding="utf-8")

    card_sprites(stage, exports)
    stage_text(project, stage, Path("Assets/Editor/PixelArtImporter.cs"),
               """            var sidecar = Path.ChangeExtension(assetPath, ".sprite.json");
            context?.DependsOnSourceAsset(sidecar);
            try""",
               """            var sidecar = Path.ChangeExtension(assetPath, ".sprite.json");
            context?.DependsOnSourceAsset(sidecar);
            if (!File.Exists(sidecar))
                return;
            try""")
    stage_text(project, stage, SCREENS / "CardView.cs",
               """            _color = ElementPalette.Get(card.Spell.Element);
            _background.color = _color;""",
               """            var face = ScreenArt.Card(card.Spell.Element);
            _background.sprite = face;
            _color = face == null ? ElementPalette.Get(card.Spell.Element) : new Color32(225, 229, 240, 255);
            _background.color = _color;
            _numberLabel.color = ScreenArt.Ink;
            _nameLabel.color = ScreenArt.Ink;""")
    stage_text(project, stage, SCREENS / "PlanningController.cs",
               """            _wave = wave;""",
               """            _wave = wave;
            ScreenArt.Frame(_detailPanel);
            ScreenArt.Frame(_confirmPanel);
            ScreenArt.Outline(_sumLabel);
            ScreenArt.Outline(_bonusLabel);
            ScreenArt.Outline(_sacrificeLabel);""")
    stage_text(project, stage, SCREENS / "GameController.cs",
               """            _planning.Bind(ComparisonPlay.MeleeWave);""",
               """            _planning.Bind(ComparisonPlay.MeleeWave);
            ScreenArt.Frame(_resultPanel);
            ScreenArt.Outline(_resultBanner);
            ScreenArt.Outline(_waveClearLabel.GetComponent<Text>());
            ScreenArt.Outline(_gameStartScreen.transform.Find("Canvas/StageNameLabel")?.GetComponent<Text>());
            ScreenArt.PrimaryButton(_startGameButton);
            ScreenArt.PrimaryButton(_startBattleButton);
            ScreenArt.PrimaryButton(_startWaveButton);""")
    shutil.copyfile(Path(__file__).with_name("ScreenArt.cs"), stage / SCREENS / "ScreenArt.cs")


if __name__ == "__main__":
    main()
