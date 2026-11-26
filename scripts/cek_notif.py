"""Cari notifikasi Windows (toast WhatsApp, baterai, dll.) yang ikut terfoto di pojok kanan bawah screenshot IDE.

    python -I cek_notif.py <folder_screenshot>

Tema IDE gelap; kotak notifikasi terang. File yang disebut perlu difoto ulang (toast di bawah output terminal
terpotong saat crop, tetapi di halaman kode menutupi baris).
"""
import glob, os, sys
from PIL import Image

kena = 0
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*_code*.png')) + glob.glob(os.path.join(sys.argv[1], '*_out*.png'))):
    im = Image.open(f).convert('L')
    w, h = im.size
    px = im.crop((w - 480, h - 300, w - 20, h - 30)).tobytes()
    terang = sum(1 for p in px if p > 200) / len(px)
    if terang > 0.15:
        kena += 1
        print(f'{os.path.basename(f)}  ({terang:.0%} terang di pojok kanan bawah)')
print('tidak ada notifikasi' if not kena else f'{kena} gambar perlu dicek/difoto ulang')
