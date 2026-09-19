"""Observable behavior of the optional personal search adapter."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_search(script):
    pwsh = shutil.which("pwsh")
    if not pwsh:
        pytest.skip("PowerShell 7 required for personal search tests")
    return subprocess.run([pwsh, "-NoProfile", "-Command", script], capture_output=True,
                          encoding="utf-8", errors="replace", timeout=30)


def test_auto_search_reaches_tinyfish_when_other_providers_fail():
    search = str(ROOT / "agent_reach/scripts/agent-search.ps1").replace("'", "''")
    result = run_search("""
function mcporter { $global:LASTEXITCODE=1; 'Exa unavailable' }
$env:TAVILY_API_KEY='test-placeholder'
function Invoke-RestMethod { throw 'Tavily unavailable' }
function firecrawl { $global:LASTEXITCODE=1; 'Firecrawl unavailable' }
function tinyfish {
    $global:LASTEXITCODE=0
    '{"results":[{"title":"one"},{"title":"two"},{"title":"three"}]}'
}
""" + f"& '{search}' -Query 'query with spaces' -Limit 2")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["success"] and data["provider"] == "tinyfish"
    assert data["query"] == "query with spaces"
    assert len(data["data"]["results"]) == 2


def test_tinyfish_failure_is_not_reported_as_search_success():
    search = str(ROOT / "agent_reach/scripts/agent-search.ps1").replace("'", "''")
    result = run_search("function tinyfish { $global:LASTEXITCODE=1; 'Service unavailable' }; "
                        + f"& '{search}' -Query 'query' -Provider tinyfish")
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["success"] is False
    assert data["attempts"][0]["provider"] == "tinyfish"
