"""Foto jendela aplikasi Tkinter mahasiswa tanpa mengubah kodenya.

    python gui_shot.py <file.py> <NamaClassApp> <folder_out> <prefix> <skenario.py>

File dimuat tanpa blok __main__, lalu root = tk.Tk(), app = NamaClassApp(root). Skenario adalah kode Python
yang dijalankan dengan nama: app, root, tk, isi(entry, teks), tangkap(nama), dialog(fungsi, nama|None).
- tangkap(nama)         -> <folder_out>/<prefix>_<nama>.png (jendela utama, termasuk judul)
- dialog(fungsi, nama)  -> jalankan fungsi yang membuka messagebox, foto dialognya, lalu tutup
                           dialog dengan Enter. nama=None: dialog hanya ditutup.
Jangan sentuh keyboard/mouse selama berjalan (Enter dikirim ke jendela aktif).
"""
import ctypes, ctypes.wintypes as wt, os, runpy, sys, time
ctypes.windll.shcore.SetProcessDpiAwareness(2)   # koordinat piksel asli
import tkinter as tk
from PIL import ImageGrab

path, kelas, folder, prefix, skenario = sys.argv[1:6]
os.makedirs(folder, exist_ok=True)
os.chdir(os.path.dirname(os.path.abspath(skenario)))   # file keluaran aplikasi (ekspor) tidak masuk folder kode
ns = runpy.run_path(path, run_name='gui_shot')
root = tk.Tk()
# skala 100%: ukuran geometry() di kode (piksel) dan font tetap sebanding seperti di layar biasa,
# kalau tidak, font ikut membesar (DPI aware) dan isi jendela terpotong
root.tk.call('tk', 'scaling', 96 / 72)
app = ns[kelas](root)
root.attributes('-topmost', True)
u32, dwm = ctypes.windll.user32, ctypes.windll.dwmapi

def kotak(hwnd):
    r = wt.RECT()   # batas jendela tanpa bayangan
    dwm.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(r), ctypes.sizeof(r))
    return r.left, r.top, r.right, r.bottom

def tanpa_bingkai(hwnd):
    # Windows 11: sudut membulat (latar belakang ikut terfoto di pojok) dan garis bingkai 1 px abu-abu.
    # Keduanya menempel ke border 1 pt di Word sehingga tepi tampak tebal/kotor -> sudut siku, tanpa garis bingkai
    dwm.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(ctypes.c_int(1)), 4)            # DWMWCP_DONOTROUND
    dwm.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(ctypes.c_uint(0xFFFFFFFE)), 4)  # DWMWA_COLOR_NONE

def utama():
    return u32.GetParent(root.winfo_id()) or int(root.wm_frame(), 16)

def simpan(bbox, nama):
    p = os.path.join(folder, f'{prefix}_{nama}.png')
    l, t, r, b = bbox   # tanpa garis bingkai, 1 px kiri/kanan/bawah batas DWM berisi latar di belakang jendela
    ImageGrab.grab(bbox=(l + 1, t, r - 1, b - 1), all_screens=True).save(p)
    print('ok', p)

def isi(entry, teks):
    entry.delete(0, tk.END)
    entry.insert(0, teks)

def tangkap(nama):
    tanpa_bingkai(utama())
    root.update(); time.sleep(0.5); root.update()
    simpan(kotak(utama()), nama)

def dialog(fungsi, nama):
    def foto():
        h = u32.GetForegroundWindow()
        if nama and h != utama():
            tanpa_bingkai(h); time.sleep(0.4)
            simpan(kotak(h), nama)   # dialog saja: posisinya di tengah layar, bukan di atas jendela utama
        u32.keybd_event(0x0D, 0, 0, 0); u32.keybd_event(0x0D, 0, 2, 0)
    root.update()
    root.after(1200, foto)
    fungsi()
    root.update()

root.update(); time.sleep(0.8)
exec(open(skenario, encoding='utf-8-sig').read(), {'app': app, 'root': root, 'tk': tk, 'isi': isi,
                                                'tangkap': tangkap, 'dialog': dialog})
root.destroy()
