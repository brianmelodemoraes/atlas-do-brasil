# v57 — Meio a Meio + apagar conta no app

Brian (vídeo do GeoGuessr/"population split"): "um quadrado e temos que achar a exata divisão de população. Conseguimos implementar?" → "Faça".
Patch `v57.py` (+ `meio57.js`, `skin57.css`, fonte completa em `https://atlasbrexplora.app/trivia-src-v57.zip`), aplica sobre v56.

## Meio a Meio (décimo modo)
- **Recortes por nível**: 1 = Brasil (35 %) ou uma das 5 regiões; 2 = estado com ≥ 60 municípios (75 %) ou região; 3 = quadrado aleatório de 26–54 unidades do viewBox (≈ 400–800 km) centrado perto de um município ≥ 30 mil hab., com ≥ 40 municípios e ≥ 400 mil pessoas. Guarda: nenhum município pode ter > 35 % do recorte (Manaus = 56 % do Amazonas tornaria o jogo impossível). Não repete o recorte dentro da partida.
- **Projeção**: os 5.570 municípios vão para o viewBox do `UF_MINI` (300×300) por Web Mercator ajustado (`x = 7,325·lng + 542,5`, `y = 44,5 − 7,25·mercator(lat)`), 95,6 % dos pontos caem dentro do próprio estado — os contornos dos estados servem de fundo. Pontos com raio ∝ √pop.
- **Interação**: SVG com duas alças (pointer events, `setPointerCapture`, `touch-action:none`); arrasta alça A, alça B ou a reta inteira. "Dividir" soma a população de cada lado pelo sinal do produto com a normal.
- **Pontuação**: diff = |fração − 0,5|; ≤ 1 % = 1.000; senão 1000·(1 − diff/0,25)^1,5 (55/45 ≈ 716, 60/40 ≈ 447); ok até 60/40, fora disso perde vida. × nível como os outros modos.
- **Revelação**: reta verde tracejada = paralela à do jogador deslocada até a mediana populacional; placar azul/laranja por lado com nome do lado (leste/oeste/norte/sul); lição diz a distância em km até a metade exata e os três municípios que puxam o peso. A faixa de acerto fica 3,6 s (em vez de 1,8) para a reta verde ser vista.
- Entra em `MODO`, `montarModos` ("os dez modos"), Sem parar (`#jogo/livre/meio`) e fecha a rodada completa (`DIA_PLANO[11]`, nível 3). Meu Brasil aprende os 3 maiores do recorte; "Ver no mapa" acende os três.

## Apagar conta (Apple 5.1.1(v) / Google Play)
- Edge Function `conta-apagar` (verify_jwt): valida o JWT do usuário, apaga `assinaturas` e `perfis` e chama `auth.admin.deleteUser` com a service role. (Uma função SQL `security definer` com `delete from auth.users` foi tentada antes; a ferramenta de migração trava pedindo confirmação para esse comando.)
- App: Perfil → Sua conta → "Apagar conta" (vermelho) → folha de confirmação → POST na função → sessão removida, `est.pro` zerado, progresso local preservado, toast. Evento `conta_apagada`. Privacidade e ficha atualizadas.

Testado no rig (probe47: geração, arrasto de alça e de reta, divisão perfeita = 1.000, erro grosseiro perde vida, lição, apagar conta; probe48: 14 rodadas seguidas, níveis 1→2→3 sem repetição; probe46: 16 rotas sem erro).
