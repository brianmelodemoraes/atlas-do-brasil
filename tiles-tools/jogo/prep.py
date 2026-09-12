#!/usr/bin/env python3
"""Desafio diário — preparação de dados.
Saídas: final/jogo-silhuetas.json (contornos simplificados dos municípios candidatos, por CD_MUN)
        jogo/desafios.json (calendário: dia → tipo + alvo + dicas), jogo/candidatos.json (listas para autocomplete/feedback)."""
import json, subprocess, collections, math, random, datetime, os
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
T = '/home/claude/atlas/tiles'; F = '/home/claude/atlas/final'; J = '/home/claude/atlas/jogo'
os.makedirs(J, exist_ok=True)
K = 111.32
def dist_km(a, b): return math.hypot((a[0]-b[0]) * K * math.cos(math.radians((a[1]+b[1])/2)), (a[1]-b[1]) * K)

idx = json.load(open(f'{F}/busca-index.json'))
cidades = [e for e in idx if e['t'] == 'cidade']
# o calendário publicado (a partir de 08/09/2026) foi sorteado com Recife como p=1 (erro do índice, corrigido depois);
# manter a mesma classificação AQUI para não mudar os alvos já jogados — a correção vale só para o mapa/busca
for e in cidades:
    if (e['n'], e['uf']) == ('Recife', 'PE'): e['p'] = 1
por_nome_uf = {(e['n'], e['uf']): e for e in cidades}
_SD = json.load(open(f'{J}/sedes.json')) if os.path.exists(f'{J}/sedes.json') else {}
sede_xy = lambda e: _SD.get(f"{e['n']}|{e['uf']}", [e['x'], e['y']])

# ── 1) silhuetas dos municípios candidatos (p ≤ 2) ─────────────────────────────────────────────
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
cand = {(e['n'], e['uf']) for e in cidades if e.get('p', 3) <= 2}
grupos = collections.defaultdict(list); props = {}
for f in feats(f'{T}/municipios.pmtiles', 7):
    p = f['properties']; k = (p.get('NM_MUN'), p.get('SIGLA_UF'))
    if k not in cand: continue
    try: grupos[k].append(make_valid(shape(f['geometry'])))
    except Exception: pass
    props[k] = p
sil = {}; meta = {}
for k, gs in grupos.items():
    u = make_valid(unary_union(gs)).buffer(0)
    if u.geom_type not in ('Polygon', 'MultiPolygon'): continue
    # só o(s) maior(es) polígono(s): ilhas minúsculas e lascas de tile fora
    polys = sorted((list(u.geoms) if u.geom_type == 'MultiPolygon' else [u]), key=lambda p: -p.area)
    c0 = polys[0].centroid
    keep = [p for p in polys if p.area >= polys[0].area * 0.02 and p.distance(polys[0]) < 0.5][:6]   # Trindade (Vitória) fora
    s = unary_union(keep).simplify(0.004, preserve_topology=True)
    rings = []
    for p in (list(s.geoms) if s.geom_type == 'MultiPolygon' else [s]):
        rings.append([[round(x, 4), round(y, 4)] for x, y in p.exterior.coords])
    pr = props[k]; e = por_nome_uf[k]
    cd = pr.get('CD_MUN'); sil[cd] = rings
    meta[cd] = { 'cd': cd, 'nome': k[0], 'uf': k[1], 'x': e['x'], 'y': e['y'], 'p': e.get('p', 3), 'area': round(float(pr.get('AREA_KM2') or 0)),
                 'rgi': pr.get('NM_RGI'), 'rgint': pr.get('NM_RGINT'), 'regiao': pr.get('NM_REGIAO'), 'bbox': [round(v, 3) for v in s.bounds] }
json.dump(sil, open(f'{F}/jogo-silhuetas.json', 'w'), separators=(',', ':'))
print('silhuetas', len(sil), 'bytes', os.path.getsize(f'{F}/jogo-silhuetas.json'))

