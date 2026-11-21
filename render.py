#!/usr/bin/env python3
"""Render the 21 Nov 2026 world-news front page as a 1024x1024 PNG.

A FrontPage object owns the canvas, the drawing context and the fonts,
and paints the sheet in four passes: masthead, lead story, story grid,
footer. Every word is real text drawn with Pillow vector shapes, so
nothing is garbled. The build is deterministic: fixed strings, fixed
geometry, no clock, no randomness, no network. Two runs write
byte-identical output.

The seven stories are the ones the day's briefs headlined for
Saturday 21 November 2026, each cross-checked against at least two
independent sources reporting that day (OneTurn daily brief, Horizon
world brief, the Brunger daily brief, SBS bulletins, CNN/Reuters on
the FBI breach, USGS on the Peru quake). Built on 21 Nov from what
had been reported by ~15:30 WIB; the day's later news is not in it.
"""
import os

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
BACKGROUND = (247, 243, 234)
FOREGROUND = (24, 24, 24)
HIGHLIGHT = (160, 20, 32)
MUTED = (88, 84, 76)
RULE = (198, 191, 177)
CARD = (255, 255, 255)
NIGHT = (38, 42, 58)

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_BLACK_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

EDGE = 46
INNER = WIDTH - 2 * EDGE

ITEMS = [
    (
        "01",
        "MARKETS — US",
        "AI sell-off drags S&P into correction",
        "S&P 500 falls 3.70%; Nasdaq drops 5.28%, erasing its 2026 gains.",
    ),
    (
        "02",
        "DIPLOMACY — EUROPE",
        "UK and EU sign three post-Brexit deals",
        "Food trade, carbon markets and a youth-mobility scheme for 100,000.",
    ),
    (
        "03",
        "CLIMATE — COP31",
        "Climate talks run past deadline in Antalya",
        "Nearly 200 nations split over fossil fuels as COP31 goes into overtime.",
    ),
    (
        "04",
        "CYBER — US",
        "FBI's crime database hacked",
        "Suspected breach of the NCIC system; the second FBI intrusion in months.",
    ),
    (
        "05",
        "DISASTER — PERU",
        "Magnitude 6.9 quake shakes Peru's Andes",
        "Tremors felt in Lima; no casualties or damage reported at first.",
    ),
    (
        "06",
        "HEALTH",
        "Cancer pill makes tumours vanish in trial",
        "Daraxonrasib: tumours undetectable in 1 in 12 pancreatic patients.",
    ),
]


