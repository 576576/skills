# Templates & Example README

## Placeholders

`assets/templates/README.md` uses `{{token}}` placeholders, e.g.:
`{{icon_prefix}}`, `{{languages}}`, `{{title}}`, `{{version}}`, `{{platforms}}`,
`{{license}}`, `{{tagline_block}}`, `{{heading_*}}`, `{{feat_*}}`, `{{building}}`,
`{{arch_*}}`, `{{stack_*}}`, `{{i18n}}`, `{{ack_*}}`.

`assets/templates/i18n.md` uses: `{{title}}`, `{{date}}`, `{{rows}}`,
`{{bundles_hash}}`, `{{docs_hash}}`, `{{templates_hash}}`.

## Example README (template excerpt)

```markdown
<p align="center">
  <img src="{{icon_prefix}}assets/images/icon.png" width="64" alt="{{title}}">
</p>

<h1 align="center">{{title}}</h1>

<p align="center">
{{languages}}
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-{{platforms}}-blue" alt="Platform">
  <img alt="version" src="https://img.shields.io/badge/version-{{version}}-informational" />
</p>

<em>{{tagline_block}}</em>

---

## {{heading_features}}

| {{heading_features}} |
|---|
| {{feat_feature1}} |
...
```

## Example generated README (root view, `root_lang: en`)

```markdown
<p align="center">
  <img src="assets/images/icon.png" width="64" alt="YourApp">
</p>

<h1 align="center">YourApp</h1>

<p align="center">
<a href="docs/zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; <a href="docs/ja/README.md">日本語</a> &nbsp;|&nbsp; English
</p>
...
```

> The **same content** in `docs/en/README.md` uses the **docs view**: language
> links become `../zh/README.md`, the icon becomes `../../assets/images/icon.png`,
> and body doc links become `](../docs/...` instead of `](docs/...`.

## Root view vs docs view

| Element | Root view (`README.md`) | Docs view (`docs/{code}/README.md`) |
|---------|------------------------|-------------------------------------|
| Language links | `docs/{code}/README.md` | `../{code}/README.md` |
| Icon prefix | `assets/...` | `../../assets/...` |
| Doc link prefix (`DOC_PREFIX`) | `docs/` | `../` |
