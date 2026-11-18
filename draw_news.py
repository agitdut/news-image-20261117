#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a dense single front page summing up
Tuesday 17 November 2026, drawn with Pillow (build time only; the entry
itself is the finished entry.png, copied by main.ts).

Layout (1024x1024): masthead + Gulf lead with a world-at-a-glance map,
Shenzhen summit box, three illustrated features (Kerch bridge, An-12
crash, measles), three columns of short items (America / The World /
Markets & Money), a markets strip and an also-in-brief footer. About
27 distinct stories, every one reported on 17 Nov 2026 (Reuters, AP,
BBC, UN News, Le Monde, ECDC, market closes).

Verified facts used:
  Gulf: US jets hit a Revolutionary Guard missile site on Qeshm Island
    (Tue) after Iran fired drones at a US radar site in Bahrain, its
    third attack there in under a week; Iran fires drones at Bahrain
    and Kuwait; tankers hit mines in the Strait of Hormuz, Tehran says;
    a third US carrier, the Theodore Roosevelt, arrives in the region.
  Shenzhen: Trump to meet Xi on the sidelines of APEC in Shenzhen; a
    three-way meeting with Putin may follow; expectations low.
  Kerch/Kyiv: Ukraine and Russia trade bridge strikes; the Crimea link
    is damaged and Kyiv's North and South bridges are closed after
    Russian strikes on Monday evening.
  An-12: Russian military transport crashes near Kemerovo, Siberia;
    all 19 on board killed; ministry cites a technical fault.
  Measles: US loses measles elimination status after 26 years; 5,400+
    cases and 10 deaths, a first since the early 1990s.
  Shorts: judge cancels stay limits for foreign students; California
    sues OpenAI after the Hugging Face attack; Chase bug delays Zelle
    payments; US data centres emit as much CO2 as Denmark (Harvard);
    Kushner reports progress in Ukraine talks; Raye leads 2027 Grammy
    nominations with 11; five EU states to open a migrant return centre
    in Rwanda; Jordan and Iraq ban Telegram; Ukraine 'double tap'
    strike kills 72 in the south; Japan protests Russian jets in its
    airspace; Sudan army airstrike kills 13 in West Kordofan; Le Pen
    says no more Ukraine aid if elected; tech stocks plunge (Nasdaq
    -2.49%, S&P 500 -1.92%); Nikkei nears a bear market, ~20% off its
    peak; Nvidia refuses Huang's return despite a 180,000-name
    petition; Brent $91.56, gold $3,879.60; US chip curbs hit Asia's
    data centres; France strikes over the cost of living, third day.
  Markets (close 17 Nov): S&P 500 7,416.59 -1.92%, Nasdaq 24,509.76
    -2.49%, CAC 40 8,352 -0.20%, DAX 26,599 -0.57%, Nikkei 58,860
    -1.34%, Brent $91.56, gold $3,879.60 +0.69%, Bitcoin $64,591.
  Also: Pope Leo XIV hit in the eye by a rosary in Peru; gas leak at
    an ONGC well in India, residents evacuated; Japan's Fugaku
    supercomputer breached; Sudan army airstrike kills 13 in West
    Kordofan; EU revives its Syria cooperation deal.
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
RULE = (190, 186, 176)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, w, text, fnt, fill, leading, max_lines=None):
    """Draw wrapped text, return y after last line. Raises if it overflows."""
    lines = wrap(draw, text, fnt, w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"text overflows ({len(lines)} > {max_lines}): {text[:60]!r}")
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


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


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24  # margin

# ---- masthead ----
d.rectangle([0, 0, W, 84], fill=NAVY)
d.text((MX, 10), "THE WORLD TODAY", font=font(F_SERIF, 46), fill=(255, 255, 255))
d.text((MX, 62), "TUESDAY, 17 NOVEMBER 2026  •  ONE DAY, ONE PAGE  •  WORLD NEWS",
       font=font(F_BIG, 13), fill=(180, 200, 220))

# ---- lead: Gulf (left) + map & Shenzhen (right) ----
LY = 96
# left column
d.text((MX, LY), "WAR IN THE GULF — US STRIKES QESHM", font=font(F_BIG, 14), fill=RED)
y = block(d, MX, LY + 22, 596, "US jets strike Iran's Qeshm Island",
          font(F_SERIF, 36), INK, 42, max_lines=2)
y = block(d, MX, y + 4, 596,
          "American jets hit a Revolutionary Guard missile site after Iran "
          "fired drones at a US radar site in Bahrain — its third attack "
          "there in under a week.",
          font(F_REG, 15), (52, 56, 66), 20, max_lines=3)
