#!/usr/bin/env sh
set -eu

mkdir -p reports

docker compose run --rm --no-deps zap \
  zap.sh -cmd -autorun /zap/wrk/zap/automation.yaml

echo "Scan completata. Report in ./reports"
