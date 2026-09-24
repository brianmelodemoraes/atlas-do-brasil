# Trivia do dia — base factual e gerador (v42)

Fontes completas (scripts + dados intermediários): https://atlasbrexplora.app/trivia-src-v42.zip · base factual: https://atlasbrexplora.app/fatos.json (3,5 MB).

Pipeline reproduzível (Python 3 + shapely, pmtiles, mapbox-vector-tile, requests). Tudo roda contra fontes públicas e os PMTiles do R2:

1. `extrair.py <tileset> <camada> <z>` — extrai uma camada dos PMTiles remotos para GeoJSON (biomas, ZEE, semiárido, Amazônia Legal, Matopiba, faixa de fronteira, portos, aeroportos, rios_nomeados z7, rodovias_federais z7).
2. IBGE: `localidades/municipios?view=nivelado` (mun_ibge.json), SIDRA t/4714 v/93,6318 p/2022 (população e área), malha `intrarregiao=municipio&qualidade=intermediaria` (malha_int.json).
3. `fatos.py` → `fatos.json` (5.570 municípios: UF, regiões, população, área, bioma, litoral, fronteira, semiárido, Amazônia Legal, Matopiba, faixa, rios `Nome|cocursodag`, BRs, vizinhos).
4. `refinar.py` (rios só contam com ≥ 5 km dentro do município; zona cinzenta `perto` a < 6 km), `refinar_br.py` (só trechos existentes — `leg_multim` ≠ Planejada; ≥ 8 km), `fronteira.py` (linha de fronteira = borda da união dos municípios, longe do mar e junto à borda da faixa de fronteira → 120 municípios); litoral = borda do município junto ao mar aberto (ZEE − terra, erodida para excluir lagoas e baías fechadas → 266; Macapá excluída à mão).
5. `viz_capitais.py` — divisas medidas (km compartilhados) para o modo "Fazem divisa com…".
6. `licoes.py` — lições curadas por categoria (rios, BRs, atributos; estados e vizinhanças geradas dos dados); `gerador_trivia.py` — 110 categorias, impostores só fora da zona cinzenta, calendário de 180 dias com curva da semana (seg/ter fácil · qua/qui/dom média · sex/sáb difícil), sem repetir categoria em 60 dias → `trivias.json`.
7. Carga no Supabase: RPC `trivias_carregar(chave, linhas)` (chave = `config.painel`), 30 dias por chamada. Tabelas `trivias` (RLS: dia ≤ hoje SP) e `trivia_jogadas` (insert público); `trivia_resumo(d)`; `liga_ranking` soma mapa + trivia.

Cliente (v42, `scripts/patches/v42.py` no zip): rota `#jogo/trivia[/AAAA-MM-DD]`, 10 chips, 3 vidas, pontos 1000/700/400, tela de lição ("o que fica de hoje" + parágrafo + por-quê de cada item + fonte), WhatsApp, herói no índice, CTA no resultado do mapa, linha nas estatísticas.
