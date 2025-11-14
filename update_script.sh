#!/usr/bin/env bash
set -euo pipefail

VENV_PY="$(pwd)/.venv/bin/python"
echo "Using venv python: $VENV_PY"
echo "Python executable check:"
"$VENV_PY" -c 'import sys; print(sys.executable); print("python %s" % sys.version.split()[0])'

echo
echo "pyvenv.cfg (system-site-packages?):"
if [ -f .venv/pyvenv.cfg ]; then
  grep -i "system-site-packages" .venv/pyvenv.cfg || true
else
  echo " .venv/pyvenv.cfg not found"
fi

echo
echo "Current pip-installed metadata for yt-dlp (if any):"
"$VENV_PY" -m pip show yt-dlp || echo "yt-dlp not found by pip in this venv"

echo
echo "List installed files for yt-dlp (pip show -f):"
"$VENV_PY" -m pip show -f yt-dlp || true

echo
echo "Location of yt-dlp module & runtime version (if importable):"
"$VENV_PY" - <<'PY'
try:
    import importlib
    m = importlib.import_module("yt_dlp")
    v = getattr(m, "__version__", None)
    print("yt_dlp importable, __file__:", getattr(m, "__file__", None))
    print("yt_dlp.__version__:", v)
except Exception as e:
    print("yt_dlp not importable or error:", e)
PY

echo
if [ -f .venv/bin/yt-dlp ]; then
  echo "Shebang of .venv/bin/yt-dlp (first line):"
  head -n 1 .venv/bin/yt-dlp || true
else
  echo ".venv/bin/yt-dlp not present"
fi

echo
echo "=== FORCE reinstall requested version 2025.11.12 ==="
# uninstall first to avoid editable/leftover files and then force reinstall a specific version
"$VENV_PY" -m pip uninstall -y yt-dlp || true
"$VENV_PY" -m pip install --no-cache-dir --force-reinstall yt-dlp==2025.11.12

echo
echo "After reinstall, pip show:"
"$VENV_PY" -m pip show yt-dlp || true

echo
echo "Runtime import check again:"
"$VENV_PY" - <<'PY'
try:
    import importlib
    m = importlib.import_module("yt_dlp")
    print("yt_dlp __file__:", m.__file__)
    print("yt_dlp __version__:", getattr(m, "__version__", None))
except Exception as e:
    print("Import error:", e)
PY

echo
echo "Done."
