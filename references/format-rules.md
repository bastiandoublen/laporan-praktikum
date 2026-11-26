# Aturan format laporan

Semua aturan ini sudah dijalankan oleh `scripts/build_report.py`. Baca file ini kalau harus mengedit docx secara
manual, menambah jenis bagian baru, atau pengguna mengeluhkan tampilan. Setiap aturan berasal dari koreksi pengguna,
jadi alasannya ikut ditulis supaya tidak "diperbaiki" balik.

Satuan: twip (1/20 pt). 360 twip = 18 pt = 0,635 cm.

## Indentasi bertingkat (paling sering dikoreksi)

Prinsipnya: setiap penanda (huruf/nomor) berada tepat di bawah **teks** tingkat di atasnya, bukan di bawah penandanya.
Tidak boleh ada ruang kosong di kiri huruf heading.

| Elemen | Posisi penanda | Posisi teks |
|---|---|---|
| Heading 2 `A.`–`E.` (Tujuan, Alat dan Bahan, Landasan Teori, Kegiatan Praktikum, Tugas) | 0 (mentok kiri) | 360 |
| Paragraf langsung di bawah heading (kegiatan, pengantar tugas) | – | 360, baris pertama menjorok +360 |
| Tingkat 1 `1.` (tujuan, alat, subjudul teori, nomor praktikum, poin tugas) | 360 | 720 |
| Tingkat 2 `a.` | 720 | 1080 |
| Tingkat 3 `1)` | 1080 | 1440 |
| Tingkat 4 `a)` | 1440 | 1800 |
| Gambar, "File: ...", paragraf analisis, link di bawah sebuah butir | – | posisi teks butir itu |
| Daftar pustaka (APA) | baris 1 di 0 | baris berikutnya 720 (Ctrl+T), rata kiri-kanan (Ctrl+J) |

- Heading Modul (Heading 1) rata tengah, mengikuti style template.
- Struktur per modul: A. Tujuan, B. Alat dan Bahan, C. Landasan Teori (subjudul bernomor), D. Kegiatan Praktikum
  (paragraf pelaksanaan lalu langsung nomor 1., 2., … per bagian praktikum), E. Tugas. Tidak ada bagian
  "Langkah-Langkah Praktikum" atau nomor induk "Kerjakan semua contoh program...".
- Penomoran mulai ulang di setiap daftar dan setiap modul (startOverride untuk semua level).
- Paragraf ≥100 karakter menjorok di baris pertama; label pendek ("File: ...", link) tidak.

## Gambar

- Lebar **tepat 10 cm** untuk semua gambar — tidak lebih, tidak kurang. Jangan mengecilkan gambar agar muat
  di halaman; pengguna memilih lebar seragam.
- Border hitam 1 pt di setiap gambar (`a:ln w=12700`, warna tema `schemeClr tx1` = "Black, Text 1" supaya tersorot
  di menu Picture Border Word). Wajib `wp:effectExtent` 6350 di keempat sisi: garis digambar separuh di luar gambar,
  tanpa ruang itu sisi atas/kanan terpotong dan tampak abu-abu tipis.
- Tepi gambar sendiri tidak boleh gelap/berbingkai (bingkai jendela Windows, sudut membulat, latar di belakang):
  menempel ke border sehingga sisi itu tampak tebal. `gui_shot.py` mematikan sudut bulat dan garis bingkai jendela
  lalu memotong 1 px kiri/kanan/bawah; screenshot lain cek dengan Read sebelum dipakai.
- Screenshot kode utuh: area editor dengan tab + breadcrumb; potongan baris (`dari`/`sampai`): hanya baris itu
  lengkap dengan nomor barisnya. Output: area terminal. Ruang hitam kosong di kanan/bawah dipangkas, tetapi lebar
  crop minimal 700 px — crop selebar 1000+ px membuat huruf kode terlalu kecil setelah dijadikan 10 cm.
