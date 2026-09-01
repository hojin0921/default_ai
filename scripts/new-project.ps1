# Copy template into a new project folder (Windows)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
& python (Join-Path $PSScriptRoot "new_project.py") @args
exit $LASTEXITCODE
