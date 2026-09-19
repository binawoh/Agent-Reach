#Requires -Version 7.0
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$branch = & git -C $repoRoot branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
    throw 'Update requires the personal main branch.'
}
$changes = & git -C $repoRoot status --porcelain
if ($LASTEXITCODE -ne 0 -or $changes) {
    throw 'Save/commit local changes before updating; nothing was overwritten.'
}
$origin = & git -C $repoRoot remote get-url origin
if ($LASTEXITCODE -ne 0 -or $origin -notmatch '^(https://github\.com/|git@github\.com:)binawoh/Agent-Reach(?:\.git)?/?$') {
    throw 'origin must be the personal binawoh/Agent-Reach repository.'
}
& git -C $repoRoot pull --ff-only origin main
if ($LASTEXITCODE -ne 0) { throw 'Pull failed; the installed version was not changed.' }
& (Join-Path $PSScriptRoot 'setup-personal.ps1')
