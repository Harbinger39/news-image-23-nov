#!/usr/bin/env python3
"""Compose the 23 November 2026 news-image entry: a dense newspaper front page.

Drawn entirely in code with PIL (flat editorial art style, one consistent
palette). No photos, no network, deterministic output: same bytes every run.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (90, 90, 86)
LIGHT = (232, 228, 218)
RED = (178, 34, 28)
BLUE = (24, 62, 110)
GREEN = (22, 110, 58)
NAVY = (16, 34, 64)
GOLD = (196, 148, 28)
TEAL = (14, 110, 110)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FDIR}/{name}.ttf", size)


SERIF = lambda s: font("DejaVuSerif-Bold", s)      # noqa: E731
SERIF_R = lambda s: font("DejaVuSerif", s)         # noqa: E731
SANS = lambda s: font("DejaVuSans", s)             # noqa: E731
BOLD = lambda s: font("DejaVuSans-Bold", s)        # noqa: E731
MONO = lambda s: font("DejaVuSansMono-Bold", s)    # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped paragraph; returns y just below last line."""
    lh = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, x, y, text, size, width, fill=INK, max_lines=3):
    fnt = BOLD(size)
    lh = int(size * 1.12)
    lines = wrap(draw, text, fnt, width)[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, text, fill):
    """Small CONFIRMED / REPORTED tag chip; returns width used."""
    fnt = BOLD(9)
    w = int(draw.textlength(text, font=fnt)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 16  # page margin

# ---------------------------------------------------------------- masthead
rule(d, MX, W - MX, 10, 3)
d.text((MX, 16), "EST. 2026  •  ONE DAY, ONE PAGE", font=BOLD(10), fill=GREY)
d.text((W - MX - d.textlength("PRICE: FREE  •  1024 x 1024", font=BOLD(10)), 16),
       "PRICE: FREE  •  1024 x 1024", font=BOLD(10), fill=GREY)
title = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(title, font=SERIF(46))) / 2, 30),
       title, font=SERIF(46), fill=INK)
date = "MONDAY 23 NOVEMBER 2026"
d.text(((W - d.textlength(date, font=BOLD(21))) / 2, 82),
       date, font=BOLD(21), fill=RED)
rule(d, MX, W - MX, 108, 3)
rule(d, MX, W - MX, 112, 1)

# ------------------------------------------------------------- numbers strip
strip = [
    ("NASDAQ", "+7.1%"), ("S&P 500", "+5.1%"), ("DOW", "+1,466"),
    ("NVIDIA", "+34.5%"), ("KOSPI", "-3.3%"), ("SENSEX", "-1,484"),
    ("HOUSE SEATS", "258"), ("SEA DRONES", "7"), ("MISSILES IN POLAND", "3"),
    ("MEGA DEAL", "$43.9BN"),
]
d.rectangle([MX, 118, W - MX, 146], fill=INK)
sx = MX + 8
for label, val in strip:
    d.text((sx, 122), label, font=BOLD(8), fill=(200, 200, 190))
    d.text((sx, 131), val, font=BOLD(12), fill=(255, 255, 255))
    sx += int(max(d.textlength(label, font=BOLD(8)),
                  d.textlength(val, font=BOLD(12)))) + 16

# ------------------------------------------------------------ picture makers
# Each draws one story inside (x, y, w, h) in a flat editorial style.

def pic_nvidia(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(12, 40, 26))
    # rising chart
    pts = [(x + 8, y + h - 18), (x + w * 0.28, y + h - 44),
           (x + w * 0.5, y + h - 30), (x + w * 0.72, y + h - 58),
           (x + w - 10, y + 16)]
    for i in range(len(pts) - 1):
        dr.line([pts[i], pts[i + 1]], fill=(118, 200, 80), width=4)
    dr.polygon([(x + w - 22, y + 10), (x + w - 6, y + 10), (x + w - 10, y + 26)],
               fill=(118, 200, 80))
    # chip
    cx, cy, cw, chh = x + 14, y + 12, 74, 52
    dr.rectangle([cx, cy, cx + cw, cy + chh], fill=(24, 90, 44),
                 outline=(118, 200, 80), width=2)
    for i in range(4):
        px = cx + 12 + i * 16
        dr.line([(px, cy - 7), (px, cy)], fill=(118, 200, 80), width=3)
        dr.line([(px, cy + chh), (px, cy + chh + 7)], fill=(118, 200, 80), width=3)
    dr.rectangle([cx + 22, cy + 15, cx + 52, cy + 37], fill=(118, 200, 80))
    dr.text((cx + 27, cy + 20), "NV", font=BOLD(13), fill=(12, 40, 26))
    dr.text((x + w - 92, y + h - 24), "+34.5%", font=BOLD(17), fill=(255, 255, 255))


