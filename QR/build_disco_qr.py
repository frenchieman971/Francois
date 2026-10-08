import math
import os
import random

import segno
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "/Users/frenchie/Library/Mobile Documents/com~apple~CloudDocs/Francois DJ/QR"
URL = "https://frenchieman971.github.io/Francois/"

BG_TOP, BG_BOT = (42, 8, 69), (10, 4, 20)
MAGENTA, CYAN, GOLD = (255, 46, 154), (46, 230, 255), (255, 200, 61)
INK = (27, 10, 46)
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

rnd = random.Random(7)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(text, path, max_w, size):
    while size > 20:
        f = font(path, size)
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return font(path, size)


def gradient(w, h):
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        c = tuple(round(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c + (255,))
    return img


def rays(img, apex):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ax, ay = apex
    cols = [MAGENTA, CYAN, GOLD]
    for i, a in enumerate(range(-72, 73, 12)):
        pts = [(ax, ay)]
        for da in (a - 3.5, a + 3.5):
            r = math.radians(da)
            pts.append((ax + 4000 * math.sin(r), ay + 4000 * math.cos(r)))
        d.polygon(pts, fill=cols[i % 3] + (52,))
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(img, layer)


def sparkles(img, n):
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rnd.randrange(img.width), rnd.randrange(img.height)
        s = rnd.randrange(8, 26)
        col = rnd.choice([GOLD, CYAN, (255, 255, 255), MAGENTA])
        d.line([(x - s, y), (x + s, y)], fill=col + (230,), width=3)
        d.line([(x, y - s), (x, y + s)], fill=col + (230,), width=3)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=col + (255,))


def disco_ball(img, cx, cy, r):
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([cx - r - 60, cy - r - 60, cx + r + 60, cy + r + 60], fill=GOLD + (90,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(60)))

    d = ImageDraw.Draw(img)
    d.line([(cx, 0), (cx, cy - r)], fill=GOLD + (160,), width=5)

    ball = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    bd = ImageDraw.Draw(ball)
    bd.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=(150, 150, 170, 255))
    step = r // 5
    for gy in range(0, 2 * r, step):
        for gx in range(0, 2 * r, step):
            shade = 245 - 22 * rnd.randrange(5)
            bd.rectangle([gx + 4, gy + 4, gx + step - 5, gy + step - 5], fill=(shade, shade, shade + 12, 255))
    hl = Image.new("RGBA", ball.size, (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse([r * 0.30, r * 0.18, r * 0.78, r * 0.52], fill=(255, 255, 255, 150))
    ball = Image.alpha_composite(ball, hl.filter(ImageFilter.GaussianBlur(14)))
    mask = Image.new("L", ball.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    ball.putalpha(mask)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(ball, (cx - r, cy - r), ball)
    return Image.alpha_composite(img, layer)


def qr_block(img, cx, cy, mod):
    qr = segno.make(URL, error="m")
    n = qr.symbol_size(border=0)[0]
    quiet = 4 * mod
    side = n * mod + 2 * quiet
    x0, y0 = cx - side // 2, cy - side // 2
    fr = 28
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0 - fr, y0 - fr, x0 + side + fr, y0 + side + fr], radius=56, fill=GOLD + (255,))
    d.rounded_rectangle([x0 - fr + 12, y0 - fr + 12, x0 + side + fr - 12, y0 + side + fr - 12],
                        radius=44, outline=MAGENTA + (255,), width=6)
    d.rounded_rectangle([x0, y0, x0 + side, y0 + side], radius=40, fill=(255, 255, 255, 255))
    for ry, row in enumerate(qr.matrix_iter(border=0)):
        for rx, bit in enumerate(row):
            if bit:
                px = x0 + quiet + rx * mod
                py = y0 + quiet + ry * mod
                d.rectangle([px, py, px + mod - 1, py + mod - 1], fill=INK + (255,))
    return side + 2 * fr


def stripes(img, y):
    d = ImageDraw.Draw(img)
    for i, col in enumerate([MAGENTA, GOLD, CYAN, MAGENTA]):
        d.rectangle([0, y + i * 25, img.width, y + i * 25 + 24], fill=col + (255,))


def centered(d, cx, cy, text, fnt, fill, shadow=None, off=0, stroke=None, sw=0):
    if shadow:
        d.text((cx + off, cy + off), text, font=fnt, fill=shadow + (255,), anchor="mm")
    d.text((cx, cy), text, font=fnt, fill=fill + (255,), anchor="mm", stroke_width=sw,
           stroke_fill=(stroke + (255,)) if stroke else None)


def build_a5():
    W, H = 1748, 2480
    img = gradient(W, H)
    img = rays(img, (874, 330))
    sparkles(img, 90)
    img = disco_ball(img, 874, 330, 150)
    d = ImageDraw.Draw(img)

    centered(d, 874, 640, "DJ FRANCOIS", fit_font("DJ FRANCOIS", IMPACT, 1500, 200), GOLD, shadow=MAGENTA, off=10)
    centered(d, 874, 830, "DE ST FRANCOIS", fit_font("DE ST FRANCOIS", IMPACT, 1500, 170), MAGENTA,
             shadow=CYAN, off=12, stroke=GOLD, sw=12)
    centered(d, 874, 1095, "KARAOKÉ • DISCO", fit_font("KARAOKÉ • DISCO", ARIAL_B, 1500, 96), CYAN)

    qr_block(img, 874, 1600, 22)
    d = ImageDraw.Draw(img)

    centered(d, 874, 2200, "SCANNEZ POUR LES CATALOGUES",
             fit_font("SCANNEZ POUR LES CATALOGUES", ARIAL_B, 1500, 84), GOLD)
    stripes(img, 2380)
    return img.convert("RGB")


def build_square():
    W, H = 1200, 1400
    img = gradient(W, H)
    img = rays(img, (600, 170))
    sparkles(img, 50)
    d = ImageDraw.Draw(img)
    centered(d, 600, 115, "DJ FRANCOIS", fit_font("DJ FRANCOIS", IMPACT, 1100, 150), GOLD, shadow=MAGENTA, off=7)
    centered(d, 600, 245, "DE ST FRANCOIS", fit_font("DE ST FRANCOIS", IMPACT, 1100, 130), MAGENTA,
             shadow=CYAN, off=6, stroke=GOLD, sw=6)
    qr_block(img, 600, 760, 22)
    d = ImageDraw.Draw(img)
    centered(d, 600, 1290, "SCANNEZ POUR LES CATALOGUES",
             fit_font("SCANNEZ POUR LES CATALOGUES", ARIAL_B, 1100, 60), GOLD)
    stripes(img, 1340)
    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    a5 = build_a5()
    a5.save(os.path.join(OUT, "carte-qr-francois-dj-disco-A5.png"))
    a5.save(os.path.join(OUT, "carte-qr-francois-dj-disco-A5.pdf"), "PDF", resolution=300.0)
    build_square().save(os.path.join(OUT, "qr-francois-dj-disco.png"))
    print("ok")
