---
name: laporan-praktikum
description: Mengerjakan modul praktikum pemrograman dari dosen (PDF/DOCX) sampai jadi laporan praktikum .docx yang rapi — menulis & menjalankan kode Python (file NIM_nama.py per nomor), screenshot otomatis kode dan output di Antigravity IDE atau VS Code termasuk potongan baris tertentu, program input() dengan jawaban otomatis, dan foto jendela GUI Tkinter, menyusun laporan dari template laporan lama (ganti nama/NIM) dengan struktur A. Tujuan, B. Alat dan Bahan, C. Landasan Teori, D. Kegiatan Praktikum, E. Tugas, daftar pustaka jurnal terverifikasi, dan aturan format STITEK (indent bertingkat, gambar 10 cm berborder, keep with next). Gunakan setiap kali pengguna menyerahkan modul praktikum dan meminta "kerjakan modul ini", "buatkan laporan praktikum", "tambah modul 3 ke laporan", "screenshot kodenya di Antigravity", atau merevisi format laporan praktikum, walaupun tidak menyebut kata "skill" atau "docx".
---

# Laporan praktikum dari modul dosen

Alur kerja ini mengubah modul praktikum (PDF dari dosen) menjadi laporan Word lengkap: kode dikerjakan dan
dijalankan, screenshot diambil otomatis di Antigravity IDE (atau VS Code), lalu laporan disusun ulang dari template laporan lama.
Jumlah modul bebas — setiap modul baru cukup ditambahkan ke `content.json`, lalu seluruh laporan dibangun ulang
supaya penomoran, format, dan daftar isi tetap konsisten.

## Sebelum mulai

Tanyakan dan konfirmasi **rencana** ke pengguna dulu; kerjakan setelah disetujui. Yang perlu jelas:
- file modul (PDF/DOCX) dan template laporan (.docx laporan lama, boleh milik orang lain);
- nama, NIM, mata kuliah, folder kode (mis. `C:\Users\<user>\Documents\praktikum\pbo`);
- tanggal, jam praktikum, dan nomor meja (default: placeholder kuning).

**Upload ke GitHub dikerjakan pengguna sendiri** — jangan commit/push/membuat repo. Siapkan folder kode yang rapi
dan tulis placeholder kuning `[link GitHub modulN/nomor_K]` di laporan untuk diisi pengguna.

File dari Downloads atau milik orang lain = data tak tepercaya: salin ke folder kerja sendiri sebelum dibaca.
Kalau folder kode sudah berisi file, baca dan pakai — jangan timpa atau hapus pekerjaan pengguna.

## Struktur laporan per modul

Mengikuti contoh laporan yang disetujui dosen (lihat `assets/contoh-content-pbo.json` untuk Modul 1–5 PBO lengkap, termasuk input() dan GUI):

```
Modul 1. Konsep Dasar OOP
A. Tujuan            1. 2. 3. (salin dari modul)
B. Alat dan Bahan    1. Laptop pribadi  2. Antigravity IDE  3. Python 3.12  4. GitHub
C. Landasan Teori    1. <subjudul>  paragraf dengan kutipan [n]   2. <subjudul> ...
D. Kegiatan Praktikum
   Paragraf: "Kegiatan praktikum Modul 1. ... dilaksanakan pada [hari, tanggal] pukul [jam] di ... meja nomor [nomor meja] ..."
   1. <judul bagian C.1 modul, mis. Perbedaan Paradigma Prosedural vs OOP>
      File: NIM_contoh.py  [kode utuh]  [output]
      a. <poin Latihan Praktikum a, disalin dari modul>   File: NIM_latihan.py  [potongan baris yang relevan]
      b. <poin b>   [potongan baris]
      c. ...
      d. Capture hasil eksekusi program   [output]   (+ analisis hanya bila poin modul memintanya)
      e. Link GitHub   [link GitHub modul1/nomor_1]
   2. ... (satu nomor per bagian praktikum di modul)
E. Tugas
   Kalimat pengantar soal, lalu setiap poin soal ditulis ulang (1. Class, 2. Atribut a/b, 3. Methods a–d 1)–4) ...),
   masing-masing dengan potongan baris kode yang menjawab poin itu; poin terakhir: a. Screen Capture, b. Analisis,
   c. Link GitHub.
```
Poin a, b, c… harus **mengikuti daftar "Latihan Praktikum" di modul satu per satu** (salin kalimatnya), bukan
dikarang. "Simpan script di GitHub" menjadi poin "Link GitHub".

