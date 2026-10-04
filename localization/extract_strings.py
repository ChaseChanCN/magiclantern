import re, glob, sys, json

files = glob.glob('src/*.c') + glob.glob('modules/*/*.c')
strings = {}

# match .name/.help/.help2 = "..." possibly with format args
field_pat = re.compile(r'\.(name|help|help2)\s*=\s*("((?:[^"\\]|\\.)*)")')
# choices: (const char *[]) { "a", "b", ... }
choices_pat = re.compile(r'\.choices\s*=\s*\([^)]*\)\s*\{([^}]*)\}')
str_pat = re.compile(r'"((?:[^"\\]|\\.)*)"')

def add(s, f):
    if not s: return
    if s.startswith('%'): return  # format string only
    if len(s) < 2: return
    strings.setdefault(s, set()).add(f)

for f in files:
    try:
        txt = open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for m in field_pat.finditer(txt):
        add(m.group(3), f)
    for m in choices_pat.finditer(txt):
        for s in str_pat.findall(m.group(1)):
            add(s, f)

print("unique strings:", len(strings))
out = sorted(strings.keys())
for s in out:
    print(s)