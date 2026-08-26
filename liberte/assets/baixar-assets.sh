#!/usr/bin/env bash
# ---------------------------------------------------------------
# Liberté Dance Studio — traz as imagens e o vídeo definitivos
# para dentro de assets/.
#
#     bash assets/baixar-assets.sh
#
# OPCIONAL: o site já funciona sem isso. Quando um arquivo local
# não existe, o próprio index.html busca a cópia hospedada. Rodar
# este script só deixa o site autocontido e mais rápido.
# ---------------------------------------------------------------
cd "$(dirname "$0")" || exit 1
B="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8"
mkdir -p img video

if ! command -v curl >/dev/null 2>&1; then
  echo "!! curl não encontrado. Instale-o, ou simplesmente use o site"
  echo "   como está: ele busca as imagens sozinho pela internet."
  exit 1
fi

OK=0; FALHA=0
get(){                       # get <destino> <url>
  printf '  %-26s' "$1"
  if curl -fsSL --retry 3 --max-time 180 -o "$1.tmp" "$2" 2>/dev/null; then
    mv -f "$1.tmp" "$1"; echo "ok"; OK=$((OK+1))
  else
    rm -f "$1.tmp"; echo "FALHOU"; FALHA=$((FALHA+1))
  fi
}

echo "Imagens…"
get img/hero-3d.png       "$B/hf_20260826_200513_a795b386-4cb3-4dea-9d11-fad8bcb21a1f.png"
get img/portal-tall.png   "$B/hf_20260826_200513_7e526f0c-b9c0-4abe-8014-d711d61f8ab4.png"
get img/jazz.png          "$B/hf_20260826_200513_2f04de68-2b29-4716-9f28-03ffcf5710f8.png"
get img/contemporaneo.png "$B/hf_20260826_200513_735463bf-b9f1-415e-8138-dc839d91f348.png"
get img/sapateado.png     "$B/hf_20260826_200513_513632d0-8f86-4d46-b9b3-693ed3cee7dc.png"
get img/urbanas.png       "$B/hf_20260826_200513_8989866d-f1c1-4358-94f4-f573d4b2a04b.png"
get img/estudio.png       "$B/hf_20260826_200513_56b0c09c-f376-46d4-94a5-1de12afb6c7f.png"
get img/exame.png         "$B/hf_20260826_200513_f40f5c6f-5b33-4479-884a-021d779851b1.png"
get img/bailarina.png     "$B/hf_20260826_200513_0d7e7344-f4bf-4bbf-9b1f-e5bd0d49baf9.png"
get img/barra.png         "$B/hf_20260826_201140_fe7c5c04-f8f1-44cf-97f5-92a46a9c1900.png"

echo "Vídeo do hero (15s · 1080p)…"
get video/hero.mp4        "$B/hf_20260826_200641_414366f8-dd7a-4bad-b58d-3d21874d589b.mp4"

# --- PNG → JPG. Se não houver conversor, o site usa os PNG mesmo. -----
CONV=""
command -v magick  >/dev/null 2>&1 && CONV="magick"
[ -z "$CONV" ] && command -v convert >/dev/null 2>&1 && CONV="convert"

if [ -n "$CONV" ]; then
  echo "Convertendo para JPG ($CONV)…"
  for f in img/*.png; do
    [ -e "$f" ] || continue
    "$CONV" "$f" -strip -resize '1800x1800>' -quality 82 "${f%.png}.jpg" \
      && rm -f "$f" && echo "  ${f##*/} → jpg"
  done
elif command -v python3 >/dev/null 2>&1 && python3 -c "import PIL" 2>/dev/null; then
  echo "Convertendo para JPG (Pillow)…"
  python3 - <<'PY'
from PIL import Image; import glob, os
for f in glob.glob("img/*.png"):
    try:
        im = Image.open(f).convert("RGB"); im.thumbnail((1800,1800))
        im.save(f[:-4]+".jpg", "JPEG", quality=82, optimize=True); os.remove(f)
        print("  "+os.path.basename(f)+" → jpg")
    except Exception as e:
        print("  "+os.path.basename(f)+": "+str(e))
PY
else
  echo "Sem ImageMagick nem Pillow — os PNG ficam como estão."
  echo "O site reconhece .png automaticamente, então está tudo certo."
fi

echo
echo "  $OK baixado(s), $FALHA falha(s)."
if [ "$FALHA" -gt 0 ]; then
  echo "  Os que falharam continuam sendo buscados online pelo site."
fi
echo "✅ Abra index.html no navegador."
