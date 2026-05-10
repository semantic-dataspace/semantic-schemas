#!/usr/bin/env bash
# run_notebooks.sh — execute and validate all workflow notebooks
#
# Usage:
#   ./scripts/run_notebooks.sh              # run all notebooks (test mode)
#   ./scripts/run_notebooks.sh --refresh    # re-execute and save outputs in-place
#   ./scripts/run_notebooks.sh path/to/nb.ipynb  # run a single notebook
#
# Requirements: activate your virtual environment first.
#   python -m venv .venv && source .venv/bin/activate
#   pip install -r requirements-dev.txt

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ── Collect notebooks ──────────────────────────────────────────────────────
if [ $# -ge 1 ] && [ "$1" = "--refresh" ]; then
    MODE="--refresh"
    if [ $# -ge 2 ]; then
        # Specific notebooks: ./scripts/run_notebooks.sh --refresh path/to/nb.ipynb ...
        NOTEBOOKS=("${@:2}")
    else
        # All notebooks under schemas/, excluding checkpoint folders
        mapfile -t NOTEBOOKS < <(
            find schemas -name "*.ipynb" \
                ! -path "*/.ipynb_checkpoints/*" \
                | sort
        )
    fi
elif [ $# -ge 1 ]; then
    # Single/multiple notebooks in test mode
    NOTEBOOKS=("$@")
    MODE="test"
else
    # All notebooks in test mode
    mapfile -t NOTEBOOKS < <(
        find schemas -name "*.ipynb" \
            ! -path "*/.ipynb_checkpoints/*" \
            | sort
    )
    MODE="test"
fi

echo "Found ${#NOTEBOOKS[@]} notebook(s)."
echo ""

# ── Run ────────────────────────────────────────────────────────────────────
if [ "$MODE" = "--refresh" ]; then
    # Re-execute and save outputs in-place (for documentation commits)
    echo "Mode: refresh (executing and saving outputs in-place)"
    echo ""
    for nb in "${NOTEBOOKS[@]}"; do
        echo "  Refreshing: $nb"
        jupyter nbconvert \
            --to notebook \
            --execute \
            --inplace \
            --ExecutePreprocessor.timeout=300 \
            "$nb"
    done
    echo ""
    echo "Regenerating manifest …"
    python scripts/generate_manifest.py
    echo ""
    echo "Done. Commit *.ipynb and schemas/manifest.json together with any schema changes."
else
    # Test mode: execute and check for errors, do not save outputs
    echo "Mode: test (pytest + nbmake + manifest check)"
    echo ""
    pytest --nbmake "${NOTEBOOKS[@]}"
    pytest tests/test_manifest.py -v
fi
