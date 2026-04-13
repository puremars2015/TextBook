Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $scriptRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $pythonExe)) {
    throw 'Python virtual environment was not found at .venv\Scripts\python.exe.'
}

& $pythonExe -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to install PyInstaller.'
}

$dataArg = 'scripts\openclaw_helper.ps1;scripts'

$pyInstallerArgs = @(
    '-m',
    'PyInstaller',
    '--noconfirm',
    '--clean',
    '--windowed',
    '--onefile',
    '--name',
    'OpenClawManager',
    '--add-data',
    $dataArg,
    '--collect-submodules',
    'tkinter',
    'openclaw_manager.py'
)

& $pythonExe @pyInstallerArgs

if ($LASTEXITCODE -ne 0) {
    throw 'PyInstaller build failed.'
}

Write-Host 'Build complete: .\dist\OpenClawManager.exe'