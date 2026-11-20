# Soup take-home: working CLI starter

This is the first working application for the release-pipeline exercise.
It prints its installed version, the current Python version and operating
system, and a message read from a JSON file shipped in the package.

The distribution name `danial-soupcheck-demo` is a local working name.
Its availability on TestPyPI has not been checked or reserved.

## Start in Ubuntu / WSL

Work in the Linux filesystem, for example `~/projects/soap_hometask`.
If a Conda base environment is active, run `conda deactivate` in this shell.

```bash
cd ~/projects/soap_hometask
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation -e .
soupcheck --version
soupcheck report
python -m unittest discover -s tests -v
```

If Ubuntu reports that `ensurepip` is unavailable, install `python3-venv`
with `sudo apt update` and `sudo apt install python3-venv`, then retry
creating the environment. Use project pip after activating `.venv`.

## What the files do

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Package name, version, build settings, command, and included JSON file |
| `src/soupcheck/cli.py` | Command-line arguments and report |
| `src/soupcheck/message.json` | Data that must reach the installed package |
| `src/soupcheck/__init__.py` | Marks the regular Python package |
| `tests/test_cli.py` | Two checks of source-level behavior |
| `requirements-dev.txt` | Pinned versions of build tools |
| `.gitignore` | Keeps environments and build outputs out of Git |

The project version is defined in `pyproject.toml`. The program reads the
installed distribution metadata. Run the installation command again after
changing metadata such as the version or console entry point.

## Build a wheel and a source archive

```bash
python -m build
```

This should produce:

```text
dist/danial_soupcheck_demo-0.1.0-py3-none-any.whl
dist/danial_soupcheck_demo-0.1.0.tar.gz
```

Building these files is not a test of their installed behavior.
The filenames below are for version 0.1.0. When changing the version later,
use the artifacts produced by that new build.

## Check the wheel independently

Run from the project directory after the build:

```bash
wheel_path="$PWD/dist/danial_soupcheck_demo-0.1.0-py3-none-any.whl"
smoke_dir=$(mktemp -d /tmp/soupcheck-wheel.XXXXXX)
/usr/bin/python3 -m venv "$smoke_dir/venv"
"$smoke_dir/venv/bin/python" -m pip install --no-index --no-deps "$wheel_path"
(
  set -e
  cd "$smoke_dir"
  "$smoke_dir/venv/bin/soupcheck" --version
  "$smoke_dir/venv/bin/soupcheck" report
)
```

The temporary environment does not inherit the editable installation.
The command runs outside the source checkout, so repository files cannot
silently replace files omitted from the wheel.

For source-archive verification, create another fresh environment and install
the `.tar.gz` file there. Do not count the wheel check as an sdist check.

## Status and remaining assignment work

This starter requests Python 3.10 or newer. The intended compatibility range
still needs evidence from the actual CI matrix. A local green check is not
proof that all supported environments work.

Remaining work: naive and hardened GitHub Actions workflows; four isolated
fault experiments with real run links; native Windows checks; Docker smoke
test; at least three supply-chain protections; tag-driven TestPyPI publishing
using OIDC; GPU design and cost estimate; the two-page note and reflection.

The dev requirements pin tool versions but do not include integrity hashes.
This is not yet a complete supply-chain protection strategy.

## AI assistance

ChatGPT prepared this starter's code, tests, packaging settings and instructions.
The applicant should record the commands they actually ran, the logs they
reviewed, and any changes they made. No applicant-side verification or GitHub
Actions result is claimed by this starter.

Assistant validation completed on Linux with Python 3.12.14: the two source
tests passed; wheel and source archive were each installed in their own fresh
environment and run outside the checkout. Version, help, report, and invalid
command behavior were checked. Windows, Python 3.10, Docker, GitHub Actions,
and TestPyPI publication are not yet verified.
