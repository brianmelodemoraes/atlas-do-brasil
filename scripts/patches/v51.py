#!/usr/bin/env python3
"""v51 — auditoria de vazamentos: nada na tela pode entregar a resposta.
- Impostor com categoria de estado ("Ficam no Ceará"): a sigla do estado sai dos chips (entra a população).
- Conexões com algum grupo de estado: sigla sai de todos os chips.
- Grade 3×3: as opções não mostram a sigla (a coluna "outro estado" ficava óbvia).
- Ficha misteriosa: opções só com o nome (a pista "Estado" e a "População" entregavam).
- Bingo com casa de estado: o lugar da vez não mostra a sigla.
- Cartão do Impostor: sem sigla quando a categoria é de estado.
Aplica sobre v50 → v51.  Uso: python3 v51.py <entrada.html> <saida.html>"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

sub1('<!-- v50 -->', '<!-- v51 -->')
# opcoesHTML ganha o terceiro parâmetro semUF
sub1('''const opcoesHTML = (ops, comPop) => `<div class="es-grid">${ops.map(i => { const m = mun(i); return `<div class="es-op" data-i="${i}"><div class="n">${esc(m.nome)}</div><div class="u">${m.uf}${comPop && m.pop ? " · " + fmtN(m.pop) + " hab." : ""}</div></div>`;''',
     '''const opcoesHTML = (ops, comPop, semUF) => `<div class="es-grid">${ops.map(i => { const m = mun(i); return `<div class="es-op" data-i="${i}"><div class="n">${esc(m.nome)}</div><div class="u">${semUF ? "" : m.uf}${comPop && m.pop ? (semUF ? "" : " · ") + fmtN(m.pop) + " hab." : ""}</div></div>`;''')
# impostor: categoria de estado → sem sigla
sub1('''      const tocado = Object.fromEntries(e.toques.map(x => [x.i, x.imp])), fim = !!e.fim, ult = e.toques.length ? e.toques[e.toques.length - 1].i : -1;''',
     '''      const tocado = Object.fromEntries(e.toques.map(x => [x.i, x.imp])), fim = !!e.fim, ult = e.toques.length ? e.toques[e.toques.length - 1].i : -1, semUF = !!(p.cat && p.cat.tema === "uf");''')
sub1('''<div class="tv-chip ${cls}${it.i === ult ? " novo" : ""}" data-i="${it.i}"><div class="n">${esc(m.nome)}</div><div class="u">${m.uf}</div>''',
     '''<div class="tv-chip ${cls}${it.i === ult ? " novo" : ""}" data-i="${it.i}"><div class="n">${esc(m.nome)}</div><div class="u">${semUF ? fmtN(m.pop) + " hab." : m.uf}</div>''')
# conexões: algum grupo de estado → sem sigla
sub1('''const chips = rest.map(it => { const m = mun(it.i); return `<div class="cx-chip ${e.sel.includes(it.i) ? "sel" : ""}" data-i="${it.i}"><div class="n">${esc(m.nome)}</div><div class="u">${m.uf}</div></div>`; }).join("");''',
     '''const semUF = p.grupos.some(G => G.cat && G.cat.tema === "uf");
      const chips = rest.map(it => { const m = mun(it.i); return `<div class="cx-chip ${e.sel.includes(it.i) ? "sel" : ""}" data-i="${it.i}"><div class="n">${esc(m.nome)}</div><div class="u">${semUF ? "" : m.uf}</div></div>`; }).join("");''')
# grade: opções sem sigla
sub1('''opcoesHTML(p.celulas[e.aberta].ops, true)''', '''opcoesHTML(p.celulas[e.aberta].ops, true, true)''')
# ficha: opções só com o nome
sub1('''${!fim && e.rev < p.pistas.length ? `<div class="mais" id="fi-mais">+ mais uma pista (−40)</div>` : ""}</div>` + opcoesHTML(p.opcoes) +''',
     '''${!fim && e.rev < p.pistas.length ? `<div class="mais" id="fi-mais">+ mais uma pista (−40)</div>` : ""}</div>` + opcoesHTML(p.opcoes, false, true) +''')
# bingo: casa de estado na cartela → o lugar da vez sem sigla
sub1('''<div class="u">${mun(atual.i).uf} · ${fmtN(mun(atual.i).pop)} hab.</div>''',
     '''<div class="u">${p.celulas.some(c => c.tema === "uf") ? "" : mun(atual.i).uf + " · "}${fmtN(mun(atual.i).pop)} hab.</div>''')
# cartão do impostor: sem sigla em categoria de estado
sub1('''nomes:p.itens.map(it => [mun(it.i).nome, mun(it.i).uf]), cena:cenaDoEnigma(p) };''',
     '''nomes:p.itens.map(it => [mun(it.i).nome, p.cat && p.cat.tema === "uf" ? "" : mun(it.i).uf]), cena:cenaDoEnigma(p) };''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
