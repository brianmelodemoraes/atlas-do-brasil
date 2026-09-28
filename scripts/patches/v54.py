#!/usr/bin/env python3
"""v54 — conta opcional (e-mail sem senha, código ou link mágico), perfil na nuvem (tabela `perfis`), convites em quatro
momentos de intenção alta, bloco "Sua conta" no Perfil. Ninguém é obrigado a entrar. Aplica sobre v53 → v54.
Uso: python3 v54.py <entrada.html> <saida.html>   (precisa de auth54.js e skin54.css ao lado — trivia-src-v56.zip no R2)"""
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
SKIN = open(os.path.join(here, 'skin54.css'), encoding='utf-8').read()
AUTH = open(os.path.join(here, 'auth54.js'), encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

sub1('<!-- v53 -->', '<!-- v54 -->')
sub1("#carregando { position:fixed;", SKIN + "\n#carregando { position:fixed;")
# ── salvar() avisa a sincronização (debounce dentro do AUTH) ──
sub1('''  function salvar() { try { localStorage.setItem("atlas_jogo", JSON.stringify(est)); } catch(e) {} }''',
     '''  let sincAgendar = null;                          // v54: definido pelo AUTH — empurra o perfil para a nuvem quando há conta
  function salvar() { try { localStorage.setItem("atlas_jogo", JSON.stringify(est)); } catch(e) {} if (sincAgendar) sincAgendar(); }''')
# ── módulo AUTH dentro do JOGO; exposto como JOGO.conta ──
sub1('''  return { abrir, fechar, toque, cartaoIndice, desafio, abas, filtroMeu, bboxMeu, abertura, story: () => storyFile, run: () => RUN };''',
     AUTH + '''  sincAgendar = AUTH.agendar;
  return { abrir, fechar, toque, cartaoIndice, desafio, abas, filtroMeu, bboxMeu, abertura, conta:AUTH, story: () => storyFile, run: () => RUN };''')
# ── Perfil: bloco "Sua conta" logo abaixo de "Como você aparece" ──
sub1('''        <button class="jg-btn" id="pf-ok">Salvar</button></div>
      <div class="gcard"><div class="eyebrow red">Patentes</div>''',
     '''        <button class="jg-btn" id="pf-ok">Salvar</button></div>
      ${AUTH.perfilHTML()}
      <div class="gcard"><div class="eyebrow red">Patentes</div>''')
sub1('''    document.getElementById("pf-ok").onclick = () => { est.nome = document.getElementById("pf-nome").value.replace(/[<>]/g, "").trim().slice(0, 18); est.uf = document.getElementById("pf-uf").value || ""; salvar(); toast("PERFIL SALVO"); montarPerfil(); };''',
     '''    document.getElementById("pf-ok").onclick = () => { est.nome = document.getElementById("pf-nome").value.replace(/[<>]/g, "").trim().slice(0, 18); est.uf = document.getElementById("pf-uf").value || ""; salvar(); toast("PERFIL SALVO"); montarPerfil(); };
    AUTH.ligarPerfil();''')
# ── convites ──
sub1('''    placarImpostor(dia);
    try { document.getElementById("v-jogo").scrollTo({ top:0 }); } catch(x) {}''',
     '''    placarImpostor(dia);
    if (dia === hoje() && (est.sequencia || 0) >= 3) setTimeout(() => AUTH.convidar("sequencia"), 1600);   // v54
    try { document.getElementById("v-jogo").scrollTo({ top:0 }); } catch(x) {}''')
sub1('''    document.getElementById("nu-ok").onclick = () => el.remove();''',
     '''    document.getElementById("nu-ok").onclick = () => { el.remove(); if (novaPatente && pat === "Viajante") setTimeout(() => AUTH.convidar("patente"), 400); };''')
sub1('''    document.getElementById("imp-desafiar").onclick = () => comNome(() => compartilharDesafio(I, dia));''',
     '''    document.getElementById("imp-desafiar").onclick = () => comNome(async () => { await compartilharDesafio(I, dia); setTimeout(() => AUTH.convidar("desafio"), 700); });''')
sub1('''    if (novos) salvar();
    return novos;''',
     '''    if (novos) { salvar(); const n = resumoMeu().n; if (n >= 25 && n - novos < 25) setTimeout(() => AUTH.convidar("meu"), 1800); }
    return novos;''')
# ── boot / navegação: tokens no hash são do login, não uma rota ──
sub1('''async function navegar() {
  if (location.hash.startsWith("#d/"))''',
     '''async function navegar() {
  if (/access_token=/.test(location.hash)) { JOGO.conta.capturar(); return; }   // v54: volta do link mágico / OAuth
  if (location.hash.startsWith("#d/"))''')
sub1('''    montarIndice();
    navegar();''',
     '''    montarIndice();
    navegar();
    JOGO.conta.iniciar();   // v54: sessão salva → sincroniza o perfil em segundo plano''')
# ── Sobre: privacidade ──
sub1('''O Atlas não exige cadastro nem coleta dados pessoais. O Desafio do dia usa um identificador anônimo criado no seu aparelho.''',
     '''O Atlas não exige cadastro: jogar é anônimo, com um identificador criado no seu aparelho. A conta é opcional e guarda só o seu e-mail e o seu progresso no jogo, para você continuar em outro aparelho. Dá para sair (e apagar a conta pelo e-mail acima) quando quiser.''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
