import re, glob, collections

files = glob.glob('src/*.c') + glob.glob('modules/*/*.c')
names = collections.Counter()
field_pat = re.compile(r'\.name\s*=\s*"((?:[^"\\]|\\.)*)"')

for f in files:
    try:
        txt = open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for m in field_pat.finditer(txt):
        s = m.group(1)
        if s and not s.startswith('%'):
            names[s] += 1

print("unique .name values:", len(names))
for s, c in names.most_common(120):
    print(f"{c:3d}  {s}")