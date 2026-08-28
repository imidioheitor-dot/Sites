#!/usr/bin/env python3
"""
Vídeo hero: 1920x1080, 15s, 30fps, sem áudio e SEM TEXTO.
Voo de câmera por um corredor de painéis de lâmina de madeira suspensos,
com serragem em suspensão pegando a luz quente. Projeção perspectiva real.
Loop perfeito: a câmera percorre exatamente um período do padrão.
"""
import os, sys, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from importlib import import_module
G = import_module("gerar-imagens")

W, H, FPS, SEGS = 1920, 1080, 30, 15
NF = FPS * SEGS
FOV = 1.05
CX, CY = W / 2, H * 0.52
F = (W / 2) / math.tan(FOV / 2)

P, SPACING = 12, 3.2          # período do padrão
PERIODO = P * SPACING          # distância de um loop completo
rng = np.random.default_rng(7)

ESPECIES = ["freijo", "imbuia", "carvalho", "nogueira", "freijo", "imbuia"]

# ── painéis: um padrão que se repete a cada PERIODO em z ───────────
paineis = []
for i in range(P):
    lado = -1 if i % 2 == 0 else 1
    pw = 1.5 + rng.random() * 1.0
    ph = 2.0 + rng.random() * 1.4
    paineis.append(dict(
        z0=i * SPACING,
        x=lado * (1.5 + rng.random() * 1.1),
        y=(rng.random() - 0.5) * 1.2,
        w=pw, h=ph,
        esp=ESPECIES[i % len(ESPECIES)],
        giro=(rng.random() - .5) * 0.16,
    ))

print("pré-renderizando lâminas…")
TEX = {}
for p in paineis:
    key = (p["esp"], round(p["w"], 2), round(p["h"], 2))
    if key not in TEX:
        t = G.lamina(420, int(420 * p["h"] / p["w"]), p["esp"])
        a = np.array(t, np.float32)
        a *= np.linspace(1.18, 0.70, a.shape[0], dtype=np.float32)[:, None, None]
        a *= np.linspace(1.12, 0.72, a.shape[1], dtype=np.float32)[None, :, None]
        TEX[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    p["tex"] = TEX[key]

# ── serragem em suspensão ──────────────────────────────────────────
NM = 900
motes = np.stack([
    (rng.random(NM) - .5) * 11.0,
    (rng.random(NM) - .5) * 6.5,
    rng.random(NM) * PERIODO,
], 1).astype(np.float32)
mfase = rng.random(NM).astype(np.float32) * math.tau
mvel = (0.25 + rng.random(NM) * 0.5).astype(np.float32)

# fundo: parede quente com queda de luz
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
dl = np.sqrt(((xx - W * .26) / W) ** 2 + ((yy - H * .16) / W) ** 2)
FUNDO = np.clip(np.array(G.CASCA, np.float32)[None, None, :]
                * (0.34 + np.clip(1.15 - dl * 2.5, 0, 1)[:, :, None] * 1.85), 0, 255)

# vinheta reutilizável
dv = np.sqrt(((xx / W - .5) / .5) ** 2 + ((yy / H - .5) / .6) ** 2)
VIN = np.clip(1 - 0.5 * np.clip(dv - .34, 0, None) ** 1.4 * 1.85, 0, 1)[:, :, None]


def frame(k):
    t = k / NF
    camz = t * PERIODO
    # respiração lateral suave da câmera (período inteiro -> loopa)
    camx = math.sin(t * math.tau) * 0.30
    camy = math.cos(t * math.tau) * 0.16

    img = Image.fromarray(FUNDO.astype(np.uint8))

    # painéis: do mais distante para o mais próximo
    vis = []
    for p in paineis:
        z = (p["z0"] - camz) % PERIODO
        if z < 0.45 or z > PERIODO * 0.92:
            continue
        vis.append((z, p))
    vis.sort(key=lambda a: -a[0])

    for z, p in vis:
        s = F / z
        pw = max(2, int(p["w"] * s))
        ph = max(2, int(p["h"] * s))
        if pw > W * 3.2:
            continue
        sx = int(CX + (p["x"] - camx) * s)
        sy = int(CY + (p["y"] - camy) * s)

        tex = p["tex"].resize((pw, ph), Image.BILINEAR)
        if abs(p["giro"]) > 0.01:
            tex = tex.rotate(math.degrees(p["giro"]), Image.BILINEAR, expand=True)
            pw, ph = tex.size

        # névoa por profundidade
        f = np.clip((z - 1.0) / (PERIODO * 0.72), 0, 1) ** 0.85
        a = np.array(tex, np.float32) * (1 - f * 0.94)
        a += np.array([26, 18, 12], np.float32) * f * 0.85
        tex = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

        img.paste(tex, (sx - pw // 2, sy - ph // 2))

    # serragem
    d = ImageDraw.Draw(img, "RGBA")
    mz = (motes[:, 2] - camz) % PERIODO
    ok = (mz > 0.7) & (mz < PERIODO * 0.8)
    s = F / np.maximum(mz, 0.7)
    px = CX + (motes[:, 0] - camx + np.sin(mfase + t * math.tau * mvel) * 0.16) * s
    py = CY + (motes[:, 1] - camy + np.cos(mfase + t * math.tau * mvel) * 0.11) * s
    r = np.clip(s * 0.006, 0.6, 3.4)
    al = np.clip(190 * (1 - mz / (PERIODO * 0.8)) ** 1.5, 0, 190)
    for i in np.nonzero(ok & (px > -8) & (px < W + 8) & (py > -8) & (py < H + 8))[0]:
        rr = r[i]
        d.ellipse([px[i] - rr, py[i] - rr, px[i] + rr, py[i] + rr],
                  fill=(255, 206, 148, int(al[i])))

    a = np.array(img, np.float32)

    # brilho quente rasante + leve bloom
    bl = np.array(img.filter(ImageFilter.GaussianBlur(22)), np.float32)
    a = a * 0.88 + bl * 0.20
    a *= VIN
    a += rng.normal(0, 3.0, a.shape).astype(np.float32)
    return np.clip(a, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    ffmpeg = subprocess.run(
        ["node", "-e", "process.stdout.write(require('/tmp/claude-0/-home-user-Sites/e0c382d2-98b4-5e0a-bf23-351c68076563/scratchpad/node_modules/ffmpeg-static'))"],
        capture_output=True, text=True).stdout.strip()
    out = os.path.join(os.path.dirname(__file__), "..", "assets", "video", "hero.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    cmd = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "23",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-profile:v", "high", "-level", "4.0", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    for k in range(NF):
        pr.stdin.write(frame(k).tobytes())
        if k % 45 == 0:
            print(f"  frame {k}/{NF}", flush=True)
    pr.stdin.close()
    pr.wait()
    print("vídeo:", os.path.abspath(out), os.path.getsize(out) // 1024, "KB")
