#!/usr/bin/env python3
"""Compose the 19 November 2026 world-news front page (1024x1024).

Two text-free illustrations live in assets/ (Shenzhen at dusk, a neon
Vice City street). Every headline, deck, date and label is drawn here
with PIL so the words stay crisp. Deterministic: fixed inputs, no clock,
no randomness. Writes entry.png next to this file; if the PNG would pass
1 MiB it writes JPEG bytes instead (same filename).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MARGIN = 20
INNER = W - 2 * MARGIN

PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (15, 30, 51)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fonts = {}


def get_font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def wrap_text(draw, text, font, max_width):
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def shrink_to_fit(draw, text, path, size, max_width):
    while size > 10 and draw.textlength(
            text, font=get_font(path, size)) > max_width:
        size -= 1
    return get_font(path, size)


def cover_crop(image, width, height):
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    grown = image.resize((round(src_w * scale), round(src_h * scale)),
                         Image.LANCZOS)
    left = (grown.width - width) // 2
    top = (grown.height - height) // 2
    return grown.crop((left, top, left + width, top + height))


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=21):
    draw.text((x, y), text, font=get_font(SANS_BOLD, size), fill=RED)


def headline(draw, x, y, text, size, width, leading, fill=INK):
    font = get_font(SERIF_BOLD, size)
    return draw_lines(draw, x, y, wrap_text(draw, text, font, width),
                      font, fill, leading)


def deck(draw, x, y, text, size, width, leading):
    font = get_font(SANS, size)
    return draw_lines(draw, x, y, wrap_text(draw, text, font, width),
                      font, GREY, leading)


def build():
    summit = Image.open(os.path.join(
        ASSETS,
        "media-generation-summit-hero-0-89f84d1a-6847-4680-a90f-dada009896eb.webp"))
    vice = Image.open(os.path.join(
        ASSETS,
        "media-generation-vice-city-hero-0-f19fcf57-c12e-4d98-98c2-3edebda78b7f.webp"))

    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # Masthead.
    d.rectangle([4, 4, W - 5, 108], fill=NAVY)
    tag = "T H E   W O R L D   I N   O N E   P A G E"
    tag_font = get_font(SANS_BOLD, 23)
    d.text(((W - d.textlength(tag, font=tag_font)) / 2, 16),
           tag, font=tag_font, fill=GOLD)
    date = "THURSDAY, 19 NOVEMBER 2026"
    date_font = shrink_to_fit(d, date, SERIF_BOLD, 56, INNER - 10)
    d.text(((W - d.textlength(date, font=date_font)) / 2, 46),
           date, font=date_font, fill=WHITE)
    d.rectangle([4, 108, W - 5, 114], fill=RED)

    # Lead: APEC summit photo, headline, deck.
    page.paste(cover_crop(summit, INNER, 230), (MARGIN, 126))
    d.rectangle([MARGIN, 126, MARGIN + INNER - 1, 126 + 230 - 1],
                outline=INK, width=2)
    y = 370
    kicker(d, MARGIN, y, "APEC  •  LEAD STORY")
    y = headline(d, MARGIN, 396,
                 "FIRST-EVER TRUMP–XI–PUTIN SUMMIT OPENS IN SHENZHEN",
                 33, INNER, 38)
    y += 6
    deck(d, MARGIN, y,
         "The three leaders meet face to face for the first time at the "
         "APEC summit, with nuclear arms and AI on the agenda.",
         21, INNER, 27)

    d.line([(MARGIN, 556), (MARGIN + INNER, 556)], fill=INK, width=2)

    # Second row: GTA VI photo plus story.
    y0 = 570
    page.paste(cover_crop(vice, 300, 170), (MARGIN, y0))
    d.rectangle([MARGIN, y0, MARGIN + 300 - 1, y0 + 170 - 1],
                outline=INK, width=2)
    tx = MARGIN + 300 + 22
    tw = INNER - 300 - 22
    kicker(d, tx, y0, "GAMING  •  CULTURE", size=19)
    y = headline(d, tx, y0 + 26, "GTA VI ROLLS OUT WORLDWIDE",
                 33, tw, 38)
    deck(d, tx, y + 4,
         "Gamers return to Vice City as the long-awaited sequel launches "
         "for PlayStation 5 and Xbox; millions expected to play on day one.",
         21, tw, 27)

    d.line([(MARGIN, 754), (MARGIN + INNER, 754)], fill=INK, width=2)

    # Third row: two panels.
    col = (INNER - 24) // 2
    y0 = 768
    kicker(d, MARGIN, y0, "BUSINESS", size=19)
    y = headline(d, MARGIN, y0 + 26, "ANTHROPIC PRICES MEGA IPO",
                 28, col, 33)
    deck(d, MARGIN, y + 4,
         "The Claude maker prices its Nasdaq debut as ANT, one of the "
         "biggest listings ever, with Amazon and Google among its backers.",
         20, col, 26)

    rx = MARGIN + col + 24
    kicker(d, rx, y0, "LAW", size=19)
    y = headline(d, rx, y0 + 26,
                 "WORLD COURT RULES ON ROHINGYA GENOCIDE", 28, col, 33)
    deck(d, rx, y + 4,
         "The ICJ delivers its verdict in The Gambia v. Myanmar — the "
         "first time a state could be found guilty of genocide.",
         20, col, 26)

    # Footer ticker.
    d.rectangle([4, 952, W - 5, 1020], fill=NAVY)
    foot_font = get_font(SANS, 19)
    ticker = ("ALSO:  Crimea bridge hit again  •  Israeli tanks cross "
              "Gaza line  •  Cyclone Akvan nears India  •  Fed: more hikes "
              "likely  •  Oil $83.26  •  Van Gogh $190.4m record  •  "
              "Voyager 1 passes light-day")
    y = 962
    for line in wrap_text(d, ticker, foot_font, INNER - 16):
        d.text((MARGIN + 8, y), line, font=foot_font, fill=WHITE)
        y += 23

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    if os.path.getsize(out) > 1048576:
        page.save(out, format="JPEG", quality=88, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
