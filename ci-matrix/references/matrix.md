# The matrix: one contract per file

Notation: `call` = reusable workflow invoked with `uses: ./.github/workflows/<f>.yml`.

## Call graph

```
        push: main ─┐                     pull_request ─┐
                   ▼                                    ▼
             ┌───────────┐                        ┌──────────┐
             │release.yml│                        │  pr.yml  │
             └─────┬─────┘                        └────┬─────┘
        prep ──┬───┴───┬── publish                    ├── call lint.yml
               │       │                              └── call build.yml (pack_zip: false)
       call lint.yml   call build.yml (pack_zip: true)
               │             │
               └── gate ─────┴── artifact ──► download in `publish`
```

`clear.yml` and `update_i18n.yml` hang off the side: manual (and, for i18n, a
filtered push), no relation to the release chain.

## Per-file contract

| | `lint.yml` | `build.yml` | `release.yml` | `pr.yml` | `clear.yml` | `update_i18n.yml` |
|---|---|---|---|---|---|---|
| `on:` | `workflow_call`, `workflow_dispatch` | `workflow_call` | `push: main`, `workflow_dispatch` | `pull_request: branches:[main]`, `workflow_dispatch` | `workflow_dispatch` | `push: main`, `workflow_dispatch` |
| job-level `permissions` | `contents: read` (caller side) | `contents: read` (+ `packages: write` if it pushes images) | `prep`: read; `publish`: `contents: write` | `contents: read` | `contents: write` | `contents: write` |
| `concurrency` | none | none | none (or queue, see below) | group by PR number, `cancel-in-progress: true` | none | none |
| produces | check results only | artifacts | a Release + tag | check results only | (deletes Releases) | a commit + push |
| may not | run on its own | write tags/Releases | contain a build command | pack artifacts that get published | touch stable releases | run for ordinary pushes |

**Reusable means reusable.** `lint.yml` / `build.yml` must not appear on any
`push` or `pull_request`: they are entered only through `workflow_call`. That is
what lets the same gate sit on the release path *and* on the PR path without the
two runs racing each other.

## "Where does this new step go?"

| The step… | goes in |
|---|---|
| is a lint / format / typecheck / test command | `lint.yml` |
| compiles or packages the project | `build.yml` |
| computes a version, tag, or the target matrix | `release.yml`'s `prep` job |
| creates a tag, edits release notes, publishes | `release.yml`'s `publish` job |
| decides *whether* to build at all (paths filter, channel choice) | the caller's `on:` / `prep` |
| only makes sense for PRs | `pr.yml` (and add a `pack_*`-style switch if it also lives in `build.yml`) |
| deletes old releases | `clear.yml` |
| fetches or regenerates translations and commits them | `update_i18n.yml` |

## Variations seen in practice

- **A repo with nothing to gate.** `lint.yml` is still worth keeping: the moment
  a test exists, it belongs in exactly one place. Until then the file is three
  lines of `run:` and costs nothing.
- **A repo with no i18n yet.** Keep `update_i18n.yml` as an inert skeleton with
  a hard guard (see `examples/workflows/update_i18n.yml`). Do **not** ship a
  body that silently does nothing — the first real run must tell you it is not
  wired up yet.
- **A repo with several build products** (desktop + Android + container image).
  One `build.yml`, several jobs inside it, each with its own matrix and its own
  `upload-artifact` name; `release.yml` downloads all of them in `publish`. Do
  not create `build-desktop.yml` / `build-android.yml` — the trigger face would
  be identical, which is the definition of one file.
- **A repo whose release is dispatched by a sibling repo.** Add
  `concurrency: {group: release-${{ github.ref }}, cancel-in-progress: false}` to
  `release.yml`: two dispatches must queue, never cancel — cancelling throws away
  a half-finished run whose artifacts the dispatcher is waiting for.
- **Matrix dimension added later** (a second Windows toolchain, a new ABI).
  Expand it in `prep` and pass the resulting JSON array as an input; `build.yml`
  only does `matrix: include: ${{ fromJson(inputs.targets) }}`. Product names
  derived from the target stay derived — never re-derive them in `build.yml`.

## Cross-repo alignment

When several repositories ship together, keep the **file set, file names, job
display names and trigger faces** identical across them. A reviewer who knows one
repo then already knows the others, and tooling written against one repo's
structure (verifiers, dispatch scripts, `uses:` paths) transfers unchanged.

Differences that are *fine*: the commands inside `lint.yml`, the runner labels,
the number of jobs in `build.yml`, whether `pr.yml` also builds.