- Kode utuh yang panjang dipecah jadi potongan seimbang ±19 baris (tidak dipecah bila hanya lebih ≤6 baris, supaya
  tidak ada potongan berisi 1 baris), tepat di batas baris, supaya potongan bisa mengisi sisa halaman.

## Pemisahan halaman

- Semua butir bernomor dan paragraf yang tepat berada di atas gambar ("File: ...") memakai **keep with next**,
  jadi label selalu satu halaman dengan gambar/teks di bawahnya.
- Semua paragraf isi memakai **keep lines together**: paragraf tidak terbelah, utuh pindah ke halaman berikutnya.
- Jangan pasang keep with next pada paragraf gambar atau teks biasa. Kalau dipasang, gambar akan mengunci satu sama
  lain dan pindah halaman bergerombol.
- Setiap modul baru dan DAFTAR PUSTAKA dimulai di halaman baru (page break).

## Judul & daftar isi

- Judul bagian A.–E. tebal melalui style Heading 2 (bukan format langsung pada teks), supaya entri daftar isi tidak
  ikut tebal — format langsung terbawa ke TOC saat diperbarui.
- Style daftar isi tingkat 2 (`toc 2`): tab teks diletakkan 360 setelah indent kirinya, jadi "A. Tujuan" rapat
  seperti di isi laporan; tab nomor halaman disamakan dengan `toc 1`. Template lama memakai tab 851 yang membuat
  jarak huruf–judul terlalu lebar.

## Teks

- Paragraf rata kiri-kanan (justify), kecuali paragraf yang berisi URL: rata kiri, karena URL panjang tidak bisa
  dipotong sehingga spasi antarkata meregang.
- **Tidak boleh ada baris meregang** (jarak antarkata berlebihan). Setelah menyusun, jalankan
  `scripts/check_stretch.py <pdf> 9.5` — harus "tidak ada baris meregang". Penyebabnya kata panjang yang tak bisa
  dipotong jatuh di awal baris berikutnya:
  - "kata/kata" (Programming/OOP) dan DOI/URL: script menyisipkan titik potong tak terlihat (U+200B) setelah "/".
  - nama ber-underscore (`_maks_pinjam`, `daftar_peminjaman`, `mhs1.__ipk`): JANGAN dipotong (jadi "daftar_ /
    peminjaman"); susun ulang kalimatnya (mis. tambah kata "atribut"/"method" di depan nama, pecah jadi dua kalimat),
    bangun ulang, cek lagi sampai bersih.
  - butir bernomor (instruksi dari modul) dibuat rata kiri karena pendek dan sering berisi nama method.
- Daftar pustaka gaya APA: urut abjad nama belakang penulis pertama, tanpa nomor; judul buku / nama jurnal + volume
  dicetak miring (`*...*` di content.json); jurnal tanpa DOI cukup tanpa URL. Kutipan di teks: (Nama, tahun),
  3 penulis atau lebih → (Nama dkk., tahun), dua penulis → (Nama & Nama, tahun).
- Garis merah/biru cek ejaan dan tata bahasa Word disembunyikan untuk seluruh dokumen
  (`hideSpellingErrors`, `hideGrammaticalErrors` di settings) — laporan berbahasa campuran Indonesia–Inggris
  selalu penuh garis.
- Isian yang harus diisi mahasiswa ditulis dalam kurung siku dan di-highlight kuning: `[hari, tanggal]`,
  `[nomor meja]`, `[Tempel foto kartu kendali praktikum di sini]`.
- Kata Pengantar: tidak ada baris kosong antara judul dan paragraf pertama. Baris tanggal ("Bontang, November 2026"),
  baris tanda tangan, dan nama memakai format yang sama (rata tengah dalam blok kanan).

## Bersih-bersih dari template orang lain

- Hapus tanda tangan dan foto kartu kendali pemilik template; jangan ikut terbawa.
- Bibliografi lama (field CITATION/sdt) diganti daftar pustaka teks biasa `[1] ...`.
- Gambar yang tidak dipakai lagi dibuang dari paket docx (relasi yatim), supaya file tidak membengkak.
- Metadata (author, last modified by) diganti nama mahasiswa.
