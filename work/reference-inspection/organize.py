from collections import Counter
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import csv
import hashlib
import json
import os
import re

from PIL import Image


def pairs(rows):
    return dict(line.split(":", 1) for line in rows.split())


controls = {
    "button": ("버튼", "기본-버튼"), "icon_button": ("버튼", "아이콘-버튼"),
    "wide_button": ("버튼", "넓은-버튼"), "slot": ("카드와-슬롯", "정사각-슬롯"),
    "tab": ("탭", "기본-탭"), "compact_tab": ("탭", "소형-탭"),
    "bar": ("게이지", "가로-게이지"), "checkbox": ("입력-컨트롤", "체크박스"),
    "dropdown_field": ("입력-컨트롤", "드롭다운"), "input_field": ("입력-컨트롤", "입력란"),
    "keycap_blank": ("입력-컨트롤", "빈-키캡"), "quantity_stepper": ("입력-컨트롤", "수량-조절"),
    "radio": ("입력-컨트롤", "라디오-버튼"), "scroll": ("입력-컨트롤", "스크롤바"),
    "slider": ("입력-컨트롤", "슬라이더"), "toggle": ("입력-컨트롤", "토글"),
    "divider": ("입력-컨트롤", "구분선"),
}
states = pairs("""
normal:기본 hover:호버 pressed:누름 disabled:비활성 selected:선택
empty_locked:빈칸-잠금 epic:영웅 quest:퀘스트 rare:희귀
off:꺼짐 on:켜짐 track:트랙 thumb:손잡이 fill_blue:채움-파랑 fill_green:채움-초록 fill_red:채움-빨강
""")
windows = pairs("""
confirmation_window:확인-창 crafting_panel:제작-패널 dialogue:대화-상자 equipment_panel:장비-패널
journal_book:펼친-일지 notification_banner:알림-배너 panel_tall:범용-세로-패널 panel_wide:범용-가로-패널
portrait_frame:초상화-프레임 quest_board:퀘스트-게시판 quest_list_panel:퀘스트-목록-패널
reward_panel:보상-패널 scroll_window:두루마리-창 shop_item_card:상점-아이템-카드 skill_tree_panel:스킬-트리-패널 tooltip:툴팁
""")
icon_groups = {
    "조작과-이동": pairs("""
        arrow_left:왼쪽-화살표 arrow_right:오른쪽-화살표 check:체크 close:닫기 gear:설정 info:정보
        lock:잠금 minus:빼기 music:음악 pause:일시정지 play:재생 plus:더하기 question:도움말
        save:저장 search:검색 sound_off:음소거 sound_on:소리 trash:휴지통 unlock:잠금-해제 warning:경고
    """),
    "전투와-재화": pairs("""
        blue_shards:푸른-수정 bolt:번개 coin:금화 copper_coin:동화 heart:체력 mana:마나
        shield:방패 silver_coin:은화 star:별 sword:검 trophy:트로피
    """),
    "탐험과-생활": pairs("""
        anvil:모루 backpack:배낭 bell:종 campfire:모닥불 chat:말풍선 compass:나침반
        crafting_tools:제작-도구 fishing_rod:낚싯대 ladder:사다리 moon:달 pickaxe:곡괭이
        quest_marker:퀘스트-표식 scroll_icon:두루마리 seedling:새싹 sun:태양 watering_can:물뿌리개 world_map:세계-지도
    """),
}
item_groups = {
    "무기": pairs("""
        battle_axe:전투-도끼 crossbow:석궁 dagger:단검 flail:쇠사슬-철퇴 greatsword:대검 halberd:미늘창
        katana:일본도 short_bow:단궁 short_sword:단검보다-긴-검 spear:창 spiked_mace:가시-철퇴 trident:삼지창 war_hammer:전투-망치
    """),
    "방어구": pairs("""
        boots:장화 buckler:버클러 cape:망토 chainmail:사슬-갑옷 gloves:장갑 iron_helmet:철제-투구
        kite_shield:연꼴-방패 leather_armor:가죽-갑옷 leather_belt:가죽-허리띠 plate_armor:판금-갑옷
        quiver:화살통 ranger_hood:사냥꾼-후드 round_shield:원형-방패 tower_shield:대형-방패 wizard_hat:마법사-모자 wizard_robe:마법사-로브
    """),
    "식량과-포션": pairs("""
        antidote_vial:해독제 apple:사과 bread:빵 carrot:당근 cheese:치즈 cooked_meat:구운-고기 egg:달걀
        health_flask:체력-물약 honey_jar:꿀단지 mana_bottle:마나-물약 milk_bottle:우유 mushroom:버섯 pumpkin:호박 raw_fish:생선
    """),
    "재료와-재화": pairs("""
        coin_pouch:동전-주머니 crystal_cluster:푸른-수정-무리 feather:깃털 gold_coin:금화 gold_ingot:금괴
        herb_bundle:약초-묶음 iron_ingot:철괴 leather_roll:가죽-두루마리 ruby:루비 wood_bundle:장작-묶음
    """),
    "도구와-장신구": pairs("""
        brass_key:황동-열쇠 crown:왕관 iron_ring:철제-반지 locked_chest:잠긴-상자 moon_amulet:달-부적
        rope_bundle:밧줄 scroll:주문-두루마리 sewing_kit:바느질-도구 spell_book:마법책 torch:횃불 treasure_map:보물-지도
    """),
}
skills = pairs("""
arcane_orb:비전-구체 arrow_volley:화살-연사 earth_spike:대지-가시 fireball:화염탄 healing_spark:치유-섬광 holy_beam:신성-광선
ice_spike:얼음-가시 lightning_burst:번개-폭발 magic_barrier:마법-방어막 poison_cloud:독구름 shadow_step:그림자-이동
status_bleed:출혈 status_burn:화상 status_defense:방어-증가 status_freeze:빙결 status_haste:가속 status_poison:중독
status_regen:재생 status_stun:기절 summon_wisp:정령-소환 sword_dash:검-돌진 time_slow:시간-감속 water_wave:물결 wind_cut:바람-베기
""")
magic = pairs("""
Earth_Spike:대지-가시 Explosion:폭발 Fire_Ball:화염탄 Molten_Spear:용암-창 Portal:포탈
Rocks:낙석 Tornado:회오리 Water:물-투사체 Water_Geyser:물기둥 Wind:바람-베기
""")
magic_icons = ["화염탄", "낙석", "물-투사체", "바람-베기", "포탈", "폭발", "용암-창", "대지-가시", "물기둥", "회오리"]
atlases = pairs("icons:인터페이스-아이콘 items:아이템 skills:스킬과-상태-아이콘 ui:UI-버튼과-패널")
tone = pairs("""
cross-hue:같은-명도와-채도-다른-색상 oklch:OKLCH-세-속성 palette-comparison:색상별-명암표-비교
hue-shift:색상-회전 reference-analysis:레퍼런스-색-추출 pipeline:제작-색감-검수-흐름
""")
loose = {
    "cardBacks.png": "UI/카드와-슬롯/카드-뒷면/카드-뒷면-문양-20종.png",
    "cardbacks4092021.png": "UI/카드와-슬롯/카드-뒷면/카드-뒷면-틀과-배경-모음.png",
    "pixelCardAssest.png": "UI/카드와-슬롯/카드-프레임/카드-프레임과-아이콘-모음-기본.png",
    "pixelCardAssest_V01.png": "UI/카드와-슬롯/카드-프레임/카드-프레임과-아이콘-모음-확장.png",
    "cardripFX_spritesheet.png": "이펙트/카드-찢어짐/카드-찢어짐-시트-02.png",
    "MediavelFree.png": "아틀라스/중세-나무-UI-버튼과-게이지.png",
    "squareCircle_vector.png": "UI/카드와-슬롯/카드-프레임/사각형과-원형-프레임-모음.png",
}
qpack = "Questwood-Pixel-UI-Complete-v1.2"
fpack = "Foozle_2DE0001_Pixel_Magic_Effects"


