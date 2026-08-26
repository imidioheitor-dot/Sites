#!/usr/bin/env bash
# ---------------------------------------------------------------
# Liberté Dance Studio — baixa as imagens e o vídeo gerados por IA
# para dentro de assets/. Rode UMA vez, na sua máquina:
#
#     bash assets/baixar-assets.sh
#
# (Os arquivos ficam hospedados na sua conta Higgsfield. O download
#  não foi possível na sessão do Claude porque o CDN está fora da
#  allowlist de rede daquele ambiente — na sua máquina funciona.)
# ---------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"
B="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8"
mkdir -p img video

get(){ echo "  → $1"; curl -fsSL --retry 3 -o "$1" "$2"; }

echo "Imagens…"
get img/hero-3d.png        "$B/hf_20260826_200513_a795b386-4cb3-4dea-9d11-fad8bcb21a1f.png"
get img/portal-tall.png    "$B/hf_20260826_200513_7e526f0c-b9c0-4abe-8014-d711d61f8ab4.png"
get img/jazz.png           "$B/hf_20260826_200513_2f04de68-2b29-4716-9f28-03ffcf5710f8.png"
get img/contemporaneo.png  "$B/hf_20260826_200513_735463bf-b9f1-415e-8138-dc839d91f348.png"
get img/sapateado.png      "$B/hf_20260826_200513_513632d0-8f86-4d46-b9b3-693ed3cee7dc.png"
get img/urbanas.png        "$B/hf_20260826_200513_8989866d-f1c1-4358-94f4-f573d4b2a04b.png"
get img/estudio.png        "$B/hf_20260826_200513_56b0c09c-f376-46d4-94a5-1de12afb6c7f.png"
get img/exame.png          "$B/hf_20260826_200513_f40f5c6f-5b33-4479-884a-021d779851b1.png"
get img/bailarina.png      "$B/hf_20260826_200513_0d7e7344-f4bf-4bbf-9b1f-e5bd0d49baf9.png"
get img/barra.png          "$B/hf_20260826_201140_fe7c5c04-f8f1-44cf-97f5-92a46a9c1900.png"

echo "Vídeo do hero (15s · 1080p)…"
get video/hero.mp4         "$B/hf_20260826_200641_414366f8-dd7a-4bad-b58d-3d21874d589b.mp4"

# --- converte PNG → JPG (o site referencia .jpg) --------------------
if command -v magick >/dev/null 2>&1;   then CONV="magick";
elif command -v convert >/dev/null 2>&1; then CONV="convert";
else CONV=""; fi

if [ -n "$CONV" ]; then
  echo "Convertendo para JPG…"
  for f in img/*.png; do
    "$CONV" "$f" -strip -resize '1800x1800>' -quality 82 "${f%.png}.jpg" && rm "$f"
  done
elif command -v python3 >/dev/null 2>&1 && python3 -c "import PIL" 2>/dev/null; then
  echo "Convertendo para JPG (Pillow)…"
  python3 - <<'PY'
from PIL import Image; import glob, os
for f in glob.glob("img/*.png"):
    im = Image.open(f).convert("RGB"); im.thumbnail((1800,1800))
    im.save(f[:-4]+".jpg", "JPEG", quality=82, optimize=True); os.remove(f)
PY
else
  echo "!! Nem ImageMagick nem Pillow encontrados."
  echo "   Os PNGs foram baixados. Renomeie/converta para .jpg manualmente,"
  echo "   ou troque as extensões no index.html de .jpg para .png."
fi

echo
echo "✅ Pronto. Abra index.html no navegador."
