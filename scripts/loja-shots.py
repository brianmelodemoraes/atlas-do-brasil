#!/usr/bin/env python3
"""Compõe as capturas de tela das lojas: moldura de aparelho + legenda editorial sobre papel.
Entrada: PNGs 1290×2796 (viewport 430×932 @3x) em local/shots-loja/. Saída: docs/lojas/shots/{ios-6.7,ios-6.5,android}/NN.png
Uso: python3 scripts/loja-shots.py [pasta_das_capturas]   (pip install pillow)"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/atlas/local/shots-loja'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'lojas', 'shots')
LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'www', 'lib')
PAPER, HI, INK, SOFT, RED, GRID = (235, 223, 194), (243, 234, 211), (55, 48, 31), (107, 95, 69), (169, 62, 42), (169, 62, 42, 40)
TELAS = [
  ('1-indice',    'Um atlas que se move', 'enquanto você lê', 'DEZESSEIS CAPÍTULOS · CARTOGRAFIA NARRATIVA'),
  ('2-capitulo',  'O mapa acompanha', 'cada parágrafo', 'ROLE O TEXTO · O MAPA VOA'),
  ('3-atlas',     'Quarenta e três', 'camadas oficiais', 'IBGE · ANA · DNIT · ANEEL · ICMBio · FUNAI'),
  ('4-aguas',     'Expedições prontas', 'num toque', 'BRASIL DAS ÁGUAS · PAÍS ELÉTRICO · TERRA PROTEGIDA'),
  ('4b-ficha',    'Toque em qualquer lugar:', 'ficha na hora', '34 MIL LUGARES PESQUISÁVEIS'),
  ('5-desafio',   'Um enigma geográfico', 'por dia', 'SILHUETAS · LUGARES · RIOS'),
  ('6-resultado', 'Compare, compartilhe,', 'volte amanhã', 'RANKING DO DIA · SEQUÊNCIA · STORY'),
]
def fonte(nome, tam):
    for f in [f'{LIB}/{nome}.woff2', f'{LIB}/{nome}.ttf', f'/home/claude/atlas/lib/{nome}.ttf']:
        if os.path.exists(f):
            try: return ImageFont.truetype(f, tam)
            except Exception: pass
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf' if 'serif' in nome else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', tam)
def compor(src, W, H, l1, l2, eb):
    img = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(img, 'RGBA')
    for x in range(60, W, 120): d.line([(x, 0), (x, H)], fill=GRID, width=2)
    for y in range(40, H, 120): d.line([(0, y), (W, y)], fill=GRID, width=2)
    fs, fe, fm = fonte('instrument-serif-latin-400-normal', int(W * .068)), fonte('instrument-serif-latin-400-italic', int(W * .068)), fonte('ibm-plex-mono-latin-400-normal', int(W * .019))
    y = int(H * .055)
    d.text((W / 2, y), eb, font=fm, fill=RED, anchor='mt'); y += int(W * .05)
    d.text((W / 2, y), l1, font=fs, fill=INK, anchor='mt'); y += int(W * .075)
    d.text((W / 2, y), l2, font=fe, fill=INK, anchor='mt'); y += int(W * .09)
    # aparelho: moldura escura com cantos redondos; a captura ocupa 80 % da largura
    tela = Image.open(src).convert('RGB'); tw = int(W * .80); th = int(tw * tela.height / tela.width); tela = tela.resize((tw, th), Image.LANCZOS)
    bx, by, r = int((W - tw) / 2), y + int(W * .02), int(W * .09)
    borda = int(W * .012)
    d.rounded_rectangle([bx - borda + 10, by - borda + 14, bx + tw + borda + 10, by + th + borda + 14], radius=r + borda, fill=(55, 48, 31, 60))
    d.rounded_rectangle([bx - borda, by - borda, bx + tw + borda, by + th + borda], radius=r + borda, fill=(28, 24, 16))
    mask = Image.new('L', (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=r, fill=255)
    img.paste(tela, (bx, by), mask)
    d.text((W / 2, H - int(H * .03)), 'ATLAS DO BRASIL · BY BREXPLORA', font=fm, fill=SOFT, anchor='mb')
    return img
if __name__ == '__main__':
    tamanhos = { 'ios-6.7': (1290, 2796), 'ios-6.5': (1242, 2688), 'android': (1080, 2340) }
    for pasta, (W, H) in tamanhos.items():
        os.makedirs(f'{OUT}/{pasta}', exist_ok=True)
        for i, (arq, l1, l2, eb) in enumerate(TELAS, 1):
            src = f'{SRC}/{arq}.png'
            if not os.path.exists(src): print('falta', src); continue
            compor(src, W, H, l1, l2, eb).save(f'{OUT}/{pasta}/{i:02d}-{arq}.png', optimize=True)
        print(pasta, 'ok')
