# O que só o Brian pode fazer — e na ordem

Tudo o que não está aqui já foi feito (código nativo, ficha das lojas, capturas, política, ícones, deep-link templates).

## 1 · Contas (abrir hoje — é o gargalo de calendário)
- [ ] **Apple Developer Program** (developer.apple.com, US$ 99/ano, pessoa física ou Brexplora como empresa — empresa exige D-U-N-S e leva mais dias). Anotar o **Team ID** (10 caracteres).
- [ ] **Google Play Console** (play.google.com/console, US$ 25 uma vez). Exige verificação de identidade; contas novas de pessoa física precisam de **teste fechado com 12 testadores por 14 dias** antes da produção — começar isso cedo.

## 2 · Mac (uma tarde)
- [ ] Xcode (App Store) + `xcode-select --install`; Android Studio (SDK 34+); Node 18+.
- [ ] Na pasta do repositório: `git pull && npm install && npm run libs && npm run assets && npx cap add ios && npx cap add android && npx cap sync`.
- [ ] iOS (Xcode): *Signing & Capabilities* → Team; adicionar **Associated Domains** com `applinks:atlasbrexplora.app`; *Product → Archive → Distribute → TestFlight*.
- [ ] Android (Android Studio): *Build → Generate Signed Bundle* (criar keystore — **guardar o .jks e a senha em lugar seguro**, perder = nunca mais atualizar o app); depois `keytool -list -v -keystore <arquivo>.jks` e copiar o **SHA-256**.
- [ ] Mandar para mim: **Team ID** e **SHA-256** → eu preencho `www/.well-known/apple-app-site-association` e `assetlinks.json` e publico no R2 (deep links passam a abrir o app).

## 3 · Lojas (uma hora, com `docs/lojas/ficha.md` aberto ao lado)
- [ ] App Store Connect: criar o app (`com.brexplora.atlas`), colar nome/subtítulo/descrição/palavras-chave, subir capturas de `docs/lojas/shots/ios-6.7`, responder *App Privacy* como na ficha, URL de privacidade, notas ao revisor, escolher o build do TestFlight, enviar.
- [ ] Play Console: criar o app, ficha da loja (descrição curta/longa, capturas `android/`, *feature graphic*), *Data safety* como na ficha, classificação de conteúdo (questionário — tudo "não"), teste interno → fechado → produção.

## 4 · Decisões que são suas
- [ ] **Pergunte ao Atlas**: fica desligado nesta versão (é o que a ficha diz). Se quiser ligado ou pago, me avisa antes da submissão — muda a ficha e o questionário de privacidade.
- [ ] **Rotacionar a chave da Anthropic** (Supabase → Edge Functions → Secrets) — pendente desde a v12.
- [ ] Silhueta: começar pela **região** (como está) ou já pelo **estado**? Um ajuste de uma linha.
- [ ] Nome jurídico no © e no contato: "Brexplora" está como marca; se houver CNPJ, me passa a razão social para a política e o rodapé.

## 5 · Testes com gente (uma semana)
- [ ] TestFlight: você + 5–10 pessoas (convite por e-mail no App Store Connect). Play: lista de testadores internos.
- [ ] Me mandar prints/vídeos do que estranhar: primeira abertura sem rede, permissão de notificação, voltar do Android, teclado, Story.

## Depois que estiver no ar
- [ ] Me mandar os dois links das lojas → eu monto a landing na raiz do domínio (`atlasbrexplora.app`) com os selos e publico o Story de lançamento.
