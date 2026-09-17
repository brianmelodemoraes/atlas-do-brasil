# v40 · ligas e retenção (aplicado via MCP em 17/09/2026)

Migrations aplicadas no projeto `oolwrsxdwnzofinvjael`: `ligas_v40`, `ligas_v40_fix2`, `ligas_v40_fix3`, `eventos_tipos_v40`.

- Tabelas `ligas(codigo pk 5 letras, nome, criador, criada_em)` e `liga_membros(codigo, jogador, apelido, entrou_em)` — RLS ligado, sem políticas: só as RPCs `security definer` acessam.
- RPCs (anon): `liga_criar(nome, apelido, jogador) → {codigo, nome}` (máx. 20 ligas por jogador), `liga_entrar(codigo, apelido, jogador) → {codigo, nome} | null` (máx. 200 membros), `liga_sair(codigo, jogador)`, `liga_ranking(codigo, jogador)` (só membros; semana ISO em América/Sao_Paulo; pontos, jogos, acertos, resultado de hoje por membro), `liga_minhas(jogador)`.
- `retencao_d7(dias)` (só o `painel` chama): coorte = quem apareceu pela 1ª vez há ≥ 8 dias; voltou = evento entre o 2º e o 8º dia.
- `eventos.tipo` aceita também `revela` e `liga`.
