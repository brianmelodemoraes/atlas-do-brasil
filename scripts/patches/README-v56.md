# v54 → v56 — conta opcional, vidas e gelo, Trivia Pro (rumo às lojas)

Mandato do Brian: "execute tudo o que não depende de lojas ou de mim, sempre direcionado ao app na Play Store e na App Store".
Três patches encadeados (`v54.py` → `v55.py` → `v56.py`, cada um com seu `.js`/`.css` ao lado — fonte completa em `https://atlasbrexplora.app/trivia-src-v56.zip`); o build publicado é o v56.
Backend (Supabase, migração `v54_perfis_assinaturas_flags`): tabelas `perfis` (id = auth.users, nome, uf, est jsonb, anonimos uuid[]),
`assinaturas` (usuario, origem manual/stripe/apple/google, status, plano, inicio, fim, ref), `flags` (chave/valor públicas);
RPCs `tem_pro()` e `perfil_vincular(anon)`; RLS "só o próprio".

## v54 — conta opcional (`auth54.js`, `skin54.css`)
- Sem SDK: GoTrue REST direto. `POST /auth/v1/otp {email, create_user}` → `POST /auth/v1/verify {type:"email", email, token}` (código de 6 dígitos)
  **ou** link mágico: tokens chegam em `#access_token=…`; `navegar()` desvia para `AUTH.capturar()`, que busca `/auth/v1/user`, guarda a sessão
  (`localStorage.atlas_sessao`, renovação por `refresh_token` quando falta < 1 min) e cai em `#perfil`.
- Apple/Google só aparecem quando `/auth/v1/settings` diz que o provedor está ligado (hoje: nenhum). Web OAuth via `/auth/v1/authorize`.
- Perfil na nuvem: `puxar()` (GET perfis) → `fundir(local, remoto)` (xp máx, Meu Brasil união, imp/hist união, best máx, sequência pelo `ultimo` mais recente,
  vidas/gelo pelo maior) → `empurrar()` (upsert `on_conflict=id`, `resolution=merge-duplicates`). `salvar()` agenda um empurrão (debounce 3 s) quando há sessão.
  `perfil_vincular(est.jogador)` liga o uuid anônimo à conta.
- Convites (folha inferior, uma vez cada, no máximo um por dia, nunca sobre outro overlay): sequência ≥ 3 (fim do impostor), patente Viajante (ao fechar a
  cerimônia), primeiro "Desafiar" (depois da folha de share), Meu Brasil cruzando 25. Eventos: `conta_convite{gatilho}`, `conta_codigo`, `conta_criada{gatilho, provedor}`,
  `conta_depois`, `conta_saiu`. Bloco "Sua conta" no Perfil (entrar / sincronizar / sair — sair não apaga o progresso local).
- **Depende do Brian** (dashboard do Supabase): Site URL + Redirect URLs, `{{ .Token }}` no template Magic Link, SMTP próprio (Resend, domínio `brexplora.com.br` já verificado).

## v55 — vidas globais e gelo (`vidas55.js`, `skin55.css`)
- `est.vidas {n, t}`: 5 (flag `vidas_max`), +1 a cada 2 h (`vidas_horas`); cheio = relógio parado. `perderVida()` também gasta do estoque, **exceto no Impostor do dia**
  (`ehImpostorDoDia()`), e `alinharVidas()` limita os corações da partida ao estoque. Sem parar e rodada completa não começam com 0 → `semVidas()` mostra
  próxima vida, "+1 lendo a lição de hoje" e "+1 desafiando um amigo" (`darVida`, uma vez por dia cada, `est.bonus`) e o atalho para o Pro.
- Gelo: `est.gelo {n, sem}`, 1 por semana ISO (Pro: 2). `avancarSequencia(dia)` substitui as duas cópias da lógica de sequência: se `ultimo` foi anteontem e há gelo
  (e sequência ≥ 2), gasta o gelo e a sequência continua (toast "🧊 gelo usado"). Home: corações + gelo no cartão de identidade.

## v56 — Trivia Pro (`pro56.js`, `skin56.css`)
- `FLAGS` (tabela `flags`, cache `localStorage.atlas_flags`, `carregarFlags()` no boot): preços, `checkout_url_mes/ano`, vidas, gelo.
- `PRO.conferir()` após login: `rpc/tem_pro` com o token do usuário → `est.pro {pro, ate, origem, plano}`; `ehPro()` libera vidas ∞, 2 gelos, arquivo.
- `#jogo/pro`: herói, 4 benefícios, planos (anual em destaque com preço de lançamento) e ação por plataforma: iOS nativo → "Em breve" (sem link externo — diretriz 3.1.1);
  web/Android → abre `checkout_url_*` (com `client_reference_id` = uid e `prefilled_email`), exigindo conta antes; sem URL → "Avise-me" (`pro_interesse`).
- `#jogo/impostores`: arquivo de 30 dias; hoje + 2 anteriores (ou dia de desafio recebido) livres, o resto 🔒 Pro. `#jogo/trivia/<dia>` respeita a mesma regra.
  Atalhos: fim do impostor/rodada ("Anteriores"), Perfil (05 Impostores anteriores · 06 Trivia Pro · 07 Sobre), selo PRO na home. Sobre: link para termos.
- Loja: `docs/lojas/ficha.md` (nome, textos, privacidade com conta e assinatura), `docs/lojas/so-voce.md` (checklist do Brian), capturas 6,7"
  (`scripts/loja-shots.py`, visual Night; PNGs em `https://atlasbrexplora.app/loja-shots-v56.zip`), `scripts/make-assets.py` (ícone/splash com a marca), `capacitor.config.ts` (`com.brexplora.trivia`), `privacidade.html` + `termos.html` no R2.

Testado no rig iPhone (Playwright) com GoTrue/perfis/flags simulados: `local/probe44.js` (conta), `probe45.js` (vidas, gelo, Pro, arquivo), `probe46.js` (todas as rotas, 0 erros).
