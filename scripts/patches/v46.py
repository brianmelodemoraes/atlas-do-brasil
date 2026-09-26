#!/usr/bin/env python3
"""v46 — layout "fluxo" nas telas de trivia/ligas/estatísticas: o cartucho deixa de ficar ancorado no rodapé
(herança dos jogos de mapa) e passa a fluir logo abaixo do cabeçalho, com a tela inteira rolando.
Os jogos de mapa (#jogo/mapa, anteriores) continuam com o cartucho sobre o mapa. Aplica sobre v45 → v46.
Uso: python3 v46.py <entrada.html> <saida.html>"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)

sub1('<!-- v45 -->', '<!-- v46 -->')
# CSS: modo fluxo
sub1("#carregando { position:fixed;", """/* v46: telas sem mapa (trivia, ligas, estatísticas) fluem de cima para baixo e a vista rola inteira */
#v-jogo.fluxo { background:var(--paper); overflow-y:auto; -webkit-overflow-scrolling:touch; overscroll-behavior:contain; }
#v-jogo.fluxo #jogo-fundo { display:none !important; }
#v-jogo.fluxo #jogo-topo { position:relative; padding-bottom:6px; }
#v-jogo.fluxo #jogo-card { position:relative; left:auto; right:auto; bottom:auto; width:calc(100% - 24px); max-height:none; overflow:visible; margin:4px auto calc(env(safe-area-inset-bottom) + 28px); }
#carregando { position:fixed;""")
# JS: liga o fluxo nas telas de cabeçalho (trivia, ligas, estatísticas) e desliga nos jogos de mapa e ao fechar
sub1("""  function cabecalho(eb, titulo) {
    document.getElementById("jogo-fundo").style.display = "block"; mapaJogo(true); interagir(false);""",
"""  const fluxo = on => document.getElementById("v-jogo").classList.toggle("fluxo", !!on);
  function cabecalho(eb, titulo) {
    fluxo(true); document.getElementById("jogo-fundo").style.display = "block"; mapaJogo(true); interagir(false);""")
sub1("""    document.getElementById("jogo-fundo").style.display = "block";
    marcar([]); selecionarTodo(null, {}); limparHL();""",
"""    fluxo(false); document.getElementById("jogo-fundo").style.display = "block";
    marcar([]); selecionarTodo(null, {}); limparHL();""")
sub1("""  async function arquivo() {
    document.getElementById("jogo-fundo").style.display = "block";""",
"""  async function arquivo() {
    fluxo(false); document.getElementById("jogo-fundo").style.display = "block";""")
sub1('function fechar() { ativo = false; mapaJogo(false); document.getElementById("jogo-fundo").style.display = "none"; }',
     'function fechar() { ativo = false; fluxo(false); mapaJogo(false); document.getElementById("jogo-fundo").style.display = "none"; }')
# o ajuste do teclado (cartucho ancorado) não se aplica ao fluxo
sub1('const ajustar = () => { const c = document.getElementById("jogo-card"); if (!c || !ativo) return;',
     'const ajustar = () => { const c = document.getElementById("jogo-card"); if (!c || !ativo || document.getElementById("v-jogo").classList.contains("fluxo")) return;')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
# texto do jogo do rio ainda falava em "vermelho" (traçado é verde desde a v44)
s = open(dst, encoding='utf-8').read()
assert s.count('traçado em vermelho') == 2
s = s.replace('traçado em vermelho', 'traçado em verde')
open(dst, 'w', encoding='utf-8').write(s)
print('ok2', len(s))