def pic_warship(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(150, 196, 224))
    dr.rectangle([x, y, x + w, y + h * 0.62], fill=(214, 232, 244))
    # sun + clouds
    dr.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(250, 214, 90))
    dr.ellipse([x + 16, y + 12, x + 64, y + 30], fill=(255, 255, 255))
    dr.ellipse([x + 44, y + 6, x + 92, y + 24], fill=(255, 255, 255))
    # sea
    dr.rectangle([x, y + h * 0.62, x + w, y + h], fill=(28, 84, 128))
    for i in range(5):
        wx = x + 10 + i * 62
        dr.arc([wx, y + h - 26, wx + 44, y + h - 8], 0, 180, fill=(150, 196, 224), width=2)
    # warship hull + superstructure
    hx, hy = x + w * 0.30, y + h * 0.42
    dr.polygon([(hx, hy + 26), (hx + 150, hy + 26), (hx + 168, hy + 44),
                (hx + 8, hy + 44)], fill=(74, 84, 92))
    dr.rectangle([hx + 34, hy, hx + 108, hy + 26], fill=(96, 106, 114))
    dr.rectangle([hx + 58, hy - 16, hx + 84, hy], fill=(96, 106, 114))
    dr.line([(hx + 70, hy - 30), (hx + 70, hy - 16)], fill=(60, 66, 72), width=4)
    dr.rectangle([hx + 118, hy + 6, hx + 128, hy + 26], fill=(60, 66, 72))
    # explosion burst mid-hull, with smoke above it
    bx, by = hx + 70, hy + 12
    for ang in range(0, 360, 30):
        import math as _m
        ex = bx + 20 * _m.cos(_m.radians(ang))
        ey = by + 20 * _m.sin(_m.radians(ang))
        dr.line([(bx, by), (ex, ey)], fill=(250, 160, 30), width=4)
    dr.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(250, 200, 60))
    dr.ellipse([bx - 8, by - 34, bx + 8, by - 18], fill=(90, 90, 90))
    dr.ellipse([bx + 4, by - 42, bx + 18, by - 28], fill=(110, 110, 110))
    # sea drones: small fast boats with wakes
    for dx0 in (x + 12, x + w - 66):
        dr.polygon([(dx0, y + h - 14), (dx0 + 34, y + h - 14),
                    (dx0 + 40, y + h - 6), (dx0 + 2, y + h - 6)],
                   fill=(30, 30, 30))
        dr.line([(dx0 - 14, y + h - 10), (dx0, y + h - 10)],
                fill=(255, 255, 255), width=2)


