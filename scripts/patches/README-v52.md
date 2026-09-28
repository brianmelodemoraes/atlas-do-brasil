# v52 — Conexões inteligente

Brian: "tinham quatro capitais, mas eram correlacionadas por outro fator; tanto um quanto o outro funcionam — tem que ter essa inteligência". Duas frentes (`v52.py`, fonte no container e no próximo zip):

1. **Gerador** (`gerarConexoes`): depois de montar os 4 grupos, `conexoesAmbiguas()` procura qualquer outra categoria de `BASE.cat` (ou o mesmo estado) que junte ≥ 4 dos 16 lugares vindos de ≥ 2 grupos diferentes; se achar, tenta de novo (até 100 de 120 tentativas; depois aceita e deixa o item 2 cuidar). Em ~40 enigmas gerados no rig, sobrou 1 ambíguo (região amazônica no nível 3).
2. **Envio** (`trEnviarCx`): se os 4 selecionados não são um grupo oficial, `conexaoAlternativa()` verifica se compartilham uma categoria fora das oficiais, o mesmo estado ("Ficam no Amazonas") ou o mesmo bioma. Se sim: mensagem verde "✓ Também vale: Capitais estaduais · +50. Mas não é um dos quatro grupos de hoje — procure outra ligação.", +50 pontos (uma vez por categoria alternativa), **sem perder vida** e sem contar tentativa. A grade só treme no erro de verdade (`e.msgOk`).
