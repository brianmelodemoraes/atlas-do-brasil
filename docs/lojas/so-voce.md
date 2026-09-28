# O que só o Brian pode fazer — e na ordem (atualizado na v56)

Tudo o que não está aqui já foi feito: conta opcional (e-mail sem senha), perfil na nuvem, vidas e gelo, paywall e arquivo do Pro,
tabelas `perfis` / `assinaturas` / `flags`, política de privacidade e termos, ficha das lojas, projeto Capacitor, capturas.

## 0 · Cinco minutos no Supabase (destrava a conta por e-mail de verdade)
Painel: https://supabase.com/dashboard/project/oolwrsxdwnzofinvjael
- [ ] **Authentication → URL Configuration**: *Site URL* = `https://atlasbrexplora.app/atlas.html`; *Redirect URLs* = `https://atlasbrexplora.app/*` e `com.brexplora.trivia://*`. Sem isso o link mágico do e-mail manda para `localhost:3000`. (O código de 6 dígitos funciona mesmo sem isso.)
- [ ] **Authentication → Emails → Templates → Magic Link**: acrescentar o código no corpo, ex.: `<p>Seu código: <b>{{ .Token }}</b></p>` acima do link. É o que faz o "digite o código" funcionar; o link continua valendo.
- [ ] **Authentication → SMTP Settings** (Project Settings → Auth): ligar *Custom SMTP* com o **Resend**: host `smtp.resend.com`, porta `465`, usuário `resend`, senha = uma API key do Resend (resend.com → API Keys → Create, permissão *Sending access*), remetente `trivia@brexplora.com.br` (o domínio **brexplora.com.br já está verificado** no seu Resend — nada de DNS). Nome do remetente: `Trivia by Brexplora`. Sem isso o Supabase só entrega e-mail para você mesmo e no máximo 2 por hora.
- [ ] (Opcional) **Authentication → Rate Limits**: e-mails por hora ≥ 30.

## 1 · Contas (abrir hoje — é o gargalo de calendário)
- [ ] **Apple Developer Program** (developer.apple.com, US$ 99/ano). Anotar o **Team ID** (10 caracteres). Empresa exige D-U-N-S e leva mais dias; pessoa física é mais rápido.
- [ ] **Google Play Console** (play.google.com/console, US$ 25 uma vez). Contas novas de pessoa física precisam de **teste fechado com 12 testadores por 14 dias** antes da produção — começar cedo.

## 2 · Mac (uma tarde)
- [ ] Xcode (App Store) + `xcode-select --install`; Android Studio (SDK 34+); Node 18+.
- [ ] Na pasta do repositório: `git pull && npm install && npm run libs && npm run assets && npx cap add ios && npx cap add android && npx cap sync`.
- [ ] iOS (Xcode): *Signing & Capabilities* → Team; **Associated Domains** `applinks:atlasbrexplora.app`; *Product → Archive → Distribute → TestFlight*.
- [ ] Android (Android Studio): *Build → Generate Signed Bundle* (criar keystore — **guardar o .jks e a senha**; perder = nunca mais atualizar o app); `keytool -list -v -keystore <arquivo>.jks` e copiar o **SHA-256**.
- [ ] Me mandar **Team ID** e **SHA-256** → eu preencho `www/.well-known/apple-app-site-association` e `assetlinks.json` e publico no R2 (deep links e o link mágico do e-mail passam a abrir o app).

