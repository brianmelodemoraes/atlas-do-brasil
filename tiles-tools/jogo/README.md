# Desafio do dia (v32)

`prep.py` gera, a partir dos tiles e do índice de busca:

- `final/jogo-silhuetas.json` — contornos simplificados dos municípios candidatos (p ≤ 2), por CD_MUN (R2, `?v=1`)
- `final/jogo-candidatos.json` — listas para autocomplete/feedback (municípios e rios ≥150 km com código Otto)
- `jogo/desafios.json` — calendário de 200 dias (seg/qui município-polo · dom capital · ter/sex "onde é?" · qua/sáb rio)

O calendário vai para a tabela `desafios` do Supabase (upsert por `dia`); RLS só entrega o desafio de hoje e os passados
(fuso America/Sao_Paulo). Resultados anônimos em `jogadas` (insert-only, unique dia+jogador); ranking do dia por `resumo_dia(d)`.
