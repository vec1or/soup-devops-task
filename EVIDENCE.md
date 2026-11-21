# Verification evidence

## Controlled failures

GitHub's Actions API confirmed the run IDs, commit SHAs, and conclusions below. The source and artifact runs in each faulty pair refer to the same commit. Historical failed-step log retrieval returned empty output. The failure mechanisms described in the README come from the repository history.

| Fault | Faulty commit | Naive CI success | Artifact Check failure | Fixed commit | Artifact Check success |
| --- | --- | --- | --- | --- | --- |
| Entry point | `7bafea3` | [44790766979](https://github.com/vec1or/soup-devops-task/actions/runs/44790766979) | [44790767116](https://github.com/vec1or/soup-devops-task/actions/runs/44790767116) | `cd98d89` | [44794766552](https://github.com/vec1or/soup-devops-task/actions/runs/44794766552) |
| Package data | `b31357d` | [44795942486](https://github.com/vec1or/soup-devops-task/actions/runs/44795942486) | [44795942115](https://github.com/vec1or/soup-devops-task/actions/runs/44795942115) | `597fbe7` | [44797301493](https://github.com/vec1or/soup-devops-task/actions/runs/44797301493) |
| Python 3.10 | `6be03a7` | [44800905066](https://github.com/vec1or/soup-devops-task/actions/runs/44800905066) | [44800905102](https://github.com/vec1or/soup-devops-task/actions/runs/44800905102) | `3825b7f` | [44801745823](https://github.com/vec1or/soup-devops-task/actions/runs/44801745823) |
| Windows | `0ec1f27` | [44879814489](https://github.com/vec1or/soup-devops-task/actions/runs/44879814489) | [44879814554](https://github.com/vec1or/soup-devops-task/actions/runs/44879814554) | `c82d693` | [44880410452](https://github.com/vec1or/soup-devops-task/actions/runs/44880410452) |

## Current checks

- Release implementation, `6560851`: [44899082745](https://github.com/vec1or/soup-devops-task/actions/runs/44899082745) passed on GitHub. Build, Ruff and seven source tests, Docker, and all four wheel jobs succeeded. Both tag-only jobs were skipped on the branch push.
- Codex ran Ruff and seven tests in WSL with Python 3.12.3, built the wheel and sdist, validated `v0.1.0`, observed nonzero exit for `v0.2.0`, and ran wheel smoke tests in a new venv outside the checkout.
- Earlier applicant-reported checks include a local Docker build and successful `soupcheck --version` and `soupcheck report` in the container.
- GitHub API confirmed creation of the `testpypi` environment and its tag-only `v*` policy. The TestPyPI simple and JSON project endpoints returned HTTP 404 on 2026-11-21. This shows no public listing for the name at check time.
- TestPyPI release pending Trusted Publisher registration. No tag-triggered upload or registry installation has been verified. See [the intended TestPyPI project](https://test.pypi.org/project/danial-soupcheck-demo/).

## AI disclosure

ChatGPT helped prepare the starter code and tests. Codex added the release checks, publishing workflow and stronger smoke assertions, prepared the submission materials, and executed the checks attributed to Codex above. The applicant's checks are based on the applicant's project handoff.
