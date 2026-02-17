#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

"$SCRIPT_DIR/01-up.sh"
"$SCRIPT_DIR/02-scan.sh"
"$SCRIPT_DIR/03-down.sh"
