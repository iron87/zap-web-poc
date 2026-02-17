#!/usr/bin/env sh
set -eu

exec "$(dirname "$0")/sso-local/02-scan.sh"
