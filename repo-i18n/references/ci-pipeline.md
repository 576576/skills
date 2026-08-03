# CI Pipeline (`build.yml`)

A ready-to-copy version ships with the example at
`../examples/folder-structure/.github/workflows/i18n.yml`, with the render
script `render_i18n.py` colocated in the same folder.

```
prebuild (hash-check) → i18n job → commit job → build-* jobs
```

## Step A — prebuild: "Check i18n & docs changes"

Compute short hashes (first 8 chars of SHA256 over **all files sorted**):

- `BUNDLES_HASH`   = `find assets/bundles -name '*.json' | sha256sum`
- `DOCS_HASH`      = `find assets/docs   -name '*.json' | sha256sum`
- `TEMPLATES_HASH` = `find assets/templates assets/.i18n_config | sha256sum`
  (covers templates **and** the i18n config — config changes force regeneration)

- Commit message containing `b-doc` → force both (`do_i18n=true`, `do_docs=true`).
- Otherwise read the previous hashes from the `docs/i18n.md` footer
  (`grep 'bundles:' | tail -1 | awk '{print $2}'`) and compare:

| Change | do_i18n | do_docs |
|--------|:-------:|:-------:|
| `TEMPLATES_HASH` changed | ✅ | ✅ (treated like `b-doc`) |
| `BUNDLES_HASH` changed | ✅ | — |
| `DOCS_HASH` changed | ✅ | ✅ |

Outputs: `i18n_do`, `docs_do`, `bundles_hash`, `docs_hash`, `templates_hash`.

## Step B — i18n job (runs if `i18n_do` or `docs_do` is true)

### Generate i18n status (when `i18n_do == 'true'`) → `assets/templates/i18n.md` → `docs/i18n.md`

- `HEADER_KEYS=4`; `ACTUAL = total non-underscore keys − 4`.
- For each bundle sorted with `sort -r` (reverse alphabetical):
  - `KEYS = total non-underscore keys − 4`; `PCT = 100 * KEYS / ACTUAL` (capped at 100).
  - Doc count: files under `docs/{code}/` for **every** locale (en included).
  - `📄` marker if `assets/docs/{code}.json` exists.
  - Row: `| [LANG](LINK) | \`CODE\` | REGION | KEYS/ACTUAL (PCT%) | DOCS📄 |`.
  - Link: `{code}/README.md` for **all** locales (en → `en/README.md`, because
    `docs/en/` always exists).
- `sed` replaces `{{date}}`, `{{rows}}`, and the three hash tokens.
- Upload artifact `i18n-md` → `docs/i18n.md`.

### Generate READMEs (when `docs_do == 'true'`) for every `assets/docs/*.json`

- Read `root_lang` from `assets/.i18n_config/i18n.yml` (default `en`).
- A `render_readme DATA LANG OUTPUT ROOT_VIEW` shell function renders one README:
  - `ROOT_VIEW=false` → `docs/{code}/README.md` (docs view);
  - `ROOT_VIEW=true` → root `README.md` (root view), only for `root_lang`.
- Every locale gets `docs/{code}/README.md`; the root language additionally gets
  the root `README.md`. **`docs/en/` is always produced.**
- View differences handled by the function (see [templates.md](templates.md)).
- Language switch bar: for a language label shared by multiple variants
  (e.g. `中文` in both `zh` and `zh-Hant`), append `(region)` — `label="label (region)"`.
- Extract every field with `jq -r '.key'`, then `sed` replace each `{{token}}`.
- ⚠️ `{{languages}}` HTML must be escaped: `sed 's/&/\\&/g'` before substitution
  (raw `&` in sed replacement is treated as the whole match).
- Upload artifact `readme-md` → `README.md` + `docs/*/README.md`.

## Step C — commit job (depends on prebuild + test)

- Applies version bump to the project version file (e.g. `pubspec.yaml`,
  `package.json`) from the `new_build` output.
- Downloads `i18n-md` and/or `readme-md` artifacts.
- Commit message: `Auto commit by Github Actions` + lines like
  `- Update i18n.` / `- Update documents.` / `- Update build number N.`, suffixed `[skip ci]`.
- `git pull --rebase` before push.
- Uploads a `version-synced` artifact (updated version file) for build jobs to
  download, so they use the bumped version.

## Step D — build jobs

- `actions/download-artifact@v4` the `version-synced` artifact → ensures builds
  use the latest version.
