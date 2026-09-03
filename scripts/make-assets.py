#!/usr/bin/env python3
"""Gera assets/ (ícone e splash, claro e escuro) — rosa-dos-ventos do Atlas do Brasil.
Uso: python3 scripts/make-assets.py   (precisa de Pillow: pip install pillow)
Depois: npm run assets  (o @capacitor/assets deriva todos os tamanhos iOS/Android daqui)."""
import math, os
from PIL import Image, ImageDraw

AREIA, TINTA, ARGILA, PEDRA = (235, 223, 194), (55, 48, 31), (176, 61, 42), (140, 130, 100)
NOITE, GIZ = (16, 24, 32), (234, 241, 247)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
S = 4  # supersampling


def rosa(draw, cx, cy, r, tinta, argila, pedra):
    """r = raio dos braços principais. Dois anéis, 4 braços diagonais curtos, 4 principais, norte em argila."""
    draw.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72], outline=tinta, width=int(r * .02))
    draw.ellipse([cx - r * .58, cy - r * .58, cx + r * .58, cy + r * .58], outline=tinta, width=int(r * .006))
    def braco(ang, comp, larg, cor):
        a = math.radians(ang)
        tip = (cx + comp * math.sin(a), cy - comp * math.cos(a))
        l = (cx + larg * math.sin(a + math.pi / 2), cy - larg * math.cos(a + math.pi / 2))
        rr = (cx + larg * math.sin(a - math.pi / 2), cy - larg * math.cos(a - math.pi / 2))
        draw.polygon([tip, l, rr], fill=cor)
    for ang in (45, 135, 225, 315): braco(ang, r * .62, r * .06, pedra)
    for ang in (90, 180, 270): braco(ang, r, r * .075, tinta)
    braco(0, r, r * .075, argila)


def render(size, fundo, tinta, argila, pedra, raio_rel, transparente=False):
    big = size * S
    im = Image.new("RGBA" if transparente else "RGB", (big, big), (0, 0, 0, 0) if transparente else fundo)
    rosa(ImageDraw.Draw(im), big / 2, big / 2, big * raio_rel, tinta, argila, pedra)
    return im.resize((size, size), Image.LANCZOS)


os.makedirs(OUT, exist_ok=True)
render(1024, AREIA, TINTA, ARGILA, PEDRA, .48).save(f"{OUT}/icon.png")
render(1024, NOITE, GIZ, ARGILA, PEDRA, .48).save(f"{OUT}/icon-dark.png")
render(1024, AREIA, TINTA, ARGILA, PEDRA, .40, transparente=True).save(f"{OUT}/icon-foreground.png")
Image.new("RGB", (1024, 1024), AREIA).save(f"{OUT}/icon-background.png")
render(2732, AREIA, TINTA, ARGILA, PEDRA, .17).save(f"{OUT}/splash.png")
render(2732, NOITE, GIZ, ARGILA, PEDRA, .17).save(f"{OUT}/splash-dark.png")
print("assets gerados em", os.path.abspath(OUT))
