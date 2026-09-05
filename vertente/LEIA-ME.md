# VERTENTE — site de exemplo

Site de teste gerado com o `PROMPT-MESTRE.md` v2.0 (ver `../prompt/`).
Estabelecimento fictício: **ateliê de perfumaria de autor em Goiânia (GO)**,
que destila botânicas do Cerrado — pequi, baru, copaíba, buriti, angico,
barbatimão. Pequeno negócio, não-restaurante, com um objeto físico fotogênico
(o frasco) para sustentar o vídeo 3D e a peça de produto interativa.

## Como abrir

Abra `index.html` no navegador. Não há build, não há `npm install`,
não há dependência externa além das fontes do Google Fonts.

## O que tem dentro

| Seção | Efeito |
|---|---|
| Hero | Vídeo Higgsfield 1080p / 15s reenquadrado pelo scroll (máscara + escala), sem texto no vídeo |
| Hero + rodapé | **TextPressure** — letras respondem à proximidade do cursor via eixos de fonte variável |
| §02 Portal | **Portal Animation (scrollable)** — abertura circular dirigida 100% pelo scroll, três camadas de profundidade, borda com material |
| §03 Produto | **3D Product Animation** — turntable em vídeo, arrastável com o cursor, com nudge por scroll e hotspots ancorados no ângulo |
| §04 Bancada | **Object Reveal on Hover** — lente amortecida revela o flat-lay por baixo; varredura automática quando ninguém está com o cursor lá (e no toque) |
| §04 Espécimes | Segunda variação do reveal: o recorte da matéria-prima segue o cursor |
| §05 Processo | Scroll horizontal dirigido pelo scroll vertical, com glifos SVG desenhados para este negócio |
| §07 Campo | Campo de pontos em canvas com bojo no cursor |
| §08 Encomenda | Input curvado em `textPath` (CurvedInput), com validação real |
| Global | Scroll suave com damping exponencial, cursor de duas latências, grão SVG |

## Onde mexer

- **Cores e tipografia**: bloco `:root` no primeiro `<style>`. São 8 cores e
  3 famílias + 1 variável de propósito único (a do TextPressure).
- **Mídia**: objeto `ASSETS` no início do `<script>`.
- **Peso do scroll**: constante `7.2` na chamada `damp(SS.current, SS.target, 7.2, dt)`.
  Menor = mais pesado e lento; maior = mais seco.

## Mídia

O vídeo e as imagens estão referenciados pela URL do CDN da geração. Para
deixar o arquivo 100% offline, baixe os quatro arquivos e troque as URLs do
objeto `ASSETS` por caminhos em `assets/`:

```
assets/hero.mp4       ← ASSETS.heroVideo
assets/hero.png       ← ASSETS.heroPoster
assets/frasco.mp4     ← ASSETS.prodVideo
assets/frasco.png     ← ASSETS.prodPoster
assets/bancada.png    ← ASSETS.bench
```

Se a mídia não carregar, o site continua legível: cada vídeo tem `poster`,
cada superfície tem cor de token por baixo e nenhuma seção depende da imagem
para fazer sentido.

## Créditos Higgsfield gastos

56 de 60 — 3 imagens (`nano_banana_pro`, 2 cada) + hero 15 s 1080p (30) +
turntable 10 s 1080p (20). A MCP do nano banana estava sem créditos, o que
liberou o uso do Higgsfield conforme a regra do prompt.
