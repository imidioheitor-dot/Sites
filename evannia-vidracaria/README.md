# Evannia Vidraçaria — site

Página única (`index.html`), **sem dependências e sem build**. Abrir o arquivo no
navegador já funciona; publicar é só subir esta pasta.

---

## ⚠️ Passo obrigatório: colocar as mídias

O site foi construído em volta de um vídeo e 8 fotos **que já foram gerados**, mas a
sessão que montou o site teve o CDN de download bloqueado pela política de rede
(erro 403 no proxy), então os arquivos **não puderam ser salvos aqui**.

Rode `bash baixar-midias.sh` nesta pasta e ele baixa tudo com os nomes certos.
Se preferir fazer à mão, os links estão dentro do script — os destinos são:

| Salvar como | Conteúdo |
|---|---|
| `assets/video/hero.mp4` | Vídeo do topo — 15 s, 1080p, vidro em 3D, sem texto |
| `assets/img/box-banheiro.jpg` | Box de banheiro em temperado |
| `assets/img/espelho.jpg` | Espelho sob medida com bisotê |
| `assets/img/janela.jpg` | Janela de correr em alumínio |
| `assets/img/sacada.jpg` | Sacada com cortina de vidro |
| `assets/img/porta.jpg` | Porta de vidro temperado |
| `assets/img/macro-vidro.jpg` | Macro da borda do vidro (também é o *poster* do vídeo e a imagem de compartilhamento) |
| `assets/img/tampo.jpg` | Prateleira / tampo em vidro |
| `assets/img/oficina.jpg` | Oficina — usada na animação de portal |

As imagens saem em `.png`; podem ser renomeadas para `.jpg` sem problema, mas o
ideal é **converter para JPG ou WebP** (qualidade ~80) para o site ficar leve.

**Enquanto os arquivos não estiverem lá, o site não quebra**: cada bloco de imagem
vira uma "chapa de vidro" animada com a legenda da peça, de propósito.

---

## Editar os dados do negócio

Tudo que muda com frequência está num único bloco no topo do `index.html`,
marcado com `▼▼▼ PARA PUBLICAR, EDITE APENAS ESTE BLOCO ▼▼▼`:

```js
window.EVANNIA = {
  telefone: "(16) 98156-0904",
  whatsapp: "5516981560904",   // só dígitos: 55 + DDD + número
  endereco: "Rua Altino Arantes, 585",
  bairro:   "Boulevard",
  ...
};
```

Telefone, link do WhatsApp, endereço, link do mapa, horário, Instagram e e-mail
saem todos daí. Deixar `email` ou `instagram` como `""` esconde a linha.

> Confira o endereço antes de publicar — ele foi usado exatamente como enviado.

---

## Publicar

Qualquer hospedagem de site estático serve:

- **Netlify Drop** — arraste a pasta `evannia-vidracaria/` em app.netlify.com/drop.
- **Vercel / Cloudflare Pages / GitHub Pages** — apontar para esta pasta.
- **Hospedagem comum** — subir a pasta inteira por FTP.

---

## O que está implementado

| Recurso | Onde |
|---|---|
| **Hero rolável com vídeo** | topo, com parallax e *poster* de fallback |
| **TextPressure** | "EVANNIA" reage ao cursor pelos eixos `wght`/`wdth` do Roboto Flex |
| **Portal Animation (scroll)** | seção "A origem" — a abertura cresce e revela o texto de dentro |
| **Object Reveal on Hover** | lista de serviços — a foto da peça segue o cursor |
| **3D Product Animation** | box de canto em CSS 3D: arrasta para girar, abre a porta, troca o vidro, monta-se ao entrar na tela |
| **Efeito de cursor** | lente de vidro que refrata o conteúdo + rótulo contextual |
| **DotField** | malha de pontos que abre espaço para o cursor |
| **Parallax na galeria** | fotos deslizam em ritmos diferentes |
| **Formulário → WhatsApp** | monta a mensagem pronta e abre o `wa.me` |
| **Menu mobile** | painel de vidro em tela cheia |

### Decisões técnicas

- **Zero dependências.** Sem React, sem GSAP, sem Three.js — os efeitos do
  React Bits foram portados para JS puro. O único recurso externo é a fonte
  (Google Fonts), com fallback de sistema.
- **O 3D é CSS 3D, não WebGL.** Vidro plano é literalmente um plano: `preserve-3d`
  entrega o mesmo resultado com uma fração do custo, roda em celular fraco e não
  precisa de biblioteca.
- **`prefers-reduced-motion` é respeitado** em tudo: o vídeo nem carrega, o portal
  já abre aberto e as animações são desligadas.
- **Mobile:** sem overflow horizontal de 360 px a 1920 px; efeitos de cursor
  desligados no toque; `DotField` com menos pontos.

---

## Testes já feitos

Rodados em Chromium (Playwright) antes da entrega:

- Ajuste do "EVANNIA" e overflow horizontal em 7 larguras (360 → 1920): tudo cabe.
- Portal: nenhum ponto do scroll fica sem texto legível.
- Formulário: validação de vazio, máscara de telefone e URL final do `wa.me`.
- `prefers-reduced-motion`: nada some, nada anima, zero erro de JS.
- Acessibilidade: 1 `<h1>`, todo `img` com `alt`, todo campo com `label`,
  todo botão com nome acessível.
