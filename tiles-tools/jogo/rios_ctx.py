#!/usr/bin/env python3
"""Contexto por rio candidato (v38): estados que atravessa, cidades à margem (sede a ≤7–15 km do eixo) e cidade mais perto da foz.
Lê rh/rios_nomeados_v3.multi.geojsonl uma vez (437 MB), só as feições (nome, código) dos candidatos. Saída: jogo/rios_ctx.json"""
import json, re, math, collections
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import shape, Point
from shapely.prepared import prep
from shapely.validation import make_valid
# estados: polígonos simplificados (0.01°) para contar por onde o rio passa
EST = []
for f in json.load(open('/mnt/user-data/uploads/ATLAS/ATLAS DEM/estados.geojson'))['features']:
    g = make_valid(shape(f['geometry'])).simplify(0.01); EST.append((f['properties']['SIGLA_UF'], g.bounds, prep(g)))
idx = json.load(open('/home/claude/atlas/final/busca-index.json'))
cid = [e for e in idx if e['t'] == 'cidade']
SEDES = json.load(open('/home/claude/atlas/jogo/sedes.json'))   # sede ≈ maior mancha urbana (o índice guarda o centroide)
for e in cid:
    sd = SEDES.get(f"{e['n']}|{e['uf']}")
    if sd: e['x'], e['y'] = sd
K = 111.32
P = np.array([[e['x'] * math.cos(math.radians(e['y'])), e['y']] for e in cid]); tree = cKDTree(P)
cand = json.load(open('/home/claude/atlas/final/jogo-candidatos.json'))['rios']
alvo = {(r['nome'], r['cod']) for r in cand}
nomes = {r['nome'] for r in cand}
rx = re.compile(r'"NORIOCOMP": "([^"]*)", "cocursodag": "([^"]*)"')
pts = collections.defaultdict(list); n = 0
with open('/home/claude/atlas/rh/rios_nomeados_v3.multi.geojsonl') as f:
    for line in f:
        m = rx.search(line[:400])
        if not m or m.group(1) not in nomes or (m.group(1), m.group(2)) not in alvo: continue
        g = json.loads(line)['geometry']; ls = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
        for l in ls: pts[(m.group(1), m.group(2))].extend(l[::3])
        n += 1
print('feições', n, 'rios com geometria', len(pts))
km_de = {(r['nome'], r['cod']): r['km'] for r in cand}
def limpa(n): return n.replace('Rio ', '').replace('Ribeirão ', '').split(' ou ')[0].strip().lower()
def entrega(nome_cidade, core):
    c = nome_cidade.lower(); return core in c or (len(c) >= 4 and c in core)   # "Itajaí" entrega "Itajaí-açu"; "Cuiabá" entrega "Rio Cuiabá"
out = {}
for (nome, cod), l in pts.items():
    A = np.array([[x * math.cos(math.radians(y)), y] for x, y in l])
    km = km_de.get((nome, cod), 0); raio = 15 if km >= 1000 else 10 if km >= 500 else 7   # rios largos: a sede fica longe do eixo
    core = limpa(nome)
    perto = tree.query_ball_point(A, r=raio / K); ids = set(i for s in perto for i in s)
    cidades = sorted(({'n': cid[i]['n'], 'uf': cid[i]['uf'], 'p': cid[i].get('p', 3)} for i in ids if not entrega(cid[i]['n'], core)), key=lambda c: (c['p'], c['n']))
    # estados: por onde passam os pontos do eixo (≥ 5 % deles) — não pelas cidades vizinhas
    amostra = l[::max(1, len(l) // 400)]; ufs = collections.Counter()
    for x, y in amostra:
        for uf, (x0, y0, x1, y1), pg in EST:
            if x0 <= x <= x1 and y0 <= y <= y1 and pg.contains(Point(x, y)): ufs[uf] += 1; break
    tot = sum(ufs.values()) or 1
    out[cod + '|' + nome] = {'ufs': [u for u, c in ufs.most_common() if c >= max(1, .05 * tot)], 'cidades': cidades[:6]}
json.dump(out, open('/home/claude/atlas/jogo/rios_ctx.json', 'w'), ensure_ascii=False)
print('ok', len(out))
