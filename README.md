# Soupcheck

`soupcheck` prints the installed application version, Python version, operating system, username, UTC timestamp, and a message shipped as JSON package data. The distribution is `danial-soupcheck-demo` and has no third-party runtime dependencies.

## Run the checks locally

Use Python 3.12 for the release tooling. Activate the virtual environment with `.venv\Scripts\Activate.ps1` on Windows or the command below on Linux.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --no-cache-dir -r requirements-dev.txt -r requirements-lint.txt
python -m pip install --no-build-isolation -e .
soupcheck --version
soupcheck report
python -m ruff check --no-cache src tests ci
python -m unittest discover -s tests -v
```

Start the artifact checks with an empty `dist/` directory.

```bash
python -m build
python ci/validate_release.py v0.1.0 dist
python ci/smoke_wheel.py dist
docker build --no-cache -t soupcheck:local .
docker run --rm --network none soupcheck:local --version
docker run --rm --network none soupcheck:local report
```

## CI and experiments

**Naive CI** is the experimental control. Source tests call the Python function directly and exercise the checkout on a single runner.

**Artifact Check** runs Ruff and source tests, then checks a single uploaded build across Ubuntu 24.04 and Windows 2022 on Python 3.10 and 3.12. Each wheel check creates a temporary venv, clears `PYTHONPATH` and `PYTHONHOME`, installs with `--no-index --no-deps`, and checks output outside the checkout. The Docker job uses the same wheel, a digest-pinned base, a non-root user, and network-disabled CLI runs. The jobs run independently where their dependencies permit.

| Fault | What failed for an installed user | Fix |
| --- | --- | --- |
| Entry point | Console launcher targets a missing function | Point it to `soupcheck.cli:main` |
| Package data | `report` cannot read the packaged JSON | Declare the resource in setuptools package data |
| Python 3.10 | `datetime.UTC` is unavailable | Use `timezone.utc` |
| Windows | Unix account APIs are unavailable | Use `getpass.getuser()` |

See [EVIDENCE.md](EVIDENCE.md) for commits and runs.

## Supply-chain controls

| Risk | Control and verification |
| --- | --- |
| Stale or substituted artifact | The build outputs one immutable artifact ID. Wheel, Docker, release validation, and publishing download that ID with digest mismatch set to error. Review their download steps and build output in the same tag run. |
| Tag/version disagreement | Release validation requires `vMAJOR.MINOR.PATCH` and compares the source version plus distribution name and version in both archives. Unit tests reject wrong tags, versions, names, and extra files. |
| Fork PR publishing | Use `pull_request`, keep default permissions at `contents: read`, and grant OIDC only to the TestPyPI job gated on an upstream tag push and all required jobs. The GitHub environment allows only `v*` tags. Branch CI shows the publish job skipped. |

Actions are pinned by full SHA and checkout disables credential persistence. Build and lint tool versions are pinned, but dependency hashes are absent. Dependency substitution and reproducible builds are still open. The wheel matrix samples four environments. The sdist is used to build the wheel and its root metadata is checked. A separate clean sdist installation is outside the final CI coverage.

## TestPyPI release

In [TestPyPI Publishing](https://test.pypi.org/manage/account/publishing/), register a pending GitHub Trusted Publisher with these values.

| Setting | Value |
| --- | --- |
| Project name | `danial-soupcheck-demo` |
| Owner | `vec1or` |
| Repository | `soup-devops-task` |
| Workflow filename | `artifact-check.yml` |
| Environment | `testpypi` |

After a matching release tag is pushed, the publish job takes the validated wheel and sdist from the same build. The PyPA action uploads them to TestPyPI using OIDC. To verify a successful upload, install in a fresh directory and venv using just TestPyPI.

```bash
smoke_dir=$(mktemp -d)
cd "$smoke_dir"
python3.12 -m venv venv
env -u PYTHONPATH -u PYTHONHOME PIP_CONFIG_FILE=/dev/null \
  venv/bin/python -m pip --isolated install --no-deps --only-binary=:all: \
  --index-url https://test.pypi.org/simple/ danial-soupcheck-demo==0.1.0
env -u PYTHONPATH -u PYTHONHOME venv/bin/soupcheck --version
env -u PYTHONPATH -u PYTHONHOME venv/bin/soupcheck report
```
