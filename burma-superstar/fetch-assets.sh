#!/usr/bin/env bash
# Downloads the generated media into ./assets/ and switches index.html over to
# local files, so the site becomes fully self-contained (no CDN dependency).
#
#   ./fetch-assets.sh
#
# Run it from this folder. Needs curl. If ffmpeg is present it also produces a
# web-weight version of the hero video (the original is ~15 MB).
set -euo pipefail
cd "$(dirname "$0")"

BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3Fn9kvwewWSxcmhyI5mG7uDadG8"
mkdir -p assets

get () { # get <remote-filename> <local-name>
  if [ -s "assets/$2" ]; then
    echo "  · $2 (already here)"
    return
  fi
  echo "  ↓ $2"
  curl -fsSL --retry 3 --retry-delay 2 -o "assets/$2" "$BASE/$1"
}

echo "Fetching media…"
get hf_20260824_195938_c305d714-419d-4860-a314-832a03d66bc2.mp4 hero.mp4
get hf_20260824_195737_e27afdd1-da83-4edd-95a4-c6a859cef1a0.png tea-leaf-salad.png
get hf_20260824_195758_3f94b48f-b138-4e61-a477-1c911ed7d367.png samusa-soup.png
get hf_20260824_195758_84434e4d-e6ef-4696-84f7-9d46e10c980d.png rainbow-salad.png
get hf_20260824_195758_12fee7ab-9845-4a17-96b9-f3661dea4f73.png platha.png
get hf_20260824_195758_a6700c99-2c5d-49e8-b4f7-5ee89a927fed.png sesame-chicken.png
get hf_20260824_195758_f958da0f-9aa5-42ed-9270-72452f3456f7.png garlic-noodles.png
get hf_20260824_195758_272c8c86-1a34-47c0-8b75-6f53a3518c2c.png pork-belly.png
get hf_20260824_195758_f8392653-6310-4ce2-90c2-ff62224d12ea.png coconut-rice.png
get hf_20260824_195758_bf262599-59c6-4d6a-960c-59d14a70d3a9.png chili-lamb.png

# The source PNGs are 2048px and the video is ~15 MB. Shrink them for the web.
if command -v ffmpeg >/dev/null 2>&1; then
  if [ ! -s assets/hero.web.mp4 ]; then
    echo "Compressing hero video for the web…"
    ffmpeg -v error -y -i assets/hero.mp4 -an \
      -vf "scale=1280:-2" -c:v libx264 -profile:v high -crf 26 -preset slow \
      -movflags +faststart assets/hero.web.mp4
    mv assets/hero.mp4 assets/hero.original.mp4
    mv assets/hero.web.mp4 assets/hero.mp4
    echo "  hero.mp4 is now $(du -h assets/hero.mp4 | cut -f1) (original kept as hero.original.mp4)"
  fi
else
  echo "! ffmpeg not found — hero.mp4 stays at its original ~15 MB."
fi

if command -v magick >/dev/null 2>&1 || command -v convert >/dev/null 2>&1; then
  CONV=$(command -v magick || command -v convert)
  echo "Resizing stills…"
  for f in assets/*.png; do
    "$CONV" "$f" -resize '1200x1200>' -strip -quality 86 "$f"
  done
fi

# point the page at the local copies
if grep -q 'var ASSET_LOCAL = false;' index.html; then
  sed -i.bak 's/var ASSET_LOCAL = false;/var ASSET_LOCAL = true;/' index.html
  rm -f index.html.bak
  echo "index.html now reads from ./assets/"
else
  echo "index.html already points at ./assets/"
fi

echo
echo "Done. Open index.html, or serve the folder:  python3 -m http.server 8080"
