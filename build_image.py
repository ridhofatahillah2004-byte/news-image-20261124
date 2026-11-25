#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 PNG summing up the
world's news of Tuesday 24 November 2026, newspaper front-page style.

Run:  python3 build_image.py
Writes entry.png next to this script (must stay <= 1 MiB, <= 1024x1024).

v2 redesign (for blind round 3):
  - Lead illustration bigger and more dramatic: larger fireball with a
    horizon glow, taller smoke plume, flames licking the deck, a drone
    silhouette overhead, and a bigger ship.
  - Stronger headline hierarchy: lead headline 46pt, red rule under each
    kicker, a big green "+31%" stat on the Nvidia card.
  - Fixed the Nvidia "SK hynix +20%" line that overflowed the card in v1.
  - Bottom band loosened: slightly larger type, cleaner spacing.
  - Same 6 stories + ticker as v1; no facts changed.

Stories (all first reported on 24 Nov 2026, from world newswires):
  1. Ukraine says its drones sank a Russian warship off Libya.
  2. Jensen Huang returns as Nvidia CEO; shares surge 31%.
  3. 24 killed in a candy factory fire in Indonesia.
  4. COP31 climate talks stall in Turkiye.
  5. Trump seals trade deals with Japan and Indonesia; EU threatens
     $84bn tariff retaliation.
  6. South Korea scrambles jets as Russian planes approach.
  Plus ticker: Himalayan flood, Bangladesh typhoid drive, UN AI call.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (14, 42, 71)
