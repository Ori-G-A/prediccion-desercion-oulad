param(
    [string]$PdfLatex = $env:OULAD_PDFLATEX,
    [string]$BibTex = $env:OULAD_BIBTEX,
    [switch]$InstalarPaquetes
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$documentPath = Join-Path $projectRoot 'Plantilla_ProyAplicado'
function Resolve-TexTool([string]$Provided, [string]$Name) {
    if ($Provided) {
        if (Test-Path -LiteralPath $Provided -PathType Leaf) { return (Resolve-Path -LiteralPath $Provided).Path }
        throw "No existe el ejecutable indicado: $Provided"
    }
    if ($env:LOCALAPPDATA) {
        $candidate = Join-Path $env:LOCALAPPDATA "Programs/MiKTeX/miktex/bin/x64/$Name.exe"
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    $found = Get-Command $Name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) { return $found.Source }
    throw "No se encontró $Name. Añádalo a PATH o indique su ruta con el parámetro correspondiente."
}
$texBinary = Resolve-TexTool $PdfLatex 'pdflatex'
$bibBinary = Resolve-TexTool $BibTex 'bibtex'
$installerOption = if ($InstalarPaquetes) { '-enable-installer' } else { '-disable-installer' }
Push-Location -LiteralPath $documentPath
try {
    & $texBinary -interaction=nonstopmode -halt-on-error $installerOption proyecto.tex *> compilacion_proyecto.txt
    if ($LASTEXITCODE -ne 0) { Get-Content compilacion_proyecto.txt -Tail 30; throw 'Falló la primera compilación' }
    & $bibBinary $installerOption proyecto *>> compilacion_proyecto.txt
    if ($LASTEXITCODE -ne 0) { Get-Content compilacion_proyecto.txt -Tail 30; throw 'Falló BibTeX' }
    foreach ($pass in 1..3) {
        & $texBinary -interaction=nonstopmode -halt-on-error $installerOption proyecto.tex *>> compilacion_proyecto.txt
        if ($LASTEXITCODE -ne 0) { Get-Content compilacion_proyecto.txt -Tail 30; throw "Falló compilación $pass" }
    }
    Write-Output 'Proyecto compilado. Registro: Plantilla_ProyAplicado/compilacion_proyecto.txt'
} finally { Pop-Location }
