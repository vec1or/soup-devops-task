"""Install one wheel in a clean environment and run its console command."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command, workdir, environment):
    command = [str(part) for part in command]
    print("Running:", " ".join(command), flush=True)
    subprocess.run(command, cwd=workdir, env=environment, check=True)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python ci/smoke_wheel.py DIST_DIRECTORY")

    wheels = list(Path(sys.argv[1]).resolve().glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"Expected exactly one wheel; found {len(wheels)}")

    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)

    with tempfile.TemporaryDirectory(prefix="soupcheck-smoke-") as temporary:
        root = Path(temporary)
        venv_dir = root / "venv"
        workdir = root / "work"
        workdir.mkdir()

        run([sys.executable, "-m", "venv", venv_dir], workdir, environment)

        windows = os.name == "nt"
        bin_dir = venv_dir / ("Scripts" if windows else "bin")
        python = bin_dir / ("python.exe" if windows else "python")
        cli = bin_dir / ("soupcheck.exe" if windows else "soupcheck")

        run(
            [python, "-m", "pip", "--isolated", "install",
             "--no-index", "--no-deps", wheels[0]],
            workdir,
            environment,
        )
        run([cli, "--version"], workdir, environment)
        run([cli, "report"], workdir, environment)


if __name__ == "__main__":
    main()
