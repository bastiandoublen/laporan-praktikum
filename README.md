# laporan-praktikum

Skill agent AI (Agent Skills) untuk mengerjakan modul praktikum pemrograman dari dosen sampai menjadi
laporan praktikum `.docx` yang rapi.

Yang dikerjakan skill ini:
- menulis dan menjalankan kode Python per nomor (`NIM_nama.py`, folder `modulN/nomor_K` dan `tugas`);
- screenshot otomatis kode dan output di Antigravity IDE atau VS Code, termasuk potongan baris tertentu;
- program yang memakai `input()` dijalankan dengan jawaban otomatis, aplikasi GUI Tkinter difoto jendelanya;
- menyusun laporan dari template laporan lama (ganti nama dan NIM) dengan struktur A. Tujuan, B. Alat dan Bahan,
  C. Landasan Teori, D. Kegiatan Praktikum, E. Tugas, dan daftar pustaka APA dari jurnal yang dicek ke sumber aslinya;
- aturan format: indent bertingkat, gambar lebar 10 cm dengan border 1 pt, keep with next, daftar isi otomatis.

Jumlah modul bebas: setiap modul baru cukup ditambahkan ke `content.json`, lalu laporan dibangun ulang.

## Pasang

Salin folder repo ini ke folder skill:

```powershell
git clone https://github.com/bastiandoublen/laporan-praktikum
```

Lalu minta agent, misalnya: "kerjakan modul praktikum ini" sambil melampirkan PDF modul dan template laporan.
Panduan lengkap ada di [SKILL.md](SKILL.md), aturan tampilan di [references/format-rules.md](references/format-rules.md),
dan contoh isi laporan (Modul 1–5 PBO) di [assets/contoh-content-pbo.json](assets/contoh-content-pbo.json).

## Kebutuhan

- Windows dengan Microsoft Word (memperbarui daftar isi dan ekspor PDF)
- Antigravity IDE atau VS Code (perintah `code` terpasang)
- Python 3 dengan `python-docx`, `Pillow`, `PyMuPDF`

```powershell
pip install python-docx Pillow PyMuPDF
```

## Catatan

- Selama screenshot berjalan, jangan sentuh keyboard dan mouse, dan nyalakan Do Not Disturb Windows supaya
  notifikasi tidak ikut terfoto.
- Upload kode praktikum ke GitHub tetap dikerjakan sendiri; laporan hanya berisi tempat untuk link GitHub.
- Laporan yang dihasilkan adalah bantuan penyusunan. Pahami kode dan isinya sebelum dikumpulkan.
