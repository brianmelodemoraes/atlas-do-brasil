# Ficha das lojas — Atlas do Brasil · by Brexplora

Textos prontos para colar no App Store Connect e no Google Play Console. Limites de caracteres respeitados.

## Identidade
| Campo | Valor |
|---|---|
| Nome (30) | **Atlas do Brasil** |
| Subtítulo iOS (30) | **Geografia que se move** |
| Descrição curta Android (80) | **Um atlas que se move enquanto você lê — 16 capítulos, 43 camadas, um enigma por dia.** |
| Bundle / package | `com.brexplora.atlas` |
| Categoria | Primária: **Educação** · Secundária: **Referência** (iOS) / **Educação** (Android) |
| Classificação etária | iOS **4+** · Android **Livre (L)** — sem violência, sem compras (por ora), sem conteúdo gerado por usuários visível |
| Preço | Grátis |
| Idioma | Português (Brasil) |
| Site | https://atlasbrexplora.app |
| Suporte | https://atlasbrexplora.app/#sobre · brianmelodemoraes@gmail.com |
| Política de privacidade | https://atlasbrexplora.app/privacidade.html |
| Copyright | © 2026 Brexplora |

## Palavras-chave (iOS, 100 caracteres, separadas por vírgula, sem espaço)
`atlas,mapa,geografia,brasil,rios,biomas,relevo,municípios,enem,vestibular,quiz,ibge,educação,estados`

## Descrição (iOS 4000 / Android 4000)

Um atlas que se move enquanto você lê.

O Atlas do Brasil é uma enciclopédia geográfica ilustrada feita para o celular: o mapa acompanha cada parágrafo, voa para o lugar de que o texto fala, acende rios, biomas, serras e cidades no momento certo. Dezesseis capítulos — dos Rios do Brasil ao Sertão, das Montanhas ao Litoral — escritos como reportagem, com números, comparações e verbetes.

ATLAS LIVRE
Quarenta e três camadas oficiais para ligar e cruzar: rios e bacias, biomas, relevo, clima, solos, geologia e aquíferos; municípios, bairros e regiões metropolitanas; rodovias, ferrovias, hidrovias, portos e aeroportos; usinas e linhas de transmissão; terras indígenas, unidades de conservação e quilombos; Amazônia Legal, semiárido, fusos horários e a Amazônia Azul. Bases papel, noturna, satélite e híbrida. Expedições prontas num toque. Toque em qualquer lugar do mapa e abra a ficha: 34 mil lugares pesquisáveis, com textos curados para os mais importantes.

DESAFIO DO DIA
Um enigma geográfico novo todos os dias, em rodízio: reconheça um município pela silhueta, ache uma cidade no mapa, descubra que rio é aquele pelo traçado. Seis tentativas, distância e direção a cada palpite, dicas que se abrem uma a uma, ranking do dia, sequência de acertos e um cartão pronto para o Story. Jogue também os desafios anteriores.

FEITO COM DADOS PÚBLICOS
IBGE, ANA, DNIT, ANEEL, ICMBio, FUNAI, INCRA, CPRM e Embrapa — tratados, simplificados e unidos pela Brexplora. Relevo Mapzen/AWS; satélite Sentinel-2 cloudless (EOX, CC BY 4.0).

SEM CADASTRO
Nada de conta, e-mail ou senha. O Desafio usa um identificador anônimo criado no seu aparelho.

Para estudantes, professores, viajantes e curiosos: o Brasil inteiro, camada por camada, na palma da mão.

## Novidades desta versão (iOS "What's New" / Android "Notas da versão")
Primeira versão nas lojas: 16 capítulos, Atlas Livre com 43 camadas, busca de 34 mil lugares e o Desafio do dia com lembrete diário.

## Texto promocional iOS (170)
Dezesseis capítulos em que o mapa acompanha o texto, 43 camadas oficiais e um enigma geográfico por dia. Sem cadastro.