def pic_missile(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    dr.ellipse([x + w - 60, y + 10, x + w - 24, y + 46], fill=(240, 224, 170))
    # ground + pine trees
    dr.rectangle([x, y + h - 26, x + w, y + h], fill=(34, 74, 44))
    for tx in (x + 14, x + 44, x + w - 52, x + w - 22):
        dr.polygon([(tx, y + h - 62), (tx + 10, y + h - 84), (tx + 20, y + h - 62)],
                   fill=(22, 92, 52))
        dr.rectangle([tx + 8, y + h - 62, tx + 12, y + h - 50], fill=(90, 60, 30))
    # missile with smoke trail
    import math as _m
    mx, my = x + w * 0.42, y + h * 0.52
    dr.line([(x + 8, y + h - 30), (mx, my)], fill=(200, 200, 200), width=5)
    dr.line([(x + 8, y + h - 30), (mx, my)], fill=(140, 140, 140), width=2)
    dr.ellipse([mx - 26, my - 9, mx + 26, my + 9], fill=(210, 210, 210),
               outline=(120, 120, 120))
    dr.polygon([(mx + 26, my - 9), (mx + 44, my), (mx + 26, my + 9)],
               fill=(178, 34, 28))
    dr.polygon([(mx - 18, my - 9), (mx - 30, my - 18), (mx - 12, my - 6)],
               fill=(178, 34, 28))
    dr.polygon([(mx - 18, my + 9), (mx - 30, my + 18), (mx - 12, my + 6)],
               fill=(178, 34, 28))
    dr.text((x + 10, y + 8), "Kh-101", font=BOLD(15), fill=(255, 255, 255))
    dr.text((x + 10, y + 28), "DEBRIS AT 3 SITES", font=BOLD(11), fill=(250, 200, 60))


def pic_capitol(dr, x, y, w, h):
    # Art was drafted for a 128px-tall box; scale the offsets from the
    # bottom so nothing pokes above the picture box (the dome used to
    # cover words in the lead text above this card).
    k = h / 128.0

    def up(v):
        return y + h - int(round(v * k))

    dr.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
    dr.rectangle([x, up(22), x + w, y + h], fill=(46, 92, 52))
    cx = x + w / 2
    dr.rectangle([cx - 62, up(62), cx + 62, up(22)], fill=(240, 238, 230))
    dr.rectangle([cx - 30, up(92), cx + 30, up(62)], fill=(240, 238, 230))
    dr.pieslice([cx - 26, up(118), cx + 26, up(66)], 180, 360,
                fill=(240, 238, 230))
    dr.rectangle([cx - 2, up(128), cx + 2, up(116)], fill=(120, 110, 96))
    for i in range(-2, 3):
        dr.rectangle([cx + i * 22 - 3, up(58), cx + i * 22 + 3, up(24)],
                     fill=(180, 176, 164))
    dr.text((x + 8, y + 6), "258", font=BOLD(26), fill=(24, 62, 110))
    dr.text((x + 8, y + 34), "SEATS", font=BOLD(11), fill=(24, 62, 110))


def pic_eu(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(16, 42, 96))
    # Star ring sized to stay inside the box (radius 52 poked 27px above it).
    cx, cy = x + w / 2, y + h / 2 + 1
    import math as _m
    for i in range(12):
        a = _m.radians(i * 30 - 90)
        sx, sy = cx + 26 * _m.cos(a), cy + 26 * _m.sin(a)
        dr.polygon([(sx, sy - 6), (sx + 2, sy - 1), (sx + 6, sy), (sx + 2, sy + 2),
                    (sx + 1, sy + 6), (sx - 1, sy + 2), (sx - 6, sy + 1),
                    (sx - 2, sy - 2)], fill=(250, 204, 0))
    # tanker with ban slash
    dr.rectangle([cx - 46, cy - 2, cx + 46, cy + 18], fill=(120, 40, 30))
    dr.rectangle([cx + 20, cy - 16, cx + 40, cy - 2], fill=(90, 90, 90))
    dr.line([(cx - 56, cy + 26), (cx + 56, cy - 26)], fill=(220, 60, 40), width=6)
    dr.text((x + 8, y + h - 18), "22nd PACKAGE", font=BOLD(11), fill=(255, 255, 255))


def pic_chipfall(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(26, 26, 34))
    pts = [(x + 8, y + 18), (x + w * 0.3, y + 34), (x + w * 0.55, y + 30),
           (x + w * 0.75, y + 62), (x + w - 10, y + h - 16)]
    for i in range(len(pts) - 1):
        dr.line([pts[i], pts[i + 1]], fill=(230, 60, 50), width=4)
    dr.polygon([(x + w - 24, y + h - 26), (x + w - 8, y + h - 26),
                (x + w - 12, y + h - 8)], fill=(230, 60, 50))
    dr.rectangle([x + 12, y + h - 46, x + 58, y + h - 12], fill=(60, 90, 140),
                 outline=(160, 200, 240), width=2)
    for i in range(3):
        px = x + 20 + i * 14
        dr.line([(px, y + h - 52), (px, y + h - 46)], fill=(160, 200, 240), width=2)
    dr.text((x + w - 66, y + 8), "-5.8%", font=BOLD(16), fill=(255, 120, 110))


def pic_fire(dr, x, y, w, h):
    # Art was drafted for a 128px-tall box; scale the offsets from the
    # bottom so flames, chimney and smoke stay inside the picture box
    # (the flames used to reach into the lead text above this card).
    k = h / 128.0

    def up(v):
        return y + h - int(round(v * k))

    dr.rectangle([x, y, x + w, y + h], fill=(40, 34, 30))
    dr.rectangle([x, up(34), x + w, y + h], fill=(60, 54, 48))
    # factory block
    dr.rectangle([x + 14, up(66), x + w - 14, up(34)], fill=(120, 110, 100))
    dr.rectangle([x + w - 52, up(92), x + w - 30, up(66)], fill=(96, 88, 80))
    # flames
    for fx, fh, col in ((x + 30, 44, (250, 140, 20)), (x + 58, 58, (250, 90, 10)),
                        (x + 92, 40, (250, 180, 40)), (x + 124, 52, (250, 110, 15))):
        dr.polygon([(fx, up(66)), (fx + 12, up(66) - int(round(fh * k))),
                    (fx + 24, up(66))], fill=col)
    # smoke (kept inside the box top)
    for i, (sx0, sy0, r) in enumerate(((x + 40, y + 16, 8), (x + 66, y + 12, 9),
                                      (x + 96, y + 16, 8))):
        dr.ellipse([sx0 - r, sy0 - r, sx0 + r, sy0 + r], fill=(150, 150, 150))
    dr.text((x + 8, y + h - 20), "24 DEAD", font=BOLD(13), fill=(255, 255, 255))


def pic_smog(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(196, 168, 120))
    dr.rectangle([x, y, x + w, y + h * 0.55], fill=(214, 190, 150))
    dr.ellipse([x + w - 56, y + 10, x + w - 18, y + 48], fill=(240, 200, 90))
    # skyline in haze (buildings scaled to stay inside the picture box;
    # at full height they poked 16px above it, into the leads above).
    for bx, bw, bh in ((x + 8, 26, 52), (x + 38, 20, 70), (x + 62, 30, 44),
                       (x + 96, 18, 62), (x + 118, 26, 50), (x + 148, 22, 58)):
        bh = int(round(bh * (h - 22) / 70.0))
        dr.rectangle([bx, y + h - 20 - bh, bx + bw, y + h - 20], fill=(110, 96, 78))
    dr.rectangle([x, y + h - 20, x + w, y + h], fill=(70, 60, 48))
    dr.text((x + 8, y + 6), "AQI 500+", font=BOLD(16), fill=(120, 30, 20))
    dr.text((x + 8, y + 26), "LAHORE", font=BOLD(11), fill=(120, 30, 20))


def pic_deal(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    # two shields merging
    def shield(cx, cy, col):
        dr.polygon([(cx - 26, cy - 26), (cx + 26, cy - 26), (cx + 26, cy + 4),
                    (cx, cy + 30), (cx - 26, cy + 4)], fill=col)
        dr.text((cx - 4, cy - 12), "✓", font=BOLD(16), fill=(255, 255, 255))
    shield(x + 52, y + h / 2 - 4, (200, 40, 40))
    shield(x + w - 52, y + h / 2 - 4, (24, 62, 110))
    dr.text((x + w / 2 - 8, y + h / 2 - 14), "+", font=BOLD(20), fill=INK)
    dr.text((x + 8, y + h - 18), "$43.9BN", font=BOLD(13), fill=INK)


def pic_storm(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(70, 78, 96))
    dr.ellipse([x + 10, y + 8, x + 90, y + 44], fill=(52, 58, 74))
    dr.ellipse([x + 60, y + 2, x + 150, y + 40], fill=(44, 50, 66))
    dr.ellipse([x + 120, y + 10, x + w - 8, y + 46], fill=(52, 58, 74))
    # lightning
    dr.polygon([(x + w / 2 + 6, y + 40), (x + w / 2 - 8, y + 78),
                (x + w / 2 + 2, y + 78), (x + w / 2 - 10, y + 112),
                (x + w / 2 + 14, y + 70), (x + w / 2 + 4, y + 70)],
               fill=(250, 220, 60))
    # damaged houses
    for hx in (x + 10, x + 62, x + 118):
        dr.polygon([(hx, y + h - 34), (hx + 18, y + h - 52), (hx + 36, y + h - 34)],
                   fill=(150, 60, 40))
        dr.rectangle([hx + 2, y + h - 34, hx + 34, y + h - 16], fill=(200, 170, 130))
    dr.text((x + 8, y + h - 14), "5 KILLED", font=BOLD(11), fill=(255, 255, 255))


def pic_cricket(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(52, 110, 52))
    dr.ellipse([x + 10, y + 10, x + w - 10, y + h - 10], fill=(96, 150, 80))
    # pitch strip
    dr.rectangle([x + w / 2 - 22, y + 8, x + w / 2 + 22, y + h - 8],
                 fill=(210, 190, 140))
    # stumps
    for sx in (x + w / 2 - 12, x + w / 2, x + w / 2 + 12):
        dr.line([(sx, y + h - 30), (sx, y + h - 52)], fill=(250, 220, 120), width=3)
    # bat + red ball
    dr.line([(x + 26, y + 34), (x + 62, y + 84)], fill=(180, 130, 70), width=9)
    dr.ellipse([x + w - 52, y + 26, x + w - 30, y + 48], fill=(200, 30, 30))
    dr.text((x + 8, y + h - 20), "720/9", font=BOLD(16), fill=(255, 255, 255))


def pic_satellite(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for sx0, sy0 in ((x + 14, y + 12), (x + 70, y + 22), (x + 130, y + 8),
                     (x + 160, y + 30), (x + 40, y + 40), (x + 110, y + 48)):
        dr.ellipse([sx0 - 1, sy0 - 1, sx0 + 1, sy0 + 1], fill=(255, 255, 255))
    # satellite body with solar panels
    cx, cy = x + w / 2, y + h / 2 - 4
    dr.rectangle([cx - 58, cy - 8, cx - 16, cy + 8], fill=(30, 90, 160))
    dr.rectangle([cx + 16, cy - 8, cx + 58, cy + 8], fill=(30, 90, 160))
    for i in range(3):
        dr.line([(cx - 44 + i * 14, cy - 8), (cx - 44 + i * 14, cy + 8)],
                fill=(140, 190, 240), width=1)
        dr.line([(cx + 30 + i * 14, cy - 8), (cx + 30 + i * 14, cy + 8)],
                fill=(140, 190, 240), width=1)
    dr.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(200, 200, 200),
                 outline=(120, 120, 120))
    dr.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=(250, 200, 60))
    # radiation trefoil badge
    bx, by = x + w - 30, y + h - 28
    dr.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(250, 200, 60))
    dr.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(12, 16, 34))
    dr.text((x + 8, y + 6), "REPORTED", font=BOLD(10), fill=(250, 200, 60))


