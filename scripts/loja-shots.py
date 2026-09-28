#!/usr/bin/env python3
"""Compõe as capturas de tela das lojas (v56, visual Brexplora Night): fundo noturno, legenda em Plus Jakarta + Baskerville
itálico, moldura de aparelho. Entrada: PNGs 1290×2796 (viewport 430×932 @3x). Saída: docs/lojas/shots/{ios-6.7,ios-6.5,android}/NN.png
Uso: python3 scripts/loja-shots.py [pasta_das_capturas]   (pip install pillow brotli fonttools — as fontes woff2 de www/lib são convertidas na hora)"""
import os, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, 'local', 'shots-loja')
OUT = os.path.join(RAIZ, 'docs', 'lojas', 'shots')
FONTES = [os.path.join(RAIZ, 'fonts', 'ttf'), os.path.join(RAIZ, 'fonts'), os.path.join(RAIZ, 'www', 'lib')]
ALTO, BAIXO, INK, SOFT, ACC, OURO = (20, 27, 51), (7, 10, 18), (244, 244, 245), (154, 163, 199), (74, 222, 128), (245, 165, 36)
TELAS = [
  ('1-home',      'Um impostor', 'por dia.', 'TRIVIA BY BREXPLORA · GEOGRAFIA DO BRASIL'),
  ('2-impostor',  'Dez lugares,', 'três não pertencem.', 'ACHE OS IMPOSTORES EM UM MINUTO'),
  ('3-resultado', 'Depois, a lição —', 'e o mapa de verdade.', 'IBGE · ANA · DNIT · VER NO MAPA'),
  ('4-conexoes',  'Nove modos', 'de enigma.', 'CONEXÕES · TOP 10 · VIZINHOS · BINGO · RELÂMPAGO'),
  ('5-meu',       'Cada acerto', 'acende um lugar.', 'MEU BRASIL · ESTADO POR ESTADO'),
  ('6-perfil',    'Sequência, patentes,', 'sem cadastro.', 'CONTA OPCIONAL · SEM SENHA · SEM ANÚNCIOS'),
  ('7-atlas',     'Um atlas de verdade', 'por trás do jogo.', '36 CAMADAS · 16 CAPÍTULOS · ATLAS LIVRE'),
]
def fonte(nome, tam):
    for d in FONTES:
        for ext in ('ttf', 'otf'):
            f = os.path.join(d, f'{nome}.{ext}')
            if os.path.exists(f):
                try: return ImageFont.truetype(f, tam)
                except Exception: pass
        w = os.path.join(d, f'{nome}.woff2')
        if os.path.exists(w):
            try:
                from fontTools.ttLib import TTFont
                t = TTFont(w); t.flavor = None; out = os.path.join(tempfile.gettempdir(), f'{nome}.ttf'); t.save(out); return ImageFont.truetype(out, tam)
            except Exception: pass
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf' if 'baskerville' in nome else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', tam)
def fundo(W, H):
    img = Image.new('RGB', (W, H), BAIXO); px = img.load(); cx, cy = W / 2, 0
    for y in range(H):
        for x in range(W):
            k = min(1.0, ((x - cx) ** 2 / (W * 0.9) ** 2 + (y - cy) ** 2 / (H * 0.55) ** 2) ** .5)
            px[x, y] = tuple(int(ALTO[i] * (1 - k) + BAIXO[i] * k) for i in range(3))
    return img
def compor(src, W, H, l1, l2, eb, base):
    img = base.copy(); d = ImageDraw.Draw(img, 'RGBA')
    fh, fi, fm = fonte('plus-jakarta-sans-latin-800-normal', int(W * .072)), fonte('libre-baskerville-latin-400-italic', int(W * .066)), fonte('jetbrains-mono-latin-500-normal', int(W * .019))
    y = int(H * .05)
    d.text((W / 2, y), eb, font=fm, fill=ACC, anchor='mt'); y += int(W * .055)
    d.text((W / 2, y), l1, font=fh, fill=INK, anchor='mt'); y += int(W * .082)
    d.text((W / 2, y), l2, font=fi, fill=SOFT, anchor='mt'); y += int(W * .1)
    tela = Image.open(src).convert('RGB'); tw = int(W * .80); th = int(tw * tela.height / tela.width); tela = tela.resize((tw, th), Image.LANCZOS)
    bx, by, r = int((W - tw) / 2), y + int(W * .02), int(W * .1); borda = int(W * .014)
    for k in range(6, 0, -1): d.rounded_rectangle([bx - borda - k * 6, by - borda + 30 - k * 3, bx + tw + borda + k * 6, by + th + borda + 30 + k * 6], radius=r + borda + k * 4, fill=(0, 0, 0, 22))
    d.rounded_rectangle([bx - borda, by - borda, bx + tw + borda, by + th + borda], radius=r + borda, fill=(11, 15, 30))
    d.rounded_rectangle([bx - borda, by - borda, bx + tw + borda, by + th + borda], radius=r + borda, outline=(255, 255, 255, 40), width=3)
    mask = Image.new('L', (tw, th), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=r, fill=255)
    img.paste(tela, (bx, by), mask)
    d.text((W / 2, H - int(H * .022)), 'TRIVIA BY BREXPLORA · ATLASBREXPLORA.APP', font=fm, fill=SOFT, anchor='mb')
    return img
if __name__ == '__main__':
    tamanhos = { 'ios-6.7': (1290, 2796), 'ios-6.5': (1242, 2688), 'android': (1080, 2340) }
    for pasta, (W, H) in tamanhos.items():
        os.makedirs(f'{OUT}/{pasta}', exist_ok=True); base = fundo(W, H)
        for i, (arq, l1, l2, eb) in enumerate(TELAS, 1):
            src = f'{SRC}/{arq}.png'
            if not os.path.exists(src): print('falta', src); continue
            compor(src, W, H, l1, l2, eb, base).save(f'{OUT}/{pasta}/{i:02d}-{arq}.png', optimize=True)
        print(pasta, 'ok')
    # feature graphic do Google Play (1024×500)
    W, H = 1024, 500; img = fundo(W, H); d = ImageDraw.Draw(img)
    fh, fi, fm = fonte('plus-jakarta-sans-latin-800-normal', 66), fonte('libre-baskerville-latin-400-italic', 60), fonte('jetbrains-mono-latin-500-normal', 17)
    marca = os.path.join(RAIZ, 'www', 'brexplora-marca.webp')
    if os.path.exists(marca): m = Image.open(marca).convert('RGBA'); m = m.resize((300, int(300 * m.height / m.width)), Image.LANCZOS); img.paste(m, (W - 360, (H - m.height) // 2), m)
    d.text((70, 150), 'TRIVIA BY BREXPLORA', font=fm, fill=ACC); d.text((70, 190), 'Um impostor', font=fh, fill=INK); d.text((70, 270), 'por dia.', font=fi, fill=SOFT); d.text((70, 360), 'GEOGRAFIA DO BRASIL · SEM CADASTRO · DADOS OFICIAIS', font=fm, fill=SOFT)
    img.save(f'{OUT}/../feature-graphic.png', optimize=True); print('feature graphic ok')
