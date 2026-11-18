#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026 in four panels, drawn with Pillow (build time
only; the entry itself is the finished entry.png, copied by main.ts).

Stories (all reported on 17 Nov 2026):
  1. Crimea bridge partly collapses -- Ukrainian missile and drone
     strike damages the Kerch Strait link; Russia strikes Kyiv's
     bridges in reply.
  2. Gulf strikes -- US jets hit a Revolutionary Guard missile site
     on Qeshm Island; Iran fires drones at Bahrain and Kuwait.
  3. Russian An-12 military transport crashes in the Kemerovo region
     of Siberia, all 19 on board killed; technical fault suspected.
  4. US loses measles elimination status after 26 years -- 5,400+
     cases and 10 deaths, a first since the early 1990s.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
MUTED = (90, 92, 98)

F_BIG = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def cloud(draw, x, y, s, color=(255, 255, 255)):
    draw.ellipse([x, y, x + 70 * s, y + 34 * s], fill=color)
    draw.ellipse([x + 18 * s, y - 16 * s, x + 62 * s, y + 22 * s], fill=color)
    draw.ellipse([x + 42 * s, y - 8 * s, x + 84 * s, y + 30 * s], fill=color)


def panel_text(draw, x, y, w, headline, sub, hl_size=27):
    f_hl = font(F_BIG, hl_size)
    f_sub = font(F_REG, 17)
    lines = wrap(draw, headline, f_hl, w)
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=f_hl, fill=INK)
        yy += hl_size + 6
    for ln in wrap(draw, sub, f_sub, w):
        draw.text((x, yy + 4), ln, font=f_sub, fill=MUTED)
        yy += 22


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 86], fill=NAVY)
d.text((28, 16), "TUESDAY, 17 NOVEMBER 2026", font=font(F_BIG, 40), fill=(255, 255, 255))
d.text((28, 62), "THE DAY IN FOUR PICTURES  •  WORLD NEWS", font=font(F_REG, 17), fill=(180, 200, 220))

# ---- hero: Crimea bridge ----
HX, HY, HW = 24, 102, 976
HH = 452
vgrad(d, (HX, HY, HX + HW, HY + 300), (232, 196, 150), (250, 222, 190))
# sun low over the strait
d.ellipse([HX + 780, HY + 30, HX + 880, HY + 130], fill=(240, 180, 90))
cloud(d, 90, 130, 1.0, (250, 238, 220))
cloud(d, 560, 110, 0.8, (250, 238, 220))
# sea
d.rectangle([HX, HY + 300, HX + HW, HY + 330], fill=(44, 92, 130))
for i in range(14):
    d.line([(HX + 30 + i * 70, HY + 314), (HX + 70 + i * 70, HY + 314)], fill=(120, 170, 205), width=3)
# bridge: two pylons, deck, broken middle span
d.rectangle([HX + 130, HY + 90, HX + 150, HY + 300], fill=(70, 76, 86))
d.rectangle([HX + 826, HY + 90, HX + 846, HY + 300], fill=(70, 76, 86))
d.polygon([(HX + 120, HY + 90), (HX + 140, HY + 52), (HX + 160, HY + 90)], fill=(52, 58, 68))
d.polygon([(HX + 816, HY + 90), (HX + 836, HY + 52), (HX + 856, HY + 90)], fill=(52, 58, 68))
# cables
for x0 in (140, 836):
    d.line([(x0, HY + 70), (HX + 488, HY + 240)], fill=(120, 126, 134), width=3)
# intact deck left and right
d.rectangle([HX, HY + 240, HX + 380, HY + 262], fill=(52, 58, 68))
d.rectangle([HX + 596, HY + 240, HX + HW, HY + 262], fill=(52, 58, 68))
# broken span plunging into the strait
d.polygon([(HX + 380, HY + 240), (HX + 470, HY + 244), (HX + 452, HY + 306), (HX + 396, HY + 300)], fill=(40, 44, 54))
d.polygon([(HX + 596, HY + 240), (HX + 520, HY + 246), (HX + 534, HY + 300), (HX + 580, HY + 296)], fill=(40, 44, 54))
# smoke + flash at the break
cloud(d, HX + 400, HY + 150, 1.1, (90, 90, 96))
cloud(d, HX + 500, HY + 120, 0.8, (120, 118, 116))
d.ellipse([HX + 460, HY + 190, HX + 520, HY + 250], fill=(255, 200, 60))
d.ellipse([HX + 474, HY + 204, HX + 506, HY + 236], fill=(255, 120, 40))
# red banner
d.rectangle([HX + 250, HY + 150, HX + 726, HY + 196], fill=RED)
d.text((HX + 268, HY + 158), "BRIDGE IN RUINS", font=font(F_BIG, 28), fill=(255, 255, 255))
# hero text block
panel_text(d, HX + 8, HY + 348, HW - 16,
           "Crimea bridge partly collapses",
           "Ukrainian missile and drone strike damages the Kerch link; "
           "Russia hits Kyiv's bridges in reply.",
           hl_size=36)

