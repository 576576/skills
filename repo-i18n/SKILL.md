---
name: repo-i18n
description: >-
  Manage repository multi-language documentation (README + i18n status page)
  for repos that keep translations in JSON. Covers the assets folder
  layout (bundles/docs/templates),
  the independent i18n config (assets/.i18n_config/i18n.yml → root_lang + fallback tree), the JSON
  translation schemas, the CI regeneration pipeline (hash-check → i18n job → commit
  job), and step-by-step workflows to add/update a language or change the root
  README language. Use when adding/updating translations, adding a language,
  touching assets/templates or assets/.i18n_config, or debugging the i18n/docs CI jobs.
  Detailed guides live under references/, and a ready-to-copy en+zh+zh-Hant layout
  under examples/.
---

# Repository i18n & Docs Skill

The repo keeps **app UI strings** and **generated README/i18n docs** in JSON files
under `assets/`, and CI renders them from Markdown templates with `{{placeholders}}`.

## Skill layout

```
repo-i18n/
├── SKILL.md                    # this entry point
├── scripts/
│   └── keyops.py               # add/ren/del/check keys across locales
├── references/
│   ├── folder-layout.md        # input/output folders + preset structure + app runtime
│   ├── i18n-config.md          # assets/.i18n_config/i18n.yml (root_lang, fallback)
│   ├── json-schemas.md         # bundle + docs JSON schemas
│   ├── templates.md            # placeholders + example README (root vs docs view)
│   ├── ci-pipeline.md          # hash-check → i18n job → commit job → build
│   ├── workflows.md            # add / update / change root language
│   └── gotchas.md              # pitfalls & rules
└── examples/
    ├── README.md               # example index
    └── folder-structure/       # ready-to-copy en+zh+zh-Hant repo layout
        ├── .github/workflows/  # i18n.yml workflow + render_i18n.py (colocated)
        ├── assets/             # .i18n_config / bundles / docs / templates
        └── docs/               # {code}/README.md + i18n.md + BUILD.md
```

## Quick start

1. **Folder layout** — read [references/folder-layout.md](references/folder-layout.md);
   copy [examples/folder-structure/](examples/folder-structure/) as a baseline
   (it includes the CI workflow `i18n.yml` and the render script, colocated
   under `.github/workflows/`).
2. **Config** — set the root README language (and optional `fallback` tree) via
   [references/i18n-config.md](references/i18n-config.md)
   (`assets/.i18n_config/i18n.yml`, `root_lang` default `en`).
3. **Schemas** — follow [references/json-schemas.md](references/json-schemas.md)
   when adding/editing `assets/bundles/*.json` or `assets/docs/*.json`.
4. **Templates** — see [references/templates.md](references/templates.md) for
   placeholders and the root-view vs docs-view link rules.
5. **CI** — understand regeneration in
   [references/ci-pipeline.md](references/ci-pipeline.md).
6. **Workflows** — add/update languages or change the root language per
   [references/workflows.md](references/workflows.md); always mind
   [references/gotchas.md](references/gotchas.md).

## Key operations — `scripts/keyops.py`

When you add, rename, or remove a translation key, keep every locale's JSON in
sync with one command instead of hand-editing each file. **Prefer the script;
manual model edits are only a final fallback.**

```bash
python3 scripts/keyops.py add   assets/bundles/en.json  newKey   "English value"  --after settings
python3 scripts/keyops.py ren   assets/bundles/en.json  oldKey   newKey
python3 scripts/keyops.py del   assets/bundles/en.json  oldKey
python3 scripts/keyops.py check assets/bundles/en.json
```

- `add <json> <key> [value] [--after KEY | --before KEY]` — adds the key to
  **every** locale file in the same folder; the named file gets `value`
  (default `""`), the others get `""` as a to-translate placeholder. Use
  `--after KEY` / `--before KEY` to place the new key next to an anchor key
  (default: append at the end; a missing anchor appends with a warning).
- `ren <json> <old> <new>` — renames the key in every locale file, keeping its
  position.
- `del <json> <key>` — removes the key from every locale file.
- `check [json]` — compares each locale's non-`_` key set against the target
  (usually `en.json`) and reports missing/extra keys.

Use it on either `assets/bundles/*.json` or `assets/docs/*.json`. Keys starting
with `_` are comments — `add` only touches the file you name for those, and
`check` ignores them. After key ops, translate the placeholders, run `check`,
then push (CI regenerates `docs/i18n.md` and the READMEs).

## Key facts

- Root README language is configurable via `assets/.i18n_config/i18n.yml`
  (`root_lang`, default `en`, plus the optional `fallback` tree); CI reads it.
- **Every locale — including `en` — always gets `docs/{code}/README.md`.**
  `docs/en/` is never omitted, even when `en` is the root language.
- The root `README.md` is a root-view copy of the `root_lang` README.
- CI regenerates docs only when content hashes change (`b-doc` in the commit
  message forces regeneration).
