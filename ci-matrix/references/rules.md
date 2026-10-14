# Rules, and the failure each one prevents

Every rule here exists because the alternative fails in a way that is expensive
to notice: a green run that verified nothing, a check that never appears, or a
release that quietly misses assets.

## 1. Separate "reusable" from "entry"

A reusable workflow (`workflow_call`) has no trigger of its own; an entry point
has the trigger and calls the reusable ones.

*Without it:* putting `pull_request` directly on the file that also runs the
release chain gives that file two semantics (verify vs publish) and two
permission sets. Every input that is required for release has no value on a PR,
so the file fills with `if:` guards and fake defaults — and the release path
gets edited by people who were only trying to fix a PR check.

## 2. The gate is a job dependency, not a step

```yaml
lint:
  uses: ./.github/workflows/lint.yml
build:
  needs: [prep, lint]
```

*Without it:* "run lint first, then build" as sequential steps inside one job
lets a future reordering or a `continue-on-error` bypass the gate, and the release
still comes out green. As a `needs:` edge, a failing gate leaves `build`
**skipped** — the release cannot exist.

## 3. Write each command list exactly once

`lint.yml` holds `fmt / lint / typecheck / test`; `pr.yml` and `release.yml`
only ever `uses:` it.

*Without it:* the two copies drift the moment someone adds a test to the release
path. The drifted copy is the PR one — so PRs pass a gate that the release path
does not run, and the failure surfaces after merge.

## 4. `paths-ignore`: push yes, pull_request never

- On `release.yml`'s `push`: `paths-ignore: ['docs/**', '*.md', '**/*.md']` so a
  docs-only push does not burn a 12-minute matrix and publish a build.
- On `pr.yml`: **nothing**. A workflow skipped by `paths-ignore` is *absent* from
  the PR — not "successful". If that check is required in branch protection, the
  PR sits at "pending" forever, with no red light anywhere.

Precondition for ignoring a path: nothing in the build may read it. Before
ignoring `**/*.md`, prove no build step resolves a `.md` file (a changelog
writer, a docs generator, a template loader). A build input that is excluded
from CI is invisible: that path permanently stops being built, silently.

## 5. Compute once, in the entry point

Version, tag, suffix, target matrix, pack switches: computed in `release.yml`'s
`prep`, passed to `build.yml` as inputs. The reusable workflow never re-derives
them, and never invents a default for an input that genuinely has no value in
some caller.

*Without it:* the artifact name in `build.yml` and the tag in `publish` are two
independent derivations that disagree on the edge cases (channel suffix, toolchain
segment, patch padding) — and you get a release whose asset names do not match
its tag.

**Exception:** an input that has a *meaningful* fallback in the tool itself may
be optional. (A version-writer script that defaults to `r<commit count>` and
channel `local` needs no CI-supplied value on a PR — that is a real default, not
a fabricated one.)

## 6. Permissions: never wider downstream

A called workflow cannot exceed the caller's `permissions`. Set the minimum per
job: PR and gate jobs take `contents: read`; only the publish job takes
`contents: write`; only a job that pushes images adds `packages: write`.

Artifact upload needs no `permissions:` entry — it uses the run's runtime token,
not `GITHUB_TOKEN`.

*Without it:* the failure is a 403 **only on the runs that exercise the path**
(e.g. OCI push), which is easy to leave broken for weeks.

## 7. Concurrency per trigger

| Chain | concurrency |
|---|---|
| PR | `group: pr-${{ github.event.pull_request.number || github.ref }}`, `cancel-in-progress: true` |
| release (self-triggered) | usually none — pushes to main queue naturally |
| release (dispatched by another repo) | `group: release-${{ github.ref }}`, `cancel-in-progress: false` |

*Without it:* cancel-on-release throws away a half-finished run whose artifacts
the dispatching repository is waiting for, and that repository then fails with a
"tag has no assets" error that looks like its own bug. No concurrency on PRs
means every push to a busy PR keeps a full matrix alive.

## 8. Hand artifacts across jobs explicitly

`build.yml` does `upload-artifact`; the entry point's `publish` job does
`download-artifact` and publishes from the downloaded directory. A `workflow_call`
job and its caller share one run, so artifacts are visible to later jobs.

Always set `if-no-files-found: error`: the default is a *warning*, so a packaging
glitch uploads an empty artifact and surfaces two jobs later as "no assets found"
— with the real cause already scrolled away.

## 9. Job display names are public API

`name:` on a job is what branch protection calls the required check, and what a
reviewer sees on the PR. Keep them short and stable: `质量门禁`, `check`, `build`.

*Without it:* a name like `质量门禁（复用 lint.yml）` bakes an implementation
detail into a repository setting — rename the file and the required check points
at a name that no longer exists, so the PR never turns green and nobody knows why.

## 10. Filters belong on the job, not on the trigger

A workflow that only does something for certain pushes (translations) keeps the
same trigger face as its siblings and filters in `if:`:

```yaml
jobs:
  update-i18n:
    if: >-
      github.event_name == 'workflow_dispatch' ||
      contains(github.event.head_commit.message, 'Translations update from Hosted Weblate')
```

*Without it:* an ordinary push would run the job and either fail or commit
nothing. With the filter, ordinary pushes show up as **skipped** — a visible,
harmless, one-line entry instead of a red X on every delivery.

## 11. An unfinished workflow must fail loudly

A file that is not wired up yet (no token, no source of truth) gets a step that
prints the missing prerequisites and `exit 1`, plus a comment at the top of the
file. Never a body that no-ops successfully.

*Without it:* the skeleton runs green, everyone assumes i18n is being updated,
and the first real translation never lands.

## 12. Script stdout is an interface

A script whose output is consumed by `$GITHUB_OUTPUT` prints **only** `k=v` on
stdout; progress and diagnostics go to stderr, and the caller extracts values
(`sed -n 's/^key=//p'`) instead of dumping the whole capture into the file.

*Without it:* the step dies with `Unable to process file command 'output'
successfully` / `Value cannot be null. (Parameter 'name')`. This cannot be
reproduced with a local harness — locally there is no `$GITHUB_OUTPUT` parser —
so assert *stdout purity* in the harness instead (see gotchas).

## 13. Verify locally, verify the platform on CI

Static verification is free and catches most mistakes before a 10-minute matrix:
YAML parse, trigger-face assertions, `bash -n` on every `run:` block, `uses:`
targets exist, and *running* the pure-logic steps (version computation) in a
throwaway git repo with a fake `$GITHUB_OUTPUT`.

What a harness cannot cover — platform behaviour (installers, code signing,
cross-compilation, PE/Mach-O branches) — is exactly what CI is for. Say so
explicitly in the PR description instead of implying the harness proved it.
