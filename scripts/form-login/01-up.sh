#!/usr/bin/env sh
set -eu

mkdir -p reports

docker compose up -d --build app

echo "App started on http://localhost:8080"