# ---- bottom row: three panels ----
BW, GAP = 309, 24
BY = 578
panels = [
    ("GULF STRIKES", (28, 52, 96), "draw_gulf"),
    ("PLANE CRASH IN SIBERIA", (30, 90, 120), "draw_plane"),
    ("MEASLES STATUS LOST", (58, 48, 92), "draw_measles"),
]
for i, (tag, bg, kind) in enumerate(panels):
    x = 24 + i * (BW + GAP)
    d.rectangle([x, BY, x + BW, BY + 400], fill=(255, 255, 255), outline=(200, 198, 190), width=2)
    d.rectangle([x, BY, x + BW, BY + 34], fill=NAVY)
    d.text((x + 10, BY + 8), tag, font=font(F_BIG, 15), fill=(255, 255, 255))
    ix, iy, iw, ih = x + 2, BY + 36, BW - 4, 168
    if kind == "draw_gulf":
        vgrad(d, (ix, iy, ix + iw, iy + ih), (214, 178, 130), (240, 210, 170))
        d.rectangle([ix, iy + 118, ix + iw, iy + ih], fill=(38, 84, 130))
        # island with a launch site, jets overhead, drone trails
        d.polygon([(ix + 90, iy + 168), (ix + 150, iy + 96), (ix + 220, iy + 168)], fill=(120, 100, 70))
        d.rectangle([ix + 142, iy + 76, ix + 158, iy + 100], fill=(60, 60, 66))
        d.line([(ix + 150, iy + 76), (ix + 190, iy + 40)], fill=(255, 200, 60), width=4)
        d.ellipse([ix + 184, iy + 30, ix + 206, iy + 52], fill=(255, 120, 40))
        d.polygon([(ix + 40, iy + 40), (ix + 70, iy + 48), (ix + 40, iy + 56)], fill=(30, 34, 44))
        d.polygon([(ix + 230, iy + 60), (ix + 260, iy + 68), (ix + 230, iy + 76)], fill=(30, 34, 44))
        d.line([(ix + 40, iy + 48), (ix + 10, iy + 48)], fill=(200, 200, 200), width=2)
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "U.S. hits Qeshm, Iran hits back",
                   "American jets strike a missile site on Qeshm Island; "
                   "Iran fires drones at Bahrain and Kuwait.",
                   hl_size=24)
    elif kind == "draw_plane":
        vgrad(d, (ix, iy, ix + iw, iy + ih), (200, 214, 228), (240, 244, 248))
        d.rectangle([ix, iy + 132, ix + iw, iy + ih], fill=(228, 232, 236))
        # snowy ridge
        d.polygon([(ix, iy + 168), (ix + 90, iy + 120), (ix + 180, iy + 168)], fill=(255, 255, 255))
        d.polygon([(ix + 140, iy + 168), (ix + 240, iy + 112), (ix + iw, iy + 168)], fill=(244, 246, 248))
        # falling transport plane, nose down
        d.ellipse([ix + 120, iy + 60, ix + 220, iy + 84], fill=(52, 58, 68))
        d.polygon([(ix + 200, iy + 64), (ix + 232, iy + 44), (ix + 236, iy + 66)], fill=(52, 58, 68))
        d.polygon([(ix + 150, iy + 82), (ix + 164, iy + 100), (ix + 176, iy + 82)], fill=(52, 58, 68))
        d.line([(ix + 120, iy + 72), (ix + 90, iy + 100)], fill=(180, 180, 180), width=3)
        d.ellipse([ix + 60, iy + 96, ix + 110, iy + 140], fill=(200, 200, 200))
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "Military plane crash kills 19",
                   "An-12 transport goes down in the Kemerovo region; "
                   "defence ministry blames a technical fault.",
                   hl_size=24)
    else:
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(214, 226, 240))
        # virus dots over a clinic cross
        d.rectangle([ix + 120, iy + 30, ix + 186, iy + 138], fill=(255, 255, 255), outline=(180, 190, 200), width=2)
        d.rectangle([ix + 146, iy + 48, ix + 160, iy + 120], fill=RED)
        d.rectangle([ix + 124, iy + 70, ix + 182, iy + 84], fill=RED)
        for cx, cy, r in [(ix + 40, iy + 40, 12), (ix + 70, iy + 120, 9),
                          (ix + 250, iy + 50, 11), (ix + 265, iy + 130, 8),
                          (ix + 30, iy + 150, 7)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 34, 34))
            for dx, dy in [(-r - 5, 0), (r + 5, 0), (0, -r - 5), (0, r + 5)]:
                d.line([(cx, cy), (cx + dx, cy + dy)], fill=(178, 34, 34), width=2)
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "U.S. loses measles-free status",
                   "5,400+ cases and 10 deaths end 26 years of "
                   "elimination — a first since the early 1990s.",
                   hl_size=24)

# ---- footer ----
d.text((28, 984), "Sources: BBC, AP, CBS, Reuters — Tuesday 17 November 2026",
       font=font(F_REG, 14), fill=MUTED)
d.text((28, 1002), "Also: Quad leaders meet in Manila · Depardieu admits assault · Mongolia's president resigns",
       font=font(F_REG, 14), fill=MUTED)

img.save(OUT, optimize=True)
print("saved", img.size)
print(os.path.getsize(OUT), "bytes")
