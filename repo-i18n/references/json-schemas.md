# JSON Schemas

## Bundle (`assets/bundles/{code}.json`) — app UI strings

```json
{
  "lang": "English",              // display name
  "langCode": "en",               // locale code
  "langRegion": "United States",  // region / script label
  "langRegionCode": ["US", "GB"], // BCP-47 region/script tags

  "_comment_common": "── Common ──",   // "_" prefix = comment, ignored
  "appName": "YourApp",
  ...
}
```

Rules:

- Keys starting with `_` are ignored by the app and by CI coverage counting.
- `lang`, `langCode`, `langRegion`, `langRegionCode` are the 4 header keys
  (CI uses `HEADER_KEYS=4` when computing real translation counts).
- **Variant files (`zh-Hant`) only need keys that differ** from their base
  language (`zh`) — missing keys fall back at runtime and in coverage math.
  Default fallback is `variant → base → en`; an optional `fallback` tree in
  `assets/.i18n_config/i18n.yml` overrides it (see
  [i18n-config.md](i18n-config.md)).
- `langCode` must be the **full locale code** of the bundle (e.g. `zh-Hant`,
  not `zh`) — CI uses it for the i18n table `CODE` column and the
  `docs/{code}/` link target (bundles must distinguish `zh` from `zh-Hant`).

## Docs (`assets/docs/{code}.json`) — README content

Top-level keys: `lang`, `langCode`, `langRegion`, `langRegionCode`, `platforms`,
`license`, `title`, `headings`, `descriptions`, `features`, `archTree`. Nested
fields map to dot-path `{{placeholder}}`s (e.g. `headings.block1`,
`features.title.0`, `archTree.dir1.1`).

- Docs `langCode` is the **base language code** (e.g. `zh-Hant` → `zh`); the
  script uses the **file name** as the unique code (`zh-Hant.json` →
  `zh-Hant`), which drives `docs/{code}/` paths and the language links.
  Variants are distinguished by `langRegionCode` (e.g. `Hant`).

```json
{
  "_comment_meta": "── Meta ──",
  "lang": "English",
  "langCode": "en",
  "langRegion": "United States",
  "langRegionCode": ["US", "GB"],
  "platforms": ["Windows", "Linux", "Android"],  // platform badge list ({{platforms}})
  "license": "LicenseName",                       // license badge + section ({{license}})
  "title": "AppName",

  "headings": { "block1": "Block1Heading", "block2": "Block2Heading",
                "block3": "Block3Heading", "license": "License" },
  "descriptions": { "desc1": "Description1" },
  "features": { "title": ["title1", "title2"],
                "feat1": ["feat1", "desc1"], "feat2": ["feat2", "desc2"] },
  "archTree": { "title": "folderTitle", "dir1": ["dir1", "desc1"],
                "dir2": ["dir2", "desc2"] }
}
```