# bioma predominante por município (dica): decodifica biomas z4 e testa o centroide
biomas = [(shape(f['geometry']), f['properties'].get('Bioma')) for f in feats(f'{T}/biomas.pmtiles', 4)]
from shapely.geometry import Point
def bioma_de(x, y):
    pt = Point(x, y)
    for g, n in biomas:
        try:
            if g.contains(pt): return n
        except Exception: pass
    return None
for cd, m in meta.items(): m['bioma'] = bioma_de(m['x'], m['y'])
print('biomas', collections.Counter(m['bioma'] for m in meta.values()))

# ── 2) rios candidatos (≥150 km, com foz e cadeia) ─────────────────────────────────────────────
cn = json.load(open(f'{F}/cursos-nomes.json')); nomes = cn['nomes']; foz = cn['foz']
RH = [["7792", "Atlântico Sudeste"], ["7793", "Atlântico Sudeste"], ["7794", "Atlântico Sudeste"], ["7795", "Atlântico Sul"], ["7796", "Atlântico Sul"], ["7797", "Atlântico Sul"], ["7798", "Atlântico Sul"], ["7799", "Atlântico Sul"], ["771", "Atlântico Leste"], ["772", "Atlântico Leste"], ["773", "Atlântico Leste"], ["774", "Atlântico Leste"], ["775", "Atlântico Leste"], ["776", "Atlântico Sudeste"], ["777", "Atlântico Sudeste"], ["778", "Atlântico Sudeste"], ["71", "Atlântico Nordeste Ocidental"], ["72", "Atlântico Nordeste Ocidental"], ["73", "Atlântico Nordeste Ocidental"], ["74", "Parnaíba"], ["75", "Atlântico Nordeste Oriental"], ["76", "São Francisco"], ["78", "Atlântico Sul"], ["79", "Atlântico Sul"], ["82", "Uruguai"], ["86", "Paraná"], ["89", "Paraguai"], ["2", "Atlântico Sul"], ["3", "Amazônica"], ["4", "Amazônica"], ["5", "Amazônica"], ["6", "Tocantins-Araguaia"], ["8", "Paraguai"]]
from shapely.geometry import Point as _Pt
_RHP = { (f['properties'].get('nome') or f['properties'].get('NOME')): make_valid(shape(f['geometry'])) for f in json.load(open('/home/claude/atlas/rh/regioes_hidrograficas.geojson'))['features'] }
def rh_de(c, foz=None, bbox=None, nome=''):
    # região hidrográfica REAL (polígono da ANA), não o prefixo Otto: 77x inclui Doce/Paraíba do Sul, que são Atlântico Sudeste
    for n in _RHP:
        if n.lower() in nome.lower(): return n                       # "Rio Parnaíba", "Rio Paraguai": a foz cai na divisa
    for pt in ([foz] if foz else []) + ([[(bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2]] if bbox else []):
        for n, pl in _RHP.items():
            if pl.contains(_Pt(*pt)): return n
    for p, n in RH:
        if c.startswith(p): return n
    return None
def pai(c):
    if len(c) <= 1: return None
    c = c[:-1]
    while len(c) > 1 and c[-1] in '13579': c = c[:-1]
    return c or None
def nome_no(cod, ponto):
    lst = nomes.get(cod)
    if not lst: return None
    d = lambda e: max(0, e[1]-ponto[0], ponto[0]-e[3]) + max(0, e[2]-ponto[1], ponto[1]-e[4])
    fz = foz.get(cod); df = (lambda e: max(0, e[1]-fz[0], fz[0]-e[3]) + max(0, e[2]-fz[1], fz[1]-e[4])) if fz else (lambda e: 0)
    return sorted(lst, key=lambda e: ((0 if d(e) <= .05 else d(e)), df(e)))[0][0]
DESAGUA_FIX = { 'Rio Paraná': 'Rio da Prata', 'Rio Uruguai': 'Rio da Prata', 'Rio Paraguai': 'Rio Paraná', 'Rio Amazonas': 'oceano Atlântico', 'Rio Tocantins': 'oceano Atlântico (baía de Marajó)', 'Rio Solimões': 'Rio Amazonas', 'Rio Araguaia': 'Rio Tocantins', 'Rio Paranaíba': 'Rio Paraná', 'Rio Guamá': 'baía de Guajará, em Belém', 'Rio Capim': 'Rio Guamá', 'Rio Camaquã': 'Lagoa dos Patos', 'Rio Jacuí': 'Lago Guaíba, em Porto Alegre', 'Rio Araguari': 'oceano Atlântico', 'Rio Cuiabá': 'Rio Paraguai' }
FAMOSOS = ['Rio Amazonas','Rio São Francisco','Rio Paraná','Rio Tocantins','Rio Tietê','Rio Paraíba do Sul','Rio Araguaia','Rio Xingu','Rio Tapajós','Rio Madeira','Rio Negro','Rio Solimões','Rio Purus','Rio Juruá','Rio Uruguai','Rio Paraguai','Rio Iguaçu','Rio Doce','Rio Jequitinhonha','Rio Parnaíba','Rio Grande','Rio Paranaíba','Rio Paranapanema','Rio Jacuí','Rio Taquari','Rio Ribeira de Iguape','Rio Mucuri','Rio Itapecuru','Rio Mearim','Rio Gurupi','Rio Capibaribe','Rio Piranhas ou Açu','Rio Jaguaribe','Rio Acaraú','Rio das Velhas','Rio Cuiabá','Rio São Manuel ou Teles Pires','Rio Juruena','Rio Trombetas','Rio Jari','Rio Branco','Rio Japurá','Rio Içá','Rio Javari','Rio Aripuanã','Rio Ji-paraná ou Machado','Rio de Contas','Rio Paraguaçu','Rio Ivaí','Rio Tibagi','Rio Itajaí-açu','Rio Camaquã','Rio Ibicuí','Rio das Mortes','Rio Piracicaba','Rio Mogi Guaçu','Rio Urucuia','Rio Poti','Rio Paraíba','Rio Pelotas','Rio Uatumã','Rio Araguari','Rio Guamá','Rio Capim','Rio Sapucaí','Rio Corumbá','Rio Pardo','Rio Verde','Rio Preto','Rio Miranda','Rio Aquidauana','Rio Acre','Rio Guaporé','Rio Mamoré','Rio Roosevelt','Rio Sono','Rio Manuel Alves']
FAMOSOS2 = ['Rio Piquiri','Rio Pomba','Rio Muriaé','Rio Carinhanha','Rio Corrente','Rio Canindé','Rio Balsas','Rio Turvo','Rio Claro','Rio Canoas','Rio Chapecó','Rio Cubatão','Rio Iriri','Rio Nhamundá','Rio Anapu','Rio Pacajá','Rio Fresco','Rio Itacaiúnas','Rio Palma','Rio Gurgueia','Rio Longá','Rio Piauí','Rio Salgado','Rio Moxotó','Rio Ipojuca','Rio Una','Rio Mundaú','Rio Coruripe','Rio Real','Rio Sergipe','Rio Japaratuba','Rio Inhambupe','Rio Pojuca','Rio Jacuípe','Rio Paramirim','Rio Jucuruçu','Rio São Mateus','Rio Itapemirim','Rio Itabapoana','Rio Macaé','Rio Guandu','Rio Piabanha','Rio Itanhaém','Rio Verde ou Verdão','Rio Coxim','Rio Sepotuba','Rio Jauru','Rio São Lourenço','Rio Vermelho','Rio Arinos','Rio do Sangue','Rio Guariba','Rio Manicoré','Rio Abunã','Rio Jamari','Rio Candeias','Rio Iaco','Rio Envira','Rio Tarauacá','Rio Moa','Rio Coari','Rio Tefé','Rio Jutaí','Rio Uaupés','Rio Içana','Rio Demini','Rio Padauari','Rio Catrimani','Rio Mucajaí','Rio Uraricoera','Rio Tacutu','Rio Anauá','Rio Jatapu','Rio Mapuera','Rio Cachorro','Rio Erepecuru','Rio Maicuru','Rio Curuá','Rio Pajeú','Rio Vaza-Barris','Rio Itapicuru','Rio Itajaí']
EXCLUI = {'Linha de Costa', 'Rio Marañon', 'Rio Ucayali', 'Rio Beni', 'Rio Mamoré', 'Rio Guaporé', 'Rio Iténez', 'Rio Putumayo', 'Rio Napo', 'Rio Yavarí', 'Rio Caquetá', 'Rio Pilcomayo', 'Rio Apa', 'Rio Quaraí', 'Rio Jaguarão', 'Rio Oiapoque'}
def letra_rio(n):
    n = n.split(' ou ')[0]
    w = [x for x in n.split() if x.lower() not in ('rio','ribeirão','vereda','córrego','da','das','do','dos','de','d\'água')]
    return (w[0] if w else n)[0].upper()
rios = []
for cod, lst in nomes.items():
    for e in lst:
        n, km = e[0], e[5]
        if km < 150 or n in EXCLUI or not n.startswith(('Rio ', 'Ribeirão ')): continue
        # cadeia a jusante
        cadeia = []; cur = pai(cod); junta = foz.get(cod) or [(e[1]+e[3])/2, (e[2]+e[4])/2]
        for _ in range(8):
            if not cur: break
            nm = nome_no(cur, junta)
            if nm and nm != n and (not cadeia or nm != cadeia[-1]): cadeia.append(nm)
            junta = foz.get(cur, junta); cur = pai(cur)
        # outro nome no MESMO curso, mais perto da foz: é o vizinho a jusante (Solimões→Amazonas, Paranaíba→Paraná, Araguaia→Tocantins)
        fz = foz.get(cod); desagua = None
        if fz:
            dfz = lambda b: max(0, b[1]-fz[0], fz[0]-b[3]) + max(0, b[2]-fz[1], fz[1]-b[4])
            minha = dfz(e)
            if minha > .05:
                jus = [o for o in lst if o[0] != n and o[5] >= 30 and dfz(o) < minha - .05]
                if jus: desagua = max(jus, key=dfz)[0]      # o mais próximo de mim (mais longe da foz)
        if not desagua: desagua = cadeia[0] if cadeia else ('oceano Atlântico' if len(cod) <= 2 or cod.startswith('7') else None)
        desagua = DESAGUA_FIX.get(n, desagua)
        if desagua and cadeia and desagua != cadeia[0]: cadeia = [desagua] + cadeia
        rios.append({ 'nome': n, 'cod': cod, 'km': km, 'bbox': [e[1], e[2], e[3], e[4]], 'rh': rh_de(cod, fz, [e[1], e[2], e[3], e[4]], n), 'foz': fz, 'desagua': desagua, 'cadeia': cadeia[:4] })
# um só por nome (o maior)
melhor = {}
for r in rios:
    if r['nome'] not in melhor or r['km'] > melhor[r['nome']]['km']: melhor[r['nome']] = r
rios = sorted(melhor.values(), key=lambda r: -r['km'])
print('rios candidatos', len(rios), [r['nome'] for r in rios[:10]])

# ── 3) "onde é?": cidades p ≤ 1 com ponto urbano (mancha) mais próximo do centroide ────────────
# v38: sede = maior mancha densamente edificada dentro do município (jogo/sedes.py); antes era a mancha mais perto do centroide
SEDES = json.load(open(f'{J}/sedes.json'))
au = [f['geometry']['coordinates'] for f in json.load(open('/home/claude/atlas/rh/au_pts.geojson'))['features']]
onde = []
for e in cidades:
    if e.get('p', 3) > 1: continue
    sd = SEDES.get(f"{e['n']}|{e['uf']}")
    perto = sd or min(au, key=lambda c: dist_km(c, [e['x'], e['y']]))
    pt = perto if dist_km(perto, [e['x'], e['y']]) < 40 else [e['x'], e['y']]
    onde.append({ 'nome': e['n'], 'uf': e['uf'], 'x': round(pt[0], 4), 'y': round(pt[1], 4), 'p': e.get('p', 3), 'bioma': bioma_de(e['x'], e['y']) })
print('onde é', len(onde))

# ── 3b) capitais e direção (dicas de localização) ────────────────────────────────────────────
REGIAO_UF = { 'AC':'Norte','AM':'Norte','AP':'Norte','PA':'Norte','RO':'Norte','RR':'Norte','TO':'Norte', 'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste','PE':'Nordeste','PI':'Nordeste','RN':'Nordeste','SE':'Nordeste',
              'DF':'Centro-oeste','GO':'Centro-oeste','MS':'Centro-oeste','MT':'Centro-oeste', 'ES':'Sudeste','MG':'Sudeste','RJ':'Sudeste','SP':'Sudeste', 'PR':'Sul','RS':'Sul','SC':'Sul' }
CAPITAL_NOME = { 'AC':'Rio Branco','AL':'Maceió','AM':'Manaus','AP':'Macapá','BA':'Salvador','CE':'Fortaleza','DF':'Brasília','ES':'Vitória','GO':'Goiânia','MA':'São Luís','MG':'Belo Horizonte','MS':'Campo Grande','MT':'Cuiabá','PA':'Belém','PB':'João Pessoa','PE':'Recife','PI':'Teresina','PR':'Curitiba','RJ':'Rio de Janeiro','RN':'Natal','RO':'Porto Velho','RR':'Boa Vista','RS':'Porto Alegre','SC':'Florianópolis','SE':'Aracaju','SP':'São Paulo','TO':'Palmas' }
CAPITAIS = { uf: por_nome_uf[(n, uf)] for uf, n in CAPITAL_NOME.items() if (n, uf) in por_nome_uf }   # explícito: o índice tinha Recife como p=1
def capital_de(uf): return CAPITAIS.get(uf)
def rumo(de, para):
    dx = (para[0]-de[0]) * math.cos(math.radians((de[1]+para[1])/2)); dy = para[1]-de[1]
    a = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    return ['a leste','a nordeste','ao norte','a noroeste','a oeste','a sudoeste','ao sul','a sudeste'][int(round(a / 45)) % 8]
def da_capital(m, cap):
    if not cap: return "Interior do estado"
    cx, cy = sede_xy(cap)   # v38: distância a partir da cidade, não do centroide do município (Manaus: 40 km de diferença)
    d = dist_km([cx, cy], [m['x'], m['y']])
    if d < 60: return f"A menos de 60 km {'do' if cap['n'] == 'Rio de Janeiro' else 'de'} {cap['n']}, a capital"
    de = 'do ' if cap['n'] == 'Rio de Janeiro' else 'de '
    return f"A cerca de {int(round(d, -1))} km {rumo([cx, cy], [m['x'], m['y']])} {de}{cap['n']}, a capital"

RIOS_CTX = json.load(open(f'{J}/rios_ctx.json')) if os.path.exists(f'{J}/rios_ctx.json') else {}
UF_NOME = { 'AC':'Acre','AL':'Alagoas','AM':'Amazonas','AP':'Amapá','BA':'Bahia','CE':'Ceará','DF':'Distrito Federal','ES':'Espírito Santo','GO':'Goiás','MA':'Maranhão','MG':'Minas Gerais','MS':'Mato Grosso do Sul','MT':'Mato Grosso','PA':'Pará','PB':'Paraíba','PE':'Pernambuco','PI':'Piauí','PR':'Paraná','RJ':'Rio de Janeiro','RN':'Rio Grande do Norte','RO':'Rondônia','RR':'Roraima','RS':'Rio Grande do Sul','SC':'Santa Catarina','SE':'Sergipe','SP':'São Paulo','TO':'Tocantins' }
def limpa_rio(n): return n.replace('Rio ', '').replace('Ribeirão ', '').split(' ou ')[0].strip().lower()
def nome_ok(n): return not any(t in n for t in ('"', "'", '“', 'Área', 'Base ', 'Usina', 'Distrito Industrial'))

# ── 4) calendário ─────────────────────────────────────────────────────────────────────────────
rnd = random.Random(2026)
muns = sorted(meta.values(), key=lambda m: (m['p'], m['nome'])); capitais = [m for m in muns if m['p'] == 0]; polos = [m for m in muns if m['p'] >= 1]
rnd.shuffle(polos); rnd.shuffle(capitais); rr = rios[:]; rnd.shuffle(rr); oo = onde[:]; rnd.shuffle(oo)
# rios: os 60 maiores primeiro (mais reconhecíveis), embaralhados; depois o resto
fam = [r for r in rios if r['nome'] in FAMOSOS]; fam2 = [r for r in rios if r['nome'] in FAMOSOS2 and r not in fam]; resto = [r for r in rios if r not in fam and r not in fam2]
rr = sorted(fam, key=lambda r: rnd.random()) + sorted(fam2, key=lambda r: rnd.random()) + sorted(resto, key=lambda r: rnd.random())
print('rios famosos', len(fam), len(fam2), 'faltam', [n for n in FAMOSOS if n not in {r['nome'] for r in rios}])
dias = []; d0 = datetime.date(2026, 9, 8)
ptr = { 'polos': 0, 'capitais': 0, 'onde': 0, 'rios': 0 }; listas = { 'polos': polos, 'capitais': capitais, 'onde': oo, 'rios': rr }
ultimo = {}
def proximo(chave, i):
    # cidades: a mesma (nome, uf) não volta em menos de 45 dias, seja qual for o modo
    L = listas[chave]
    for _ in range(len(L)):
        m = L[ptr[chave] % len(L)]; ptr[chave] += 1
        k = (m['nome'], m.get('uf'))
        if chave == 'rios' or i - ultimo.get(k, -999) >= 45:
            ultimo[k] = i; return m
    return L[ptr[chave] % len(L)]
for i in range(200):
    d = d0 + datetime.timedelta(days=i); wd = d.weekday()   # 0 = segunda
    if wd in (0, 3): tipo = 'municipio'; m = proximo('polos', i)
    elif wd == 6: tipo = 'municipio'; m = proximo('capitais', i)
    elif wd in (1, 4): tipo = 'onde'; m = proximo('onde', i)
    else: tipo = 'rio'; m = proximo('rios', i)
    if tipo == 'municipio':
        alvo = { 'cd': m['cd'], 'nome': m['nome'], 'uf': m['uf'], 'x': m['x'], 'y': m['y'], 'area': m['area'], 'bbox': m['bbox'] }
        # a dica regional nunca pode ser o próprio nome (polo da região intermediária, capital): vira distância da capital
        cap = capital_de(m['uf']); eh_cap = cap and cap['n'] == m['nome']
        regional = (f"Região intermediária {'do' if m['rgint'] == 'Rio de Janeiro' else 'de'} {m['rgint']}" if m['rgint'] and m['rgint'] != m['nome'] and not eh_cap else
                    ("É capital de estado" if eh_cap else da_capital(m, cap)))
        dicas = [f"Fica na região {m['regiao']}", f"Bioma: {m['bioma']}" if m['bioma'] else "Bioma: —", f"Estado: {m['uf']}", regional, f"Começa com “{m['nome'][0]}”"]
    elif tipo == 'onde':
        alvo = { 'nome': m['nome'], 'uf': m['uf'], 'x': m['x'], 'y': m['y'] }
        # o nome já é dado: as dicas só podem ajudar a LOCALIZAR
        cap = capital_de(m['uf']); eh_cap = cap and cap['n'] == m['nome']
        dicas = [f"Fica na região {REGIAO_UF.get(m['uf'], '—')}", f"Bioma: {m['bioma']}" if m['bioma'] else "Bioma: —", f"Estado: {m['uf']}",
                 ("É a capital do estado" if eh_cap else da_capital(m, cap))]
    else:
        ctx = RIOS_CTX.get(m['cod'] + '|' + m['nome'], {'ufs': [], 'cidades': []})
        ufs = [UF_NOME.get(u, u) for u in ctx['ufs']][:3]
        atravessa = ("Corre por " + (ufs[0] if len(ufs) == 1 else ', '.join(ufs[:-1]) + ' e ' + ufs[-1])) if ufs else f"Região hidrográfica: {m['rh']}"
        cids = [c['n'] for c in ctx['cidades'] if nome_ok(c['n'])][:3]
        # sem cidade na margem: a região hidrográfica (se ainda não foi usada) ou a cadeia até o mar
        cad = m.get('cadeia') or []
        if cids: margem = "Cidades à margem: " + ', '.join(cids)
        elif ufs and m['rh']: margem = f"Região hidrográfica: {m['rh']}"
        elif len(cad) >= 2: margem = f"Suas águas chegam ao {cad[1] if cad[1] != 'oceano Atlântico' else 'mar'} pelo {cad[0]}"
        else: margem = "Poucas cidades na margem"
        # foz: cidade mais próxima (≤40 km) dá o "perto de" — só se a foz é do próprio rio (código compartilhado com o tronco fica de fora)
        foz_txt = f"Deságua em: {m['desagua']}" if m['desagua'] else "Deságua no mar"
        b = m['bbox']
        if m['foz'] and b[0] - .2 <= m['foz'][0] <= b[2] + .2 and b[1] - .2 <= m['foz'][1] <= b[3] + .2 and ' em ' not in foz_txt and '(' not in foz_txt:
            pc = min((e for e in cidades if nome_ok(e['n'])), key=lambda e: dist_km(sede_xy(e), m['foz']))
            if dist_km(sede_xy(pc), m['foz']) <= 40 and limpa_rio(m['nome']) not in pc['n'].lower(): foz_txt += f", perto de {pc['n']} ({pc['uf']})"
        alvo = { 'nome': m['nome'], 'nomes': [(x.strip() if x.strip().split()[0] in ('Rio','Ribeirão','Vereda','Paraná','Braço') else 'Rio ' + x.strip()) for x in m['nome'].split(' ou ')], 'cod': m['cod'], 'km': m['km'], 'bbox': m['bbox'], 'foz': m['foz'], 'desagua': m['desagua'] }
        dicas = [atravessa, foz_txt, margem, f"Extensão: cerca de {int(round(m['km'], -1))} km", f"Começa com “{letra_rio(m['nome'])}”"]
    dias.append({ 'dia': d.isoformat(), 'tipo': tipo, 'alvo': alvo, 'dicas': dicas })
json.dump(dias, open(f'{J}/desafios.json', 'w'), ensure_ascii=False)
json.dump({ 'municipios': [ { 'cd': m['cd'], 'nome': m['nome'], 'uf': m['uf'], 'x': m['x'], 'y': m['y'] } for m in muns ],
            'rios': [ { 'nome': r['nome'], 'cod': r['cod'], 'x': round((r['bbox'][0]+r['bbox'][2])/2, 3), 'y': round((r['bbox'][1]+r['bbox'][3])/2, 3), 'km': r['km'] } for r in rios ] },
          open(f'{F}/jogo-candidatos.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('calendário', len(dias), dias[0]['tipo'], dias[0]['alvo']['nome'], '|', dias[1]['tipo'], dias[1]['alvo']['nome'], '|', dias[2]['tipo'], dias[2]['alvo']['nome'])
print('candidatos bytes', os.path.getsize(f'{F}/jogo-candidatos.json'))
