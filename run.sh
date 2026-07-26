#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "== check.py =="
python3 check.py
echo
echo "== unittest =="
python3 -m unittest -v
