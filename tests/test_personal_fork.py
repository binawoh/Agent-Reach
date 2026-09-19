"""Personal deployment isolation and observable search fallback behavior."""

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("deploy_personal", ROOT / "scripts/deploy_personal.py")
deploy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy_module)


def test_deploy_resolves_new_home_preserves_credentials_and_is_idempotent(tmp_path, monkeypatch):
    home = tmp_path / "different user"
    codex = tmp_path / "custom codex"
    monkeypatch.setenv("CODEX_HOME", str(codex))
    credential = home / ".tinyfish/config.json"
    credential.parent.mkdir(parents=True)
    credential.write_text('{"test_placeholder": "leave alone"}', encoding="utf-8")
    original = credential.read_bytes()

    first = deploy_module.deploy(home)
    assert (codex / "skills/agent-reach/SKILL.md").read_bytes() == (
        ROOT / "agent_reach/skill/SKILL.md"
    ).read_bytes()
    assert (home / ".local/bin/agent-search.ps1").is_file()
    assert credential.read_bytes() == original
    assert first["changed_files"]
    assert deploy_module.deploy(home)["changed_files"] == []
    assert json.loads((home / ".agent-reach/personal-install.json").read_text())["source"] == str(ROOT)


def test_deploy_preserves_link_and_unrelated_skill_file(tmp_path):
    canonical = tmp_path / "canonical"
    canonical.mkdir()
    root = tmp_path / "skills"
    root.mkdir()
    link = root / "agent-reach"
    try:
        link.symlink_to(canonical, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks unavailable")
    unrelated = canonical / "personal-note.txt"
    unrelated.write_text("keep", encoding="utf-8")
    deploy_module.deploy(tmp_path / "home", [root], tmp_path / "commands")
    assert link.is_symlink()
    assert unrelated.read_text() == "keep"
    assert (canonical / "SKILL.md").is_file()


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