y += 8
for b in [
    "Iran fires drones at Bahrain and Kuwait; Gulf defences intercept them.",
    "Tankers hit mines in the Strait of Hormuz, Tehran says; oil steadies.",
    "A third US carrier, the Theodore Roosevelt, arrives in the Middle East.",
]:
    d.ellipse([MX + 2, y + 5, MX + 8, y + 11], fill=RED)
    y = block(d, MX + 14, y, 582, b, font(F_REG, 12), (52, 56, 66), 16, max_lines=2)
    y += 3

# right column: world map panel
RX, RW = 644, 356
d.rectangle([RX, LY, RX + RW, LY + 124], fill=(214, 226, 240), outline=(150, 160, 175), width=1)
d.text((RX + 8, LY + 4), "THE WORLD AT A GLANCE", font=font(F_BIG, 11), fill=NAVY)
# schematic continents (equirectangular, coarse but recognisable)
ox, oy = RX + 8, LY + 22
LAND = (168, 178, 158)
d.polygon([(ox + 6, oy + 22), (ox + 30, oy + 6), (ox + 72, oy + 4), (ox + 96, oy + 16),
           (ox + 88, oy + 38), (ox + 60, oy + 52), (ox + 34, oy + 46), (ox + 12, oy + 36)], fill=LAND)  # N America
d.polygon([(ox + 62, oy + 58), (ox + 88, oy + 56), (ox + 92, oy + 78), (ox + 76, oy + 96),
           (ox + 64, oy + 82)], fill=LAND)  # S America
d.polygon([(ox + 158, oy + 8), (ox + 182, oy + 4), (ox + 192, oy + 18), (ox + 178, oy + 32),
           (ox + 160, oy + 28)], fill=LAND)  # Europe
d.polygon([(ox + 158, oy + 36), (ox + 186, oy + 34), (ox + 196, oy + 52), (ox + 184, oy + 78),
           (ox + 168, oy + 72), (ox + 156, oy + 52)], fill=LAND)  # Africa
d.polygon([(ox + 196, oy + 4), (ox + 250, oy + 2), (ox + 300, oy + 10), (ox + 318, oy + 30),
           (ox + 300, oy + 52), (ox + 268, oy + 58), (ox + 238, oy + 44), (ox + 206, oy + 34),
           (ox + 194, oy + 18)], fill=LAND)  # Asia
d.polygon([(ox + 272, oy + 76), (ox + 302, oy + 74), (ox + 306, oy + 88), (ox + 280, oy + 92)],
          fill=LAND)  # Australia
