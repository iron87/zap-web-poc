#!/usr/bin/env sh
set -eu

mkdir -p reports

docker compose up -d --build app

echo "App avviata su http://localhost:8080"
