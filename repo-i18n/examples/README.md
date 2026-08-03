# Examples

## `folder-structure/`

A ready-to-copy, minimal repo layout with **three languages** (`en` + `zh` +
`zh-Hant`, a script **variant** of `zh`) that demonstrates every piece of the
i18n system:

```
folder-structure/
├── README.md                          # root README (en, root view — root_lang)
├── assets/
│   ├── .i18n_config/i18n.yml          # root_lang: en
│   ├── bundles/                       # app UI strings: en.json, zh.json, zh-Hant.json
│   ├── docs/                          # README content: en.json, zh.json, zh-Hant.json
│   └── templates/README.md, i18n.md   # {{placeholder}} templates
└── docs/
    ├── en/README.md                   # en docs (docs view — NEVER omitted)
    ├── zh/README.md                   # zh docs (docs view)
    ├── zh-Hant/README.md              # zh-Hant docs (docs view — variant of zh)
    ├── i18n.md                        # status page + hash footer
    └── BUILD.md                       # hand-maintained
```

Use it as a baseline when setting up a new repo, or as a reference when
debugging link/view differences:

- Root `README.md` links to `docs/zh-Hant/README.md` and `docs/zh/README.md`
  (root view).
- `docs/en/README.md` links to `../zh-Hant/README.md` and `../zh/README.md`
  (docs view).
- `docs/zh/README.md` links to `../zh-Hant/README.md` (docs view), current lang
  plain text.
- `docs/zh-Hant/README.md` links to `../zh/README.md` (docs view), current lang
  plain text.
- `docs/i18n.md` links every locale to `{code}/README.md` (e.g.
  `zh-Hant/README.md`).
