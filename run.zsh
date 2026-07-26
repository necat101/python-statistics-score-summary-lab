#!/usr/bin/env zsh
set -euo pipefail
cd "${0:a:h}"

echo "== check.py =="
python3 check.py
echo
echo "== unittest =="
python3 -m unittest -v
