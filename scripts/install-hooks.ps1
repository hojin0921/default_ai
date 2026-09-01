# Install git hooks + Cursor hook Python command (Windows)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
& python (Join-Path $PSScriptRoot "install_hooks.py") @args
exit $LASTEXITCODE