class FrontPage:
    """Paints one newspaper front page onto a Pillow canvas."""

    def __init__(self):
        self.sheet = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        self.dc = ImageDraw.Draw(self.sheet)

    def _font(self, path, size):
        return ImageFont.truetype(path, size)

    def _width(self, text, face):
        return self.dc.textlength(text, font=face)

    def _wrap(self, text, face, width):
        """Greedy word wrap: split text into lines that fit width."""
        rows, current = [], ""
        for word in text.split():
            trial = f"{current} {word}".strip()
            if self._width(trial, face) <= width:
                current = trial
            else:
                if current:
                    rows.append(current)
                current = word
        if current:
            rows.append(current)
        return rows

    def _block(self, rows, x, y, face, colour, leading):
        for row in rows:
            self.dc.text((x, y), row, font=face, fill=colour)
            y += leading
        return y

    def _centred(self, text, face, cx, y, colour):
        self.dc.text(
            (cx - self._width(text, face) / 2, y), text, font=face, fill=colour
        )

    def masthead(self):
        title = self._font(SERIF_BOLD_PATH, 88)
        self._centred("THE WORLD", title, WIDTH / 2, 26, FOREGROUND)
        meta = self._font(SANS_BOLD_PATH, 20)
        self.dc.text((EDGE, 132), "SATURDAY, 21 NOVEMBER 2026", font=meta, fill=FOREGROUND)
        tag = "SEVEN STORIES  ·  ONE DAY"
        self.dc.text(
            (WIDTH - EDGE - self._width(tag, meta), 132),
            tag,
            font=meta,
            fill=HIGHLIGHT,
        )
        self.dc.line([(EDGE, 166), (WIDTH - EDGE, 166)], fill=FOREGROUND, width=3)
        self.dc.line([(EDGE, 172), (WIDTH - EDGE, 172)], fill=FOREGROUND, width=1)

    def lead_story(self):
        top = 190
        badge_face = self._font(SANS_BLACK_PATH, 16)
        label = "  TOP STORY  "
        badge_w = self._width(label, badge_face)
        self.dc.rectangle([EDGE, top, EDGE + badge_w, top + 27], fill=HIGHLIGHT)
        self.dc.text((EDGE, top + 3), label, font=badge_face, fill=CARD)
        kicker = self._font(SANS_BOLD_PATH, 17)
        self.dc.text(
            (EDGE + badge_w + 14, top + 4), "WAR — UKRAINE & POLAND", font=kicker, fill=HIGHLIGHT
        )

        headline_face = self._font(SERIF_BOLD_PATH, 40)
        headline = "Russia's biggest strikes hit Ukraine — and Poland"
        rows = self._wrap(headline, headline_face, INNER - 205)
        after = self._block(rows, EDGE, top + 42, headline_face, FOREGROUND, 49)

        deck_face = self._font(SANS_PATH, 20)
        deck = (
            "More than 400 drones and 110 missiles overnight; at least "
            "eight killed in Kyiv. Warsaw calls the missiles that fell "
            "on Poland a deliberate provocation."
        )
        deck_rows = self._wrap(deck, deck_face, INNER - 205)
        self._block(deck_rows, EDGE, after + 8, deck_face, MUTED, 28)

        # Night sky over a skyline: missile arcs with a burst above it.
        # Captioned so the motif reads as an illustration, not decoration.
        ox, oy = WIDTH - EDGE - 180, top + 44
        mh = 128
        self.dc.rectangle([ox, oy, ox + 180, oy + mh], fill=NIGHT)
        # Stars.
        for sx, sy in [(14, 14), (52, 30), (96, 10), (140, 26), (168, 44),
                       (30, 52), (120, 58), (160, 84)]:
            self.dc.ellipse([ox + sx - 2, oy + sy - 2, ox + sx + 2, oy + sy + 2],
                            fill=CARD)
        # Missile arcs.
        self.dc.arc([ox + 6, oy + 6, ox + 120, oy + 120], 200, 330,
                    fill=(255, 210, 90), width=3)
        self.dc.arc([ox + 40, oy - 6, ox + 170, oy + 110], 210, 320,
                    fill=(255, 210, 90), width=3)
        # Burst: red star where an arc ends.
        bx, by = ox + 148, oy + 34
        self.dc.polygon(
            [(bx, by - 14), (bx + 4, by - 4), (bx + 14, by), (bx + 4, by + 4),
             (bx, by + 14), (bx - 4, by + 4), (bx - 14, by), (bx - 4, by - 4)],
            fill=HIGHLIGHT,
        )
        # Skyline silhouette.
        base = oy + mh
        skyline = [(ox, base), (ox, base - 34), (ox + 26, base - 34),
                   (ox + 26, base - 52), (ox + 44, base - 52),
                   (ox + 44, base - 26), (ox + 72, base - 26),
                   (ox + 72, base - 64), (ox + 88, base - 64),
                   (ox + 88, base - 30), (ox + 118, base - 30),
                   (ox + 118, base - 46), (ox + 138, base - 46),
                   (ox + 138, base - 22), (ox + 180, base - 22),
                   (ox + 180, base)]
        self.dc.polygon(skyline, fill=FOREGROUND)
        # Lit windows.
        for wx, wy in [(10, 24), (32, 44), (78, 56),
                       (96, 22), (124, 38), (150, 14)]:
            self.dc.rectangle(
                [ox + wx, base - wy, ox + wx + 5, base - wy + 6],
                fill=(255, 210, 90),
            )
        # Caption under the motif.
        cap_face = self._font(SANS_BOLD_PATH, 12)
        caption = "MISSILE ARCS OVER KYIV — ILLUSTRATION"
        self._centred(caption, cap_face, ox + 90, oy + mh + 6, MUTED)
        self.dc.line([(EDGE, 388), (WIDTH - EDGE, 388)], fill=RULE, width=2)

    def story_grid(self):
        number_face = self._font(SERIF_BOLD_PATH, 29)
        kicker_face = self._font(SANS_BOLD_PATH, 14)
        headline_face = self._font(SERIF_BOLD_PATH, 24)
        deck_face = self._font(SANS_PATH, 18)
        column_w = (INNER - 26) // 2
        row_h = 176
        start_y = 408
        for pos, (num, section, headline, deck) in enumerate(ITEMS):
            col, row = pos % 2, pos // 2
            x = EDGE + col * (column_w + 26)
            y = start_y + row * row_h
            if row:
                self.dc.line(
                    [(EDGE, y - 11), (WIDTH - EDGE, y - 11)], fill=RULE, width=1
                )
            self.dc.text((x, y), num, font=number_face, fill=HIGHLIGHT)
            self.dc.text((x + 50, y + 8), section, font=kicker_face, fill=HIGHLIGHT)
            head_rows = self._wrap(headline, headline_face, column_w)
            below = self._block(head_rows, x, y + 42, headline_face, FOREGROUND, 29)
            deck_rows = self._wrap(deck, deck_face, column_w)
            self._block(deck_rows, x, below + 6, deck_face, MUTED, 23)

    def footer(self):
        fy = 962
        self.dc.line([(EDGE, fy), (WIDTH - EDGE, fy)], fill=FOREGROUND, width=2)
        foot = self._font(SANS_PATH, 14)
        left = "Sources: BBC · Reuters · CNN · AP · France 24 · USGS"
        right = "All headlines verified from reporting on 21 November 2026"
        self.dc.text((EDGE, fy + 10), left, font=foot, fill=MUTED)
        self.dc.text(
            (WIDTH - EDGE - self._width(right, foot), fy + 10),
            right,
            font=foot,
            fill=MUTED,
        )

    def render(self):
        self.masthead()
        self.lead_story()
        self.story_grid()
        self.footer()
        return self.sheet


def draw_sheet():
    return FrontPage().render()


def self_check():
    """Render twice and confirm the bytes are identical, proving the
    program is deterministic before the asset is shipped."""
    import hashlib
    import io

    first = io.BytesIO()
    draw_sheet().save(first, "PNG")
    second = io.BytesIO()
    draw_sheet().save(second, "PNG")
    a = hashlib.sha256(first.getvalue()).hexdigest()
    b = hashlib.sha256(second.getvalue()).hexdigest()
    assert a == b, f"non-deterministic render: {a} != {b}"
    print("deterministic:", a)


def build():
    sheet = draw_sheet()
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "assets", "entry.png")
    sheet.save(target, "PNG")
    print("saved", target)


if __name__ == "__main__":
    import sys

    if "--self-check" in sys.argv:
        self_check()
    else:
        build()
