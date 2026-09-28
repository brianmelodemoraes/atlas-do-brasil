# Ficha das lojas — Trivia by Brexplora

Textos prontos para colar no App Store Connect e no Google Play Console (v56). Limites de caracteres respeitados.
O app mudou de posicionamento na v48–v49: **o jogo é a porta de entrada; o Atlas do Brasil vive dentro dele.** A ficha antiga
("Atlas do Brasil · Geografia que se move") fica no histórico do git.

## Identidade
| Campo | Valor |
|---|---|
| Nome (30) | **Trivia by Brexplora** |
| Subtítulo iOS (30) | **Geografia do Brasil, todo dia** |
| Descrição curta Android (80) | **Um impostor por dia entre dez lugares do Brasil. Ache os três, aprenda o porquê.** |
| Bundle / package | `com.brexplora.trivia` (definido em `capacitor.config.ts`; **não muda depois de publicado**) |
| Categoria | iOS: primária **Jogos › Trivia**, secundária **Educação** · Android: **Trivia** (tipo Jogo) |
| Classificação etária | iOS **4+** · Android **Livre (L)**. Sem violência, sem anúncios, sem conteúdo de usuários visível (apelido só nos cartões que a própria pessoa compartilha). Tem compras no app (assinatura). |
| Preço | Grátis · assinatura opcional **Trivia Pro** (mensal / anual) |
| Idioma | Português (Brasil) |
| Site | https://atlasbrexplora.app |
| Suporte | https://atlasbrexplora.app/#sobre · brianmelodemoraes@gmail.com |
| Política de privacidade | https://atlasbrexplora.app/privacidade.html |
| Termos de uso (EULA) | https://atlasbrexplora.app/termos.html — colar também no campo *License Agreement* (iOS) porque há assinatura |
| Copyright | © 2026 Brexplora |

## Palavras-chave (iOS, 100 caracteres, separadas por vírgula, sem espaço)
`trivia,quiz,geografia,brasil,mapa,atlas,municípios,estados,rios,enem,vestibular,ibge,desafio,diário`

## Descrição (iOS 4000 / Android 4000)

Um impostor por dia. Dez lugares do Brasil na tela — três não pertencem à categoria. Ache os impostores em um minuto e descubra o porquê.

O IMPOSTOR DO DIA
Todo mundo joga o mesmo enigma, gerado dos dados oficiais do IBGE, da ANA e do DNIT: "ficam no Ceará", "são banhadas pelo São Francisco", "estão na BR-116", "têm mais de 500 mil habitantes". Ao terminar, a lição explica cada lugar — e um botão mostra tudo no mapa de verdade. Desafie um amigo pelo WhatsApp com o placar lado a lado, ou compartilhe o cartão no Story.

RODADA COMPLETA E SEM PARAR
Depois do impostor, mais onze enigmas em nove modos: Top 10, Conexões (quatro grupos de quatro), Vizinhos, Ficha misteriosa, Bingo, Grade 3×3, Pirâmide e Relâmpago. No modo sem parar, o nível sobe enquanto você acerta.

SEU BRASIL VAI ACENDENDO
Cada lugar que você aprende pinta o seu mapa — o Meu Brasil — estado por estado, no atlas. Sequência diária com gelo para não perder tudo por um dia, xp, patentes de explorador (de Curioso a Lenda do Atlas) e ligas com amigos.

UM ATLAS DE VERDADE POR TRÁS
O jogo nasce do Atlas do Brasil: 5.570 municípios, dezenas de camadas oficiais (rios e bacias, biomas, relevo, rodovias, terras indígenas, unidades de conservação, fusos, semiárido, Amazônia Legal…) e 16 capítulos ilustrados em que o mapa acompanha o texto. Tudo aberto no Atlas Livre, camada por camada, com fichas de 34 mil lugares.

SEM CADASTRO
Jogar não pede conta, e-mail ou senha. Se quiser guardar o progresso em outro aparelho, a conta é opcional e sem senha (código por e-mail).

TRIVIA PRO (OPCIONAL)
Vidas sem limite, o arquivo dos últimos 30 impostores e dois gelos por semana — e você apoia um atlas aberto, sem anúncios, feito no Brasil. O Impostor do dia continua grátis para todo mundo, sempre.

Para quem gosta de mapas, para quem estuda para o ENEM e para quem só quer descobrir, todo dia, um pedaço do Brasil que não conhecia.

## Novidades desta versão (iOS "What's New" / Android "Notas da versão")
Primeira versão nas lojas: o Impostor do dia, nove modos de enigma, Meu Brasil, patentes, ligas, conta opcional e o Atlas do Brasil completo por trás do jogo.

## Texto promocional iOS (170)
Um impostor por dia entre dez lugares do Brasil. Ache os três, aprenda o porquê e pinte o seu mapa. Gerado de dados oficiais. Sem cadastro.

## Assinatura (produtos nas lojas — criar ANTES de submeter, com os mesmos IDs)
| | ID do produto | Nome exibido | Preço sugerido |
|---|---|---|---|
| Mensal | `pro_mensal` | Trivia Pro · mensal | R$ 9,90 |
| Anual | `pro_anual` | Trivia Pro · anual | R$ 49,90 (lançamento R$ 39,90 via oferta introdutória) |

