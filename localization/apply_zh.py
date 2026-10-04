#!/usr/bin/env python3
"""Apply the EN->ZH dictionary to ML menu strings in src/ and modules/*/.

Replaces string literals only in menu contexts:
  .name = "EN"   .help = "EN"   .help2 = "EN"   menu_add("EN"   .choices{..."EN"...}
Trailing padding inside the quotes is preserved.  Non-UI strings are untouched.
"""
import json, re, glob, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dct = json.loads((ROOT / "localization" / "zh_dict.json").read_text(encoding="utf-8"))
# drop comment keys
trans = {k: v for k, v in dct.items() if not k.startswith("_comment")}
# sort longest first so "White Balance" wins over "White"
keys = sorted(trans.keys(), key=lambda s: -len(s))

files = glob.glob(str(ROOT / "src" / "*.c")) + glob.glob(str(ROOT / "modules" / "*" / "*.c"))

total = 0
per_file = {}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

for f in files:
    p = Path(f)
    txt = p.read_text(encoding="utf-8", errors="replace")
    orig = txt
    nfile = 0

    for en in keys:
        if en not in txt:
            continue
        zh = trans[en]
        en_e = re.escape(en)
        zh_r = zh  # json values are plain unicode

        # 1) .name/.help/.help2 = "EN[padding]"
        for field in ("name", "help", "help2"):
            pat = re.compile(r'(\.' + field + r'\s*=\s*)"' + en_e + r'(\s*)"')
            txt, c = pat.subn(lambda m: m.group(1) + '"' + zh_r + m.group(2) + '"', txt)
            nfile += c

        # 2) menu_add("EN"
        pat = re.compile(r'(menu_add\(\s*)"' + en_e + r'"')
        txt, c = pat.subn(lambda m: m.group(1) + '"' + zh_r + '"', txt)
        nfile += c

        # 3) inside .choices = (const char *[]) { ... }
        def repl_choices(m):
            global nfile
            block = m.group(0)
            inner = re.compile('"' + en_e + r'(\s*)"')
            block2, c = inner.subn(lambda mm: '"' + zh_r + mm.group(1) + '"', block)
            nfile += c
            return block2
        txt = re.sub(r'\.choices\s*=\s*\([^)]*\)\s*\{[^}]*\}', repl_choices, txt)

    if txt != orig:
        p.write_text(txt, encoding="utf-8")
        per_file[str(p.relative_to(ROOT))] = nfile
        total += nfile

# fix the one literal name-lookup in selftest
st = ROOT / "modules" / "selftest" / "selftest.c"
if st.exists():
    t = st.read_text(encoding="utf-8", errors="replace")
    t2 = t.replace('select_menu_by_name("Overlay", "Cropmarks")',
                   'select_menu_by_name("叠加", "裁切标记")')
    if t2 != t:
        st.write_text(t2, encoding="utf-8")
        per_file["modules/selftest/selftest.c (lookup fix)"] = 1
        total += 1

print(f"total replacements: {total}")
print(f"files changed: {len(per_file)}")
for f in sorted(per_file, key=lambda k: -per_file[k])[:25]:
    print(f"  {per_file[f]:4d}  {f}")