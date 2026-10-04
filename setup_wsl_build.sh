#!/usr/bin/env bash
# =============================================================================
# Run INSIDE WSL Ubuntu.  Sets up the ML 70D Chinese build + QEMU emulation.
# =============================================================================
# From WSL, run:
#   cd /mnt/d/Deskpot/magiclantern_simplified-dev
#   bash setup_wsl_build.sh
#
# It will:
#   1. apt install: ARM toolchain (gcc-arm-none-eabi), make, python3,
#      libguestfs-tools (for disk_image), and qemu-eos build deps.
#   2. Copy the repo into WSL native FS (building over /mnt is very slow).
#   3. Build ML for 70D with CONFIG_QEMU=y  ->  magiclantern.zip + autoexec.bin
#   4. make disk_image  ->  sd.qcow2 / cf.qcow2  (needs libguestfs)
#   5. Print how to run qemu-eos (you must supply a 70D ROM dump).
# =============================================================================
set -e

WIN_REPO="$(pwd)"
WSL_REPO="$HOME/ml-70d-build"
echo "=== ML 70D QEMU build inside WSL ==="

# ---- 1. dependencies --------------------------------------------------------
echo "[1/5] installing build dependencies (sudo)..."
sudo apt update
sudo apt install -y \
    build-essential gcc-arm-none-eabi make python3 python3-pip \
    libguestfs-tools \
    git ninja-build meson python3-venv \
    libglib2.0-dev libpixman-1-dev libfdt-dev zlib1g-dev

# ---- 2. copy repo into WSL native FS ----------------------------------------
echo "[2/5] copying repo to $WSL_REPO (native FS, faster builds)..."
rsync -a --delete --exclude='.codeartsdoer' --exclude='.build-deps' \
    "$WIN_REPO/" "$WSL_REPO/"
cd "$WSL_REPO"

# ---- 3. build ML for QEMU ---------------------------------------------------
echo "[3/5] building ML 70D with CONFIG_QEMU=y..."
cd platform/70D.112
make clean
make CONFIG_QEMU=y -j"$(nproc)"
echo "  -> build/magiclantern.zip  and  build/autoexec.bin"

# ---- 4. disk image for qemu-eos ---------------------------------------------
echo "[4/5] creating qemu disk image (needs libguestfs)..."
make disk_image
echo "  -> build/sd.qcow2  and  build/cf.qcow2"

# ---- 5. qemu-eos instructions -----------------------------------------------
cat <<EOF

=== build complete ===
ML 70D QEMU build: $WSL_REPO/platform/70D.112/build/
  - magiclantern.zip   (the 成品)
  - autoexec.bin
  - sd.qcow2 / cf.qcow2 (qemu disk images)

=== next: run under qemu-eos ===
qemu-eos (the patched QEMU) is NOT installed yet.  To emulate the 70D you need:

  A) a 70D ROM dump (NOT bundled — you must dump it from your camera):
       * Install ML on the 70D, then Debug menu -> Dump -> ROM dump,
         or use the 'romdump' module.  This yields ROM1.BIN (and maybe ROM0).
       * Copy the ROM into e.g. ~/70D-rom/

  B) build qemu-eos from source (one time, ~15 min):
       git clone --branch qemu-eos-v4.2.1 https://github.com/reticulatedpines/qemu-eos
       cd qemu-eos
       mkdir build && cd build
       ../configure --target-list=arm-softmmu --disable-werror
       make -j\$(nproc)

  C) run the emulator (see qemu-eos repo for exact flags / run_qemu.py):
       qemu-system-arm -M eos -romfile ~/70D-rom/ROM1.BIN \\
         -drive file=$WSL_REPO/platform/70D.112/build/sd.qcow2,format=qcow2,if=sd

The ML menu should appear in the emulated LCD window with Chinese text.
If glyphs show as blank boxes, the CRBF font isn't being loaded — check
that ML/FONTS/cjk*.crbf are present on the sd.qcow2 image.
EOF