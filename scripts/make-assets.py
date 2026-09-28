#!/usr/bin/env python3
"""Gera assets/ (ícone e splash, claro e escuro) — a marca Brexplora sobre o fundo "Brexplora Night" (v49).
Uso: python3 scripts/make-assets.py   (precisa de Pillow: pip install pillow; usa www/brexplora-marca.webp, ou baixa do R2)
Depois: npm run assets  (o @capacitor/assets deriva todos os tamanhos iOS/Android daqui)."""
import os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(RAIZ, "assets")
MARCA = os.path.join(RAIZ, "www", "brexplora-marca.webp")
if not os.path.exists(MARCA):
    os.makedirs(os.path.dirname(MARCA), exist_ok=True)
    urllib.request.urlretrieve("https://atlasbrexplora.app/brexplora-marca.webp", MARCA)
NOITE_ALTO, NOITE_BAIXO = (20, 27, 51), (7, 10, 18)


def fundo(size, radial=True):
    """radial: #141B33 no alto-centro → #070A12 embaixo (mesmo gradiente do app)."""
    im = Image.new("RGB", (size, size), NOITE_BAIXO)
    if not radial: return im
    px = im.load(); cx, cy = size / 2, size * 0.1
    for y in range(size):
        for x in range(0, size, 1):
            d = ((x - cx) ** 2 / (size * 0.75) ** 2 + (y - cy) ** 2 / (size * 0.9) ** 2) ** .5
            k = max(0.0, min(1.0, d))
            px[x, y] = tuple(int(NOITE_ALTO[i] * (1 - k) + NOITE_BAIXO[i] * k) for i in range(3))
    return im


def marca(size, rel):
    m = Image.open(MARCA).convert("RGBA")
    w = int(size * rel); h = int(w * m.height / m.width)
    return m.resize((w, h), Image.LANCZOS)


def compor(size, rel, sombra=True, transparente=False):
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0)) if transparente else fundo(size).convert("RGBA")
    m = marca(size, rel); x, y = (size - m.width) // 2, (size - m.height) // 2
    if sombra and not transparente:
        sh = Image.new("RGBA", (size, size), (0, 0, 0, 0)); sh.paste((46, 154, 85, 140), (x, y + int(size * .04)), m)
        sh = sh.filter(ImageFilter.GaussianBlur(size * .06)); base = Image.alpha_composite(base, sh)
    base.paste(m, (x, y), m)
    return base.convert("RGB") if not transparente else base


os.makedirs(OUT, exist_ok=True)
compor(1024, .66).save(f"{OUT}/icon.png")
compor(1024, .66).save(f"{OUT}/icon-dark.png")
compor(1024, .56, transparente=True).save(f"{OUT}/icon-foreground.png")       # Android adaptive: só a marca
fundo(1024).save(f"{OUT}/icon-background.png")
compor(2732, .22).save(f"{OUT}/splash.png")
compor(2732, .22).save(f"{OUT}/splash-dark.png")
print("assets gerados em", os.path.abspath(OUT))
