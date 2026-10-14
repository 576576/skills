# Examples

Six skeletons, one per role in the matrix. Copy them into
`.github/workflows/` of a repository and replace the project-specific parts —
which is exactly: the install/build/lint commands, the runner labels, and the
target rows in `release.yml`'s `prep`.

| File | Demonstrates |
|---|---|
| [`workflows/lint.yml`](workflows/lint.yml) | the reusable gate: `workflow_call` only, the sole copy of the commands |
| [`workflows/build.yml`](workflows/build.yml) | reusable build with a `fromJson` matrix, an empty-matrix guard, `pack_artifacts` switch, `if-no-files-found: error` |
| [`workflows/release.yml`](workflows/release.yml) | the only entry point: `prep` computes channel/version/matrix, gate as `needs:`, artifact hand-off, tag + release |
| [`workflows/pr.yml`](workflows/pr.yml) | PR gate reusing both files, no `paths-ignore`, `concurrency` by PR number |
| [`workflows/clear.yml`](workflows/clear.yml) | window-based pre-release cleanup: paginated listing, oldest-first delete, dry run |
| [`workflows/update_i18n.yml`](workflows/update_i18n.yml) | push-triggered job filtered by log message, token, commit-back — plus the "not wired yet must fail loudly" variant |
| [`verify_workflows.py`](verify_workflows.py) | local harness: YAML, `bash -n` per run block, `uses:` targets, `with:` contract, PR path filters, trigger faces |

## Running the verifier

```bash
python verify_workflows.py /path/to/repo            # structure + syntax
python verify_workflows.py /path/to/repo --expect expectations.json
```

`expectations.json` pins each file's trigger face — the thing that is easiest to
change by accident:

```json
{
  "lint.yml":        ["workflow_call", "workflow_dispatch"],
  "build.yml":       ["workflow_call"],
  "release.yml":     ["push", "workflow_dispatch"],
  "pr.yml":          ["pull_request", "workflow_dispatch"],
  "clear.yml":       ["workflow_dispatch"],
  "update_i18n.yml": ["push", "workflow_dispatch"]
}
```

Exit code is 1 on any failure, so it drops straight into a pre-commit hook or a
`Makefile` target. Needs `pyyaml`.

The harness deliberately stops where local conditions end: platform behaviour
(installers, signing, cross-compilation) can only be proven by the real runners.
What it *can* do is run pure-logic steps — a version-computation step can be
executed for real in a throwaway git repository with a fake `$GITHUB_OUTPUT`,
one case per trigger path (`push`, and each dispatch channel).