def pic_plane(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(170, 205, 230))
    dr.ellipse([x + 16, y + 10, x + 70, y + 28], fill=(255, 255, 255))
    dr.ellipse([x + 60, y + 16, x + 120, y + 34], fill=(255, 255, 255))
    # runway
    dr.rectangle([x, y + h - 26, x + w, y + h], fill=(80, 80, 80))
    for i in range(6):
        dr.rectangle([x + 8 + i * 32, y + h - 16, x + 26 + i * 32, y + h - 12],
                     fill=(255, 255, 255))
    # plane body
    px, py = x + 30, y + h / 2 - 6
    dr.ellipse([px, py, px + 130, py + 26], fill=(240, 240, 240),
               outline=(120, 120, 120))
    dr.polygon([(px + 128, py + 6), (px + 158, py + 13), (px + 128, py + 20)],
               fill=(200, 40, 40))
    dr.polygon([(px + 60, py - 2), (px + 84, py - 26), (px + 96, py - 2)],
               fill=(200, 40, 40))
    dr.polygon([(px + 96, py + 22), (px + 112, py + 40), (px + 120, py + 22)],
               fill=(200, 40, 40))
    dr.ellipse([px + 132, py + 9, px + 142, py + 17], fill=(24, 62, 110))
    dr.text((x + 8, y + 6), "146 ABOARD", font=BOLD(11), fill=(24, 62, 110))