def grouped_name(groups, stem):
    return next((folder, names[stem]) for folder, names in groups.items() if stem in names)


def questwood(parts):
    if parts == ("LICENSE.txt",):
        return "출처와-라이선스/Questwood-사용조건.txt"
    if parts == ("asset_map.json",):
        return "Questwood-에셋-좌표와-경계.json"
    if parts[0] == "Atlases_1x":
        leaf = PurePosixPath(parts[1])
        return f"아틀라스/Questwood-{atlases[leaf.stem]}-1x{leaf.suffix}"
    scale, group, filename = parts
    scale = scale.removeprefix("PNG_")
    stem = PurePosixPath(filename).stem
    if group == "Windows":
        folder, title = "UI/패널과-창", windows[stem]
    elif group in {"Buttons", "Controls"}:
        key = next(key for key in sorted(controls, key=len, reverse=True)
                   if stem == key or stem.startswith(key + "_"))
        kind, title = controls[key]
        state = stem[len(key):].lstrip("_")
        folder = f"UI/{kind}/{title}"
        title += "-" + states[state] if state else ""
    elif group == "Icons":
        kind, title = grouped_name(icon_groups, stem)
        folder = f"아이콘/인터페이스/{kind}"
    elif group == "Items":
        kind, title = grouped_name(item_groups, stem)
        folder = f"아이콘/아이템/{kind}"
    elif group == "Skills":
        title = skills[stem]
        folder = "아이콘/상태-이상과-강화" if stem.startswith("status_") else f"아이콘/스킬/{title}"
    else:
        raise ValueError(parts)
    return f"{folder}/{title}-Questwood-{scale}.png"


