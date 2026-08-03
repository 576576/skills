# JSON Schemas

## Bundle (`assets/bundles/{code}.json`) — app UI strings

```json
{
  "lang": "English",              // display name
  "langCode": "en",               // locale code
  "langRegion": "United States",  // region / script label
  "langRegionCode": ["US", "GB"], // BCP-47 region/script tags

  "_comment_common": "── Common ──",   // "_" prefix = comment, ignored
  "appName": "FlCroc",
  ...
}
```

Rules:

- Keys starting with `_` are ignored by the app and by CI coverage counting.
- `lang`, `langCode`, `langRegion`, `langRegionCode` are the 4 header keys
  (CI uses `HEADER_KEYS=4` when computing real translation counts).
- **Variant files (`zh-Hant`) only need keys that differ** from their base
  language (`zh`) — missing keys fall back at runtime and in coverage math.
- `langCode` must be the **full locale code** of the file (e.g. `zh-Hant`, not
  `zh`) — CI uses it for the i18n table `CODE` column and the `docs/{code}/`
  link target.

## Docs (`assets/docs/{code}.json`) — README content

Top-level keys: `lang`, `langCode`, `langRegion`, `langRegionCode`, `title`,
`tagline_block`, `feat_table`, `headings`, `building`, `arch_tree`, `stack_tree`,
`i18n`, `ack_tree`. Each maps 1:1 to a `{{placeholder}}` in the README template.

```json
{
  "_comment_meta": "── Meta ──",
  "lang": "English",
  "langCode": "en",
  "langRegion": "United States",
  "langRegionCode": ["US", "GB"],
  "title": "FlCroc",
  "tagline_block": "A Flutter GUI for croc — ...",

  "feat_table": { "platform": "...", "encryption": "...", "i18n": "...", "theme": "..." },
  "headings": { "features": "Features", "build": "Build", "architecture": "Architecture",
                "stack": "Tech Stack", "i18n": "I18n", "acknowledgments": "Acknowledgments",
                "license": "License" },
  "building": "See [BUILD.md](docs/BUILD.md) ...",
  "arch_tree": { "lib": "...", "go_bridge": "...", "submodules": "...", "assets": "...", "ci": "..." },
  "stack_tree": { "col_layer": "...", "col_tech": "...", "l_ui": "...", "l_state": "...",
                  "l_backend": "...", "l_i18n": "...", "l_ci": "...", "ui": "...",
                  "state": "...", "backend": "...", "i18n": "...", "ci": "..." },
  "i18n": "See [docs/i18n.md](docs/i18n.md) ...",
  "ack_tree": { "col_project": "...", "col_desc": "...", "croc": "...", "flutter": "...",
                "flclash": "...", "crocapp": "..." }
}
```
