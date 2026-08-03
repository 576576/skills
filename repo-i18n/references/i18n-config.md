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

## `fallback` (optional) — fallback tree

Defines how missing translation keys are resolved, **overriding the default
fallback behavior**. It is only read when the key is present **and non-empty**.

### Default behavior (no `fallback`)

- A **variant** locale (e.g. `zh-Hant`) falls back to its **base** locale (`zh`,
  the code before the first `-`), then to `en`.
- Any other locale falls back to `en`; `en` itself never falls back.

### Overriding with a fallback tree

The `fallback` key stays in place but its entries are **commented out by
default**, so the default behavior applies; uncomment the entries to enable:

```yaml
root_lang: en

fallback:
  # zh-Hant: [zh, en]   # variant falls back to zh, then en
  # zh: [en]            # zh falls back to en
  # en: []              # empty chain = no fallback
```

When enabled:

- Key = locale code; value = **ordered** list of locale codes to fall back to
  (first listed = highest priority).
- **Listed** locales use their configured chain instead of the default;
  **unlisted** locales keep the default behavior.
- An empty chain (`en: []`) means "no fallback".
- **Fallback is recursive**: after a locale's own chain is exhausted, each hop
  contributes its own (configured or default) chain — e.g. `zh-Hant: [zh]`
  with `zh: [en]` resolves to `zh → en`. Cycles are broken and every locale is
  visited at most once.

### How it's used

- **Runtime (app)**: a missing key walks the chain and returns the first hit.
- **Coverage (CI)**: a locale's effective key set = its own keys ∪ every key
  along its chain, so variants with few keys still report full coverage.
- Changing the tree changes `TEMPLATES_HASH` (the config is folded into it), so
  CI re-renders the i18n table and READMEs.

## How CI reads it

```bash
ROOT_LANG=$(awk -F: '/^[[:space:]]*root_lang[[:space:]]*:/{gsub(/[[:space:]"]/,"",$2); print $2; exit}' assets/.i18n_config/i18n.yml 2>/dev/null)
ROOT_LANG=${ROOT_LANG:-en}
```

- `awk` splits on `:`, strips whitespace/quotes from the value, and prints the
  first match; missing file/key falls back to `en`.
- The config is folded into `TEMPLATES_HASH`, so any change to it re-triggers
  both i18n status and README regeneration (see [ci-pipeline.md](ci-pipeline.md)).
