---
name: ci-matrix
description: >-
  Design, review and extend a multi-workflow GitHub Actions CI family: one
  reusable quality gate, one reusable build, one release entry point, a PR
  gate, a pre-release cleaner and an i18n updater. Covers the six-file matrix
  (lint / build / release / pr / clear / update_i18n) — which trigger each file
  may take, how jobs call each other with workflow_call, where the version
  number and the target matrix get computed, permission and concurrency rules
  per trigger, and the local verification harness (YAML parse + trigger-face
  assertions + bash -n per run block + mutation testing). Use when adding or
  renaming a workflow, changing triggers, wiring lint/build into release or PR,
  aligning the CI file set across sibling repositories, or debugging "the check
  never runs" / "required check stuck pending" / "workflow skipped on a docs-only
  change" / "release published but assets missing".
  Ready-to-copy skeletons live under examples/, the rules and traps under references/.
---

# CI Matrix Skill

A repository's CI is not one file. It is a small **matrix of files**, each with
one trigger face, one role, and a fixed relation to the others. This skill is
that matrix, plus the rules that keep it from drifting.

The shape below is the one proven across four sibling repositories
(Rust server, Tauri desktop shell, Java sandbox, Node front end) — ~20 workflows,
all following the same six roles.

## The six files

| File | Trigger | Role | Reusable |
|---|---|---|---|
| `lint.yml` | `workflow_call` + `workflow_dispatch` | quality gate (fmt / lint / tests) | **yes** |
| `build.yml` | `workflow_call` | compile + package + `upload-artifact` | **yes** |
| `release.yml` | `push: main` + `workflow_dispatch(channel)` | **only entry point**: compute version → gate → build → publish | no |
| `pr.yml` | `pull_request: main` + `workflow_dispatch` | PR gate: call `lint.yml` (+ `build.yml`) | no |
| `clear.yml` | `workflow_dispatch` | delete surplus pre-releases in a time window | no |
| `update_i18n.yml` | `push: main` (marked commits only) + `workflow_dispatch` | pull translations, commit them back | no |

```
release.yml ──┬── uses: lint.yml      (gate runs on the release path)
              └── uses: build.yml     (pack_zip: true)
pr.yml ───────┬── uses: lint.yml
              └── uses: build.yml     (pack_zip: false — "does it still build?")
lint.yml / build.yml themselves: never follow push or pull_request
```

`lint.yml` and `build.yml` hold the **only** copy of their commands. Everything
else is a trigger face plus `uses:`, because a second copy of a command list
drifts — and the copy that drifts is always the one nobody runs locally.

## Layout

```
ci-matrix/
├── SKILL.md                      # this entry point
├── references/
│   ├── matrix.md                 # per-file contract: trigger, permissions, concurrency, may/may-not
│   ├── rules.md                  # the rules, each with the failure it prevents
│   └── gotchas.md                # traps that don't fail loudly (silent skips, $GITHUB_OUTPUT, check names)
└── examples/
    ├── README.md                 # which example shows what
    ├── workflows/                # six copy-ready skeletons
    └── verify_workflows.py       # local harness: YAML + trigger faces + bash -n + anchor checks
```

## Quick start

1. **Understand the contract** — read [references/matrix.md](references/matrix.md)
   before touching a trigger. The trigger face of a file is what makes it
   reusable; changing it silently changes every caller.
2. **Copy a skeleton** from [examples/workflows/](examples/workflows/) and keep
   the file name — the names *are* the matrix.
3. **Mind the rules** — [references/rules.md](references/rules.md) (what each
   rule prevents) and [references/gotchas.md](references/gotchas.md) (what fails
   without a red light).
4. **Verify locally** before pushing — a matrix run costs minutes and may publish:

   ```bash
   python verify_workflows.py /path/to/repo
   ```

   It parses every workflow, asserts each file's trigger face, runs every `run:`
   block through `bash -n`, and checks that every `uses: ./.github/workflows/x.yml`
   points at a file that exists.

## Invariants worth memorizing

- **One entry point per chain.** Pushes and manual dispatches both enter through
  `release.yml`; there is no second door, so nothing can bypass the gate.
- **The gate is a dependency, not a step.** `build.needs = [prep, lint]` — the
  gate is called as a job, so "green CI that never ran the gate" is impossible.
- **Never add `pull_request` to a file that already follows `push`.** The same
  file would then have two semantics (publish vs verify) and two permission sets.
- **No `paths-ignore` on `pull_request`.** A skipped workflow is *absent*: the PR
  has no check, and a required check stays pending forever. Put `paths-ignore`
  on the `push` side of `release.yml` only.
- **Compute once, pass down.** Version numbers and matrices are computed in the
  entry point's `prep` job and handed to `build.yml` as inputs; the reusable
  workflow never re-derives them.
- **A job's display name is the required-check name.** Rename a job and branch
  protection silently points at nothing.
