# Dipakai shot.ps1 dan ide_palette.ps1: cari editor yang dipakai untuk screenshot.
# Antigravity IDE dan VS Code sama-sama turunan VS Code: perintah palette, shortcut, dan tata letaknya sama.
#   auto        -> Antigravity kalau terpasang, selain itu VS Code
#   antigravity -> %LOCALAPPDATA%\Programs\Antigravity*\bin\antigravity*.cmd, proses Antigravity*
#   vscode      -> code.cmd (user/system install atau PATH), proses Code

function Get-Editor([string]$Pilih = "auto") {
  $daftar = @(
    @{ Kunci = "antigravity"; Nama = "Antigravity IDE"; Proses = "Antigravity*"
       Cli = (Get-ChildItem "$env:LOCALAPPDATA\Programs\Antigravity*\bin\antigravity*.cmd" -ErrorAction SilentlyContinue |
              Select-Object -First 1 -ExpandProperty FullName) },
    @{ Kunci = "vscode"; Nama = "VS Code"; Proses = "Code"
       Cli = (@("$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd", "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd",
                (Get-Command code.cmd -ErrorAction SilentlyContinue).Source) |
              Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1) }
  )
  $cocok = $daftar | Where-Object { ($Pilih -eq "auto" -or $_.Kunci -eq $Pilih) -and $_.Cli } | Select-Object -First 1
  if (-not $cocok) { throw "Editor '$Pilih' tidak ditemukan (Antigravity IDE atau VS Code dengan perintah code.cmd)." }
  $cocok
}

function Get-EditorWindow($Ed, [string]$Judul = "") {
  $jendela = Get-Process | Where-Object { $_.ProcessName -like $Ed.Proses -and $_.MainWindowHandle -ne 0 }
  $p = $jendela | Where-Object { $Judul -and $_.MainWindowTitle -like "*$Judul*" } | Select-Object -First 1
  if (-not $p) { $p = $jendela | Select-Object -First 1 }
  if (-not $p) { throw "$($Ed.Nama) belum terbuka." }
  $p
}
