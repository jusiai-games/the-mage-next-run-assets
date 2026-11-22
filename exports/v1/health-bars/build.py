"""머리 위 체력바 PNG, 매니페스트, 미리보기를 만든다.

실행: py exports/v1/health-bars/build.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
NEAREST = Image.Resampling.NEAREST

W, H = 20, 4            # 테두리 포함 바 크기
INNER = (1, 1, 18, 2)   # 채움 영역 x, y, w, h
GAP = 2                 # 머리 꼭대기와 바 아래 사이

OUTLINE = "#222034"
TRACK = ("#393B5B", "#28283F")  # 위/아래 줄
FILL = ("#EC6942", "#A74739")
CHIP = ("#FFD78F", "#FFAD54")


def frame():
    image = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W - 1, H - 1), fill=OUTLINE)
    x, y, w, h = INNER
    for row, color in enumerate(TRACK):
        draw.line((x, y + row, x + w - 1, y + row), fill=color)
    for corner in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)):
        image.putpixel(corner, (0, 0, 0, 0))
    return image


def bar(colors):
    _, _, w, h = INNER
    image = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(image)
    for row, color in enumerate(colors):
        draw.line((0, row, w - 1, row), fill=color)
    return image


def composed(hp, chip=None):
    """hp, chip은 0~1. chip은 방금 깎인 구간까지의 비율."""
    image = frame()
    x, y, w, _ = INNER
    if chip is not None:
        width = round(w * chip)
        if width:
            image.alpha_composite(bar(CHIP).crop((0, 0, width, 2)), (x, y))
    width = max(1, round(w * hp)) if hp > 0 else 0
    if width:
        image.alpha_composite(bar(FILL).crop((0, 0, width, 2)), (x, y))
    return image


def first_frame(path, cell=32):
    with Image.open(path) as sheet:
        return sheet.convert("RGBA").crop((0, 0, cell, cell))


def anchor(sprite, pivot=(16, 28)):
    top = sprite.getbbox()[1]
    return [-W // 2, -(pivot[1] - top) - GAP - H]


def preview(wizard, slime, offsets):
    detailed = V1 / "meadow-wave-mobile/detailed"
    scene = Image.new("RGBA", (160, 224))
    for name, origin in (("mountains.png", (0, 0)), ("foothills.png", (0, 55)), ("battlefield.png", (0, 80))):
        with Image.open(detailed / "stage-01" / name) as layer:
            scene.alpha_composite(layer.convert("RGBA"), origin)
    scene = scene.crop((0, 104, 160, 168))

    feet_wizard, feet_slime = (24, 153 - 104), (129, 153 - 104)
    scene.alpha_composite(wizard, (feet_wizard[0] - 16, feet_wizard[1] - 28))
    scale = 0.75
    small = slime.resize((round(32 * scale), round(32 * scale)), NEAREST)
    scene.alpha_composite(small, (feet_slime[0] - round(16 * scale), feet_slime[1] - round(28 * scale)))

    wx, wy = offsets["wizard"]
    sx, sy = offsets["slime"]
    scene.alpha_composite(composed(1.0), (feet_wizard[0] + wx, feet_wizard[1] + wy))
    scene.alpha_composite(composed(0.4, chip=0.65), (feet_slime[0] + sx, feet_slime[1] + round(sy * scale)))

    states = Image.new("RGBA", (160, 20), "#212535")
    for index, (hp, chip) in enumerate(((1.0, None), (0.65, None), (0.4, 0.65), (0.15, None), (0.0, None))):
        states.alpha_composite(composed(hp, chip), (8 + index * 30, 8))

    out = Image.new("RGBA", (160, 84))
    out.alpha_composite(scene, (0, 0))
    out.alpha_composite(states, (0, 64))
    return out.resize((out.width * 4, out.height * 4), NEAREST)


def main():
    frame().save(HERE / "hp-frame.png")
    bar(FILL).save(HERE / "hp-fill.png")
    bar(CHIP).save(HERE / "hp-chip.png")

    wizard = first_frame(V1 / "wizard/idle/hood_staff_idle.png")
    slime = first_frame(V1 / "meadow-slime/idle/slime32_idle.png")
    offsets = {"wizard": anchor(wizard), "slime": anchor(slime)}

    manifest = {
        "pixelsPerUnit": 32,
        "filter": "Point",
        "barSizePx": [W, H],
        "files": {"frame": "hp-frame.png", "fill": "hp-fill.png", "chip": "hp-chip.png"},
        "fillOriginPx": INNER[:2],
        "fillSizePx": INNER[2:],
        "fillRule": "채움 너비 = round(18 × 현재체력/최대체력). 체력이 0보다 크면 최소 1px.",
        "barTopLeftFromFeetPx": {
            "wizard": offsets["wizard"],
            "slime": offsets["slime"],
            "note": "원본 32px 셀 기준. 표시 배율이 있는 캐릭터는 y 오프셋에만 배율을 곱하고 바는 1배로 그린다.",
        },
        "timing": {
            "chipHoldMs": 350,
            "chipDrainMs": 250,
            "hideWhenFullForEnemies": True,
            "hideAfterDeathMs": 0,
        },
        "colors": {"outline": OUTLINE, "track": list(TRACK), "fill": list(FILL), "chip": list(CHIP)},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    preview(wizard, slime, offsets).save(HERE / "preview.png", optimize=True)


if __name__ == "__main__":
    main()
