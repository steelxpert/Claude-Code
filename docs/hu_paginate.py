"""Build a HU note, render it with LibreOffice, and move any heading stranded at a page foot to the next page."""
import os, re, subprocess, sys, zipfile
from pathlib import Path
script, out, extra = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
breaks = []
for it in range(4):
    env = dict(os.environ, HU_BREAK_BEFORE="|".join(breaks))
    subprocess.run([sys.executable, script, "--out", str(out), *extra], check=True, env=env, stdout=subprocess.DEVNULL)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(out)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    pdf = out.with_suffix(".pdf")
    doc = zipfile.ZipFile(out).read("word/document.xml").decode()
    heads = [re.sub(r"<[^>]+>", "", m) for m in re.findall(r'<w:pStyle w:val="Heading\d"/>.*?</w:p>', doc, re.S)]
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    stranded = []
    for pg in text.split("\f"):
        lines = [l.strip() for l in pg.splitlines() if l.strip() and not re.search(r"Oldal: \d+ / \d+", l)]
        if lines:
            last = re.sub(r"\s+", " ", lines[-1])
            stranded += [h for h in heads if re.sub(r"\s+", " ", h) == last and h not in breaks]
    if not stranded:
        print(out.name, "pages ok, breaks:", breaks or "none"); break
    breaks += stranded
else:
    print(out.name, "WARNING: still stranded after 4 passes", stranded)
