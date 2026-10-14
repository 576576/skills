# Gotchas

Traps that do not announce themselves. Each one either passes silently or fails
far from its cause.

## Silent: the run is green but nothing was verified

- **A skipped workflow/job has no conclusion.** With `paths-ignore` on
  `pull_request`, the check never appears; a required check then blocks the PR
  forever. Same for a job gated by `if:` — "skipped" is not "success".
- **"Green" on a PR you have never seen run.** Workflows on a PR from a first-time
  contributor wait for maintainer approval; the run's conclusion is
  `action_required`. Locally running the same commands proves nothing about CI.
- **The gate ran, but not on *this* code.** If the gate is only reachable from the
  release chain, PR feedback is always absent — you learn about a broken gate
  after merge, on the run that also publishes.
- **Fork PRs have no secrets.** A reusable gate that reads a secret silently gets
  an empty value on fork PRs (some tools then skip work instead of failing).

## Silent: checks disappear

- **Renaming a job renames the required check.** Branch protection stores the job
  display name as a string. Rename `质量门禁（复用 lint.yml）` to `质量门禁` and the
  setting now points at a name that no longer exists: the PR shows a *missing*
  check, not a failing one.
- **`uses:` typo.** `uses: ./.github/workflows/lintx.yml` is accepted by the YAML
  and by every linter; it fails at the moment the caller is triggered.
- **Branch protection is not in the repository.** Required checks, "require
  branches to be up to date", and fork-approval policy live in GitHub settings.
  A workflow change can therefore *break* a required check without touching the
  workflow's logic.

## `$GITHUB_OUTPUT`

- The file accepts **only** `key=value` (or the `key<<DELIM` heredoc form). Writing
  a captured multi-line blob into it kills the step with:

  ```
  Unable to process file command 'output' successfully.
  Value cannot be null. (Parameter 'name')
  ```

  Keep the producing script's stdout pure (`k=v` only), send progress to stderr,
  and have the caller extract with `sed -n 's/^key=//p'`.
- **This cannot be caught by a local harness** — locally there is no parser for
  that file, so extra lines look harmless. Assert *stdout purity* in the harness:
  every line must match `^(key)=|^::`.
- Values only exist after the step has run: a later step reading a never-written
  output gets an empty string, not an error.

## Trigger faces

- **`workflow_dispatch` inputs do not exist on `push`.** `${{ github.event.inputs.channel }}`
  is an empty string there. Branch on the event (`github.event_name`) and set the
  auto-path values explicitly, or use `|| 'default'` deliberately — never let the
  auto path read a dispatch input.
- **`push: branches: [main]` does not fire for tags.** A workflow that creates a
  tag needs `contents: write` and a checkout with `fetch-depth: 0` (a shallow
  clone has no local tags, so anything that deletes a local tag fails).
- **`paths-ignore` needs both `*.md` and `**/*.md`.** Whether `**/` matches zero
  directory levels is implementation-defined; listing both covers the root file.
- **`paths` is a whitelist, `paths-ignore` is a blacklist.** Writing `paths` when
  you meant "skip these" silently stops building everything except the listed
  paths — and no run will ever be red.
- **An empty matrix is an error**, not a no-op: guard with
  `if: inputs.targets != '[]'` and pass `[]` deliberately for "no targets".
- **`matrix` defaults to `fail-fast: true`**: the first failing leg cancels the
  rest, so a round of CI tells you about one failure instead of all of them.

## `${{ }}` substitution

- Expressions inside `run:` are **textual** substitution, including in comments —
  a comment mentioning `${{ secrets.X }}` gets the value substituted into the
  script (and into the logs). Write expressions as prose in comments.
- Expression output is injected into the shell *before* the shell parses it:
  `"${{ github.event.inputs.x }}"` with a value containing `"` or `$(...)` is an
  injection point. Prefer `env:` + `"$VAR"`.

## Local-tooling traps (Windows)

- **`python3` may be the Microsoft Store alias.** `command -v python3` →
  `…/AppData/Local/Microsoft/WindowsApps/python3`: piping a script into it gives
  **no output and exit code 49**. Any harness whose `run:` block shells out to
  `python3` then fails in every scenario at once, looking like a workflow bug.
  Put a real interpreter (or a shim) earlier on `PATH` and say so in the docs.
- **Text-mode writes convert line endings.** Python's `open(path, "w")` on Windows
  writes CRLF, so a scripted edit turns LF files into CRLF in the working tree.
  With `.gitattributes: * text eol=lf` the committed blob stays LF, but `git
  status` shows the file as modified (stale stat cache) until a `git add`/`git
  diff` refreshes it, and every later diff is noisy. Write bytes, or
  `open(..., newline="\n")`.
- **Never run two writers on one file in parallel.** Concurrent edits to the same
  file lose one of them while both report success. Same for editing a file while
  a background harness is running against it.

## Release plumbing

- **`gh release delete --cleanup-tag` needs a git repository** (it deletes the
  local tag too). Without `actions/checkout` every deletion fails, with an
  unhelpful error; check `git rev-parse --git-dir` first and fail early.
- **Delete oldest-first.** If the loop dies halfway, the newest releases must be
  the ones still present.
- **A publish job that assumes the artifact exists** turns a packaging warning
  into a late, confusing error. `if-no-files-found: error` on the upload keeps
  the cause next to the effect.
- **Action major versions change semantics** (artifact actions became immutable,
  upload layouts changed). Pin the major and re-read the changelog on bump —
  a bump is a behaviour change, not housekeeping.
