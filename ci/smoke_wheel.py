"""Install one wheel in a clean environment and run its console command."""

import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command, workdir, environment, *, capture=False):
    command = [str(part) for part in command]
    print("Running:", " ".join(command), flush=True)
    result = subprocess.run(
        command, cwd=workdir, env=environment, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    if capture:
        print(result.stdout, end="", flush=True)
        return result.stdout


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
        version_output = run([cli, "--version"], workdir, environment, capture=True)
        match = re.fullmatch(r"soupcheck ([0-9]+\.[0-9]+\.[0-9]+)", version_output.strip())
        if not match:
            raise SystemExit(f"Unexpected version output: {version_output!r}")

        report = run([cli, "report"], workdir, environment, capture=True)
        expected = {
            f"Application version: {match[1]}",
            f"Python version: {platform.python_version()}",
            f"Operating system: {platform.system()}",
            "Message: Everything works!",
        }
        missing = expected.difference(report.splitlines())
        if missing:
            raise SystemExit(f"Missing expected report lines: {sorted(missing)}")


if __name__ == "__main__":
    main()
