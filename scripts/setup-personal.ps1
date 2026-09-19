#Requires -Version 7.0
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
foreach ($tool in @('python', 'pipx')) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "$tool is required. See docs/personal-fork.md."
    }
}

# Pin package installation to this checkout; never install the upstream ZIP here.
& pipx install --force $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'Package installation failed; skills were not deployed.' }
& python (Join-Path $PSScriptRoot 'deploy_personal.py')
if ($LASTEXITCODE -ne 0) { throw 'Skill deployment failed.' }

$localBin = Join-Path $HOME '.local/bin'
if (($env:PATH -split [IO.Path]::PathSeparator) -notcontains $localBin) {
    $env:PATH = $localBin + [IO.Path]::PathSeparator + $env:PATH
}
& pipx ensurepath
if ($LASTEXITCODE -ne 0) { throw 'Could not persist the command directory in PATH.' }
& agent-reach --version
if ($LASTEXITCODE -ne 0) { throw 'Installed CLI did not start.' }

$missing = @('mcporter', 'firecrawl', 'tinyfish') | Where-Object {
    -not (Get-Command $_ -ErrorAction SilentlyContinue)
}
if ($missing) {
    Write-Warning ('Search tools still need setup: ' + ($missing -join ', ') + '. See docs/personal-fork.md.')
}
Write-Output 'Personal skill and search command installed. Credentials are configured separately.'
