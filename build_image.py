#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 PNG summing up the
world's news of Tuesday 24 November 2026, newspaper front-page style.

Run:  python3 build_image.py
Writes entry.png next to this script (must stay <= 1 MiB, <= 1024x1024).

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


def kicker(draw, x, y, text, size=19):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 8


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_ship_scene(draw, x, y, w, h):
    """Flat illustration: a warship at sea with an explosion astern."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sea
    sea_y = y + int(h * 0.55)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for wx in range(0, w, 46):
        draw.arc([x + wx, sea_y + 14, x + wx + 44, sea_y + 34],
                 start=200, end=340, fill=(255, 255, 255), width=3)
    for wx in range(23, w, 46):
        draw.arc([x + wx, sea_y + 44, x + wx + 44, sea_y + 62],
                 start=200, end=340, fill=(160, 200, 225), width=3)
    # explosion behind the ship (right side)
    ex, ey = x + int(w * 0.80), sea_y - 26
    starburst(draw, ex, ey, 52, 26, 10, (255, 140, 0))
    starburst(draw, ex, ey, 34, 17, 10, (255, 205, 0))
    draw.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=(200, 30, 20))
    # smoke
    for sx, sy, sr in [(ex - 46, ey - 44, 13), (ex - 26, ey - 58, 16),
                       (ex - 2, ey - 62, 14)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
    # ship hull
    hx, hy = x + 30, sea_y - 6
    hull = [(hx, hy), (hx + 210, hy), (hx + 238, hy + 26),
            (hx + 226, hy + 34), (hx + 12, hy + 34), (hx - 6, hy + 22)]
    draw.polygon(hull, fill=(28, 43, 54))
    draw.rectangle([hx + 6, hy + 26, hx + 232, hy + 30], fill=(255, 255, 255))
    # superstructure
    draw.rectangle([hx + 44, hy - 34, hx + 150, hy], fill=(230, 232, 235))
    draw.rectangle([hx + 60, hy - 52, hx + 120, hy - 34], fill=(200, 205, 210))
    # mast + flag
    draw.line([hx + 168, hy - 34, hx + 168, hy - 56], fill=(28, 43, 54), width=4)
    draw.polygon([(hx + 168, hy - 56), (hx + 184, hy - 51),
                  (hx + 168, hy - 46)], fill=(178, 34, 34))
    # funnel
    draw.rectangle([hx + 128, hy - 46, hx + 146, hy - 34], fill=(178, 34, 34))
    # portholes
    for px in range(hx + 20, hx + 200, 26):
        draw.ellipse([px, hy + 12, px + 7, hy + 19], fill=(250, 225, 150))


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
    lx, ly, lw, lh = 36, 146, 612, 412
    card(d, lx, ly, lw, lh)
    y = kicker(d, lx + 24, ly + 20, "LEAD STORY  —  UKRAINE WAR SPILLS INTO THE MED")
    f_head = font(SERIF_B, 40)
    lines = wrap(d, "Ukraine sinks Russian warship off Libya", f_head, lw - 48)
    y = draw_lines(d, lines, lx + 24, y, f_head, INK, 50)
    draw_ship_scene(d, lx + 36, y + 10, lw - 72, 160)
    f_body = font(SANS, 22)
    sub = ("Kyiv says its drones struck Russian naval forces far from the "
           "front line — opening a new front in the Mediterranean.")
    draw_lines(d, wrap(d, sub, f_body, lw - 48), lx + 24, y + 182,
               f_body, MUTED, 29)

    # ---- right column, card A: Nvidia ----
    rx, rw = 672, 316
    ax, ay, ah = rx, 146, 204
    card(d, ax, ay, rw, ah)
    y = kicker(d, ax + 20, ay + 16, "TECH  ·  MARKETS")
    f_h2 = font(SERIF_B, 30)
    lines = wrap(d, "Huang is back at Nvidia", f_h2, rw - 40)
    y = draw_lines(d, lines, ax + 20, y, f_h2, INK, 36)
    f_s = font(SANS, 20)
    y = draw_lines(d, wrap(d, "Shares surge 31% as the Trump-backed "
                          "CEO returns.", f_s, rw - 40),
                   ax + 20, y + 4, f_s, MUTED, 26)
    d.rectangle([ax + 20, ay + ah - 28, ax + 32, ay + ah - 16], fill=GREEN)
    d.text((ax + 40, ay + ah - 30), "SK hynix +20% on the news",
           font=font(SANS_B, 17), fill=INK)

    # ---- right column, card B: Indonesia fire ----
    bx, by, bh = rx, 374, 184
    card(d, bx, by, rw, bh)
    y = kicker(d, bx + 20, by + 16, "INDONESIA")
    f_h2b = font(SERIF_B, 28)
    lines = wrap(d, "Candy factory fire kills 24", f_h2b, rw - 40)
    y = draw_lines(d, lines, bx + 20, y, f_h2b, INK, 34)
    draw_lines(d, wrap(d, "Blaze rips through the plant; rescue "
                      "under way.", f_s, rw - 40),
               bx + 20, y + 4, f_s, MUTED, 26)

    # ---- middle band: COP31 ----
    mx, my, mw, mh = 36, 582, 952, 172
    card(d, mx, my, mw, mh)
    draw_globe(d, mx + 22, my + 26, 120)
    tx = mx + 168
    y = kicker(d, tx, my + 22, "CLIMATE  —  COP31, TÜRKIYE")
    f_h3 = font(SERIF_B, 34)
    lines = wrap(d, "COP31 climate talks stall", f_h3, mw - 220)
    y = draw_lines(d, lines, tx, y, f_h3, INK, 40)
    y = draw_lines(d, wrap(d, "Nations split over fossil fuels and finance "
                          "for developing states, as Saudi Arabia is blamed "
                          "for the breakdown.", f_body, mw - 220),
                   tx, y + 4, f_body, MUTED, 29)

    # ---- trade + security band ----
    byy, bhh = 778, 130
    f_h4 = font(SERIF_B, 23)
    f_sub = font(SANS, 18)
    # left: trade
    card(d, 36, byy, 464, bhh)
    y = kicker(d, 56, byy + 14, "TRADE", size=18)
    lines = wrap(d, "Trump seals Japan & Indonesia deals", f_h4, 424)
    y = draw_lines(d, lines, 56, y, f_h4, INK, 28)
    draw_lines(d, wrap(d, "EU threatens $84bn tariff retaliation.",
                   f_sub, 424), 56, y + 4, f_sub, MUTED, 23)
    # right: security
    card(d, 524, byy, 464, bhh)
    y = kicker(d, 544, byy + 14, "SECURITY", size=18)
    lines = wrap(d, "Seoul scrambles jets", f_h4, 424)
    y = draw_lines(d, lines, 544, y, f_h4, INK, 28)
    draw_lines(d, wrap(d, "Russian military planes approach South "
                       "Korean airspace.", f_sub, 424),
               544, y + 4, f_sub, MUTED, 23)

    # ---- ticker ----
    d.rectangle([36, 920, 988, 968], fill=NAVY)
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
