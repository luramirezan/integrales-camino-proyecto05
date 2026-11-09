# Descarga los PDF de acceso abierto (arXiv) de fase2/fuentes_control/fuentes_control.md.
# Uso en PowerShell, desde la carpeta donde quieras guardarlos:
#   powershell -ExecutionPolicy Bypass -File .\descargar_fuentes.ps1
# Los artículos de APS (Phys. Rev.) no son de acceso abierto: bájalos con el acceso de la universidad (proxy de biblioteca).
$dest = Join-Path (Get-Location) "pdf_fuentes_control"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$pdfs = [ordered]@{
  "H8_Gonul2000_Hulthen_SUSY.pdf"            = "https://arxiv.org/pdf/nucl-th/0106002"
  "H9_Roy_GPS_Hulthen_Yukawa.pdf"            = "https://arxiv.org/pdf/1312.5900"
  "H10_Roy_Hulthen_confinado.pdf"            = "https://arxiv.org/pdf/1802.04373"
  "Y1_delValle_Nader_Yukawa.pdf"             = "https://arxiv.org/pdf/1807.11898"
  "P1_Jugdutt_Marsiglio_pozo_esferico.pdf"   = "https://arxiv.org/pdf/1211.5236"
  "P3_Daboul_Nieto_energia_cero.pdf"         = "https://arxiv.org/pdf/hep-th/9405154"
  "PI1_Kole_DeRaedt_PIQMC_Coulomb.pdf"       = "https://arxiv.org/pdf/physics/0102015"
  "PI2_Myrheim_integracion_Coulomb.pdf"      = "https://arxiv.org/pdf/physics/0306168"
  "PI3_Dluhy_paredes_integral_camino.pdf"    = "https://arxiv.org/pdf/1112.3674"
}
foreach ($k in $pdfs.Keys) {
  $out = Join-Path $dest $k
  Write-Host "Descargando $k ..."
  try { Invoke-WebRequest -Uri $pdfs[$k] -OutFile $out -UserAgent "Mozilla/5.0" } catch { Write-Warning "Falló $k : $_" }
  Start-Sleep -Seconds 4   # arXiv limita descargas seguidas
}
Write-Host "Listo: $dest"
