#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -n "${DISPLAY:-}" ]]; then
    python gui.py
elif command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a python gui.py
else
    echo "No graphical display or xvfb-run was found."
    echo "Install Xvfb with:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install -y xvfb"
    exit 1
fi