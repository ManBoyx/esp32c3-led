#!/bin/sh
# Lance le tableau en direct (Ctrl+C pour quitter)
cd "$(dirname "$0")" && exec .venv/bin/python pc/tableau.py "$@"