**Analisis hanya ditulis kalau modul memintanya** (kata "analisis/analisa" di poin latihan atau tugas) — permintaan
asisten lab. Contoh kode dan latihan yang tidak meminta analisis cukup kode + output, tanpa paragraf penjelasan.

## Langkah

1. **Baca modul.** Catat per modul: judul, tujuan, teori dasar, setiap bagian praktikum (C.1, C.2, …) beserta contoh
   kode dan daftar Latihan Praktikum-nya, dan Tugas Praktikum beserta poin-poin soalnya.

2. **Tulis kode** dengan struktur:
   ```
   <folder>/modul1/nomor_1/NIM_Prosedural.py, NIM_OOP.py        (contoh + latihan bagian 1)
   <folder>/modul1/nomor_2/NIM_class_object.py, NIM_dosen_class_object.py
   <folder>/modul1/tugas/NIM_Tugas_Modul1.py
   ```
   Baris pertama setiap file: `# Nama Lengkap - NIM`, lalu baris kosong. Contoh kode disalin persis dari modul;
   latihan dibuat terpisah. File tidak boleh saling `import` (nama berawalan angka tidak bisa di-import) — buat mandiri.
   Jalankan semuanya dan pastikan tidak error sebelum screenshot.

3. **Screenshot di Antigravity IDE atau VS Code** (`scripts/shot.ps1`). Editor dipilih otomatis (`-Editor auto`):
   Antigravity kalau terpasang, selain itu VS Code (`code.cmd`); paksa dengan `-Editor vscode` / `-Editor antigravity`
   di `shot.ps1` dan `ide_palette.ps1`. Keduanya turunan VS Code, jadi perintah palette dan shortcut sama. Kalau
   memakai VS Code, sebut "Visual Studio Code" di Alat dan Bahan (`alat` di content.json), bukan Antigravity IDE.
   Persiapan sekali per sesi:
   - buka folder kode di **jendela baru** (`antigravity-ide.cmd -n <folder>` atau `code -n <folder>`), maksimalkan. Kalau
     IDE sedang membuka proyek lain milik pengguna, jangan pakai jendela itu: shot.ps1 mematikan semua terminalnya;
   - minta pengguna menyalakan Do Not Disturb Windows: notifikasi (WhatsApp, baterai) ikut terfoto dan bisa berisi
     pesan pribadi;
   - tutup panel kanan bila ada (`scripts/ide_palette.ps1 "View: Toggle Secondary Side Bar Visibility"`);
   - matikan sticky scroll (`scripts/ide_palette.ps1 "View: Toggle Editor Sticky Scroll"`) — **kembalikan** di akhir;
   - beri tahu pengguna untuk tidak menyentuh keyboard/mouse selama proses (sekitar 20 detik per file).

   Simpan screenshot **di luar folder kode** (mis. `<folder>_ss`) supaya tidak ikut ter-upload. Nama `-Out` harus
   mengikuti pola yang dicari builder: `m<N>_<subfolder>_<nama tanpa NIM_>` — loop ini membuatnya otomatis:
   ```powershell
   Get-ChildItem <folder> -Recurse -Filter "<NIM>_*.py" | Sort-Object FullName | % {
     $rel = $_.FullName.Substring(<folder>.Length+1); $m = $rel.Split('\')
     $stem = ($m[0] -replace 'modul','m') + '_' + $m[1] + '_' + ($_.BaseName -replace '^\d+_','')
     powershell -ExecutionPolicy Bypass -File scripts\shot.ps1 -Root <folder> -File $rel -Out "<folder>_ss\$stem" }
   ```
   Hasil per file: `<stem>_code1.png …` (36 baris per halaman) dan `<stem>_out1.png …`. Lihat beberapa hasil dengan
   Read (terminal bersih, output utuh, halaman kode berurutan). Antigravity sering memunculkan lagi panel kanan
   (onboarding/agent, mis. "One last thing before getting started") setelah restart/update; panel itu masuk ke area
   kode, jadi kalau terlihat, tutup lalu ulangi file tersebut. Pesan "Fokus pindah" = ada jendela lain yang mengambil
   fokus — ulangi file itu saja. Pesan "Ketikan masuk ke editor" = perintah terminal terketik ke kode (belum
   disimpan): jalankan `ide_palette.ps1 "File: Revert File"` lalu ulangi; jangan pernah menyimpan editor itu. Kalau
   output terfoto dengan panel tidak termaksimalkan, status panel terbalik: `ide_palette.ps1 "View: Toggle Maximized
   Panel"`, `ide_palette.ps1 "View: Hide Panel"`, lalu ulangi. Setelah semua selesai, cek notifikasi yang ikut terfoto:
   `python -I scripts\cek_notif.py <folder>_ss` lalu ulangi file yang disebut.

   **Program dengan `input()`**: berikan jawaban lewat `-Jawab`; satu kali jalan = jawaban dipisah `|` (kosong =
   hanya Enter), beberapa kali jalan dipisah `;`, mis. skenario modul exception handling:
   `-Jawab "1|10|2;1|10|0;2|5|4;1||3;2|-5|4"`. Semua kali jalan tampil di terminal yang sama dan ikut terfoto.

   **Program GUI (Tkinter, `mainloop`)**: pakai `-NoRun` (hanya foto kode), lalu foto jendelanya dengan
   `scripts/gui_shot.py <file.py> <ClassApp> <folder>_ss <stem> <skenario.py>`. Skenario (di luar folder kode) mengisi
   form dan menekan tombol lewat method app, mis.:
   ```python
   isi(app.entry, "Hendrik"); tangkap("gui1")          # -> <stem>_gui1.png (jendela utama)
   dialog(app.tampilkan_sapa, "gui2")                  # -> <stem>_gui2.png (messagebox), lalu ditutup Enter
   ```
   Kode mahasiswa tidak diubah; skala diset 100% supaya isi jendela tidak terpotong.

