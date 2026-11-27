#!/usr/bin/env python3
"""Draw a 1024x1024 editorial news poster summing up the world news of
Thursday 26 November 2026, and write it to /output/entry.png.

Pure Python 3 standard library: a hand-written PNG encoder (zlib + CRC32),
a small raster canvas and a 5x7 bitmap font. No network, no third-party
packages, no clock or randomness — two runs write the same bytes.
"""

import os
import sys

# The grader runs `python3 -P -s /bot/main.py`, and -P keeps the script
# directory off sys.path, so sibling imports need this bootstrap first.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
import struct
import zlib

from font5x7 import glyph_rows, text_width
import stories

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 231)
INK = (22, 32, 54)
RED = (192, 57, 43)
GOLD = (201, 162, 39)
TEAL = (31, 122, 110)
SKY = (141, 182, 205)
SKY_DARK = (70, 120, 150)
ORANGE = (230, 126, 34)
YELLOW = (241, 196, 15)
GREEN = (39, 174, 96)
WHITE = (255, 255, 255)
GREY = (110, 110, 100)

WIDTH = 1024
HEIGHT = 1024


# ------------------------------------------------------------------- PNG
def _chunk(kind, data):
    body = kind + data
    return (
        struct.pack(">I", len(data))
        + body
        + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    )


