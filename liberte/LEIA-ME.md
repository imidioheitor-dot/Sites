# Liberté Dance Studio — site

Arquivo único: **`index.html`**. Sem build, sem npm, sem dependências externas.
Nenhuma requisição sai para fora do domínio: fontes, CSS, JS e efeitos 3D estão
todos dentro da pasta.

```
liberte/
├── index.html                 ← o site inteiro
├── assets/
│   ├── fonts/                 ← Archivo (variável) + Cormorant Garamond, OFL-1.1
│   ├── img/                   ← 10 imagens  (hoje: PROVISÓRIAS — ver passo 1)
│   ├── video/hero.mp4         ← 15s · 1080p (hoje: AUSENTE — ver passo 1)
│   └── baixar-assets.sh       ← baixa as imagens e o vídeo definitivos
└── LEIA-ME.md
```

---

## 1. Primeiro passo, obrigatório: baixar os assets reais

As imagens que estão na pasta agora são **placeholders** da paleta da marca, com
a palavra `IMAGEM PROVISORIA` escrita nelas. As definitivas — 10 imagens e o vídeo
3D de 15s em 1080p — já foram geradas e estão hospedadas na sua conta Higgsfield.
Elas não puderam ser baixadas no ambiente do Claude porque o CDN
(`d8j0ntlcm91z4.cloudfront.net`) está fora da allowlist de rede daquela sessão.

Na sua máquina não há esse bloqueio. Rode uma vez:

```bash
bash assets/baixar-assets.sh
```

O script baixa tudo, converte PNG→JPG e coloca cada arquivo no nome certo.
Depois disso o site está completo — o vídeo do hero aparece e os placeholders
somem.

> Se preferir usar fotos reais do estúdio, é só substituir os arquivos em
> `assets/img/` mantendo os nomes. Os nomes usados são:
> `hero-3d, portal-tall, barra, jazz, contemporaneo, sapateado, urbanas,
> estudio, exame, bailarina`.

---

## 2. Publicar

Qualquer host estático serve. A pasta inteira é o site.

- **Netlify Drop** — arraste a pasta `liberte/` para app.netlify.com/drop.
- **Netlify contínuo** — aponte o *publish directory* para `liberte`.
  (O `netlify.toml` na raiz do repositório aponta para `site/`, que é outro
  projeto; não mexi nele para não quebrar aquele deploy.)

---

## 3. O que ainda depende de você

Estes pontos estão marcados no código como `PLACEHOLDER`:

| O quê | Onde | Situação |
|---|---|---|
| Grade de horários | `const TURMAS` no `<script>` | 21 turmas plausíveis inventadas. Substituir pela agenda oficial. |
| Valores dos planos | `const PLANOS` | Preços estão como `—`. O botão já leva ao WhatsApp perguntando o valor. |
| Nomes da equipe | `const EQUIPE` | Cargos genéricos. Trocar por nomes, funções e fotos reais. |
| Ano de fundação | markup do hero | Está "Desde 2016". Confirmar. |
| Registro RAD | rodapé | Se o estúdio for *Registered/Approved Dance Centre* da RAD, o número de registro pode virar credencial oficial no site. |

Os depoimentos também são fictícios e devem ser trocados por reais antes de ir ao ar.

---

## 4. Sobre o nome

O site é do **Liberté Dance Studio**. A *Royal Academy of Dance* aparece como
**metodologia e certificação** — que é o que ela é — e não como nome do
estabelecimento. A RAD é uma instituição britânica registrada; um site que se
apresentasse como sendo ela, com endereço em Ribeirão Preto e WhatsApp de
matrícula, induziria o visitante a erro. O rodapé traz a nota de atribuição.

---

## 5. Efeitos implementados

Todos escritos à mão, sem biblioteca:

| Efeito | Onde | Técnica |
|---|---|---|
| **TextPressure** | título do hero | Archivo variável (eixos `wght` 100–900 e `wdth` 62–125) reagindo à distância do cursor, letra a letra |
| **Splash Cursor** | hero | simulação de fluido em WebGL — advecção, vorticidade e solver de pressão em shaders, tingida na paleta vinho |
| **Object Reveal on Hover** | Modalidades | imagem que persegue o cursor com atraso e inclina conforme a velocidade |
| **Portal Animation** | seção "O outro lado" | máscara circular dirigida pelo scroll ao longo de 340vh, com anel e parallax |
| **3D Product Animation** | Sapatilha | malha gerada em tempo real: loft de seções superelípticas, casco oco com garganta em V, fitas em hélice, sombra de contato. Arrastar gira, roda aproxima, chips destacam partes |
| **Magic Bento** | "Por que aqui" | spotlight de proximidade, inclinação 3D, faíscas e ondulação no clique |
| **Dot Field** | seção RAD | malha de pontos em canvas que abaula sob o cursor |
| **Card Swap** | Galeria | pilha 3D com troca automática |
| **Curved Input** | newsletter | campo curvo em SVG com texto sobre `textPath` |
| **Marquee** | duas faixas | rolagem infinita, pausa no hover |
| **Cursor personalizado** | site todo | círculo com atraso + ponto sem atraso, cresce sobre elementos interativos |

Tudo tem caminho alternativo: `prefers-reduced-motion` desliga as animações,
telas de toque recebem versões estáticas ou por gesto, e a ausência de WebGL
degrada para imagem.

## 6. Conversão

O site inteiro converge para a **grade de horários** (o filtro por modalidade,
idade e dia) e para o WhatsApp. Nenhum formulário envia dados para servidor
nosso: o botão monta a mensagem — com turma, horário e idade já escritos — e
abre o WhatsApp do estúdio (16) 99207-8252.
