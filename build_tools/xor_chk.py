#!/usr/bin/env python3
"""Python port of build_tools/xor_chk.c — patches the XOR checksum field in the
autoexec.bin footer.  Usage: python xor_chk.py <file>"""
import sys, struct

FOOTER_MAGIC = 0xCCCCCCCCE12FFF13

def main():
    if len(sys.argv) != 2:
        print("Invalid parameter count (%d)" % len(sys.argv)); sys.exit(1)
    path = sys.argv[1]
    with open(path, "rb") as f:
        buf = f.read()

    # XOR all 4-byte little-endian words from the start
    checksum = 0
    data = 0
    n = len(buf)
    off = 0
    while off + 4 <= n:
        data = struct.unpack_from("<I", buf, off)[0]
        checksum = (checksum ^ data) & 0xFFFFFFFF
        off += 4

    # value to write = last_word ^ checksum
    out = (data ^ checksum) & 0xFFFFFFFF

    # check footer magic (last 8 bytes, little-endian)
    if n < 8:
        print("File too small"); sys.exit(1)
    footer = struct.unpack_from("<Q", buf, n - 8)[0]
    if footer != FOOTER_MAGIC:
        print("Footer magic error (expected 0x%X, got 0x%X)" % (FOOTER_MAGIC, footer)); sys.exit(1)

    # write `out` at -4 from end
    buf = buf[:n - 4] + struct.pack("<I", out)
    with open(path, "wb") as f:
        f.write(buf)

if __name__ == "__main__":
    main()