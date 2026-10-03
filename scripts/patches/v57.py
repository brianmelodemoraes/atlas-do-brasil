#!/usr/bin/env python3
"""v57 — (1) modo "Meio a Meio": dividir a população de um recorte ao meio com uma reta (Brasil/regiões → estados → quadrados),
entra em Modos, no Sem parar e no fim da rodada completa; (2) apagar a conta dentro do app (Apple 5.1.1(v)) via Edge Function
`conta-apagar`. Aplica sobre v56 → v57.  Uso: python3 v57.py <entrada.html> <saida.html>   (precisa de meio57.js e skin57.css ao lado — trivia-src-v57.zip)"""
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
SKIN = open(os.path.join(here, 'skin57.css'), encoding='utf-8').read()
MEIO = open(os.path.join(here, 'meio57.js'), encoding='utf-8').read()
def sub1(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

sub1('<!-- v56 -->', '<!-- v57 -->')
sub1("#carregando { position:fixed;", SKIN + "\n#carregando { position:fixed;")
# ── módulo do modo (depois de GERA/RENDER/LICAO e do UF_MINI; antes das vidas) ──
sub1('''  /* ═══════════ v55: VIDAS GLOBAIS E GELO''', MEIO + '''  /* ═══════════ v55: VIDAS GLOBAIS E GELO''')
# ── ícone, plano da rodada, textos ──
sub1('''    ficha:`<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>`,''',
     '''    ficha:`<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>`,
    meio:`<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M4.5 19.5L19.5 4.5"/><circle cx="8.5" cy="9" r="1.4" fill="#fff"/><circle cx="15.5" cy="15" r="1.4" fill="#fff"/><circle cx="14" cy="8" r=".9" fill="#fff"/><circle cx="10" cy="16" r=".9" fill="#fff"/></svg>`,''')
sub1('''"impostor", "conexoes", "piramide"];''', '''"impostor", "conexoes", "meio"];   // v57: o Meio a Meio fecha a rodada''')
sub1('''A rodada completa junta os nove.''', '''A rodada completa junta os dez.''')
sub1('''Doze enigmas, seis vidas, os nove modos''', '''Doze enigmas, seis vidas, os dez modos''')
# ── Meu Brasil e "ver no mapa" aprendem os três maiores do recorte ──
sub1('''        case "ficha": return ok ? [p.mi] : [];''', '''        case "meio": return ok ? p.top : [];
        case "ficha": return ok ? [p.mi] : [];''')
sub1('''        case "ficha": push(p.mi, "ok"); break;''', '''        case "meio": p.top.forEach(i => push(i, "ok")); break;
        case "ficha": push(p.mi, "ok"); break;''')
# ── a faixa de acerto fica mais tempo no Meio a Meio (a reta verde é a revelação) ──
sub1('''const t = setTimeout(seguir, 1800);''', '''const t = setTimeout(seguir, p.modo === "meio" ? 3600 : 1800);''')
# ── apagar a conta no app ──
sub1('''<span id="conta-sinc">Sincronizar agora</span> · <span id="conta-sair">Sair</span></div></div>`;''',
     '''<span id="conta-sinc">Sincronizar agora</span> · <span id="conta-sair">Sair</span> · <span id="conta-apagar" class="perigo">Apagar conta</span></div></div>`;''')
sub1('''if (x) x.onclick = sair; }''', '''if (x) x.onclick = sair; const ap = document.getElementById("conta-apagar"); if (ap) ap.onclick = apagarConfirmar; }''')
sub1('''    /* ── bloco no perfil ── */''',
     '''    /* ── v57: apagar a conta (exigência das lojas) — confirma em folha, chama a Edge Function, mantém o progresso local ── */
    function apagarConfirmar() {
      if (!logado() || document.getElementById("conta-sheet")) return;
      const el = document.createElement("div"); el.id = "conta-sheet";
      el.innerHTML = `<div class="veu"></div><div class="folha"><div class="puxa"></div><div class="eb" style="color:var(--err)">APAGAR A CONTA</div><h2>Tem certeza, <em>${esc(email())}</em>?</h2>
        <p>Apagamos agora o seu e-mail, o progresso guardado na nuvem e a assinatura ligada a esta conta. O que está neste aparelho continua aqui, como jogador anônimo. Não dá para desfazer.</p>
        <button class="play perigo" id="ca-ok"><span class="tri"></span><span>APAGAR MINHA CONTA</span></button><div class="depois" id="ca-nao">Cancelar</div></div>`;
      document.body.appendChild(el); requestAnimationFrame(() => el.classList.add("on"));
      const fechar = () => { el.classList.remove("on"); setTimeout(() => el.remove(), 320); };
      el.querySelector(".veu").onclick = fechar; document.getElementById("ca-nao").onclick = fechar;
      document.getElementById("ca-ok").onclick = async () => {
        const b = document.getElementById("ca-ok"); b.disabled = true; b.querySelector("span:last-child").textContent = "APAGANDO…";
        const t = await token(); let ok = false, msg = "";
        try { const r = await fetch(`${SB_URL}/functions/v1/conta-apagar`, { method:"POST", headers:cab(t), body:"{}" }); ok = r.ok; if (!ok) msg = (await erroDe(r)) || ("erro " + r.status); } catch(e) { msg = "sem conexão"; }
        if (!ok) { b.disabled = false; b.querySelector("span:last-child").textContent = "APAGAR MINHA CONTA"; toast("NÃO DEU: " + msg.toUpperCase().slice(0, 40)); return; }
        guardar(null); est.pro = null; salvar(); medir("conta_apagada", {}); fechar(); hap("sucesso"); toast("CONTA APAGADA · VOCÊ CONTINUA JOGANDO COMO ANÔNIMO");
        if (typeof montarPerfil === "function") montarPerfil();
      };
    }
    /* ── bloco no perfil ── */''')
sub1('''Dá para sair (e apagar a conta pelo e-mail acima) quando quiser.''', '''Dá para sair ou apagar a conta no Perfil quando quiser.''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
