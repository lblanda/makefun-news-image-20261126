#!/usr/bin/env python3
"""Draw one 1024x1024 editorial poster summing up 26 November 2026.

Pure standard library. Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
The image is a newspaper front page: a masthead, a hero story about the
Gulf, a trade story, three regional stories, and a strip of smaller news.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
import struct
import zlib

from font5x7 import draw_text, draw_text_centered, text_width, wrap_lines
from stories import (
    ALSO_TODAY,
    FOOTER_LINE,
    HERO,
    MASTHEAD_DATE,
    MASTHEAD_TAG,
    MASTHEAD_TITLE,
    MIDDLE,
    TRADE,
)

SIZE = 1024

PAPER = (247, 240, 221)
PANEL = (255, 250, 240)
PANEL_BLUE = (232, 238, 245)
INK = (20, 24, 29)
NAVY = (16, 35, 46)
RED = (179, 32, 42)
BLUE = (29, 78, 137)
GOLD = (200, 155, 60)
GREY = (96, 92, 84)


class Poster:
    """A flat RGB canvas with simple filled-shape drawing."""

    def __init__(self, width, height, background):
        self.w = width
        self.h = height
        self.px = bytearray(width * height * 3)
        self.fill_rect(0, 0, width, height, background)

    def fill_rect(self, x, y, w, h, color):
        if w <= 0 or h <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        span = (x1 - x0) * 3
        for yy in range(y0, y1):
            off = (yy * self.w + x0) * 3
            self.px[off:off + span] = row

    def frame(self, x, y, w, h, color, thick=2):
        self.fill_rect(x, y, w, thick, color)
        self.fill_rect(x, y + h - thick, w, thick, color)
        self.fill_rect(x, y, thick, h, color)
        self.fill_rect(x + w - thick, y, thick, h, color)

    def hline(self, x, y, length, color, thick=1):
        self.fill_rect(x, y, length, thick, color)

    def vline(self, x, y, length, color, thick=1):
        self.fill_rect(x, y, thick, length, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            half = int(math.sqrt(r * r - dy * dy))
            self.fill_rect(cx - half, cy + dy, 2 * half + 1, 1, color)

    def ring(self, cx, cy, r, color):
        steps = max(24, int(2 * math.pi * r))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.fill_rect(int(cx + r * math.cos(a)),
                           int(cy + r * math.sin(a)), 2, 2, color)

    def triangle(self, x1, y1, x2, y2, x3, y3, color):
        pts = sorted(((x1, y1), (x2, y2), (x3, y3)), key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts

        def along(xa, ya, xb, yb, y):
            if yb == ya:
                return float(xa)
            return xa + (xb - xa) * (y - ya) / (yb - ya)

        for y in range(ay, cy + 1):
            if y < by:
                xl = along(ax, ay, bx, by, y)
                xr = along(ax, ay, cx, cy, y)
            else:
                xl = along(bx, by, cx, cy, y)
                xr = along(ax, ay, cx, cy, y)
            if xl > xr:
                xl, xr = xr, xl
            self.fill_rect(int(xl), y, int(xr) - int(xl) + 1, 1, color)


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(px, width, height):
    """Encode flat RGB bytes as a deterministic PNG (filter 0 rows)."""
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    return png


def _kicker(p, x, y, text, color, scale=2):
    draw_text(p.px, p.w, x, y, text, color, scale)


def _headline(p, x, y, max_w, text, color=INK, scale=2):
    lines = wrap_lines(text, max_w, scale)
    for i, line in enumerate(lines):
        draw_text(p.px, p.w, x, y + i * (7 * scale + 6), line, color, scale)
    return y + len(lines) * (7 * scale + 6)


def _body(p, x, y, lines, max_w, color=INK, scale=2, gap=6):
    """Draw body lines, wrapping any that are too wide for max_w."""
    flat = []
    for line in lines:
        flat.extend(wrap_lines(line, max_w, scale))
    for i, line in enumerate(flat):
        draw_text(p.px, p.w, x, y + i * (7 * scale + gap), line, color, scale)
    return y + len(flat) * (7 * scale + gap)


def _refinery(p, x, base_y):
    """Three refinery towers, a flame, a tanker and a sea mine."""
    p.fill_rect(x, base_y - 58, 24, 58, INK)
    p.fill_rect(x + 34, base_y - 78, 24, 78, INK)
    p.fill_rect(x + 68, base_y - 48, 24, 48, INK)
    p.fill_rect(x, base_y - 6, 92, 6, GOLD)
    p.triangle(x + 38, base_y - 108, x + 30, base_y - 80,
               x + 54, base_y - 80, RED)
    # Tanker hull and bridge.
    p.fill_rect(x + 130, base_y - 26, 150, 26, BLUE)
    p.triangle(x + 280, base_y - 26, x + 306, base_y - 12,
               x + 280, base_y, BLUE)
    p.fill_rect(x + 240, base_y - 50, 26, 24, INK)
    p.fill_rect(x + 240, base_y - 58, 26, 4, RED)
    # A spiked sea mine bobbing beside the tanker.
    mx, my = x + 340, base_y - 12
    for dx, dy in ((0, -14), (0, 14), (-14, 0), (14, 0),
                   (-10, -10), (10, -10), (-10, 10), (10, 10)):
        p.fill_rect(mx + dx - 1, my + dy - 1, 3, 3, INK)
    p.disc(mx, my, 11, INK)
    p.disc(mx - 3, my - 3, 3, PAPER)


def _stars(p, cx, cy, r, color):
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        p.disc(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), 3, color)


def _rocket(p, cx, base_y):
    p.triangle(cx - 12, base_y - 78, cx, base_y - 104, cx + 12, base_y - 78, RED)
    p.fill_rect(cx - 12, base_y - 78, 24, 56, INK)
    p.fill_rect(cx - 4, base_y - 66, 8, 8, PAPER)
    p.triangle(cx - 12, base_y - 40, cx - 26, base_y - 14, cx - 12, base_y - 22, RED)
    p.triangle(cx + 12, base_y - 40, cx + 26, base_y - 14, cx + 12, base_y - 22, RED)
    p.triangle(cx - 7, base_y - 22, cx + 7, base_y - 22, cx, base_y - 2, GOLD)


def _radar(p, cx, cy):
    for r in (16, 28, 40):
        p.ring(cx, cy, r, BLUE)
    p.fill_rect(cx - 1, cy - 40, 2, 40, BLUE)
    p.disc(cx + 20, cy - 20, 5, RED)
    p.disc(cx, cy, 4, INK)


def build():
    p = Poster(SIZE, SIZE, PAPER)

    # Outer double rule.
    p.frame(10, 10, SIZE - 20, SIZE - 20, INK, 3)
    p.frame(20, 20, SIZE - 40, SIZE - 40, INK, 1)

    # Masthead: navy band, title, date, tag line.
    p.fill_rect(24, 24, SIZE - 48, 128, NAVY)
    draw_text_centered(p.px, p.w, SIZE // 2, 44, MASTHEAD_TITLE, PAPER, 4)
    p.hline(212, 88, SIZE - 424, GOLD, 2)
    draw_text_centered(p.px, p.w, SIZE // 2, 100, MASTHEAD_DATE, GOLD, 2)
    draw_text_centered(p.px, p.w, SIZE // 2, 128, MASTHEAD_TAG, PAPER, 1)
    p.hline(24, 158, SIZE - 48, RED, 4)

    # ---- Hero: the Gulf story, left; trade story, right. ----
    p.fill_rect(24, 172, 628, 300, PANEL)
    p.frame(24, 172, 628, 300, INK, 2)
    _kicker(p, 44, 190, HERO[0], RED, 2)
    _headline(p, 44, 220, 588, HERO[1], INK, 3)
    _body(p, 44, 252, HERO[2], 588, INK, 2, 8)
    _refinery(p, 60, 448)

    p.fill_rect(676, 172, 300, 300, PANEL_BLUE)
    p.frame(676, 172, 300, 300, INK, 2)
    _kicker(p, 696, 190, TRADE[0], BLUE, 2)
    _headline(p, 696, 220, 260, TRADE[1], INK, 2)
    p.triangle(924, 424, 906, 452, 942, 452, RED)
    p.fill_rect(920, 452, 8, 14, RED)
    _body(p, 696, 336, TRADE[2], 260, INK, 2, 8)

    # ---- Middle row: three regional stories. ----
    mid_y = 492
    mid_h = 258
    panel_w = 312
    for i, story in enumerate(MIDDLE):
        x = 24 + i * (panel_w + 20)
        p.fill_rect(x, mid_y, panel_w, mid_h, PANEL)
        p.frame(x, mid_y, panel_w, mid_h, INK, 2)
        accent = (BLUE, RED, NAVY)[i]
        _kicker(p, x + 20, mid_y + 18, story[0], accent, 2)
        end_y = _headline(p, x + 20, mid_y + 48, panel_w - 40, story[1], INK, 2)
        _body(p, x + 20, end_y + 8, story[2], panel_w - 40, INK, 2, 8)
        cx = x + panel_w // 2
        if i == 0:
            _stars(p, cx, mid_y + 208, 30, BLUE)
        elif i == 1:
            _rocket(p, cx, mid_y + 240)
        else:
            _radar(p, cx, mid_y + 214)

    # ---- Bottom strip: smaller news of the day. ----
    p.hline(24, 782, SIZE - 48, INK, 2)
    _kicker(p, 24, 798, "ALSO TODAY", RED, 2)
    col_w = 236
    for i, (head, sub) in enumerate(ALSO_TODAY):
        x = 24 + i * (col_w + 8)
        if i:
            p.vline(x - 8, 798, 128, GREY, 1)
        y = _headline(p, x, 834, col_w - 12, head, INK, 1)
        _body(p, x, y + 4, (sub,), col_w - 12, GREY, 1, 4)
    # Dateline: the cities this day's news came from.
    draw_text_centered(p.px, p.w, SIZE // 2, 898,
                       "RIYADH  •  HORMUZ  •  BRUSSELS  •  SEOUL  •  "
                       "KYIV  •  CAIRO  •  NEW YORK", GREY, 1)

    # Footer.
    p.hline(24, 958, SIZE - 48, INK, 2)
    draw_text_centered(p.px, p.w, SIZE // 2, 976, FOOTER_LINE, INK, 1)
    return p


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the contents of the output directory, never the dir itself.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
    poster = build()
    data = encode_png(poster.px, poster.w, poster.h)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