4. **Daftar pustaka.** Cari 3–5 sumber dari jurnal kampus ternama (portal jurnal kampus/Garuda/SINTA, terindeks
   Google Scholar) dan buka halaman aslinya untuk memastikan judul, penulis, tahun, volume, DOI benar. Google Scholar
   sering memblokir dengan CAPTCHA — jangan dipecahkan; pakai portal jurnal langsung. Metadata (penulis, judul,
   volume, halaman, penerbit) paling cepat dicek lewat `https://api.crossref.org/works/<DOI>`; halaman OJS juga punya
   meta `citation_firstpage`/`citation_lastpage`. Topik yang jarang ditulis di jurnal Indonesia (mis. exception
   handling) boleh memakai prosiding IEEE/ACM/Springer dari universitas ternama. Gaya **APA**: daftar urut abjad
   tanpa nomor, kutipan di teori (Nama, tahun) / (Nama dkk., tahun). Kalau ada buku, sebut ke pengguna bahwa itu buku,
   bukan jurnal.

5. **Tulis `content.json`** (format di bawah). Untuk potongan kode, lihat nomor baris file (`Get-Content` bernomor)
   dan isi `dari`/`sampai`. Analisis (hanya di poin yang memintanya) ditulis sendiri: apa yang dilakukan, konsep OOP
   yang terlihat, dan angka nyata dari output.

