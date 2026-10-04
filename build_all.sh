#!/bin/bash
# Build all ML platforms and collect results
BIN="/d/Deskpot/magiclantern_simplified-dev/.build-deps/xpacks/.bin"
export PATH="$BIN:$PATH"
ROOT="/d/Deskpot/magiclantern_simplified-dev"
RESULTS="$ROOT/build_all_results.txt"
> "$RESULTS"

PLATFORMS="100D.101 1100D.105 500D.111 50D.109 550D.109 5D2.212 5D3.113 5D3.123 600D.102 60D.111 650D.104 6D.116 700D.115 70D.112 7D.203 7D2.112 EOSM.202"

for p in $PLATFORMS; do
    echo "=== Building $p ===" | tee -a "$RESULTS"
    cd "$ROOT/platform/$p"
    make ARM_BINPATH="$BIN" -j4 clean 2>&1 > /dev/null
    if make ARM_BINPATH="$BIN" -j4 2>&1 | tail -3 | grep -q "magiclantern.zip"; then
        ZIP="$ROOT/platform/$p/build/magiclantern.zip"
        SIZE=$(stat -c "%s" "$ZIP" 2>/dev/null || echo "0")
        echo "SUCCESS $p $SIZE" | tee -a "$RESULTS"
        cp "$ZIP" "$ROOT/magiclantern-$p.zip"
    else
        echo "FAILED $p" | tee -a "$RESULTS"
    fi
done

echo "=== DONE ===" | tee -a "$RESULTS"