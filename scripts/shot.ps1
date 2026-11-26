# Screenshot otomatis di Antigravity IDE (fork VS Code) atau VS Code untuk satu file Python:
#   <Out>_out1.png ...  : terminal IDE (panel dimaksimalkan) setelah `python <file>` dijalankan
#   <Out>_code1.png ... : editor (panel tertutup), satu gambar per <PerPage> baris
# Pakai (dari PowerShell biasa, JANGAN sentuh keyboard/mouse selama jalan):
#   powershell -ExecutionPolicy Bypass -File shot.ps1 -Root C:\...\pbo -File modul2\relasi.py -Out ss\m2_relasi
# Syarat: folder -Root sudah terbuka di editor (-Editor auto: Antigravity kalau terpasang, selain itu VS Code),
#         jendela di monitor utama 1920x1080 (skala 100%),
#         panel kanan (agent/secondary side bar) tertutup, sticky scroll editor dimatikan (lihat ide_palette.ps1).
param(
  [Parameter(Mandatory)][string]$Root,
  [Parameter(Mandatory)][string]$File,
  [Parameter(Mandatory)][string]$Out,
  [int]$Wait = 3,          # detik menunggu program selesai
  [int]$PerPage = 36,      # baris kode per screenshot (editor 1080p menampilkan ~37 baris)
  [int]$RowsPerOut = 41,   # baris terminal yang muat saat panel dimaksimalkan
  [string]$Python = "python",
  # program yang memakai input(): satu string per kali jalan, jawaban dipisah "|" (kosong = hanya Enter),
  # mis. -Jawab "1|10|2;1|10|0"  -> program dijalankan dua kali dengan jawaban itu
  [string[]]$Jawab = @(),
  # program GUI (mainloop): hanya screenshot kode; jendela GUI difoto terpisah (gui_shot.py)
  [switch]$NoRun,
  [ValidateSet("auto", "antigravity", "vscode")][string]$Editor = "auto"
)
. (Join-Path $PSScriptRoot "editor.ps1")
$ed = Get-Editor $Editor
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, int f, int e);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  public struct RECT { public int L, T, R, B; }
}
"@
[W]::SetProcessDPIAware() | Out-Null   # tangkapan resolusi penuh, bukan versi terskala
$full = Join-Path $Root $File
$dir = Split-Path $full; $name = Split-Path $full -Leaf
$outBase = if ([IO.Path]::IsPathRooted($Out)) { $Out } else { Join-Path $Root $Out }
New-Item -ItemType Directory -Force (Split-Path $outBase) | Out-Null

function Keys($k, $ms = 400) { [System.Windows.Forms.SendKeys]::SendWait($k); Start-Sleep -Milliseconds $ms }
function Palette($cmd) { Keys "^+p" 600; Keys $cmd 600; Keys "{ENTER}" 800 }
function Grab($h, $path) {
  # tombol dikirim ke jendela aktif; kalau fokus pindah (notifikasi, klik pengguna) hasilnya salah -> berhenti
  if ([W]::GetForegroundWindow() -ne $h) { throw "Fokus pindah dari $($ed.Nama) sebelum $path. Ulangi file ini tanpa menyentuh PC." }
  # judul berakhiran titik = editor berubah: ketikan untuk terminal masuk ke kode. Jangan simpan; File: Revert File
  if ((Get-Process -Id $p.Id).MainWindowTitle -match '●') { throw "Ketikan masuk ke editor $name (belum disimpan). Jalankan ide_palette.ps1 'File: Revert File' lalu ulangi." }
  $r = New-Object W+RECT; [W]::GetWindowRect($h, [ref]$r) | Out-Null
  $wa = [System.Windows.Forms.Screen]::FromHandle($h).WorkingArea
  $x = [Math]::Max($r.L, $wa.Left); $y = [Math]::Max($r.T, $wa.Top)
  $w = [Math]::Min($r.R, $wa.Right) - $x; $hh = [Math]::Min($r.B, $wa.Bottom) - $y
  $bmp = New-Object System.Drawing.Bitmap $w, $hh
  $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($x, $y, 0, 0, $bmp.Size); $g.Dispose()
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
}

& $ed.Cli -r $full | Out-Null
Start-Sleep 2
$p = Get-EditorWindow $ed $name
$h = $p.MainWindowHandle
[W]::ShowWindow($h, 3) | Out-Null
[W]::keybd_event(0x12, 0, 0, 0); [W]::keybd_event(0x12, 0, 2, 0)   # tap Alt agar SetForegroundWindow diizinkan
[W]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 500
$wr = New-Object W+RECT; [W]::GetWindowRect($h, [ref]$wr) | Out-Null
# parkir kursor di judul jendela (tengah, kiri dari tombol layout): tidak memunculkan tooltip di editor/terminal
[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(([int](($wr.L + $wr.R) / 2) - 250), ($wr.T + 20))
Start-Sleep 1

# 1. Terminal baru yang bersih, panel dimaksimalkan, jalankan program
$outPages = 0
if (-not $NoRun) {
Keys "^1"
Palette "Terminal: Kill All Terminals"
Keys "^1"
Keys "^``" 4000
Palette "View: Toggle Maximized Panel"
Set-Clipboard "cd $dir; cls"; Keys "^v" 500; Keys "{ENTER}" 1500   # tempel, bukan ketik: ketikan panjang bisa terpotong
$OutputEncoding = New-Object System.Text.UTF8Encoding $false     # pipa ke python tanpa BOM
$outLines = 1
$Jawab = @($Jawab | ForEach-Object { $_ -split ';' })   # lewat -File: beberapa kali jalan ditulis "1|10|2;1|10|0"
$runs = if ($Jawab.Count) { $Jawab } else { ,"<tanpa-input>" }
foreach ($run in $runs) {
  Set-Clipboard "$Python $name"; Keys "^v" 500
  if ($run -eq "<tanpa-input>") {
    Keys "{ENTER}" ($Wait * 1000)
    Push-Location $dir; $outLines += @(& $Python $name).Count + 1; Pop-Location
    continue
  }
  Keys "{ENTER}" 1500
  $isi = $run.Split('|')
  foreach ($j in $isi) {
    if ($j -ne "") { Set-Clipboard $j; Keys "^v" 300 }
    Keys "{ENTER}" 800
  }
  Start-Sleep 1
  # baris di terminal = keluaran (prompt dan jawaban satu baris) + satu baris per jawaban + baris perintah
  Push-Location $dir; $outLines += @(($isi -join "`n") | & $Python $name).Count + $isi.Count + 1; Pop-Location
}
$outPages = [Math]::Ceiling($outLines / $RowsPerOut)
if ($outPages -gt 1) { Palette "Terminal: Scroll to Top" }
for ($i = 1; $i -le $outPages; $i++) {
  if ($i -gt 1) { Keys "+{PGDN}" 800 }
  Grab $h "${outBase}_out$i.png"
}
Keys "^``" 300; Keys "^``" 800   # fokus balik ke terminal sebelum un-maximize
Palette "View: Toggle Maximized Panel"
Keys "^j"
}

# 2. Panel tertutup, ambil kode per halaman
Keys "^1"
Keys "^{HOME}"
$lines = (Get-Content $full).Count
$pages = [Math]::Max(1, [Math]::Ceiling($lines / $PerPage))
for ($i = 1; $i -le $pages; $i++) {
  if ($i -gt 1) { Keys "^{DOWN $PerPage}" 800 }   # scroll baris (PageDown hanya memindah kursor)
  Grab $h "${outBase}_code$i.png"
}
"ok $Out lines=$lines code_pages=$pages out_pages=$outPages"
