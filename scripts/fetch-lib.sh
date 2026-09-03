#!/usr/bin/env bash
# Reconstrói www/lib a partir das fontes originais (npm + GitHub). Nada de CDN em produção.
set -euo pipefail
cd "$(dirname "$0")/../www/lib"
TMP=$(mktemp -d)
( cd "$TMP" && npm pack maplibre-gl@4.7.1 pmtiles@3.2.0 @fontsource/instrument-serif @fontsource/instrument-sans @fontsource/ibm-plex-mono --silent >/dev/null
  for t in *.tgz; do mkdir -p "x/${t%.tgz}" && tar xzf "$t" -C "x/${t%.tgz}"; done )
cp "$TMP"/x/maplibre-gl-*/package/dist/maplibre-gl.js .
cp "$TMP"/x/maplibre-gl-*/package/dist/maplibre-gl.css .
cp "$TMP"/x/pmtiles-*/package/dist/pmtiles.js .
for f in instrument-serif-latin-400-normal instrument-serif-latin-400-italic instrument-sans-latin-400-normal instrument-sans-latin-400-italic instrument-sans-latin-500-normal instrument-sans-latin-600-normal ibm-plex-mono-latin-400-normal ibm-plex-mono-latin-500-normal; do
  cp "$TMP"/x/fontsource-*/package/files/$f.woff2 . 2>/dev/null || cp "$TMP"/x/*/package/files/$f.woff2 .
done
# glifos Noto Sans (OFL) — mesmos do maplibre/demotiles, auto-hospedados como lib/glyphs-<stack>-<range>.pbf
B="https://raw.githubusercontent.com/maplibre/demotiles/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/font"
for st in "Noto Sans Regular:NotoRegular" "Noto Sans Italic:NotoItalic"; do
  src="${st%%:*}"; dst="${st##*:}"
  for r in 0-255 256-511 512-767 7680-7935 8192-8447; do curl -sL -o "glyphs-$dst-$r.pbf" "$B/${src// /%20}/$r.pbf"; done
done
curl -sL -o LICENSE-NotoSans.md "$B/Noto%20Sans%20Regular/LICENSE.md"
rm -rf "$TMP"; ls -la
