# Atlas do Brasil · by Brexplora

Atlas geográfico narrativo, nascido mobile: 14 capítulos com *scrollytelling* cartográfico, Atlas Livre com 43 camadas
(IBGE · ANA · DNIT · ANEEL · ICMBio · FUNAI · INCRA · CPRM · Embrapa), fichas curadas + geradas sob demanda, busca de
34 mil lugares e o módulo **Pergunte ao Atlas** (IA, Pro).

## Arquitetura (o que roda onde)

| Peça | Onde | Observação |
|---|---|---|
| App (HTML único) | `www/index.html` = `atlas.html` publicado no R2 | mesmo arquivo no site e dentro do app nativo. **Produção (R2) é a fonte da verdade**: a Action `espelhar-r2` copia o `atlas.html` do R2 para `www/index.html` a cada mudança em `VERSION` (e todo dia às 6h UTC) |
| Bibliotecas, fontes, glifos | `www/lib/` (auto-hospedado) | **zero CDN** em produção; `npm run libs` reconstrói |
| Tiles vetoriais | R2: `atlas-base.pmtiles` (449 MB), `atlas-detail.pmtiles` (926 MB), `atlas-overview.pmtiles` (4,0 MB, z0–6 infra + rios ≥120 km) | Cloudflare R2, bucket `atlas-brexplora` |
| Relevo | AWS Terrain Tiles (Mapzen, terrarium) | público |
| Satélite | EOX Sentinel-2 cloudless **2016** (CC BY 4.0) | edições 2018+ são CC BY-NC-SA — não usar sem licença comercial |
| Conteúdo | Supabase `oolwrsxdwnzofinvjael`: `capitulos`, `blocos`, `verbetes`, `destaques`, `rotulos` | RLS: leitura pública do publicado |
| Edge Functions | `ficha` (cauda sob demanda, cache em `destaques`), `pergunte` (IA, senha de teste → assinatura) | Supabase; chave Anthropic em Secrets |
| Índice de busca | R2: `busca-index.json?v=N` | subir `?v` a cada atualização (cache) |

## Versionar
O app é publicado direto no R2 (dashboard ou `npm run deploy:web`). Para o repositório acompanhar, basta subir o número em `VERSION` —
a GitHub Action baixa o `atlas.html` publicado e faz o commit de `www/index.html` com os bytes exatos que estão no ar.

## Publicar o site (R2)
```bash
npm run deploy:web      # rclone copyto www/index.html → atlas.html + sync www/lib
```
Sempre conferir por fetch que o marcador `<!-- vN -->` novo está no ar (cache de borda ~60 s).
Staging: `atlas-teste.html` no mesmo bucket.

## F4 · App nativo (Capacitor) — passo a passo no Mac

Pré-requisitos: Node 18+, Xcode 15+ (com simulador iOS), Android Studio (SDK 34+), conta Apple Developer e Google Play Console.

```bash
npm install
npm run libs                                 # clone novo: baixa MapLibre, PMTiles, fontes e glifos para www/lib (nada disso é versionado)
python3 scripts/make-assets.py               # clone novo: desenha assets/ (icon.png, splash.png, …) — pip install pillow
npx cap add ios
npx cap add android
npm run assets                               # deriva todos os tamanhos de ícone e splash a partir de assets/
npx cap sync
npx cap open ios                             # Xcode → Signing & Capabilities → Team; Product → Archive → TestFlight
npx cap open android                         # Android Studio → Build → Generate Signed Bundle (AAB) → Play Console (teste interno)
```

### Nativo dentro do HTML (v36)
Tudo em `atlas.html` sob `NATIVO` e protegido por `window.Capacitor` (no navegador não roda):
- **Lembrete diário** (`@capacitor/local-notifications`): oferecido uma vez ao terminar o desafio de hoje; agenda 9h locais; reagendado a cada abertura; tocar abre `#jogo`.
- **Story** (`@capacitor/share` + `@capacitor/filesystem`): o cartão PNG vai para o cache e sai pela folha do sistema (Instagram/WhatsApp).
- **Deep links** (`@capacitor/app` `appUrlOpen`): `https://atlasbrexplora.app/#jogo` abre a rota no app. Precisa de `www/.well-known/apple-app-site-association` (TEAMID) e `assetlinks.json` (SHA-256 do keystore) publicados no R2 com `Content-Type: application/json`, mais *Associated Domains* `applinks:atlasbrexplora.app` no Xcode e, no `AndroidManifest.xml` (dentro da `<activity>` principal):
  ```xml
  <intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="atlasbrexplora.app" />
  </intent-filter>
  ```
