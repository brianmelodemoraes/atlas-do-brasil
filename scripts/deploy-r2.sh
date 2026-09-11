#!/usr/bin/env bash
# Publica o app web no R2 (bucket atlas-brexplora). Requer rclone configurado com o remote "r2".
set -euo pipefail
cd "$(dirname "$0")/.."
npm run -s version:json
rclone copyto www/index.html r2:atlas-brexplora/atlas.html --header-upload "Content-Type: text/html; charset=utf-8" --s3-no-check-bucket
rclone copyto www/VERSION.json r2:atlas-brexplora/VERSION.json --header-upload "Content-Type: application/json" --s3-no-check-bucket
rclone copyto www/privacidade.html r2:atlas-brexplora/privacidade.html --header-upload "Content-Type: text/html; charset=utf-8" --s3-no-check-bucket
# deep links (só depois de preencher TEAMID e SHA-256):
rclone copyto www/.well-known/apple-app-site-association r2:atlas-brexplora/.well-known/apple-app-site-association --header-upload "Content-Type: application/json" --s3-no-check-bucket
rclone copyto www/.well-known/assetlinks.json r2:atlas-brexplora/.well-known/assetlinks.json --header-upload "Content-Type: application/json" --s3-no-check-bucket
rclone sync www/lib r2:atlas-brexplora/lib
echo "Publicado. Verifique: curl -s https://atlasbrexplora.app/atlas.html | grep -o '<!-- v[0-9]* -->'"