def classify(source):
    _, first, *rest = source.parts
    if first == qpack:
        return questwood(tuple(rest))
    if first == fpack:
        if rest == ["Readme.txt"]:
            return "출처와-라이선스/Foozle-마법-이펙트-안내.txt"
        if rest == ["Pixel_Magic_Effects_Animations.png"]:
            return "아틀라스/Foozle-마법-이펙트-애니메이션.png"
        if rest == ["Pixel_Magic_Effects_Icons.png"]:
            return "아틀라스/Foozle-마법-스킬-아이콘.png"
        group, file = rest
        stem = PurePosixPath(file).stem
        if group == "Icons":
            title = magic_icons[int(stem.removeprefix("tile"))]
            return f"아이콘/스킬/{title}/{title}-Foozle.png"
        title = magic[group]
        return f"이펙트/마법/{title}/{title}-프레임-{stem}.png"
    if first == "cardRIPfx":
        leaf, = rest
        if leaf == "cardripSHEET.png":
            return "이펙트/카드-찢어짐/카드-찢어짐-시트-01.png"
        # The visible sequence goes from intact to torn, the inverse of the export sort.
        order = 15 - int(leaf.split("_")[1])
        return f"이펙트/카드-찢어짐/프레임/카드-찢어짐-프레임-{order:02}.png"
    if first == "cardSHEENfx":
        leaf, = rest
        if "Background" in leaf:
            return "이펙트/카드-광택/카드-광택-마스크-바탕.png"
        order = int(leaf.split("_")[2]) + 1
        return f"이펙트/카드-광택/프레임/카드-광택-프레임-{order:02}.png"
    if first == "OreAndGem":
        stem = PurePosixPath(rest[0]).stem
        if stem == "OreGemSpritesheet":
            return "아이콘/아이템/광석과-보석/광석과-보석-아이콘-50종.png"
        _, motion, frames = stem.split("_")
        title = pairs("charge:충전 float:부유 shimmer:반짝임 spin:회전")[motion]
        return f"이펙트/광석과-보석/광석과-보석-{title}-{frames.removesuffix('f')}프레임-시트.png"
    if first == "color-tone-blog":
        if rest == ["article.md"]:
            return "색감-가이드/색감-분석-글.md"
        _, leaf = rest
        _, _, order, label = PurePosixPath(leaf).stem.split("-", 3)
        return f"색감-가이드/이미지/{order}-{tone[label]}.png"
    return loose[first]


root = Path(__file__).resolve().parents[2] / "references" / "reference-components"
with ZipFile(Path.home() / "Downloads/REFERENCE.zip") as archive:
    assert archive.testzip() is None
    sources = [PurePosixPath(info.filename) for info in archive.infolist() if not info.is_dir()]
    targets = {source: PurePosixPath(classify(source)) for source in sources}
    assert len({str(path).casefold() for path in targets.values()}) == len(sources)
    assert all(p.parts[0] == "REFERENCE" and ".." not in p.parts for p in sources)
    assert all(not p.is_absolute() and ".." not in p.parts for p in targets.values())
    root.mkdir()

    for source, target in targets.items():
        output = root.joinpath(*target.parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        raw = archive.read(str(source))
        if source.name == "article.md":
            payload = raw.decode("utf-8")
            for old, new in targets.items():
                if old.parts[:3] == ("REFERENCE", "color-tone-blog", "images"):
                    payload = payload.replace(f"images/{old.name}", f"이미지/{new.name}")
            output.write_text(payload, encoding="utf-8")
        elif source.name == "asset_map.json":
            model = json.loads(raw)
            for asset in model["assets"]:
                source_path = PurePosixPath("REFERENCE", qpack, asset["path"])
                asset["path"] = str(targets[source_path])
            output.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        elif source.parent.name == "Atlases_1x" and source.suffix == ".json":
            model = json.loads(raw)
            model["meta"]["image"] = targets[source.with_name(model["meta"]["image"])].name
            output.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
        else:
            output.write_bytes(raw)
            assert output.read_bytes() == raw, source

    with (root / "원본-파일-이름-대조표.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["정리한 경로", "압축 속 원본 경로", "너비", "높이", "원본 SHA-256"])
        for old, new in sorted(targets.items(), key=lambda entry: str(entry[1])):
            raw = archive.read(str(old))
            dimension = ("", "")
            if old.suffix.lower() == ".png":
                with Image.open(BytesIO(raw)) as sprite:
                    dimension = sprite.size
            writer.writerow([str(new), str(old), *dimension, hashlib.sha256(raw).hexdigest()])

counts = Counter(target.parts[0] for target in targets.values() if target.suffix.lower() == ".png")
assert sum(counts.values()) == 761
assert len(list(root.rglob("*.png"))) == 761
asset_map = json.loads((root / "Questwood-에셋-좌표와-경계.json").read_text(encoding="utf-8"))
for asset in asset_map["assets"]:
    assert (root / asset["path"]).is_file(), asset
for atlas in (root / "아틀라스").glob("*.json"):
    assert (atlas.parent / json.loads(atlas.read_text())["meta"]["image"]).is_file()
article = root / "색감-가이드" / "색감-분석-글.md"
assert len(re.findall(r"이미지/[^\x22) >]+\.png", article.read_text(encoding="utf-8"))) == 6
for rel in re.findall(r"이미지/[^\x22) >]+\.png", article.read_text(encoding="utf-8")):
    assert (article.parent / rel).is_file(), rel

print(f"{len(targets)} source files; {sum(counts.values())} PNGs; {dict(sorted(counts.items()))}")