F_MAP = font(F_BIG, 9)
markers = [
    ("QESHM", 238, 46, 8, -12), ("KERCH", 208, 22, -34, -12),
    ("SHENZHEN", 292, 44, -14, 12), ("RWANDA", 172, 66, -40, 2),
    ("SIBERIA", 268, 12, -8, -12),
]
for name, mx, my, dx, dy in markers:
    d.ellipse([ox + mx - 4, oy + my - 4, ox + mx + 4, oy + my + 4], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((ox + mx + dx, oy + my + dy), name, font=F_MAP, fill=(120, 20, 20))
# Shenzhen box under map
SY = LY + 132
d.rectangle([RX, SY, RX + RW, SY + 92], fill=(255, 255, 255), outline=RULE, width=1)
d.text((RX + 10, SY + 6), "APEC • SHENZHEN", font=font(F_BIG, 11), fill=RED)
block(d, RX + 10, SY + 24, RW - 20, "Trump, Xi and Putin head for Shenzhen",
      font(F_BIG, 17), INK, 21, max_lines=2)
block(d, RX + 10, SY + 66, RW - 20,
      "Trump to meet Xi at APEC; a three-way meeting with Putin may follow.",
      font(F_REG, 11), MUTED, 14, max_lines=2)

d.line([(MX, 332), (W - MX, 332)], fill=INK, width=2)

# ---- feature row: three illustrated stories ----
FY = 344
FW, FGAP = 309, 24
features = [
    ("KERCH BRIDGE", "bridge", "Ukraine and Russia trade bridge strikes",
     "Crimea link damaged; Kyiv's North and South bridges closed after Russian strikes."),
    ("PLANE CRASH", "plane", "Russian An-12 crashes in Siberia; 19 dead",
     "Military transport goes down near Kemerovo; the ministry cites a technical fault."),
    ("MEASLES", "measles", "US loses measles-free status after 26 years",
     "5,400+ cases and 10 deaths — a first since the early 1990s."),
]
for i, (tag, kind, hl, sub) in enumerate(features):
    x = MX + i * (FW + FGAP)
    d.rectangle([x, FY, x + FW, FY + 212], fill=(255, 255, 255), outline=RULE, width=1)
    ix, iy, iw, ih = x + 1, FY + 1, FW - 2, 96
    if kind == "bridge":
        vgrad(d, (ix, iy, ix + iw, iy + ih), (232, 196, 150), (250, 222, 190))
        d.rectangle([ix, iy + 62, ix + iw, iy + ih], fill=(44, 92, 130))
        d.rectangle([ix + 40, iy + 20, ix + 52, iy + 78], fill=(70, 76, 86))
        d.rectangle([ix + 256, iy + 20, ix + 268, iy + 78], fill=(70, 76, 86))
        d.rectangle([ix, iy + 62, ix + 118, iy + 74], fill=(52, 58, 68))
        d.rectangle([ix + 190, iy + 62, ix + iw, iy + 74], fill=(52, 58, 68))
        d.polygon([(ix + 118, iy + 62), (ix + 146, iy + 66), (ix + 140, iy + 96),
                   (ix + 124, iy + 92)], fill=(40, 44, 54))
        d.polygon([(ix + 190, iy + 62), (ix + 164, iy + 68), (ix + 170, iy + 94),
                   (ix + 184, iy + 90)], fill=(40, 44, 54))
        cloud(d, ix + 118, iy + 40, 0.7, (120, 118, 116))
        cloud(d, ix + 150, iy + 30, 0.55, (140, 138, 136))
        d.ellipse([ix + 142, iy + 56, ix + 162, iy + 76], fill=(255, 200, 60))
        d.ellipse([ix + 148, iy + 62, ix + 156, iy + 70], fill=(255, 120, 40))
    elif kind == "plane":
        vgrad(d, (ix, iy, ix + iw, iy + ih), (170, 200, 230), (220, 232, 240))
        cloud(d, ix + 20, iy + 12, 0.8, (255, 255, 255))
        cloud(d, ix + 190, iy + 60, 0.7, (255, 255, 255))
        # transport plane banking down, smoke trailing
        d.polygon([(ix + 60, iy + 55), (ix + 240, iy + 30), (ix + 250, iy + 42),
                   (ix + 70, iy + 70)], fill=(90, 96, 104))
        d.polygon([(ix + 130, iy + 62), (ix + 170, iy + 30), (ix + 190, iy + 34),
                   (ix + 160, iy + 66)], fill=(70, 76, 84))
        d.polygon([(ix + 90, iy + 52), (ix + 120, iy + 78), (ix + 132, iy + 74),
                   (ix + 108, iy + 48)], fill=(70, 76, 84))
        cloud(d, ix + 30, iy + 58, 0.7, (120, 118, 116))
        cloud(d, ix + 8, iy + 66, 0.5, (140, 138, 136))
    else:
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(150, 30, 34))
        # white disc with a red cross, virus dots around it
        d.ellipse([ix + 104, iy + 8, ix + 204, iy + 88], fill=(255, 255, 255))
        d.rectangle([ix + 140, iy + 22, ix + 168, iy + 74], fill=RED)
        d.rectangle([ix + 120, iy + 38, ix + 188, iy + 58], fill=RED)
        for cx, cy, r in [(ix + 40, iy + 24, 9), (ix + 268, iy + 28, 10),
                          (ix + 282, iy + 76, 8), (ix + 34, iy + 78, 8)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 200, 60))
            for dx2, dy2 in [(-r - 5, 0), (r + 5, 0), (0, -r - 5), (0, r + 5)]:
                d.line([(cx, cy), (cx + dx2, cy + dy2)], fill=(255, 200, 60), width=2)
    d.rectangle([x, FY + 98, x + FW, FY + 120], fill=NAVY)
    d.text((x + 10, FY + 104), tag, font=font(F_BIG, 13), fill=(255, 255, 255))
    block(d, x + 10, FY + 126, FW - 20, hl, font(F_BIG, 16), INK, 20, max_lines=2)
    block(d, x + 10, FY + 166, FW - 20, sub, font(F_REG, 11), MUTED, 14, max_lines=2)

d.line([(MX, 568), (W - MX, 568)], fill=INK, width=2)

