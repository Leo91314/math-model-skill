#!/usr/bin/env python3
"""Install an explicit group of local skills without replacing existing folders."""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--group", choices=["core", "project", "all"], default="core")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "provenance/skill-manifest.json").read_text(encoding="utf-8"))
    groups = {"core"} if args.group == "core" else {"core", "bzd", "scientific"}
    if args.group == "all":
        groups.add("supporting")
    destination = args.project.expanduser().resolve() / ".agents" / "skills"
    destination.mkdir(parents=True, exist_ok=True)
    installed = 0
    skipped = 0
    for skill in manifest["skills"]:
        if skill["group"] not in groups:
            continue
        source = ROOT / skill["path"]
        target = destination / skill["name"]
        if target.exists() or target.is_symlink():
            skipped += 1
            print(f"Skipped existing: {skill['name']}")
            continue
        shutil.copytree(source, target)
        installed += 1
        print(f"Installed: {skill['name']}")
    print(f"Installed {installed}; skipped {skipped}. Destination: {destination}")


if __name__ == "__main__":
    main()
