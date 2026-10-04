#!/usr/bin/env bash
# Run via Git Bash.  Fixes the two missing pieces (make + real python3) and
# builds ML for 70D.  Assumes build_zh_70D.sh already installed the ARM toolchain.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
BIN="$ROOT/.build-deps/xpacks/.bin"
PYREAL="/c/Users/xuela/AppData/Local/Programs/Python/Python311/python.exe"

# fall back to whatever `py -3` resolves to
if [ ! -x "$PYREAL" ]; then
  PYREAL="$(py -3 -c 'import sys; print(sys.executable)' 2>/dev/null)"
fi
echo "real python: $PYREAL"

export PATH="$BIN:$PATH"

# ---- make ----
if ! command -v make >/dev/null 2>&1; then
  echo "[fix] installing make from MSYS2 package..."
  "$PYREAL" "$ROOT/build_tools/install_make.py" "$BIN"
fi

# ---- python3 shim (Store stub is useless) ----
if [ ! -f "$BIN/python3" ]; then
  echo "[fix] creating python3 shim -> $BIN/python3"
  printf '#!/bin/sh\nexec "%s" "$@"\n' "$PYREAL" > "$BIN/python3"
  chmod +x "$BIN/python3"
fi

# ---- verify ----
echo "[check] arm-none-eabi-gcc: $(command -v arm-none-eabi-gcc || echo MISSING) [$(arm-none-eabi-gcc --version 2>/dev/null | head -1)]"
echo "[check] make:              $(command -v make || echo MISSING)"
echo "[check] python3:           $(python3 --version 2>&1 || echo MISSING)"
command -v arm-none-eabi-gcc >/dev/null || { echo "ERROR: toolchain missing — run build_zh_70D.sh first"; exit 1; }
command -v make >/dev/null || { echo "ERROR: make install failed"; exit 1; }

# ---- build 70D ----
echo
echo "=== building platform/70D.112 ==="
cd "$ROOT/platform/70D.112"
make clean 2>/dev/null || true
make -j4

echo
echo "=== done ==="
ls -la build/magiclantern.zip build/autoexec.bin 2>/dev/null
echo "成品: $ROOT/platform/70D.112/build/magiclantern.zip"