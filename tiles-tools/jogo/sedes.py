#!/usr/bin/env python3
"""Sede aproximada de cada município (v38): a maior mancha densamente edificada dentro do polígono do município.
O busca-index guarda o centroide do município (Santarém fica a 28 km da cidade), o que estraga "cidades à margem" e o alvo do "Onde é?".
Saída: jogo/sedes.json { "Nome|UF": [x, y] }"""
import json, subprocess, collections, math
from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely.strtree import STRtree
T = '/home/claude/atlas/tiles'; J = '/home/claude/atlas/jogo'
def feats(pm, z):
    o = subprocess.run(['tippecanoe-decode', '-z', str(z), '-Z', str(z), pm], capture_output=True, text=True).stdout
    j = json.loads(o); res = []
    def walk(x):
        if isinstance(x, dict):
            if x.get('type') == 'Feature' and 'properties' in x: res.append(x)
            else:
                for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(j); return res
au = json.load(open('/mnt/user-data/uploads/ATLAS/ATLAS DEM/area densamente edificada.geojson'))['features']
pts = []; areas = []
for f in au:
    try: g = make_valid(shape(f['geometry']))
    except Exception: continue
    c = g.centroid; pts.append(c); areas.append(g.area * math.cos(math.radians(c.y)))
print('manchas', len(pts))
tree = STRtree(pts)
grupos = collections.defaultdict(list)
for f in feats(f'{T}/municipios.pmtiles', 7):
    p = f['properties']; k = (p.get('NM_MUN'), p.get('SIGLA_UF'))
    if not k[0]: continue
    try: grupos[k].append(make_valid(shape(f['geometry'])))
    except Exception: pass
print('municípios', len(grupos))
sedes = {}; sem = 0
for k, gs in grupos.items():
    u = make_valid(unary_union(gs)).buffer(0)
    cand = [i for i in tree.query(u) if u.contains(pts[i])]
    if not cand: sem += 1; continue
    i = max(cand, key=lambda i: areas[i]); sedes[f'{k[0]}|{k[1]}'] = [round(pts[i].x, 4), round(pts[i].y, 4)]
print('sedes', len(sedes), 'sem mancha', sem)
json.dump(sedes, open(f'{J}/sedes.json', 'w'), ensure_ascii=False)
