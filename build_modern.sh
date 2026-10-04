#!/bin/bash
BIN="/d/Deskpot/magiclantern_simplified-dev/.build-deps/xpacks/.bin"
export PATH="$BIN:$PATH"
ROOT="/d/Deskpot/magiclantern_simplified-dev"

PLATFORMS="5D4.133 5DSR.112 6D2.111 750D.110 77D.110 80D.103 850D.100 M50.110 M6II.111 R.180 R5.152 R6.150 RP.160 SX70.111 SX740.102 200D.101"

for p in $PLATFORMS; do
    echo "=== Building $p ==="
    cd "$ROOT/platform/$p"
    make ARM_BINPATH="$BIN" -j4 clean 2>&1 > /dev/null
    if make ARM_BINPATH="$BIN" -j4 2>&1 | tail -3 | grep -q "magiclantern.zip"; then
        ZIP="$ROOT/platform/$p/build/magiclantern.zip"
        SIZE=$(stat -c "%s" "$ZIP" 2>/dev/null || echo "0")
        echo "SUCCESS $p $SIZE"
        cp "$ZIP" "$ROOT/magiclantern-$p.zip"
    else
        echo "FAILED $p"
    fi
done
echo "=== DONE ==="