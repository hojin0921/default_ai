# Phase gate CLI (Windows PowerShell)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $Root "scripts"
& python (Join-Path $PSScriptRoot "_gate_cli.py") @args
exit $LASTEXITCODE
