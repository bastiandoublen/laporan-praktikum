# Finalisasi lewat Microsoft Word: update daftar isi (TOC), simpan, ekspor PDF untuk dicek.
# Pakai: powershell -ExecutionPolicy Bypass -File finalize.ps1 -Docx C:\...\laporan.docx [-Pdf C:\...\cek.pdf]
param([Parameter(Mandatory)][string]$Docx, [string]$Pdf)
try { [IO.File]::Open($Docx, 'Open', 'ReadWrite', 'None').Close() } catch { throw "File sedang dibuka di Word, tutup dulu: $Docx" }
$w = New-Object -ComObject Word.Application; $w.Visible = $false
try {
  $doc = $w.Documents.Open($Docx)
  foreach ($t in $doc.TablesOfContents) { $t.Update() }
  $doc.Save()
  if ($Pdf) { $doc.ExportAsFixedFormat($Pdf, 17) }
  $n = $doc.ComputeStatistics(2)
  $doc.Close()
} finally { $w.Quit() }
"pages=$n"
