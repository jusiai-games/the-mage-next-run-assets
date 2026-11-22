from pathlib import Path
from random import Random
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
SIZE = (160, 352)
FONT = Path(os.environ["WINDIR"]) / "Fonts/malgunbd.ttf"
HERO = HERE.parent / "wizard-unhooded/hero-wizard.png"
DESIGNS = [
    ("trail", "첫 발걸음", (47,232), 3),
    ("gate", "별빛 관문", (76,251), 3),
    ("camp", "모닥불의 지도", (60,233), 4),
]

def stars(draw, points, color):
    for x,y in points:
        draw.line((x-2,y,x+2,y),fill=color)
        draw.line((x,y-2,x,y+2),fill=color)

def sky(draw, colors):
    for i,color in enumerate(colors):
        draw.rectangle((0,i*31,159,i*31+30),fill=color)

def cloud(draw,x,y,color):
    draw.polygon([(x-20,y),(x-13,y-2),(x-10,y-5),(x-4,y-5),(x+1,y-10),
                  (x+8,y-10),(x+13,y-6),(x+16,y-5),(x+21,y)],fill=color)

def ridge(draw, points, color):
    draw.polygon(points+[(159,351),(0,351)],fill=color)

def pine(draw,x,y,h,color):
    draw.rectangle((x-1,y-4,x+1,y+2),fill=color)
    for band in (0,1,2):
        lift=band*h//5
        draw.polygon([(x,y-h+lift),(x-h//6-band,y-h//2+lift),
                      (x+h//6+band,y-h//2+lift)],fill=color)

def flecks(draw, seed, bounds, colors, count):
    rng = Random(seed)
    left,top,right,bottom = bounds
    for i in range(count):
        x,y = rng.randrange(left,right),rng.randrange(top,bottom)
        draw.line((x,y,x+rng.randrange(1,4),y),fill=rng.choice(colors))

def trail(draw):
    sky(draw,["#2b5665","#41787d","#6c9e96","#a1bab0","#d4cc9d","#dfd3a3"])
    draw.ellipse((109,105,137,133),fill="#fbe5af")
    for x,y in [(19,101),(82,117),(146,97)]:
        cloud(draw,x,y,"#adc4ad")
    ridge(draw,[(0,156),(24,136),(36,138),(63,112),(85,139),(111,128),(159,158)],"#769d95")
    draw.polygon([(63,112),(85,139),(111,128),(126,155),(86,161),(78,133)],fill="#638b86")
    ridge(draw,[(0,165),(26,149),(43,152),(67,173),(101,164),(138,148),(159,152)],"#517b73")
    ridge(draw,[(0,181),(31,184),(63,174),(91,177),(128,164),(159,175)],"#668d72")
    ridge(draw,[(0,207),(30,201),(58,186),(88,195),(120,189),(159,201)],"#517a62")
    draw.polygon([(102,180),(113,181),(105,189),(80,199),(70,216),(87,230),
                  (119,243),(129,258),(116,280),(83,309),(73,351),(0,351),(14,312),
                  (47,278),(72,258),(73,247),(55,232),(51,219),(63,202),(83,190)],fill="#b89a72")
    draw.line([(102,181),(79,195),(59,213),(57,225),(76,244),(82,255),(53,283),(23,314),(10,351)],fill="#d3b481",width=2)
    flecks(draw,2,(0,236,160,278),["#70936a","#597e61"],32)
    flecks(draw,3,(0,319,160,351),["#486f5a","#6c8c66"],36)
    for x,y in [(8,224),(23,236),(100,228),(127,213),(142,236),(134,254),(14,269),(21,282),(148,279)]:
        draw.line((x,y,x-1,y+5),fill="#365d51")
        draw.point((x+1,y),fill="#f3d5a3")
        draw.point((x-1,y+1),fill="#dca0a0")
        draw.point((x,y-1),fill="#eed9bc")
    for x,y,h in [(1,201,43),(14,190,25),(154,203,53),(144,195,29)]:
        pine(draw,x,y,h,"#365f57")

def gate(draw):
    sky(draw,["#202641","#2d3551","#3c4867","#525e7d","#706e92","#867f9b"])
    moon = Image.new("1",(33,31))
    mask = ImageDraw.Draw(moon)
    mask.ellipse((6,4,32,30),fill=1)
    mask.ellipse((0,0,25,22),fill=0)
    draw.bitmap((109,86),moon,fill="#e9d8bb")
    stars(draw,[(25,94),(102,102),(68,112),(149,122),(51,87)],"#b8c6d7")
    ridge(draw,[(0,149),(19,121),(35,142),(51,129),(80,158),(115,139),(138,125),(159,148)],"#515875")
    ridge(draw,[(0,162),(25,153),(53,164),(78,153),(111,169),(134,151),(159,158)],"#383f62")
    ridge(draw,[(0,210),(22,194),(53,199),(80,185),(109,188),(159,202)],"#2a4054")
    draw.polygon([(69,211),(100,211),(114,235),(126,268),(149,351),(16,351),(38,275),(53,239)],fill="#4b5269")
    draw.line([(69,211),(53,239),(38,275),(16,351)],fill="#64617a",width=2)
    for x,y,h in [(2,228,75),(15,228,47),(26,233,63),(139,229,68),(154,233,82),(126,239,41)]:
        pine(draw,x,y,h,"#233548")
    draw.polygon([(48,213),(48,169),(54,151),(67,138),(79,134),(97,137),(111,147),
                  (119,164),(119,214),(105,214),(105,169),(99,154),(89,149),(76,149),
                  (65,156),(61,172),(61,214)],fill="#272a49")
    draw.polygon([(53,208),(53,169),(60,152),(70,143),(82,139),(96,142),(107,151),
                  (114,166),(114,208),(105,208),(105,166),(98,154),(86,149),(76,151),
                  (66,158),(61,174),(61,208)],fill="#788296")
    draw.polygon([(62,207),(63,172),(68,159),(77,152),(89,151),(99,157),(105,170),(105,207)],fill="#487280")
    draw.polygon([(66,206),(67,174),(75,160),(86,155),(98,163),(102,174),(102,206)],fill="#80b6ae")
    draw.polygon([(71,205),(77,182),(86,162),(86,172),(90,177),(85,188),(92,202)],fill="#b8e3cc")
    for x,y in [(57,175),(57,190),(109,173),(110,189),(83,145)]:
        stars(draw,[(x,y)],"#abd2c3")
    for x,y in [(52,217),(54,221),(80,218),(94,220),(106,220),(118,224)]:
        draw.line((x,y,x+9,y),fill="#7b8b9a")
    flecks(draw,7,(2,239,156,351),["#667088","#33495e","#607189"],45)
    stars(draw,[(34,204),(97,226),(123,195),(65,229)],"#9dcab6")

def camp(draw):
    sky(draw,["#272942","#433753","#67506b","#936477","#bd7d80","#dea88b"])
    draw.ellipse((108,104,136,132),fill="#f4c094")
    for x,y in [(21,105),(134,95),(75,123)]:
        cloud(draw,x,y,"#ad7780")
    ridge(draw,[(0,155),(24,134),(36,139),(60,120),(88,153),(106,147),(127,129),(159,146)],"#775d78")
    ridge(draw,[(0,173),(27,153),(61,158),(84,172),(107,166),(133,151),(159,157)],"#514963")
    ridge(draw,[(0,207),(29,192),(62,184),(106,179),(159,191)],"#45465b")
    for x,y,h in [(4,224,100),(23,223,58),(149,227,109),(134,219,59),(158,221,77)]:
        pine(draw,x,y,h,"#292b42")
    ridge(draw,[(0,225),(25,215),(52,216),(75,220),(108,212),(124,216),(159,226)],"#4e4b54")
    draw.ellipse((42,213,148,283),fill="#645451")
    draw.ellipse((62,224,135,272),fill="#836454")
    draw.ellipse((80,230,128,260),fill="#9a785d")
    draw.polygon([(23,251),(54,247),(76,251),(72,254),(54,255),(49,274),(45,274),
                  (43,255),(23,256)],fill="#362e3e")
    draw.polygon([(24,245),(50,242),(75,247),(65,253),(30,252)],fill="#a78062")
    draw.polygon([(33,245),(45,243),(67,245),(64,250),(42,249),(36,251)],fill="#ebc98d")
    draw.line([(40,247),(47,246),(51,248),(58,246),(61,247)],fill="#9b7161")
    stars(draw,[(62,246)],"#b2574c")
    draw.ellipse((87,240,121,252),fill="#524554")
    for x,y in [(88,243),(95,248),(104,249),(113,247),(119,243)]:
        draw.rectangle((x-3,y-1,x+2,y+1),fill="#b0987f")
        draw.line((x-2,y+2,x+2,y+2),fill="#705c62")
    draw.line((95,247,112,239),fill="#392e3c",width=3)
    draw.line((96,239,114,247),fill="#473442",width=3)
    draw.polygon([(95,243),(92,235),(98,229),(99,234),(102,229),(104,219),
                  (109,226),(107,233),(111,231),(113,240),(108,245),(100,245)],fill="#cf7358")
    draw.polygon([(98,241),(101,236),(104,233),(105,227),(108,233),(107,237),
                  (110,238),(107,244),(101,244)],fill="#ffd193")
    stars(draw,[(109,215),(98,220),(118,226)],"#ecc287")
    flecks(draw,8,(0,263,160,351),["#5e5058","#6e5c59","#434354"],55)

def label(draw, xy, value, size, color, outline, width=0):
    draw.text(xy,value,font=ImageFont.truetype(str(FONT),size),anchor="mt",
              fill=color,stroke_width=width,stroke_fill=outline)

def interface(theme):
    image = Image.new("RGBA", SIZE)
    draw = ImageDraw.Draw(image)
    accent = {"trail":"#eac890","gate":"#b7e0d3","camp":"#f6bc89"}[theme]
    dark = "#222139"
    label(draw,(80,26),"주문 넣고 갑니다",17,"#fff0cf",dark,1)
    label(draw,(80,52),"Spells to Go",11,accent,dark,1)
    draw.line((50,72,73,72),fill=accent)
    draw.line((87,72,110,72),fill=accent)
    draw.polygon([(80,68),(84,72),(80,76),(76,72)],fill=accent)
    button = [(40,288),(120,288),(128,296),(128,312),(121,320),
              (39,320),(32,313),(32,296)]
    draw.polygon([(x,y+3) for x,y in button],fill="#18182b")
    draw.polygon(button,fill=dark)
    draw.polygon([(41,291),(119,291),(125,297),(125,311),(119,317),
                  (41,317),(35,311),(35,297)],fill=accent)
    draw.polygon([(42,293),(118,293),(123,298),(123,310),(118,315),
                  (42,315),(37,310),(37,298)],fill={"trail":"#546b60","gate":"#414e65","camp":"#734e52"}[theme])
    label(draw,(80,297),"게임 시작",12,"#fff2d9",dark,1)
    return image

def main():
    hero = Image.open(HERO).convert("RGBA")
    assert hero.size == (32,32)
    board = Image.new("RGB",(1016,774),"#202537")
    headings = ImageDraw.Draw(board)
    designs = []
    for index,(key,name,foot,scale) in enumerate(DESIGNS):
        out = HERE / key
        out.mkdir(exist_ok=True)
        background = Image.new("RGBA",SIZE)
        {"trail":trail,"gate":gate,"camp":camp}[key](ImageDraw.Draw(background))
        assert background.getchannel("A").getextrema() == (255,255)
        hero_layer = Image.new("RGBA",SIZE)
        draw = ImageDraw.Draw(hero_layer)
        x,y = foot
        draw.ellipse((x-13,y-3,x+13,y+3),fill=(25,24,41,135))
        hero_layer.alpha_composite(hero.resize((32*scale,32*scale),Image.Resampling.NEAREST),
                                   (x-16*scale,y-28*scale))
        ui = interface(key)
        scene = Image.alpha_composite(Image.alpha_composite(background,hero_layer),ui)
        for filename,image in [("background",background),("wizard",hero_layer),("ui",ui),("preview",scene)]:
            image.save(out/f"{filename}.png")
        ox = 20+328*index
        headings.text((ox,13),name,font=ImageFont.truetype(str(FONT),21),fill="#f4e7cc")
        board.paste(scene.resize((320,704),Image.Resampling.NEAREST),(ox,52))
        designs.append(dict(directory=key,name=name,feet_px=foot,wizard_scale=scale))
    board.save(HERE/"comparison.png")
    (HERE/"manifest.json").write_text(json.dumps(dict(viewport_px=SIZE,
        layers=["background.png","wizard.png","ui.png"],start_button_rect_px=[32,288,96,33],
        hero_source="../wizard-unhooded/hero-wizard.png",hero_source_pivot_px=[16,28],designs=designs),
        ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__":
    main()