Grupo de assinatura (iOS): `Trivia Pro`. Descrição do produto (ambas as lojas): "Vidas sem limite, arquivo dos últimos 30 impostores e dois gelos por semana. Renova automaticamente; cancele quando quiser."
O app, na v56, **não tem o fluxo de compra nativo ainda**: no iOS a tela do Pro mostra "Em breve" (nenhum link externo, como exige a diretriz 3.1.1);
no Android/web abre o link de checkout guardado na tabela `flags` (`checkout_url_mes/ano`) — enquanto vazio, mostra "Avise-me". Quando os produtos existirem, a v57 liga o StoreKit/Play Billing (RevenueCat é o caminho curto).

## Capturas de tela
`docs/lojas/shots/` — geradas do rig iPhone (Playwright) em `ios-6.7/` (1290×2796) a partir do build v56 (PNGs: https://atlasbrexplora.app/loja-shots-v56.zip); refazer com prints reais quando o TestFlight rodar (`python3 scripts/loja-shots.py <pasta>`).
1. Home (herói, sequência, PLAY) · 2. Impostor do dia em jogo · 3. Resultado com a lição e "Ver no mapa" · 4. Conexões · 5. Meu Brasil · 6. Perfil com patentes · 7. Atlas Livre.
Android: 1080×2340 derivadas das mesmas telas. Feature graphic 1024×500: `docs/lojas/feature-graphic.png`. iPad: marcar *iPhone only* na primeira submissão.

## Privacidade — App Store Connect ("App Privacy")
- **Contact Info → Email Address**: coletado, **Linked to You**, finalidade *App Functionality* (conta opcional). Não usado para rastreamento.
- **User Content → Other**: progresso do jogo ligado à conta (xp, resultados) — *App Functionality*, Linked to You.
- **Identifiers → User ID**: o identificador anônimo criado no aparelho — **Not Linked to You** enquanto não há conta; ao criar conta passa a ficar ligado. Responder "Linked" para simplificar.
- **Usage Data → Product Interaction**: eventos anônimos (rota aberta, enigma iniciado/terminado, share) — *Analytics*, Not Linked.
- **Purchases → Purchase History**: só o estado da assinatura (ativa/plano/validade) — *App Functionality*, Linked.
- Tudo o mais: **não coletado** (localização, contatos, fotos, saúde, financeiro — o número do cartão nunca passa pelo app). Rastreamento (ATT): **não**.

## Privacidade — Google Play ("Data safety")
- Coleta dados? **Sim**. Compartilha com terceiros? **Não** (Supabase, Cloudflare, Stripe/Play são processadores).
- **Personal info → Email address**: opcional; finalidade *Account management*; usuário pode pedir exclusão: **Sim**.
- **App activity → App interactions**: eventos anônimos; *Analytics*; opcional (não dá para desligar, mas não é obrigatório para o funcionamento — marcar "required").
- **Device or other IDs**: identificador gerado pelo app; *App functionality* (placar do dia) e *Analytics*.
- **Financial info → Purchase history**: estado da assinatura; *App functionality*.
- Criptografado em trânsito: **Sim**. Exclusão de dados: **Sim** (link: https://atlasbrexplora.app/privacidade.html, seção "Seus direitos"). Play exige também uma **URL de exclusão de conta** — usar a mesma página.

## Permissões que o app pede
- **Notificações** (opcional, oferecida uma vez após o primeiro impostor): lembrete diário às 9h. Justificativa: "Para avisar quando o Impostor do dia estiver disponível".
- Nenhuma outra: sem câmera, localização, contatos ou fotos. Compartilhar usa a folha do sistema (a imagem vai para o cache do próprio app).

## Login social — o que a Apple exige
Se o app oferecer "Continuar com o Google", a diretriz 4.8 obriga a oferecer também **Sign in with Apple**. A v56 só mostra esses botões quando o provedor está ligado no Supabase (`/auth/v1/settings`) — hoje os dois estão desligados, então o app exibe apenas e-mail e a regra não se aplica. Ligar os dois juntos ou nenhum.

## Notas para o revisor (App Review Notes / Play "Instructions for reviewers")
Trivia by Brexplora é um jogo diário de geografia do Brasil. Não exige conta. Para avaliar:
1. Abra o app → "JOGAR O IMPOSTOR": toque nos três lugares que não pertencem à categoria. Ao terminar, abra "A lição de hoje" e "Ver no mapa".
2. "Rodada completa" e a aba "Modos" mostram os outros enigmas. As vidas (5) voltam com o tempo; o Impostor do dia nunca gasta vida.
3. Aba "Perfil" → "Conta · opcional": informe um e-mail e receba um código de 6 dígitos (sem senha). Conta de teste, se preferir não usar um e-mail seu: revisor@… (vamos criar um endereço só para a revisão e colar aqui) — código chega no e-mail em segundos.
4. A tela "Trivia Pro" (Perfil → Trivia Pro) descreve a assinatura; nesta versão a compra dentro do iOS ainda não está ativa e a tela mostra "Em breve", sem links externos.
Conteúdo e mapas vêm de servidores próprios (Cloudflare/Supabase); o app precisa de internet. Contato: brianmelodemoraes@gmail.com.

## Argumento para a diretriz 4.2 (Apple, "minimum functionality") — só se questionado
Não é um site empacotado: jogo diário gerado localmente a partir de uma base de 5.570 municípios, lembrete por notificação local, haptics, compartilhamento nativo de imagem, deep links de desafio, atualização de conteúdo sem passar pela loja, botão voltar nativo no Android e um atlas editorial próprio (16 capítulos, 550+ fichas curadas). A versão web é a porta de entrada; a experiência principal é o app.
