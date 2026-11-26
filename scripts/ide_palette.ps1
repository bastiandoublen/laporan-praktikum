# Jalankan perintah Command Palette di editor yang sedang terbuka (Antigravity IDE atau VS Code).
# Persiapan sebelum shot.ps1 (lalu kembalikan setelah selesai):
#   ide_palette.ps1 "View: Toggle Editor Sticky Scroll"            # matikan sticky scroll (toggle)
#   ide_palette.ps1 "View: Toggle Secondary Side Bar Visibility"   # tutup panel kanan bila terbuka
#   ide_palette.ps1 "File: Revert File" -Editor vscode             # pilih editor; default auto (Antigravity dulu)
param(
  [Parameter(Mandatory)][string]$Command,
  [ValidateSet("auto", "antigravity", "vscode")][string]$Editor = "auto"
)
. (Join-Path $PSScriptRoot "editor.ps1")
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System; using System.Runtime.InteropServices;
public class WP { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, int f, int e); [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow(); }
"@
$ed = Get-Editor $Editor
$p = Get-EditorWindow $ed
[WP]::keybd_event(0x12, 0, 0, 0); [WP]::keybd_event(0x12, 0, 2, 0); [WP]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep 1
# tombol dikirim ke jendela aktif: kalau bukan editor (mis. jendela chat), perintah bisa terketik di aplikasi lain
if ([WP]::GetForegroundWindow() -ne $p.MainWindowHandle) { throw "$($ed.Nama) tidak di depan; '$Command' tidak dikirim. Ulangi tanpa menyentuh PC." }
foreach ($k in "^1", "^+p", $Command, "{ENTER}") { [System.Windows.Forms.SendKeys]::SendWait($k); Start-Sleep -Milliseconds 700 }
"done: $Command ($($ed.Nama))"