# ------------------------------------------------------------------- leads
LY = 154
COLW = (W - 2 * MX - 2 * 12) // 3


def lead(col, kicker, head, picfn, body, source, tagtxt):
    x = MX + col * (COLW + 12)
    d.text((x, LY), kicker, font=BOLD(10), fill=RED)
    y = headline(d, x, LY + 14, head, 17, COLW)
    picfn(d, x, y + 4, COLW, 84)
    y = y + 4 + 84 + 2
    y = para(d, x, y, body, SANS(10), COLW, max_lines=4)
    tw = tag(d, x, y + 2, tagtxt, GREEN if tagtxt == "CONFIRMED" else GOLD)
    d.text((x + tw + 6, y + 4), "Source: " + source, font=SANS(9), fill=GREY)


lead(0, "MARKETS  •  LEAD STORY",
     "Huang is back: Nvidia board reinstates its founder as chief",
     pic_nvidia,
     "Eleven days after he resigned, Jensen Huang returns as president, "
     "CEO and director by unanimous vote. Shares soared 34.5% in morning "
     "trade; the Nasdaq jumped 7.1% and the Dow 1,466 points.",
     "Reuters / Nvidia Newsroom", "CONFIRMED")
lead(1, "WAR AT SEA  •  LIBYA",
     "Zelenskyy says sea drones sank a Russian warship off Libya",
     pic_warship,
     "Seven Ukrainian naval drones struck the corvette Merkury off "
     "Benghazi, Kyiv says, destroying a Ka-27 helicopter and hitting the "
     "cargo ship MV Angara. Libyan officials say it was severely damaged.",
     "AP / Reuters / CNN", "REPORTED")
