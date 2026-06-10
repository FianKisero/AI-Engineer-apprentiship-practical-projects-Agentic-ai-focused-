#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    target_script = project_dir / "venv" / "agent.py"

    if not target_script.exists():
        raise SystemExit(f"Could not find the agent script at {target_script}")

    sys.argv[0] = str(target_script)
    runpy.run_path(str(target_script), run_name="__main__")
