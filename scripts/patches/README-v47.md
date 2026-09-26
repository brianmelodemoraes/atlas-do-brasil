# v47 — mão de iPhone

Patch reproduzível: `v47.py` (aplica sobre a v46 → v47; usa `skin47.css`). O `.py` completo está no zip de fontes do R2 (`trivia-src-v47.zip`) e no container da sessão (`/home/claude/atlas/patches/v47.py`); esta pasta guarda o CSS e o manifest.

O que muda (tudo no `atlas.html`, JS do bloco JOGO):

1. **Abertura instantânea** — o `#carregando` só espera o mapa nas rotas `capitulo`/`atlas`; nas outras (índice, `#jogo`, ligas, sobre) libera assim que as fontes carregam (até 1,2 s). `carregarDados()` faz as 4 consultas do Supabase em paralelo. `<link rel=preload>` da `trivia-base.json`.
2. **Resposta ao toque** — `:active` com `scale(.965)` em tudo que se toca; classe `novo` no último chip/casa tocado (pop no acerto, shake no erro; `flash-erro` no Bingo); coração perdido pulsa (`RUN.vidaFx`); `hap(tipo)` usa `Capacitor.Plugins.Haptics` quando existe (impact LIGHT / notification ERROR|SUCCESS), senão `navigator.vibrate`.
3. **Transições** — `#jogo-corpo.entra` (enigma novo desliza da direita, e a vista volta ao topo), `#tr-fim.sobe` (lição sobe), placar do resultado conta de 0 até os pontos (`#tr-pts`).
4. **Sem cheiro de site** — `touch-action:manipulation`, `user-select:none` no jogo, `overscroll-behavior:none`, `-webkit-touch-callout:none`. O COMO JOGAR vive no `trTopo()`: compacto, aberto só enquanto `est.tutorial[chaveComo(modo)]` não existe; depois o `?` do cabeçalho abre/fecha (`RUN.pe.ajuda`, listener delegado em `#jogo-corpo`).
5. **Barra de ação** — `.jg-btn.acao` é `position:sticky` no rodapé da vista em fluxo (Confirmar ordem, Enviar grupo, Pular este lugar, Próximo →). Alvos mínimos de 44–48 pt.
6. **Progresso da rodada** — `.tr-prog` com 12 casinhas (ok/erro/atual) no topo do cartucho.
7. **Standalone** — `manifest.json`, `apple-mobile-web-app-capable`, `black-translucent`, `theme-color`, `apple-touch-icon` (`icon-180.png`; 192/512 no manifest).
8. **Ritmo** — `trFimEnigma`: acerto → faixa `.tr-ok` (+pontos, combo, uma frase) e `trProximo()` sozinho em 1,8 s (toque na faixa pula; `POR QUÊ?` segura e abre a lição); erro ou fim → lição + botão sticky. A lição de cada enigma fica em `RUN.log[k].lic` e reabre no resultado (`.tr-item`). Relâmpago: cronômetro de 10 s por afirmação (`e.timer`; estourar = erro).