NAVY_DARK = (9, 30, 52)
RED = (178, 34, 34)
GOLD = (217, 164, 65)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
BORDER = (200, 192, 175)
SEA = (20, 72, 107)
SKY = (214, 230, 240)
GREEN = (118, 185, 0)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=19, rule=False):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=RED)
    if rule:
        draw.rectangle([x, y + size + 5, x + 64, y + size + 8], fill=RED)
        return y + size + 14
    return y + size + 8


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_ship_scene(draw, x, y, w, h):
    """Flat illustration: a warship at sea, hit by a drone strike.
    Bigger fireball, horizon glow, smoke plume, deck flames, drone."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    sea_y = y + int(h * 0.55)
    # explosion centre, just above the waterline
    ex, ey = x + int(w * 0.80), sea_y - 12
    # warm glow on the horizon behind the explosion
    for r, col in [(78, (255, 205, 130)), (60, (255, 175, 70)),
                   (46, (255, 145, 30))]:
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    # sea
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    # fire glow reflected on the water
    draw.ellipse([ex - 46, sea_y + 6, ex + 46, sea_y + 26], fill=(255, 150, 40))
    for wx in range(0, w, 46):
        draw.arc([x + wx, sea_y + 16, x + wx + 44, sea_y + 36],
                 start=200, end=340, fill=(255, 255, 255), width=3)
    for wx in range(23, w, 46):
        draw.arc([x + wx, sea_y + 48, x + wx + 44, sea_y + 66],
                 start=200, end=340, fill=(160, 200, 225), width=3)
    # explosion (bigger than v1)
    starburst(draw, ex, ey, 68, 32, 10, (255, 140, 0))
    starburst(draw, ex, ey, 46, 22, 10, (255, 205, 0))
    draw.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], fill=(200, 30, 20))
    # smoke plume
    for sx, sy, sr, col in [(ex - 62, ey - 44, 15, (110, 110, 110)),
                            (ex - 40, ey - 58, 18, (90, 90, 90)),
                            (ex - 12, ey - 62, 16, (110, 110, 110)),
                            (ex + 10, ey - 50, 13, (90, 90, 90)),
                            (ex - 76, ey - 26, 12, (110, 110, 110))]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col)
    # drone overhead (upper left) — the strike came from drones
    dx, dy = x + 64, y + 20
    draw.rectangle([dx - 9, dy - 4, dx + 9, dy + 4], fill=(45, 45, 45))
    for ox, oy in [(-18, -8), (18, -8), (-18, 8), (18, 8)]:
        draw.line([dx, dy, dx + ox, dy + oy], fill=(45, 45, 45), width=2)
        draw.ellipse([dx + ox - 6, dy + oy - 2, dx + ox + 6, dy + oy + 2],
                     fill=(45, 45, 45))
    draw.line([dx - 5, dy + 4, dx - 5, dy + 10], fill=(45, 45, 45), width=2)
    draw.line([dx + 5, dy + 4, dx + 5, dy + 10], fill=(45, 45, 45), width=2)
    # ship hull (bigger than v1)
    hx, hy = x + 24, sea_y - 8
    hull = [(hx, hy), (hx + 272, hy), (hx + 306, hy + 30),
            (hx + 292, hy + 40), (hx + 14, hy + 40), (hx - 8, hy + 26)]
    draw.polygon(hull, fill=(28, 43, 54))
    draw.rectangle([hx + 6, hy + 30, hx + 296, hy + 34], fill=(255, 255, 255))
    # superstructure
    draw.rectangle([hx + 56, hy - 40, hx + 190, hy], fill=(230, 232, 235))
    draw.rectangle([hx + 76, hy - 62, hx + 150, hy - 40], fill=(200, 205, 210))
    # mast + flag
    draw.line([hx + 216, hy - 40, hx + 216, hy - 66], fill=(28, 43, 54), width=4)
    draw.polygon([(hx + 216, hy - 66), (hx + 234, hy - 60),
                  (hx + 216, hy - 54)], fill=(178, 34, 34))
    # funnel
    draw.rectangle([hx + 164, hy - 54, hx + 186, hy - 40], fill=(178, 34, 34))
    # portholes
    for px in range(hx + 26, hx + 276, 30):
        draw.ellipse([px, hy + 14, px + 8, hy + 22], fill=(250, 225, 150))
    # flames licking the deck near the stern
    fx, fy = hx + 252, hy - 6
    starburst(draw, fx, fy, 24, 11, 8, (255, 140, 0))
    starburst(draw, fx, fy, 15, 7, 8, (255, 205, 0))
    # splash at the bow
    draw.arc([hx + 296, sea_y + 18, hx + 340, sea_y + 44],
             start=200, end=340, fill=(255, 255, 255), width=3)


def draw_flame(draw, cx, cy, s):
    """Small flame icon (orange outer, yellow inner)."""
    outer = [(cx, cy - s / 2), (cx + s * 0.30, cy - s * 0.10),
             (cx + s * 0.42, cy + s * 0.12), (cx + s * 0.28, cy + s * 0.38),
             (cx + s * 0.14, cy + s * 0.50), (cx, cy + s * 0.50),
             (cx - s * 0.14, cy + s * 0.50), (cx - s * 0.28, cy + s * 0.38),
             (cx - s * 0.42, cy + s * 0.12), (cx - s * 0.30, cy - s * 0.10)]
    draw.polygon(outer, fill=(255, 140, 0))
    k = 0.55
    inner = [(cx, cy - s * k / 2 + s * 0.12),
             (cx + s * k * 0.30, cy - s * k * 0.10 + s * 0.12),
             (cx + s * k * 0.42, cy + s * k * 0.12 + s * 0.12),
             (cx + s * k * 0.28, cy + s * k * 0.38 + s * 0.12),
             (cx, cy + s * k * 0.50 + s * 0.12),
             (cx - s * k * 0.28, cy + s * k * 0.38 + s * 0.12),
             (cx - s * k * 0.42, cy + s * k * 0.12 + s * 0.12),
             (cx - s * k * 0.30, cy - s * k * 0.10 + s * 0.12)]
    draw.polygon(inner, fill=(255, 205, 0))


def draw_globe(draw, x, y, s):
    """Flat globe icon, teal."""
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(23, 120, 140))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=0, end=360, fill=(255, 255, 255), width=2)
    draw.arc([cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8],
             start=20, end=160, fill=(255, 255, 255), width=2)


def card(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 122], fill=NAVY)
    d.rectangle([0, 122, W, 128], fill=GOLD)
    f_title = font(SERIF_B, 58)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_title)) / 2, 16), t,
           font=f_title, fill=(255, 255, 255))
    f_date = font(SANS_B, 24)
    dt = "TUESDAY  ·  24 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 84), dt,
           font=f_date, fill=GOLD)

    # ---- lead story ----
    lx, ly, lw, lh = 36, 146, 612, 426
    card(d, lx, ly, lw, lh)
    y = kicker(d, lx + 24, ly + 18, "LEAD STORY  —  UKRAINE WAR SPILLS INTO THE MED",
               rule=True)
    f_head = font(SERIF_B, 42)
    lines = wrap(d, "Ukraine sinks Russian warship off Libya", f_head, lw - 48)
    y = draw_lines(d, lines, lx + 24, y + 7, f_head, INK, 52)
    draw_ship_scene(d, lx + 36, y + 10, lw - 72, 170)
    f_body = font(SANS, 20)
    sub = ("Kyiv says its drones struck Russian naval forces far from the "
           "front line — opening a new front in the Mediterranean.")
    draw_lines(d, wrap(d, sub, f_body, lw - 48), lx + 24, y + 188,
               f_body, MUTED, 25)

    # ---- right column, card A: Nvidia ----
    rx, rw = 672, 316
    ax, ay, ah = rx, 146, 210
    card(d, ax, ay, rw, ah)
    y = kicker(d, ax + 20, ay + 14, "TECH  ·  MARKETS", rule=True)
    f_h2 = font(SERIF_B, 30)
    lines = wrap(d, "Huang is back at Nvidia", f_h2, rw - 40)
    y = draw_lines(d, lines, ax + 20, y + 5, f_h2, INK, 35)
    # big green stat: +31% shares surge
    f_stat = font(SANS_B, 34)
    d.text((ax + 20, y + 6), "+31%", font=f_stat, fill=GREEN)
    sx = ax + 20 + d.textlength("+31%", font=f_stat) + 10
    d.text((sx, y + 16), "shares surge", font=font(SANS, 20), fill=MUTED)
    y = y + 6 + 34
    draw_lines(d, wrap(d, "Trump-backed CEO returns.",
                   font(SANS, 19), rw - 40),
               ax + 20, y + 2, font(SANS, 19), MUTED, 24)
    d.rectangle([ax + 20, ay + ah - 22, ax + 32, ay + ah - 10], fill=GREEN)
    d.text((ax + 40, ay + ah - 24), "SK hynix +20%",
           font=font(SANS_B, 17), fill=INK)

    # ---- right column, card B: Indonesia fire ----
    bx, by, bh = rx, 378, 194
    card(d, bx, by, rw, bh)
    y = kicker(d, bx + 20, by + 16, "INDONESIA", rule=True)
    draw_flame(d, bx + rw - 36, by + 30, 30)
    f_h2b = font(SERIF_B, 28)
    lines = wrap(d, "Candy factory fire kills 24", f_h2b, rw - 40)
    y = draw_lines(d, lines, bx + 20, y + 5, f_h2b, INK, 34)
    f_s = font(SANS, 20)
    draw_lines(d, wrap(d, "Blaze rips through the plant; rescue "
                      "under way.", f_s, rw - 40),
               bx + 20, y + 6, f_s, MUTED, 26)

    # ---- middle band: COP31 ----
    mx, my, mw, mh = 36, 596, 952, 164
    card(d, mx, my, mw, mh)
    draw_globe(d, mx + 22, my + 26, 120)
    tx = mx + 168
    y = kicker(d, tx, my + 22, "CLIMATE  —  COP31, TÜRKIYE", rule=True)
    f_h3 = font(SERIF_B, 36)
    lines = wrap(d, "COP31 climate talks stall", f_h3, mw - 220)
    y = draw_lines(d, lines, tx, y + 5, f_h3, INK, 42)
    draw_lines(d, wrap(d, "Nations split over fossil fuels and finance "
                      "for developing states, as Saudi Arabia is blamed "
                      "for the breakdown.", font(SANS, 22), mw - 220),
               tx, y + 4, font(SANS, 22), MUTED, 29)

    # ---- trade + security band ----
    byy, bhh = 784, 126
    f_h4 = font(SERIF_B, 24)
    f_sub = font(SANS, 18)
    # left: trade
    card(d, 36, byy, 464, bhh)
    y = kicker(d, 56, byy + 12, "TRADE", size=18)
    lines = wrap(d, "Trump seals Japan & Indonesia deals", f_h4, 424)
    y = draw_lines(d, lines, 56, y + 4, f_h4, INK, 29)
    draw_lines(d, wrap(d, "EU threatens $84bn tariff retaliation.",
                   f_sub, 424), 56, y + 4, f_sub, MUTED, 23)
    # right: security
    card(d, 524, byy, 464, bhh)
    y = kicker(d, 544, byy + 12, "SECURITY", size=18)
    lines = wrap(d, "Seoul scrambles jets", f_h4, 424)
    y = draw_lines(d, lines, 544, y + 4, f_h4, INK, 29)
    draw_lines(d, wrap(d, "Russian military planes approach South "
                       "Korean airspace.", f_sub, 424),
               544, y + 4, f_sub, MUTED, 23)

    # ---- ticker ----
    d.rectangle([36, 922, 988, 968], fill=NAVY)
    tick = ("ALSO: Himalayan flood kills 4 · Bangladesh vaccinates 50m "
            "children · UN chief urges AI rules")
    size = 20
    f_tick = font(SANS_B, size)
    while d.textlength(tick, font=f_tick) > 952 - 32 and size > 14:
        size -= 1
        f_tick = font(SANS_B, size)
    while d.textlength(tick, font=f_tick) > 952 - 32:
        tick = tick[:-4].rstrip() + "…"
    d.text((36 + (952 - d.textlength(tick, font=f_tick)) / 2, 934),
           tick, font=f_tick, fill=(255, 255, 255))

    # ---- footer ----
    f_foot = font(SANS, 17)
    ft = "Compiled from world newswires  ·  Tuesday 24 November 2026"
    d.text(((W - d.textlength(ft, font=f_foot)) / 2, 980), ft,
           font=f_foot, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
