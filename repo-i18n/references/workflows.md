# Workflows

## Add a New Language

1. `assets/bundles/{code}.json` — copy `en.json`, translate values (keep header keys).
   For a **variant** of an existing language (e.g. `zh-Hant`), copy the base file
   (`zh.json`) and only override keys that differ. Set `langCode` to the **full**
   locale code (`zh-Hant`, not `zh`).
2. `assets/docs/{code}.json` — copy `en.json`, translate all fields.
3. `lib/l10n/app_localizations.dart`:
   - add to `supportedLocales` (use `Locale.fromSubtags` for script variants);
   - add/update `allKeys` if any key changed.
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
