#!/usr/bin/env sh
set -eu

exec "$(dirname "$0")/api-openapi/02-scan.sh"
