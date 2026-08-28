# Marcenaria JR — site

Arquivo único: **`index.html`**. Sem build, sem npm, sem CDN externo.
Arraste a pasta inteira para o Netlify e está no ar.

```
marcenaria-junior/
├── index.html                 ← o site inteiro (HTML + CSS + JS)
├── assets/
│   ├── archivo.woff2          fonte variável (wght 100–900, wdth 62–125)
│   ├── fraunces.woff2         fonte variável de display (opsz/wght/SOFT/WONK)
│   ├── js/three.min.js        Three.js 0.160 (armário 3D)
│   ├── video/hero.mp4         1920×1080 · 15,00s · 30fps · sem áudio
│   └── img/                   ambientes, materiais e poster
├── tools/                     geradores das imagens e do vídeo (Python)
├── SPEC-VISUAL.md             spec canônica da marca
└── LEIA-ME.md
```

## Dados do cliente já configurados

| | |
|---|---|
| WhatsApp | +55 16 99348-2301 (`5516993482301`) |
| Instagram | @marcenariajr_rp |
| Endereço | Rua Itapetinga, 1422 — Sumarezinho, Ribeirão Preto/SP |
| CEP | 14050-355 |

Para trocar o telefone, procure `const FONE` no `<script>`.

## O que o site faz

- **Hero escrolável com vídeo** 1080p/15s com painéis de lâmina em profundidade
  e serragem na luz. Sem texto embutido no vídeo.
- **TextPressure** — "MARCENARIA JR" reage ao cursor pelos eixos `wght` e `wdth`
  da fonte variável. O tamanho é medido no extremo dos eixos, então nunca estoura.
- **Corredor em perspectiva** — os projetos vêm da profundidade em direção a quem
  olha, conduzidos pela rolagem, com paralaxe do cursor.
- **Object reveal on hover** — passar o mouse num ambiente revela a imagem
  flutuando junto ao cursor, com inclinação pela velocidade do ponteiro.
- **Armário 3D interativo** (Three.js) — arrasta para girar, roda para aproximar,
  abre as portas, troca a lâmina. Tem fallback em imagem se não houver WebGL.
- **Portal escrolável** — as duas folhas da porta abrem com a rolagem e revelam
  o ambiente entregue.
- **Cursor customizado** com rótulo contextual, desligado no toque.
- **Prancheta de desenho** — o cliente rabisca o móvel no canvas e usa o desenho
  no orçamento.
- **Formulário → WhatsApp** — monta a mensagem completa e abre a conversa.

## Como o formulário funciona

O WhatsApp **não aceita anexo por link** (`wa.me` só transporta texto). Então:

1. O cliente preenche e, se quiser, anexa uma foto ou desenha na prancheta.
2. Ao enviar, a imagem é **baixada no aparelho dele** e a conversa abre com todo
   o texto preenchido.
3. Ele toca no clipe e escolhe o arquivo que acabou de salvar.

O aviso embaixo do botão explica isso para o cliente, e muda de texto depois do
envio dizendo o nome exato do arquivo salvo.

## Sobre as imagens e o vídeo

**São provisórios.** O CDN do Higgsfield e o Instagram estão bloqueados pela
política de rede desta sessão, então a imagética foi **gerada localmente** por
`tools/gerar-imagens.py` (elevações ortográficas dos ambientes + amostras de
lâmina, com veio catedral procedural) e `tools/gerar-video.py` (voo de câmera
com projeção perspectiva real).

Para trocar pelas fotos reais da marcenaria, basta substituir os arquivos
mantendo os nomes:

```
assets/img/cozinha.jpg      + cozinha-sm.jpg      (versão 640×360)
assets/img/closet.jpg       + closet-sm.jpg
assets/img/painel-tv.jpg    + painel-tv-sm.jpg
assets/img/home-office.jpg  + home-office-sm.jpg
assets/img/dormitorio.jpg   + dormitorio-sm.jpg
assets/img/banheiro.jpg     + banheiro-sm.jpg
assets/img/gourmet.jpg      + gourmet-sm.jpg
assets/img/mat-freijo.jpg   mat-imbuia · mat-carvalho · mat-nogueira · mat-laca
assets/video/hero.mp4       + assets/img/hero-poster.jpg
```

As `-sm` alimentam o corredor em perspectiva e o reveal no hover (arquivos leves).
Nenhuma linha de código precisa mudar.

## Regerar os assets

```bash
python3 tools/gerar-imagens.py     # ~5 s
python3 tools/gerar-video.py       # ~12 min, precisa de ffmpeg
```

## Testado

- Sem erros de JavaScript no console (desktop 1440×900 e iPhone 390×844).
- Sem rolagem horizontal em nenhuma das duas larguras.
- `prefers-reduced-motion` desliga as animações.
- Âncoras param abaixo do cabeçalho fixo (`scroll-margin-top`).
