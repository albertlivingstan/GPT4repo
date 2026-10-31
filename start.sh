#!/usr/bin/env bash
#
# One-command launcher for all 6 AI experiments
#
cd "$(dirname "$0")"

if [ -f ".venv_shared/bin/python" ]; then
    .venv_shared/bin/python run_all.py
else
    python3 run_all.py
fi

