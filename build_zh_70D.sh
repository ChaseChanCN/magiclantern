#!/usr/bin/env bash
# =============================================================================
# Magic Lantern — Chinese (汉化) build for Canon EOS 70D (70D.112)
# =============================================================================
# Run this in Git Bash / MSYS2 on Windows.  It:
#   1. Installs the ARM cross-toolchain (arm-none-eabi-gcc) + make via xpm/npm
#      (NO admin rights needed).  This step is ~500MB and slow — run it in a
#      real terminal, not inside the IDE sandbox.
#   2. Builds platform/70D.112  ->  platform/70D.112/build/magiclantern.zip
#   3. Prints the location of the finished 成品 (autoexec.bin + zip).
#
# If you already have arm-none-eabi-gcc + make on PATH, the install is skipped.
# =============================================================================
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
echo "=== Magic Lantern 70D 汉化 build ==="

# ---- 1. toolchain -----------------------------------------------------------
have_tc() { command -v arm-none-eabi-gcc >/dev/null 2>&1; }
have_make() { command -v make >/dev/null 2>&1; }

if ! have_tc || ! have_make; then
  echo "[setup] installing xpm + ARM toolchain (no admin)..."
  npm install -g xpm@latest --no-fund --no-audit || true
  DEPS="$ROOT/.build-deps"
  mkdir -p "$DEPS"
  (
    cd "$DEPS"
    xpm init-y 2>/dev/null || true
    xpm install @xpack-dev-tools/arm-none-eabi-gcc@latest || true
    xpm install @xpack-dev-tools/make@latest || true
  )
  # locate the binaries and put them on PATH
  for d in "$DEPS"/xpacks/.bin "$DEPS"/xpacks/@xpack-dev-tools/arm-none-eabi-gcc/*/.content/bin "$DEPS"/xpacks/@xpack-dev-tools/make/*/.content/bin; do
    [ -d "$d" ] && export PATH="$d:$PATH"
  done
fi

echo "[check] arm-none-eabi-gcc: $(command -v arm-none-eabi-gcc || echo MISSING)"
echo "[check] make:              $(command -v make || echo MISSING)"
echo "[check] python3:           $(command -v python3 || command -v python || echo MISSING)"

if ! have_tc; then
  echo
  echo "ERROR: arm-none-eabi-gcc not found."
  echo "Install one of:"
  echo "  - xpm:  npm i -g xpm; xpm install @xpack-dev-tools/arm-none-eabi-gcc@latest"
  echo "  - WSL:  sudo apt install gcc-arm-none-eabi make"
  echo "  - Arm:  https://developer.arm.com/downloads/-/gnu-embedded-toolchain-for-arm"
  echo "then re-run this script."
  exit 1
fi
if ! have_make; then
  echo "ERROR: make not found (install via xpm @xpack-dev-tools/make or MSYS2)."
  exit 1
fi

# ---- 2. build 70D.112 -------------------------------------------------------
echo
echo "=== building platform/70D.112 ==="
cd "$ROOT/platform/70D.112"
make clean 2>/dev/null || true
make -j4

# ---- 3. report --------------------------------------------------------------
echo
echo "=== build complete ==="
ZIP="$ROOT/platform/70D.112/build/magiclantern.zip"
BIN="$ROOT/platform/70D.112/build/autoexec.bin"
echo "成品 zip: $ZIP"
echo "autoexec.bin: $BIN"
ls -la "$ZIP" "$BIN" 2>/dev/null || true
echo
echo "Copy the contents of the zip to your SD card (root), then boot the 70D."
echo "TEST ON QEMU FIRST (make CONFIG_QEMU=y) before running on a real camera!"