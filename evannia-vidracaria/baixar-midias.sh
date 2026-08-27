#!/usr/bin/env bash
# Baixa o vídeo e as 8 fotos geradas para dentro de assets/, com os nomes que o
# index.html espera. Rode a partir desta pasta:
#
#   bash baixar-midias.sh
#
# (A sessão que montou o site não conseguiu baixar: o proxy de rede bloqueou o
#  CDN com 403. Na sua máquina funciona normalmente.)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/img assets/video
B="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8"

get(){ echo "  → $2"; curl -fsSL -o "$2" "$B/$1"; }

echo "Baixando o vídeo do topo (15 s, 1080p)…"
get hf_20260827_154431_a14d2af3-a906-46e0-8887-96dc7f942402.mp4 assets/video/hero.mp4

echo "Baixando as fotos…"
get hf_20260827_154539_91534977-f8c5-4a47-a4ea-1fde49fa4f12.png assets/img/box-banheiro.jpg
get hf_20260827_154539_17594e15-1d28-4f80-b93e-7cc7f369e478.png assets/img/espelho.jpg
get hf_20260827_154539_c64b00f8-8591-4495-b2d7-cc3437df790c.png assets/img/janela.jpg
get hf_20260827_154539_f3b7b295-ab81-485d-8888-45447bb7490e.png assets/img/sacada.jpg
get hf_20260827_154539_f7e2fa43-a030-4a34-93f7-aa73db5faf9e.png assets/img/porta.jpg
get hf_20260827_154539_deec0890-1500-47f6-b00e-6b63089a837b.png assets/img/macro-vidro.jpg
get hf_20260827_154539_c0860255-95c1-409e-bbcb-10d533b693bb.png assets/img/tampo.jpg
get hf_20260827_154539_d78536f1-c7a4-48d4-be17-713642abb3f3.png assets/img/oficina.jpg

echo
echo "Pronto. Abra index.html no navegador."
echo "Obs.: os arquivos são PNG com extensão .jpg — funciona, mas para o site"
echo "ficar leve, converta para JPG/WebP (qualidade ~80) mantendo os nomes."
