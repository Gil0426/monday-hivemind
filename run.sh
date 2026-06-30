#!/usr/bin/env bash
set -e

# Resolve the script's own directory so this works when called via alias or from any path
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Load .env if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Guard: API key must be set
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY is not set."
  echo "Copy .env.example to .env and add your key, or export the variable in your shell."
  exit 1
fi

# Activate venv if one exists
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi

python -m manager.manager "$@"