def encode_png(width, height, pixels):
    """pixels: bytes of RGB triples, row-major. Returns whole PNG bytes."""
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter: none
        raw += pixels[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, width, height, background):
        self.w = width
        self.h = height
        self.pixels = bytearray(background * (width * height))

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.pixels[i] = color[0]
            self.pixels[i + 1] = color[1]
            self.pixels[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            row = bytes(color) * (x1 - x0)
            self.pixels[base:base + (x1 - x0) * 3] = row

    def hline(self, x0, x1, y, color, thick=1):
        self.fill_rect(min(x0, x1), y, abs(x1 - x0) + 1, thick, color)

    def vline(self, x, y0, y1, color, thick=1):
        self.fill_rect(x, min(y0, y1), thick, abs(y1 - y0) + 1, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            dx2 = r * r - dy * dy
            if dx2 < 0:
                continue
            dx = int(dx2 ** 0.5)
            self.fill_rect(cx - dx, y, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, thick, inner):
        self.fill_circle(cx, cy, r, color)
        self.fill_circle(cx, cy, r - thick, inner)

    def ellipse_outline(self, cx, cy, rx, ry, color):
        steps = max(48, 4 * (rx + ry))
        for i in range(steps + 1):
            a = 2.0 * math.pi * i / steps
            x = int(cx + rx * math.cos(a))
            y = int(cy + ry * math.sin(a))
            self.fill_rect(x - 1, y - 1, 3, 3, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        if ay == cy:
            return

        def interp(y, xt, yt, xb, yb):
            if yb == yt:
                return float(xt)
            return xt + (xb - xt) * (y - yt) / (yb - yt)

        for y in range(ay, cy + 1):
            if y < by:
                xa = interp(y, ax, ay, bx, by)
                xb = interp(y, ax, ay, cx, cy)
            else:
                xa = interp(y, bx, by, cx, cy)
                xb = interp(y, ax, ay, cx, cy)
            lo = int(min(xa, xb))
            hi = int(max(xa, xb))
            self.fill_rect(lo, y, hi - lo + 1, 1, color)

    def text(self, s, x, y, scale, color):
        # The font covers capitals only, so all poster copy renders upper
        # case even when a story line was written in sentence case.
        cx = x
        for ch in s.upper():
            rows = glyph_rows(ch)
            for ry, row in enumerate(rows):
                for rx, bit in enumerate(row):
                    if bit == "#":
                        self.fill_rect(
                            cx + rx * scale, y + ry * scale,
                            scale, scale, color,
                        )
            cx += 6 * scale

    def text_centered(self, s, cx, y, scale, color):
        self.text(s, cx - text_width(s, scale) // 2, y, scale, color)


# ------------------------------------------------------------------ icons
def _flame(cv, cx, y_top, w, h):
    """A two-tone flame whose tip is at (cx, y_top)."""
    cv.fill_triangle(cx - w, y_top + h, cx + w, y_top + h, cx, y_top, ORANGE)
    cv.fill_triangle(
        cx - w // 2, y_top + h, cx + w // 2, y_top + h, cx, y_top + h // 2,
        YELLOW,
    )


def icon_globe(cv, x, y):
    """A globe with a red 20% tariff badge, for the tariffs panel."""
    cx, cy, r = x + 32, y + 44, 34
    cv.fill_circle(cx, cy, r, SKY)
    cv.ring(cx, cy, r, INK, 3, SKY)
    cv.ellipse_outline(cx, cy, 12, r, SKY_DARK)
    cv.ellipse_outline(cx, cy, 24, r, SKY_DARK)
    cv.vline(cx, cy - r, cy + r, SKY_DARK)
    for dy in (-16, 0, 16):
        dx = int((r * r - dy * dy) ** 0.5)
        cv.hline(cx - dx, cx + dx, cy + dy, SKY_DARK, 2)
    cv.fill_circle(cx - 14, cy - 12, 6, GREEN)
    cv.fill_circle(cx + 12, cy + 12, 7, GREEN)
    bx, by, br = x + 48, y + 14, 19
    cv.ring(bx, by, br, WHITE, 2, RED)
    cv.text_centered("20%", bx, by - 7, 2, WHITE)


def icon_bank(cv, x, y):
    """A classical bank facade, for the ECB panel. Fits ~64x96 at (x, y)."""
    cx = x + 32
    cv.fill_triangle(x + 4, y + 26, x + 60, y + 26, cx, y + 4, GOLD)
    cv.fill_circle(cx, y + 18, 5, INK)
    cv.fill_rect(x + 4, y + 26, 56, 5, INK)
    for px in (8, 24, 40):
        cv.fill_rect(x + px, y + 31, 8, 44, INK)
    cv.fill_rect(x + 2, y + 75, 60, 6, INK)
    cv.fill_rect(x + 8, y + 81, 48, 5, INK)


def icon_missile(cv, x, y):
    """A missile climbing with a flame trail, for the Korea panel."""
    cx = x + 32
    cv.fill_triangle(cx - 9, y + 24, cx + 9, y + 24, cx, y + 2, RED)
    cv.fill_rect(cx - 9, y + 24, 18, 36, WHITE)
    cv.vline(cx - 9, y + 24, y + 60, INK)
    cv.vline(cx + 9, y + 24, y + 60, INK)
    cv.hline(cx - 9, cx + 9, y + 60, INK, 2)
    cv.fill_circle(cx, y + 40, 5, SKY)
    cv.fill_circle(cx, y + 40, 2, INK)
    cv.fill_triangle(cx - 9, y + 50, cx - 20, y + 68, cx - 9, y + 60, RED)
    cv.fill_triangle(cx + 9, y + 50, cx + 20, y + 68, cx + 9, y + 60, RED)
    cv.fill_triangle(cx - 6, y + 62, cx + 6, y + 62, cx, y + 88, ORANGE)
    cv.fill_triangle(cx - 3, y + 62, cx + 3, y + 62, cx, y + 78, YELLOW)


def icon_awacs(cv, x, y):
    """A radar plane (AWACS) in profile, for the Ukraine panel."""
    cx = x + 32
    cv.fill_circle(cx, y + 22, 12, SKY)
    cv.ring(cx, y + 22, 12, INK, 2, SKY)
    cv.vline(cx, y + 34, y + 46, INK, 3)
    cv.fill_rect(x + 4, y + 46, 56, 12, INK)
    cv.fill_triangle(x + 60, y + 46, x + 60, y + 58, x + 72, y + 52, INK)
    cv.fill_triangle(x + 4, y + 46, x + 4, y + 58, x - 6, y + 52, INK)
    cv.fill_triangle(cx - 4, y + 46, cx + 10, y + 46, cx + 3, y + 70, INK)
    cv.fill_triangle(cx + 2, y + 58, cx + 16, y + 58, cx + 9, y + 76, INK)
    cv.fill_rect(x + 52, y + 49, 10, 4, GOLD)


def draw_lead_art(cv):
    """The lead illustration: a refinery tower in flames above a tanker
    on the sea, with a sea mine drifting beside it. Occupies x 690..1000,
    y 130..400."""
    # Sky: a low sun and a smoke plume drifting clear of the tower flame.
    cv.fill_circle(940, 168, 26, GOLD)
    cv.fill_circle(788, 142, 12, GREY)
    cv.fill_circle(802, 124, 9, GREY)
    cv.fill_circle(776, 120, 8, GREY)
    # Refinery tower with a flame on top.
    tx = 716
    _flame(cv, tx + 22, 128, 18, 30)
    cv.fill_rect(tx, 158, 44, 8, INK)
    cv.fill_rect(tx + 4, 166, 36, 150, INK)
    for wy in (182, 208, 234, 260, 286):
        cv.fill_rect(tx + 10, wy, 8, 10, GOLD)
        cv.fill_rect(tx + 26, wy, 8, 10, GOLD)
    # Sea.
    cv.fill_rect(688, 316, 312, 84, TEAL)
    cv.hline(688, 1000, 316, SKY_DARK, 3)
    cv.hline(700, 780, 344, WHITE, 2)
    cv.hline(880, 980, 360, WHITE, 2)
    cv.hline(740, 830, 378, WHITE, 2)
    # Tanker on the sea.
    cv.fill_rect(716, 330, 150, 34, RED)
    cv.fill_rect(716, 330, 150, 6, WHITE)
    cv.fill_rect(866, 322, 26, 42, INK)
    cv.fill_rect(730, 318, 26, 12, GOLD)
    cv.fill_rect(766, 318, 26, 12, GOLD)
    cv.fill_rect(802, 318, 26, 12, GOLD)
    cv.fill_triangle(716, 364, 700, 380, 716, 380, INK)
    cv.fill_triangle(866, 364, 892, 380, 892, 364, INK)
    # Sea mine drifting beside the tanker.
    mx, my, mr = 946, 348, 16
    cv.fill_circle(mx, my, mr, INK)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x1 = int(mx + (mr - 2) * math.cos(a))
        y1 = int(my + (mr - 2) * math.sin(a))
        x2 = int(mx + (mr + 9) * math.cos(a))
        y2 = int(my + (mr + 9) * math.sin(a))
        cv.line(x1, y1, x2, y2, INK)
    cv.fill_circle(mx, my, 5, GOLD)


# ----------------------------------------------------------------- poster
def draw_panel(cv, x0, y0, story, icon, compact=False):
    """One of the four smaller story panels (460 wide).

    The bottom row is shorter (its strip starts at y=928), so it uses a
    compact layout: tighter kicker, headline and deck spacing.
    """
    if compact:
        kick, head, hpitch, deck, dpitch, rule = 8, 30, 26, 124, 20, 206
        icon_y = y0 + 2
    else:
        kick, head, hpitch, deck, dpitch, rule = 12, 38, 28, 140, 24, 244
        icon_y = y0 + 4
    cv.text(story["kicker"], x0, y0 + kick, 2, RED)
    y = y0 + head
    for line in story["headline"]:
        cv.text(line, x0, y, 3, INK)
        y += hpitch
    y = y0 + deck
    for line in story["deck"]:
        cv.text(line, x0, y, 2, INK)
        y += dpitch
    cv.hline(x0, x0 + 459, y0 + rule, GOLD, 2)
    icon(cv, x0 + 396, icon_y)


def draw_poster(cv):
    # Masthead.
    cv.fill_rect(0, 0, WIDTH, 104, INK)
    cv.text_centered(stories.MASTHEAD_TITLE, WIDTH // 2, 22, 4, WHITE)
    cv.text_centered(stories.MASTHEAD_DATE, WIDTH // 2, 64, 2, GOLD)
    cv.fill_rect(0, 104, WIDTH, 6, RED)

    # Lead story: the Gulf war widens.
    lead = stories.LEAD
    cv.text(lead["kicker"], 28, 128, 2, RED)
    y = 156
    for line in lead["headline"]:
        cv.text(line, 28, y, 4, INK)
        y += 36
    y = 312
    for line in lead["deck"]:
        cv.text(line, 28, y, 2, INK)
        y += 20
    draw_lead_art(cv)

    # Dividers and the four panels.
    cv.hline(24, 1000, 416, GREY, 2)
    cv.hline(24, 1000, 696, GREY, 2)
    cv.vline(512, 424, 688, GREY, 2)
    cv.vline(512, 704, 920, GREY, 2)
    draw_panel(cv, 28, 424, stories.PANEL_TARIFFS, icon_globe)
    draw_panel(cv, 536, 424, stories.PANEL_EUROPE, icon_bank)
    draw_panel(cv, 28, 704, stories.PANEL_KOREA, icon_missile, compact=True)
    draw_panel(cv, 536, 704, stories.PANEL_UKRAINE, icon_awacs, compact=True)

    # Bottom strip: four more stories from the same day.
    cv.fill_rect(0, 928, WIDTH, 88, INK)
    cv.text(stories.STRIP_LABEL, 28, 940, 2, GOLD)
    y = 966
    for line in stories.STRIP_LINES:
        cv.text(line, 28, y, 2, WHITE)
        y += 24


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the contents of the output directory, never the directory
    # itself: it may be a mount point the grader owns.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path):
            os.remove(path)
    cv = Canvas(WIDTH, HEIGHT, PAPER)
    draw_poster(cv)
    png = encode_png(WIDTH, HEIGHT, bytes(cv.pixels))
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
