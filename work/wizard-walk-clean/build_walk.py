import sys
from PIL import Image, ImageDraw

ROOT = sys.argv[1]
OUT = sys.argv[2]
src = Image.open(ROOT + '/work/wizard-walk-clean/source-frame-00.png').convert('RGBA')

C = {
    '0': (22, 19, 27, 255), '1': (53, 36, 45, 255), '3': (56, 49, 59, 255),
    '4': (81, 44, 43, 255), '6': (97, 59, 40, 255), '7': (112, 56, 50, 255),
    '9': (146, 70, 58, 255), 'a': (147, 89, 48, 255), 'c': (118, 101, 107, 255),
}
T = (0, 0, 0, 0)

# Upper body template: frame 0 (staff held at chest, idle face), legs removed.
tmpl = Image.new('RGBA', (32, 32), T)
for y in range(32):
    for x in range(32):
        p = src.getpixel((x, y))
        if not p[3]:
            continue
        if y <= 21 or (x <= 10 and y <= 24):
            tmpl.putpixel((x, y), p)
# close the cloak's lower outline where leg pixels used to sit
tmpl.putpixel((11, 22), C['0'])
tmpl.putpixel((11, 23), C['0'])
# the bare-knee skin block at the hem belongs to the old wide stance;
# turn it into coat so the new legs read cleanly
for (x, y) in ((13, 20), (14, 20), (13, 21), (14, 21)):
    tmpl.putpixel((x, y), C['1'])

def is_cloak_tail(x, y):
    return x <= 10 and y >= 19

# staff, crystal and the hand holding it; the first staff column per row
STAFF_FROM = {10: 22, 11: 21, 12: 21, 13: 20, 14: 20, 15: 20, 16: 20,
              17: 20, 18: 19, 19: 19}
STAFF = {(x, y) for y, x0 in STAFF_FROM.items() for x in range(x0, 26)
         if tmpl.getpixel((x, y))[3]}

def body_layer(staff_dx, stretch):
    """Template with the staff block shifted and the cloak tip extended."""
    out = Image.new('RGBA', (32, 32), T)
    for y in range(32):
        for x in range(32):
            px = tmpl.getpixel((x, y))
            if px[3] and (x, y) not in STAFF:
                out.putpixel((x, y), px)
    if stretch:
        # pull the cloak tip one pixel further back; column 8 stays as the fill
        for y in range(19, 25):
            for x in range(1, 9):
                px = tmpl.getpixel((x, y))
                if px[3]:
                    out.putpixel((x - 1, y), px)
    for (x, y) in STAFF:
        out.putpixel((x + staff_dx, y), tmpl.getpixel((x, y)))
    if staff_dx > 0:
        # stretch the sleeve to the moved hand and keep the coat edge closed
        out.putpixel((20, 17), tmpl.getpixel((19, 17)))
        for y in (18, 19):
            if not out.getpixel((19, y))[3]:
                out.putpixel((19, y), C['0'])
    return out

# 16-bit RPG field gait: three held poses instead of a smooth stride.
# step A (near leg forward) -> legs together -> step B -> legs together.
# With the frame durations in timing.json (50,30,20,50,50,50,30,20,50,50 ms)
# every pose is held for 100 ms, so the 400 ms loop reads as four even beats.
STEP = 3          # foot offset from FOOT_CENTER in the split poses
TOGETHER = 1      # foot offset in the legs-together pose
# (name, near_dx, far_dx, body_bob, staff_dx, cloak_stretch)
# The staff is pushed 1px forward on every other step, like planting a walking
# staff (pulling it back would press the crystal into the hair). The cloak tail
# flares 1px on both strides.
A = ('A', STEP, -STEP, 0, 0, 1)
S = ('S', TOGETHER, -TOGETHER, -1, 0, 0)  # legs straight, body 1px taller
B = ('B', -STEP, STEP, 0, 1, 1)
FRAME_POSES = [A, S, S, S, B, B, S, S, S, A]
HIP_NEAR, HIP_FAR = 15, 14
FOOT_CENTER = 14.5  # both feet use the same centre so the two steps mirror

def put(img, x, y, k):
    if 0 <= x < 32 and 0 <= y < 32:
        img.putpixel((x, y), C[k])

def draw_leg(img, hip_x, hip_y, dx, near):
    ank_x = round(FOOT_CENTER + dx)
    boot_y = 26                 # boot foot row; sole is boot_y + 1 (y=27)
    shin = ('1', 'c', 'c') if near else ('1', '3', '3')
    rows = list(range(hip_y, boot_y - 1))
    n = max(1, len(rows) - 1)
    for i, y in enumerate(rows):
        x = round(hip_x + (ank_x - hip_x) * i / n)
        put(img, x - 1, y, '0')
        for j, k in enumerate(shin):
            put(img, x + j, y, k)
        put(img, x + 3, y, '0')
    s = ank_x
    # chunky boot: cuff, foot with forward toe, dark sole
    cuff = ('4', '7', '7') if near else ('1', '4', '4')
    put(img, s - 1, boot_y - 1, '0')
    for j, k in enumerate(cuff):
        put(img, s + j, boot_y - 1, k)
    put(img, s + 3, boot_y - 1, '0')
    top = ('4', '9', '9', 'a') if near else ('1', '7', '4', '4')
    put(img, s - 1, boot_y, '0')
    for j, k in enumerate(top):
        put(img, s + j, boot_y, k)
    put(img, s + 4, boot_y, '0')
    sole = ['0', '6' if near else '0', '0', '0', '0', '0']
    for j, k in enumerate(sole):
        put(img, s - 1 + j, boot_y + 1, k)

sheet = Image.new('RGBA', (320, 32), T)
for i, (_, near_dx, far_dx, b, staff_dx, stretch) in enumerate(FRAME_POSES):
    layer = body_layer(staff_dx, stretch)
    f = Image.new('RGBA', (32, 32), T)
    b_lag = FRAME_POSES[i - 1][3]   # cloak tail follows the body a beat late
    hip_y = 22 + b
    draw_leg(f, HIP_FAR, hip_y, far_dx, near=False)
    draw_leg(f, HIP_NEAR, hip_y, near_dx, near=True)
    for y in range(32):
        for x in range(32):
            px = layer.getpixel((x, y))
            if not px[3]:
                continue
            oy = b_lag if is_cloak_tail(x, y) else b
            if 0 <= y + oy < 32:
                f.putpixel((x, y + oy), px)
            # when the tail hangs lower than the body, repeat its top row at
            # the body offset so no 1px gap opens between cloak and torso
            if b_lag > b and is_cloak_tail(x, y) and not is_cloak_tail(x, y - 1):
                if not f.getpixel((x, y + b))[3]:
                    f.putpixel((x, y + b), px)
    sheet.paste(f, (i * 32, 0))

sheet.save(OUT)