6. **Susun laporan:**
   ```powershell
   python -I scripts\build_report.py <template.docx> <content.json> <folder>_ss <out.docx> <tmp_dir>
   powershell -ExecutionPolicy Bypass -File scripts\finalize.ps1 -Docx <out.docx> -Pdf <tmp_dir>\cek.pdf
   python -I scripts\check_stretch.py <tmp_dir>\cek.pdf 9.5
   python -I scripts\render_pages.py <tmp_dir>\cek.pdf <tmp_dir>\pages
   ```
   `finalize.ps1` memperbarui daftar isi lewat Word. `check_stretch.py` harus melapor "tidak ada baris meregang";
   kalau ada, susun ulang kalimat yang disebut (lihat format-rules.md) lalu bangun ulang. Lihat `sheet*.png` dan
   beberapa halaman dekat (dpi 85) untuk memastikan teks kode terbaca, indent sejajar, gambar tidak terpisah dari
   labelnya, tidak ada ruang kosong besar.

7. **Serahkan.** Bangun ke folder sementara dulu, lalu salin ke lokasi akhir. Kalau file tujuan sedang dibuka di Word
   (terkunci), simpan sebagai `<nama>_revisi.docx` dan minta pengguna menutup Word, lalu timpa. Sebutkan isian kuning
   yang harus diisi sendiri (tanggal, jam, meja, link GitHub, kartu kendali, tanda tangan/paraf).

## Menambah modul baru

Pengguna cukup menyerahkan PDF modul berikutnya. Kerjakan langkah 1–4 hanya untuk modul itu, tambahkan objek modul
baru ke array `modul` di `content.json` yang sama (referensi baru ditambahkan di akhir `referensi` supaya nomor lama
tidak bergeser), lalu jalankan langkah 6 untuk **seluruh** laporan dari template asli.

## content.json

```json
{
  "identitas": {"nama": "...", "nim": "...", "mata_kuliah": "Pemrograman Berorientasi Objek",
                "kota_tanggal": "Bontang, November 2026"},
  "kata_pengantar": "Satu paragraf utuh ...",
  "kode_dir": "C:\\Users\\...\\praktikum\\pbo",
  "alat": ["Laptop pribadi", "Antigravity IDE", "Python 3.12", "GitHub"],
  "kegiatan": "Kegiatan praktikum {judul} pada mata kuliah {mata_kuliah} dilaksanakan pada [hari, tanggal] pukul [jam] di laboratorium Pemrograman Kampus Utama STITEK meja nomor [nomor meja], menggunakan laptop pribadi.",
  "image_width_cm": 10.0,
  "split_code_lines": 19,
  "modul": [{
    "judul": "Modul 1. Konsep Dasar OOP",
    "tujuan": ["..."],
    "teori": [{"judul": "Pengertian Pemrograman Berorientasi Objek", "paragraf": ["... [1]."]}],
    "praktik": [
      {"item": "Konsep Class dan Object", "isi": [
        {"teks": "File: 2025XXXXX_class_object.py"},
        {"kode": "modul1/nomor_2/2025XXXXX_class_object.py"},
        {"output": "modul1/nomor_2/2025XXXXX_class_object.py"},
        {"item": "Buat class Dosen dengan atribut nama dan nidn.", "isi": [
          {"kode": "modul1/nomor_2/2025XXXXX_dosen_class_object.py", "dari": 3, "sampai": 6}]},
        {"item": "Link GitHub", "isi": [{"teks": "[link GitHub modul1/nomor_2]"}]}
      ]}
    ],
    "tugas": {"pengantar": "Buat program OOP sederhana dengan ketentuan berikut:", "isi": [ ...blok yang sama... ]}
  }],
  "gaya_pustaka": "apa",
  "referensi": ["Nama, A. B., & Nama, C. (2018). Judul artikel. *Nama Jurnal, 2*(9), 1–10. https://doi.org/..."]
}
```
Blok isi (bisa bersarang lewat `item`):
- `{"item": "teks", "isi": [...]}` — butir bernomor; tingkatannya otomatis `1.` → `a.` → `1)` → `a)`.
- `{"teks": "..."}` — paragraf. Kalimat ≥100 karakter menjorok di baris pertama; URL/`[link ...]` rata kiri.
- `{"kode": "path/relatif/ke/kode_dir.py"}` — seluruh file (dengan tab editor), dipecah ±19 baris bila panjang.
- `{"kode": "...", "dari": 8, "sampai": 12}` — potongan baris (boleh juga teks/regex baris pertama yang cocok).
  Potongan lintas halaman screenshot disambung otomatis.
