#!/usr/bin/env python3
"""
Gera a imagética do site sem depender de rede.
Produz: texturas de lâmina de madeira + elevações ortográficas dos ambientes.
Paleta e materiais seguem SPEC-VISUAL.md.
"""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20260827)

# ── paleta canônica ────────────────────────────────────────────────
BREU     = (13, 9, 6)
CASCA    = (23, 16, 11)
SERRAGEM = (241, 229, 210)
BRASA    = (200, 118, 58)

MADEIRAS = {
    # nome        claro            escuro           veio
    "freijo":   ((198, 142, 82),  (120, 74, 36),   0.55),
    "imbuia":   ((112, 66, 36),   (46, 26, 14),    0.75),
    "carvalho": ((176, 137, 92),  (104, 76, 46),   0.45),
    "nogueira": ((132, 88, 54),   (58, 35, 20),    0.65),
    "laca":     ((238, 230, 216), (198, 188, 172), 0.10),
}


def ruido(h, w, escala, oitavas=4):
    """Ruído fractal por upsample bilinear — sem dependências extras."""
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(oitavas):
        gh = max(2, int(h / (escala / (2 ** o))))
        gw = max(2, int(w / (escala / (2 ** o))))
        g = rng.random((gh, gw)).astype(np.float32)
        img = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
        acc += img * amp
        tot += amp
        amp *= 0.5
    return acc / tot