## 3 · Lojas (uma hora, com `docs/lojas/ficha.md` aberto ao lado)
- [ ] App Store Connect: criar o app (`com.brexplora.trivia`), colar nome/subtítulo/descrição/palavras-chave, capturas de `docs/lojas/shots/ios-6.7` (zip em https://atlasbrexplora.app/loja-shots-v56.zip), *App Privacy* como na ficha, URL de privacidade **e** EULA (termos), notas ao revisor, build do TestFlight, enviar.
- [ ] App Store Connect → **Subscriptions**: grupo `Trivia Pro`, produtos `pro_mensal` (R$ 9,90) e `pro_anual` (R$ 49,90, oferta introdutória R$ 39,90). Precisam existir e estar "Ready to Submit" junto com o build que ligar a compra (v57).
- [ ] Play Console: criar o app, ficha (descrição curta/longa, capturas, *feature graphic*), *Data safety* como na ficha (inclui e-mail e assinatura), classificação de conteúdo, **Produtos → Assinaturas** (`pro_mensal`, `pro_anual`), teste interno → fechado → produção.
- [ ] **Assinatura na web (hoje mesmo, sem depender das lojas)**: no Stripe, criar os dois preços e dois *Payment Links* (com Pix ligado). Colar as URLs na tabela `flags` (Supabase → Table Editor → `flags` → `checkout_url_mes` e `checkout_url_ano`). O botão "ASSINAR O PRO" na web e no Android passa a abrir o checkout na hora; o app manda `client_reference_id` = id do usuário. Quando alguém pagar, ative o Pro com o SQL abaixo (ou me passe o e-mail — a automação por webhook vem na v57):
  ```sql
  insert into public.assinaturas (usuario, origem, status, plano, inicio, fim, ref)
  select id, 'stripe', 'ativa', 'ano', now(), now() + interval '1 year', 'cs_xxx' from auth.users where email = 'pessoa@exemplo.com';
  ```
  (Para dar Pro de presente: mesmo comando com `origem = 'manual'` e `ref` = qualquer texto único.)

## 3b · Duas coisas no GitHub (2 minutos, pelo site mesmo)
- [ ] Mover `scripts/workflows-pendentes/backup-conteudo.yml` e `espelhar-r2.yml` para `.github/workflows/` (a integração do Claude não grava ali). Abrir o arquivo → lápis → trocar o caminho no nome → *Commit*.
- [ ] Guardar a chave do painel (`https://atlasbrexplora.app/painel.html#chave=…`, está no diário de bordo) em um lugar seu.

## 4 · Decisões que são suas
- [ ] **Login social**: ligar Google **e** Apple juntos no Supabase (Authentication → Providers) — ou nenhum. A Apple obriga a oferecer Sign in with Apple se houver Google. O app já mostra os botões sozinho quando os provedores estão ligados. Precisa de: OAuth client no Google Cloud (Web) e, na Apple, um *Services ID* + chave `.p8`.
- [ ] **Preços**: R$ 9,90 / R$ 49,90 (lançamento R$ 39,90) estão na tabela `flags` — mude lá e o app acompanha sem publicar nada.
- [ ] **Vidas**: 5 vidas, +1 a cada 2 h — também em `flags` (`vidas_max`, `vidas_horas`, `gelo_por_semana`).
- [ ] **Pergunte ao Atlas** fica desligado nesta versão. Rotacionar a chave da Anthropic (Supabase → Edge Functions → Secrets), pendente desde a v12.
- [ ] Nome jurídico no © e nos termos: "Brexplora" está como marca; se houver CNPJ, me passa a razão social.

## 5 · Testes com gente (uma semana)
- [ ] TestFlight: você + 5–10 pessoas. Play: lista de testadores internos.
- [ ] Testar de verdade a conta: criar com o seu e-mail no celular, entrar com o mesmo e-mail no computador e ver o progresso fundido; sair e entrar de novo; o link do e-mail abrindo o app.
- [ ] Me mandar prints/vídeos do que estranhar: primeira abertura sem rede, permissão de notificação, teclado no formulário de e-mail, Story, tela "sem vidas".

## Depois que estiver no ar
- [ ] Me mandar os dois links das lojas → landing na raiz do domínio com os selos e o Story de lançamento.
- [ ] v57: compra nativa (StoreKit/Play Billing via RevenueCat) + webhook Stripe → `assinaturas` automático.