lead(2, "NATO  •  POLAND",
     "Poland summons Russia's envoy as missile debris is found",
     pic_missile,
     "Kh-101 debris was found at all three sites after missiles entered "
     "Polish airspace on Friday during an attack on Ukraine. NATO's North "
     "Atlantic Council meets on Monday to discuss the incursion.",
     "hromadske / Reuters", "CONFIRMED")
rule(d, MX, W - MX, 364, 2)

# ------------------------------------------------------------ pictured cards
d.text((MX, 370), "THE DAY IN PICTURES", font=BOLD(13), fill=INK)
d.text((W - MX - d.textlength("Every picture shows its own story", font=SANS(10)), 372),
       "Every picture shows its own story", font=SANS(10), fill=GREY)
CARDS = [
    ("US HOUSE", "Democrats clinch House majority — 258 seats, best since 1992",
     pic_capitol, "CONFIRMED", "Reuters"),
    ("EU  •  SANCTIONS", "Brussels proposes 22nd sanctions package on Russia",
     pic_eu, "CONFIRMED", "Reuters"),
    ("ASIA  •  MARKETS", "Asian chip stocks slide: Kospi dives 5.8% intraday",
     pic_chipfall, "CONFIRMED", "Economic Times"),
    ("INDONESIA", "Candy-factory fire toll confirmed: 24 dead, ~30 missing",
     pic_fire, "CONFIRMED", "Xinhua"),
    ("PAKISTAN", "Lahore tops world pollution list as AQI crosses 500",
     pic_smog, "CONFIRMED", "Daily Star"),
    ("DEALS", "CrowdStrike to buy Zscaler in a $43.9bn all-stock deal",
     pic_deal, "CONFIRMED", "Reuters"),
    ("BRAZIL", "Supercell storm wrecks 8,000 homes and kills five",
     pic_storm, "CONFIRMED", "AP"),
    ("CRICKET  •  WELLINGTON", "India pile up 720/9 in first Test against New Zealand",
     pic_cricket, "CONFIRMED", "Times of India"),
    ("AVIATION", "Air Niugini jet makes emergency landing, 146 aboard",
     pic_plane, "CONFIRMED", "AP"),
    ("NUCLEAR  •  REPORTED", "NATO intelligence: Russia plans nuclear-armed satellite launch",
     pic_satellite, "REPORTED", "German media"),
]
CW = (W - 2 * MX - 4 * 10) // 5
CH = 148
for i, (kick, head, picfn, ttag, src) in enumerate(CARDS):
    cx = MX + (i % 5) * (CW + 10)
    cy = 390 + (i // 5) * (CH + 8)
    d.rectangle([cx, cy, cx + CW, cy + CH], outline=LIGHT, width=1)
    picfn(d, cx + 1, cy + 1, CW - 2, 74)
    d.text((cx + 4, cy + 80), kick, font=BOLD(8), fill=RED)
    headline(d, cx + 4, cy + 92, head, 10, CW - 8, max_lines=3)
    tw = tag(d, cx + 4, cy + CH - 18, ttag, GREEN if ttag == "CONFIRMED" else GOLD)
    d.text((cx + 4 + tw + 4, cy + CH - 16), src, font=SANS(8), fill=GREY)
rule(d, MX, W - MX, 700, 2)

# ------------------------------------------------- dotted world map + pins
MAPX, MAPY, MAPW, MAPH = MX, 708, 600, 128
d.text((MAPX, MAPY), "WHERE THE NEWS HAPPENED", font=BOLD(12), fill=INK)
d.text((MAPX, MAPY + 16), "Pins mark the pictured stories", font=SANS(9), fill=GREY)
# Stylised landmasses as ellipse blobs (lon/lat -> map px).
BLOBS = [
    # (lon0, lon1, lat0, lat1) rough continent boxes
    (-168, -52, 15, 72),    # North America
    (-82, -34, -56, 12),    # South America
    (-12, 32, 36, 70),      # Europe
    (-18, 52, -35, 36),     # Africa
    (32, 180, 5, 78),       # Asia
    (112, 155, -40, -10),   # Australia
    (166, 180, -47, -34),   # New Zealand
]


def lonlat_to_xy(lon, lat):
    px = MAPX + (lon + 170) / 360 * MAPW
    py = MAPY + 34 + (75 - lat) / 130 * (MAPH - 40)
    return px, py


# dot grid
for gx in range(0, MAPW, 7):
    for gy in range(34, MAPH - 4, 7):
        lon = (MAPX + gx - MAPX) / MAPW * 360 - 170
        lat = 75 - (MAPY + gy - MAPY - 34) / (MAPH - 40) * 130
        inside = any(lo0 <= lon <= lo1 and la0 <= lat <= la1
                     for lo0, lo1, la0, la1 in BLOBS)
        if inside:
            d.ellipse([MAPX + gx - 1, MAPY + gy - 1, MAPX + gx + 1, MAPY + gy + 1],
                      fill=(120, 120, 116))
PINS = [
    ("Benghazi", 20, 32, 6, 6), ("Warsaw", 21, 52, 6, -14),
    ("Delhi", 77, 28, -34, 8), ("Seoul", 127, 37, 6, -14),
    ("Banten", 106, -6, 6, 6), ("Lahore", 74, 31, 6, -14),
    ("Washington", -77, 39, 6, -4), ("Brasilia", -48, -16, 6, -4),
    ("Wellington", 175, -41, -56, -4), ("Manila", 121, 14, 6, 6),
]
for name, lon, lat, dx, dy in PINS:
    px, py = lonlat_to_xy(lon, lat)
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((px + dx, py + dy), name, font=BOLD(8), fill=RED)

# ------------------------------------------------------------ UTC timeline
TX = MAPX + MAPW + 14
TW = W - MX - TX
d.text((TX, MAPY), "THE DAY IN UTC", font=BOLD(12), fill=INK)
TIMELINE = [
    ("02:00", "Asian chip stocks slide; Kospi down 5.8% intraday"),
    ("05:30", "Modi–Shah talks open in Delhi (11:00 IST)"),
    ("08:05", "Zelenskyy: sea drones sank the Merkury"),
    ("09:39", "Poland: Kh-101 debris at all three sites"),
    ("11:31", "Zelenskyy offers four-way talks"),
    ("14:30", "Nvidia reinstates Huang; Wall St surges"),
    ("14:35", "Poland summons Russia's ambassador"),
    ("15:45", "Dow +1,466, Nasdaq +7.1% mid-morning"),
    ("EVE", "Indonesia confirms 24 dead in factory fire"),
]
ty = MAPY + 16
for t, txt in TIMELINE:
    d.text((TX, ty), t, font=MONO(10), fill=RED)
    ty = para(d, TX + 46, ty, txt, SANS(9), TW - 46, leading=11, max_lines=1)
    ty += 2
rule(d, MX, W - MX, 844, 2)

# ------------------------------------------------------------- ALSO ON list
d.text((MX, 850), "ALSO ON", font=BOLD(12), fill=INK)
ALSO = [
    ("EUROPE", "Babis rejects EU budget plan, opposes €100bn for Ukraine"),
    ("EUROPE", "French police jailed over racist assault on producer"),
    ("EUROPE", "Russian strikes killed 534 civilians in Ukraine in Oct"),
    ("EUROPE", "Kyiv seeks police help to compel ex-minister to testify"),
    ("N. AMER", "US shields air-traffic network ahead of Thanksgiving"),
    ("N. AMER", "US citizen deported to Mexico; DOJ admits mistake"),
    ("N. AMER", "Democrats propose new Green Card route for migrants"),
    ("N. AMER", "Five suicides among NSA / Cyber Command staff"),
    ("N. AMER", "US Army to detonate bomb chemicals in Iowa"),
    ("N. AMER", "Trump hosts gala for investors in his meme coin"),
    ("M. EAST", "Netanyahu–Eisenkot coalition talks end in deadlock"),
    ("M. EAST", "Netanyahu urges Trump to strike Iran “ASAP” — report"),
    ("M. EAST", "Iran seeks “clear and operational” end to stalemate"),
    ("M. EAST", "Iran's “Fereydun Plan”: 14 tankers to defy US blockade"),
    ("ASIA", "Myanmar calls ASEAN peace-plan review “unfair”"),
    ("ASIA", "S. Korea education minister quits over AI exam chaos"),
    ("ASIA", "Nepal PM Shah meets Modi; India pledges ₹24,000 cr"),
    ("ASIA", "India–China end 10-day talks to ease LAC tensions"),
    ("ASIA", "Dhaka vows to arrest Hasina if she returns in Dec"),
    ("ASIA", "Kim: N. Korea seeks security, not supremacy"),
    ("ASIA", "Pakistan army chief Munir meets Malaysia's Anwar"),
    ("ASIA", "Sensex −1,484; rupee 92.91 to the dollar"),
    ("ASIA", "Singapore builds 350m barrage, 15th reservoir"),
    ("LATAM", "Mexico captures cartel leader after 11 killed"),
    ("SPORT", "SA v Bangladesh Day 1: Rabada, Jansen, Nortje star"),
    ("SPORT", "De Villiers: Aussie ball-tampering began in 2018"),
    ("MARKETS", "US PCE report due Wednesday 25 November"),
]
COLW2 = (W - 2 * MX - 2 * 16) // 3
ay = 868
col = 0
per_col = (len(ALSO) + 2) // 3
for i, (region, txt) in enumerate(ALSO):
    if i and i % per_col == 0:
        col += 1
        ay = 868
    ax = MX + col * (COLW2 + 16)
    d.text((ax, ay), region, font=BOLD(8), fill=RED)
    rw = int(d.textlength(region, font=BOLD(8))) + 6
    ay = para(d, ax + rw, ay, txt, SANS(9), COLW2 - rw, leading=10, max_lines=1)
    ay += 1

# ------------------------------------------------------------ DATE CHECK box
DY = 972
d.rectangle([MX, DY, W - MX, DY + 34], outline=RED, width=2)
d.text((MX + 6, DY + 3), "DATE CHECK — NOT TODAY'S NEWS:",
       font=BOLD(9), fill=RED)
d.text((MX + 6, DY + 16),
       "COP31 ended Sun 22 Nov with no deal  •  186 drones over Ukraine (22 Nov)  •  Iran radar claim (22 Nov)  •  Peru quake late Sun  •  Gaza truck strike Sat, 3 killed",
       font=SANS(8), fill=INK)

# ------------------------------------------------------------------- footer
d.text((MX, 1012), "SOURCES: Reuters, AP, CNN, Al Jazeera, The Hindu, Daily Star, hromadske, Xinhua, Times of India, Tribune Online, Legion.org, Just Security, Economic Times",
       font=SANS(8), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
