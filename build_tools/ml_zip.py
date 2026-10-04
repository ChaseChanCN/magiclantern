#!/usr/bin/env python3
"""Create a zip archive with an archive comment, replacing `zip -z ... -r .`.
Usage: python ml_zip.py <output.zip> <comment_file> <source_dir>
Walks source_dir recursively and adds all files to output.zip, storing the
contents of comment_file as the zip archive comment.
"""
import sys, os, zipfile

def main():
    out, comment_file, src_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    comment = b""
    if os.path.exists(comment_file):
        with open(comment_file, "rb") as f:
            comment = f.read().strip()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            dirs.sort()
            for fn in sorted(files):
                full = os.path.join(root, fn)
                arc = os.path.relpath(full, src_dir).replace(os.sep, "/")
                zf.write(full, arc)
        if comment:
            zf.comment = comment
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")

if __name__ == "__main__":
    main()