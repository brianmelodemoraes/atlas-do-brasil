# Atlas do Brasil · by Brexplora

Atlas geográfico narrativo, nascido mobile: 14 capítulos com *scrollytelling* cartográfico, Atlas Livre com 43 camadas
(IBGE · ANA · DNIT · ANEEL · ICMBio · FUNAI · INCRA · CPRM · Embrapa), fichas curadas + geradas sob demanda, busca de
34 mil lugares e o módulo **Pergunte ao Atlas** (IA, Pro).

## Arquitetura (o que roda onde)

| Peça | Onde | Observação |
|---|---|---|
| App (HTML único) | `www/index.html` → publicado como `atlas.html` no R2 | mesmo arquivo no site e dentro do app nativo |
| Bibliotecas, fontes, glifos | `www/lib/` (auto-hospedado) | **zero CDN** em produção; `npm run libs` reconstrói |
| Tiles vetoriais | R2: `atlas-base.pmtiles` (449 MB), `atlas-detail.pmtiles` (926 MB), `atlas-overview.pmtiles` (4,0 MB, z0–6 infra + rios ≥120 km) | Cloudflare R2, bucket `atlas-brexplora` |
| Relevo | AWS Terrain Tiles (Mapzen, terrarium) | público |
| Satélite | EOX Sentinel-2 cloudless **2016** (CC BY 4.0) | edições 2018+ são CC BY-NC-SA — não usar sem licença comercial |
| Conteúdo | Supabase `oolwrsxdwnzofinvjael`: `capitulos`, `blocos`, `verbetes`, `destaques`, `rotulos` | RLS: leitura pública do publicado |
| Edge Functions | `ficha` (cauda sob demanda, cache em `destaques`), `pergunte` (IA, senha de teste → assinatura) | Supabase; chave Anthropic em Secrets |
| Índice de busca | R2: `busca-index.json?v=N` | subir `?v` a cada atualização (cache) |

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

Checklist antes de enviar às lojas:
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
