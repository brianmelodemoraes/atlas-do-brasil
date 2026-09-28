#!/usr/bin/env python3
"""v56 — Trivia Pro: paywall (#jogo/pro) com preços e checkout vindos da tabela `flags`, estado Pro conferido na nuvem
(tem_pro), arquivo dos últimos 30 Impostores (#jogo/impostores; hoje + 2 dias livres, o resto Pro), selo PRO na home.
Regras de loja: iOS nativo sem compra externa. Aplica sobre v55 → v56.  Uso: python3 v56.py <entrada.html> <saida.html>   (precisa de pro56.js e skin56.css ao lado)"""
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
SKIN = open(os.path.join(here, 'skin56.css'), encoding='utf-8').read()
PRO = open(os.path.join(here, 'pro56.js'), encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

sub1('<!-- v55 -->', '<!-- v56 -->')
sub1("#carregando { position:fixed;", SKIN + "\n#carregando { position:fixed;")
# ── flags (preços, checkout, vidas) — cache local + busca em segundo plano ──
sub1('''const BASE_URL = location.href.replace(/[#?].*$/, "").replace(/[^/]*$/, "");   // pasta do app (R2 ou bundle nativo)''',
     '''const BASE_URL = location.href.replace(/[#?].*$/, "").replace(/[^/]*$/, "");   // pasta do app (R2 ou bundle nativo)
/* v56: flags remotas (preços do Pro, links de checkout, vidas) — tabela `flags`, cache em localStorage */
let FLAGS = {}; try { FLAGS = JSON.parse(localStorage.getItem("atlas_flags") || "{}") || {}; } catch(e) {}
async function carregarFlags() { try { const l = await sb("flags?select=chave,valor"); const f = {}; l.forEach(x => { f[x.chave] = x.valor; }); FLAGS = f; localStorage.setItem("atlas_flags", JSON.stringify(f)); } catch(e) {} }''')
sub1('''    JOGO.conta.iniciar();   // v54: sessão salva → sincroniza o perfil em segundo plano''',
     '''    JOGO.conta.iniciar();   // v54: sessão salva → sincroniza o perfil em segundo plano
    carregarFlags();        // v56''')
# ── módulo PRO ──
sub1('''  sincAgendar = AUTH.agendar;''', PRO + '''  sincAgendar = AUTH.agendar;''')
# ── rotas ──
sub1('''    if (diaPedido === "estatisticas") return estatisticas();''',
     '''    if (diaPedido === "estatisticas") return estatisticas();
    if (diaPedido === "pro") return PRO.tela();                 // v56
    if (diaPedido === "impostores") return PRO.arquivo();       // v56''')
sub1('''    if (diaPedido.startsWith("trivia/")) { const d = diaPedido.split("/")[1]; return rodada("dia", null, /^\\d{4}-\\d{2}-\\d{2}$/.test(d) && d < hoje() ? d : hoje()); }''',
     '''    if (diaPedido.startsWith("trivia/")) { const d = diaPedido.split("/")[1], dd = /^\\d{4}-\\d{2}-\\d{2}$/.test(d) && d < hoje() ? d : hoje(); if (dd !== hoje() && !PRO.podeJogarDia(dd)) return PRO.tela(); return rodada("dia", null, dd); }''')
# ── atalhos: fim do impostor / fim da rodada, perfil, home ──
sub1('''<span data-ir="#jogo/ligas" style="cursor:pointer;text-decoration:underline">Ligas</span> · <span data-ir="#"''',
     '''<span data-ir="#jogo/impostores" style="cursor:pointer;text-decoration:underline">Anteriores</span> · <span data-ir="#jogo/ligas" style="cursor:pointer;text-decoration:underline">Ligas</span> · <span data-ir="#"''', 2)
sub1('''        <div class="sumario-item" data-ir="#sobre" style="cursor:pointer;border-bottom:none"><span class="num">05</span><span class="tit">Sobre · fontes · privacidade</span><span class="meta">→</span></div></div>`;''',
     '''        <div class="sumario-item" data-ir="#jogo/impostores" style="cursor:pointer"><span class="num">05</span><span class="tit">Impostores anteriores</span><span class="meta">→</span></div>
        <div class="sumario-item" data-ir="#jogo/pro" style="cursor:pointer"><span class="num">06</span><span class="tit" style="color:var(--ouro)">Trivia Pro${ehPro() ? " · ativo" : ""}</span><span class="meta">→</span></div>
        <div class="sumario-item" data-ir="#sobre" style="cursor:pointer;border-bottom:none"><span class="num">07</span><span class="tit">Sobre · fontes · privacidade</span><span class="meta">→</span></div></div>`;''')
sub1('''<span class="ed">EDITAR</span>''', '''${ehPro() ? `<span class="pro">PRO</span>` : ""}<span class="ed">EDITAR</span>''')
# ── Sobre: termos de uso ao lado da privacidade ──
sub1('''privacidade.html" target="_blank" rel="noopener">Política de privacidade completa →</a></div>''',
     '''privacidade.html" target="_blank" rel="noopener">Política de privacidade →</a> · <a href="https://atlasbrexplora.app/termos.html" target="_blank" rel="noopener">Termos de uso →</a></div>''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
