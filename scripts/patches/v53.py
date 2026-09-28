#!/usr/bin/env python3
"""v53 — Conexões: no máximo um grupo "Ficam em <estado>" por enigma e no máximo dois grupos do mesmo tema
(dois rios ok; dois estados não). Aplica sobre v52 → v53."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)
sub1('<!-- v52 -->', '<!-- v53 -->')
sub1('''      const tenta = c => {
        if (escolhidas.some(g => g.itens.some(i => c.setC.has(i)))) return false;          // itens já escolhidos não podem pertencer a esta''',
'''      const tenta = c => {
        if (c.tema === "uf" && escolhidas.some(g => g.cat.tema === "uf")) return false;    // v53: um "Ficam em…" por enigma
        if (escolhidas.filter(g => g.cat.tema === c.tema).length >= 2) return false;        // v53: no máximo dois do mesmo tema
        if (escolhidas.some(g => g.itens.some(i => c.setC.has(i)))) return false;          // itens já escolhidos não podem pertencer a esta''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
