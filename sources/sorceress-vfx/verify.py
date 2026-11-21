"""Verify the exported PNGs and GIFs and package the finished assets."""

from hashlib import sha256
import json
from pathlib import Path
import struct
import sys
from zipfile import ZIP_DEFLATED, ZipFile
import zlib


def rgba_png(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    width, height, depth, color = struct.unpack_from(">IIBB", data, 16)
    assert (depth, color) == (8, 6), path
    offset = 8
    chunks = []
    while offset < len(data):
        size, kind = struct.unpack_from(">I4s", data, offset)
        chunk = data[offset + 8:offset + size + 8]
        assert zlib.crc32(kind + chunk) == struct.unpack_from(">I", data, offset + size + 8)[0], path
        if kind == b"IDAT":
            chunks.append(chunk)
        offset += size + 12
    filtered = zlib.decompress(b"".join(chunks))
    stride = width * 4
    assert len(filtered) == (stride + 1) * height, path
    pixels = bytearray()
    for y in range(height):
        start = y * (stride + 1)
        assert filtered[start] == 1, path
        row = bytearray(filtered[start + 1:start + 1 + stride])
        for i in range(4, stride):
            row[i] = (row[i] + row[i - 4]) & 255
        pixels.extend(row)
    return width, height, pixels


def gif_frames(path):
    data = path.read_bytes()
    assert data[:6] in (b"GIF87a", b"GIF89a"), path
    width, height, packed = struct.unpack_from("<HHB", data, 6)
    i = 13 + (3 * (2 << (packed & 7)) if packed & 128 else 0)
    delays = []
    delay = None
    while data[i] != 0x3B:
        marker = data[i]
        if marker == 0x21:
            if data[i + 1] == 0xF9:
                delay = struct.unpack_from("<H", data, i + 4)[0]
            i += 2
        else:
            assert marker == 0x2C, path
            palette = data[i + 9]
            i += 11 + (3 * (2 << (palette & 7)) if palette & 128 else 0)
            assert delay is not None, path
            delays.append(delay)
            delay = None
        while data[i]:
            i += data[i] + 1
        i += 1
    assert i == len(data) - 1, path
    return width, height, delays


def verify(folder):
    manifest = json.loads((folder / "unity-slicing.json").read_text(encoding="utf-8"))
    effects = manifest["effects"]
    assert len(effects) == len({item["name"] for item in effects}) == 30
    sheets = {item["sheet"] for item in effects}
    gifs = {item["gif"] for item in effects}
    assert sheets == {file.relative_to(folder).as_posix() for file in folder.glob("spritesheets/*/*.png")}
    assert gifs == {file.relative_to(folder).as_posix() for file in folder.glob("gifs/*/*.gif")}
    assert len(sheets) == len(gifs) == 30
    fingerprints = set()
    report = {}
    for item in effects:
        path = folder / item["sheet"]
        w, h, data = rgba_png(path)
        cw, ch = item["cell"]
        columns, rows, count = item["columns"], item["rows"], item["frameCount"]
        assert (w, h) == (columns * cw, rows * ch) and w <= 2048 and h <= 2048, path
        assert rows == (count + columns - 1) // columns, path
        px, py = item["pivotTopLeftPx"]
        assert 0 < px < cw and 0 < py < ch and item["pivotUnity"] == [px / cw, 1 - py / ch], path
        palette = {bytes.fromhex(hex_color[1:]) for hex_color in manifest["palettes"][item["tree"]]}
        colors = set()
        visible = []
        hashes = set()
        for frame in range(columns * rows):
            x, y = frame % columns * cw, frame // columns * ch
            start = (y * w + x) * 4
            cell = b"".join(data[start + j * w * 4:start + (j * w + cw) * 4] for j in range(ch))
            assert not any(cell[3:cw * 4:4]) and not any(cell[-cw * 4 + 3::4]), path
            assert not any(cell[3::cw * 4]) and not any(cell[cw * 4 - 1::cw * 4]), path
            if frame >= count or (frame == count - 1 and not item["loop"]):
                assert not any(cell), path
            if frame < count:
                hashes.add(sha256(cell).digest())
                visible.append(any(cell[3::4]))
            colors.update(cell[i:i + 3] for i in range(0, len(cell), 4) if cell[i + 3])
        assert colors and colors <= palette and len(hashes) >= 4 and visible[item["contactFrameIndex"]], path
        digest = sha256(path.read_bytes()).digest()
        assert digest not in fingerprints, path
        fingerprints.add(digest)
        gw, gh, delays = gif_frames(folder / item["gif"])
        expected = count if item["loop"] else count + 4
        assert (gw, gh) == (cw * 2, ch * 2) and len(delays) == expected and set(delays) == {5}, path
        report[item["name"]] = {"pngFrames": count, "gifFrames": len(delays), "distinctFrames": len(hashes)}
    assert (folder / "contact-sheet.png").stat().st_size > 0
    return report


if __name__ == "__main__":
    export, archive, review = map(Path, sys.argv[1:])
    results = verify(export)
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(json.dumps({"passed": True, "spells": results}, indent=2) + "\n", encoding="utf-8")
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for file in sorted(export.rglob("*")):
            if file.is_file():
                bundle.write(file, file.relative_to(export).as_posix())
    with ZipFile(archive, "r") as bundle:
        assert bundle.testzip() is None
        assert len(bundle.namelist()) == 65
    print(f"Verified {len(results)} spells, {sum(row['pngFrames'] for row in results.values())} PNG frames, and ZIP integrity.")