# ---- three columns of short items ----
CY = 580
COLS = [
    ("AMERICA", [
        ("Judge cancels stay limits for foreign students",
         "Trump-era rule capping student visas at 4 years void."),
        ("OpenAI sued by California after Hugging Face attack",
         "AG Bonta: the attack was entirely foreseeable."),
        ("Chase bug delays Zelle in US bank outage",
         "Chase blames a software bug, rules out cyberattack."),
        ("US data centres emit as much CO2 as Denmark",
         "Harvard study: top centres use ~2% of US power."),
        ("Kushner reports progress in Ukraine talks",
         "Moscow refuses a European role in the next round."),
        ("Raye leads Grammy nominations with 11",
         "UK singer tops the 2027 Grammy list, BBC reports."),
    ]),
    ("THE WORLD", [
        ("Five EU states to open migrant centre in Rwanda",
         "Germany, Austria, Denmark, Greece, Netherlands agree."),
        ("Jordan and Iraq ban Telegram over extremism",
         "App accused of fuelling radicalisation."),
        ("Ukraine 'double tap' strike kills 72 in south",
         "Kyiv accuses Moscow of targeting rescuers."),
        ("Japan protests Russian jets in its airspace",
         "Tokyo scrambles fighters off Okinoshima island."),
        ("Ebola cases pass 11,300 in Congo",
         "Africa CDC warns it could become the worst on record."),
        ("Le Pen: no more Ukraine aid if elected",
         "Zelensky: a halt to French aid would hurt Kyiv."),
    ]),
    ("MARKETS & MONEY", [
        ("Tech stocks plunge; Nasdaq falls 2.49%",
         "S&P 500 down 1.92% as the AI boom falters."),
        ("Nikkei nears bear market, ~20% off peak",
         "Analysts see months to regain the highs."),
        ("Nvidia refuses Huang return despite campaign",
         "Board holds firm; petition passes 180,000 names."),
        ("Brent $91.56; gold $3,879.60 as haven bid",
         "Gold up 0.69% while stocks fall."),
        ("US chip curbs hit Asia's data centres",
         "Licences now needed for advanced AI chips."),
        ("France strikes over cost of living, third day",
         "Unions call a new day of protests on Tuesday."),
    ]),
]
for i, (sec, items) in enumerate(COLS):
    x = MX + i * (FW + FGAP)
    d.rectangle([x, CY, x + FW, CY + 24], fill=NAVY)
    d.text((x + 10, CY + 5), sec, font=font(F_BIG, 13), fill=(255, 255, 255))
    yy = CY + 32
    for j, (hl, sub) in enumerate(items):
        yy = block(d, x, yy, FW, hl, font(F_BIG, 12), INK, 15, max_lines=2)
        yy = block(d, x, yy + 1, FW, sub, font(F_REG, 10), MUTED, 13, max_lines=1)
        yy += 6
        if j < len(items) - 1:
            d.line([(x, yy - 3), (x + FW, yy - 3)], fill=(220, 218, 210), width=1)

# ---- markets strip ----
MY = 892
d.rectangle([MX, MY, W - MX, MY + 58], fill=(232, 228, 218), outline=RULE, width=1)
d.text((MX + 10, MY + 6), "MARKETS — TUESDAY'S CLOSE", font=font(F_BIG, 12), fill=RED)
block(d, MX + 10, MY + 24, W - 2 * MX - 20,
      "S&P 500 7,416.59  −1.92%   •   Nasdaq 24,509.76  −2.49%   •   CAC 40 8,352  −0.20%   •   DAX 26,599  −0.57%",
      font(F_BIG, 13), INK, 17, max_lines=1)
block(d, MX + 10, MY + 41, W - 2 * MX - 20,
      "Nikkei 58,860  −1.34%   •   Brent $91.56   •   Gold $3,879.60  +0.69%   •   Bitcoin $64,591",
      font(F_BIG, 13), INK, 17, max_lines=1)

# ---- footer: also in brief + sources ----
FY2 = 962
block(d, MX, FY2, W - 2 * MX,
      "ALSO IN BRIEF: Pope Leo XIV hit in the eye by a rosary in Peru  •  Gas leak at an ONGC well in India; residents evacuated  •  Japan's Fugaku supercomputer breached  •  Sudan army airstrike kills 13 in West Kordofan  •  EU revives its Syria cooperation deal.",
      font(F_REG, 11), (52, 56, 66), 14, max_lines=2)
d.text((MX, 1000), "Sources: Reuters, AP, BBC, UN News, Le Monde, ECDC — Tuesday 17 November 2026",
       font=font(F_REG, 11), fill=MUTED)

img.save(OUT, optimize=True)
print("saved", img.size)
print(os.path.getsize(OUT), "bytes")
