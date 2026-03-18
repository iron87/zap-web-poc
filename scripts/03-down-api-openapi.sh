#!/usr/bin/env sh
set -eu

exec "$(dirname "$0")/api-openapi/03-down.sh"
