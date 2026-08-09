# Workflows

## Add a New Language

1. `assets/bundles/{code}.json` — copy `en.json`, translate values (keep header keys).
   For a **variant** of an existing language (e.g. `zh-Hant`), copy the base file
   (`zh.json`) and only override keys that differ. Set `langCode` to the **full**
   locale code (`zh-Hant`, not `zh`). Missing keys fall back per the `fallback`
   tree in `assets/.i18n_config/i18n.yml` (recursive; default: variant → base → en).
2. `assets/docs/{code}.json` — copy `en.json`, translate all fields. Set
   `langCode` to the **base** language code (`zh-Hant` → `zh`); the unique
   code is the **file name** (`zh-Hant.json` → `zh-Hant`), which drives
   `docs/{code}/` paths and the language links.
3. App-side locale registry:
   - add the locale to the supported-locales list (use script variants for e.g. `zh-Hant`);
   - add/update the UI key set if any key changed.
4. (Optional) To make this language the repo-root README, set `root_lang` in
   `assets/.i18n_config/i18n.yml` (e.g. `root_lang: zh`). Default stays `en`.
5. Push — CI detects `BUNDLES_HASH`/`DOCS_HASH` changes and regenerates
   `docs/i18n.md` + `docs/{code}/README.md` automatically. To force regeneration
   without content changes, include `b-doc` in the commit message.

## Update an Existing Translation

1. Edit the value in `assets/bundles/{code}.json` (app UI) or
   `assets/docs/{code}.json` (README text).
2. Push. CI regenerates automatically (hash mismatch). No manual doc edits.

## Change the Root README Language

1. Edit `assets/.i18n_config/i18n.yml`, set `root_lang` to the desired locale.
2. Push — `TEMPLATES_HASH` changes (config is folded into it), so CI re-renders
   all READMEs: the new root language becomes `README.md`, every locale
   (including the new one and `en`) gets its `docs/{code}/README.md`.
