#!/usr/bin/env bash
# Publica o app web no R2 (bucket atlas-brexplora). Requer rclone configurado com o remote "r2".
set -euo pipefail
cd "$(dirname "$0")/.."
rclone copyto www/index.html r2:atlas-brexplora/atlas.html --header-upload "Content-Type: text/html; charset=utf-8"
rclone sync www/lib r2:atlas-brexplora/lib
echo "Publicado. Verifique: curl -s https://pub-58f587f01b32444d95df39d7dfb2d438.r2.dev/atlas.html | grep -o '<!-- v[0-9]* -->'"
