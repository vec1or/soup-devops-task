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
- The applicant registered the TestPyPI Trusted Publisher. Codex pushed `v0.1.0` at `7760132`. The [tag-triggered release run](https://github.com/vec1or/soup-devops-task/actions/runs/44900047105) passed the build, lint and tests, four wheel jobs, Docker, metadata validation, and the OIDC publish job.
- The [TestPyPI 0.1.0 release](https://test.pypi.org/project/danial-soupcheck-demo/0.1.0/) lists the wheel and sdist. Codex installed the published wheel in a fresh Python 3.12.3 venv outside the checkout using TestPyPI as the sole index. The CLI returned `soupcheck 0.1.0` and the report contained the expected application version and packaged message.

## AI disclosure

ChatGPT helped prepare the starter code and tests. Codex added the release checks, publishing workflow and stronger smoke assertions, prepared the submission materials, and executed the checks attributed to Codex above. The applicant's checks are based on the applicant's project handoff.
