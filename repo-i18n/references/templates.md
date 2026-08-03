# Templates & Example README

## Placeholders

`assets/templates/README.md` uses `{{token}}` placeholders:

- **Special**: `{{icon_prefix}}`, `{{languages}}`, `{{title}}`,
  `{{platforms}}` (badge, URL-encoded), `{{license}}` (badge + section text).
- **Dot paths**: `{{headings.block1}}`, `{{descriptions.desc1}}`,
  `{{features.title.0}}`, `{{features.feat1.1}}`, `{{archTree.dir1.0}}`, ... —
  a dot walks a nested dict, a trailing index addresses a list element.

The leading icon is **not** part of the template — the render script prepends
`<p align="center"><img src="...assets/images/icon.png" width="64" ...></p>`
only when `assets/images/icon.png` exists.

`assets/templates/i18n.md` uses: `{{title}}`, `{{date}}`, `{{rows}}`,
`{{bundles_hash}}`, `{{docs_hash}}`, `{{templates_hash}}`.

## Example README (template excerpt)

```markdown
<h1 align="center">{{title}}</h1>

<p align="center">
{{languages}}
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-{{platforms}}-blue" alt="Platform">
  <img src="https://img.shields.io/badge/license-{{license}}-green" alt="License">
</p>

---

## {{headings.block1}}

{{descriptions.desc1}}

## {{headings.block2}}

 {{features.title.0}} | {{features.title.1}}
 --- | ---
 {{features.feat1.0}} | {{features.feat1.1}}
 {{features.feat2.0}} | {{features.feat2.1}}

---

## {{headings.block3}}

```text
{{archTree.title}}/
├── {{archTree.dir1.0}}/               {{archTree.dir1.1}}
└── {{archTree.dir2.0}}/               {{archTree.dir2.1}}
```

## {{headings.license}}

{{license}} © {{title}} Contributors
```

## Example generated README (root view, `root_lang: en`)

```markdown
<h1 align="center">AppName</h1>

<p align="center">
<a href="docs/zh/README.md">中文 (简体)</a> &nbsp;|&nbsp; <a href="docs/zh-Hant/README.md">中文 (繁體)</a> &nbsp;|&nbsp; English
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
