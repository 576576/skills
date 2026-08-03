# Examples

## `folder-structure/`

A ready-to-copy, minimal repo layout with **two languages** (`en` + `zh`) that
demonstrates every piece of the i18n system:

```
folder-structure/
├── README.md                        # root README (en, root view — root_lang)
├── assets/
│   ├── .i18n_config/i18n.yml        # root_lang: en
│   ├── bundles/en.json, zh.json     # app UI strings
│   ├── docs/en.json, zh.json        # README content
│   └── templates/README.md, i18n.md # {{placeholder}} templates
└── docs/
    ├── en/README.md                 # en docs (docs view — NEVER omitted)
    ├── zh/README.md                 # zh docs (docs view)
    ├── i18n.md                      # status page + hash footer
    └── BUILD.md                     # hand-maintained
```

Use it as a baseline when setting up a new repo, or as a reference when
debugging link/view differences:

- Root `README.md` links to `docs/zh/README.md` (root view).
- `docs/en/README.md` links to `../zh/README.md` (docs view).
- `docs/zh/README.md` links to `../en/README.md` (docs view), current lang plain text.
- `docs/i18n.md` links every locale to `{code}/README.md`.
