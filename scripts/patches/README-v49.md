# v49 — Brexplora Night com vida

Fontes completas (`v49.py` + `skin49.css` + `home49.js`, mock `mock2/home.html`, probes 37/38) em `https://atlasbrexplora.app/trivia-src-v49.zip`.

Decisões do Brian (28/09): direção **Brexplora Night com vida** (escuro + verde da marca, com profundidade, brilho, volume, Brasil 3D como herói), **sem mascote**, **patentes de explorador** (Curioso → Viajante → Bandeirante → Cartógrafo → Cronista → Lenda do Atlas), **app de 5 abas** com o atlas dentro (Perfil e Meu Brasil).

1. **Abas** (`#abas`, `JOGO.abas(hash)`): Início (`#`), Modos (`#modos`), Meu Brasil (`#meu`), Ligas (`#jogo/ligas`), Perfil (`#perfil`). `#v-indice` tem quatro `section.aba`; a barra some ao jogar e nas vistas de mapa (`body.com-abas`).
2. **Home** (`cartaoIndice` reescrita): herói com `brexplora-marca.webp` extrudado por `drop-shadow` e órbitas, badges (🔥 sequência, xp, lugares), cartão de identidade (nome/UF, patente · nível, barra de XP do nível), calendário de 6 dias (`est.tr.imp`), `.play` com volume (“JOGAR O IMPOSTOR” → “DESAFIAR UM AMIGO”), links Rodada completa / Sem parar, placar do dia.
3. **XP/patentes** (`home49.js`): `est.xp` (+pontos de cada enigma em `trFimEnigma`; migração soma hist + imp + best), `NIVEL_XP(n) = 500·n(n+1)/2` (500, 1.500, 3.000, 5.000…), patentes em 0 / 1.000 / 5.000 / 15.000 / 40.000 / 100.000 xp. `cerimonia()` = overlay `#nivel-up` com confete 0,9 s depois do enigma.
4. **Meu Brasil**: `est.meu.m[cd] = uf` alimentado por `lugaresDe(p, e, ok)` (impostor/top10/conexões/vizinhos/ficha/bingo/grade/relâmpago); aba com `UF_MINI` (4 tons por quantidade: 1 / 4 / 10 / 25), contadores, últimos 12 lugares, **Ver no mapa** → `#atlas/meu` → `acenderMeu(true)`: camadas `meu-fill`/`meu-line` (source base / municipios, filtro `CD_MUN in [...]`), só estados+municípios visíveis, painel colapsado, `fitBounds` nos lugares.
5. **Modos**: grade 2 colunas com ícones SVG em tiles gradiente (`ICONES`, `.ic-*`), cartão largo da Rodada completa. Os mesmos ícones substituem os glifos `gl()` dentro do jogo.
6. **Perfil**: nome/UF (`est.nome`, `est.uf`), lista de patentes, atalhos (estatísticas, ligas, Atlas Livre, sobre) e o sumário dos capítulos (`#sumario` continua ali para `montarIndice`/`montarContinuar`).
7. **Skin** (`skin49.css`): fundo radial `#141B33→#070A12`, `.gcard`/`.cartucho` com gradiente + borda de luz + sombra, botões com borda inferior (branco `#A1A1AA`, verde `#157A3D`, escuro `#0B0F1E`) que afundam no `:active`, chips/opções com volume e acerto brilhando, logo no topo do jogo, modal de boas-vindas removido.
