#!/usr/bin/env python3
"""Find all remaining untranslated .help and .help2 strings in source files."""
import re, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = glob.glob(str(ROOT / "src" / "*.c")) + glob.glob(str(ROOT / "modules" / "*" / "*.c"))

results = {}
for f in files:
    try:
        txt = Path(f).read_text(encoding="utf-8")
    except:
        continue
    
    for field in ("help", "help2"):
        for m in re.finditer(r'\.' + field + r'\s*=\s*"([^"]*)"', txt):
            s = m.group(1).strip()
            if not s:
                continue
            # Check if it's English (starts with ASCII letter)
            if s and ord(s[0]) < 128 and s[0].isalpha():
                if s not in results:
                    results[s] = []
                rel = str(Path(f).relative_to(ROOT))
                if rel not in results[s]:
                    results[s].append(rel)

# Print sorted by frequency
for s in sorted(results.keys()):
    files_list = results[s]
    print(f"[{len(files_list)}] {s[:120]}")

print(f"\nTotal unique untranslated help strings: {len(results)}")