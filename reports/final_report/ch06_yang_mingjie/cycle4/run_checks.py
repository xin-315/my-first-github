"""Record personal and full-suite results; run with the isolated test interpreter."""

import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone


def main():
    root = Path(__file__).resolve().parents[4]
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).parent / "evidence/recheck"
    output.mkdir(parents=True, exist_ok=True)
    if (root / ".env").exists():
        raise SystemExit("Use a clean checkout without .env to avoid loading live credentials.")
    env = dict(os.environ, QWEN_API_KEY="", DASHSCOPE_API_KEY="", PYTHONPATH="",
               PYTHONIOENCODING="utf-8", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    tracked = subprocess.check_output(["git", "diff", "--name-only", "HEAD"], cwd=root, text=True).splitlines()
    results = []
    for name, targets in [("personal", ["tests/test_cycle4_integration.py"]), ("full", ["tests"])]:
        command = [sys.executable, "-m", "pytest", *targets, "-q", "-rx", "--disable-warnings",
                   "-p", "no:cacheprovider", f"--junitxml={output / (name + '.xml')}"]
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True,
                                encoding="utf-8", timeout=180)
        (output / (name + ".txt")).write_text(result.stdout + result.stderr, encoding="utf-8")
        results.append({"name": name, "command": command, "exit_code": result.returncode})
        print(name, "exit", result.returncode)
        print(result.stdout.splitlines()[-1] if result.stdout.splitlines() else result.stderr)
    packages = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    (output / "environment.json").write_text(json.dumps({
        "utc": datetime.now(timezone.utc).isoformat(), "base_commit": head,
        "python": sys.version, "platform": platform.platform(), "packages": packages,
        "tracked_changes": tracked, "runs": results,
        "boundary": "No .env. Empty API-key environment. Upstream failures use MockTransport. No live-model evaluation.",
    }, indent=2), encoding="utf-8")
    return max(r["exit_code"] for r in results)


if __name__ == "__main__":
    raise SystemExit(main())
