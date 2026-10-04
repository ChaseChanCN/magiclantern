#!/usr/bin/env python3
"""Extract all CJK characters from source files and regenerate CJK fonts."""
import re
from pathlib import Path

root = Path("..")
chars = set()

for f in list(root.glob("src/*.c")) + list(root.glob("modules/*/*.c")) + list(root.glob("modules/*/README.rst")):
    try:
        text = f.read_text(encoding="utf-8")
    except:
        continue
    for ch in text:
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF or 0x3000 <= cp <= 0x303F or 0xFF00 <= cp <= 0xFFEF:
            chars.add(ch)

chars_str = "".join(sorted(chars))
Path("all_chars.txt").write_text(chars_str, encoding="utf-8")
print(f"Found {len(chars)} unique CJK characters")
print(f"Sample: {chars_str[:100]}")