# i18n Config (`assets/.i18n_config/i18n.yml`)

The i18n pipeline is driven by an **independent config file**, separate from the
CI workflow, so the root README language is configurable without touching CI.

```yaml
# Repository i18n & docs configuration
root_lang: en
```

## `root_lang`

- The language whose README is **also** generated at the repo root (`README.md`).
- Defaults to `en` if the key is missing.
- All languages — including `root_lang` — are always rendered under
  `docs/{code}/README.md`, so **`docs/en/` is never omitted**, even when `en` is
  the root language.
- Changing `root_lang` changes the hash (`TEMPLATES_HASH` covers
  `assets/.i18n_config/`) and forces full regeneration.

## How CI reads it

```bash
ROOT_LANG=$(awk -F: '/^[[:space:]]*root_lang[[:space:]]*:/{gsub(/[[:space:]"]/,"",$2); print $2; exit}' assets/.i18n_config/i18n.yml 2>/dev/null)
ROOT_LANG=${ROOT_LANG:-en}
```

- `awk` splits on `:`, strips whitespace/quotes from the value, and prints the
  first match; missing file/key falls back to `en`.
- The config is folded into `TEMPLATES_HASH`, so any change to it re-triggers
  both i18n status and README regeneration (see [ci-pipeline.md](ci-pipeline.md)).
