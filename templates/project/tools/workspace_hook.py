#!/usr/bin/env python3
"""Local Codex reminders and a non-blocking Python syntax check; no model execution."""

import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(event, dict):
        return
    cwd = Path(event.get("cwd") or ROOT).resolve()
    if cwd != ROOT and ROOT not in cwd.parents:
        return
    name = event.get("hook_event_name")
    if name == "SessionStart":
        python = ROOT / ".venv/bin/python"
        state = "已就绪" if python.exists() else "缺失，请先查看 README.md 恢复环境"
        context = (
            f"数模项目：{ROOT}。本地解释器 {python}：{state}。"
            "先读 README.md 与 AGENTS.md；续接任务时查 task_plan.md、findings.md、progress.md。"
            "outputs/env_check 是合成数据环境演示，不是赛题结果。"
        )
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": name, "additionalContext": context
        }}, ensure_ascii=False))
    elif name == "Stop":
        failures = []
        checked = 0
        for folder in ("src", "scripts", "tools"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
                    continue
                checked += 1
                try:
                    ast.parse(path.read_bytes(), filename=str(path))
                except (SyntaxError, ValueError, OSError) as exc:
                    failures.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
        report = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "check": "Python AST syntax only; no execution or result validation",
            "files_checked": checked,
            "ok": not failures,
            "failures": failures,
        }
        output = ROOT / "outputs/last_hook_check.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        if failures:
            print(json.dumps({"systemMessage":
                f"数模项目语法检查发现 {len(failures)} 个问题，详见 {output}；此提示不会阻止任务结束。"
            }, ensure_ascii=False))


if __name__ == "__main__":
    main()
