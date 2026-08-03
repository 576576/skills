# Folder Layout

## Input (source of truth — hand-maintained)

| Path | Purpose |
|------|---------|
| `assets/.i18n_config/i18n.yml` | **Independent i18n config** — defines which language's README is generated at the repo root (`root_lang`, default `en`). |
| `assets/bundles/{code}.json` | App UI strings (loaded at runtime by the app). One per locale. |
| `assets/docs/{code}.json` | README content for one locale. One per locale. |
| `assets/templates/README.md` | README template with `{{placeholder}}` tokens. |
| `assets/templates/i18n.md` | i18n status page template (`{{date}}`, `{{rows}}`, hash tokens). |

Supported locales (must stay in sync everywhere): `en`, `zh`, `zh-Hant`, `ja`, `fr`.

## Output (CI-generated — never hand-edit)

| Path | Source |
|------|--------|
| `README.md` | Rendered from `assets/templates/README.md` + `assets/docs/{root_lang}.json` |
| `docs/{code}/README.md` | Rendered README for **every** locale — **including the root language**. `docs/en/` is never omitted even when `en` is the root language. |
| `docs/i18n.md` | Language coverage table + hash footer |
| `docs/BUILD.md` | Hand-maintained build doc (not generated) |

## Preset folder structure (en + zh + zh-Hant)

A ready-to-copy example lives in [`../examples/folder-structure/`](../examples/folder-structure/).

```
repo/
├── README.md                        # ← root README (language = root_lang, default en)
├── assets/
│   ├── .i18n_config/
│   │   └── i18n.yml                 # ← root_lang: en
│   ├── bundles/
│   │   ├── en.json                  # App UI translations (English)
│   │   ├── zh.json                  # App UI translations (中文 简体)
│   │   └── zh-Hant.json             # zh script variant (中文 繁體)
│   ├── docs/
│   │   ├── en.json                  # README content (English)
│   │   ├── zh.json                  # README content (中文 简体)
│   │   └── zh-Hant.json             # README content (中文 繁體)
│   └── templates/
│       ├── README.md                # {{placeholder}} template
│       └── i18n.md                  # i18n status template
└── docs/
    ├── en/README.md                 # ← en docs (NEVER omitted, even as root lang)
    ├── zh/README.md                 # ← zh docs
    ├── zh-Hant/README.md            # ← zh-Hant docs
    ├── i18n.md                      # ← status page with hash footer
    └── BUILD.md                     # hand-maintained
```

## App-side runtime

- The app's locale registry (e.g. `supportedLocales`) must list every locale.
- Locale code = `languageCode` or `languageCode-scriptCode` (e.g. `zh-Hant`).
- Loads `assets/bundles/{code}.json`; keys starting with `_` are ignored
  (comments/headers). A variant locale (`zh-Hant`) is **merged over its base**
  (`zh`): `{...base, ...variant}` — missing keys fall back to base, then to
  `en`. An optional `fallback` tree in `assets/.i18n_config/i18n.yml`
  overrides this default (see [i18n-config.md](i18n-config.md)).
- The app's UI key set must contain every key used.