- **Atualização remota**: a cada abertura o app lê `VERSION.json` no R2; se for maior que a versão embutida, baixa o `atlas.html` novo para a área de dados (lib/ passa a vir do R2) e aponta o WebView para lá (`WebView.setServerBasePath` + `persistServerBasePath`). O pacote da loja fica como reserva. **Ao publicar no R2, atualizar também `VERSION.json`** (`npm run version:json` gera `www/VERSION.json` a partir de `VERSION`; subir junto).

Checklist antes de enviar às lojas (textos, capturas e respostas de privacidade prontos em `docs/lojas/`):
- [ ] `capacitor.config.ts`: `appId` `com.brexplora.atlas` (não mudar depois de publicado).
- [ ] iOS `Info.plist`: `NSAppTransportSecurity` não precisa de exceções (tudo HTTPS). Orientação: retrato.
- [ ] Android `AndroidManifest.xml`: permissão `INTERNET` (o Capacitor já inclui). `android:screenOrientation="portrait"`.
- [ ] Testar: sem rede na primeira abertura → tela "Sem conexão" com botão; botão voltar do Android navega pelo histórico e fecha na raiz.
- [ ] Política de privacidade (URL pública) — as lojas exigem. O app não coleta dados pessoais; a IA envia só o texto da pergunta ao Supabase/Anthropic.
- [ ] Capturas de tela: iPhone 6,7"/6,5" e iPad 12,9" (Apple); telefone + tablet 7" e 10" (Google).
- [ ] Texto da loja (PT-BR): nome, subtítulo (30 car.), descrição, palavras-chave, categoria Educação/Referência.
- [ ] Assinaturas (F6): produto `pro_anual` / `pro_mensal` no App Store Connect e no Play Console antes de ligar o paywall.

## Editar conteúdo
Supabase Studio → Table Editor (`blocos`, `verbetes`, `destaques`) ou via MCP no Claude. Cada bloco de cena tem
`map_state` = `{center, zoom, camadas[], filtro?, marcadores[], focos[]}`. **`focos`** acende elementos nomeados
(mesmo contrato da IA): `{camada, campo, valor}` com o valor EXATO da camada (ex.: `rios_nomeados/NORIOCOMP/"Rio Verruga"`).

## Tiles: regra de ouro
Cada camada tem um `minzoom` no tileset (ver `vector_layers` no header do PMTiles). Tudo que um capítulo enquadra
abaixo do zoom 4 precisa existir em `atlas-overview.pmtiles` — `tiles-tools/extrair-overview.py` + tippecanoe geram.

## Licenças
MapLibre GL (BSD-3) · PMTiles (BSD-3) · Noto Sans (OFL, `www/lib/LICENSE-NotoSans.md`) · Instrument Serif/Sans (OFL) ·
IBM Plex Mono (OFL) · Sentinel-2 cloudless 2016 by EOX IT Services GmbH (CC BY 4.0, contém dados Copernicus Sentinel modificados) ·
Terrain Tiles: Mapzen/AWS Open Data. Dados públicos brasileiros conforme cada fonte.

## Histórico
`docs/diario-de-bordo.md` (sessões, decisões, lições) e `docs/handoff.md` (visão do produto e fases).

## Painel do editor e backup do conteúdo (v39)
- `www/painel.html` → https://atlasbrexplora.app/painel.html — uso real (pessoas/dia, jogadas, rotas, buscas, fichas, versões, erros nos aparelhos). Privado por chave: a RPC `painel(chave, dias)` só responde com a chave guardada na tabela `config` (a chave está no diário de bordo, não neste repositório). Abrir uma vez com `#chave=…` e o navegador guarda.
- `eventos` recebe também `tipo = 'erro'` (erros de JS no aparelho, no máximo 5 por sessão) — aparecem no painel.
- `jogadas` tem restrições de integridade (tipo, 1–6 tentativas, pontos coerentes com o acerto, dia dentro dos 31 dias do arquivo).
- Action `backup-conteudo` (diária, 5h UTC): baixa capítulos, blocos, verbetes, destaques, rótulos e desafios publicados com a chave anônima para `conteudo/*.json` e commita se mudou. **Pendente de instalação**: a integração do Claude não pode gravar em `.github/workflows/`; os dois arquivos (este e o `espelhar-r2` atualizado, que passa a copiar também painel/privacidade/índice/VERSION.json) estão em `scripts/workflows-pendentes/` — mover para `.github/workflows/` e commitar.
