"""Deploy the tracked skill/search files without copying credentials or deleting links."""

import argparse
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def deploy(home: Path, skill_roots: list[Path] | None = None,
           bin_dir: Path | None = None) -> dict:
    if skill_roots is None:
        codex = Path(os.environ.get("CODEX_HOME") or home / ".codex")
        skill_roots = [codex / "skills"]
        for root in (home / ".agents/skills", home / ".claude/skills",
                     home / ".cursor/skills", home / ".config/opencode/skills"):
            if root.is_dir():
                skill_roots.append(root)
    bin_dir = bin_dir or home / ".local/bin"
    source = REPO / "agent_reach/skill"
    writes = {}
    for root in skill_roots:
        target = (root / "agent-reach").resolve()
        # Explicit allowlist: never copy the user's config, cookies or environment.
        for item in [source / "SKILL.md", *sorted((source / "references").glob("*.md"))]:
            writes[target / item.relative_to(source)] = item.read_bytes()
    writes[(bin_dir / "agent-search.ps1").resolve()] = (
        REPO / "agent_reach/scripts/agent-search.ps1"
    ).read_bytes()
    changed = []
    for target, content in writes.items():
        if target.is_file() and target.read_bytes() == content:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        changed.append(str(target))
    # Record only the checkout location, not credentials, so a later agent can find it.
    location = home / ".agent-reach/personal-install.json"
    location.parent.mkdir(parents=True, exist_ok=True)
    location.write_text(json.dumps({"source": str(REPO)}, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    return {"source": str(REPO), "changed_files": changed, "bin_dir": str(bin_dir)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, action="append")
    parser.add_argument("--bin-dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(deploy(Path.home(), args.skill_root, args.bin_dir), ensure_ascii=False))


if __name__ == "__main__":
    main()
