"""Render PDF jadi PNG + lembar kontak 4 kolom untuk cek tata letak secara visual.

python -I render_pages.py <laporan.pdf> <out_dir> [dpi=60] [halaman_mulai=1]
Hasil: out_dir/p<N>.png dan out_dir/sheet<K>.png (16 halaman per lembar).
"""
import sys, os
import pymupdf
from PIL import Image

pdf, out = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 60
start = int(sys.argv[4]) if len(sys.argv) > 4 else 1
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(pdf)
files = []
for n in range(start, len(doc) + 1):
    f = os.path.join(out, f'p{n}.png'); doc[n - 1].get_pixmap(dpi=dpi).save(f); files.append(f)
for k in range(0, len(files), 16):
    ims = [Image.open(f) for f in files[k:k + 16]]
    w, h = ims[0].size
    sheet = Image.new('RGB', (w * 4, h * ((len(ims) + 3) // 4)), 'white')
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 4) * w, (i // 4) * h))
    sheet.save(os.path.join(out, f'sheet{k // 16 + 1}.png'))
print(len(doc), 'halaman ->', out)
