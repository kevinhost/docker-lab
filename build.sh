#!/usr/bin/env bash
# Genere les PDF de tous les labos (ou de ceux passes en argument).
#
#   ./build.sh
#   ./build.sh labs/04-dockerfile
#   ./build.sh labs/04-dockerfile/01-theorie.md
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creation de l'environnement Python (.venv)..."
  python3 -m venv .venv
  ./.venv/bin/pip install --quiet --upgrade pip
  ./.venv/bin/pip install --quiet markdown pygments
fi

exec ./.venv/bin/python tools/build_pdf.py "$@"
