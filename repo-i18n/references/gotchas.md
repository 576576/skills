# Gotchas & Rules

- **Never hand-edit generated outputs** (`README.md`, `docs/*/README.md`,
  `docs/i18n.md`) — they are overwritten by CI.
- **Never omit `docs/en/`** — every locale (en included) always gets
  `docs/{code}/README.md`; the root `README.md` is only a root-view copy of
  `root_lang`. Deleting `docs/en/README.md` breaks i18n links and doc counts.
- Never delete `docs/i18n.md`'s hash footer — it is the previous-state marker
  used by hash-check. If it's missing, hashes compare against empty and CI
  regenerates everything once.
- `_`-prefixed keys are comments in bundles — don't translate them, don't count them.
- Fallback follows `assets/.i18n_config/i18n.yml`'s `fallback` tree when it has
  content (default: variant → base → en). The tree is **recursive** — a hop's
  own chain continues after it. Keep the tree consistent with the locales you
  actually ship — a chain pointing to a missing locale is skipped.
- Keep `assets/bundles`, `assets/docs`, `assets/templates`, and the app's
  locale/key registry in sync — adding a key in the app code without the JSON
  files breaks the app's fallback (returns the raw key).
- `sort -r` gives the language ordering in `docs/i18n.md` (zh-Hant, zh, ja, fr, en).
- sed separator choice: template contains `/`, `#`, `|` — prefer `s#...#...#` and
  escape `&` inside replacements (`\&`).
- Coverage is computed against the **English** bundle (`assets/bundles/en.json`);
  keep it the most complete.
- The `b-doc` keyword and `TEMPLATES_HASH` changes (including
  `assets/.i18n_config/`) force both i18n **and** docs regeneration
  (docs README depends on templates).
- When generating the docs view from the root view (or vice versa), remember:
  language switcher uses `href="..."` (not `](...)`), while body links use `](...)`.
  Convert `href="docs/{c}/README.md"` ↔ `href="../{c}/README.md"` and
  `](docs/` ↔ `](../docs/` separately.
