#!/usr/bin/env bash
# Baixa o vídeo e as fotos do Cross Lion para ./assets e reescreve o index.html
# para apontar para os arquivos locais. Rode uma vez, na sua máquina.
#   bash baixar-assets.sh
set -euo pipefail

B="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8/hf_20260827_154448_"
V="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8/hf_20260827_154258_9e98999c-646f-4ae1-bc83-88a59354dc36.mp4"
mkdir -p assets/img assets/video

ids=(890aafcd-2aad-427c-9496-52da90b41e4e f77054e2-2ea2-4e7c-813d-4875cd7f6299
     095a26ae-d75f-4e88-931d-273cc20b264d 955dae93-af18-4009-a2c4-f9b03cfe8751
     27dd47bc-d992-4845-a17a-0e387558a01d 7e0399eb-ef50-4f96-8dab-dc4a4befe57a
     6526df44-7608-4bac-85b3-013e34eb39fd 3a68bae7-c698-47bc-8dae-9fd04eebecfd
     3de71b35-263c-4805-a9d9-b5d3083a4f50 ff6b0b3a-5dbc-44b9-be01-1df9c445eded
     d86ad8df-c38a-41c3-ba65-c94b2f179df2)

echo "→ baixando ${#ids[@]} imagens…"
for id in "${ids[@]}"; do
  curl -fsSL -o "assets/img/${id}.webp" "${B}${id}_min.webp" && echo "   ok ${id:0:8}"
done

echo "→ baixando o vídeo (1080p / 15s)…"
curl -fsSL -o assets/video/hero.mp4 "$V"

# opcional: versão leve do vídeo, se houver ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then
  echo "→ gerando versão comprimida + poster…"
  ffmpeg -y -v error -i assets/video/hero.mp4 -an -c:v libx264 -crf 34 -preset medium \
         -pix_fmt yuv420p -movflags +faststart assets/video/hero-web.mp4
  ffmpeg -y -v error -i assets/video/hero.mp4 -vframes 1 -q:v 6 -vf scale=1600:-1 assets/video/poster.jpg
fi

echo "→ reescrevendo o index.html para caminhos locais…"
cp index.html index.html.bak
python3 - <<'PY'
import re
s=open('index.html',encoding='utf-8').read()
s=re.sub(r'https://d8j0ntlcm91z4\.cloudfront\.net/[^"\']*?hf_\d+_\d+_([0-9a-f-]{36})_min\.webp', r'assets/img/\1.webp', s)
s=re.sub(r'https://d8j0ntlcm91z4\.cloudfront\.net/[^"\']*?\.mp4', 'assets/video/hero.mp4', s)
open('index.html','w',encoding='utf-8').write(s)
PY
echo "✅ pronto. Backup do original em index.html.bak"
