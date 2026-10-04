#!/usr/bin/env python3
"""Download + extract the MSYS2 `make` package into a target bin dir.
Needs the `zstandard` Python module (auto-installed via pip).
"""
import sys, os, subprocess, urllib.request, io, tarfile, shutil

URL = "https://repo.msys2.org/msys/x86_64/make-4.4.3-1-x86_64.pkg.tar.zst"
TARGET = sys.argv[1] if len(sys.argv) > 1 else "."

# 1. ensure zstandard
try:
    import zstandard
except ImportError:
    print("installing zstandard...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "zstandard"])
    import zstandard

# 2. download — try several candidate versions (MSYS2 repo churns)
CANDIDATES = [
    "make-4.4.1-3-x86_64.pkg.tar.zst",
    "make-4.4.1-2-x86_64.pkg.tar.zst",
    "make-4.4.2-1-x86_64.pkg.tar.zst",
    "make-4.4.3-1-x86_64.pkg.tar.zst",
]
BASE = "https://repo.msys2.org/msys/x86_64/"
data = None
for pkg in CANDIDATES:
    url = BASE + pkg
    print(f"trying {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ml-build"})
        data = urllib.request.urlopen(req, timeout=60).read()
        print(f"  ok ({len(data)} bytes)")
        break
    except Exception as e:
        print(f"  fail: {e}")
if data is None:
    # last resort: scrape the listing for any make-4.x and try them
    print("scraping repo listing for any make-4.x package...")
    listing = urllib.request.urlopen(BASE, timeout=30).read().decode("utf-8", "replace")
    import re
    for pkg in re.findall(r'make-4\.[0-9]+\.[0-9]+-[0-9]+-x86_64\.pkg\.tar\.zst', listing):
        try:
            req = urllib.request.Request(BASE + pkg, headers={"User-Agent": "ml-build"})
            data = urllib.request.urlopen(req, timeout=60).read()
            print(f"  got {pkg} ({len(data)} bytes)")
            break
        except Exception:
            continue
if data is None:
    sys.exit("ERROR: could not download any make package")

# 3. decompress zst -> tar
dctx = zstandard.ZstdDecompressor()
tar_bytes = dctx.decompress(data, max_output_size=64 * 1024 * 1024)

# 4. extract usr/bin/* to TARGET
count = 0
with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
    for m in tf.getmembers():
        if not m.name.startswith("usr/bin/"):
            continue
        if m.isdir():
            continue
        fname = os.path.basename(m.name)
        if not fname:
            continue
        out = os.path.join(TARGET, fname)
        with tf.extractfile(m) as src, open(out, "wb") as dst:
            shutil.copyfileobj(src, dst)
        count += 1
        print(f"  installed {fname}")
print(f"done: {count} files -> {TARGET}")