def lamina(w, h, especie, vertical=False):
    """Textura de lâmina de madeira: veio longo + poros + raios medulares."""
    claro, escuro, forca = MADEIRAS[especie]
    H, W = (w, h) if vertical else (h, w)

    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, W, dtype=np.float32)[None, :]

    # ondulação do veio: bandas largas, irregulares, com cathedral no centro
    desvio = (ruido(H, W, 300, 4) - 0.5)
    largura = 5.5 + rng.random() * 3.0
    cath = np.abs(x - (0.30 + rng.random() * 0.40)) * 2.2
    linhas = y * largura + desvio * 3.4 + cath * 1.5 + np.sin(x * 2.3 + rng.random() * 6) * 0.5
    veio = np.abs(np.sin(linhas * math.pi))
    veio = veio ** (0.35 + forca * 0.8)

    # poros finos e granulação longitudinal
    poros = ruido(H, W, 5, 3)
    fibra = np.array(Image.fromarray(
        (rng.random((H, max(3, W // 90))) * 255).astype(np.uint8)
    ).resize((W, H), Image.BILINEAR), np.float32) / 255

    m = 0.52 * veio + 0.22 * poros + 0.26 * fibra
    m = np.clip((m - m.min()) / (np.ptp(m) + 1e-6), 0, 1)
    m = m * forca + (1 - forca) * 0.5

    c1 = np.array(escuro, np.float32)
    c2 = np.array(claro, np.float32)
    rgb = c1[None, None, :] + (c2 - c1)[None, None, :] * m[:, :, None]

    # luz rasante do alto-esquerda
    gy = np.linspace(1.12, 0.72, H, dtype=np.float32)[:, None]
    gx = np.linspace(1.10, 0.80, W, dtype=np.float32)[None, :]
    rgb *= (gy * gx)[:, :, None]

    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if vertical:
        img = img.transpose(Image.ROTATE_90)
    return img.resize((w, h), Image.LANCZOS)


def vinheta(img, forca=0.42):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx / w - .5) / .5) ** 2 + ((yy / h - .5) / .62) ** 2)
    k = np.clip(1 - forca * np.clip(d - .35, 0, None) ** 1.5 * 1.9, 0, 1)
    a = np.array(img, np.float32) * k[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def grao(img, q=5.0):
    a = np.array(img, np.float32)
    a += rng.normal(0, q, a.shape).astype(np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# ── cena: elevação ortográfica de um ambiente ──────────────────────
W, H = 1600, 900


def cena(nome, modulos, piso=0.80, luz=(0.24, 0.06), acento=None):
    """
    modulos: lista de dicts {x,y,w,h, esp, puxador, led, vidro}
             coordenadas normalizadas (0-1) sobre a tela.
    """
    base = Image.new("RGB", (W, H), BREU)

    # parede com luz rasante do alto-esquerda
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = luz[0] * W, luz[1] * H
    d = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / (W * 0.95)
    luzq = np.clip(1.22 - d * 1.02, 0.17, 1.0) ** 1.35
    parede = np.zeros((H, W, 3), np.float32)
    parede += np.array(CASCA, np.float32)[None, None, :] * (0.55 + luzq[:, :, None] * 1.5)
    parede = np.clip(parede, 0, 255)
    base = Image.fromarray(parede.astype(np.uint8))

    # piso — porcelanato cimento queimado com reflexo
    py = int(H * piso)
    chao = Image.new("RGB", (W, H - py), (26, 21, 17))
    ca = np.array(chao, np.float32)
    g = np.linspace(1.35, 0.35, H - py, dtype=np.float32)[:, None, None]
    ca *= g
    ca += (ruido(H - py, W, 60, 3)[:, :, None] - .5) * 14
    base.paste(Image.fromarray(np.clip(ca, 0, 255).astype(np.uint8)), (0, py))

    d0 = ImageDraw.Draw(base)
    d0.line([(0, py), (W, py)], fill=(58, 44, 33), width=2)

    # módulos, do fundo para a frente
    brilhos = []
    for m in modulos:
        x, y = int(m["x"] * W), int(m["y"] * H)
        w, h = int(m["w"] * W), int(m["h"] * H)
        if w < 2 or h < 2:
            continue
        esp = m.get("esp", "freijo")
        tex = lamina(w, h, esp, vertical=m.get("vert", False))

        if m.get("vidro"):
            a = np.array(tex, np.float32) * 0.42 + np.array([70, 96, 104], np.float32) * 0.25
            tex = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

        # sombreamento do módulo conforme distância da luz
        cx, cy = x + w / 2, y + h / 2
        dd = math.hypot(cx - lx, cy - ly) / (W * 0.9)
        k = max(0.50, 1.24 - dd * 0.78)
        a = np.array(tex, np.float32) * k
        # gradiente interno (topo mais claro)
        a *= np.linspace(1.10, 0.86, h, dtype=np.float32)[:, None, None]
        tex = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

        # sombra projetada
        som = Image.new("RGB", (w + 26, h + 26), (0, 0, 0))
        base.paste(Image.blend(base.crop((x - 13, y - 13, x + w + 13, y + h + 13)), som, 0.55),
                   (x - 13, y - 13))
        base.paste(tex, (x, y))

        dm = ImageDraw.Draw(base)
        dm.rectangle([x, y, x + w - 1, y + h - 1], outline=(18, 13, 9), width=2)
        dm.line([(x + 1, y + 1), (x + w - 2, y + 1)], fill=(232, 200, 158), width=1)

        # puxador cava preto fosco
        p = m.get("puxador")
        if p == "h":
            hw = int(w * 0.46)
            dm.rounded_rectangle([x + (w - hw) // 2, y + int(h * .07),
                                  x + (w + hw) // 2, y + int(h * .07) + 7],
                                 radius=3, fill=(16, 14, 13))
        elif p == "v":
            hh = int(h * 0.34)
            dm.rounded_rectangle([x + int(w * .86), y + (h - hh) // 2,
                                  x + int(w * .86) + 7, y + (h + hh) // 2],
                                 radius=3, fill=(16, 14, 13))

        if m.get("led"):
            brilhos.append((x, y + h, w))

    # fita de LED quente por baixo das prateleiras
    if brilhos:
        gl = Image.new("RGB", (W, H), (0, 0, 0))
        dg = ImageDraw.Draw(gl)
        for x, yb, w in brilhos:
            dg.rectangle([x + 6, yb - 3, x + w - 6, yb + 2], fill=(255, 196, 122))
        gl = gl.filter(ImageFilter.GaussianBlur(26))
        base = Image.fromarray(np.clip(np.array(base, np.float32)
                                       + np.array(gl, np.float32) * 1.25, 0, 255).astype(np.uint8))

    # acento têxtil discreto (verde-musgo OU terracota, nunca os dois)
    if acento:
        ov = Image.new("RGB", (W, H), (0, 0, 0))
        do = ImageDraw.Draw(ov)
        ax, ay, aw, ah = acento[1]
        do.rectangle([int(ax * W), int(ay * H), int((ax + aw) * W), int((ay + ah) * H)],
                     fill=acento[0])
        ov = ov.filter(ImageFilter.GaussianBlur(9))
        base = Image.fromarray(np.clip(np.array(base, np.float32)
                                       + np.array(ov, np.float32) * 0.55, 0, 255).astype(np.uint8))

    base = grao(vinheta(base), 4.2)
    p = os.path.join(OUT, nome + ".jpg")
    base.save(p, quality=88, optimize=True, progressive=True)

    sm = base.resize((640, 360), Image.LANCZOS)
    sm.save(os.path.join(OUT, nome + "-sm.jpg"), quality=82, optimize=True, progressive=True)
    print("  ", nome + ".jpg", os.path.getsize(p) // 1024, "KB")


MUSGO, TERRACOTA = (62, 74, 58), (156, 83, 52)


def faixa(x0, x1, y, h, n, esp, puxador="h", **kw):
    """n módulos iguais lado a lado entre x0 e x1, com frestas de 4px."""
    g = 0.0035
    w = (x1 - x0 - g * (n - 1)) / n
    return [dict(x=x0 + i * (w + g), y=y, w=w, h=h, esp=esp, puxador=puxador, **kw)
            for i in range(n)]


AMBIENTES = {
    "cozinha": (
        faixa(.06, .52, .17, .25, 3, "freijo", "h", led=True)
        + faixa(.55, .74, .17, .25, 2, "laca", "h", led=True)
        + [dict(x=.06, y=.545, w=.68, h=.022, esp="laca")]                 # bancada quartzo
        + faixa(.06, .40, .567, .233, 3, "imbuia", "h")
        + faixa(.43, .74, .567, .233, 2, "freijo", "h")
        + [dict(x=.775, y=.17, w=.165, h=.63, esp="imbuia", puxador="v", vert=True)],
        (MUSGO, (.10, .50, .13, .05)),
    ),
    "closet": (
        faixa(.07, .45, .16, .19, 3, "imbuia", None, led=True)
        + faixa(.07, .45, .365, .19, 3, "imbuia", None, led=True)
        + faixa(.07, .45, .57, .23, 4, "freijo", "h")
        + [dict(x=.48, y=.16, w=.20, h=.64, esp="freijo", puxador="v", vert=True)]
        + faixa(.70, .94, .16, .30, 2, "laca", "v")
        + faixa(.70, .94, .48, .32, 2, "imbuia", "h", led=True),
        (TERRACOTA, (.72, .30, .10, .06)),
    ),
    "painel-tv": (
        faixa(.05, .62, .12, .58, 16, "freijo", None)                       # ripado
        + [dict(x=.66, y=.30, w=.29, h=.018, esp="imbuia", led=True)]       # prateleira
        + [dict(x=.66, y=.50, w=.29, h=.018, esp="imbuia", led=True)]
        + faixa(.05, .95, .715, .085, 4, "imbuia", "h"),
        (MUSGO, (.68, .34, .09, .05)),
    ),
    "home-office": (
        faixa(.06, .58, .155, .155, 3, "laca", "h", led=True)
        + [dict(x=.06, y=.455, w=.52, h=.021, esp="imbuia")]                # tampo
        + faixa(.06, .34, .478, .27, 2, "freijo", "h")
        + [dict(x=.63, y=.135, w=.31, h=.665, esp="freijo", puxador="v", vert=True)],
        (TERRACOTA, (.10, .42, .10, .045)),
    ),
    "dormitorio": (
        [dict(x=.20, y=.30, w=.44, h=.30, esp="imbuia", led=True)]          # cabeceira
        + faixa(.05, .18, .46, .12, 1, "freijo", "h")
        + faixa(.66, .79, .46, .12, 1, "freijo", "h")
        + faixa(.82, .96, .12, .68, 2, "laca", "v"),
        (MUSGO, (.30, .62, .22, .07)),
    ),
    "banheiro": (
        [dict(x=.14, y=.14, w=.34, h=.30, esp="laca", puxador="v", led=True)]
        + [dict(x=.52, y=.14, w=.30, h=.30, esp="imbuia", puxador="v", led=True)]
        + [dict(x=.14, y=.545, w=.68, h=.020, esp="laca")]
        + faixa(.14, .82, .567, .175, 3, "nogueira", "h"),
        (TERRACOTA, (.56, .49, .08, .04)),
    ),
    "gourmet": (
        faixa(.05, .40, .16, .26, 2, "carvalho", "h", led=True)
        + [dict(x=.44, y=.13, w=.28, h=.42, esp="imbuia")]                  # coifa/churrasqueira
        + faixa(.75, .95, .16, .26, 1, "carvalho", "h", led=True)
        + [dict(x=.05, y=.575, w=.90, h=.022, esp="laca")]
        + faixa(.05, .95, .597, .203, 5, "carvalho", "h"),
        (TERRACOTA, (.46, .58, .16, .05)),
    ),
}


def amostras():
    """Amostras verticais de lâmina — a seção 'nossos materiais'."""
    for esp in MADEIRAS:
        img = grao(vinheta(lamina(560, 780, esp, vertical=True), .38), 3.0)
        p = os.path.join(OUT, f"mat-{esp}.jpg")
        img.save(p, quality=88, optimize=True, progressive=True)
        print("   mat-%s.jpg" % esp, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    print("Ambientes:")
    for nome, (mods, ac) in AMBIENTES.items():
        cena(nome, mods, acento=ac)
    print("Materiais:")
    amostras()
    print("pronto ->", os.path.abspath(OUT))
