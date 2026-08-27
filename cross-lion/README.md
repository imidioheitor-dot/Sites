# Cross Lion — site

Site de página única para a **Cross Lion**, centro de cross training em Ribeirão Preto/SP.
Tudo vive em `index.html`: sem build, sem dependências, sem framework.

```
cross-lion/
├── index.html          # o site inteiro (HTML + CSS + JS, ~60 KB)
├── baixar-assets.sh    # baixa vídeo/fotos e troca para caminhos locais
└── README.md
```

Para ver: abra `index.html` no navegador, ou `python3 -m http.server` na pasta.

## ⚠️ Confira antes de publicar

| Item | Situação |
|---|---|
| **Nome** | O estabelecimento no nº 1810 se chama **Cross Lion** (não "Cross Lyon"). Endereço e Instagram batem. Se o nome correto for outro, troque as 8 ocorrências de `Cross Lion`. |
| **WhatsApp** | O botão flutuante usa `5516000000000` — **placeholder**. Procure por `<!-- TROCAR` no HTML. |
| **Horários** | Texto genérico, marcado com `<!-- TROCAR`. Não achei a grade publicada. |
| **Valores** | Ficaram "sob consulta" de propósito — não achei tabela pública. |
| **Fotos** | Geradas por IA (Higgsfield Soul 2), sem rostos identificáveis. Substitua por fotos reais do box quando tiver. |

## Dados confirmados na web

- Endereço: **Av. Antônio e Helena Zerrener, 1810 — Sumarezinho, Ribeirão Preto/SP**
- Instagram: [@crosslionrp](https://www.instagram.com/crosslionrp/)
- Parceiro **Wellhub (Gympass)** e **TotalPass**
- Oferece **aula experimental gratuita**

## Mídia

O vídeo do hero (**1920×1080, 15,04 s, sem áudio e sem texto**) e as 11 fotos são servidos
pelo CDN do Higgsfield. Para hospedar tudo junto do site:

```bash
bash baixar-assets.sh
```

Isso baixa os arquivos para `assets/` e reescreve o `index.html` (guarda um `.bak`).

## Efeitos

| Efeito | Onde | Como |
|---|---|---|
| **Object Reveal on Hover** | `#revelacao` | painel de imagem segue o cursor com *lerp*; varredura âmbar na linha |
| **Portal Animation (scrollable)** | `#portal` | 8 anéis atravessam o eixo Z em `position:sticky` (340vh de curso) |
| **Animação 3D em perspectiva** | `#vitrine` | carrossel em anel; gira com o scroll e com arrasto |
| **Grade que se inclina** | `#perspectiva` | 35 placas com `rotateX/rotateY` por proximidade + deriva automática |
| **TextPressure** | hero | eixos `wght`/`wdth` da Roboto Flex reagem à distância do cursor |
| **Cursor + DotField** | global | anel com *lerp*, `mix-blend-mode:difference`; grade de pontos que estufa |
| **Bento spotlight** | `#metodo` | brilho de borda por proximidade, tilt 3D e ondulação no clique |

**Acessibilidade e performance:** tudo respeita `prefers-reduced-motion`; os efeitos de cursor
só ligam em `(hover:hover) and (pointer:fine)`; o vídeo pausa fora da tela; imagens em `lazy`.

## Verificação feita

Renderizado no Chromium (Playwright) em 1440×900 e 390×844:

- sem scroll horizontal nos dois tamanhos (`scrollWidth == clientWidth`)
- zero erros de JavaScript
- os quatro efeitos testados por interação real (hover, scroll, movimento de mouse)
