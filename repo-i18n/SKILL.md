---
name: repo-i18n
description: >-
  Manage repository multi-language documentation (README + i18n status page)
  for FlCroc-style repos. Covers the assets folder layout (bundles/docs/templates),
  the independent i18n config (assets/.i18n_config/i18n.yml → root_lang), the JSON
  translation schemas, the CI regeneration pipeline (hash-check → i18n job → commit
  job), and step-by-step workflows to add/update a language or change the root
  README language. Use when adding/updating translations, adding a language,
  touching assets/templates or assets/.i18n_config, or debugging the i18n/docs CI jobs.
  Detailed guides live under references/, and a ready-to-copy en+zh layout under examples/.
---

# Repository i18n & Docs Skill

FlCroc keeps **app UI strings** and **generated README/i18n docs** in JSON files
under `assets/`, and CI renders them from Markdown templates with `{{placeholders}}`.

## Skill layout

```
repo-i18n/
├── SKILL.md                    # this entry point
├── references/
│   ├── folder-layout.md        # input/output folders + preset structure + app runtime
│   ├── i18n-config.md          # assets/.i18n_config/i18n.yml (root_lang)
│   ├── json-schemas.md         # bundle + docs JSON schemas
│   ├── templates.md            # placeholders + example README (root vs docs view)
│   ├── ci-pipeline.md          # hash-check → i18n job → commit job → build
│   ├── workflows.md            # add / update / change root language
│   └── gotchas.md              # pitfalls & rules
└── examples/
    ├── README.md               # example index
    └── folder-structure/       # ready-to-copy minimal en+zh repo layout
```

## Quick start

1. **Folder layout** — read [references/folder-layout.md](references/folder-layout.md);
   copy [examples/folder-structure/](examples/folder-structure/) as a baseline.
2. **Config** — set the root README language via
   [references/i18n-config.md](references/i18n-config.md)
   (`assets/.i18n_config/i18n.yml`, `root_lang`, default `en`).
3. **Schemas** — follow [references/json-schemas.md](references/json-schemas.md)
   when adding/editing `assets/bundles/*.json` or `assets/docs/*.json`.
4. **Templates** — see [references/templates.md](references/templates.md) for
   placeholders and the root-view vs docs-view link rules.
5. **CI** — understand regeneration in
   [references/ci-pipeline.md](references/ci-pipeline.md).
6. **Workflows** — add/update languages or change the root language per
   [references/workflows.md](references/workflows.md); always mind
   [references/gotchas.md](references/gotchas.md).

## Key facts

- Root README language is configurable via `assets/.i18n_config/i18n.yml`
  (`root_lang`, default `en`); CI reads it.
- **Every locale — including `en` — always gets `docs/{code}/README.md`.**
  `docs/en/` is never omitted, even when `en` is the root language.
- The root `README.md` is a root-view copy of the `root_lang` README.
- CI regenerates docs only when content hashes change (`b-doc` in the commit
  message forces regeneration).