## Capturas de tela
`docs/lojas/shots/` — sete telas por tamanho, já com moldura e legenda:
- `ios-6.7/` 1290×2796 (iPhone 15/16 Pro Max, obrigatório) · `ios-6.5/` 1242×2688 (iPhone 11 Pro Max, opcional)
- `android/` 1080×2340 (telefone). Feature graphic Android 1024×500: `docs/lojas/feature-graphic.png`
- iPad: opcional na primeira submissão (marcar o app como só iPhone em *Supported Destinations* se não houver capturas de iPad).
Regenerar com prints reais do iPhone: colocar os PNGs em uma pasta e rodar `python3 scripts/loja-shots.py <pasta>`.

## Privacidade — App Store Connect ("App Privacy")
Marcar **"Data Not Linked to You"** para:
- **Usage Data → Product Interaction** (eventos anônimos de uso: capítulo aberto, expedição, busca, ficha, jogo) — finalidade: *Analytics*; não vinculado à identidade; não usado para rastreamento.
- **Identifiers → Other Diagnostic/User ID?** Não: o UUID é gerado localmente e não identifica a pessoa. Se o revisor perguntar, descrever como "identificador aleatório não vinculado".
- Tudo o mais: **não coletado**. Localização: não. Contatos: não. Compras: não. Rastreamento (ATT): **não** — não pedir permissão de rastreamento.

## Privacidade — Google Play ("Data safety")
- Coleta dados? **Sim** (mínimo). Compartilha com terceiros? **Não** (Supabase/Cloudflare são processadores).
- Tipo: **App activity → App interactions** (eventos anônimos) — obrigatório para o funcionamento? Não; finalidade: *Analytics*. Criptografado em trânsito: **Sim**. Usuário pode pedir exclusão: **Sim** (e-mail, com o identificador mostrado em *Sobre*).
- **App info and performance**: não. **Device or other IDs**: **Sim** — "identificador gerado pelo app" (UUID local), finalidade *App functionality* (ranking do Desafio) e *Analytics*.
- Localização, contatos, mensagens, fotos, arquivos: **não**.
- Política de segurança: dados em trânsito por HTTPS; nenhum dado pessoal em repouso.

## Permissões que o app pede
- **Notificações** (opcional, depois de terminar o primeiro desafio): lembrete diário às 9h. Texto da justificativa: "Para avisar quando o enigma do dia estiver disponível".
- Nenhuma outra: sem câmera, localização, contatos ou fotos. O compartilhar usa a folha do sistema (o app grava a imagem no cache próprio).

## Notas para o revisor (App Review Notes / Play "Instructions for reviewers")
O Atlas do Brasil é um atlas geográfico editorial. Não requer conta nem login. Para avaliar:
1. Índice → toque em "I · Os Rios do Brasil" e role: o mapa acompanha o texto. Nas pranchas, "Explorar este mapa" permite zoom e fichas.
2. "Atlas Livre" → toque em "Brasil das Águas" (expedições) e depois em qualquer rio ou cidade para abrir a ficha. Busca (lupa): digite "Bonito".
3. Índice → "Desafio do dia": um enigma por dia; use o autocomplete para responder. Ao terminar, o app oferece (opcional) um lembrete diário por notificação local.
Conteúdo e mapas são carregados de servidores próprios (Cloudflare/Supabase); o app precisa de internet. O módulo "Pergunte ao Atlas" (IA) fica desligado nesta versão.
Contato do desenvolvedor: brianmelodemoraes@gmail.com.

## Argumento para a diretriz 4.2 (Apple, "minimum functionality") — só se for questionado
O app não é um site empacotado: tem lembretes diários por notificação local, compartilhamento nativo de imagem (Story), navegação por deep link, atualização de conteúdo sem passar pela loja, botão voltar nativo no Android, e conteúdo editorial próprio (16 capítulos, 550+ fichas curadas) com um jogo diário. A versão web existe como porta de entrada; a experiência principal é o app.
