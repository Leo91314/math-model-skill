#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
export MPLCONFIGDIR="$PROJECT_ROOT/.cache/matplotlib"
export IPYTHONDIR="$PROJECT_ROOT/.cache/ipython"
export JUPYTER_CONFIG_DIR="$PROJECT_ROOT/.cache/jupyter/config"
export JUPYTER_RUNTIME_DIR="$PROJECT_ROOT/.cache/jupyter/runtime"
export JUPYTER_PATH="$PROJECT_ROOT/.venv/share/jupyter${JUPYTER_PATH:+:$JUPYTER_PATH}"
export XDG_CACHE_HOME="$PROJECT_ROOT/.cache"
mkdir -p "$MPLCONFIGDIR" "$IPYTHONDIR" "$JUPYTER_CONFIG_DIR" "$JUPYTER_RUNTIME_DIR"
.venv/bin/python scripts/smoke_test.py
.venv/bin/python -m ipykernel install --prefix .venv --name math-model-skill --display-name 'Python math model skill'
.venv/bin/python scripts/check_kernel.py
if [[ "${1:-}" == "--documents" ]]; then
  .venv/bin/python scripts/build_env_documents.py
  (
    cd outputs/env_check
    xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error environment_check.tex > xelatex.stdout.log 2>&1
  )
  pdftoppm -r 120 -png -singlefile outputs/env_check/environment_check.pdf outputs/env_check/pdf_preview
  if [[ -n "${CODEX_DOCS_SKILL:-}" ]]; then
    DOCS_PYTHON="${CODEX_DOCS_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
    FONTCONFIG_FILE="$PROJECT_ROOT/.cache/fontconfig.conf" "$DOCS_PYTHON" "$CODEX_DOCS_SKILL/render_docx.py" outputs/env_check/environment_check.docx --output_dir outputs/env_check/docx_render --emit_pdf
    .venv/bin/python scripts/verify_env_artifacts.py
  else
    printf '%s\n' 'DOCX generated; Word rendering and artifact verification skipped: set CODEX_DOCS_SKILL.'
  fi
fi
