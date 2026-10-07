# Landing na raiz (`inicio.html`)

`https://atlasbrexplora.app/` → Redirect Rule da Cloudflare (302, "Raiz abre a landing") → `/inicio.html` (07/10/2026; antes apontava para `/atlas.html`).

- Página estática no R2 (bucket `atlas-brexplora`), visual "Brexplora Night" (mesmos tokens do app v49): herói com a marca, CTA `JOGAR O IMPOSTOR DE HOJE` → `/atlas.html#jogo`, "Abrir o atlas" → `/atlas.html#atlas`, seções Como funciona · Dez modos · Meu Brasil · Um atlas de verdade (5.570 · 36 · 16 · 34 mil) · Trivia Pro (R$ 9,90 / 49,90, "em breve nas lojas") · fecho · rodapé (Sobre, Privacidade, Termos, Contato).
- **Links antigos com `#…` continuam funcionando**: o primeiro `<script>` do `<head>` faz `location.replace('/atlas.html' + location.hash)` quando há hash (desafios `#d/…`, notificações `#jogo`, `#atlas`…). O fragmento sobrevive ao 302 porque o Location da regra não tem fragmento.
- Imagens `inicio-*.webp` (540×960, ~25 KB cada) recortadas dos quadros dos ads (`local/ads/out/...`); fontes em `lib/` (as mesmas do app); `brexplora-marca.webp`, `brexplora-logo.webp`, `og-card.png` já existiam no R2.
- Quando as lojas abrirem: trocar os três "Em breve · App Store · Google Play" por selos com link (herói, fecho e Pro).
- Fonte: `www/inicio.html` neste repo (as imagens só no R2).