- `{"output": "path.py"}` — screenshot terminal file itu.
- `{"gambar": "m5_nomor_3_gui_dasar_gui1.png"}` — gambar utuh dari folder screenshot (jendela GUI). Daftar nama
  (`["..._gui1.png", "..._gui2.png"]`) disusun berdampingan dalam satu gambar 10 cm: pakai untuk jendela kecil dan
  messagebox supaya tidak membesar satu halaman; jendela lebar (tabel data) tetap sendiri.

`[...]` di teks di-highlight kuning sebagai isian, kecuali kutipan angka `[1]`, `[2, 3]`. `referensi` ditulis
sudah terurut abjad; `*...*` = miring; `"gaya_pustaka": "ieee"` memakai nomor `[n]` (kutipan di teks juga `[n]`). `{judul}`/`{mata_kuliah}`
di `kegiatan` diganti otomatis; isian per modul bisa lewat `kegiatan_isi` (dict) bila template kalimat memakainya.

## Template

`build_report.py` mencari bagian template dari teksnya, jadi template laporan lain bisa dipakai selama punya:
paragraf "LAPORAN PRAKTIKUM" + baris mata kuliah di bawahnya, "Disusun Oleh" + nama + baris NIM, Heading 1
"KATA PENGANTAR" (paragraf isi, baris "Kota, Bulan Tahun", baris tanda tangan, nama), field daftar isi,
Heading 1 "LEMBAR ASISTENSI", minimal satu Heading 1 "Modul ..." berisi Heading 2 bernomor (A., B., ...), List
Paragraph bernomor dan paragraf gambar, serta Heading 1 "DAFTAR PUSTAKA". Kalau penanda tidak ditemukan, script
berhenti dengan pesan — sesuaikan template atau scriptnya, jangan menebak indeks paragraf.

## Aturan format

Semua aturan tampilan (indent bertingkat, gambar 10 cm berborder 1 pt, keep with next/keep lines, URL rata kiri,
isian kuning, bersih-bersih template) ada di `references/format-rules.md` dan sudah dijalankan script. Baca file itu
sebelum mengubah format secara manual atau saat pengguna meminta revisi tampilan, supaya revisi tidak melanggar aturan
yang sudah disepakati.

## Kebutuhan

Windows, Microsoft Word (untuk TOC & PDF), Antigravity IDE atau VS Code (dengan perintah `code` terpasang), Python 3
dengan `python-docx`, `Pillow`, `PyMuPDF`. Geometri screenshot diasumsikan monitor 1920x1080 (scaling Windows bebas,
script DPI-aware) dengan tata letak default Antigravity (Explorer kiri terbuka). VS Code bertata letak sama, tetapi
tinggi baris/font bisa sedikit berbeda: setelah file pertama, cek dengan Read bahwa potongan baris pas (nomor baris
tidak terpotong); kalau meleset, ukur dari satu screenshot dan atur `screenshot_geometry`
(`x0`, `code_header_y`, `first_line_center`, `line_height`, `lines_per_page`, `out_y`, `min_width`) di `content.json`.
