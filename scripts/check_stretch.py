"""Cari baris rata kiri-kanan yang meregang (jarak antarkata berlebihan) di PDF laporan.

python -I check_stretch.py <laporan.pdf> [batas_pt=9]
Mencetak halaman + isi baris yang jarak antarkatanya melebihi batas. Kosong = aman.
Penyebab umum & perbaikan: kata panjang tak terpotong (nama_ber_underscore, kata/kata, URL, DOI) -> build_report.py
sudah menyisipkan titik potong; kalau masih ada, ubah kalimatnya atau beri titik potong manual.
"""
import sys, re
import pymupdf

pdf = pymupdf.open(sys.argv[1])
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 9.0
found = 0
for pno, page in enumerate(pdf, 1):
    words = page.get_text('words')   # x0, y0, x1, y1, word, block, line, wno
    lines = {}
    for w in words:   # kelompokkan per posisi vertikal: jarak lebar membuat PyMuPDF memecah satu baris jadi beberapa
        lines.setdefault(round(w[3] / 3), []).append(w)
    right = max((w[2] for w in words), default=0)
    for key, ws in lines.items():
        ws.sort(key=lambda w: w[0])
        if len(ws) < 2 or ws[-1][2] < right - 6:   # baris terakhir paragraf / tidak penuh: wajar renggang
            continue
        gaps = [b[0] - a[2] for a, b in zip(ws, ws[1:])]
        if re.fullmatch(r'\(?[0-9a-zA-Z]{1,3}[.)]|\[\d+\]', ws[0][4]):
            gaps = gaps[1:]          # jarak penanda daftar (a., 1), [1]) ke teks = tab, bukan regangan
        if not gaps: continue
        if max(gaps) > limit:
            found += 1
            print(f'hal {pno}: jarak {max(gaps):.1f}pt | ' + ' '.join(w[4] for w in ws)[:110])
print(f'{found} baris meregang' if found else 'tidak ada baris meregang')
