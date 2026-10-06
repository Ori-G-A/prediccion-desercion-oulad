param(
    [string]$PdfLatex = $env:OULAD_PDFLATEX,
    [string]$BibTex = $env:OULAD_BIBTEX
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$reportsPath = Join-Path $projectRoot 'reportes/correcciones_2026_09_10/informes'
function Resolve-TexTool([string]$Provided, [string]$Name) {
    if ($Provided) {
        if (Test-Path -LiteralPath $Provided -PathType Leaf) { return $Provided }
        throw "No existe el ejecutable indicado: $Provided"
    }
    if ($env:LOCALAPPDATA) {
        $candidate = Join-Path $env:LOCALAPPDATA "Programs/MiKTeX/miktex/bin/x64/$Name.exe"
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    $found = Get-Command $Name -ErrorAction SilentlyContinue
    if ($found) { return $found.Source }
    throw "No se encontró $Name. Añádalo a PATH o indique su ruta con el parámetro correspondiente."
}
$texBinary = Resolve-TexTool $PdfLatex 'pdflatex'
$bibBinary = Resolve-TexTool $BibTex 'bibtex' 
Push-Location -LiteralPath $reportsPath
try {
    foreach ($reportName in @('01_exploracion','02_ingenieria','03_estadistica')) {
        & $texBinary -interaction=nonstopmode -halt-on-error -disable-installer "$reportName.tex"
        if ($LASTEXITCODE -ne 0) { throw "Falló pdflatex: $reportName" }
        & $bibBinary $reportName
        if ($LASTEXITCODE -ne 0) { throw "Falló bibtex: $reportName" }
        & $texBinary -interaction=nonstopmode -halt-on-error -disable-installer "$reportName.tex"
        if ($LASTEXITCODE -ne 0) { throw "Falló pdflatex: $reportName" }
        & $texBinary -interaction=nonstopmode -halt-on-error -disable-installer "$reportName.tex"
        if ($LASTEXITCODE -ne 0) { throw "Falló pdflatex: $reportName" }
    }
} finally { Pop-Location }
