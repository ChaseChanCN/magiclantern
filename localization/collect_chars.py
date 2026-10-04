#!/usr/bin/env python3
"""Collect all CJK characters used in src/ and modules/ source after translation,
write them to chars.txt so the font generator can cover every glyph."""
import glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = glob.glob(str(ROOT / "src" / "*.c")) + glob.glob(str(ROOT / "src" / "*.h")) + glob.glob(str(ROOT / "modules" / "*" / "*.c"))
chars = set()
for f in files:
    try:
        t = Path(f).read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for ch in t:
        cp = ord(ch)

        if 0x4E00 <= cp <= 0x9FFF or 0x3000 <= cp <= 0x303F or 0xFF00 <= cp <= 0xFFEF:
            chars.add(ch)

out = "".join(sorted(chars))
(ROOT / "localization" / "chars.txt").write_text(out, encoding="utf-8")
print(f"{len(chars)} unique CJK chars -> localization/chars.txt")
print("sample:", out[:60])