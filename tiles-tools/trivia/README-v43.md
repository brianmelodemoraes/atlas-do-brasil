# v43 — só trivia: banco ilimitado gerado no aparelho

Fontes completas: https://atlasbrexplora.app/trivia-src-v43.zip (scripts Python, `pacote.py`, `trivia43.js`, `v43.py`).

- `pacote.py` → `trivia-base.json` (730 KB, ~260 KB gzip; servido em https://atlasbrexplora.app/trivia-base.json): 5.570 municípios compactos `[cd, nome, uf, pop, área, x, y, bioma, flags, rios[], brs[], meso]`, vizinhos, ufviz, 112 categorias com `c` (todos os membros ≥ 12 mil hab., por população) e `i` (até 60 impostores ordenados por *tentação* = distância ao conjunto / fama), lições, notas, 120 rios por extensão.
- Cliente (`trivia43.js`, dentro da IIFE JOGO): RNG semeado (`rng(seed)`), geradores `gerarImpostor/gerarConexoes/gerarDuelo/gerarEstado(r, nível)`, rodada do dia (12 enigmas no plano `DIA_PLANO`, 5 vidas, semente = data, retomável de `est.tr.dia`) e modo livre (3 vidas, nível 1→2→3 aos 3 e 8 enigmas). Pontos: impostor 300·[1,.7,.4,.25][erros]·nível; conexões 300·(1−.2·tentativas extras)·nível; duelo/estado 50·combo(≤4)·nível.
- Supabase: `trivia_jogadas` (modo `rodada`, pontos ≤ 10000), `trivia_runs` + `trivia_ranking(m, jogador)` (melhor da semana, posição), `liga_ranking` soma trivia.
- Rotas: `#jogo` rodada do dia · `#jogo/livre/<impostor|conexoes|duelo|estado>` · `#jogo/mapa[/dia]` (jogos de mapa antigos, fora do índice).
