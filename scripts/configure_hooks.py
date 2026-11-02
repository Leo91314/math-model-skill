#!/usr/bin/env python3
"""Write optional project hook definitions without changing trust or global config."""

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    hook_file = project / ".codex/hooks.json"
    if hook_file.exists() or hook_file.is_symlink():
        parser.exit(1, f"Existing hooks preserved; merge manually: {hook_file}\n")
    script = project / "tools/workspace_hook.py"
    script.parent.mkdir(parents=True, exist_ok=True)
    if not script.exists():
        shutil.copy2(ROOT / "templates/project/tools/workspace_hook.py", script)
    config = json.loads((ROOT / "templates/hooks/hooks.example.json").read_text(encoding="utf-8"))
    command = shlex.quote(args.python) + " " + shlex.quote(str(script))
    for groups in config["hooks"].values():
        for group in groups:
            for hook in group["hooks"]:
                hook["command"] = command
    hook_file.parent.mkdir(parents=True, exist_ok=True)
    hook_file.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    layer = hook_file.parent / "config.toml"
    if not layer.exists():
        layer.write_text("# Project hooks are defined in hooks.json.\n", encoding="utf-8")
    print(f"Written: {hook_file}")
    print("Review these exact definitions in Codex /hooks before enabling them.")


if __name__ == "__main__":
    main()
