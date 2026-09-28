#!/usr/bin/env python3
"""v55 — vidas globais (5, +1 a cada 2 h; o Impostor do dia nunca gasta; rodada completa e Sem parar gastam por erro e não
começam com zero) + tela "sem vidas" com jeitos de ganhar uma + gelo semanal que salva a sequência quando se pula um dia.
Aplica sobre v54 → v55.  Uso: python3 v55.py <entrada.html> <saida.html>   (precisa de vidas55.js e skin55.css ao lado)"""
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
SKIN = open(os.path.join(here, 'skin55.css'), encoding='utf-8').read()
VIDAS = open(os.path.join(here, 'vidas55.js'), encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

sub1('<!-- v54 -->', '<!-- v55 -->')
sub1("#carregando { position:fixed;", SKIN + "\n#carregando { position:fixed;")
sub1('''  /* ═══════════ v54: CONTA OPCIONAL''', VIDAS + '''  /* ═══════════ v54: CONTA OPCIONAL''')
# ── cada erro fora do Impostor do dia gasta uma vida do estoque ──
sub1('''  function perderVida() { RUN.vidas = Math.max(0, RUN.vidas - 1); RUN.combo = 0; RUN.vidaFx = true; hap("erro"); }''',
     '''  function perderVida() { RUN.vidas = Math.max(0, RUN.vidas - 1); RUN.combo = 0; RUN.vidaFx = true; hap("erro"); gastarVida(); alinharVidas(); }''')
# ── Sem parar: não começa sem vidas; corações da partida limitados ao estoque ──
sub1('''      RUN = { tipo:"livre", modo, dia, vidas:3, vidas0:3, pontos:0, combo:0, n:0, log:[], fim:null, inicio:Date.now() };''',
     '''      if (!ehPro() && vidasAtual() <= 0) return semVidas();          // v55
      RUN = { tipo:"livre", modo, dia, vidas:3, vidas0:3, pontos:0, combo:0, n:0, log:[], fim:null, inicio:Date.now() }; alinharVidas();''')
# ── rodada completa: idem, ao entrar e ao retomar ──
sub1('''      if (RUN.fim) return trFim();
      if (RUN.n === 0) {''',
     '''      if (RUN.fim) return trFim();
      if (RUN.fase === "rodada" && !ehPro()) { if (vidasAtual() <= 0) return semVidas(); alinharVidas(); }   // v55
      if (RUN.n === 0) {''')
sub1('''if (r) r.onclick = () => { if (RUN.fim) return trFim(); RUN.fase = "rodada";''',
     '''if (r) r.onclick = () => { if (RUN.fim) return trFim(); if (!ehPro() && vidasAtual() <= 0) return semVidas(); RUN.fase = "rodada"; alinharVidas();''')
# ── sequência com gelo (as duas cópias viram uma função) ──
sub1('''      if (RUN.dia === hoje() && est.ultimo !== RUN.dia) { est.sequencia = est.ultimo === ontemDe(RUN.dia) ? (est.sequencia || 0) + 1 : 1; est.ultimo = RUN.dia; }''',
     '''      avancarSequencia(RUN.dia);   // v55: com gelo''', 2)
# ── bônus: ler a lição e desafiar dão +1 (uma vez por dia) ──
sub1('''    const li = document.getElementById("imp-lic"); if (li) li.querySelector(".l").onclick = () => li.classList.toggle("aberto");''',
     '''    const li = document.getElementById("imp-lic"); if (li) li.querySelector(".l").onclick = () => { li.classList.toggle("aberto"); if (li.classList.contains("aberto") && dia === hoje()) darVida("LIÇÃO LIDA", "licao"); };''')
sub1('''await compartilharDesafio(I, dia); setTimeout(() => AUTH.convidar("desafio"), 700); });''',
     '''await compartilharDesafio(I, dia); darVida("DESAFIO ENVIADO", "desafio"); setTimeout(() => AUTH.convidar("desafio"), 700); });''')
# ── home: corações e gelo no cartão de identidade ──
sub1('''<div class="xpbar"><i style="width:${Math.min(100, Math.round(100 * (xp - base0) / (alvo - base0)))}%"></i></div></div>''',
     '''<div class="xpbar"><i style="width:${Math.min(100, Math.round(100 * (xp - base0) / (alvo - base0)))}%"></i></div>
          <div class="vg"><span>${coracoesHTML()}</span><span class="gelo ${geloStore().n ? "" : "zero"}">🧊 ${geloStore().n} ${geloStore().n === 1 ? "GELO" : "GELOS"}</span></div></div>''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
