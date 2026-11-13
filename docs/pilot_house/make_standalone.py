#!/usr/bin/env python3
"""Build an offline, self-contained copy of a pilot-house viewer HTML.

Usage: make_standalone.py <input.html> <output.html> <three.min.js> <OrbitControls.js>

Replaces the <script src="...three.min.js"> and <script src="...OrbitControls.js">
tags by inline <script> blocks with the library source, and inserts a comment at
the top. Refuses to overwrite the input file.
"""
import os, re, sys

COMMENT = ("<!-- Self-contained copy of the pilot-house concept viewer (viewer v33 = "
           "artifact version 33; three.js r128 + OrbitControls inlined) for offline use; "
           "built 2026-11-13 -->\n")

def inline(html, pattern, path):
    with open(path, encoding="utf-8", newline="") as f:
        code = f.read().replace("</script", "<\\/script")
    rx = re.compile(r'<script\b[^>]*\bsrc="[^"]*' + pattern + r'[^"]*"[^>]*>\s*</script>', re.I)
    html, n = rx.subn(lambda m: "<script>\n" + code + "\n</script>", html)
    if n != 1:
        sys.exit("expected exactly 1 script tag matching %s, found %d" % (pattern, n))
    return html

def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    src, dst, three, orbit = sys.argv[1:]
    if os.path.exists(dst) and os.path.samefile(src, dst):
        sys.exit("refusing to overwrite input file")
    with open(src, encoding="utf-8", newline="") as f:
        html = f.read()
    html = inline(html, r"three\.min\.js", three)
    html = inline(html, r"OrbitControls\.js", orbit)
    html = COMMENT + html
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))

main()
